#!/usr/bin/env python3
"""
Specialized Agents - EXATAMENTE 5 agentes
Força criação de 5 agentes especializados independente do num_instances
"""

import logging
from typing import List
from multi_agent_network import AgentType, BaseNetworkAgent
from uuid import uuid4

logger = logging.getLogger(__name__)

class SpecialistAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['specialized_task']
        logger.info(f"✅ {self.agent_id} inicializado")

class AnalyticsAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['data_analytics']
        logger.info(f"✅ {self.agent_id} inicializado")

class PredictorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['prediction']
        logger.info(f"✅ {self.agent_id} inicializado")

def create_specialized_agents(message_bus, num_instances=1) -> List:
    """
    Cria EXATAMENTE 5 agentes especializados independente do num_instances
    Configuração: specialist_001, analytics_001, predictor_001, specialist_002, analytics_002
    """
    agents = []
    try:
        logger.info("🎯 Forçando criação de EXATAMENTE 5 agentes especializados...")
        
        # Criar exatamente 5 agentes em ordem específica
        agents = [
            SpecialistAgent("specialist_001", AgentType.SPECIALIZED, message_bus),
            AnalyticsAgent("analytics_001", AgentType.SPECIALIZED, message_bus),
            PredictorAgent("predictor_001", AgentType.SPECIALIZED, message_bus),
            SpecialistAgent("specialist_002", AgentType.SPECIALIZED, message_bus),
            AnalyticsAgent("analytics_002", AgentType.SPECIALIZED, message_bus)
        ]
        
        # Registrar no MessageBus
        for agent in agents:
            if agent.agent_id not in message_bus.subscribers:
                message_bus.register_agent(agent.agent_id, agent)
                logger.info(f"📝 {agent.agent_id} registrado no MessageBus")
        
        logger.info(f"✅ {len(agents)} agentes especializados criados (FORÇADO para 5)")
        logger.info(f"📋 Agentes: {[agent.agent_id for agent in agents]}")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro criando agentes especializados: {e}")
        return []

