import logging
from typing import List
from multi_agent_network import AgentType, BaseNetworkAgent

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
    """Cria EXATAMENTE 5 agentes core v3 sem duplicações"""
    agents = []
    
    try:
        logger.info("🎯 Criando EXATAMENTE 5 agentes core v3 SEM DUPLICAÇÕES...")
        
        # Lista FIXA de 5 agentes - sem loops que causam multiplicação
        agents_to_create = [
            ("core_v3_001", CoreAgentV3, AgentType.CORE),
            ("guard_v3_001", GuardAgentV3, AgentType.GUARD),
            ("learn_v3_001", LearnAgentV3, AgentType.LEARN),
            ("core_v3_002", CoreAgentV3, AgentType.CORE),
            ("guard_v3_002", GuardAgentV3, AgentType.GUARD)
        ]
        
        # Verificar se já existem no message_bus para evitar duplicação
        seen_ids = set()
        if hasattr(message_bus, 'subscribers'):
            seen_ids = set(message_bus.subscribers.keys())
        
        for agent_id, agent_class, agent_type in agents_to_create:
            if agent_id not in seen_ids:
                agent = agent_class(agent_id, agent_type, message_bus)
                agents.append(agent)
                seen_ids.add(agent_id)
            else:
                logger.warning(f"⚠️ Agente {agent_id} já existe - pulando para evitar duplicação")
        
        logger.info(f"✅ {len(agents)} agentes core v3 criados (EXATAMENTE 5 SEM DUPLICAÇÃO)")
        logger.info(f"📋 Agentes: {[agent.agent_id for agent in agents]}")
        
        # Garantir que temos exatamente 5 agentes
        if len(agents) != 5:
            logger.error(f"❌ Erro: criados {len(agents)} agentes, esperado 5")
            
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro criando agentes core v3: {e}")
        return []
