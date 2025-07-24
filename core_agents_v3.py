import logging
from typing import List
from multi_agent_network import AgentType, BaseNetworkAgent
from uuid import uuid4

logger = logging.getLogger(__name__)

class CoreAgentV3(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['core_processing']
        logger.info(f"✅ {self.agent_id} inicializado")

class GuardAgentV3(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['security_check']
        logger.info(f"✅ {self.agent_id} inicializado")

class LearnAgentV3(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['learning']
        logger.info(f"✅ {self.agent_id} inicializado")

def create_core_agents_v3(message_bus, num_instances=1) -> List:
    agents = []
    try:
        for i in range(num_instances):
            agents.extend([
                CoreAgentV3(f"core_v3_{(i*3+1):03d}", AgentType.CORE, message_bus),
                GuardAgentV3(f"guard_v3_{(i*3+1):03d}", AgentType.GUARD, message_bus),
                LearnAgentV3(f"learn_v3_{(i*3+1):03d}", AgentType.LEARN, message_bus)
            ])
        # Limitar a 6 agentes no total
        agents = agents[:6]
        for agent in agents:
            if agent.agent_id not in message_bus.subscribers:
                message_bus.register_agent(agent.agent_id, agent)
        logger.info(f"✅ {len(agents)} agentes core v3.0 criados")
        return agents
    except Exception as e:
        logger.error(f"❌ Erro criando agentes core v3.0: {e}")
        return []
