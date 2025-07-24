import logging
from typing import List
from multi_agent_network import AgentType, BaseNetworkAgent

logger = logging.getLogger(__name__)

class CommunicationAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['communication']
        logger.info(f"✅ {self.agent_id} inicializado")

class DecisionAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['decision_making']
        logger.info(f"✅ {self.agent_id} inicializado")

class ComplianceAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['compliance_check']
        logger.info(f"✅ {self.agent_id} inicializado")

def create_service_agents(message_bus, num_instances=1) -> List:
    agents = []
    try:
        for i in range(num_instances):
            agents.extend([
                CommunicationAgent(f"communication_{(i*3+1):03d}", AgentType.SERVICE, message_bus),
                DecisionAgent(f"decision_{(i*3+1):03d}", AgentType.SERVICE, message_bus),
                ComplianceAgent(f"compliance_{(i*3+1):03d}", AgentType.SERVICE, message_bus)
            ])
        # Registrar apenas uma vez fora do loop e limitar a 2 se num_instances == 1
        unique_agents = []
        seen_ids = set()
        for agent in agents:
            if agent.agent_id not in seen_ids:
                if num_instances == 1 and len(unique_agents) >= 2:
                    break
                if agent.agent_id not in message_bus.subscribers:
                    message_bus.register_agent(agent.agent_id, agent)
                unique_agents.append(agent)
                seen_ids.add(agent.agent_id)
        logger.info(f"✅ {len(unique_agents)} agentes de serviço criados")
        return unique_agents
    except Exception as e:
        logger.error(f"❌ Erro criando agentes de serviço: {e}")
        return []
