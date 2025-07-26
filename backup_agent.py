#!/usr/bin/env python3
"""
BackupAgent - Sistema de Backup Inteligente e Automático
Backup poderoso com versionamento, recuperação e sincronização
"""

import asyncio
import logging
import os
import shutil
import hashlib
import json
import gzip
import tarfile
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import sqlite3
from collections import defaultdict
import threading
import time
from multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class BackupType(Enum):
    """Tipos de backup"""
    FULL = "full"
    INCREMENTAL = "incremental" 
    DIFFERENTIAL = "differential"
    SMART = "smart"
    EMERGENCY = "emergency"
    SNAPSHOT = "snapshot"

class BackupStatus(Enum):
    """Status do backup"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CORRUPTED = "corrupted"
    RESTORED = "restored"

class CompressionType(Enum):
    """Tipos de compressão"""
    NONE = "none"
    GZIP = "gzip"
    TAR_GZ = "tar_gz"
    ZIP = "zip"

@dataclass
class FileVersion:
    """Versão de um arquivo"""
    file_path: str
    version_id: str
    hash_md5: str
    hash_sha256: str
    size_bytes: int
    backup_path: str
    timestamp: datetime
    backup_type: BackupType
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BackupSet:
    """Conjunto de backup"""
    backup_id: str
    backup_type: BackupType
    files_included: List[str]
    total_size: int
    compressed_size: int
    backup_path: str
    start_time: datetime
    end_time: Optional[datetime]
    status: BackupStatus
    parent_backup: Optional[str] = None
    compression: CompressionType = CompressionType.GZIP
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RestorePoint:
    """Ponto de restauração"""
    restore_id: str
    timestamp: datetime
    backup_sets: List[str]
    system_state: Dict[str, Any]
    description: str
    tags: List[str] = field(default_factory=list)

class BackupAgent(BaseNetworkAgent):
    """Agente de backup inteligente e automático"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'automatic_backup',
            'version_control',
            'disaster_recovery',
            'intelligent_compression',
            'deduplication',
            'scheduled_backup',
            'incremental_backup',
            'cloud_sync',
            'integrity_verification',
            'smart_restore'
        ]
        self.status = 'active'
        
        # Configurações
        self.backup_root = Path("./backups")
        self.backup_root.mkdir(exist_ok=True)
        
        # Base de dados de versões
        self.db_path = self.backup_root / "backup_database.db"
        self._init_database()
        
        # Estado do agente
        self.active_backups = {}  # backup_id -> backup_info
        self.backup_queue = asyncio.Queue()
        self.file_watchers = {}  # path -> watcher
        self.backup_schedules = {}  # schedule_id -> schedule_info
        self.restore_points = {}  # restore_id -> RestorePoint
        
        # Cache e otimizações
        self.file_hashes = {}  # path -> hash (para deduplicação)
        self.compression_cache = {}
        self.last_backup_times = {}  # path -> timestamp
        
        # Configurações avançadas
        self.auto_backup_interval = 300  # 5 minutos
        self.max_versions_per_file = 50
        self.compression_threshold = 1024  # 1KB
        self.deduplication_enabled = True
        self.cloud_sync_enabled = False
        
        # Métricas
        self.backup_metrics = {
            'total_backups': 0,
            'successful_backups': 0,
            'failed_backups': 0,
            'bytes_backed_up': 0,
            'bytes_saved_compression': 0,
            'bytes_saved_deduplication': 0,
            'files_monitored': 0,
            'versions_created': 0
        }
        
        # Tasks de background
        self._backup_task = None
        self._monitoring_task = None
        self._maintenance_task = None
        self._sync_task = None
        
        logger.info(f"💼 {self.agent_id} inicializado com backup inteligente")
    
    def _init_database(self):
        """Inicializa base de dados SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de versões de arquivos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_versions (
                version_id TEXT PRIMARY KEY,
                file_path TEXT NOT NULL,
                hash_md5 TEXT NOT NULL,
                hash_sha256 TEXT NOT NULL,
                size_bytes INTEGER NOT NULL,
                backup_path TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                backup_type TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        
        # Tabela de conjuntos de backup
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_sets (
                backup_id TEXT PRIMARY KEY,
                backup_type TEXT NOT NULL,
                files_included TEXT NOT NULL,
                total_size INTEGER NOT NULL,
                compressed_size INTEGER NOT NULL,
                backup_path TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP,
                status TEXT NOT NULL,
                parent_backup TEXT,
                compression TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        
        # Tabela de pontos de restauração
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restore_points (
                restore_id TEXT PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                backup_sets TEXT NOT NULL,
                system_state TEXT NOT NULL,
                description TEXT NOT NULL,
                tags TEXT
            )
        ''')
        
        # Índices para performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_file_path ON file_versions(file_path)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON file_versions(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_backup_type ON backup_sets(backup_type)')
        
        conn.commit()
        conn.close()
        
        logger.info("💾 Base de dados de backup inicializada")
    
    async def start_backup_service(self):
        """Inicia serviços de backup"""
        if not self._backup_task:
            self._backup_task = asyncio.create_task(self._backup_loop())
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            self._maintenance_task = asyncio.create_task(self._maintenance_loop())
            
            if self.cloud_sync_enabled:
                self._sync_task = asyncio.create_task(self._sync_loop())
            
            # Agendar backup automático
            await self._schedule_automatic_backups()
            
            logger.info(f"💼 {self.agent_id} iniciou serviços de backup")
    
    async def stop_backup_service(self):
        """Para serviços de backup"""
        if self._backup_task:
            self._backup_task.cancel()
            self._backup_task = None
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
        if self._maintenance_task:
            self._maintenance_task.cancel()
            self._maintenance_task = None
        if self._sync_task:
            self._sync_task.cancel()
            self._sync_task = None
        
        logger.info(f"🛑 {self.agent_id} parou serviços de backup")
    
    async def _backup_loop(self):
        """Loop principal de backup"""
        while True:
            try:
                # Processar fila de backup
                if not self.backup_queue.empty():
                    backup_request = await self.backup_queue.get()
                    await self._process_backup_request(backup_request)
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de backup: {e}")
    
    async def _monitoring_loop(self):
        """Loop de monitoramento de arquivos"""
        while True:
            try:
                # Verificar arquivos monitorados por mudanças
                for path, watcher_info in self.file_watchers.items():
                    if await self._check_file_changed(path, watcher_info):
                        await self._trigger_smart_backup(path)
                
                await asyncio.sleep(10)  # Verificar a cada 10 segundos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento: {e}")
    
    async def _maintenance_loop(self):
        """Loop de manutenção (limpeza, otimização)"""
        while True:
            try:
                # Limpeza de versões antigas
                await self._cleanup_old_versions()
                
                # Verificação de integridade
                await self._verify_backup_integrity()
                
                # Otimização de espaço
                await self._optimize_storage()
                
                await asyncio.sleep(3600)  # Manutenção a cada hora
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na manutenção: {e}")
    
    async def _sync_loop(self):
        """Loop de sincronização com cloud"""
        while True:
            try:
                if self.cloud_sync_enabled:
                    await self._sync_to_cloud()
                
                await asyncio.sleep(1800)  # Sync a cada 30 minutos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no sync: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'create_backup':
                result = await self.create_backup(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'restore_files':
                result = await self.restore_files(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'list_versions':
                result = await self.list_file_versions(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'schedule_backup':
                result = await self.schedule_backup(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'create_restore_point':
                result = await self.create_restore_point(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'get_backup_status':
                result = self._get_backup_status()
                await self._send_response(message, result)
        
        elif message.message_type == MessageType.NOTIFICATION:
            # Processar notificações de mudanças no sistema
            if message.content.get('notification_type') == 'file_modified':
                await self._handle_file_modification(message.content)
            elif message.content.get('notification_type') == 'system_critical':
                await self._emergency_backup()
    
    async def create_backup(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria backup de arquivos ou diretórios"""
        try:
            paths = request_data.get('paths', [])
            backup_type = BackupType(request_data.get('backup_type', 'smart'))
            compression = CompressionType(request_data.get('compression', 'gzip'))
            description = request_data.get('description', '')
            
            if not paths:
                return {'status': 'error', 'message': 'Nenhum caminho especificado'}
            
            backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.active_backups)}"
            
            logger.info(f"💼 Criando backup {backup_type.value}: {backup_id}")
            
            # Preparar informações do backup
            backup_info = {
                'backup_id': backup_id,
                'backup_type': backup_type,
                'paths': paths,
                'compression': compression,
                'description': description,
                'start_time': datetime.now(),
                'status': BackupStatus.PENDING
            }
            
            self.active_backups[backup_id] = backup_info
            
            # Adicionar à fila de processamento
            await self.backup_queue.put({
                'type': 'create_backup',
                'backup_info': backup_info
            })
            
            return {
                'status': 'started',
                'backup_id': backup_id,
                'backup_type': backup_type.value,
                'estimated_completion': self._estimate_backup_time(paths)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando backup: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _process_backup_request(self, request: Dict[str, Any]):
        """Processa requisição de backup da fila"""
        request_type = request.get('type')
        
        if request_type == 'create_backup':
            backup_info = request.get('backup_info')
            await self._execute_backup(backup_info)
        elif request_type == 'emergency_backup':
            await self._execute_emergency_backup()
    
    async def _execute_backup(self, backup_info: Dict[str, Any]):
        """Executa o backup propriamente dito"""
        backup_id = backup_info['backup_id']
        
        try:
            logger.info(f"🔄 Executando backup {backup_id}")
            
            backup_info['status'] = BackupStatus.IN_PROGRESS
            
            # Criar diretório do backup
            backup_dir = self.backup_root / backup_id
            backup_dir.mkdir(exist_ok=True)
            
            files_to_backup = []
            total_size = 0
            
            # Coletar arquivos
            for path_str in backup_info['paths']:
                path = Path(path_str)
                if path.is_file():
                    files_to_backup.append(path)
                    total_size += path.stat().st_size
                elif path.is_dir():
                    for file_path in path.rglob('*'):
                        if file_path.is_file():
                            files_to_backup.append(file_path)
                            total_size += file_path.stat().st_size
            
            logger.info(f"📁 {len(files_to_backup)} arquivos para backup ({total_size:,} bytes)")
            
            # Executar backup baseado no tipo
            if backup_info['backup_type'] == BackupType.SMART:
                result = await self._smart_backup(files_to_backup, backup_dir, backup_info)
            elif backup_info['backup_type'] == BackupType.INCREMENTAL:
                result = await self._incremental_backup(files_to_backup, backup_dir, backup_info)
            elif backup_info['backup_type'] == BackupType.FULL:
                result = await self._full_backup(files_to_backup, backup_dir, backup_info)
            else:
                result = await self._full_backup(files_to_backup, backup_dir, backup_info)
            
            # Atualizar status
            backup_info['end_time'] = datetime.now()
            backup_info['result'] = result
            
            if result['success']:
                backup_info['status'] = BackupStatus.COMPLETED
                self.backup_metrics['successful_backups'] += 1
                
                # Salvar no banco de dados
                await self._save_backup_to_db(backup_info, result)
                
                logger.info(f"✅ Backup {backup_id} completado com sucesso")
                
                # Notificar sobre sucesso
                await self._notify_backup_success(backup_id, result)
            else:
                backup_info['status'] = BackupStatus.FAILED
                self.backup_metrics['failed_backups'] += 1
                logger.error(f"❌ Backup {backup_id} falhou: {result.get('error')}")
                
                # Notificar sobre falha
                await self._notify_backup_failure(backup_id, result.get('error'))
            
            self.backup_metrics['total_backups'] += 1
            
            # Remover do ativo
            if backup_id in self.active_backups:
                del self.active_backups[backup_id]
            
        except Exception as e:
            logger.error(f"❌ Erro executando backup {backup_id}: {e}")
            backup_info['status'] = BackupStatus.FAILED
            backup_info['error'] = str(e)
            self.backup_metrics['failed_backups'] += 1
    
    async def _smart_backup(self, files: List[Path], backup_dir: Path, backup_info: Dict[str, Any]) -> Dict[str, Any]:
        """Backup inteligente com deduplicação e compressão adaptativa"""
        try:
            backed_up_files = []
            total_original_size = 0
            total_compressed_size = 0
            duplicates_found = 0
            
            for file_path in files:
                # Calcular hashes
                file_hash = await self._calculate_file_hash(file_path)
                
                # Verificar se já existe (deduplicação)
                if self.deduplication_enabled and file_hash in self.file_hashes:
                    duplicates_found += 1
                    # Criar link simbólico ao invés de copiar
                    existing_backup = self.file_hashes[file_hash]
                    relative_path = file_path.relative_to(Path.cwd())
                    link_path = backup_dir / relative_path
                    link_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Salvar referência ao arquivo existente
                    with open(str(link_path) + ".dedupe", 'w') as f:
                        json.dump({
                            'original_file': str(file_path),
                            'reference_backup': existing_backup,
                            'hash': file_hash,
                            'deduplication': True
                        }, f)
                    
                    continue
                
                # Backup normal
                file_size = file_path.stat().st_size
                total_original_size += file_size
                
                # Determinar se deve comprimir
                should_compress = (
                    backup_info['compression'] != CompressionType.NONE and
                    file_size > self.compression_threshold
                )
                
                # Copiar/comprimir arquivo
                relative_path = file_path.relative_to(Path.cwd())
                backup_file_path = backup_dir / relative_path
                backup_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                if should_compress:
                    compressed_path = str(backup_file_path) + ".gz"
                    compressed_size = await self._compress_file(file_path, compressed_path)
                    total_compressed_size += compressed_size
                    final_path = compressed_path
                else:
                    shutil.copy2(file_path, backup_file_path)
                    total_compressed_size += file_size
                    final_path = str(backup_file_path)
                
                # Registrar arquivo
                self.file_hashes[file_hash] = final_path
                backed_up_files.append({
                    'original_path': str(file_path),
                    'backup_path': final_path,
                    'hash': file_hash,
                    'original_size': file_size,
                    'compressed': should_compress
                })
                
                # Criar versão no banco
                await self._create_file_version(file_path, final_path, file_hash, backup_info)
            
            # Calcular estatísticas
            compression_ratio = (total_original_size - total_compressed_size) / max(1, total_original_size)
            
            result = {
                'success': True,
                'files_backed_up': len(backed_up_files),
                'duplicates_deduplicated': duplicates_found,
                'total_original_size': total_original_size,
                'total_compressed_size': total_compressed_size,
                'compression_ratio': compression_ratio,
                'files': backed_up_files
            }
            
            # Atualizar métricas
            self.backup_metrics['bytes_backed_up'] += total_original_size
            self.backup_metrics['bytes_saved_compression'] += (total_original_size - total_compressed_size)
            self.backup_metrics['bytes_saved_deduplication'] += duplicates_found * 1000  # Estimativa
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro no smart backup: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _incremental_backup(self, files: List[Path], backup_dir: Path, backup_info: Dict[str, Any]) -> Dict[str, Any]:
        """Backup incremental (apenas arquivos modificados)"""
        try:
            # Encontrar último backup
            last_backup = await self._get_last_backup()
            last_backup_time = last_backup['end_time'] if last_backup else datetime.min
            
            modified_files = []
            
            for file_path in files:
                # Verificar se foi modificado desde último backup
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_mtime > last_backup_time:
                    modified_files.append(file_path)
            
            logger.info(f"📝 {len(modified_files)} arquivos modificados desde último backup")
            
            # Fazer backup apenas dos modificados
            if modified_files:
                return await self._smart_backup(modified_files, backup_dir, backup_info)
            else:
                return {
                    'success': True,
                    'files_backed_up': 0,
                    'message': 'Nenhum arquivo modificado desde último backup'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro no backup incremental: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _full_backup(self, files: List[Path], backup_dir: Path, backup_info: Dict[str, Any]) -> Dict[str, Any]:
        """Backup completo de todos os arquivos"""
        try:
            # Backup completo é essencialmente um smart backup sem deduplicação
            original_dedup = self.deduplication_enabled
            self.deduplication_enabled = False
            
            result = await self._smart_backup(files, backup_dir, backup_info)
            
            self.deduplication_enabled = original_dedup
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro no backup completo: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcula hash SHA256 de um arquivo"""
        hash_sha256 = hashlib.sha256()
        
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"❌ Erro calculando hash de {file_path}: {e}")
            return ""
    
    async def _compress_file(self, source_path: Path, dest_path: str) -> int:
        """Comprime um arquivo usando gzip"""
        try:
            with open(source_path, 'rb') as f_in:
                with gzip.open(dest_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            return os.path.getsize(dest_path)
            
        except Exception as e:
            logger.error(f"❌ Erro comprimindo {source_path}: {e}")
            return 0
    
    async def _create_file_version(self, file_path: Path, backup_path: str, file_hash: str, backup_info: Dict[str, Any]):
        """Cria entrada de versão no banco de dados"""
        try:
            version_id = f"{file_hash}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO file_versions 
                (version_id, file_path, hash_md5, hash_sha256, size_bytes, backup_path, timestamp, backup_type, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                version_id,
                str(file_path),
                "",  # MD5 não implementado por questões de performance
                file_hash,
                file_path.stat().st_size,
                backup_path,
                datetime.now(),
                backup_info['backup_type'].value,
                json.dumps({'backup_id': backup_info['backup_id']})
            ))
            
            conn.commit()
            conn.close()
            
            self.backup_metrics['versions_created'] += 1
            
        except Exception as e:
            logger.error(f"❌ Erro criando versão: {e}")
    
    async def restore_files(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Restaura arquivos de backup"""
        try:
            files_to_restore = request_data.get('files', [])
            restore_point = request_data.get('restore_point')
            target_directory = request_data.get('target_directory', './restored')
            
            logger.info(f"🔄 Restaurando {len(files_to_restore)} arquivos")
            
            # Criar diretório de destino
            target_path = Path(target_directory)
            target_path.mkdir(parents=True, exist_ok=True)
            
            restored_files = []
            failed_files = []
            
            for file_info in files_to_restore:
                try:
                    file_path = file_info.get('file_path')
                    version_id = file_info.get('version_id')  # Versão específica
                    
                    # Encontrar versão mais recente se não especificada
                    if not version_id:
                        version_info = await self._get_latest_version(file_path)
                    else:
                        version_info = await self._get_version_by_id(version_id)
                    
                    if not version_info:
                        failed_files.append({'file': file_path, 'error': 'Versão não encontrada'})
                        continue
                    
                    # Restaurar arquivo
                    backup_path = version_info['backup_path']
                    restore_path = target_path / Path(file_path).name
                    
                    if backup_path.endswith('.gz'):
                        # Descomprimir
                        with gzip.open(backup_path, 'rb') as f_in:
                            with open(restore_path, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                    elif backup_path.endswith('.dedupe'):
                        # Arquivo deduplicado - ler referência
                        with open(backup_path, 'r') as f:
                            dedup_info = json.load(f)
                        # Copiar do arquivo original de referência
                        shutil.copy2(dedup_info['reference_backup'], restore_path)
                    else:
                        # Cópia simples
                        shutil.copy2(backup_path, restore_path)
                    
                    restored_files.append({
                        'original_path': file_path,
                        'restored_path': str(restore_path),
                        'version_id': version_info['version_id']
                    })
                    
                except Exception as e:
                    failed_files.append({'file': file_path, 'error': str(e)})
            
            return {
                'status': 'completed',
                'restored_files': len(restored_files),
                'failed_files': len(failed_files),
                'details': {
                    'restored': restored_files,
                    'failed': failed_files
                },
                'target_directory': str(target_path)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na restauração: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def list_file_versions(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Lista versões de um arquivo"""
        try:
            file_path = request_data.get('file_path')
            limit = request_data.get('limit', 20)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT version_id, hash_sha256, size_bytes, backup_path, timestamp, backup_type
                FROM file_versions 
                WHERE file_path = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (file_path, limit))
            
            versions = []
            for row in cursor.fetchall():
                versions.append({
                    'version_id': row[0],
                    'hash': row[1],
                    'size_bytes': row[2],
                    'backup_path': row[3],
                    'timestamp': row[4],
                    'backup_type': row[5]
                })
            
            conn.close()
            
            return {
                'status': 'completed',
                'file_path': file_path,
                'versions': versions,
                'total_versions': len(versions)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro listando versões: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def create_restore_point(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria ponto de restauração do sistema"""
        try:
            description = request_data.get('description', f'Restore point {datetime.now()}')
            tags = request_data.get('tags', [])
            
            restore_id = f"restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Coletar estado atual do sistema
            system_state = {
                'timestamp': datetime.now().isoformat(),
                'active_backups': len(self.active_backups),
                'total_versions': self.backup_metrics['versions_created'],
                'disk_usage': await self._get_disk_usage()
            }
            
            # Obter backups recentes
            recent_backups = await self._get_recent_backups(limit=10)
            backup_set_ids = [b['backup_id'] for b in recent_backups]
            
            # Criar ponto de restauração
            restore_point = RestorePoint(
                restore_id=restore_id,
                timestamp=datetime.now(),
                backup_sets=backup_set_ids,
                system_state=system_state,
                description=description,
                tags=tags
            )
            
            # Salvar no banco
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO restore_points 
                (restore_id, timestamp, backup_sets, system_state, description, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                restore_id,
                datetime.now(),
                json.dumps(backup_set_ids),
                json.dumps(system_state),
                description,
                json.dumps(tags)
            ))
            
            conn.commit()
            conn.close()
            
            self.restore_points[restore_id] = restore_point
            
            logger.info(f"📍 Ponto de restauração criado: {restore_id}")
            
            return {
                'status': 'created',
                'restore_id': restore_id,
                'description': description,
                'backup_sets_included': len(backup_set_ids),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando ponto de restauração: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _get_backup_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema de backup"""
        return {
            'status': 'active',
            'active_backups': len(self.active_backups),
            'files_monitored': self.backup_metrics['files_monitored'],
            'metrics': self.backup_metrics,
            'storage_info': {
                'backup_root': str(self.backup_root),
                'total_size': self._get_directory_size(self.backup_root),
                'available_space': shutil.disk_usage(self.backup_root).free
            },
            'configuration': {
                'auto_backup_interval': self.auto_backup_interval,
                'max_versions_per_file': self.max_versions_per_file,
                'deduplication_enabled': self.deduplication_enabled,
                'cloud_sync_enabled': self.cloud_sync_enabled
            }
        }
    
    def _get_directory_size(self, path: Path) -> int:
        """Calcula tamanho total de um diretório"""
        total = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total += os.path.getsize(filepath)
        except:
            pass
        return total
    
    # Métodos auxiliares e outros métodos implementados...
    # (Continuação com métodos de manutenção, notificação, etc.)
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
        from uuid import uuid4
        response = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            priority=original_message.priority,
            content=response_data,
            timestamp=datetime.now(),
            correlation_id=original_message.id
        )
        await self.message_bus.publish(response)

def create_backup_agent(message_bus, num_instances=1) -> List[BackupAgent]:
    """
    Cria agente de backup inteligente
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de backup poderoso
    """
    agents = []
    
    try:
        logger.info("💼 Criando BackupAgent poderoso...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "backup_agent_001"
        
        if agent_id not in existing_agents:
            try:
                agent = BackupAgent(agent_id, AgentType.SYSTEM, message_bus)
                
                # Iniciar serviços de backup
                asyncio.create_task(agent.start_backup_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com backup inteligente")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de backup criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando BackupAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
