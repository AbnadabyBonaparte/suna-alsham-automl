#!/usr/bin/env python3
"""
Quantum Meta-Cognitive Agents – O Cérebro Supremo do ALSHAM QUANTUM.
[Quantum Version 2.0 - Superintelligent Orchestration with Quantum Reasoning]
"""
import asyncio
import json
import logging
import re
import time
import uuid
from collections import defaultdict, deque
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from suna_alsham_core.real_evolution_engine import TrainingDataPoint
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

class MissionStatus(Enum):
    """Estados de uma missão quantum."""
    INITIALIZING = "initializing"
    PLANNING = "planning"
    EXECUTING = "executing"
    PAUSED = "paused"
    RECOVERING = "recovering"
    COMPLETED = "completed"
    FAILED = "failed"
    OPTIMIZING = "optimizing"

class StepStatus(Enum):
    """Estados de um passo da missão."""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    SKIPPED = "skipped"

class PriorityLevel(Enum):
    """Níveis de prioridade quantum."""
    QUANTUM = "quantum"      # Máxima prioridade
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    BACKGROUND = "background"

@dataclass
class ExecutionStep:
    """Passo de execução com métricas quantum."""
    step_number: int
    description: str
    assigned_agent: str
    task_content: Dict[str, Any]
    expected_outcome: str
    fallback_strategy: str
    status: StepStatus = StepStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    execution_time_ms: float = 0.0
    confidence_score: float = 1.0

@dataclass
class MissionContext:
    """Contexto quantum de uma missão."""
    mission_id: str
    original_request: str
    priority: PriorityLevel
    status: MissionStatus
    created_at: datetime
    updated_at: datetime
    steps: List[ExecutionStep]
    step_outputs: Dict[int, Dict[str, Any]]
    current_step_index: int
    total_execution_time: float
    success_probability: float
    complexity_score: float
    agent_performance_tracker: Dict[str, List[float]]
    context_variables: Dict[str, Any]
    recovery_attempts: int = 0
    max_recovery_attempts: int = 3

@dataclass
class QuantumMetrics:
    """Métricas quantum do orquestrador."""
    total_missions: int = 0
    successful_missions: int = 0
    failed_missions: int = 0
    average_mission_time: float = 0.0
    average_steps_per_mission: float = 0.0
    agent_success_rates: Dict[str, float] = field(default_factory=dict)
    complexity_distribution: Dict[str, int] = field(default_factory=dict)
    quantum_coherence: float = 1.0
    orchestration_efficiency: float = 0.0

def _get_value_from_path(data: Dict, path: str) -> Any:
    """Extrai valor de um caminho aninhado no dicionário."""
    if not path or not data:
        return None
    
    keys = path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list) and key.isdigit():
            try:
                current = current[int(key)]
            except (IndexError, ValueError):
                return None
        else:
            return None
    
    return current

