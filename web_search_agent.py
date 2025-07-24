import logging
from typing import List, Dict
from multi_agent_network import BaseNetworkAgent, AgentType
from uuid import uuid4
import requests

logger = logging.getLogger(__name__)

class WebSearchAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['web_search', 'technology_trends']
        logger.info(f"✅ {self.agent_id} inicializado")

    def search_improvements(self, query: str) -> Dict:
        try:
            # Simulação de busca (substituir por API real, ex.: GitHub API)
            response = requests.get(f"https://api.github.com/search/repositories?q={query}")
            if response.status_code == 200:
                data = response.json()
                improvements = [item['name'] for item in data['items'][:3]]  # Top 3 sugestões
                logger.info(f"🌐 Melhorias encontradas para {query}: {improvements}")
                return {"query": query, "improvements": improvements}
            else:
                logger.error(f"❌ Erro na busca: {response.status_code}")
                return {"query": query, "improvements": []}
        except Exception as e:
            logger.error(f"❌ Erro na busca: {e}")
            return {"query": query, "improvements": []}

def create_web_search_agent(message_bus) -> 'WebSearchAgent':
    try:
        agent_id = f"web_search_{uuid4()}"
        agent = WebSearchAgent(agent_id, AgentType.SPECIALIZED, message_bus)
        message_bus.register_agent(agent_id, agent)
        logger.info(f"✅ {agent_id} criado")
        return agent
    except Exception as e:
        logger.error(f"❌ Erro criando WebSearchAgent: {e}")
        return None
