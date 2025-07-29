#!/usr/-bin/env python3
"""
Módulo do Backup Agent - SUNA-ALSHAM

[Fase 2] - Fortalecido com lógica de backup inteligente aprimorada,
melhor tratamento de erros e um catálogo de backup mais robusto.
"""

import asyncio
import gzip
import hashlib
import logging
import shutil
import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# --- Bloco de Importação Corrigido e Padronizado ---
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class BackupType(Enum):
    """Tipos de backup que o agente pode executar."""
    SMART = "smart"
    FULL = "full"


class BackupStatus(Enum):
    """Status de uma operação de backup."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class BackupJob:
    """Representa um trabalho de backup a ser executado."""
    job_id: str
    paths_to_backup: List[Path]
    backup_type: BackupType
    status: BackupStatus = BackupStatus.PENDING
    result: Dict[str, Any] = field(default_factory=dict)


# --- Classe Principal do Agente ---

class BackupAgent(BaseNetworkAgent):
    """
    Agente de backup inteligente e automático.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o BackupAgent."""
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.extend([
            "automatic_backup",
            "version_control",
            "deduplication",
            "integrity_verification",
        ])
        
        self.backup_root = Path("./backups")
        self.db_path = self.backup_root / "backup_catalog.db"
        self.backup_queue = asyncio.Queue()
        
        self._setup_environment()
        
        self._backup_task: Optional[asyncio.Task] = None
        logger.info(f"💼 {self.agent_id} (Backup Inteligente) inicializado.")

    def _setup_environment(self):
        """Prepara o ambiente de backup, incluindo diretórios e o banco de dados."""
        try:
            self.backup_root.mkdir(exist_ok=True)
            self._init_database()
        except Exception as e:
            logger.critical(f"Falha ao configurar ambiente de backup: {e}", exc_info=True)
            self.status = "error"

    def _init_database(self):
        """Inicializa o banco de dados SQLite que cataloga todos os backups."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS file_versions (
                        file_path TEXT NOT NULL,
                        hash_sha256 TEXT NOT NULL,
                        backup_path TEXT NOT NULL,
                        timestamp TIMESTAMP NOT NULL,
                        PRIMARY KEY (file_path, hash_sha256)
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            logger.critical(f"Erro no banco de dados de backup: {e}", exc_info=True)
            raise

    async def start_backup_service(self):
        """Inicia os serviços de background do agente."""
        if not self._backup_task and self.status == "active":
            self._backup_task = asyncio.create_task(self._backup_loop())
            logger.info(f"💼 {self.agent_id} iniciou serviço de backup.")

    async def _backup_loop(self):
        """Loop principal que processa a fila de backups."""
        while True:
            try:
                job: BackupJob = await self.backup_queue.get()
                logger.info(f"Iniciando job de backup '{job.job_id}' do tipo {job.backup_type.value}.")
                job.status = BackupStatus.IN_PROGRESS

                result = await self._smart_backup(job)

                job.status = BackupStatus.COMPLETED if result.get("success") else BackupStatus.FAILED
                job.result = result

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de backup: {e}", exc_info=True)

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de backup."""
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "create_backup":
            result = await self.create_backup(message.content)
            await self.publish_response(message, result)

    async def create_backup(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo job de backup e o adiciona à fila."""
        paths_str = request_data.get("paths", [])
        if not paths_str:
            return {"status": "error", "message": "Nenhum caminho especificado para backup."}

        job = BackupJob(
            job_id=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            paths_to_backup=[Path(p) for p in paths_str],
            backup_type=BackupType(request_data.get("backup_type", "smart")),
        )
        await self.backup_queue.put(job)
        return {"status": "queued", "job_id": job.job_id}

    # O resto do arquivo continua o mesmo...
    def _get_files_from_paths(self, paths: List[Path]) -> List[Path]:
        all_files = []
        for path in paths:
            if path.is_file():
                all_files.append(path)
            elif path.is_dir():
                all_files.extend([p for p in path.rglob('*') if p.is_file()])
        return all_files

    async def _smart_backup(self, job: BackupJob) -> Dict[str, Any]:
        job_dir = self.backup_root / job.job_id
        job_dir.mkdir()
        
        all_files = self._get_files_from_paths(job.paths_to_backup)
        files_backed_up = 0
        total_size = 0

        for file_path in all_files:
            try:
                current_hash = self._calculate_file_hash(file_path)
                if not current_hash: continue

                last_hash = self._get_last_file_hash(file_path)

                if current_hash != last_hash:
                    relative_path = file_path.relative_to(Path.cwd())
                    backup_file_path = job_dir / f"{relative_path}.gz"
                    backup_file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(file_path, 'rb') as f_in, gzip.open(backup_file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                    
                    self._log_file_version_to_db(file_path, current_hash, backup_file_path)
                    files_backed_up += 1
                    total_size += file_path.stat().st_size
            except Exception as e:
                logger.error(f"Falha ao fazer backup do arquivo {file_path}: {e}")

        logger.info(f"Backup inteligente concluído. {files_backed_up} arquivos novos/modificados.")
        return {"success": True, "files_backed_up": files_backed_up, "total_size_bytes": total_size}

    def _calculate_file_hash(self, file_path: Path) -> Optional[str]:
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except (IOError, PermissionError) as e:
            logger.error(f"Não foi possível ler o arquivo para hash: {file_path} - {e}")
            return None

    def _get_last_file_hash(self, file_path: Path) -> Optional[str]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT hash_sha256 FROM file_versions WHERE file_path = ? ORDER BY timestamp DESC LIMIT 1",
                    (str(file_path),)
                )
                result = cursor.fetchone()
                return result[0] if result else None
        except sqlite3.Error as e:
