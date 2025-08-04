#!/usr/bin/env python3
"""
Agente Especialista: WebSearchAgent - Responsável por pesquisas na internet.

[Versão Robusta 2.0] - Implementa o ciclo completo de receber uma tarefa,
simular a sua execução e reportar o sucesso de volta ao Orquestrador.
"""

import asyncio
import logging
from typing import List, Dict

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)

class WebSearchAgent(BaseNetworkAgent):
    """
    Agente especialista que executa pesquisas na web.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.append("web_search")
        logger.info(f"🔎 {self.agent_id} (Web Search) especialista pronto para pesquisas.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa um pedido de pesquisa vindo de um orquestrador.
        """
        # 1. Ignorar mensagens que não são pedidos de execução
        if message.message_type != MessageType.REQUEST:
            return

        query = message.content.get("query")
        if not query:
            logger.error(f"🔎 [Web Search] Pedido recebido sem uma 'query' para pesquisar.")
            await self.publish_error_response(message, "A tarefa não continha a chave 'query'.")
            return

        logger.info(f"🔎 [Web Search] A iniciar pesquisa para: '{query}'...")

        # 2. Simular a execução da tarefa (aqui entraria a lógica real de pesquisa)
        try:
            # Simula o tempo que uma pesquisa real levaria
            await asyncio.sleep(3) 

            # Simula o resultado da pesquisa
            search_results = [
                f"Resultado 1 para '{query}'",
                f"Resultado 2 para '{query}'",
                f"Resultado 3 para '{query}'",
            ]
            
            logger.info(f"🔎 [Web Search] Pesquisa para '{query}' concluída com sucesso.")

            # 3. Enviar a resposta de sucesso de volta para o solicitante (o Orquestrador)
            response_content = {
                "status": "success",
                "result": {
                    "query_received": query,
                    "summary": f"A pesquisa encontrou {len(search_results)} resultados relevantes.",
                    "details": search_results
                }
            }
            await self.publish_response(message, response_content)

        except Exception as e:
            logger.error(f"🔎 [Web Search] Erro inesperado durante a pesquisa: {e}", exc_info=True)
            await self.publish_error_response(message, f"Falha interna no WebSearchAgent: {e}")


def create_web_search_agent(message_bus) -> List[BaseNetworkAgent]:
    """Fábrica para criar o WebSearchAgent."""
    try:
        return [WebSearchAgent("web_search_001", message_bus)]
    except Exception as e:
        logger.error(f"❌ Erro crítico criando WebSearchAgent: {e}", exc_info=True)
        return []
