#!/usr/bin/env python3
"""
Módulo do Agente de Busca na Web - SUNA-ALSHAM
"""
import asyncio
import logging
from typing import Any, Dict, List

try:
    import aiohttp
    from bs4 import BeautifulSoup
    WEB_LIBS_AVAILABLE = True
except ImportError:
    WEB_LIBS_AVAILABLE = False

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

class WebSearchAgent(BaseNetworkAgent):
    """
    Agente especialista em realizar buscas na web e extrair informações.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend(["web_search", "information_extraction"])
        if not WEB_LIBS_AVAILABLE:
            self.status = "degraded"
            logger.warning("Bibliotecas 'aiohttp' ou 'beautifulsoup4' não encontradas. WebSearchAgent em modo degradado.")
        logger.info(f"🌐 {self.agent_id} (Busca Web) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de busca."""
        # --- CORREÇÃO 2: Reconhecer a ação "search" ---
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "search":
            result = await self.perform_search(message.content)
            await self.publish_response(message, result)
        else:
            action = message.content.get("request_type")
            logger.warning(f"Ação de busca desconhecida: {action}")
            # --- CORREÇÃO 1: Usar o nome de função correto ---
            await self.publish_error_response(message, "Ação de busca desconhecida")

    async def perform_search(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """[LÓGICA REAL] Realiza uma busca no Google e extrai os resultados."""
        if self.status == "degraded":
            return {"status": "error", "message": "Serviço de busca indisponível."}

        query = request_data.get("query")
        max_results = request_data.get("max_results", 5)
        
        # URL de busca do Google
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    html = await response.text()
            
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            # Extrai os resultados da busca
            for g in soup.find_all('div', class_='g'):
                a_tag = g.find('a')
                h3_tag = g.find('h3')
                span_tag = g.find('div', class_='VwiC3b')
                
                if a_tag and h3_tag and span_tag and a_tag['href'].startswith('http'):
                    results.append({
                        "title": h3_tag.text,
                        "link": a_tag['href'],
                        "snippet": span_tag.text
                    })
                    if len(results) >= max_results:
                        break
            
            logger.info(f"Busca por '{query}' retornou {len(results)} resultados.")
            return {"status": "completed", "results": results}

        except Exception as e:
            logger.error(f"Erro ao realizar busca na web: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

def create_web_search_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Busca na Web."""
    agents = []
    logger.info("🌐 Criando WebSearchAgent...")
    try:
        agent = WebSearchAgent("web_search_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando WebSearchAgent: {e}", exc_info=True)
    return agents
