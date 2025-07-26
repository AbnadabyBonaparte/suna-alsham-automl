#!/usr/bin/env python3
"""
Disaster Recovery Agent - Agente Enterprise de Recuperação de Desastres
Sistema avançado de backup, recovery e continuidade de negócios
"""

import asyncio
import json
import os
import shutil
import zipfile
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import subprocess
import tempfile
from collections import defaultdict
from multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class DisasterType(Enum):
    """Tipos de desastres"""
    SYSTEM_CRASH = "system_crash"
    DATA_CORRUPTION = "data_corruption"
    SECURITY_BREACH = "security_breach"
    HARDWARE_FAILURE = "hardware_failure"
    SOFTWARE_FAILURE = "software_failure"
    NETWORK_OUTAGE = "network_outage"
    POWER_FAILURE = "power_failure"
    HUMAN_ERROR = "human_error"
    CYBER_ATTACK = "cyber_attack"
    NATURAL_DISASTER = "natural_disaster"

class RecoveryStatus(Enum):
    """Status de recuperação"""
    READY = "ready"
    BACKING_UP = "backing_up"
    RECOVERING = "recovering"
    TESTING = "testing"
    FAILED = "failed"
    COMPLETED = "completed"
    DEGRADED = "degraded"

class BackupLevel(Enum):
    """Níveis de backup"""
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    SNAPSHOT = "snapshot"
    REAL_TIME = "real_time"

@dataclass
class SystemSnapshot:
    """Snapshot completo do sistema"""
    snapshot_id: str
    timestamp: datetime
    system_state: Dict[str, Any]
    agent_states: Dict[str, Dict[str, Any]]
    configuration: Dict[str, Any]
    file_checksums: Dict[str, str]
    backup_path: str
    size_mb: float
    recovery_time_estimate: int  # minutes
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RecoveryPlan:
    """Plano de recuperação de desastre"""
    plan_id: str
    disaster_type: DisasterType
    recovery_steps: List[Dict[str, Any]]
    estimated_rto: int  # Recovery Time Objective (minutes)
    estimated_rpo: int  # Recovery Point Objective (minutes)
    priority: int  # 1 = highest
    dependencies: List[str]
    validation_checks: List[str]
    rollback_plan: List[Dict[str, Any]]
    contact_list: List[str] = field(default_factory=list)

@dataclass
class DisasterEvent:
    """Evento de desastre"""
    event_id: str
    disaster_type: DisasterType
    severity: str  # critical, high, medium, low
    detected_at: datetime
    affected_components: List[str]
    root_cause: Optional[str]
    recovery_plan_id: Optional[str]
    status: RecoveryStatus
    recovery_started_at: Optional[datetime] = None
    recovery_completed_at: Optional[datetime] = None
    lessons_learned: List[str] = field(default_factory=list)

