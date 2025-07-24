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
    agents = []
    try:
        for i in range(num_instances):
            agents.extend([
                SpecialistAgent(f"specialist_{(i*3+1):03d}", AgentType.SPECIALIZED, message_bus),
                AnalyticsAgent(f"analytics_{(i*3+1):03d}", AgentType.SPECIALIZED, message_bus),
                PredictorAgent(f"predictor_{(i*3+1):03d}", AgentType.SPECIALIZED, message_bus)
            ])
        # Limitar a 6 agentes no total
        agents = agents[:6]
        for agent in agents:
            if agent.agent_id not in message_bus.subscribers:
                message_bus.register_agent(agent.agent_id, agent)
        logger.info(f"✅ {len(agents)} agentes especializados criados")
        return agents
    except Exception as e:
        logger.error(f"❌ Erro criando agentes especializados: {e}")
        return []
