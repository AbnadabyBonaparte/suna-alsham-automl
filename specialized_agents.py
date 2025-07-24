import logging
from typing import List
from multi_agent_network import AgentType, BaseNetworkAgent

logger = logging.getLogger(__name__)

class SpecialistAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['analysis', 'optimization']
        logger.info(f"✅ {self.agent_id} inicializado")

class AnalyticsAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['data_analysis', 'reporting']
        logger.info(f"✅ {self.agent_id} inicializado")

class PredictorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['prediction', 'forecasting']
        logger.info(f"✅ {self.agent_id} inicializado")

def create_specialized_agents(message_bus, num_instances=1) -> List:
    """Cria EXATAMENTE 5 agentes especializados sem duplicações"""
    agents = []
    
    try:
        logger.info("🎯 Criando EXATAMENTE 5 agentes especializados SEM DUPLICAÇÕES...")
        
        # Lista FIXA de 5 agentes - sem loops que causam duplicação
        agents_to_create = [
            ("specialist_001", SpecialistAgent),
            ("analytics_001", AnalyticsAgent),
            ("predictor_001", PredictorAgent),
            ("specialist_002", SpecialistAgent),
            ("analytics_002", AnalyticsAgent)
        ]
        
        # Verificar se já existem no message_bus para evitar duplicação
        seen_ids = set()
        if hasattr(message_bus, 'subscribers'):
            seen_ids = set(message_bus.subscribers.keys())
        
        for agent_id, agent_class in agents_to_create:
            if agent_id not in seen_ids:
                agent = agent_class(agent_id, AgentType.SPECIALIZED, message_bus)
                agents.append(agent)
                
                # Registrar no MessageBus apenas se não existir
                if not hasattr(message_bus, 'subscribers') or agent_id not in message_bus.subscribers:
                    message_bus.register_agent(agent_id, agent)
                    
                seen_ids.add(agent_id)
            else:
                logger.warning(f"⚠️ Agente {agent_id} já existe - pulando para evitar duplicação")
        
        logger.info(f"✅ {len(agents)} agentes especializados criados (EXATAMENTE 5 SEM DUPLICAÇÃO)")
        logger.info(f"📋 Agentes: {[agent.agent_id for agent in agents]}")
        
        # Garantir que temos exatamente 5 agentes
        if len(agents) != 5:
            logger.error(f"❌ Erro: criados {len(agents)} agentes, esperado 5")
            
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro criando agentes especializados: {e}")
        return []

