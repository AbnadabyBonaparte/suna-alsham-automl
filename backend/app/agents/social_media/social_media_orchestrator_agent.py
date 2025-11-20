"""
Social Media Orchestrator Agent - ALSHAM QUANTUM Native
Orquestrador central para coordenação de workflows de mídia social
Versão: 2.1.0 - Nativa (sem dependências SUNA-ALSHAM)
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import uuid
from collections import defaultdict, deque

# Base Agent Implementation
class BaseNetworkAgent:
    """Base class para agentes do ALSHAM QUANTUM Network"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.logger = logging.getLogger(f"ALSHAM.{agent_id}")
        self.status = "initialized"
        self.metrics = {
            'tasks_processed': 0,
            'success_rate': 0.0,
            'avg_processing_time': 0.0,
            'last_activity': None
        }
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma requisição"""
        raise NotImplementedError("Subclasses devem implementar process_request")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            'agent_id': self.agent_id,
            'status': self.status,
            'metrics': self.metrics.copy()
        }

# Enums e Classes de Dados
class WorkflowType(Enum):
    CONTENT_CREATION = "content_creation"
    ENGAGEMENT_CAMPAIGN = "engagement_campaign"
    INFLUENCER_OUTREACH = "influencer_outreach"
    VIDEO_AUTOMATION = "video_automation"
    ANALYTICS_REPORT = "analytics_report"
    CRISIS_MANAGEMENT = "crisis_management"
    BRAND_MONITORING = "brand_monitoring"

class WorkflowStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    URGENT = 5

@dataclass
class WorkflowStep:
    step_id: str
    agent_id: str
    action: str
    parameters: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3

@dataclass
class Workflow:
    workflow_id: str
    workflow_type: WorkflowType
    title: str
    description: str
    steps: List[WorkflowStep]
    priority: Priority = Priority.MEDIUM
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    client_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    progress: float = 0.0
    estimated_completion: Optional[datetime] = None

@dataclass
class AgentCapability:
    agent_id: str
    capabilities: List[str]
    max_concurrent_tasks: int = 3
    average_processing_time: float = 30.0
    reliability_score: float = 1.0
    is_available: bool = True
    current_load: int = 0

class SocialMediaOrchestratorAgent(BaseNetworkAgent):
    """
    Orquestrador Central de Workflows de Mídia Social
    
    Responsabilidades:
    - Coordenação de workflows multi-agente
    - Roteamento inteligente de tarefas
    - Monitoramento de progresso
    - Otimização de recursos
    - Analytics consolidados
    """
    
    def __init__(self, agent_id: str = "social_media_orchestrator", config: Dict[str, Any] = None):
        super().__init__(agent_id, config)
        
        # Core Components
        self.active_workflows: Dict[str, Workflow] = {}
        self.workflow_history: deque = deque(maxlen=1000)
        self.agent_registry: Dict[str, AgentCapability] = {}
        self.task_queue: List[Tuple[str, WorkflowStep]] = []
        self.performance_metrics = defaultdict(list)
        
        # Configuration
        self.max_concurrent_workflows = config.get('max_concurrent_workflows', 10)
        self.workflow_timeout = config.get('workflow_timeout', 3600)
        self.health_check_interval = config.get('health_check_interval', 60)
        
        # Initialize agent registry
        self._initialize_agent_registry()
        
        self.logger.info("🎭 Social Media Orchestrator Agent inicializado")

    def _initialize_agent_registry(self):
        """Inicializa registro de agentes disponíveis"""
        self.agent_registry = {
            'content_creator_agent': AgentCapability(
                agent_id='content_creator_agent',
                capabilities=['create_post', 'generate_content', 'optimize_content'],
                max_concurrent_tasks=5,
                average_processing_time=45.0,
                reliability_score=0.95
            ),
            'engagement_maximizer_agent': AgentCapability(
                agent_id='engagement_maximizer_agent',
                capabilities=['optimize_engagement', 'schedule_posts', 'analyze_timing'],
                max_concurrent_tasks=8,
                average_processing_time=25.0,
                reliability_score=0.98
            ),
            'influencer_network_agent': AgentCapability(
                agent_id='influencer_network_agent',
                capabilities=['find_influencers', 'manage_partnerships', 'track_campaigns'],
                max_concurrent_tasks=4,
                average_processing_time=60.0,
                reliability_score=0.92
            ),
            'video_automation_agent': AgentCapability(
                agent_id='video_automation_agent',
                capabilities=['create_video', 'edit_video', 'optimize_video'],
                max_concurrent_tasks=2,
                average_processing_time=120.0,
                reliability_score=0.88
            ),
            'analytics_orchestrator_agent': AgentCapability(
                agent_id='analytics_orchestrator_agent',
                capabilities=['generate_reports', 'analyze_performance', 'track_metrics'],
                max_concurrent_tasks=6,
                average_processing_time=30.0,
                reliability_score=0.99
            )
        }

    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisições de orquestração"""
        try:
            self.logger.info(f"🎯 Processando requisição: {request.get('action', 'unknown')}")
            
            action = request.get('action', '')
            
            if action == 'create_workflow':
                return await self._create_workflow(request.get('workflow_data', {}))
            elif action == 'get_workflow_status':
                return await self._get_workflow_status(request.get('workflow_id'))
            elif action == 'cancel_workflow':
                return await self._cancel_workflow(request.get('workflow_id'))
            elif action == 'get_dashboard':
                return await self._generate_dashboard()
            elif action == 'optimize_resources':
                return await self._optimize_resources()
            elif action == 'get_performance_metrics':
                return await self._get_performance_metrics()
            else:
                return await self._handle_unknown_action(action, request)
                
        except Exception as e:
            self.logger.error(f"❌ Erro no processamento: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _create_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria e executa um novo workflow"""
        try:
            # Validate workflow data
            if not self._validate_workflow_data(workflow_data):
                return {
                    'success': False,
                    'error': 'Dados de workflow inválidos',
                    'timestamp': datetime.now().isoformat()
                }
            
            workflow = self._build_workflow(workflow_data)
            
            # Check resource availability
            if not self._check_resource_availability(workflow):
                return {
                    'success': False,
                    'error': 'Recursos insuficientes para executar workflow',
                    'estimated_wait_time': self._calculate_wait_time(),
                    'timestamp': datetime.now().isoformat()
                }
            
            # Register workflow
            self.active_workflows[workflow.workflow_id] = workflow
            
            # Start execution
            asyncio.create_task(self._execute_workflow(workflow))
            
            self.logger.info(f"🚀 Workflow criado: {workflow.workflow_id}")
            
            return {
                'success': True,
                'workflow_id': workflow.workflow_id,
                'status': workflow.status.value,
                'estimated_completion': workflow.estimated_completion.isoformat() if workflow.estimated_completion else None,
                'steps_count': len(workflow.steps),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro na criação do workflow: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _build_workflow(self, workflow_data: Dict[str, Any]) -> Workflow:
        """Constrói um workflow baseado nos dados fornecidos"""
        workflow_id = str(uuid.uuid4())
        workflow_type = WorkflowType(workflow_data['type'])
        
        # Build steps based on workflow type
        steps = self._generate_workflow_steps(workflow_type, workflow_data)
        
        # Calculate estimated completion
        estimated_completion = self._calculate_estimated_completion(steps)
        
        return Workflow(
            workflow_id=workflow_id,
            workflow_type=workflow_type,
            title=workflow_data.get('title', f'Workflow {workflow_type.value}'),
            description=workflow_data.get('description', ''),
            steps=steps,
            priority=Priority(workflow_data.get('priority', 2)),
            deadline=datetime.fromisoformat(workflow_data['deadline']) if workflow_data.get('deadline') else None,
            client_id=workflow_data.get('client_id'),
            metadata=workflow_data.get('metadata', {}),
            estimated_completion=estimated_completion
        )

    def _generate_workflow_steps(self, workflow_type: WorkflowType, data: Dict[str, Any]) -> List[WorkflowStep]:
        """Gera steps específicos para cada tipo de workflow"""
        steps = []
        
        if workflow_type == WorkflowType.CONTENT_CREATION:
            steps = [
                WorkflowStep(
                    step_id="content_generation",
                    agent_id="content_creator_agent",
                    action="generate_content",
                    parameters=data.get('content_params', {})
                ),
                WorkflowStep(
                    step_id="content_optimization",
                    agent_id="engagement_maximizer_agent",
                    action="optimize_timing",
                    parameters=data.get('timing_params', {}),
                    dependencies=["content_generation"]
                )
            ]
        
        elif workflow_type == WorkflowType.VIDEO_AUTOMATION:
            steps = [
                WorkflowStep(
                    step_id="video_creation",
                    agent_id="video_automation_agent",
                    action="create_video",
                    parameters=data.get('video_params', {})
                ),
                WorkflowStep(
                    step_id="video_optimization",
                    agent_id="video_automation_agent",
                    action="optimize_video",
                    parameters=data.get('optimization_params', {}),
                    dependencies=["video_creation"]
                ),
                WorkflowStep(
                    step_id="schedule_video",
                    agent_id="engagement_maximizer_agent",
                    action="schedule_post",
                    parameters=data.get('schedule_params', {}),
                    dependencies=["video_optimization"]
                )
            ]
        
        elif workflow_type == WorkflowType.INFLUENCER_OUTREACH:
            steps = [
                WorkflowStep(
                    step_id="influencer_research",
                    agent_id="influencer_network_agent",
                    action="find_influencers",
                    parameters=data.get('research_params', {})
                ),
                WorkflowStep(
                    step_id="outreach_campaign",
                    agent_id="influencer_network_agent",
                    action="create_campaign",
                    parameters=data.get('campaign_params', {}),
                    dependencies=["influencer_research"]
                )
            ]
        
        elif workflow_type == WorkflowType.ANALYTICS_REPORT:
            steps = [
                WorkflowStep(
                    step_id="data_collection",
                    agent_id="analytics_orchestrator_agent",
                    action="collect_metrics",
                    parameters=data.get('collection_params', {})
                ),
                WorkflowStep(
                    step_id="report_generation",
                    agent_id="analytics_orchestrator_agent",
                    action="generate_report",
                    parameters=data.get('report_params', {}),
                    dependencies=["data_collection"]
                )
            ]
        
        # Add unique step IDs
        for i, step in enumerate(steps):
            step.step_id = f"{step.step_id}_{i+1}"
        
        return steps

    async def _execute_workflow(self, workflow: Workflow):
        """Executa um workflow de forma assíncrona"""
        try:
            workflow.status = WorkflowStatus.IN_PROGRESS
            workflow.started_at = datetime.now()
            
            self.logger.info(f"🎬 Iniciando execução do workflow: {workflow.workflow_id}")
            
            while not self._is_workflow_complete(workflow):
                # Execute ready steps
                ready_steps = self._get_ready_steps(workflow)
                
                if ready_steps:
                    await self._execute_steps_parallel(workflow, ready_steps)
                else:
                    # Wait for dependencies
                    await asyncio.sleep(1)
                
                # Update progress
                workflow.progress = self._calculate_progress(workflow)
                
                # Check timeout
                if self._is_workflow_timeout(workflow):
                    workflow.status = WorkflowStatus.FAILED
                    self.logger.warning(f"⏰ Timeout no workflow: {workflow.workflow_id}")
                    break
            
            # Finalize workflow
            if workflow.status != WorkflowStatus.FAILED:
                workflow.status = WorkflowStatus.COMPLETED
                workflow.progress = 100.0
            
            workflow.completed_at = datetime.now()
            
            # Move to history
            self.workflow_history.append(workflow)
            if workflow.workflow_id in self.active_workflows:
                del self.active_workflows[workflow.workflow_id]
            
            self.logger.info(f"✅ Workflow concluído: {workflow.workflow_id} - Status: {workflow.status.value}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro na execução do workflow {workflow.workflow_id}: {e}")
            workflow.status = WorkflowStatus.FAILED
            workflow.completed_at = datetime.now()

    async def _execute_steps_parallel(self, workflow: Workflow, steps: List[WorkflowStep]):
        """Executa steps em paralelo quando possível"""
        tasks = []
        
        for step in steps:
            if self._can_execute_step(step):
                task = asyncio.create_task(self._execute_single_step(workflow, step))
                tasks.append(task)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _execute_single_step(self, workflow: Workflow, step: WorkflowStep):
        """Executa um step individual"""
        try:
            step.status = WorkflowStatus.IN_PROGRESS
            step.started_at = datetime.now()
            
            # Update agent load
            if step.agent_id in self.agent_registry:
                self.agent_registry[step.agent_id].current_load += 1
            
            self.logger.info(f"🔧 Executando step: {step.step_id} com {step.agent_id}")
            
            # Simulate agent execution (in real implementation, call actual agents)
            result = await self._simulate_agent_call(step)
            
            step.result = result
            step.status = WorkflowStatus.COMPLETED
            step.completed_at = datetime.now()
            
            # Update metrics
            self._update_step_metrics(step)
            
        except Exception as e:
            step.error_message = str(e)
            
            if step.retry_count < step.max_retries:
                step.retry_count += 1
                step.status = WorkflowStatus.PENDING
                self.logger.warning(f"🔄 Retentativa {step.retry_count} para step: {step.step_id}")
            else:
                step.status = WorkflowStatus.FAILED
                self.logger.error(f"❌ Falha no step: {step.step_id} - {e}")
        
        finally:
            # Update agent load
            if step.agent_id in self.agent_registry:
                self.agent_registry[step.agent_id].current_load = max(0, 
                    self.agent_registry[step.agent_id].current_load - 1)

    async def _simulate_agent_call(self, step: WorkflowStep) -> Dict[str, Any]:
        """Simula chamada para agente (substituir por chamada real)"""
        # Simulate processing time based on agent capabilities
        if step.agent_id in self.agent_registry:
            processing_time = self.agent_registry[step.agent_id].average_processing_time
            # Add some randomization
            processing_time *= (0.8 + 0.4 * hash(step.step_id) % 100 / 100)
            await asyncio.sleep(min(processing_time / 10, 5))  # Scale down for simulation
        
        # Return mock result
        return {
            'success': True,
            'step_id': step.step_id,
            'agent_id': step.agent_id,
            'action': step.action,
            'result_data': f"Resultado simulado para {step.action}",
            'execution_time': (datetime.now() - step.started_at).total_seconds(),
            'timestamp': datetime.now().isoformat()
        }

    async def _generate_dashboard(self) -> Dict[str, Any]:
        """Gera dashboard consolidado"""
        try:
            total_workflows = len(self.active_workflows) + len(self.workflow_history)
            active_count = len(self.active_workflows)
            completed_count = sum(1 for w in self.workflow_history if w.status == WorkflowStatus.COMPLETED)
            failed_count = sum(1 for w in self.workflow_history if w.status == WorkflowStatus.FAILED)
            
            # Agent utilization
            agent_utilization = {}
            for agent_id, capability in self.agent_registry.items():
                utilization_rate = capability.current_load / capability.max_concurrent_tasks
                agent_utilization[agent_id] = {
                    'current_load': capability.current_load,
                    'max_capacity': capability.max_concurrent_tasks,
                    'utilization_rate': round(utilization_rate * 100, 2),
                    'reliability_score': capability.reliability_score,
                    'is_available': capability.is_available
                }
            
            # Recent performance
            recent_workflows = list(self.workflow_history)[-10:]
            avg_completion_time = 0
            if recent_workflows:
                completion_times = [
                    (w.completed_at - w.started_at).total_seconds() 
                    for w in recent_workflows 
                    if w.completed_at and w.started_at
                ]
                if completion_times:
                    avg_completion_time = sum(completion_times) / len(completion_times)
            
            dashboard = {
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_workflows': total_workflows,
                    'active_workflows': active_count,
                    'completed_workflows': completed_count,
                    'failed_workflows': failed_count,
                    'success_rate': round((completed_count / max(total_workflows, 1)) * 100, 2),
                    'avg_completion_time_seconds': round(avg_completion_time, 2)
                },
                'agent_utilization': agent_utilization,
                'active_workflows_detail': [
                    {
                        'workflow_id': w.workflow_id,
                        'type': w.workflow_type.value,
                        'title': w.title,
                        'status': w.status.value,
                        'progress': round(w.progress, 2),
                        'priority': w.priority.value,
                        'created_at': w.created_at.isoformat(),
                        'estimated_completion': w.estimated_completion.isoformat() if w.estimated_completion else None
                    }
                    for w in list(self.active_workflows.values())[:10]  # Top 10
                ],
                'system_health': {
                    'orchestrator_status': self.status,
                    'total_agents_registered': len(self.agent_registry),
                    'agents_available': sum(1 for a in self.agent_registry.values() if a.is_available),
                    'system_load': self._calculate_system_load(),
                    'last_health_check': datetime.now().isoformat()
                }
            }
            
            return {
                'success': True,
                'dashboard': dashboard,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro na geração do dashboard: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _calculate_system_load(self) -> float:
        """Calcula carga geral do sistema"""
        if not self.agent_registry:
            return 0.0
        
        total_load = sum(agent.current_load for agent in self.agent_registry.values())
        total_capacity = sum(agent.max_concurrent_tasks for agent in self.agent_registry.values())
        
        return round((total_load / max(total_capacity, 1)) * 100, 2)

    # Utility Methods
    def _validate_workflow_data(self, data: Dict[str, Any]) -> bool:
        """Valida dados do workflow"""
        required_fields = ['type', 'title']
        return all(field in data for field in required_fields)
    
    def _check_resource_availability(self, workflow: Workflow) -> bool:
        """Verifica disponibilidade de recursos"""
        required_agents = set(step.agent_id for step in workflow.steps)
        
        for agent_id in required_agents:
            if agent_id not in self.agent_registry:
                return False
            
            agent = self.agent_registry[agent_id]
            if not agent.is_available or agent.current_load >= agent.max_concurrent_tasks:
                return False
        
        return True
    
    def _calculate_wait_time(self) -> int:
        """Calcula tempo estimado de espera"""
        return 300  # 5 minutes default
    
    def _is_workflow_complete(self, workflow: Workflow) -> bool:
        """Verifica se workflow está completo"""
        return all(
            step.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED] 
            for step in workflow.steps
        )
    
    def _get_ready_steps(self, workflow: Workflow) -> List[WorkflowStep]:
        """Retorna steps prontos para execução"""
        ready_steps = []
        completed_steps = {
            step.step_id for step in workflow.steps 
            if step.status == WorkflowStatus.COMPLETED
        }
        
        for step in workflow.steps:
            if (step.status == WorkflowStatus.PENDING and 
                all(dep in completed_steps for dep in step.dependencies)):
                ready_steps.append(step)
        
        return ready_steps
    
    def _can_execute_step(self, step: WorkflowStep) -> bool:
        """Verifica se step pode ser executado"""
        if step.agent_id not in self.agent_registry:
            return False
        
        agent = self.agent_registry[step.agent_id]
        return (agent.is_available and 
                agent.current_load < agent.max_concurrent_tasks)
    
    def _calculate_progress(self, workflow: Workflow) -> float:
        """Calcula progresso do workflow"""
        if not workflow.steps:
            return 0.0
        
        completed = sum(1 for step in workflow.steps if step.status == WorkflowStatus.COMPLETED)
        return (completed / len(workflow.steps)) * 100
    
    def _is_workflow_timeout(self, workflow: Workflow) -> bool:
        """Verifica timeout do workflow"""
        if not workflow.started_at:
            return False
        
        elapsed = (datetime.now() - workflow.started_at).total_seconds()
        return elapsed > self.workflow_timeout
    
    def _calculate_estimated_completion(self, steps: List[WorkflowStep]) -> datetime:
        """Calcula tempo estimado de conclusão"""
        total_time = 0
        
        for step in steps:
            if step.agent_id in self.agent_registry:
                agent = self.agent_registry[step.agent_id]
                total_time += agent.average_processing_time
        
        return datetime.now() + timedelta(seconds=total_time)
    
    def _update_step_metrics(self, step: WorkflowStep):
        """Atualiza métricas do step"""
        if step.completed_at and step.started_at:
            execution_time = (step.completed_at - step.started_at).total_seconds()
            self.performance_metrics[step.agent_id].append(execution_time)
    
    async def _get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Retorna status de um workflow específico"""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
        else:
            # Search in history
            workflow = next((w for w in self.workflow_history if w.workflow_id == workflow_id), None)
        
        if not workflow:
            return {
                'success': False,
                'error': 'Workflow não encontrado',
                'timestamp': datetime.now().isoformat()
            }
        
        return {
            'success': True,
            'workflow': {
                'workflow_id': workflow.workflow_id,
                'type': workflow.workflow_type.value,
                'title': workflow.title,
                'status': workflow.status.value,
                'progress': round(workflow.progress, 2),
                'priority': workflow.priority.value,
                'created_at': workflow.created_at.isoformat(),
                'started_at': workflow.started_at.isoformat() if workflow.started_at else None,
                'completed_at': workflow.completed_at.isoformat() if workflow.completed_at else None,
                'estimated_completion': workflow.estimated_completion.isoformat() if workflow.estimated_completion else None,
                'steps': [
                    {
                        'step_id': step.step_id,
                        'agent_id': step.agent_id,
                        'action': step.action,
                        'status': step.status.value,
                        'retry_count': step.retry_count,
                        'error_message': step.error_message
                    }
                    for step in workflow.steps
                ]
            },
            'timestamp': datetime.now().isoformat()
        }
    
    async def _cancel_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Cancela um workflow ativo"""
        if workflow_id not in self.active_workflows:
            return {
                'success': False,
                'error': 'Workflow não encontrado ou não está ativo',
                'timestamp': datetime.now().isoformat()
            }
        
        workflow = self.active_workflows[workflow_id]
        workflow.status = WorkflowStatus.CANCELLED
        workflow.completed_at = datetime.now()
        
        # Cancel pending steps
        for step in workflow.steps:
            if step.status == WorkflowStatus.PENDING:
                step.status = WorkflowStatus.CANCELLED
        
        # Move to history
        self.workflow_history.append(workflow)
        del self.active_workflows[workflow_id]
        
        return {
            'success': True,
            'message': f'Workflow {workflow_id} cancelado com sucesso',
            'timestamp': datetime.now().isoformat()
        }
    
    async def _optimize_resources(self) -> Dict[str, Any]:
        """Otimiza alocação de recursos"""
        optimizations = []
        
        # Identify overloaded agents
        for agent_id, agent in self.agent_registry.items():
            utilization = agent.current_load / agent.max_concurrent_tasks
            
            if utilization > 0.8:
                optimizations.append({
                    'agent_id': agent_id,
                    'issue': 'high_utilization',
                    'current_load': agent.current_load,
                    'recommendation': 'Consider load balancing or scaling'
                })
        
        # Check for idle agents
        idle_agents = [
            agent_id for agent_id, agent in self.agent_registry.items()
            if agent.current_load == 0 and agent.is_available
        ]
        
        if idle_agents:
            optimizations.append({
                'type': 'idle_resources',
                'agents': idle_agents,
                'recommendation': 'Consider reassigning workflows to idle agents'
            })
        
        return {
            'success': True,
            'optimizations': optimizations,
            'system_load': self._calculate_system_load(),
            'timestamp': datetime.now().isoformat()
        }
    
    async def _get_performance_metrics(self) -> Dict[str, Any]:
        """Retorna métricas de performance"""
        metrics = {}
        
        for agent_id, execution_times in self.performance_metrics.items():
            if execution_times:
                metrics[agent_id] = {
                    'avg_execution_time': round(sum(execution_times) / len(execution_times), 2),
                    'min_execution_time': round(min(execution_times), 2),
                    'max_execution_time': round(max(execution_times), 2),
                    'total_executions': len(execution_times)
                }
        
        return {
            'success': True,
            'performance_metrics': metrics,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _handle_unknown_action(self, action: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Trata ações não reconhecidas"""
        return {
            'success': False,
            'error': f'Ação não reconhecida: {action}',
            'available_actions': [
                'create_workflow',
                'get_workflow_status', 
                'cancel_workflow',
                'get_dashboard',
                'optimize_resources',
                'get_performance_metrics'
            ],
            'timestamp': datetime.now().isoformat()
        }

def create_agents(config: Dict[str, Any] = None) -> Dict[str, BaseNetworkAgent]:
    """
    Factory function para criar instâncias dos agentes do módulo Social Media
    
    Returns:
        Dict[str, BaseNetworkAgent]: Dicionário com instâncias dos agentes
    """
    config = config or {}
    
    agents = {
        'social_media_orchestrator': SocialMediaOrchestratorAgent(
            agent_id="social_media_orchestrator_agent",
            config=config.get('orchestrator', {})
        )
    }
    
    # Log da criação
    logger = logging.getLogger("ALSHAM.SocialMedia")
    logger.info(f"🎭 Social Media Orchestrator Agent criado - Total: {len(agents)} agentes")
    
    return agents

# Export para compatibilidade
__all__ = [
    'SocialMediaOrchestratorAgent',
    'BaseNetworkAgent', 
    'create_agents',
    'WorkflowType',
    'WorkflowStatus',
    'Priority',
    'Workflow',
    'WorkflowStep',
    'AgentCapability'
]

if __name__ == "__main__":
    # Test básico
    import asyncio
    
    async def test_orchestrator():
        agent = SocialMediaOrchestratorAgent()
        
        # Test workflow creation
        workflow_data = {
            'type': 'content_creation',
            'title': 'Campanha de Verão 2024',
            'description': 'Criação de conteúdo para campanha de verão',
            'priority': 3,
            'content_params': {
                'theme': 'summer',
                'target_audience': 'young_adults',
                'platforms': ['instagram', 'facebook', 'tiktok']
            }
        }
        
        result = await agent.process_request({
            'action': 'create_workflow',
            'workflow_data': workflow_data
        })
        
        print(f"✅ Resultado do teste: {result}")
        
        # Test dashboard
        dashboard = await agent.process_request({
            'action': 'get_dashboard'
        })
        
        print(f"📊 Dashboard: {dashboard['dashboard']['summary']}")
    
    asyncio.run(test_orchestrator())
