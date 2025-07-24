import logging
from typing import List
from multi_agent_network import AgentType, BaseNetworkAgent

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['orchestration']
        logger.info(f"✅ {self.agent_id} inicializado")

    async def orchestrate_system_wide_task(self, task):
        logger.info(f"👑 Orquestrando tarefa: {task}")

class MetaCognitiveAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['meta_cognition']
        logger.info(f"✅ {self.agent_id} inicializado")

def create_meta_cognitive_agents(message_bus) -> List:
    agents = []
    try:
        agents.extend([
            OrchestratorAgent("orchestrator_001", AgentType.ORCHESTRATOR, message_bus),
            MetaCognitiveAgent("metacognitive_001", AgentType.META_COGNITIVE, message_bus)
        ])
        for agent in agents:
            message_bus.register_agent(agent.agent_id, agent)
        logger.info(f"✅ {len(agents)} agentes meta-cognitivos criados")
        return agents
    except Exception as e:
        logger.error(f"❌ Erro criando agentes meta-cognitivos: {e}")
        return []
