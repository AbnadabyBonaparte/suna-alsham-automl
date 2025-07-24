#!/usr/bin/env python3
"""
Core Agents v3 - EXATAMENTE 5 agentes
Força criação de 5 agentes core v3 independente do num_instances
"""

import logging
from typing import List
from multi_agent_network import AgentType, BaseNetworkAgent
from uuid import uuid4

logger = logging.getLogger(__name__)

class CoreAgentV3(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['core_processing', 'advanced_reasoning']
        logger.info(f"✅ {self.agent_id} inicializado")

class GuardAgentV3(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['security', 'validation', 'protection']
        logger.info(f"✅ {self.agent_id} inicializado")

class LearnAgentV3(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['learning', 'adaptation', 'meta_cognition']
        logger.info(f"✅ {self.agent_id} inicializado")

def create_core_agents_v3(message_bus, num_instances=1) -> List:
    """
    Cria EXATAMENTE 5 agentes core v3 independente do num_instances
    Configuração: core_v3_001, guard_v3_001, learn_v3_001, core_v3_002, guard_v3_002
    """
    agents = []
    try:
        logger.info("🎯 Forçando criação de EXATAMENTE 5 agentes core v3...")
        
        # Criar exatamente 5 agentes em ordem específica
        agents = [
            CoreAgentV3("core_v3_001", AgentType.CORE, message_bus),
            GuardAgentV3("guard_v3_001", AgentType.GUARD, message_bus),
            LearnAgentV3("learn_v3_001", AgentType.LEARN, message_bus),
            CoreAgentV3("core_v3_002", AgentType.CORE, message_bus),
            GuardAgentV3("guard_v3_002", AgentType.GUARD, message_bus)
        ]
        
        # Registrar no MessageBus
        for agent in agents:
            if agent.agent_id not in message_bus.subscribers:
                message_bus.register_agent(agent.agent_id, agent)
                logger.info(f"📝 {agent.agent_id} registrado no MessageBus")
        
        logger.info(f"✅ {len(agents)} agentes core v3.0 criados (FORÇADO para 5)")
        logger.info(f"📋 Agentes: {[agent.agent_id for agent in agents]}")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro criando agentes core v3: {e}")
        return []