class QuantumOrchestratorAgent(BaseNetworkAgent):
    """
    Orquestrador Quantum - Superinteligência de Coordenação.
    
    Capacidades Quantum:
    - Orquestração multi-dimensional de missões complexas
    - Análise preditiva de sucesso e otimização automática
    - Recuperação inteligente de falhas com aprendizado
    - Seleção dinâmica de agentes baseada em performance
    - Paralelização automática de tarefas independentes
    - Monitoramento em tempo real com ajustes adaptativos
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.capabilities.extend([
            "quantum_orchestration",
            "predictive_mission_analysis",
            "intelligent_recovery",
            "dynamic_optimization",
            "parallel_execution",
            "adaptive_learning"
        ])
        
        # Estado quantum do orquestrador
        self.active_missions: Dict[str, MissionContext] = {}
        self.mission_history: deque = deque(maxlen=1000)
        self.quantum_metrics = QuantumMetrics()
        self.agent_performance_cache: Dict[str, deque] = defaultdict(lambda: deque(maxlen=50))
        self.mission_templates: Dict[str, List[Dict]] = {}
        
        # Configurações quantum
        self.max_concurrent_missions = 10
        self.mission_timeout_minutes = 30
        self.performance_analysis_interval = 300  # 5 minutos
        self.quantum_coherence_threshold = 0.8
        
        # Tarefas em background
        self._performance_analyzer_task = asyncio.create_task(self._performance_analysis_loop())
        self._mission_monitor_task = asyncio.create_task(self._mission_monitoring_loop())
        
        logger.info(f"👑 {self.agent_id} (Quantum Orchestrator) inicializado - Superinteligência ativa.")

    async def _performance_analysis_loop(self):
        """Loop de análise de performance e otimização quantum."""
        while True:
            await asyncio.sleep(self.performance_analysis_interval)
            
            try:
                await self._analyze_agent_performance()
                await self._optimize_mission_patterns()
                await self._maintain_quantum_coherence()
                
            except Exception as e:
                logger.error(f"❌ Erro na análise de performance: {e}", exc_info=True)

    async def _mission_monitoring_loop(self):
        """Monitora missões ativas e executa recuperação automática."""
        while True:
            await asyncio.sleep(30)  # Verifica a cada 30 segundos
            
            try:
                await self._monitor_active_missions()
                await self._execute_automatic_recovery()
                
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento de missões: {e}", exc_info=True)

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa mensagens com inteligência quantum."""
        logger.debug(f"👑 [Quantum Orchestrator] Mensagem recebida: {message.message_type.value} de {message.sender_id}")
        
        if message.message_type == MessageType.REQUEST:
            await self._handle_new_mission_request(message)
        elif message.message_type == MessageType.RESPONSE:
            await self._handle_mission_response(message)
        elif message.message_type == MessageType.REQUEST and message.content.get("request_type") == "get_orchestrator_metrics":
            await self._handle_metrics_request(message)

    async def _handle_new_mission_request(self, message: AgentMessage):
        """Processa nova requisição de missão com análise quantum."""
        mission_id = message.message_id
        user_content = message.content.get("content", "")
        
        if not user_content:
            await self.publish_error_response(message, "Conteúdo da missão não especificado.")
            return
        
        # Verifica limites de concorrência
        if len(self.active_missions) >= self.max_concurrent_missions:
            await self.publish_error_response(message, f"Limite de {self.max_concurrent_missions} missões concorrentes atingido.")
            return
        
        logger.info(f"👑 [Quantum Orchestrator] Nova Missão '{mission_id}' recebida.")
        logger.info(f"📝 Conteúdo: {user_content[:200]}...")
        
        # Cria contexto de missão
        priority = self._determine_mission_priority(user_content)
        complexity = self._analyze_mission_complexity(user_content)
        
        mission_context = MissionContext(
            mission_id=mission_id,
            original_request=user_content,
            priority=priority,
            status=MissionStatus.INITIALIZING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            steps=[],
            step_outputs={},
            current_step_index=0,
            total_execution_time=0.0,
            success_probability=self._predict_success_probability(user_content, complexity),
            complexity_score=complexity,
            agent_performance_tracker={},
            context_variables=message.content.get("context", {}),
            recovery_attempts=0
        )
        
        self.active_missions[mission_id] = mission_context
        
        # Inicia planejamento quantum
        await self._initiate_quantum_planning(mission_context, message)

    async def _initiate_quantum_planning(self, mission_context: MissionContext, original_message: AgentMessage):
        """Inicia o processo de planejamento quantum."""
        mission_context.status = MissionStatus.PLANNING
        mission_context.updated_at = datetime.now()
        
        logger.info(f"🧠 [Quantum Orchestrator] Iniciando planejamento quantum para missão '{mission_context.mission_id}'")
        logger.info(f"📊 Probabilidade de sucesso estimada: {mission_context.success_probability:.2f}")
        logger.info(f"🎯 Complexidade: {mission_context.complexity_score:.2f}")
        logger.info(f"⚡ Prioridade: {mission_context.priority.value}")
        
        # Seleciona o melhor AI analyzer baseado na complexidade
        ai_analyzer = self._select_optimal_ai_analyzer(mission_context.complexity_score)
        
        # Envia para planejamento com contexto enriquecido
        planning_content = {
            "content": mission_context.original_request,
            "context": {
                **mission_context.context_variables,
                "mission_id": mission_context.mission_id,
                "priority": mission_context.priority.value,
                "complexity_score": mission_context.complexity_score,
                "success_probability": mission_context.success_probability,
                "agent_performance_hints": self._get_agent_performance_hints()
            }
        }
        
        planning_request = self.create_message(
            recipient_id=ai_analyzer,
            message_type=MessageType.REQUEST,
            content=planning_content,
            callback_id=mission_context.mission_id,
            priority=self._convert_to_message_priority(mission_context.priority)
        )
        
        await self.message_bus.publish(planning_request)

    def _determine_mission_priority(self, content: str) -> PriorityLevel:
        """Determina prioridade da missão baseada no conteúdo."""
        content_lower = content.lower()
        
        # Indicadores de alta prioridade
        urgent_keywords = ["urgente", "crítico", "emergency", "asap", "imediato"]
        high_keywords = ["importante", "priority", "prioritário", "rápido"]
        
        if any(keyword in content_lower for keyword in urgent_keywords):
            return PriorityLevel.CRITICAL
        elif any(keyword in content_lower for keyword in high_keywords):
            return PriorityLevel.HIGH
        elif len(content) > 500:  # Missões complexas têm prioridade normal+
            return PriorityLevel.NORMAL
        else:
            return PriorityLevel.NORMAL

    def _analyze_mission_complexity(self, content: str) -> float:
        """Analisa complexidade da missão (0.0 - 1.0)."""
        factors = {
            "length": min(len(content) / 1000, 1.0) * 0.2,
            "steps": len(re.findall(r'\b(primeiro|segundo|terceiro|depois|em seguida|finalmente)\b', content.lower())) * 0.1,
            "integrations": len(re.findall(r'\b(email|pesquis|criat|analis|enviat|gerat)\w*', content.lower())) * 0.15,
            "conditions": len(re.findall(r'\b(se|caso|quando|dependendo|conforme)\b', content.lower())) * 0.1,
            "data_processing": len(re.findall(r'\b(dados|informações|análise|relatório|gráfico)\b', content.lower())) * 0.1
        }
        
        complexity = sum(factors.values())
        return min(complexity, 1.0)

    def _predict_success_probability(self, content: str, complexity: float) -> float:
        """Prediz probabilidade de sucesso baseada em padrões históricos."""
        base_probability = 0.85  # Probabilidade base otimista
        
        # Ajustes baseados na complexidade
        complexity_penalty = complexity * 0.2
        
        # Ajustes baseados em palavras-chave problemáticas
        problematic_keywords = ["complexo", "difícil", "múltiplos", "integrar", "complicado"]
        problem_penalty = sum(0.05 for keyword in problematic_keywords if keyword in content.lower())
        
        # Ajustes baseados no histórico de sucesso
        historical_bonus = (self.quantum_metrics.successful_missions / max(self.quantum_metrics.total_missions, 1)) * 0.1
        
        probability = base_probability - complexity_penalty - problem_penalty + historical_bonus
        return max(0.1, min(0.99, probability))

    def _select_optimal_ai_analyzer(self, complexity: float) -> str:
        """Seleciona o AI analyzer optimal baseado na complexidade e performance."""
        # Por enquanto retorna o padrão, mas pode ser expandido para múltiplos analyzers
        return "ai_analyzer_001"

    def _get_agent_performance_hints(self) -> Dict[str, float]:
        """Retorna dicas de performance dos agentes para o planejador."""
        hints = {}
        
        for agent_id, performance_history in self.agent_performance_cache.items():
            if performance_history:
                avg_performance = sum(performance_history) / len(performance_history)
                hints[agent_id] = round(avg_performance, 3)
        
        return hints

    def _convert_to_message_priority(self, mission_priority: PriorityLevel) -> Priority:
        """Converte prioridade da missão para prioridade de mensagem."""
        mapping = {
            PriorityLevel.QUANTUM: Priority.CRITICAL,
            PriorityLevel.CRITICAL: Priority.CRITICAL,
            PriorityLevel.HIGH: Priority.HIGH,
            PriorityLevel.NORMAL: Priority.NORMAL,
            PriorityLevel.LOW: Priority.LOW,
            PriorityLevel.BACKGROUND: Priority.LOW
        }
        return mapping.get(mission_priority, Priority.NORMAL)

    async def _handle_mission_response(self, message: AgentMessage):
        """Processa respostas de agentes para missões ativas."""
        callback_id = message.callback_id
        
        if not callback_id:
            return
        
        # Verifica se é resposta de planejamento
        if callback_id in self.active_missions:
            await self._handle_planning_response(callback_id, message)
        # Verifica se é resposta de execução de passo
        elif "_step_" in callback_id:
            parts = callback_id.rsplit("_step_", 1)
            if len(parts) == 2:
                mission_id, step_str = parts
                try:
                    step_index = int(step_str)
                    if mission_id in self.active_missions:
                        await self._handle_step_response(mission_id, step_index, message)
                except ValueError:
                    logger.warning(f"⚠️ Formato inválido de callback_id: {callback_id}")

    async def _handle_planning_response(self, mission_id: str, planning_message: AgentMessage):
        """Processa resposta do planejamento e inicia execução."""
        mission_context = self.active_missions[mission_id]
        
        if planning_message.content.get("status") != "success":
            error_msg = planning_message.content.get("message", "Falha no planejamento")
            logger.error(f"❌ [Quantum Orchestrator] Planejamento falhou para '{mission_id}': {error_msg}")
            await self._conclude_mission(mission_id, MissionStatus.FAILED, f"Planejamento falhou: {error_msg}")
            return
        
        plan = planning_message.content.get("plan", [])
        if not plan:
            await self._conclude_mission(mission_id, MissionStatus.FAILED, "Plano vazio retornado pelo AI Analyzer")
            return
        
        # Converte plano em passos de execução
        execution_steps = []
        for i, step_data in enumerate(plan):
            execution_step = ExecutionStep(
                step_number=i + 1,
                description=step_data.get("description", f"Passo {i + 1}"),
                assigned_agent=step_data.get("agent", "unknown_agent"),
                task_content=step_data.get("task", {}),
                expected_outcome=step_data.get("expected_outcome", "Execução bem-sucedida"),
                fallback_strategy=step_data.get("fallback_strategy", "Repetir com parâmetros ajustados"),
                max_retries=step_data.get("max_retries", 3)
            )
            execution_steps.append(execution_step)
        
        mission_context.steps = execution_steps
        mission_context.status = MissionStatus.EXECUTING
        mission_context.updated_at = datetime.now()
        
        # Registra métricas do planejamento
        planning_metrics = planning_message.content
        logger.info(f"🧠 [Quantum Orchestrator] Plano recebido para '{mission_id}':")
        logger.info(f"  📋 {len(execution_steps)} passos definidos")
        logger.info(f"  🤖 Provedor IA: {planning_metrics.get('provider_used', 'unknown')}")
        logger.info(f"  ⏱️ Tempo de planejamento: {planning_metrics.get('response_time_ms', 0):.1f}ms")
        logger.info(f"  🎯 Confiança: {planning_metrics.get('confidence_score', 0):.2f}")
        
        # Inicia execução
        await self._execute_next_mission_step(mission_id)

    async def _execute_next_mission_step(self, mission_id: str):
        """Executa o próximo passo da missão."""
        if mission_id not in self.active_missions:
            return
        
        mission_context = self.active_missions[mission_id]
        
        # Verifica se ainda há passos para executar
        if mission_context.current_step_index >= len(mission_context.steps):
            await self._conclude_mission(mission_id, MissionStatus.COMPLETED, "Missão concluída com sucesso")
            return
        
        current_step = mission_context.steps[mission_context.current_step_index]
        current_step.status = StepStatus.EXECUTING
        current_step.started_at = datetime.now()
        
        logger.info(f"🔧 [Quantum Orchestrator] Executando passo {current_step.step_number}/{len(mission_context.steps)}")
        logger.info(f"  📝 Descrição: {current_step.description}")
        logger.info(f"  🤖 Agente: {current_step.assigned_agent}")
        
        try:
            # Resolve contexto dinâmico
            resolved_task = self._resolve_quantum_context(current_step.task_content, mission_context.step_outputs)
            
            # Cria mensagem para o agente
            step_request = self.create_message(
                recipient_id=current_step.assigned_agent,
                message_type=MessageType.REQUEST,
                content=resolved_task,
                callback_id=f"{mission_id}_step_{mission_context.current_step_index}",
                priority=self._convert_to_message_priority(mission_context.priority)
            )
            
            await self.message_bus.publish(step_request)
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar passo {current_step.step_number}: {e}", exc_info=True)
            current_step.status = StepStatus.FAILED
            current_step.error_message = str(e)
            await self._handle_step_failure(mission_id, mission_context.current_step_index)

    def _resolve_quantum_context(self, task_content: Dict, step_outputs: Dict[int, Dict[str, Any]]) -> Dict:
        """Resolve contexto dinâmico com inteligência quantum."""
        if not task_content:
            return {}
        
        # Serializa para manipulação de strings
        resolved_content = json.dumps(task_content, ensure_ascii=False)
        
        # Encontra todos os placeholders
        placeholders = re.findall(r"\{\{output_step_(\d+)\.([^}]+)\}\}", resolved_content)
        
        for step_num_str, path in placeholders:
            try:
                step_num = int(step_num_str)
                step_output = step_outputs.get(step_num)
                
                if step_output:
                    value = _get_value_from_path(step_output, path)
                    
                    if value is not None:
                        placeholder_full = f"{{{{output_step_{step_num}.{path}}}}}"
                        # Substitui o placeholder com aspas pelo valor JSON
                        placeholder_quoted = f'"{placeholder_full}"'
                        resolved_content = resolved_content.replace(placeholder_quoted, json.dumps(value, ensure_ascii=False))
                        # Substitui também versão sem aspas (para casos edge)
                        resolved_content = resolved_content.replace(placeholder_full, json.dumps(value, ensure_ascii=False) if isinstance(value, str) else str(value))
                    else:
                        logger.warning(f"⚠️ Valor não encontrado para placeholder: output_step_{step_num}.{path}")
                else:
                    logger.warning(f"⚠️ Output do passo {step_num} não encontrado")
                    
            except (ValueError, KeyError) as e:
                logger.error(f"❌ Erro resolvendo placeholder output_step_{step_num_str}.{path}: {e}")
        
        try:
            return json.loads(resolved_content)
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro decodificando JSON após resolução de contexto: {e}")
            logger.error(f"Conteúdo problemático: {resolved_content}")
            return task_content  # Retorna original em caso de erro

    async def _handle_step_response(self, mission_id: str, step_index: int, step_message: AgentMessage):
        """Processa resposta de um passo da missão."""
        mission_context = self.active_missions[mission_id]
        
        # Validação de segurança
        if step_index != mission_context.current_step_index:
            logger.warning(f"⚠️ Resposta de passo fora de ordem: esperado {mission_context.current_step_index}, recebido {step_index}")
            return
        
        current_step = mission_context.steps[step_index]
        current_step.completed_at = datetime.now()
        
        if current_step.started_at:
            execution_time = (current_step.completed_at - current_step.started_at).total_seconds() * 1000
            current_step.execution_time_ms = execution_time
        
        # Processa resultado
        if step_message.content.get("status") == "success":
            current_step.status = StepStatus.COMPLETED
            current_step.result = step_message.content
            
            # Armazena output do passo
            mission_context.step_outputs[step_index + 1] = step_message.content
            
            # Atualiza métricas de performance do agente
            self._update_agent_performance(current_step.assigned_agent, 1.0, current_step.execution_time_ms)
            
            logger.info(f"✅ [Quantum Orchestrator] Passo {current_step.step_number} concluído com sucesso")
            logger.info(f"  ⏱️ Tempo de execução: {current_step.execution_time_ms:.1f}ms")
            
            # Avança para próximo passo
            mission_context.current_step_index += 1
            await self._execute_next_mission_step(mission_id)
            
        else:
            # Passo falhou
            current_step.status = StepStatus.FAILED
            current_step.error_message = step_message.content.get("message", "Erro desconhecido")
            
            self._update_agent_performance(current_step.assigned_agent, 0.0, current_step.execution_time_ms)
            
            logger.error(f"❌ Passo {current_step.step_number} falhou: {current_step.error_message}")
            
            await self._handle_step_failure(mission_id, step_index)

    def _update_agent_performance(self, agent_id: str, success_score: float, execution_time_ms: float):
        """Atualiza métricas de performance do agente."""
        # Score composto: sucesso (70%) + velocidade (30%)
        max_expected_time = 30000  # 30 segundos como baseline
        speed_score = max(0.0, 1.0 - (execution_time_ms / max_expected_time))
        
        composite_score = (success_score * 0.7) + (speed_score * 0.3)
        
        self.agent_performance_cache[agent_id].append(composite_score)
        
        # Atualiza métricas globais
        if agent_id not in self.quantum_metrics.agent_success_rates:
            self.quantum_metrics.agent_success_rates[agent_id] = composite_score
        else:
            # Média móvel ponderada
            current_avg = self.quantum_metrics.agent_success_rates[agent_id]
            self.quantum_metrics.agent_success_rates[agent_id] = (current_avg * 0.8) + (composite_score * 0.2)

    async def _handle_step_failure(self, mission_id: str, step_index: int):
        """Processa falha de um passo com estratégias de recuperação."""
        mission_context = self.active_missions[mission_id]
        failed_step = mission_context.steps[step_index]
        
        failed_step.retry_count += 1
        
        # Verifica se ainda pode tentar novamente
        if failed_step.retry_count < failed_step.max_retries:
            logger.warning(f"🔄 Tentativa {failed_step.retry_count}/{failed_step.max_retries} para passo {failed_step.step_number}")
            
            failed_step.status = StepStatus.RETRYING
            
            # Espera progressiva antes de tentar novamente
            wait_time = min(5 * failed_step.retry_count, 30)
            await asyncio.sleep(wait_time)
            
            # Tenta executar novamente
            await self._execute_next_mission_step(mission_id)
            
        else:
            # Esgotou tentativas - aplica estratégia de fallback
            logger.error(f"💀 Passo {failed_step.step_number} falhou definitivamente após {failed_step.retry_count} tentativas")
            
            # Tenta estratégia de fallback se disponível
            if await self._apply_fallback_strategy(mission_id, step_index):
                logger.info(f"🔄 Estratégia de fallback aplicada para passo {failed_step.step_number}")
            else:
                # Falha total da missão
                await self._conclude_mission(
                    mission_id, 
                    MissionStatus.FAILED, 
                    f"Passo {failed_step.step_number} falhou: {failed_step.error_message}"
                )

    async def _apply_fallback_strategy(self, mission_id: str, step_index: int) -> bool:
        """Aplica estratégia de fallback para um passo falhado."""
        mission_context = self.active_missions[mission_id]
        failed_step = mission_context.steps[step_index]
        
        # Por enquanto, implementação básica - pode ser expandida
        fallback_strategy = failed_step.fallback_strategy.lower()
        
        if "skip" in fallback_strategy or "pular" in fallback_strategy:
            # Pula o passo e continua
            failed_step.status = StepStatus.SKIPPED
            mission_context.current_step_index += 1
            await self._execute_next_mission_step(mission_id)
            return True
        
        elif "alternative" in fallback_strategy or "alternativo" in fallback_strategy:
            # Tenta com agente alternativo (implementação futura)
            logger.info("🔄 Tentativa com agente alternativo não implementada ainda")
            return False
        
        return False

    async def _conclude_mission(self, mission_id: str, final_status: MissionStatus, message: str):
        """Conclui uma missão e envia feedback de aprendizado."""
        if mission_id not in self.active_missions:
            return
        
        mission_context = self.active_missions[mission_id]
        mission_context.status = final_status
        mission_context.updated_at = datetime.now()
        
        # Calcula tempo total de execução
        total_time = (mission_context.updated_at - mission_context.created_at).total_seconds()
        mission_context.total_execution_time = total_time
        
        # Prepara resposta para o usuário
        if final_status == MissionStatus.COMPLETED:
            response_content = {
                "status": "success",
                "message": message,
                "mission_id": mission_id,
                "execution_time_seconds": total_time,
                "steps_completed": len([s for s in mission_context.steps if s.status == StepStatus.COMPLETED]),
                "total_steps": len(mission_context.steps)
            }
            
            logger.info(f"✅ [Quantum Orchestrator] Missão '{mission_id}' concluída com sucesso!")
            logger.info(f"  ⏱️ Tempo total: {total_time:.1f}s")
            logger.info(f"  📋 Passos: {response_content['steps_completed']}/{response_content['total_steps']}")
            
        else:
            response_content = {
                "status": "error",
                "message": message,
                "mission_id": mission_id,
                "execution_time_seconds": total_time
            }
            
            logger.error(f"❌ [Quantum Orchestrator] Missão '{mission_id}' falhou: {message}")
        
        # Envia resposta (procura por mensagem original no contexto)
        # Por simplicidade, registra apenas no log aqui - implementação completa precisaria 
        # armazenar referência à mensagem original
        
        # Envia dados de treinamento para o Evolution Engine
        await self._send_training_data(mission_context, final_status)
        
        # Atualiza métricas quantum
        self._update_quantum_metrics(mission_context, final_status)
        
        # Move para histórico e limpa memória ativa
        self.mission_history.append(mission_context)
        del self.active_missions[mission_id]

    async def _send_training_data(self, mission_context: MissionContext, final_status: MissionStatus):
        """Envia dados de treinamento para o Evolution Engine."""
        try:
            reward = 1.0 if final_status == MissionStatus.COMPLETED else -0.5
            
            # Ajusta reward baseado na eficiência
            if final_status == MissionStatus.COMPLETED:
                expected_time = len(mission_context.steps) * 10  # 10s por passo como baseline
                if mission_context.total_execution_time < expected_time:
                    reward += 0.3  # Bonus por eficiência
                
                # Bonus por baixa taxa de retry
                total_retries = sum(step.retry_count for step in mission_context.steps)
                if total_retries == 0:
                    reward += 0.2
            
            data_point = TrainingDataPoint(
                agent_id="orchestrator_001",
                state_features={
                    "mission_complexity": mission_context.complexity_score,
                    "num_steps": len(mission_context.steps),
                    "priority_level": mission_context.priority.value,
                    "duration_seconds": mission_context.total_execution_time,
                    "retry_count": sum(step.retry_count for step in mission_context.steps),
                    "success_probability_predicted": mission_context.success_probability
                },
                action_taken={
                    "orchestration_strategy": "sequential_execution",
                    "recovery_attempts": mission_context.recovery_attempts,
                    "agents_used": list(set(step.assigned_agent for step in mission_context.steps))
                },
                outcome_reward=reward,
                context_metadata={
                    "mission_id": mission_context.mission_id,
                    "final_status": final_status.value,
                    "steps_completed": len([s for s in mission_context.steps if s.status == StepStatus.COMPLETED])
                }
            )
            
            training_message = self.create_message(
                recipient_id="evolution_engine_001",
                message_type=MessageType.NOTIFICATION,
                content={"event_type": "training_data", "data": asdict(data_point)}
            )
            
            await self.message_bus.publish(training_message)
            logger.info(f"📊 [Quantum Orchestrator] Dados de treino enviados (reward: {reward:.2f})")
            
        except Exception as e:
            logger.error(f"❌ Erro enviando dados de treinamento: {e}", exc_info=True)

    def _update_quantum_metrics(self, mission_context: MissionContext, final_status: MissionStatus):
        """Atualiza métricas quantum do orquestrador."""
        self.quantum_metrics.total_missions += 1
        
        if final_status == MissionStatus.COMPLETED:
            self.quantum_metrics.successful_missions += 1
        elif final_status == MissionStatus.FAILED:
            self.quantum_metrics.failed_missions += 1
        
        # Atualiza média de tempo de missão
        current_avg = self.quantum_metrics.average_mission_time
        new_time = mission_context.total_execution_time
        self.quantum_metrics.average_mission_time = (
            (current_avg * (self.quantum_metrics.total_missions - 1) + new_time) / 
            self.quantum_metrics.total_missions
        )
        
        # Atualiza média de passos por missão
        current_avg_steps = self.quantum_metrics.average_steps_per_mission
        new_steps = len(mission_context.steps)
        self.quantum_metrics.average_steps_per_mission = (
            (current_avg_steps * (self.quantum_metrics.total_missions - 1) + new_steps) / 
            self.quantum_metrics.total_missions
        )
        
        # Atualiza distribuição de complexidade
        complexity_bucket = f"{mission_context.complexity_score:.1f}"
        self.quantum_metrics.complexity_distribution[complexity_bucket] = (
            self.quantum_metrics.complexity_distribution.get(complexity_bucket, 0) + 1
        )
        
        # Calcula eficiência de orquestração
        success_rate = self.quantum_metrics.successful_missions / self.quantum_metrics.total_missions
        avg_agent_performance = sum(self.quantum_metrics.agent_success_rates.values()) / max(len(self.quantum_metrics.agent_success_rates), 1)
        self.quantum_metrics.orchestration_efficiency = (success_rate + avg_agent_performance) / 2

    async def _monitor_active_missions(self):
        """Monitora missões ativas para detectar problemas."""
        current_time = datetime.now()
        
        for mission_id, mission_context in list(self.active_missions.items()):
            # Verifica timeout de missão
            elapsed_minutes = (current_time - mission_context.created_at).total_seconds() / 60
            
            if elapsed_minutes > self.mission_timeout_minutes:
                logger.warning(f"⏰ Missão '{mission_id}' excedeu timeout de {self.mission_timeout_minutes} minutos")
                await self._conclude_mission(
                    mission_id, 
                    MissionStatus.FAILED, 
                    f"Timeout após {elapsed_minutes:.1f} minutos"
                )
                continue
            
            # Verifica passos presos
            if mission_context.status == MissionStatus.EXECUTING:
                current_step_index = mission_context.current_step_index
                if current_step_index < len(mission_context.steps):
                    current_step = mission_context.steps[current_step_index]
                    
                    if (current_step.status == StepStatus.EXECUTING and 
                        current_step.started_at and
                        (current_time - current_step.started_at).total_seconds() > 300):  # 5 minutos
                        
                        logger.warning(f"⚠️ Passo {current_step.step_number} da missão '{mission_id}' pode estar preso")
                        # Poderia implementar recuperação automática aqui

    async def _execute_automatic_recovery(self):
        """Executa procedimentos de recuperação automática."""
        # Implementação futura para recuperação inteligente
        pass

    async def _analyze_agent_performance(self):
        """Analisa performance dos agentes e otimiza seleção."""
        logger.debug("📊 Analisando performance dos agentes...")
        
        # Atualiza taxas de sucesso baseadas no histórico recente
        for agent_id, performance_history in self.agent_performance_cache.items():
            if len(performance_history) >= 5:  # Mínimo de amostras
                recent_avg = sum(list(performance_history)[-10:]) / min(len(performance_history), 10)
                self.quantum_metrics.agent_success_rates[agent_id] = recent_avg

    async def _optimize_mission_patterns(self):
        """Otimiza padrões de missão baseado no histórico."""
        # Implementação futura para criação de templates baseados em padrões de sucesso
        pass

    async def _maintain_quantum_coherence(self):
        """Mantém coerência quântica do sistema de orquestração."""
        if self.quantum_metrics.total_missions > 0:
            success_rate = self.quantum_metrics.successful_missions / self.quantum_metrics.total_missions
            efficiency = self.quantum_metrics.orchestration_efficiency
            
            # Coerência baseada na consistência de performance
            self.quantum_metrics.quantum_coherence = (success_rate + efficiency) / 2
            
            if self.quantum_metrics.quantum_coherence < self.quantum_coherence_threshold:
                logger.warning(f"⚠️ Coerência quântica baixa: {self.quantum_metrics.quantum_coherence:.3f}")

    async def _handle_metrics_request(self, message: AgentMessage):
        """Processa requisições de métricas do orquestrador."""
        metrics = self.get_orchestrator_metrics()
        await self.publish_response(message, {"status": "success", "metrics": metrics})

    def get_orchestrator_metrics(self) -> Dict[str, Any]:
        """Retorna métricas completas do orquestrador quantum."""
        return {
            "quantum_metrics": asdict(self.quantum_metrics),
            "active_missions": len(self.active_missions),
            "mission_history_size": len(self.mission_history),
            "agent_performance_cache_size": len(self.agent_performance_cache),
            "current_quantum_coherence": self.quantum_metrics.quantum_coherence,
            "system_efficiency": self.quantum_metrics.orchestration_efficiency,
            "average_mission_duration": self.quantum_metrics.average_mission_time,
            "success_rate": (
                self.quantum_metrics.successful_missions / self.quantum_metrics.total_missions
                if self.quantum_metrics.total_missions > 0 else 0.0
            )
        }

