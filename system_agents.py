import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import psutil
import platform
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class SystemMetricType(Enum):
    """Tipos de métricas do sistema"""
    CPU = "cpu_usage"
    MEMORY = "memory_usage"
    DISK = "disk_usage"
    NETWORK = "network_usage"
    TEMPERATURE = "temperature"
    PROCESSES = "processes"
    SERVICES = "services"

class SystemStatus(Enum):
    """Status do sistema"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

class ControlAction(Enum):
    """Ações de controle do sistema"""
    RESTART_SERVICE = "restart_service"
    STOP_SERVICE = "stop_service"
    START_SERVICE = "start_service"
    ADJUST_RESOURCES = "adjust_resources"
    CLEAR_CACHE = "clear_cache"
    OPTIMIZE_MEMORY = "optimize_memory"

@dataclass
class SystemMetrics:
    """Métricas do sistema"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    active_processes: int
    status: SystemStatus
    alerts: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class RecoveryPlan:
    """Plano de recuperação"""
    issue_type: str
    severity: str
    actions: List[str]
    estimated_time: int  # minutos
    success_probability: float

class SystemMonitorAgent(BaseNetworkAgent):
    """Agente de monitoramento do sistema"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['system_monitoring', 'metrics_collection', 'alert_generation']
        self.metrics_history = []
        self.alert_thresholds = {
            'cpu': 80.0,
            'memory': 85.0,
            'disk': 90.0
        }
        self.monitoring_interval = 30  # segundos
        self._monitoring_task = None
        self._setup_monitoring_handlers()
        logger.info(f"✅ {self.agent_id} inicializado com monitoramento ativo")
    
    def _setup_monitoring_handlers(self):
        """Configura handlers de monitoramento"""
        self.monitoring_handlers = {
            'get_metrics': self._get_system_metrics,
            'check_health': self._check_system_health,
            'generate_report': self._generate_monitoring_report
        }
    
    async def start_monitoring(self):
        """Inicia monitoramento contínuo"""
        if not self._monitoring_task:
            self._monitoring_task = asyncio.create_task(self._continuous_monitoring())
            logger.info(f"📊 {self.agent_id} iniciou monitoramento contínuo")
    
    async def stop_monitoring(self):
        """Para monitoramento contínuo"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
            logger.info(f"🛑 {self.agent_id} parou monitoramento")
    
    async def _continuous_monitoring(self):
        """Loop de monitoramento contínuo"""
        while True:
            try:
                metrics = await self._collect_metrics()
                self._analyze_metrics(metrics)
                await asyncio.sleep(self.monitoring_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento: {e}")
                await asyncio.sleep(self.monitoring_interval)
    
    async def _collect_metrics(self) -> SystemMetrics:
        """Coleta métricas do sistema"""
        try:
            # Coletar métricas usando psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            process_count = len(psutil.pids())
            
            # Determinar status
            status = SystemStatus.HEALTHY
            alerts = []
            
            if cpu_percent > self.alert_thresholds['cpu']:
                status = SystemStatus.WARNING
                alerts.append({
                    'type': 'cpu_high',
                    'value': cpu_percent,
                    'threshold': self.alert_thresholds['cpu']
                })
            
            if memory.percent > self.alert_thresholds['memory']:
                if status == SystemStatus.WARNING:
                    status = SystemStatus.CRITICAL
                else:
                    status = SystemStatus.WARNING
                alerts.append({
                    'type': 'memory_high',
                    'value': memory.percent,
                    'threshold': self.alert_thresholds['memory']
                })
            
            metrics = SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                disk_percent=disk.percent,
                active_processes=process_count,
                status=status,
                alerts=alerts
            )
            
            # Armazenar no histórico (manter últimas 100 métricas)
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Erro coletando métricas: {e}")
            return SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=0.0,
                memory_percent=0.0,
                disk_percent=0.0,
                active_processes=0,
                status=SystemStatus.UNKNOWN
            )
    
    def _analyze_metrics(self, metrics: SystemMetrics):
        """Analisa métricas e gera alertas se necessário"""
        if metrics.alerts:
            logger.warning(f"⚠️ {len(metrics.alerts)} alertas detectados")
            
            # Enviar alerta para o sistema de controle
            alert_message = AgentMessage(
                id=str(uuid4()),
                sender_id=self.agent_id,
                recipient_id="control_001",  # Agente de controle
                message_type=MessageType.NOTIFICATION,
                priority=Priority.HIGH if metrics.status == SystemStatus.CRITICAL else Priority.MEDIUM,
                content={
                    'alert_type': 'system_metrics',
                    'metrics': {
                        'cpu': metrics.cpu_percent,
                        'memory': metrics.memory_percent,
                        'disk': metrics.disk_percent
                    },
                    'alerts': metrics.alerts,
                    'status': metrics.status.value
                },
                timestamp=datetime.now()
            )
            asyncio.create_task(self.message_bus.publish(alert_message))
    
    async def _get_system_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna métricas atuais do sistema"""
        try:
            metrics = await self._collect_metrics()
            
            return {
                'status': 'completed',
                'metrics': {
                    'cpu_percent': metrics.cpu_percent,
                    'memory_percent': metrics.memory_percent,
                    'disk_percent': metrics.disk_percent,
                    'active_processes': metrics.active_processes,
                    'system_status': metrics.status.value
                },
                'timestamp': metrics.timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo métricas: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _check_system_health(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica saúde geral do sistema"""
        try:
            # Análise das últimas métricas
            if not self.metrics_history:
                return {
                    'status': 'completed',
                    'health': 'unknown',
                    'message': 'Sem dados históricos'
                }
            
            recent_metrics = self.metrics_history[-10:]  # Últimas 10 métricas
            
            # Calcular médias
            avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
            
            # Determinar saúde
            health_score = 100
            issues = []
            
            if avg_cpu > 70:
                health_score -= 20
                issues.append(f"CPU alta: {avg_cpu:.1f}%")
            
            if avg_memory > 80:
                health_score -= 25
                issues.append(f"Memória alta: {avg_memory:.1f}%")
            
            # Verificar tendências
            if len(self.metrics_history) > 20:
                cpu_trend = self._calculate_trend([m.cpu_percent for m in self.metrics_history[-20:]])
                if cpu_trend > 0.5:  # Crescimento > 0.5% por medição
                    health_score -= 10
                    issues.append("CPU em tendência crescente")
            
            health_status = 'healthy' if health_score >= 80 else 'warning' if health_score >= 60 else 'critical'
            
            return {
                'status': 'completed',
                'health': health_status,
                'health_score': health_score,
                'issues': issues,
                'recommendations': self._get_health_recommendations(issues)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro verificando saúde: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calcula tendência linear simples"""
        if len(values) < 2:
            return 0.0
        
        n = len(values)
        x = list(range(n))
        
        # Cálculo simples de tendência
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _get_health_recommendations(self, issues: List[str]) -> List[str]:
        """Gera recomendações baseadas nos problemas"""
        recommendations = []
        
        if any('CPU' in issue for issue in issues):
            recommendations.append("Verificar processos consumindo CPU")
            recommendations.append("Considerar escalonamento horizontal")
        
        if any('Memória' in issue for issue in issues):
            recommendations.append("Liberar cache de memória")
            recommendations.append("Identificar vazamentos de memória")
        
        return recommendations
    
    async def _generate_monitoring_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera relatório de monitoramento"""
        try:
            period = data.get('period', 'last_hour')
            
            # Filtrar métricas pelo período
            now = datetime.now()
            if period == 'last_hour':
                start_time = now - timedelta(hours=1)
            elif period == 'last_day':
                start_time = now - timedelta(days=1)
            else:
                start_time = now - timedelta(minutes=30)
            
            relevant_metrics = [
                m for m in self.metrics_history 
                if m.timestamp >= start_time
            ]
            
            if not relevant_metrics:
                return {
                    'status': 'completed',
                    'report': 'Sem dados para o período solicitado'
                }
            
            # Calcular estatísticas
            report = {
                'status': 'completed',
                'period': period,
                'statistics': {
                    'cpu': {
                        'avg': sum(m.cpu_percent for m in relevant_metrics) / len(relevant_metrics),
                        'max': max(m.cpu_percent for m in relevant_metrics),
                        'min': min(m.cpu_percent for m in relevant_metrics)
                    },
                    'memory': {
                        'avg': sum(m.memory_percent for m in relevant_metrics) / len(relevant_metrics),
                        'max': max(m.memory_percent for m in relevant_metrics),
                        'min': min(m.memory_percent for m in relevant_metrics)
                    },
                    'alerts_count': sum(len(m.alerts) for m in relevant_metrics)
                },
                'total_measurements': len(relevant_metrics)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"❌ Erro gerando relatório: {e}")
            return {'status': 'error', 'message': str(e)}

class SystemControlAgent(BaseNetworkAgent):
    """Agente de controle do sistema"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['system_control', 'resource_management', 'service_control']
        self.control_history = []
        self.automation_rules = self._setup_automation_rules()
        self._setup_control_handlers()
        logger.info(f"✅ {self.agent_id} inicializado com controle automático")
    
    def _setup_automation_rules(self) -> Dict[str, Dict[str, Any]]:
        """Define regras de automação"""
        return {
            'high_cpu': {
                'condition': lambda metrics: metrics.get('cpu_percent', 0) > 85,
                'actions': [ControlAction.OPTIMIZE_MEMORY, ControlAction.ADJUST_RESOURCES],
                'cooldown': 300  # 5 minutos
            },
            'high_memory': {
                'condition': lambda metrics: metrics.get('memory_percent', 0) > 90,
                'actions': [ControlAction.CLEAR_CACHE, ControlAction.OPTIMIZE_MEMORY],
                'cooldown': 600  # 10 minutos
            }
        }
    
    def _setup_control_handlers(self):
        """Configura handlers de controle"""
        self.control_handlers = {
            'execute_action': self._execute_control_action,
            'adjust_resources': self._adjust_system_resources,
            'manage_service': self._manage_service
        }
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens e executa ações automáticas"""
        await super().handle_message(message)
        
        # Processar alertas do monitor
        if message.message_type == MessageType.NOTIFICATION and message.content.get('alert_type') == 'system_metrics':
            await self._process_system_alert(message)
    
    async def _process_system_alert(self, alert_message: AgentMessage):
        """Processa alertas do sistema e executa ações automáticas"""
        try:
            metrics = alert_message.content.get('metrics', {})
            
            # Verificar regras de automação
            for rule_name, rule in self.automation_rules.items():
                if rule['condition'](metrics):
                    logger.info(f"🎯 Regra '{rule_name}' ativada")
                    
                    # Verificar cooldown
                    last_execution = self._get_last_execution(rule_name)
                    if last_execution and (datetime.now() - last_execution).seconds < rule['cooldown']:
                        logger.info(f"⏳ Regra '{rule_name}' em cooldown")
                        continue
                    
                    # Executar ações
                    for action in rule['actions']:
                        await self._execute_control_action({
                            'action': action.value,
                            'reason': f'Automação: {rule_name}',
                            'metrics': metrics
                        })
                    
                    # Registrar execução
                    self.control_history.append({
                        'timestamp': datetime.now(),
                        'rule': rule_name,
                        'actions': [a.value for a in rule['actions']],
                        'metrics': metrics
                    })
            
        except Exception as e:
            logger.error(f"❌ Erro processando alerta: {e}")
    
    def _get_last_execution(self, rule_name: str) -> Optional[datetime]:
        """Obtém última execução de uma regra"""
        for entry in reversed(self.control_history):
            if entry.get('rule') == rule_name:
                return entry['timestamp']
        return None
    
    async def _execute_control_action(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa ação de controle no sistema"""
        try:
            action = data.get('action')
            reason = data.get('reason', 'Manual')
            
            logger.info(f"⚡ Executando ação: {action} - Razão: {reason}")
            
            result = {
                'status': 'completed',
                'action': action,
                'timestamp': datetime.now().isoformat(),
                'result': None
            }
            
            # Simular execução de ações
            if action == ControlAction.CLEAR_CACHE.value:
                # Simular limpeza de cache
                result['result'] = {
                    'freed_memory_mb': 512,
                    'cache_types_cleared': ['system', 'application', 'temp']
                }
                
            elif action == ControlAction.OPTIMIZE_MEMORY.value:
                # Simular otimização de memória
                result['result'] = {
                    'optimized_processes': 15,
                    'memory_freed_mb': 1024,
                    'garbage_collected': True
                }
                
            elif action == ControlAction.ADJUST_RESOURCES.value:
                # Simular ajuste de recursos
                result['result'] = {
                    'cpu_throttling': 'enabled',
                    'process_priority_adjusted': 8,
                    'resource_limits_applied': True
                }
            
            # Registrar ação
            self.control_history.append({
                'timestamp': datetime.now(),
                'action': action,
                'reason': reason,
                'result': result['result']
            })
            
            # Notificar sistema de recuperação se necessário
            if data.get('notify_recovery'):
                await self._notify_recovery_agent(action, result)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro executando ação de controle: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _adjust_system_resources(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ajusta recursos do sistema dinamicamente"""
        try:
            resource_type = data.get('resource_type', 'cpu')
            adjustment = data.get('adjustment', 'optimize')
            
            adjustments_made = []
            
            if resource_type == 'cpu':
                # Simular ajuste de CPU
                adjustments_made.append({
                    'type': 'cpu_governor',
                    'from': 'performance',
                    'to': 'balanced'
                })
                adjustments_made.append({
                    'type': 'process_affinity',
                    'adjusted_processes': 5
                })
            
            elif resource_type == 'memory':
                # Simular ajuste de memória
                adjustments_made.append({
                    'type': 'swap_usage',
                    'swappiness': 10
                })
                adjustments_made.append({
                    'type': 'memory_compaction',
                    'compacted_mb': 256
                })
            
            return {
                'status': 'completed',
                'resource_type': resource_type,
                'adjustments': adjustments_made,
                'expected_improvement': '15-20%'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ajustando recursos: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _manage_service(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gerencia serviços do sistema"""
        try:
            service_name = data.get('service_name')
            action = data.get('action', 'status')
            
            logger.info(f"🔧 Gerenciando serviço: {service_name} - Ação: {action}")
            
            # Simular gerenciamento de serviço
            if action == 'restart':
                result = {
                    'status': 'completed',
                    'service': service_name,
                    'action': 'restarted',
                    'downtime_seconds': 3,
                    'new_pid': 12345
                }
            elif action == 'stop':
                result = {
                    'status': 'completed',
                    'service': service_name,
                    'action': 'stopped',
                    'cleanup_performed': True
                }
            elif action == 'start':
                result = {
                    'status': 'completed',
                    'service': service_name,
                    'action': 'started',
                    'pid': 12346,
                    'startup_time_ms': 1500
                }
            else:  # status
                result = {
                    'status': 'completed',
                    'service': service_name,
                    'is_running': True,
                    'pid': 12345,
                    'uptime_hours': 48.5,
                    'memory_mb': 256
                }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro gerenciando serviço: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _notify_recovery_agent(self, action: str, result: Dict[str, Any]):
        """Notifica agente de recuperação sobre ações executadas"""
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="recovery_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.MEDIUM,
            content={
                'notification_type': 'control_action_executed',
                'action': action,
                'result': result,
                'timestamp': datetime.now().isoformat()
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)

# Importações necessárias
from uuid import uuid4
import platform

def create_system_agents(message_bus, num_instances=1) -> List:
    """
    Cria agentes de sistema
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com exatamente 3 agentes de sistema
    """
    agents = []
    
    try:
        logger.info("🖥️ Criando agentes de Sistema...")
        
        # Verificar agentes existentes
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        # IDs fixos para os 3 agentes
        agent_configs = [
            ('monitor_001', SystemMonitorAgent),
            ('control_001', SystemControlAgent),
            ('recovery_001', SystemRecoveryAgent)
        ]
        
        # Criar agentes
        for agent_id, agent_class in agent_configs:
            if agent_id not in existing_agents:
                try:
                    agent = agent_class(agent_id, AgentType.SYSTEM, message_bus)
                    
                    # Iniciar monitoramento automático para o monitor
                    if isinstance(agent, SystemMonitorAgent):
                        asyncio.create_task(agent.start_monitoring())
                    
                    agents.append(agent)
                    logger.info(f"✅ {agent_id} criado com sucesso")
                    logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                    
                except Exception as e:
                    logger.error(f"❌ Erro criando {agent_id}: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
            else:
                logger.warning(f"⚠️ Agente {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agentes de Sistema criados com sucesso")
        
        # Validar quantidade
        if len(agents) != 3:
            logger.warning(f"⚠️ Esperado 3 agentes, criados {len(agents)}")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando agentes de Sistema: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []

class SystemRecoveryAgent(BaseNetworkAgent):
    """Agente de recuperação do sistema"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['system_recovery', 'disaster_recovery', 'backup_restore']
        self.recovery_plans = self._initialize_recovery_plans()
        self.recovery_history = []
        self.backup_configurations = {}
        self._setup_recovery_handlers()
        logger.info(f"✅ {self.agent_id} inicializado com planos de recuperação")
    
    def _initialize_recovery_plans(self) -> Dict[str, RecoveryPlan]:
        """Inicializa planos de recuperação predefinidos"""
        return {
            'high_cpu_sustained': RecoveryPlan(
                issue_type='high_cpu_sustained',
                severity='high',
                actions=[
                    'Identificar processos com alto consumo',
                    'Finalizar processos não essenciais',
                    'Reiniciar serviços críticos',
                    'Escalar recursos se necessário'
                ],
                estimated_time=15,
                success_probability=0.85
            ),
            'memory_leak': RecoveryPlan(
                issue_type='memory_leak',
                severity='critical',
                actions=[
                    'Identificar processo com vazamento',
                    'Capturar dump de memória',
                    'Reiniciar processo afetado',
                    'Aplicar patch se disponível'
                ],
                estimated_time=30,
                success_probability=0.75
            ),
            'service_failure': RecoveryPlan(
                issue_type='service_failure',
                severity='critical',
                actions=[
                    'Verificar logs do serviço',
                    'Tentar reinicialização',
                    'Restaurar de backup se necessário',
                    'Ativar serviço de fallback'
                ],
                estimated_time=10,
                success_probability=0.90
            ),
            'disk_full': RecoveryPlan(
                issue_type='disk_full',
                severity='high',
                actions=[
                    'Identificar arquivos grandes',
                    'Limpar logs antigos',
                    'Comprimir arquivos não essenciais',
                    'Mover dados para storage secundário'
                ],
                estimated_time=20,
                success_probability=0.95
            )
        }
    
    def _setup_recovery_handlers(self):
        """Configura handlers de recuperação"""
        self.recovery_handlers = {
            'execute_recovery': self._execute_recovery_plan,
            'create_backup': self._create_system_backup,
            'restore_backup': self._restore_from_backup,
            'test_recovery': self._test_recovery_plan
        }
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens e inicia recuperação se necessário"""
        await super().handle_message(message)
        
        # Processar notificações de problemas
        if message.message_type == MessageType.EMERGENCY:
            await self._handle_emergency(message)
    
    async def _handle_emergency(self, emergency_message: AgentMessage):
        """Trata situações de emergência"""
        try:
            issue_type = emergency_message.content.get('issue_type')
            severity = emergency_message.content.get('severity', 'high')
            
            logger.error(f"🚨 EMERGÊNCIA: {issue_type} - Severidade: {severity}")
            
            # Selecionar plano de recuperação
            recovery_plan = self.recovery_plans.get(issue_type)
            
            if recovery_plan:
                # Executar plano de recuperação
                await self._execute_recovery_plan({
                    'plan_name': issue_type,
                    'auto_execute': True,
                    'context': emergency_message.content
                })
            else:
                # Criar plano dinâmico
                logger.warning(f"⚠️ Sem plano predefinido para {issue_type}, criando plano dinâmico")
                await self._create_dynamic_recovery_plan(issue_type, emergency_message.content)
            
        except Exception as e:
            logger.error(f"❌ Erro tratando emergência: {e}")
    
    async def _execute_recovery_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa plano de recuperação"""
        try:
            plan_name = data.get('plan_name')
            auto_execute = data.get('auto_execute', False)
            context = data.get('context', {})
            
            plan = self.recovery_plans.get(plan_name)
            if not plan:
                return {
                    'status': 'error',
                    'message': f'Plano {plan_name} não encontrado'
                }
            
            logger.info(f"🔧 Executando plano de recuperação: {plan_name}")
            
            execution_result = {
                'status': 'in_progress',
                'plan': plan_name,
                'started_at': datetime.now().isoformat(),
                'steps_completed': [],
                'steps_failed': []
            }
            
            # Executar cada ação do plano
            for i, action in enumerate(plan.actions):
                logger.info(f"   Step {i+1}/{len(plan.actions)}: {action}")
                
                # Simular execução da ação
                success = await self._simulate_recovery_action(action, context)
                
                if success:
                    execution_result['steps_completed'].append({
                        'step': i+1,
                        'action': action,
                        'status': 'completed'
                    })
                else:
                    execution_result['steps_failed'].append({
                        'step': i+1,
                        'action': action,
                        'status': 'failed'
                    })
                    
                    if not auto_execute:
                        # Parar em caso de falha se não for automático
                        break
                
                # Pequeno delay entre ações
                await asyncio.sleep(2)
            
            # Calcular resultado final
            total_steps = len(plan.actions)
            completed_steps = len(execution_result['steps_completed'])
            
            if completed_steps == total_steps:
                execution_result['status'] = 'completed'
                execution_result['message'] = 'Recuperação concluída com sucesso'
            elif completed_steps > 0:
                execution_result['status'] = 'partial'
                execution_result['message'] = f'Recuperação parcial: {completed_steps}/{total_steps} passos completos'
            else:
                execution_result['status'] = 'failed'
                execution_result['message'] = 'Recuperação falhou'
            
            execution_result['completed_at'] = datetime.now().isoformat()
            execution_result['duration_minutes'] = plan.estimated_time
            
            # Registrar no histórico
            self.recovery_history.append(execution_result)
            
            # Notificar sistema sobre resultado
            await self._notify_recovery_result(execution_result)
            
            return execution_result
            
        except Exception as e:
            logger.error(f"❌ Erro executando plano de recuperação: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _simulate_recovery_action(self, action: str, context: Dict[str, Any]) -> bool:
        """Simula execução de uma ação de recuperação"""
        try:
            # Simular diferentes tipos de ações com taxa de sucesso variável
            import random
            
            # Taxa de sucesso baseada no tipo de ação
            success_rates = {
                'Identificar': 0.95,
                'Finalizar': 0.90,
                'Reiniciar': 0.85,
                'Restaurar': 0.80,
                'Limpar': 0.95,
                'Verificar': 0.98
            }
            
            # Determinar taxa de sucesso
            success_rate = 0.85  # padrão
            for key, rate in success_rates.items():
                if key in action:
                    success_rate = rate
                    break
            
            # Simular execução com delay
            await asyncio.sleep(1)
            
            # Determinar sucesso baseado na taxa
            success = random.random() < success_rate
            
            if success:
                logger.info(f"   ✅ Ação concluída: {action}")
            else:
                logger.warning(f"   ❌ Ação falhou: {action}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Erro simulando ação: {e}")
            return False
    
    async def _create_system_backup(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria backup do sistema"""
        try:
            backup_type = data.get('type', 'incremental')
            components = data.get('components', ['config', 'data', 'logs'])
            
            logger.info(f"💾 Criando backup {backup_type} de {components}")
            
            backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            backup_result = {
                'status': 'completed',
                'backup_id': backup_id,
                'type': backup_type,
                'components': components,
                'size_mb': 0,
                'files_backed_up': 0,
                'timestamp': datetime.now().isoformat()
            }
            
            # Simular processo de backup
            for component in components:
                if component == 'config':
                    backup_result['size_mb'] += 10
                    backup_result['files_backed_up'] += 50
                elif component == 'data':
                    backup_result['size_mb'] += 500
                    backup_result['files_backed_up'] += 1000
                elif component == 'logs':
                    backup_result['size_mb'] += 100
                    backup_result['files_backed_up'] += 200
            
            # Armazenar configuração do backup
            self.backup_configurations[backup_id] = {
                'type': backup_type,
                'components': components,
                'created_at': datetime.now(),
                'size_mb': backup_result['size_mb'],
                'location': f'/backups/{backup_id}'
            }
            
            logger.info(f"✅ Backup {backup_id} criado com sucesso")
            
            return backup_result
            
        except Exception as e:
            logger.error(f"❌ Erro criando backup: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _restore_from_backup(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Restaura sistema de um backup"""
        try:
            backup_id = data.get('backup_id')
            components = data.get('components', 'all')
            
            if backup_id not in self.backup_configurations:
                return {
                    'status': 'error',
                    'message': f'Backup {backup_id} não encontrado'
                }
            
            backup_config = self.backup_configurations[backup_id]
            logger.info(f"🔄 Restaurando de {backup_id}")
            
            restore_result = {
                'status': 'in_progress',
                'backup_id': backup_id,
                'started_at': datetime.now().isoformat(),
                'components_restored': [],
                'errors': []
            }
            
            # Determinar componentes a restaurar
            if components == 'all':
                components_to_restore = backup_config['components']
            else:
                components_to_restore = components if isinstance(components, list) else [components]
            
            # Simular restauração
            for component in components_to_restore:
                logger.info(f"   Restaurando {component}...")
                await asyncio.sleep(2)  # Simular tempo de restauração
                
                # Simular possível falha (10% de chance)
                import random
                if random.random() > 0.9:
                    restore_result['errors'].append({
                        'component': component,
                        'error': 'Falha na verificação de integridade'
                    })
                else:
                    restore_result['components_restored'].append(component)
            
            # Resultado final
            if not restore_result['errors']:
                restore_result['status'] = 'completed'
                restore_result['message'] = 'Restauração concluída com sucesso'
            elif restore_result['components_restored']:
                restore_result['status'] = 'partial'
                restore_result['message'] = 'Restauração parcial concluída'
            else:
                restore_result['status'] = 'failed'
                restore_result['message'] = 'Restauração falhou'
            
            restore_result['completed_at'] = datetime.now().isoformat()
            
            return restore_result
            
        except Exception as e:
            logger.error(f"❌ Erro restaurando backup: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _test_recovery_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Testa plano de recuperação sem executar"""
        try:
            plan_name = data.get('plan_name')
            
            if plan_name not in self.recovery_plans:
                return {
                    'status': 'error',
                    'message': f'Plano {plan_name} não encontrado'
                }
            
            plan = self.recovery_plans[plan_name]
            logger.info(f"🧪 Testando plano de recuperação: {plan_name}")
            
            test_result = {
                'status': 'completed',
                'plan_name': plan_name,
                'plan_details': {
                    'issue_type': plan.issue_type,
                    'severity': plan.severity,
                    'steps': len(plan.actions),
                    'estimated_time': f"{plan.estimated_time} minutos",
                    'success_probability': f"{plan.success_probability * 100:.0f}%"
                },
                'validation': {
                    'prerequisites_met': True,
                    'resources_available': True,
                    'conflicts_detected': False
                },
                'recommendations': []
            }
            
            # Simular validações
            if plan.severity == 'critical':
                test_result['recommendations'].append(
                    'Considere notificar administradores antes da execução'
                )
            
            if plan.estimated_time > 20:
                test_result['recommendations'].append(
                    'Plano pode causar indisponibilidade significativa'
                )
            
            return test_result
            
        except Exception as e:
            logger.error(f"❌ Erro testando plano: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _create_dynamic_recovery_plan(self, issue_type: str, context: Dict[str, Any]):
        """Cria plano de recuperação dinâmico para problemas não previstos"""
        try:
            logger.info(f"🔨 Criando plano dinâmico para {issue_type}")
            
            # Analisar contexto e criar plano básico
            severity = context.get('severity', 'medium')
            
            # Ações genéricas baseadas na severidade
            if severity == 'critical':
                actions = [
                    'Isolar componente afetado',
                    'Capturar diagnóstico completo',
                    'Tentar recuperação automática',
                    'Escalar para administrador se falhar'
                ]
                estimated_time = 25
            elif severity == 'high':
                actions = [
                    'Analisar logs do sistema',
                    'Identificar causa raiz',
                    'Aplicar correção padrão',
                    'Monitorar resultado'
                ]
                estimated_time = 15
            else:
                actions = [
                    'Coletar informações do problema',
                    'Aplicar solução conhecida',
                    'Verificar resolução'
                ]
                estimated_time = 10
            
            # Criar novo plano
            dynamic_plan = RecoveryPlan(
                issue_type=issue_type,
                severity=severity,
                actions=actions,
                estimated_time=estimated_time,
                success_probability=0.70  # Menor probabilidade por ser dinâmico
            )
            
            # Adicionar ao conjunto de planos
            self.recovery_plans[f"dynamic_{issue_type}"] = dynamic_plan
            
            # Executar o plano criado
            await self._execute_recovery_plan({
                'plan_name': f"dynamic_{issue_type}",
                'auto_execute': True,
                'context': context
            })
            
        except Exception as e:
            logger.error(f"❌ Erro criando plano dinâmico: {e}")
    
    async def _notify_recovery_result(self, result: Dict[str, Any]):
        """Notifica sistema sobre resultado da recuperação"""
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="broadcast",  # Notificar todos
            message_type=MessageType.NOTIFICATION,
            priority=Priority.HIGH,
            content={
                'notification_type': 'recovery_completed',
                'result': result,
                'timestamp': datetime.now().isoformat()
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)
