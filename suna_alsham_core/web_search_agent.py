#!/usr/bin/env python3
"""
Módulo do Agente de Busca na Web - SUNA-ALSHAM

[Versão Final Otimizada]
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
)

logger = logging.getLogger(__name__)

class WebSearchAgent(BaseNetworkAgent):
    """
    Agente especialista em realizar buscas na web e extrair informações estruturadas.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend(["web_search", "information_extraction"])

        if not WEB_LIBS_AVAILABLE:
            self.status = "degraded"
            logger.warning("Bibliotecas 'aiohttp' ou 'beautifulsoup4' não encontradas. WebSearchAgent em modo degradado.")

        logger.info(f"🌐 {self.agent_id} (Busca Web) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de busca com validação robusta."""
        if message.message_type != MessageType.REQUEST:
            return

        search_action = message.content.get("request_type")
        query = message.content.get("query")

        if search_action != "search":
            await self.publish_error_response(message, f"Ação de busca desconhecida: {search_action}")
            return

        if not query:
            await self.publish_error_response(message, "Termo de busca ('query') ausente ou vazio.")
            return

        results = await self.search(query)
        await self.publish_response(message, results)

    async def search(self, query: str) -> Dict[str, Any]:
        """Realiza uma busca web simulada e retorna resultados estruturados."""
        logger.info(f"🔎 Realizando busca simulada por: '{query}'")
        await asyncio.sleep(1.5)

        simulated_results = [
            {"title": f"Resultado 1 para '{query}'", "link": f"https://example.com/search?q={query}&p=1", "snippet": "Este é o primeiro resultado da busca."},
            {"title": f"Resultado 2 para '{query}'", "link": f"https://example.com/search?q={query}&p=2", "snippet": "Este é o segundo resultado da busca."},
        ]

        return {"status": "completed", "results": simulated_results}


def create_web_search_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Busca na Web com segurança."""
    agents = []
    logger.info("🌐 Criando WebSearchAgent...")
    try:
        agent = WebSearchAgent("web_search_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando WebSearchAgent: {e}", exc_info=True)
    return agents