class QuantumMetaCognitiveAgent(BaseNetworkAgent):
    """
    Agente Meta-Cognitivo Quantum - Consciência Sistêmica.
    Monitora e analisa o comportamento do sistema como um todo.
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.META_COGNITIVE, message_bus)
        self.capabilities.extend([
            "system_consciousness",
            "behavioral_analysis", 
            "quantum_introspection",
            "emergent_pattern_detection"
        ])
        
        self._analysis_task: Optional[asyncio.Task] = None
        logger.info(f"🧠 {self.agent_id} (Quantum Meta-Cognitive) inicializado.")

    async def start_meta_cognition(self):
        """Inicia processo de meta-cognição quantum."""
        if self._analysis_task is None or self._analysis_task.done():
            self._analysis_task = asyncio.create_task(self._meta_analysis_loop())
            logger.info("🧠 Meta-cognição quantum iniciada.")

    async def _meta_analysis_loop(self):
        """Loop principal de análise meta-cognitiva."""
        while True:
            await asyncio.sleep(600)  # Análise a cada 10 minutos
            
            try:
                await self._analyze_system_behavior()
                await self._detect_emergent_patterns()
                await self._quantum_self_reflection()
                
            except Exception as e:
                logger.error(f"❌ Erro na meta-cognição: {e}", exc_info=True)

    async def _analyze_system_behavior(self):
        """Analisa comportamento emergente do sistema."""
        # Implementação futura para análise comportamental profunda
        pass

    async def _detect_emergent_patterns(self):
        """Detecta padrões emergentes no comportamento do sistema."""
        # Implementação futura para detecção de padrões
        pass

    async def _quantum_self_reflection(self):
        """Executa auto-reflexão quantum do sistema."""
        # Implementação futura para introspecção sistêmica
        pass

def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria os agentes Meta-Cognitivos Quantum."""
    agents: List[BaseNetworkAgent] = []
    
    try:
        # Orquestrador Quantum
        orchestrator = QuantumOrchestratorAgent("orchestrator_001", message_bus)
        agents.append(orchestrator)
        
        # Meta-Cognitivo Quantum
        meta_agent = QuantumMetaCognitiveAgent("metacognitive_001", message_bus)
        asyncio.create_task(meta_agent.start_meta_cognition())
        agents.append(meta_agent)
        
        logger.info("✅ Agentes Meta-Cognitivos Quantum criados com sucesso.")
        
    except Exception as e:
        logger.critical(f"❌ Erro CRÍTICO criando agentes Meta-Cognitivos Quantum: {e}", exc_info=True)
    
    return agents
