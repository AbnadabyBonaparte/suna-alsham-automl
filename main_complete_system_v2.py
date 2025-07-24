import logging
from typing import List, Dict, Any
from datetime import datetime
import json
import uuid
from multi_agent_network import MultiAgentNetwork, AgentType, AgentMessage, MessageType, Priority

try:
    from specialized_agents import create_specialized_agents
except ImportError:
    create_specialized_agents = None
try:
    from ai_powered_agents import create_ai_agents
except ImportError:
    create_ai_agents = None
try:
    from core_agents_v3 import create_core_agents_v3
except ImportError:
    create_core_agents_v3 = None
try:
    from system_agents import create_system_agents
except ImportError:
    create_system_agents = None
try:
    from service_agents import create_service_agents
except ImportError:
    create_service_agents = None
try:
    from meta_cognitive_agents import create_meta_cognitive_agents
except ImportError:
    create_meta_cognitive_agents = None

logger = logging.getLogger(__name__)

def verificar_arquivos():
    return all([create_specialized_agents, create_ai_agents, create_core_agents_v3,
                create_system_agents, create_service_agents, create_meta_cognitive_agents])

class SUNAAlshamSystemV2:
    def __init__(self):
        self.network = None
        self.all_agents = {}
        self.agent_categories = {
            'specialized': 0,
            'ai_powered': 0,
            'core_v3': 0,
            'system': 0,
            'service': 0,
            'meta_cognitive': 0
        }
        self.system_status = 'initializing'
        self.created_at = datetime.now()
        self.initialization_log = []

    def _register_agents(self, agents: List, category: str):
        try:
            for agent_instance in agents:
                if not hasattr(agent_instance, 'agent_id') or not hasattr(agent_instance, 'status'):
                    logger.error(f"❌ Agente inválido em {category}: {agent_instance}")
                    continue
                if self.network:
                    self.network.add_agent(agent_instance)
                self.all_agents[agent_instance.agent_id] = {
                    'instance': agent_instance,
                    'category': category,
                    'status': agent_instance.status,
                    'capabilities': getattr(agent_instance, 'capabilities', [])
                }
                self.agent_categories[category] += 1
                self.initialization_log.append({
                    'agent_id': agent_instance.agent_id,
                    'category': category,
                    'initialized_at': datetime.now().isoformat()
                })
                logger.info(f"✅ Agente {agent_instance.agent_id} registrado na categoria {category}")
        except Exception as e:
            logger.error(f"❌ Erro registrando agentes {category}: {e}", exc_info=True)

    def _setup_supreme_orchestration(self):
        try:
            logger.info(f"🔍 Verificando {len(self.all_agents)} agentes para encontrar orquestrador")
            orchestrator = None
            for agent_id, agent_data in self.all_agents.items():
                logger.info(f"🔎 Agente encontrado: {agent_id} (categoria: {agent_data['category']})")
                if 'orchestrator' in agent_id.lower():
                    orchestrator = agent_data['instance']
                    logger.info(f"👑 Orquestrador encontrado: {agent_id}")
                    break
            if orchestrator:
                logger.info(f"👑 Orquestração suprema configurada com {len(self.all_agents)-1} agentes")
            else:
                logger.error("❌ Agente orquestrador não encontrado")
                logger.warning("⚠️ Usando coordenação distribuída")
        except Exception as e:
            logger.error(f"❌ Erro configurando orquestração: {e}", exc_info=True)

    async def initialize_complete_system(self):
        try:
            logger.info("🚀 Iniciando SUNA-ALSHAM Sistema Completo v2.0")
            if not verificar_arquivos():
                logger.error("❌ Arquivos necessários não encontrados")
                self.system_status = 'error'
                return False
            
            if MultiAgentNetwork:
                self.network = MultiAgentNetwork()
                await self.network.initialize()
                logger.info("✅ Rede Multi-Agente inicializada")
            else:
                logger.error("❌ MultiAgentNetwork não disponível")
                self.system_status = 'error'
                return False
            
            def log_agent_creation(func, category, num_instances=1):
                try:
                    if func is None:
                        logger.error(f"❌ Função para {category} não disponível")
                        return
                    agents = func(self.network.message_bus, num_instances=num_instances) if category != 'meta_cognitive' else func(self.network.message_bus)
                    if not agents:
                        logger.error(f"❌ Nenhum agente criado para {category}")
                        return
                    if category == 'service' and num_instances == 1:
                        agents = agents[:
