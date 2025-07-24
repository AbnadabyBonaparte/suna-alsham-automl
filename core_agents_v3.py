import logging
from typing import List
from multi_agent_network import AgentType, BaseNetworkAgent

logger = logging.getLogger(__name__)

class CoreAgentV3NetworkAdapter(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['automl']
        logger.info(f"✅ {self.agent_id} inicializado")

class GuardAgentV3NetworkAdapter(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['security_check']
        logger.info(f"✅ {self.agent_id} inicializado")

class LearnAgentV3NetworkAdapter(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['meta_learning']
        logger.info(f"✅ {self.agent_id} inicializado")

def create_core_agents_v3(message_bus, num_instances=1) -> List:
    agents = []
    try:
        for i in range(num_instances):
            agents.extend([
                CoreAgentV3NetworkAdapter(f"core_v3_{(i*3+1):03d}", AgentType.CORE, message_bus),
                GuardAgentV3NetworkAdapter(f"guard_v3_{(i*3+1):03d}", AgentType.GUARD, message_bus),
                LearnAgentV3NetworkAdapter(f"learn_v3_{(i*3+1):03d}", AgentType.LEARN, message_bus)
            ])
        for agent in agents:
            message_bus.register_agent(agent.agent_id, agent)
        logger.info(f"✅ {len(agents)} agentes core v3.0 criados")
        return agents
    except Exception as e:
        logger.error(f"❌ Erro criando agentes core_v3: {e}")
        return []
