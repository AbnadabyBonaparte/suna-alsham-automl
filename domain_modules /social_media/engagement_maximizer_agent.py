#!/usr/bin/env python3
"""
Módulo do Agente Maximizador de Engajamento - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente é projetado para aumentar a interação em posts de mídias sociais.
Ele analisa comentários usando o AIAnalyzerAgent para determinar o sentimento
e, com base nisso, executa ações como curtir ou responder.
"""

import logging
import uuid
from typing import Any, Dict

# Importa a classe base e os tipos essenciais do núcleo do sistema
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


class EngagementMaximizerAgent(BaseNetworkAgent):
    """
    Agente especialista em analisar e interagir com o público para
    maximizar o engajamento em plataformas de mídia social.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o EngagementMaximizerAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "comment_analysis",
            "automated_liking",
            "sentiment_detection_delegation",
            "automated_replying",
        ])
        # Armazena o estado das tarefas em andamento
        self.pending_tasks = {}
        logger.info(f"🚀 Agente Maximizador de Engajamento ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa mensagens recebidas. Pode ser uma requisição inicial para
        analisar um comentário ou uma resposta do AIAnalyzerAgent.
        """
        # Se for uma resposta a uma de nossas requisições
        if message.message_type == MessageType.RESPONSE:
            await self._handle_response(message)
            return

        # Se for uma nova requisição de tarefa
        if message.message_type == MessageType.REQUEST:
            handler = self._get_request_handler(message.content.get("request_type"))
            if handler:
                await handler(message)
            else:
                logger.warning(f"Tipo de requisição desconhecida: {message.content.get('request_type')}")

    def _get_request_handler(self, request_type: str):
        """Retorna a função de tratamento apropriada para a requisição."""
        handlers = {
            "analyze_and_engage_comment": self.handle_analyze_comment_request,
        }
        return handlers.get(request_type)

    async def handle_analyze_comment_request(self, original_message: AgentMessage):
        """
        Recebe um comentário, delega a análise de sentimento para a IA
        e armazena o contexto para a ação futura.
        """
        comment_text = original_message.content.get("comment_text")
        comment_id = original_message.content.get("comment_id")
        post_id = original_message.content.get("post_id")

        if not all([comment_text, comment_id, post_id]):
            await self.publish_error_response(original_message, "Dados da requisição incompletos.")
            return

        logger.info(f"Analisando comentário '{comment_text[:30]}...' (ID: {comment_id})")

        # 1. Criar uma mensagem para o AIAnalyzerAgent
        task_id = str(uuid.uuid4())
        request_to_analyzer = self.create_message(
            recipient_id="ai_analyzer_001",  # ID do agente de análise de IA
            message_type=MessageType.REQUEST,
            content={
                "request_type": "analyze_sentiment",
                "text": comment_text,
            },
            callback_id=task_id # ID para rastrear a resposta
        )

        # 2. Armazenar o contexto da tarefa original
        self.pending_tasks[task_id] = {
            "original_message": original_message,
            "comment_id": comment_id,
            "post_id": post_id
        }

        # 3. Enviar a requisição para a fila de mensagens
        await self.message_bus.publish(request_to_analyzer)
        logger.info(f"Requisição de análise de sentimento enviada para ai_analyzer_001 com task_id: {task_id}")

    async def _handle_response(self, response_message: AgentMessage):
        """
        Processa a resposta recebida do AIAnalyzerAgent.
        """
        task_id = response_message.callback_id
        if task_id not in self.pending_tasks:
            logger.warning(f"Recebida resposta para uma tarefa desconhecida ou já concluída: {task_id}")
            return

        task_context = self.pending_tasks.pop(task_id)
        original_message = task_context["original_message"]
        
        if response_message.content.get("status") != "completed":
            logger.error(f"Análise de sentimento falhou para a tarefa {task_id}.")
            await self.publish_error_response(original_message, "Falha na análise de sentimento.")
            return

        sentiment = response_message.content.get("result", {}).get("sentiment", "neutral")
        logger.info(f"Sentimento recebido para a tarefa {task_id}: {sentiment.upper()}")

        # 4. Tomar uma ação com base no sentimento
        action_taken = None
        if sentiment == "positive":
            await self._like_post(task_context["post_id"], task_context["comment_id"])
            action_taken = "liked"
        elif sentiment == "question":
            # [LÓGICA FUTURA] Delegar para um agente de resposta
            action_taken = "marked_for_reply"

        # 5. Enviar a resposta final para o solicitante original
        final_response_content = {
            "status": "completed",
            "action_taken": action_taken,
            "sentiment_detected": sentiment,
            "comment_id": task_context["comment_id"]
        }
        final_response = self.create_response(original_message, final_response_content)
        await self.message_bus.publish(final_response)

    async def _like_post(self, post_id: str, comment_id: str):
        """
        [SIMULAÇÃO] Simula a ação de curtir um comentário via API.
        """
        logger.info(f"AÇÃO SIMULADA: Curtindo o comentário {comment_id} no post {post_id}.")
        # Em uma implementação real, aqui iria o código da API:
        # await social_media_api.like_comment(comment_id=comment_id)
        await asyncio.sleep(0.1) # Simula latência de rede
