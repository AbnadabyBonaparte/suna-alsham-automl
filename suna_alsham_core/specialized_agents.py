#!/usr/bin/env python3
"""
Módulo dos Agentes Especializados - SUNA-ALSHAM

Define agentes que realizam tarefas especializadas e complexas,
muitas vezes orquestrando outros agentes para atingir um objetivo.
"""

import asyncio
import logging
from typing import Any, Dict, List, Set

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


class TaskDelegatorAgent(BaseNetworkAgent):
    """
    Agente que pode receber uma tarefa complexa e dividi-la em subtarefas
    para serem executadas por outros agentes.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.append("task_delegation")


class NewAgentOnboardingAgent(BaseNetworkAgent):
    """
    Agente responsável por integrar novos agentes à rede,
    verificando suas capacidades e registrando-os.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.append("agent_onboarding")
        self.onboarding_task = asyncio.create_task(self._check_for_new_agents())

    async def _check_for_new_agents(self, interval: int = 30):
        """Verifica periodicamente se novos agentes entraram na rede."""
        known_agents: Set[str] = set()
        
        while True:
            await asyncio.sleep(interval)
            
            # --- CORREÇÃO APLICADA AQUI ---
            # Trocado .subscribers por .queues para alinhar com a classe MessageBus
            current_agents = set(self.message_bus.queues.keys())
            
            new_agents = current_agents - known_agents
            
            if new_agents:
                logger.info(f"Novos agentes detectados na rede: {new_agents}")
                # Lógica de onboarding (verificação de saúde, etc.) entraria aqui
            
            known_agents = current_agents


def create_specialized_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria os agentes Especializados."""
    logger.info("🛠️ Criando agentes Especializados...")
    agents = [
        TaskDelegatorAgent("task_delegator_001", message_bus),
        NewAgentOnboardingAgent("onboarding_001", message_bus),
    ]
    return agents
