import logging
from typing import List
from multi_agent_network import AgentType, BaseNetworkAgent
from uuid import uuid4

logger = logging.getLogger(__name__)

class AIAnalyzerAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['ai_analysis']
        logger.info(f"✅ {self.agent_id} inicializado")

class AIOptimizerAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['ai_optimization']
        logger.info(f"✅ {self.agent_id} inicializado")

class AIChatAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['ai_chat']
        logger.info(f"✅ {self.agent_id} inicializado")

def create_ai_agents(message_bus, num_instances=1) -> List:
    agents = []
    try:
        for i in range(num_instances):
            agents.extend([
                AIAnalyzerAgent(f"ai_analyzer_{(i*3+1):03d}", AgentType.AI_POWERED, message_bus),
                AIOptimizerAgent(f"ai_optimizer_{(i*3+1):03d}", AgentType.AI_POWERED, message_bus),
                AIChatAgent(f"ai_chat_{(i*3+1):03d}", AgentType.AI_POWERED, message_bus)
            ])
        # Limitar a 3 agentes no total
        agents = agents[:3]
        for agent in agents:
            if agent.agent_id not in message_bus.subscribers:
                message_bus.register_agent(agent.agent_id, agent)
        logger.info(f"✅ {len(agents)} agentes com IA criados")
        return agents
    except Exception as e:
        logger.error(f"❌ Erro criando agentes com IA: {e}")
        return []
