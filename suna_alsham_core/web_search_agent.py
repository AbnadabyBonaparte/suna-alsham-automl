#!/usr/bin/env python3
"""
Agente Especialista: WebSearchAgent - Responsável por pesquisas na internet.

[Versão 100% Real] - Usa 'requests' e 'BeautifulSoup' para executar
pesquisas reais na web e extrair dados concretos. Zero simulações.
"""

import asyncio
import logging
from typing import List, Dict

# Ferramentas para interação real com a web
import requests
from bs4 import BeautifulSoup

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)

class WebSearchAgent(BaseNetworkAgent):
    """
    Agente especialista que executa pesquisas reais na web para coletar dados.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.append("real_web_search")
        logger.info(f"🔎 {self.agent_id} (Web Search) especialista 100% real pronto para pesquisas.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa um pedido de pesquisa, executa-o na internet e retorna os dados.
        """
        if message.message_type != MessageType.REQUEST:
            return

        query = message.content.get("query")
        if not query:
            await self.publish_error_response(message, "A tarefa não continha a chave 'query'.")
            return

        logger.info(f"🔎 [Web Search] A iniciar pesquisa REAL para: '{query}'...")

        try:
            # Executa a pesquisa de forma síncrona num executor para não bloquear o loop de eventos
            loop = asyncio.get_running_loop()
            search_results = await loop.run_in_executor(
                None, self._perform_real_search, query
            )
            
            logger.info(f"🔎 [Web Search] Pesquisa real para '{query}' concluída com sucesso.")

            response_content = {
                "status": "success",
                "result": {
                    "query_received": query,
                    "summary": f"A pesquisa real encontrou {len(search_results)} links e títulos.",
                    "details": search_results # Retorna os dados reais coletados
                }
            }
            await self.publish_response(message, response_content)

        except Exception as e:
            logger.error(f"🔎 [Web Search] Erro inesperado durante a pesquisa real: {e}", exc_info=True)
            await self.publish_error_response(message, f"Falha interna no WebSearchAgent durante a pesquisa real: {e}")

    def _perform_real_search(self, query: str) -> List[Dict[str, str]]:
        """
        Função que executa a pesquisa web síncrona.
        É chamada dentro do 'run_in_executor' para não bloquear o sistema.
        """
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(search_url, headers=headers)
        response.raise_for_status() # Lança um erro se o pedido HTTP falhar

        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        # Procura pelos contêineres que geralmente englobam título e link
        for g in soup.find_all('div', class_='g'):
            a_tag = g.find('a')
            h3_tag = g.find('h3')
            if a_tag and h3_tag and a_tag['href']:
                results.append({
                    "title": h3_tag.get_text(),
                    "link": a_tag['href']
                })
                # Limita a 5 resultados para ser conciso
                if len(results) >= 5:
                    break
        
        if not results:
            # Fallback se a primeira busca não funcionar
            for a_tag in soup.find_all('a'):
                h3_tag = a_tag.find('h3')
                if h3_tag and a_tag['href'].startswith('http'):
                     results.append({
                        "title": h3_tag.get_text(),
                        "link": a_tag['href']
                    })
                if len(results) >= 5:
                    break

        return results


def create_web_search_agent(message_bus) -> List[BaseNetworkAgent]:
    """Fábrica para criar o WebSearchAgent 100% real."""
    try:
        return [WebSearchAgent("web_search_001", message_bus)]
    except Exception as e:
        logger.error(f"❌ Erro crítico criando WebSearchAgent real: {e}", exc_info=True)
        return []
