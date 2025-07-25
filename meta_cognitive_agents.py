import logging
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import json
from collections import defaultdict, deque
from multi_agent_network import AgentType, BaseNetworkAgent, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """Status de tarefas do sistema"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class OrchestrationStrategy(Enum):
    """Estratégias de orquestração"""
    ROUND_ROBIN = "round_robin"
    LOAD_BALANCED = "load_balanced"
    CAPABILITY_BASED = "capability_based"
    PRIORITY_BASED = "priority_based"
    ADAPTIVE = "adaptive"

class SystemState(Enum):
    """Estados do sistema cognitivo"""
    LEARNING = "learning"
    OPTIMIZING = "optimizing"
    STABLE = "stable"
    ADAPTING = "adapting"
    RECOVERING = "recovering"

@dataclass
class SystemTask:
    """Tarefa do sistema"""
    task_id: str
    task_type: str
    description: str
    priority: Priority
    requirements: List[str]
    assigned_agents: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentPerformance:
    """Métricas de performance de agente"""
    agent_id: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    average_completion_time: float = 0.0
    reliability_score: float = 1.0
    current_load: int = 0
    specializations: List[str] = field(default_factory=list)
    last_activity: datetime = field(default_factory=datetime.now)

@dataclass
class SystemInsight:
    """Insight do sistema meta-cognitivo"""
    insight_id: str
    type: str
    description: str
    confidence: float
    impact: str  # low, medium, high
    recommendations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

class OrchestratorAgent(BaseNetworkAgent):
    """Agente orquestrador supremo do sistema"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'orchestration',
            'task_distribution',
            'load_balancing',
            'system_coordination',
            'resource_optimization'
        ]
        
        # Estado do orquestrador
        self.active_tasks = {}  # task_id -> SystemTask
        self.completed_tasks = deque(maxlen=1000)  # Histórico limitado
        self.agent_registry = {}  # agent_id -> AgentPerformance
        self.task_queue = asyncio.Queue()
        self.orchestration_strategy = OrchestrationStrategy.ADAPTIVE
        
        # Configurações
        self.max_retries = 3
        self.task_timeout = 300  # 5 minutos padrão
        self.load_threshold = 5  # Máximo de tarefas por agente
        
        # Métricas
        self.orchestration_metrics = {
            'tasks_distributed': 0,
            'tasks_completed': 0,
            'tasks_failed': 0,
            'average_completion_time': 0.0,
            'system_efficiency': 1.0
        }
        
        # Tasks de background
        self._orchestration_task = None
        self._monitoring_task = None
        
        logger.info(f"👑 {self.agent_id} inicializado como Orquestrador Supremo")
    
    async def start_orchestration(self):
        """Inicia serviços de orquestração"""
        if not self._orchestration_task:
            self._orchestration_task = asyncio.create_task(self._orchestration_loop())
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            logger.info(f"🎯 {self.agent_id} iniciou serviços de orquestração")
    
    async def stop_orchestration(self):
        """Para serviços de orquestração"""
        if self._orchestration_task:
            self._orchestration_task.cancel()
            self._orchestration_task = None
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
        logger.info(f"🛑 {self.agent_id} parou serviços de orquestração")
    
    async def _orchestration_loop(self):
        """Loop principal de orquestração"""
        while True:
            try:
                # Processar fila de tarefas
                if not self.task_queue.empty():
                    task = await self.task_queue.get()
                    await self._distribute_task(task)
                
                # Verificar tarefas em timeout
                await self._check_task_timeouts()
                
                # Atualizar estratégia se necessário
                if self.orchestration_strategy == OrchestrationStrategy.ADAPTIVE:
                    self._adapt_orchestration_strategy()
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de orquestração: {e}")
    
    async def _monitoring_loop(self):
        """Loop de monitoramento do sistema"""
        while True:
            try:
                # Atualizar registro de agentes
                await self._update_agent_registry()
                
                # Calcular métricas do sistema
                self._calculate_system_metrics()
                
                # Detectar e resolver gargalos
                bottlenecks = self._detect_bottlenecks()
                if bottlenecks:
                    await self._resolve_bottlenecks(bottlenecks)
                
                await asyncio.sleep(30)  # Monitorar a cada 30 segundos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento: {e}")
    
    async def orchestrate_system_wide_task(self, task: Any):
        """Orquestra uma tarefa em todo o sistema"""
        try:
            logger.info(f"👑 Orquestrando tarefa sistema: {task}")
            
            # Criar SystemTask
            system_task = SystemTask(
                task_id=f"task_{len(self.active_tasks) + 1:04d}",
                task_type=task.get('type', 'general') if isinstance(task, dict) else 'general',
                description=str(task),
                priority=Priority.HIGH,
                requirements=task.get('requirements', []) if isinstance(task, dict) else []
            )
            
            # Adicionar à fila
            await self.task_queue.put(system_task)
            self.active_tasks[system_task.task_id] = system_task
            
            logger.info(f"✅ Tarefa {system_task.task_id} adicionada à fila de orquestração")
            
            return {
                'status': 'accepted',
                'task_id': system_task.task_id,
                'estimated_completion': self._estimate_completion_time(system_task)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro orquestrando tarefa: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'submit_task':
                result = await self.orchestrate_system_wide_task(message.content.get('task'))
                await self._send_response(message, result)
                
            elif request_type == 'task_status':
                result = self._get_task_status(message.content.get('task_id'))
                await self._send_response(message, result)
                
            elif request_type == 'system_overview':
                result = self._get_system_overview()
                await self._send_response(message, result)
                
            elif request_type == 'agent_performance':
                result = self._get_agent_performance_report()
                await self._send_response(message, result)
        
        elif message.message_type == MessageType.RESPONSE:
            # Processar respostas de tarefas
            await self._process_task_response(message)
        
        elif message.message_type == MessageType.NOTIFICATION:
            # Processar notificações do sistema
            await self._process_system_notification(message)
    
    async def _distribute_task(self, task: SystemTask):
        """Distribui tarefa para agentes apropriados"""
        try:
            logger.info(f"📤 Distribuindo tarefa {task.task_id}")
            
            # Selecionar agentes baseado na estratégia
            selected_agents = await self._select_agents_for_task(task)
            
            if not selected_agents:
                logger.error(f"❌ Nenhum agente disponível para tarefa {task.task_id}")
                task.status = TaskStatus.FAILED
                return
            
            # Atribuir tarefa aos agentes
            task.assigned_agents = selected_agents
            task.status = TaskStatus.ASSIGNED
            task.started_at = datetime.now()
            
            # Enviar tarefa para agentes
            for agent_id in selected_agents:
                assignment_message = AgentMessage(
                    id=str(uuid4()),
                    sender_id=self.agent_id,
                    recipient_id=agent_id,
                    message_type=MessageType.TASK_ASSIGNMENT,
                    priority=task.priority,
                    content={
                        'task_id': task.task_id,
                        'task_type': task.task_type,
                        'description': task.description,
                        'requirements': task.requirements,
                        'timeout': self.task_timeout
                    },
                    timestamp=datetime.now()
                )
                
                await self.message_bus.publish(assignment_message)
                
                # Atualizar carga do agente
                if agent_id in self.agent_registry:
                    self.agent_registry[agent_id].current_load += 1
            
            self.orchestration_metrics['tasks_distributed'] += 1
            logger.info(f"✅ Tarefa {task.task_id} distribuída para {selected_agents}")
            
        except Exception as e:
            logger.error(f"❌ Erro distribuindo tarefa: {e}")
            task.status = TaskStatus.FAILED
    
    async def _select_agents_for_task(self, task: SystemTask) -> List[str]:
        """Seleciona agentes apropriados para uma tarefa"""
        available_agents = []
        
        # Filtrar agentes por capacidade e disponibilidade
        for agent_id, performance in self.agent_registry.items():
            # Verificar se agente está ativo
            if (datetime.now() - performance.last_activity).seconds > 300:
                continue
            
            # Verificar carga
            if performance.current_load >= self.load_threshold:
                continue
            
            # Verificar capacidades (se especificadas)
            if task.requirements:
                if not any(req in performance.specializations for req in task.requirements):
                    continue
            
            available_agents.append((agent_id, performance))
        
        if not available_agents:
            return []
        
        # Aplicar estratégia de seleção
        if self.orchestration_strategy == OrchestrationStrategy.LOAD_BALANCED:
            # Ordenar por menor carga
            available_agents.sort(key=lambda x: x[1].current_load)
        
        elif self.orchestration_strategy == OrchestrationStrategy.CAPABILITY_BASED:
            # Ordenar por melhor match de capacidades
            available_agents.sort(
                key=lambda x: sum(1 for req in task.requirements if req in x[1].specializations),
                reverse=True
            )
        
        elif self.orchestration_strategy == OrchestrationStrategy.PRIORITY_BASED:
            # Para alta prioridade, escolher agentes mais confiáveis
            if task.priority == Priority.CRITICAL:
                available_agents.sort(key=lambda x: x[1].reliability_score, reverse=True)
        
        # Selecionar agentes (1-3 dependendo da complexidade)
        num_agents = 1
        if task.priority == Priority.CRITICAL:
            num_agents = min(3, len(available_agents))
        elif len(task.requirements) > 3:
            num_agents = min(2, len(available_agents))
        
        return [agent[0] for agent in available_agents[:num_agents]]
    
    async def _process_task_response(self, message: AgentMessage):
        """Processa resposta de uma tarefa"""
        try:
            task_id = message.content.get('task_id')
            if task_id not in self.active_tasks:
                return
            
            task = self.active_tasks[task_id]
            status = message.content.get('status')
            
            if status == 'completed':
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                task.result = message.content.get('result')
                
                # Atualizar métricas do agente
                if message.sender_id in self.agent_registry:
                    perf = self.agent_registry[message.sender_id]
                    perf.tasks_completed += 1
                    perf.current_load = max(0, perf.current_load - 1)
                    
                    # Atualizar tempo médio
                    completion_time = (task.completed_at - task.started_at).total_seconds()
                    perf.average_completion_time = (
                        (perf.average_completion_time * (perf.tasks_completed - 1) + completion_time) /
                        perf.tasks_completed
                    )
                
                # Mover para completadas
                self.completed_tasks.append(task)
                del self.active_tasks[task_id]
                
                self.orchestration_metrics['tasks_completed'] += 1
                logger.info(f"✅ Tarefa {task_id} completada com sucesso")
                
            elif status == 'failed':
                # Tentar redistribuir se houver retries
                if task.metadata.get('retry_count', 0) < self.max_retries:
                    task.metadata['retry_count'] = task.metadata.get('retry_count', 0) + 1
                    task.status = TaskStatus.PENDING
                    await self.task_queue.put(task)
                    logger.warning(f"⚠️ Tarefa {task_id} falhou, tentativa {task.metadata['retry_count']}/{self.max_retries}")
                else:
                    task.status = TaskStatus.FAILED
                    task.completed_at = datetime.now()
                    self.completed_tasks.append(task)
                    del self.active_tasks[task_id]
                    self.orchestration_metrics['tasks_failed'] += 1
                    logger.error(f"❌ Tarefa {task_id} falhou após {self.max_retries} tentativas")
                
                # Atualizar métricas do agente
                if message.sender_id in self.agent_registry:
                    perf = self.agent_registry[message.sender_id]
                    perf.tasks_failed += 1
                    perf.current_load = max(0, perf.current_load - 1)
                    perf.reliability_score *= 0.95  # Reduzir confiabilidade
            
        except Exception as e:
            logger.error(f"❌ Erro processando resposta de tarefa: {e}")
    
    async def _process_system_notification(self, message: AgentMessage):
        """Processa notificações do sistema"""
        try:
            notification_type = message.content.get('notification_type')
            
            if notification_type == 'agent_status':
                # Atualizar status do agente
                agent_id = message.sender_id
                status = message.content.get('status')
                
                if agent_id not in self.agent_registry:
                    self.agent_registry[agent_id] = AgentPerformance(agent_id=agent_id)
                
                self.agent_registry[agent_id].last_activity = datetime.now()
                
                if status == 'overloaded':
                    # Redistribuir tarefas se necessário
                    await self._rebalance_agent_load(agent_id)
            
            elif notification_type == 'system_alert':
                # Processar alertas do sistema
                alert_level = message.content.get('level')
                if alert_level == 'critical':
                    # Ativar modo de recuperação
                    await self._activate_recovery_mode()
            
        except Exception as e:
            logger.error(f"❌ Erro processando notificação: {e}")
    
    async def _check_task_timeouts(self):
        """Verifica tarefas em timeout"""
        now = datetime.now()
        timed_out_tasks = []
        
        for task_id, task in self.active_tasks.items():
            if task.status == TaskStatus.IN_PROGRESS and task.started_at:
                elapsed = (now - task.started_at).total_seconds()
                if elapsed > self.task_timeout:
                    timed_out_tasks.append(task)
        
        for task in timed_out_tasks:
            logger.warning(f"⏱️ Tarefa {task.task_id} em timeout")
            
            # Notificar agentes
            for agent_id in task.assigned_agents:
                timeout_message = AgentMessage(
                    id=str(uuid4()),
                    sender_id=self.agent_id,
                    recipient_id=agent_id,
                    message_type=MessageType.REQUEST,
                    priority=Priority.HIGH,
                    content={
                        'action': 'cancel_task',
                        'task_id': task.task_id
                    },
                    timestamp=datetime.now()
                )
                await self.message_bus.publish(timeout_message)
            
            # Remarcar tarefa
            task.metadata['timeout_count'] = task.metadata.get('timeout_count', 0) + 1
            if task.metadata['timeout_count'] < 2:
                task.status = TaskStatus.PENDING
                await self.task_queue.put(task)
            else:
                task.status = TaskStatus.FAILED
                self.completed_tasks.append(task)
                del self.active_tasks[task.task_id]
    
    async def _update_agent_registry(self):
        """Atualiza registro de agentes"""
        # Solicitar status de todos os agentes conhecidos
        for agent_id in list(self.message_bus.subscribers.keys()):
            if agent_id != self.agent_id:
                status_request = AgentMessage(
                    id=str(uuid4()),
                    sender_id=self.agent_id,
                    recipient_id=agent_id,
                    message_type=MessageType.HEARTBEAT,
                    priority=Priority.LOW,
                    content={'request': 'status'},
                    timestamp=datetime.now()
                )
                await self.message_bus.publish(status_request)
    
    def _calculate_system_metrics(self):
        """Calcula métricas do sistema"""
        if self.orchestration_metrics['tasks_distributed'] > 0:
            # Taxa de sucesso
            success_rate = (
                self.orchestration_metrics['tasks_completed'] /
                (self.orchestration_metrics['tasks_completed'] + self.orchestration_metrics['tasks_failed'])
            ) if (self.orchestration_metrics['tasks_completed'] + self.orchestration_metrics['tasks_failed']) > 0 else 0
            
            # Eficiência do sistema
            self.orchestration_metrics['system_efficiency'] = success_rate
            
            # Tempo médio de conclusão
            if self.completed_tasks:
                total_time = sum(
                    (t.completed_at - t.started_at).total_seconds()
                    for t in self.completed_tasks
                    if t.completed_at and t.started_at
                )
                self.orchestration_metrics['average_completion_time'] = (
                    total_time / len(self.completed_tasks)
                )
    
    def _detect_bottlenecks(self) -> List[Dict[str, Any]]:
        """Detecta gargalos no sistema"""
        bottlenecks = []
        
        # Verificar agentes sobrecarregados
        for agent_id, perf in self.agent_registry.items():
            if perf.current_load >= self.load_threshold:
                bottlenecks.append({
                    'type': 'overloaded_agent',
                    'agent_id': agent_id,
                    'load': perf.current_load
                })
        
        # Verificar fila de tarefas
        if self.task_queue.qsize() > 10:
            bottlenecks.append({
                'type': 'task_queue_backlog',
                'queue_size': self.task_queue.qsize()
            })
        
        # Verificar taxa de falha
        if self.orchestration_metrics['system_efficiency'] < 0.7:
            bottlenecks.append({
                'type': 'high_failure_rate',
                'efficiency': self.orchestration_metrics['system_efficiency']
            })
        
        return bottlenecks
    
    async def _resolve_bottlenecks(self, bottlenecks: List[Dict[str, Any]]):
        """Tenta resolver gargalos identificados"""
        for bottleneck in bottlenecks:
            if bottleneck['type'] == 'overloaded_agent':
                await self._rebalance_agent_load(bottleneck['agent_id'])
            
            elif bottleneck['type'] == 'task_queue_backlog':
                # Aumentar paralelismo ou criar tarefas de alta prioridade
                logger.warning(f"⚠️ Fila de tarefas com {bottleneck['queue_size']} itens")
            
            elif bottleneck['type'] == 'high_failure_rate':
                # Mudar estratégia ou ativar modo de recuperação
                logger.warning(f"⚠️ Taxa de sucesso baixa: {bottleneck['efficiency']:.2%}")
                self._adapt_orchestration_strategy()
    
    async def _rebalance_agent_load(self, overloaded_agent_id: str):
        """Rebalanceia carga de um agente sobrecarregado"""
        logger.info(f"⚖️ Rebalanceando carga do agente {overloaded_agent_id}")
        
        # Encontrar tarefas que podem ser redistribuídas
        tasks_to_redistribute = []
        for task_id, task in self.active_tasks.items():
            if overloaded_agent_id in task.assigned_agents and task.status == TaskStatus.ASSIGNED:
                tasks_to_redistribute.append(task)
        
        # Redistribuir tarefas
        for task in tasks_to_redistribute[:2]:  # Redistribuir no máximo 2 tarefas
            task.assigned_agents.remove(overloaded_agent_id)
            if not task.assigned_agents:
                task.status = TaskStatus.PENDING
                await self.task_queue.put(task)
    
    def _adapt_orchestration_strategy(self):
        """Adapta estratégia de orquestração baseada nas métricas"""
        efficiency = self.orchestration_metrics['system_efficiency']
        
        if efficiency < 0.6:
            # Sistema com muitas falhas - usar estratégia mais conservadora
            self.orchestration_strategy = OrchestrationStrategy.CAPABILITY_BASED
            logger.info("📊 Mudando para estratégia baseada em capacidades")
        
        elif efficiency > 0.9 and self.task_queue.qsize() > 5:
            # Sistema eficiente mas com fila - otimizar para velocidade
            self.orchestration_strategy = OrchestrationStrategy.LOAD_BALANCED
            logger.info("📊 Mudando para estratégia de balanceamento de carga")
        
        # Manter estratégia adaptativa em condições normais
    
    async def _activate_recovery_mode(self):
        """Ativa modo de recuperação do sistema"""
        logger.warning("🚨 Ativando modo de recuperação do sistema")
        
        # Pausar novas tarefas
        temp_queue = []
        while not self.task_queue.empty():
            temp_queue.append(await self.task_queue.get())
        
        # Cancelar tarefas não críticas
        for task_id, task in list(self.active_tasks.items()):
            if task.priority not in [Priority.CRITICAL, Priority.HIGH]:
                task.status = TaskStatus.CANCELLED
                self.completed_tasks.append(task)
                del self.active_tasks[task_id]
        
        # Recolocar tarefas críticas na fila
        for task in temp_queue:
            if task.priority in [Priority.CRITICAL, Priority.HIGH]:
                await self.task_queue.put(task)
    
    def _estimate_completion_time(self, task: SystemTask) -> str:
        """Estima tempo de conclusão de uma tarefa"""
        avg_time = self.orchestration_metrics['average_completion_time']
        queue_size = self.task_queue.qsize()
        
        # Estimativa básica
        estimated_seconds = avg_time * (1 + queue_size * 0.1)
        
        # Ajustar por prioridade
        if task.priority == Priority.CRITICAL:
            estimated_seconds *= 0.5
        elif task.priority == Priority.LOW:
            estimated_seconds *= 1.5
        
        return f"{int(estimated_seconds)} segundos"
    
    def _get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Retorna status de uma tarefa"""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            return {
                'status': 'active',
                'task_id': task_id,
                'current_status': task.status.value,
                'assigned_agents': task.assigned_agents,
                'started_at': task.started_at.isoformat() if task.started_at else None
            }
        
        # Procurar em tarefas completadas
        for task in self.completed_tasks:
            if task.task_id == task_id:
                return {
                    'status': 'completed',
                    'task_id': task_id,
                    'final_status': task.status.value,
                    'result': task.result,
                    'completed_at': task.completed_at.isoformat() if task.completed_at else None
                }
        
        return {
            'status': 'not_found',
            'message': f'Tarefa {task_id} não encontrada'
        }
    
    def _get_system_overview(self) -> Dict[str, Any]:
        """Retorna visão geral do sistema"""
        return {
            'status': 'active',
            'orchestration_strategy': self.orchestration_strategy.value,
            'active_tasks': len(self.active_tasks),
            'queued_tasks': self.task_queue.qsize(),
            'total_agents': len(self.agent_registry),
            'active_agents': sum(1 for a in self.agent_registry.values() if a.current_load > 0),
            'metrics': {
                'tasks_distributed': self.orchestration_metrics['tasks_distributed'],
                'tasks_completed': self.orchestration_metrics['tasks_completed'],
                'tasks_failed': self.orchestration_metrics['tasks_failed'],
                'system_efficiency': f"{self.orchestration_metrics['system_efficiency']:.2%}",
                'average_completion_time': f"{self.orchestration_metrics['average_completion_time']:.1f}s"
            }
        }
    
    def _get_agent_performance_report(self) -> Dict[str, Any]:
        """Retorna relatório de performance dos agentes"""
        agent_reports = []
        
        for agent_id, perf in self.agent_registry.items():
            agent_reports.append({
                'agent_id': agent_id,
                'tasks_completed': perf.tasks_completed,
                'tasks_failed': perf.tasks_failed,
                'current_load': perf.current_load,
                'reliability_score': f"{perf.reliability_score:.2%}",
                'average_completion_time': f"{perf.average_completion_time:.1f}s",
                'specializations': perf.specializations
            })
        
        # Ordenar por performance
        agent_reports.sort(
            key=lambda x: (x['tasks_completed'], -x['tasks_failed'], x['reliability_score']),
            reverse=True
        )
        
        return {
            'status': 'completed',
            'total_agents': len(agent_reports),
            'top_performers': agent_reports[:5],
            'all_agents': agent_reports
        }
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
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

class MetaCognitiveAgent(BaseNetworkAgent):
    """Agente meta-cognitivo para análise e otimização do sistema"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'meta_cognition',
            'pattern_recognition',
            'system_analysis',
            'learning',
            'optimization_recommendations'
        ]
        
        # Estado cognitivo
        self.system_state = SystemState.LEARNING
        self.knowledge_base = {
            'patterns': [],
            'insights': [],
            'optimizations': [],
            'correlations': {}
        }
        
        # Métricas de aprendizado
        self.learning_metrics = {
            'patterns_identified': 0,
            'insights_generated': 0,
            'successful_optimizations': 0,
            'system_improvements': 0
        }
        
        # Configurações
        self.analysis_interval = 60  # segundos
        self.pattern_threshold = 0.7  # confiança mínima
        self.learning_rate = 0.1
        
        # Tasks de background
        self._analysis_task = None
        self._learning_task = None
        
        logger.info(f"🧠 {self.agent_id} inicializado com capacidades meta-cognitivas")
    
    async def start_meta_cognition(self):
        """Inicia processos meta-cognitivos"""
        if not self._analysis_task:
            self._analysis_task = asyncio.create_task(self._analysis_loop())
            self._learning_task = asyncio.create_task(self._learning_loop())
            logger.info(f"🎓 {self.agent_id} iniciou processos meta-cognitivos")
    
    async def stop_meta_cognition(self):
        """Para processos meta-cognitivos"""
        if self._analysis_task:
            self._analysis_task.cancel()
            self._analysis_task = None
        if self._learning_task:
            self._learning_task.cancel()
            self._learning_task = None
        logger.info(f"🛑 {self.agent_id} parou processos meta-cognitivos")
    
    async def _analysis_loop(self):
        """Loop de análise do sistema"""
        while True:
            try:
                # Coletar dados do sistema
                system_data = await self._collect_system_data()
                
                # Identificar padrões
                patterns = self._identify_patterns(system_data)
                if patterns:
                    self.knowledge_base['patterns'].extend(patterns)
                    self.learning_metrics['patterns_identified'] += len(patterns)
                
                # Gerar insights
                insights = self._generate_insights(patterns, system_data)
                if insights:
                    await self._process_insights(insights)
                
                # Atualizar estado do sistema
                self._update_system_state()
                
                await asyncio.sleep(self.analysis_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na análise meta-cognitiva: {e}")
    
    async def _learning_loop(self):
        """Loop de aprendizado contínuo"""
        while True:
            try:
                # Analisar eficácia das otimizações anteriores
                await self._evaluate_optimizations()
                
                # Aprender com correlações
                self._update_correlations()
                
                # Adaptar estratégias baseadas no aprendizado
                if self.system_state == SystemState.LEARNING:
                    self._adapt_analysis_strategies()
                
                await asyncio.sleep(self.analysis_interval * 2)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no aprendizado: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'analyze_system':
                result = await self._analyze_system_request(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'get_insights':
                result = self._get_recent_insights()
                await self._send_response(message, result)
                
            elif request_type == 'optimization_recommendations':
                result = await self._get_optimization_recommendations()
                await self._send_response(message, result)
                
            elif request_type == 'cognitive_status':
                result = self._get_cognitive_status()
                await self._send_response(message, result)
    
    async def _collect_system_data(self) -> Dict[str, Any]:
        """Coleta dados do sistema para análise"""
        system_data = {
            'timestamp': datetime.now(),
            'agents': {},
            'messages': {},
            'performance': {}
        }
        
        # Solicitar dados do orchestrator
        data_request = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.REQUEST,
            priority=Priority.LOW,
            content={'request_type': 'system_overview'},
            timestamp=datetime.now()
        )
        
        # TODO: Implementar coleta assíncrona real
        # Por ora, retornar dados simulados
        return {
            'timestamp': datetime.now(),
            'active_agents': 20,
            'message_rate': 150,  # mensagens/minuto
            'task_completion_rate': 0.85,
            'system_load': 0.65,
            'error_rate': 0.05
        }
    
    def _identify_patterns(self, system_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica padrões no comportamento do sistema"""
        patterns = []
        
        # Análise de carga
        if system_data.get('system_load', 0) > 0.8:
            patterns.append({
                'pattern_id': f"pattern_{len(self.knowledge_base['patterns']) + 1:04d}",
                'type': 'high_load',
                'confidence': 0.9,
                'description': 'Sistema operando com alta carga',
                'data': {'load': system_data['system_load']}
            })
        
        # Análise de taxa de erro
        error_rate = system_data.get('error_rate', 0)
        if error_rate > 0.1:
            patterns.append({
                'pattern_id': f"pattern_{len(self.knowledge_base['patterns']) + 2:04d}",
                'type': 'high_error_rate',
                'confidence': 0.85,
                'description': f'Taxa de erro elevada: {error_rate:.2%}',
                'data': {'error_rate': error_rate}
            })
        
        # Análise de desempenho
        completion_rate = system_data.get('task_completion_rate', 1.0)
        if completion_rate < 0.7:
            patterns.append({
                'pattern_id': f"pattern_{len(self.knowledge_base['patterns']) + 3:04d}",
                'type': 'low_performance',
                'confidence': 0.8,
                'description': 'Taxa de conclusão de tarefas abaixo do esperado',
                'data': {'completion_rate': completion_rate}
            })
        
        return [p for p in patterns if p['confidence'] >= self.pattern_threshold]
    
    def _generate_insights(self, patterns: List[Dict[str, Any]], system_data: Dict[str, Any]) -> List[SystemInsight]:
        """Gera insights baseados nos padrões identificados"""
        insights = []
        
        # Análise de padrões combinados
        pattern_types = [p['type'] for p in patterns]
        
        if 'high_load' in pattern_types and 'high_error_rate' in pattern_types:
            insight = SystemInsight(
                insight_id=f"insight_{len(self.knowledge_base['insights']) + 1:04d}",
                type='correlation',
                description='Alta carga correlacionada com aumento de erros',
                confidence=0.85,
                impact='high',
                recommendations=[
                    'Implementar throttling de requisições',
                    'Aumentar recursos do sistema',
                    'Ativar balanceamento de carga agressivo'
                ]
            )
            insights.append(insight)
        
        if 'low_performance' in pattern_types:
            insight = SystemInsight(
                insight_id=f"insight_{len(self.knowledge_base['insights']) + 2:04d}",
                type='performance',
                description='Performance do sistema degradada',
                confidence=0.75,
                impact='medium',
                recommendations=[
                    'Analisar gargalos específicos',
                    'Otimizar algoritmos de distribuição',
                    'Considerar cache de resultados'
                ]
            )
            insights.append(insight)
        
        # Insights baseados em tendências
        if len(self.knowledge_base['patterns']) > 10:
            recent_patterns = self.knowledge_base['patterns'][-10:]
            load_trend = [p['data'].get('load', 0) for p in recent_patterns if p['type'] == 'high_load']
            
            if load_trend and all(load_trend[i] <= load_trend[i+1] for i in range(len(load_trend)-1)):
                insight = SystemInsight(
                    insight_id=f"insight_{len(self.knowledge_base['insights']) + 3:04d}",
                    type='trend',
                    description='Tendência crescente de carga no sistema',
                    confidence=0.9,
                    impact='high',
                    recommendations=[
                        'Preparar escalonamento preventivo',
                        'Revisar previsões de capacidade',
                        'Implementar auto-scaling'
                    ]
                )
                insights.append(insight)
        
        return insights
    
    async def _process_insights(self, insights: List[SystemInsight]):
        """Processa e age sobre insights gerados"""
        for insight in insights:
            self.knowledge_base['insights'].append(insight)
            self.learning_metrics['insights_generated'] += 1
            
            logger.info(f"💡 Insight gerado: {insight.description} (impacto: {insight.impact})")
            
            # Notificar orchestrator sobre insights de alto impacto
            if insight.impact == 'high':
                notification = AgentMessage(
                    id=str(uuid4()),
                    sender_id=self.agent_id,
                    recipient_id="orchestrator_001",
                    message_type=MessageType.NOTIFICATION,
                    priority=Priority.HIGH,
                    content={
                        'notification_type': 'system_insight',
                        'insight': {
                            'id': insight.insight_id,
                            'type': insight.type,
                            'description': insight.description,
                            'recommendations': insight.recommendations
                        }
                    },
                    timestamp=datetime.now()
                )
                await self.message_bus.publish(notification)
    
    def _update_system_state(self):
        """Atualiza estado cognitivo do sistema"""
        recent_insights = [
            i for i in self.knowledge_base['insights']
            if (datetime.now() - i.timestamp).seconds < 300
        ]
        
        if len(recent_insights) > 5:
            # Muitos insights recentes - sistema em adaptação
            self.system_state = SystemState.ADAPTING
        elif self.learning_metrics['successful_optimizations'] > 10:
            # Otimizações bem-sucedidas - sistema estável
            self.system_state = SystemState.STABLE
        elif any(i.impact == 'high' for i in recent_insights):
            # Insights críticos - modo de otimização
            self.system_state = SystemState.OPTIMIZING
        else:
            # Estado padrão - aprendizado
            self.system_state = SystemState.LEARNING
    
    async def _evaluate_optimizations(self):
        """Avalia eficácia das otimizações aplicadas"""
        # Verificar otimizações recentes
        recent_optimizations = [
            opt for opt in self.knowledge_base['optimizations']
            if 'applied_at' in opt and (datetime.now() - opt['applied_at']).seconds < 600
        ]
        
        for optimization in recent_optimizations:
            if 'evaluated' not in optimization:
                # Coletar métricas pós-otimização
                current_data = await self._collect_system_data()
                
                # Comparar com baseline
                if 'baseline' in optimization:
                    improvement = self._calculate_improvement(
                        optimization['baseline'],
                        current_data,
                        optimization['target_metric']
                    )
                    
                    optimization['evaluated'] = True
                    optimization['improvement'] = improvement
                    
                    if improvement > 0.1:  # 10% de melhoria
                        self.learning_metrics['successful_optimizations'] += 1
                        logger.info(f"✅ Otimização {optimization['id']} bem-sucedida: {improvement:.1%} melhoria")
    
    def _update_correlations(self):
        """Atualiza correlações aprendidas entre eventos"""
        patterns = self.knowledge_base['patterns']
        
        if len(patterns) < 2:
            return
        
        # Analisar co-ocorrência de padrões
        for i in range(len(patterns) - 1):
            p1 = patterns[i]
            p2 = patterns[i + 1]
            
            # Verificar proximidade temporal
            if hasattr(p1, 'timestamp') and hasattr(p2, 'timestamp'):
                time_diff = (p2.timestamp - p1.timestamp).seconds
                if time_diff < 60:  # Padrões dentro de 1 minuto
                    correlation_key = f"{p1['type']}->{p2['type']}"
                    
                    if correlation_key not in self.knowledge_base['correlations']:
                        self.knowledge_base['correlations'][correlation_key] = {
                            'count': 0,
                            'confidence': 0.0
                        }
                    
                    self.knowledge_base['correlations'][correlation_key]['count'] += 1
                    self.knowledge_base['correlations'][correlation_key]['confidence'] = min(
                        0.95,
                        self.knowledge_base['correlations'][correlation_key]['confidence'] + self.learning_rate
                    )
    
    def _adapt_analysis_strategies(self):
        """Adapta estratégias de análise baseadas no aprendizado"""
        # Ajustar limiares baseados em padrões frequentes
        high_confidence_patterns = [
            p for p in self.knowledge_base['patterns']
            if p['confidence'] > 0.9
        ]
        
        if len(high_confidence_patterns) > 50:
            # Muitos padrões de alta confiança - pode aumentar limiar
            self.pattern_threshold = min(0.9, self.pattern_threshold + 0.05)
            logger.info(f"📊 Limiar de padrão ajustado para {self.pattern_threshold}")
        
        # Ajustar intervalo de análise baseado na atividade
        if self.learning_metrics['insights_generated'] > 100:
            # Sistema gerando muitos insights - pode reduzir frequência
            self.analysis_interval = min(120, self.analysis_interval + 10)
    
    async def _analyze_system_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza análise específica do sistema"""
        try:
            analysis_type = data.get('type', 'general')
            
            if analysis_type == 'performance':
                # Análise de performance
                patterns = [p for p in self.knowledge_base['patterns'] if 'performance' in p['type']]
                return {
                    'status': 'completed',
                    'analysis_type': 'performance',
                    'patterns_found': len(patterns),
                    'main_issues': [p['description'] for p in patterns[-5:]],
                    'recommendations': self._get_performance_recommendations()
                }
            
            elif analysis_type == 'reliability':
                # Análise de confiabilidade
                error_patterns = [p for p in self.knowledge_base['patterns'] if 'error' in p['type']]
                avg_error_rate = sum(p['data'].get('error_rate', 0) for p in error_patterns) / max(1, len(error_patterns))
                
                return {
                    'status': 'completed',
                    'analysis_type': 'reliability',
                    'error_patterns': len(error_patterns),
                    'average_error_rate': avg_error_rate,
                    'reliability_score': 1 - avg_error_rate,
                    'recommendations': self._get_reliability_recommendations()
                }
            
            else:
                # Análise geral
                return {
                    'status': 'completed',
                    'analysis_type': 'general',
                    'system_state': self.system_state.value,
                    'total_patterns': len(self.knowledge_base['patterns']),
                    'total_insights': len(self.knowledge_base['insights']),
                    'learning_metrics': self.learning_metrics
                }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise do sistema: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _get_recent_insights(self) -> Dict[str, Any]:
        """Retorna insights recentes"""
        recent = sorted(
            self.knowledge_base['insights'],
            key=lambda x: x.timestamp,
            reverse=True
        )[:10]
        
        return {
            'status': 'completed',
            'total_insights': len(self.knowledge_base['insights']),
            'recent_insights': [
                {
                    'id': i.insight_id,
                    'type': i.type,
                    'description': i.description,
                    'confidence': i.confidence,
                    'impact': i.impact,
                    'recommendations': i.recommendations,
                    'timestamp': i.timestamp.isoformat()
                }
                for i in recent
            ]
        }
    
    async def _get_optimization_recommendations(self) -> Dict[str, Any]:
        """Gera recomendações de otimização"""
        recommendations = []
        
        # Baseado em correlações aprendidas
        strong_correlations = [
            (k, v) for k, v in self.knowledge_base['correlations'].items()
            if v['confidence'] > 0.8
        ]
        
        for correlation, data in strong_correlations:
            parts = correlation.split('->')
            if len(parts) == 2:
                recommendations.append({
                    'type': 'correlation_based',
                    'description': f"Quando {parts[0]} ocorre, {parts[1]} tende a seguir",
                    'action': f"Preparar para {parts[1]} quando {parts[0]} for detectado",
                    'confidence': data['confidence']
                })
        
        # Baseado em padrões frequentes
        pattern_counts = defaultdict(int)
        for pattern in self.knowledge_base['patterns']:
            pattern_counts[pattern['type']] += 1
        
        most_common = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        for pattern_type, count in most_common:
            recommendations.append({
                'type': 'pattern_based',
                'description': f"Padrão '{pattern_type}' ocorre frequentemente ({count} vezes)",
                'action': self._get_action_for_pattern(pattern_type),
                'confidence': 0.7
            })
        
        return {
            'status': 'completed',
            'recommendations': recommendations,
            'optimization_count': len(self.knowledge_base['optimizations']),
            'success_rate': (
                self.learning_metrics['successful_optimizations'] /
                max(1, len(self.knowledge_base['optimizations']))
            )
        }
    
    def _get_cognitive_status(self) -> Dict[str, Any]:
        """Retorna status cognitivo do agente"""
        return {
            'status': 'active',
            'cognitive_state': self.system_state.value,
            'knowledge_base_size': {
                'patterns': len(self.knowledge_base['patterns']),
                'insights': len(self.knowledge_base['insights']),
                'optimizations': len(self.knowledge_base['optimizations']),
                'correlations': len(self.knowledge_base['correlations'])
            },
            'learning_metrics': self.learning_metrics,
            'analysis_interval': f"{self.analysis_interval} segundos",
            'pattern_threshold': self.pattern_threshold
        }
    
    def _calculate_improvement(self, baseline: Dict[str, Any], current: Dict[str, Any], metric: str) -> float:
        """Calcula melhoria percentual em uma métrica"""
        baseline_value = baseline.get(metric, 0)
        current_value = current.get(metric, 0)
        
        if baseline_value == 0:
            return 0.0
        
        return (current_value - baseline_value) / baseline_value
    
    def _get_performance_recommendations(self) -> List[str]:
        """Retorna recomendações específicas de performance"""
        return [
            "Implementar cache distribuído para resultados frequentes",
            "Otimizar algoritmos de roteamento de mensagens",
            "Considerar paralelização de tarefas independentes",
            "Monitorar e ajustar timeouts dinamicamente"
        ]
    
    def _get_reliability_recommendations(self) -> List[str]:
        """Retorna recomendações específicas de confiabilidade"""
        return [
            "Implementar circuit breakers para serviços instáveis",
            "Adicionar retry logic com backoff exponencial",
            "Melhorar validação de entrada de dados",
            "Implementar health checks mais granulares"
        ]
    
    def _get_action_for_pattern(self, pattern_type: str) -> str:
        """Retorna ação recomendada para um tipo de padrão"""
        actions = {
            'high_load': "Ativar auto-scaling ou distribuir carga",
            'high_error_rate': "Investigar causas raiz e implementar correções",
            'low_performance': "Otimizar gargalos identificados",
            'memory_pressure': "Implementar garbage collection agressiva",
            'network_congestion': "Otimizar protocolos de comunicação"
        }
        
        return actions.get(pattern_type, "Monitorar e coletar mais dados")
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
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

# Importações necessárias
from uuid import uuid4

def create_meta_cognitive_agents(message_bus) -> List:
    """
    Cria agentes meta-cognitivos
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        
    Returns:
        Lista com exatamente 2 agentes meta-cognitivos
    """
    agents = []
    
    try:
        logger.info("🧠 Criando agentes Meta-Cognitivos...")
        
        # Verificar agentes existentes
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        # Criar Orchestrator
        if "orchestrator_001" not in existing_agents:
            try:
                orchestrator = OrchestratorAgent("orchestrator_001", AgentType.ORCHESTRATOR, message_bus)
                agents.append(orchestrator)
                
                # Iniciar serviços de orquestração
                asyncio.create_task(orchestrator.start_orchestration())
                
                logger.info(f"👑 orchestrator_001 criado como Orquestrador Supremo")
                logger.info(f"   └── Capabilities: {', '.join(orchestrator.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando orchestrator_001: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning("⚠️ orchestrator_001 já existe - pulando")
        
        # Criar MetaCognitive
        if "metacognitive_001" not in existing_agents:
            try:
                metacognitive = MetaCognitiveAgent("metacognitive_001", AgentType.META_COGNITIVE, message_bus)
                agents.append(metacognitive)
                
                # Iniciar processos meta-cognitivos
                asyncio.create_task(metacognitive.start_meta_cognition())
                
                logger.info(f"🧠 metacognitive_001 criado com capacidades meta-cognitivas")
                logger.info(f"   └── Capabilities: {', '.join(metacognitive.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando metacognitive_001: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning("⚠️ metacognitive_001 já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agentes Meta-Cognitivos criados com sucesso")
        
        # Validar quantidade
        if len(agents) != 2:
            logger.warning(f"⚠️ Esperado 2 agentes, criados {len(agents)}")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando agentes Meta-Cognitivos: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
