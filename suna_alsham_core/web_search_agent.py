#!/usr/bin/env python3
"""
Módulo do Agente de Busca na Web - SUNA-ALSHAM

[Versão Defensiva] - Adiciona validação de robustez na entrada para
recusar requisições malformadas imediatamente e eliminar warnings.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

# [AUTENTICIDADE] Bibliotecas de busca são importadas de forma segura.
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
    Agente especialista em realizar buscas na web, extrair informações
    de páginas e retornar os resultados de forma estruturada.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o WebSearchAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend(["web_search", "information_extraction"])
        
        if not WEB_LIBS_AVAILABLE:
            self.status = "degraded"
            logger.warning("Bibliotecas 'aiohttp' ou 'beautifulsoup4' não encontradas. WebSearchAgent em modo degradado.")
        
        logger.info(f"🌐 {self.agent_id} (Busca Web) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de busca de forma defensiva."""
        
        # --- VALIDAÇÃO DEFENSIVA ADICIONADA AQUI ---
        if message.message_type != MessageType.REQUEST:
            return # Ignora mensagens que não são requisições (ex: heartbeats)

        search_action = message.content.get("request_type")
        query = message.content.get("query")

        if not search_action:
            logger.warning(f"WebSearchAgent recebeu requisição sem 'request_type' do agente '{message.sender_id}'. Ignorando.")
            # Não enviamos erro para não poluir o log, apenas ignoramos a ordem malformada.
            return
        
        if search_action != "search":
            logger.warning(f"Ação de busca desconhecida recebida de '{message.sender_id}': {search_action}")
            await self.publish_error_response(message, f"Ação de busca desconhecida: {search_action}")
            return
            
        if not query:
            logger.error(f"WebSearchAgent recebeu uma requisição de busca sem 'query' do agente '{message.sender_id}'.")
            await self.publish_error_response(message, "Termo de busca ('query') ausente ou vazio.")
            return
        # --- FIM DA VALIDAÇÃO ---

        # Se a validação passou, executa a busca
        results = await self.search(message.content)
        await self.publish_response(message, results)

    async def search(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA SIMULADA] Simula uma busca no Google.
        """
        query = request_data.get("query")
        logger.info(f"🔎 Buscando na web por: '{query}'...")
        
        # Simulação de resultados
        await asyncio.sleep(1.5)
        
        simulated_results = [
            {"title": f"Resultado 1 para '{query}'", "link": f"https://example.com/search?q={query}&p=1", "snippet": "Este é o primeiro resultado da busca..."},
            {"title": f"Resultado 2 para '{query}'", "link": f"https://example.com/search?q={query}&p=2", "snippet": "Este é o segundo resultado da busca..."},
        ]
        
        return {"status": "completed", "results": simulated_results}


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
