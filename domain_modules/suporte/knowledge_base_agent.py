#!/usr/bin/env python3
"""
Módulo do Agente da Base de Conhecimento - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida] - Integra-se com o DatabaseAgent para realizar
buscas reais por artigos em uma tabela de base de conhecimento.
"""

import logging
import uuid
from typing import Any, Dict, List

from suna_alsham_core.multi_agent_network import (
    AgentMessage, 
    AgentType,
    BaseNetworkAgent, 
    MessageType, 
    Priority
)

logger = logging.getLogger(__name__)


class KnowledgeBaseAgent(BaseNetworkAgent):
    """
    Agente especialista em recuperação de informação de um banco de dados.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o KnowledgeBaseAgent."""
        super().__init__(agent_id, AgentType.BUSINESS_DOMAIN, message_bus)
        self.capabilities.extend([
            "information_retrieval",
            "document_search",
            "faq_lookup"
        ])
        self.pending_searches = {}
        logger.info(f"📚 Agente da Base de Conhecimento ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa uma requisição para buscar informação ou uma resposta do DatabaseAgent.
        """
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "search_article":
            await self.handle_search_request(message)

        elif message.message_type == MessageType.RESPONSE:
            await self.handle_db_response(message)

    async def handle_search_request(self, original_message: AgentMessage):
        """Recebe uma query e a transforma em uma busca SQL no banco de dados."""
        query_term = original_message.content.get("query", "")
        if not query_term:
            await self.publish_error_response(original_message, "Termo de busca não fornecido.")
            return

        search_id = str(uuid.uuid4())
        logger.info(f"Nova busca na KB [ID: {search_id}]. Buscando por artigos com a tag: '{query_term}'")

        self.pending_searches[search_id] = {
            "original_message": original_message
        }
        
        # Cria a query SQL para buscar artigos pela tag
        sql_query = "SELECT title, content FROM knowledge_base WHERE tags LIKE ?"
        # O parâmetro precisa ser formatado para a cláusula LIKE do SQL
        sql_params = [f"%{query_term}%"]

        request_to_db = self.create_message(
            recipient_id="database_001",
            message_type=MessageType.REQUEST,
            content={
                "request_type": "execute_query", 
                "query": sql_query,
                "params": sql_params
            },
            callback_id=search_id
        )
        await self.message_bus.publish(request_to_db)

    async def handle_db_response(self, response_message: AgentMessage) -> None:
        """
        Handles the result of a search from the DatabaseAgent and formats the response for the requester.

        This method validates the search context, checks the completion status,
        logs all relevant events, processes the database results, and sends the final response.
        Robust error handling is provided for diagnostics and production reliability.

        Args:
            response_message (AgentMessage): The message containing the database search results.

        Returns:
            None
        """
        search_id: str = response_message.callback_id
        if not search_id or search_id not in self.pending_searches:
            logger.warning(f"[KnowledgeBaseAgent] Resposta recebida para busca desconhecida ou já finalizada: {search_id}")
            return

        search_context: Dict[str, Any] = self.pending_searches.pop(search_id)
        original_message: AgentMessage = search_context["original_message"]

        db_data: List[List[Any]] = response_message.content.get("data", [])

        found_articles: List[Dict[str, str]] = []
        if response_message.content.get("status") == "completed" and db_data:
            for row in db_data:
                # Assumindo que a ordem das colunas é title, content
                if len(row) >= 2:
                    found_articles.append({"title": row[0], "content": row[1]})

        logger.info(f"[KnowledgeBaseAgent] Busca na KB [ID: {search_id}] concluída. {len(found_articles)} artigo(s) encontrado(s).")

        final_response: Dict[str, Any] = {
            "status": "completed",
            "found_articles": found_articles
        }
        await self.publish_response(original_message, final_response)
