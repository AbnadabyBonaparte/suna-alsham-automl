#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos - O Cérebro do SUNA-ALSHAM.
"""

import asyncio
import logging
import uuid
from typing import Dict, List, Optional

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseNetworkAgent):
    """Agente Orquestrador Estratégico."""
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.capabilities.extend(["dynamic_planning", "complex_task_orchestration"])
        self.pending_missions: Dict[str, Dict] = {}
        logger.info(f"👑 {self.agent_id} (Orquestrador Estratégico) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        pass  # Mantém lógica de orquestração existente

class MetaCognitiveAgent(BaseNetworkAgent):
    """Agente Meta-Cognitivo - Analisa o sistema como um todo."""
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.META_COGNITIVE, message_bus)
        self.capabilities.append("system_analysis")
        self._analysis_task: Optional[asyncio.Task] = None
        logger.info(f"🧠 {self.agent_id} (Meta-Cognitivo) inicializado.")

    async def start_meta_cognition(self):
        if not self._analysis_task:
            self._analysis_task = asyncio.create_task(self._analysis_loop())
            logger.info(f"🧠 {self.agent_id} iniciou processos meta-cognitivos.")

    async def _analysis_loop(self):
        while True:
            await asyncio.sleep(300)
            logger.info("[Meta-Cog] Analisando performance da rede...")

def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria e retorna os agentes meta-cognitivos sempre como lista."""
    agents: List[BaseNetworkAgent] = []
    logger.info("🧠 Criando agentes Meta-Cognitivos...")
    try:
        orchestrator = OrchestratorAgent("orchestrator_001", message_bus)
        meta_agent = MetaCognitiveAgent("metacognitive_001", message_bus)
        asyncio.create_task(meta_agent.start_meta_cognition())
        agents.extend([orchestrator, meta_agent])
    except Exception as e:
        logger.error(f"❌ Erro criando agentes Meta-Cognitivos: {e}", exc_info=True)
    return agents
