#!/usr/bin/env python3
"""
Módulo do Agente de Rede de Influenciadores - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente constrói e gerencia uma rede de influenciadores digitais.
Ele usa o WebSearchAgent do núcleo para encontrar novos influenciadores
e, futuramente, gerenciará o contato e as métricas de colaboração.
"""

import logging
import uuid
from typing import Any, Dict, List

# Importa a classe base e os tipos essenciais do núcleo do sistema
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


class InfluencerNetworkAgent(BaseNetworkAgent):
    """
    Agente especialista em descobrir, contatar e gerenciar uma rede de
    influenciadores relevantes para a marca.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o InfluencerNetworkAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "influencer_discovery",
            "web_search_delegation",
            "contact_management",
            "performance_tracking",
        ])
        # Armazena o estado das buscas em andamento
        self.pending_searches = {}
        logger.info(f"🤝 Agente de Rede de Influenciadores ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa requisições para encontrar influenciadores ou respostas do WebSearchAgent.
        """
        if message.message_type == MessageType.RESPONSE:
            await self._handle_search_response(message)
            return

        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "find_influencers":
            await self.handle_find_influencers_request(message)

    async def handle_find_influencers_request(self, original_message: AgentMessage):
        """
        Recebe um tópico, delega a busca na web e armazena o contexto.
        """
        topic = original_message.content.get("topic")
        if not topic:
            await self.publish_error_response(original_message, "O tópico para a busca de influenciadores não foi fornecido.")
            return

        logger.info(f"Iniciando busca por influenciadores sobre o tópico: '{topic}'")

        # 1. Monta uma query de busca mais elaborada
        search_query = f"top influencers for {topic} on instagram and tiktok"
        
        # 2. Cria uma mensagem para o WebSearchAgent
        search_id = str(uuid.uuid4())
        request_to_searcher = self.create_message(
            recipient_id="web_search_001",  # ID do agente de busca na web
            message_type=MessageType.REQUEST,
            content={
                "request_type": "search",
                "query": search_query,
                "max_results": 10
            },
            callback_id=search_id
        )

        # 3. Armazena o contexto da busca
        self.pending_searches[search_id] = {
            "original_message": original_message,
            "topic": topic
        }

        # 4. Envia a requisição para o agente de busca
        await self.message_bus.publish(request_to_searcher)
        logger.info(f"Requisição de busca enviada para web_search_001 com search_id: {search_id}")

    async def _handle_search_response(self, response_message: AgentMessage) -> None:
        """
        Handles the response with search results received from the WebSearchAgent.

        This method validates the search context, checks the completion status,
        logs all relevant events, processes the search results, and sends the final response
        to the original requester. Robust error handling is provided for diagnostics and production reliability.

        Args:
            response_message (AgentMessage): The message containing the web search results.

        Returns:
            None
        """
        search_id: str = response_message.callback_id
        if search_id not in self.pending_searches:
            logger.warning(f"[InfluencerNetworkAgent] Recebida resposta de busca para uma tarefa desconhecida: {search_id}")
            return

        task_context: Dict[str, Any] = self.pending_searches.pop(search_id)
        original_message: AgentMessage = task_context["original_message"]

        if response_message.content.get("status") != "completed":
            logger.error(f"[InfluencerNetworkAgent] Busca na web falhou para a tarefa {search_id}.")
            await self.publish_error_response(original_message, "Falha na busca por influenciadores.")
            return

        search_results: List[Dict] = response_message.content.get("results", [])
        logger.info(f"[InfluencerNetworkAgent] Resultados da busca recebidos para a tarefa {search_id}. {len(search_results)} links encontrados.")

        # Processar os resultados (neste caso, apenas extrair)
        processed_results: List[Dict] = self._process_search_results(search_results)

        # Enviar a resposta final para o solicitante original
        final_response_content: Dict[str, Any] = {
            "status": "completed",
            "topic": task_context["topic"],
            "found_influencers": processed_results
        }
        final_response: AgentMessage = self.create_response(original_message, final_response_content)
        await self.message_bus.publish(final_response)

    def _process_search_results(self, results: List[Dict]) -> List[Dict]:
        """
        [SIMULAÇÃO] Simula o processamento dos resultados da busca.
        A lógica real aqui seria mais complexa, envolvendo extração de
        nomes, perfis sociais, etc.
        """
        influencers = []
        for result in results:
            influencers.append({
                "source_url": result.get("link"),
                "title": result.get("title"),
                "status": "pending_analysis"
            })
        return influencers