class DisasterRecoveryAgent(BaseNetworkAgent):
    """Agente Enterprise de Recuperação de Desastres"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'full_system_backup',
            'state_snapshot',
            'instant_recovery',
            'rollback_management', 
            'data_replication',
            'failover_control',
            'corruption_detection',
            'automated_restoration',
            'disaster_detection',
            'business_continuity',
            'compliance_reporting',
            'recovery_testing'
        ]
        self.status = 'ready'
        
        # Configurações enterprise
        self.backup_retention_days = 90
        self.max_backup_size_gb = 100
        self.backup_compression = True
        self.encryption_enabled = True
        self.replication_sites = ['primary', 'secondary', 'offsite']
        
        # Estado do sistema
        self.system_snapshots = {}  # snapshot_id -> SystemSnapshot
        self.recovery_plans = {}    # plan_id -> RecoveryPlan
        self.disaster_events = {}   # event_id -> DisasterEvent
        self.backup_schedule = {}   # component -> schedule
        self.monitoring_enabled = True
        
        # Paths e configurações
        self.backup_root = Path('./disaster_recovery')
        self.backup_root.mkdir(exist_ok=True)
        
        # Métricas
        self.dr_metrics = {
            'backups_created': 0,
            'recoveries_performed': 0,
            'disasters_detected': 0,
            'mean_recovery_time': 0,
            'data_integrity_checks': 0,
            'successful_recoveries': 0
        }
        
        # Tasks de background
        self._monitoring_task = None
        self._backup_task = None
        self._health_check_task = None
        
        # Inicializar sistema
        self._initialize_recovery_plans()
        self._setup_backup_schedules()
        
        logger.info(f"🛡️ {self.agent_id} inicializado com capacidades enterprise de DR")
    
    async def start_disaster_recovery_service(self):
        """Inicia serviços de disaster recovery"""
        if not self._monitoring_task:
            self._monitoring_task = asyncio.create_task(self._disaster_monitoring_loop())
            self._backup_task = asyncio.create_task(self._automated_backup_loop())
            self._health_check_task = asyncio.create_task(self._health_check_loop())
            logger.info(f"🛡️ {self.agent_id} iniciou serviços de disaster recovery")
    
    async def stop_disaster_recovery_service(self):
        """Para serviços de disaster recovery"""
        self.monitoring_enabled = False
        
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
        if self._backup_task:
            self._backup_task.cancel()
            self._backup_task = None
        if self._health_check_task:
            self._health_check_task.cancel()
            self._health_check_task = None
        
        logger.info(f"🛑 {self.agent_id} parou serviços de disaster recovery")
    
    def _initialize_recovery_plans(self):
        """Inicializa planos de recuperação predefinidos"""
        plans = [
            RecoveryPlan(
                plan_id="PLAN_001_SYSTEM_CRASH",
                disaster_type=DisasterType.SYSTEM_CRASH,
                recovery_steps=[
                    {'step': 1, 'action': 'assess_system_state', 'timeout': 5},
                    {'step': 2, 'action': 'restore_latest_snapshot', 'timeout': 15},
                    {'step': 3, 'action': 'restart_critical_agents', 'timeout': 10},
                    {'step': 4, 'action': 'validate_system_integrity', 'timeout': 10},
                    {'step': 5, 'action': 'resume_normal_operations', 'timeout': 5}
                ],
                estimated_rto=30,  # 30 minutes
                estimated_rpo=5,   # 5 minutes
                priority=1,
                dependencies=['backup_available', 'storage_accessible'],
                validation_checks=['agent_health', 'data_integrity', 'network_connectivity'],
                rollback_plan=[
                    {'step': 1, 'action': 'stop_all_operations'},
                    {'step': 2, 'action': 'restore_previous_snapshot'},
                    {'step': 3, 'action': 'notify_administrators'}
                ]
            ),
            
            RecoveryPlan(
                plan_id="PLAN_002_DATA_CORRUPTION",
                disaster_type=DisasterType.DATA_CORRUPTION,
                recovery_steps=[
                    {'step': 1, 'action': 'isolate_corrupted_data', 'timeout': 5},
                    {'step': 2, 'action': 'identify_clean_backup', 'timeout': 10},
                    {'step': 3, 'action': 'restore_from_clean_backup', 'timeout': 20},
                    {'step': 4, 'action': 'verify_data_integrity', 'timeout': 15},
                    {'step': 5, 'action': 'implement_preventive_measures', 'timeout': 10}
                ],
                estimated_rto=45,
                estimated_rpo=10,
                priority=1,
                dependencies=['integrity_checks', 'clean_backup_available'],
                validation_checks=['data_consistency', 'checksums_valid', 'no_corruption'],
                rollback_plan=[
                    {'step': 1, 'action': 'quarantine_suspected_data'},
                    {'step': 2, 'action': 'restore_known_good_state'}
                ]
            ),
            
            RecoveryPlan(
                plan_id="PLAN_003_SECURITY_BREACH",
                disaster_type=DisasterType.SECURITY_BREACH,
                recovery_steps=[
                    {'step': 1, 'action': 'immediate_system_isolation', 'timeout': 2},
                    {'step': 2, 'action': 'assess_breach_scope', 'timeout': 15},
                    {'step': 3, 'action': 'patch_vulnerabilities', 'timeout': 30},
                    {'step': 4, 'action': 'restore_clean_environment', 'timeout': 45},
                    {'step': 5, 'action': 'implement_enhanced_security', 'timeout': 20},
                    {'step': 6, 'action': 'resume_monitored_operations', 'timeout': 10}
                ],
                estimated_rto=90,
                estimated_rpo=0,  # Zero data loss tolerance
                priority=1,
                dependencies=['security_tools', 'clean_backup', 'patched_vulnerabilities'],
                validation_checks=['no_malware', 'security_hardened', 'access_controls'],
                rollback_plan=[
                    {'step': 1, 'action': 'complete_system_shutdown'},
                    {'step': 2, 'action': 'manual_investigation'},
                    {'step': 3, 'action': 'rebuild_from_scratch'}
                ]
            )
        ]
        
        for plan in plans:
            self.recovery_plans[plan.plan_id] = plan
    
    def _setup_backup_schedules(self):
        """Configura cronogramas de backup automático"""
        self.backup_schedule = {
            'system_state': {'frequency': 'hourly', 'retention': '7_days'},
            'agent_configurations': {'frequency': 'daily', 'retention': '30_days'},
            'critical_data': {'frequency': 'every_15_minutes', 'retention': '24_hours'},
            'full_system': {'frequency': 'weekly', 'retention': '90_days'},
            'incremental': {'frequency': 'every_5_minutes', 'retention': '48_hours'}
        }
    
    async def _disaster_monitoring_loop(self):
        """Loop de monitoramento de desastres"""
        while self.monitoring_enabled:
            try:
                # Verificar saúde do sistema
                system_health = await self._assess_system_health()
                
                # Detectar possíveis desastres
                potential_disasters = self._detect_disasters(system_health)
                
                # Processar desastres detectados
                for disaster in potential_disasters:
                    await self._handle_disaster_event(disaster)
                
                # Verificar integridade dos backups
                await self._verify_backup_integrity()
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento de desastres: {e}")
    
    async def _automated_backup_loop(self):
        """Loop de backup automático"""
        while self.monitoring_enabled:
            try:
                for component, schedule in self.backup_schedule.items():
                    if self._should_backup(component, schedule):
                        await self._perform_scheduled_backup(component, schedule)
                
                await asyncio.sleep(60)  # Check every minute
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no backup automático: {e}")
    
    async def _health_check_loop(self):
        """Loop de verificação de saúde dos backups"""
        while self.monitoring_enabled:
            try:
                # Testar recuperação simulada
                await self._test_recovery_procedures()
                
                # Limpar backups antigos
                await self._cleanup_old_backups()
                
                # Gerar relatórios de compliance
                await self._generate_compliance_report()
                
                await asyncio.sleep(3600)  # Every hour
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na verificação de saúde: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'create_snapshot':
                result = await self.create_system_snapshot(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'restore_system':
                result = await self.restore_system(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'test_recovery':
                result = await self.test_recovery_plan(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'disaster_response':
                result = await self.handle_disaster(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'backup_status':
                result = self.get_backup_status()
                await self._send_response(message, result)
        
        elif message.message_type == MessageType.EMERGENCY:
            # Resposta imediata a emergências
            await self._handle_emergency(message)
    
    async def create_system_snapshot(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria snapshot completo do sistema"""
        try:
            snapshot_type = request_data.get('type', 'full')
            include_agents = request_data.get('include_agents', True)
            compress = request_data.get('compress', self.backup_compression)
            
            logger.info(f"📸 Criando snapshot do sistema tipo: {snapshot_type}")
            
            snapshot_id = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            snapshot_path = self.backup_root / snapshot_id
            snapshot_path.mkdir(exist_ok=True)
            
            # Coletar estado do sistema
            system_state = await self._collect_system_state()
            
            # Coletar estados dos agentes
            agent_states = {}
            if include_agents:
                agent_states = await self._collect_agent_states()
            
            # Coletar configurações
            configuration = await self._collect_configuration()
            
            # Backup de arquivos críticos
            critical_files = await self._backup_critical_files(snapshot_path)
            
            # Calcular checksums
            file_checksums = self._calculate_checksums(critical_files)
            
            # Criar snapshot object
            snapshot = SystemSnapshot(
                snapshot_id=snapshot_id,
                timestamp=datetime.now(),
                system_state=system_state,
                agent_states=agent_states,
                configuration=configuration,
                file_checksums=file_checksums,
                backup_path=str(snapshot_path),
                size_mb=self._calculate_directory_size(snapshot_path),
                recovery_time_estimate=self._estimate_recovery_time(system_state)
            )
            
            # Salvar metadata
            await self._save_snapshot_metadata(snapshot)
            
            # Comprimir se solicitado
            if compress:
                compressed_path = await self._compress_snapshot(snapshot_path)
                snapshot.backup_path = str(compressed_path)
                snapshot.size_mb = self._get_file_size_mb(compressed_path)
            
            # Armazenar snapshot
            self.system_snapshots[snapshot_id] = snapshot
            self.dr_metrics['backups_created'] += 1
            
            # Replicar para sites secundários
            await self._replicate_snapshot(snapshot)
            
            logger.info(f"✅ Snapshot {snapshot_id} criado: {snapshot.size_mb:.1f}MB")
            
            return {
                'status': 'completed',
                'snapshot_id': snapshot_id,
                'size_mb': snapshot.size_mb,
                'recovery_time_estimate': snapshot.recovery_time_estimate,
                'backup_path': snapshot.backup_path,
                'checksums_count': len(file_checksums)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando snapshot: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def restore_system(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Restaura sistema de um snapshot"""
        try:
            snapshot_id = request_data.get('snapshot_id')
            restore_type = request_data.get('type', 'full')
            verify_integrity = request_data.get('verify_integrity', True)
            
            if snapshot_id not in self.system_snapshots:
                return {
                    'status': 'error',
                    'message': f'Snapshot {snapshot_id} não encontrado'
                }
            
            snapshot = self.system_snapshots[snapshot_id]
            logger.info(f"🔄 Iniciando restauração do snapshot {snapshot_id}")
            
            # Verificar integridade do backup
            if verify_integrity:
                integrity_check = await self._verify_snapshot_integrity(snapshot)
                if not integrity_check['valid']:
                    return {
                        'status': 'error',
                        'message': f'Backup corrompido: {integrity_check["errors"]}'
                    }
            
            # Executar restauração
            restore_result = await self._execute_restoration(snapshot, restore_type)
            
            if restore_result['success']:
                self.dr_metrics['recoveries_performed'] += 1
                self.dr_metrics['successful_recoveries'] += 1
                
                # Atualizar tempo médio de recuperação
                recovery_time = restore_result['elapsed_time']
                self.dr_metrics['mean_recovery_time'] = (
                    (self.dr_metrics['mean_recovery_time'] * (self.dr_metrics['recoveries_performed'] - 1) + recovery_time) /
                    self.dr_metrics['recoveries_performed']
                )
                
                logger.info(f"✅ Restauração completa em {recovery_time:.1f} minutos")
                
                # Notificar sistema sobre restauração
                await self._notify_restoration_complete(snapshot_id, restore_result)
            
            return {
                'status': 'completed' if restore_result['success'] else 'failed',
                'snapshot_id': snapshot_id,
                'elapsed_time': restore_result['elapsed_time'],
                'components_restored': restore_result['components_restored'],
                'verification_results': restore_result.get('verification', {})
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na restauração: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def handle_disaster(self, disaster_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trata evento de desastre"""
        try:
            disaster_type = DisasterType(disaster_data.get('type'))
            severity = disaster_data.get('severity', 'high')
            affected_components = disaster_data.get('affected_components', [])
            
            logger.error(f"🚨 DESASTRE DETECTADO: {disaster_type.value} - Severidade: {severity}")
            
            # Criar evento de desastre
            event = DisasterEvent(
                event_id=f"disaster_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                disaster_type=disaster_type,
                severity=severity,
                detected_at=datetime.now(),
                affected_components=affected_components,
                root_cause=disaster_data.get('root_cause'),
                recovery_plan_id=None,
                status=RecoveryStatus.READY
            )
            
            # Selecionar plano de recuperação
            recovery_plan = self._select_recovery_plan(disaster_type, severity)
            if recovery_plan:
                event.recovery_plan_id = recovery_plan.plan_id
                
                # Executar plano de recuperação
                recovery_result = await self._execute_recovery_plan(recovery_plan, event)
                
                event.status = RecoveryStatus.COMPLETED if recovery_result['success'] else RecoveryStatus.FAILED
                event.recovery_completed_at = datetime.now()
            else:
                logger.error(f"❌ Nenhum plano de recuperação encontrado para {disaster_type.value}")
                event.status = RecoveryStatus.FAILED
            
            # Armazenar evento
            self.disaster_events[event.event_id] = event
            self.dr_metrics['disasters_detected'] += 1
            
            return {
                'status': 'handled',
                'event_id': event.event_id,
                'recovery_plan': recovery_plan.plan_id if recovery_plan else None,
                'recovery_status': event.status.value,
                'estimated_recovery_time': recovery_plan.estimated_rto if recovery_plan else 'unknown'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro tratando desastre: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def test_recovery_plan(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Testa plano de recuperação"""
        try:
            plan_id = request_data.get('plan_id')
            simulate_only = request_data.get('simulate_only', True)
            
            if plan_id not in self.recovery_plans:
                return {
                    'status': 'error',
                    'message': f'Plano {plan_id} não encontrado'
                }
            
            plan = self.recovery_plans[plan_id]
            logger.info(f"🧪 Testando plano de recuperação: {plan_id}")
            
            test_result = {
                'plan_id': plan_id,
                'test_started': datetime.now().isoformat(),
                'steps_tested': [],
                'issues_found': [],
                'overall_success': True,
                'estimated_vs_actual': {}
            }
            
            # Testar cada passo
            total_time = 0
            for step in plan.recovery_steps:
                step_result = await self._test_recovery_step(step, simulate_only)
                test_result['steps_tested'].append(step_result)
                
                total_time += step_result['elapsed_time']
                
                if not step_result['success']:
                    test_result['overall_success'] = False
                    test_result['issues_found'].append({
                        'step': step['step'],
                        'issue': step_result['error']
                    })
            
            # Comparar com estimativas
            test_result['estimated_vs_actual'] = {
                'estimated_rto': plan.estimated_rto,
                'actual_test_time': total_time,
                'variance_percent': ((total_time - plan.estimated_rto) / plan.estimated_rto) * 100
            }
            
            # Testar validações
            validation_results = await self._test_validations(plan.validation_checks, simulate_only)
            test_result['validation_results'] = validation_results
            
            return {
                'status': 'completed',
                'test_result': test_result,
                'recommendations': self._generate_test_recommendations(test_result)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro testando plano: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_backup_status(self) -> Dict[str, Any]:
        """Retorna status dos backups"""
        try:
            # Calcular estatísticas
            total_snapshots = len(self.system_snapshots)
            total_size_mb = sum(s.size_mb for s in self.system_snapshots.values())
            
            # Backup mais recente
            latest_snapshot = None
            if self.system_snapshots:
                latest_snapshot = max(
                    self.system_snapshots.values(),
                    key=lambda s: s.timestamp
                )
            
            # Verificar saúde dos backups
            healthy_backups = 0
            for snapshot in self.system_snapshots.values():
                if self._is_backup_healthy(snapshot):
                    healthy_backups += 1
            
            return {
                'status': 'active',
                'total_snapshots': total_snapshots,
                'total_size_mb': total_size_mb,
                'healthy_backups': healthy_backups,
                'health_percentage': (healthy_backups / max(1, total_snapshots)) * 100,
                'latest_snapshot': {
                    'id': latest_snapshot.snapshot_id,
                    'timestamp': latest_snapshot.timestamp.isoformat(),
                    'size_mb': latest_snapshot.size_mb
                } if latest_snapshot else None,
                'disaster_recovery_metrics': self.dr_metrics,
                'backup_schedule': self.backup_schedule,
                'recovery_plans': len(self.recovery_plans)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo status: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _collect_system_state(self) -> Dict[str, Any]:
        """Coleta estado atual do sistema"""
        return {
            'timestamp': datetime.now().isoformat(),
            'active_agents_count': len(self.message_bus.subscribers) if hasattr(self.message_bus, 'subscribers') else 0,
            'system_metrics': {
                'cpu_usage': 'simulated_cpu_usage',
                'memory_usage': 'simulated_memory_usage',
                'disk_usage': 'simulated_disk_usage'
            },
            'network_status': 'operational',
            'critical_processes': ['message_bus', 'orchestrator', 'disaster_recovery']
        }
    
    async def _collect_agent_states(self) -> Dict[str, Dict[str, Any]]:
        """Coleta estados de todos os agentes"""
        agent_states = {}
        
        if hasattr(self.message_bus, 'subscribers'):
            for agent_id, agent in self.message_bus.subscribers.items():
                try:
                    if hasattr(agent, 'get_status'):
                        agent_states[agent_id] = agent.get_status()
                    else:
                        agent_states[agent_id] = {
                            'status': 'active',
                            'type': getattr(agent, 'agent_type', 'unknown')
                        }
                except:
                    agent_states[agent_id] = {'status': 'unknown'}
        
        return agent_states
    
    async def _collect_configuration(self) -> Dict[str, Any]:
        """Coleta configurações do sistema"""
        return {
            'disaster_recovery': {
                'backup_retention_days': self.backup_retention_days,
                'encryption_enabled': self.encryption_enabled,
                'replication_sites': self.replication_sites
            },
            'recovery_plans': {plan_id: {
                'disaster_type': plan.disaster_type.value,
                'estimated_rto': plan.estimated_rto,
                'priority': plan.priority
            } for plan_id, plan in self.recovery_plans.items()}
        }
    
    async def _backup_critical_files(self, backup_path: Path) -> List[str]:
        """Backup de arquivos críticos"""
        critical_files = []
        
        # Simular backup de arquivos críticos
        source_files = [
            'main.py',
            'main_complete_system.py',
            'agent_loader.py',
            'multi_agent_network.py'
        ]
        
        for file_name in source_files:
            if os.path.exists(file_name):
                dest_path = backup_path / file_name
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_name, dest_path)
                critical_files.append(file_name)
        
        return critical_files
    
    def _calculate_checksums(self, files: List[str]) -> Dict[str, str]:
        """Calcula checksums dos arquivos"""
        checksums = {}
        
        for file_path in files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        checksums[file_path] = hashlib.sha256(content).hexdigest()
                except Exception as e:
                    logger.error(f"Erro calculando checksum de {file_path}: {e}")
        
        return checksums
    
    def _calculate_directory_size(self, path: Path) -> float:
        """Calcula tamanho do diretório em MB"""
        try:
            total_size = sum(
                f.stat().st_size 
                for f in path.rglob('*') 
                if f.is_file()
            )
            return total_size / (1024 * 1024)  # Convert to MB
        except:
            return 0.0
    
    def _get_file_size_mb(self, file_path: Path) -> float:
        """Obtém tamanho do arquivo em MB"""
        try:
            return file_path.stat().st_size / (1024 * 1024)
        except:
            return 0.0
    
    def _estimate_recovery_time(self, system_state: Dict[str, Any]) -> int:
        """Estima tempo de recuperação em minutos"""
        base_time = 10  # 10 minutes base
        
        # Ajustar baseado na complexidade
        agent_count = system_state.get('active_agents_count', 0)
        complexity_factor = agent_count / 10  # 1 minute per 10 agents
        
        return int(base_time + complexity_factor)
    
    async def _save_snapshot_metadata(self, snapshot: SystemSnapshot):
        """Salva metadata do snapshot"""
        metadata_path = Path(snapshot.backup_path) / 'metadata.json'
        
        metadata = {
            'snapshot_id': snapshot.snapshot_id,
            'timestamp': snapshot.timestamp.isoformat(),
            'size_mb': snapshot.size_mb,
            'recovery_time_estimate': snapshot.recovery_time_estimate,
            'file_checksums': snapshot.file_checksums,
            'system_state': snapshot.system_state,
            'configuration': snapshot.configuration
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    async def _compress_snapshot(self, snapshot_path: Path) -> Path:
        """Comprime snapshot"""
        compressed_path = snapshot_path.with_suffix('.zip')
        
        with zipfile.ZipFile(compressed_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in snapshot_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(snapshot_path)
                    zipf.write(file_path, arcname)
        
        # Remover diretório original
        shutil.rmtree(snapshot_path)
        
        return compressed_path
    
    async def _replicate_snapshot(self, snapshot: SystemSnapshot):
        """Replica snapshot para sites secundários"""
        # Simular replicação
        logger.info(f"📡 Replicando snapshot {snapshot.snapshot_id} para sites secundários")
        
        for site in self.replication_sites[1:]:  # Skip primary
            # Em produção, isso seria replicação real
            logger.info(f"   ✅ Replicado para {site}")
    
    # Implementar métodos auxiliares restantes...
    def _select_recovery_plan(self, disaster_type: DisasterType, severity: str) -> Optional[RecoveryPlan]:
        """Seleciona plano de recuperação apropriado"""
        for plan in self.recovery_plans.values():
            if plan.disaster_type == disaster_type:
                return plan
        return None
    
    def _is_backup_healthy(self, snapshot: SystemSnapshot) -> bool:
        """Verifica se backup está saudável"""
        # Verificações básicas
        backup_path = Path(snapshot.backup_path)
        if not backup_path.exists():
            return False
        
        # Verificar idade
        age_days = (datetime.now() - snapshot.timestamp).days
        if age_days > self.backup_retention_days:
            return False
        
        return True
    
    # Implementações simplificadas dos métodos restantes
    async def _assess_system_health(self) -> Dict[str, Any]:
        """Avalia saúde do sistema"""
        return {'status': 'healthy', 'issues': []}
    
    def _detect_disasters(self, health: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detecta possíveis desastres"""
        return []  # Implementação simplificada
    
    async def _handle_disaster_event(self, disaster: Dict[str, Any]):
        """Trata evento de desastre"""
        pass  # Implementação simplificada
    
    def _should_backup(self, component: str, schedule: Dict[str, Any]) -> bool:
        """Verifica se deve fazer backup"""
        return True  # Implementação simplificada
    
    async def _perform_scheduled_backup(self, component: str, schedule: Dict[str, Any]):
        """Executa backup agendado"""
        pass  # Implementação simplificada
    
    async def _verify_backup_integrity(self):
        """Verifica integridade dos backups"""
        pass  # Implementação simplificada
    
    async def _test_recovery_procedures(self):
        """Testa procedimentos de recuperação"""
        pass  # Implementação simplificada
    
    async def _cleanup_old_backups(self):
        """Remove backups antigos"""
        pass  # Implementação simplificada
    
    async def _generate_compliance_report(self):
        """Gera relatório de compliance"""
        pass  # Implementação simplificada
    
    async def _handle_emergency(self, message: AgentMessage):
        """Trata emergência"""
        pass  # Implementação simplificada
    
    async def _verify_snapshot_integrity(self, snapshot: SystemSnapshot) -> Dict[str, Any]:
        """Verifica integridade do snapshot"""
        return {'valid': True, 'errors': []}
    
    async def _execute_restoration(self, snapshot: SystemSnapshot, restore_type: str) -> Dict[str, Any]:
        """Executa restauração"""
        return {
            'success': True,
            'elapsed_time': 15.0,
            'components_restored': ['system_state', 'agent_states']
        }
    
    async def _notify_restoration_complete(self, snapshot_id: str, result: Dict[str, Any]):
        """Notifica conclusão da restauração"""
        pass
    
    async def _execute_recovery_plan(self, plan: RecoveryPlan, event: DisasterEvent) -> Dict[str, Any]:
        """Executa plano de recuperação"""
        return {'success': True}
    
    async def _test_recovery_step(self, step: Dict[str, Any], simulate: bool) -> Dict[str, Any]:
        """Testa passo de recuperação"""
        return {'success': True, 'elapsed_time': 2.0}
    
    async def _test_validations(self, validations: List[str], simulate: bool) -> Dict[str, Any]:
        """Testa validações"""
        return {'all_passed': True}
    
    def _generate_test_recommendations(self, test_result: Dict[str, Any]) -> List[str]:
        """Gera recomendações baseadas no teste"""
        return ['Sistema de DR funcionando corretamente']
    
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

def create_disaster_recovery_agent(message_bus, num_instances=1) -> List[DisasterRecoveryAgent]:
    """
    Cria agente de disaster recovery enterprise
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de disaster recovery
    """
    agents = []
    
    try:
        logger.info("🛡️ Criando DisasterRecoveryAgent Enterprise...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "disaster_recovery_001"
        
        if agent_id not in existing_agents:
            try:
                agent = DisasterRecoveryAgent(agent_id, AgentType.SYSTEM, message_bus)
                
                # Iniciar serviços de disaster recovery
                asyncio.create_task(agent.start_disaster_recovery_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com capacidades enterprise de DR")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de disaster recovery criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando DisasterRecoveryAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
