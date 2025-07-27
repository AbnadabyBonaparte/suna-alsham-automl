#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos - O Cérebro do SUNA-ALSHAM.

Define os agentes de mais alto nível:
- OrchestratorAgent: O maestro supremo, responsável pela distribuição de tarefas.
- MetaCognitiveAgent: O cérebro estratégico, que analisa e otimiza o próprio sistema.
"""

import asyncio
import logging
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class TaskStatus(Enum):
    """Status de uma tarefa gerenciada pelo orquestrador."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    COMPLETED = "completed"
    FAILED = "failed"


class OrchestrationStrategy(Enum):
    """Estratégias que o orquestrador pode usar para distribuir tarefas."""
    LOAD_BALANCED = "load_balanced"
    CAPABILITY_BASED = "capability_based"
    ADAPTIVE = "adaptive"


@dataclass
class SystemTask:
    """Representa uma tarefa a ser executada pela rede de agentes."""
    task_id: str
    task_type: str
    priority: Priority
    requirements: List[str]
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None


# --- Classes Principais dos Agentes ---

class OrchestratorAgent(BaseNetworkAgent):
    """
    Agente Orquestrador Supremo. Atua como o ponto central de distribuição de
    tarefas, balanceamento de carga e coordenação geral da rede.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o OrchestratorAgent."""
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.capabilities.extend([
            "orchestration",
            "task_distribution",
            "load_balancing",
        ])
        
        self.task_queue = asyncio.Queue()
        self.active_tasks: Dict[str, SystemTask] = {}
        self.strategy = OrchestrationStrategy.ADAPTIVE
        
        logger.info(f"👑 {self.agent_id} (Orquestrador Supremo) inicializado.")

    async def handle_message(self, message: AgentMessage):
        """Processa requisições de tarefas e notificações de status."""
        await super().handle_message(message)
        if message.message_type == MessageType.REQUEST:
            if message.content.get("request_type") == "submit_task":
                await self._queue_task(message.content)


    async def _queue_task(self, task_data: Dict[str, Any]):
        """Adiciona uma nova tarefa à fila de orquestração."""
        try:
            task = SystemTask(
                task_id=task_data.get("task_id", f"task_{int(time.time())}"),
                task_type=task_data.get("type", "general"),
                priority=Priority(task_data.get("priority", 3)),
                requirements=task_data.get("requirements", []),
            )
            await self.task_queue.put(task)
            logger.info(f"📥 Tarefa '{task.task_id}' enfileirada para orquestração.")
        except Exception as e:
            logger.error(f"❌ Erro ao enfileirar tarefa: {e}", exc_info=True)


class MetaCognitiveAgent(BaseNetworkAgent):
    """
    O Cérebro Estratégico. Este agente analisa o comportamento da rede como um
    todo, gera insights e recomenda otimizações para o OrchestratorAgent.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o MetaCognitiveAgent."""
        super().__init__(agent_id, AgentType.META_COGNITIVE, message_bus)
        self.capabilities.extend([
            "meta_cognition",
            "system_analysis",
            "optimization_recommendations",
        ])
        
        self.knowledge_base = {"patterns": [], "insights": []}
        self._analysis_task = None
        logger.info(f"🧠 {self.agent_id} (Meta-Cognitivo) inicializado.")

    async def start_meta_cognition(self):
        """Inicia o loop de análise meta-cognitiva."""
        if not self._analysis_task:
            self._analysis_task = asyncio.create_task(self._analysis_loop())
            logger.info(f"🧠 {self.agent_id} iniciou processos meta-cognitivos.")

    async def _analysis_loop(self):
        """
        [AUTENTICIDADE] Loop de análise do sistema. Na Fase 2, este loop irá
        solicitar dados reais do DatabaseAgent e do PerformanceMonitorAgent
        para identificar padrões e gerar insights.
        """
        while True:
            try:
                logger.info("[Simulação] Analisando performance da rede...")
                # Lógica de análise real a ser implementada aqui.
                await asyncio.sleep(300) # Analisa a cada 5 minutos
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na análise meta-cognitiva: {e}", exc_info=True)


def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Cria os agentes de Meta-Cognição (Orquestrador e o próprio Meta-Cognitivo).
    """
    agents = []
    logger.info("🧠 Criando agentes Meta-Cognitivos...")
    
    agent_configs = [
        {"id": "orchestrator_001", "class": OrchestratorAgent},
        {"id": "metacognitive_001", "class": MetaCognitiveAgent},
    ]

    for config in agent_configs:
        try:
            agent = config["class"](config["id"], message_bus)
            if isinstance(agent, MetaCognitiveAgent):
                asyncio.create_task(agent.start_meta_cognition())
            agents.append(agent)
        except Exception as e:
            logger.error(f"❌ Erro criando agente {config['id']}: {e}", exc_info=True)

    return agents
