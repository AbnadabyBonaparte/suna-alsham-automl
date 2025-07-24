import logging
from typing import List
from multi_agent_network import AgentType, BaseNetworkAgent

logger = logging.getLogger(__name__)

class SystemMonitorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['system_monitoring']
        logger.info(f"✅ {self.agent_id} inicializado")

class SystemControlAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['system_control']
        logger.info(f"✅ {self.agent_id} inicializado")

class SystemRecoveryAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['system_recovery']
        logger.info(f"✅ {self.agent_id} inicializado")

def create_system_agents(message_bus, num_instances=1) -> List:
    agents = []
    try:
        for i in range(num_instances):
            agents.extend([
                SystemMonitorAgent(f"monitor_{(i*3+1):03d}", AgentType.SYSTEM, message_bus),
                SystemControlAgent(f"control_{(i*3+1):03d}", AgentType.SYSTEM, message_bus),
                SystemRecoveryAgent(f"recovery_{(i*3+1):03d}", AgentType.SYSTEM, message_bus)
            ])
        # Registrar apenas uma vez fora do loop
        for agent in agents:
            if agent.agent_id not in message_bus.subscribers:
                message_bus.register_agent(agent.agent_id, agent)
        logger.info(f"✅ {len(agents)} agentes de sistema criados")
        return agents
    except Exception as e:
        logger.error(f"❌ Erro criando agentes de sistema: {e}")
        return []
