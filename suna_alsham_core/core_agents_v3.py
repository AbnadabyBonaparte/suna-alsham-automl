#!/usr/bin/env python3
"""
Módulo dos Agentes Core v3 - SUNA-ALSHAM

Define os agentes fundamentais para a operação do sistema.
"""
import logging
from typing import Any, Dict, List

# Import corrigido, sem AgentCapability
from suna_alsham_core.multi_agent_network import (
    BaseNetworkAgent,
    AgentMessage,
    AgentType,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

class CoreAgent(BaseNetworkAgent):
    """Agente central com capacidades básicas de processamento."""
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.CORE, message_bus)
        self.capabilities.append("basic_processing")
        logger.info(f"✅ CoreAgent {self.agent_id} inicializado.")

class GuardAgent(BaseNetworkAgent):
    """Agente de guarda com capacidades de segurança."""
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.CORE, message_bus)
        self.capabilities.append("security_monitoring")
        logger.info(f"🛡️ GuardAgent {self.agent_id} inicializado.")

class LearnAgent(BaseNetworkAgent):
    """Agente de aprendizado com capacidades de adaptação."""
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.CORE, message_bus)
        self.capabilities.append("learning_adaptation")
        logger.info(f"🧠 LearnAgent {self.agent_id} inicializado.")

def create_core_agents_v3(message_bus) -> List[BaseNetworkAgent]:
    """Cria a lista de agentes do núcleo v3."""
    logger.info("🎯 Criando agentes core v3...")
    agents = [
        CoreAgent("core_v3_001", message_bus),
        GuardAgent("guard_v3_001", message_bus),
        LearnAgent("learn_v3_001", message_bus),
        CoreAgent("core_v3_002", message_bus),
        GuardAgent("guard_v3_002", message_bus),
    ]
    return agents
