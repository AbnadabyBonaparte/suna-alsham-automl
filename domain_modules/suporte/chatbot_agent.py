#!/usr/bin/env python3
"""
Módulo do Agente Chatbot - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida] - Orquestra uma conversa colaborando com o
AIPoweredAgent e o KnowledgeBaseAgent para entender e responder
às perguntas dos usuários.
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


class ChatbotAgent(BaseNetworkAgent):
    """
    Agente especialista em conversação para suporte automatizado.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o ChatbotAgent."""
        super().__init__(agent_id, AgentType.BUSINESS_DOMAIN, message_bus)
        self.capabilities.extend([
            "natural_language_understanding",
            "automated_response",
            "conversation_management"
        ])
        # Armazena o estado das conversas em andamento
        self.pending_conversations = {}
        logger.info(f"🤖 Agente Chatbot ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa uma mensagem de um usuário (nova requisição) ou uma
        resposta de um agente de apoio (AIPoweredAgent ou KnowledgeBaseAgent).
        """
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "process_user_message":
            await self.start_conversation_flow(message)
        
        elif message.message_type == MessageType.RESPONSE:
            await self.continue_conversation_flow(message)

    async def start_conversation_flow(self, original_message: AgentMessage):
        """Passo 1: Recebe a mensagem do usuário e pede para a IA analisar a intenção."""
        user_message = original_message.content.get("text", "")
        if not user_message:
            await self.publish_error_response(original_message, "Mensagem do usuário está vazia.")
            return

        conv_id = str(uuid.uuid4())
        logger.info(f"Nova conversa [ID: {conv_id}]. Analisando intenção da mensagem: '{user_message[:50]}...'")

        # Armazena o estado inicial da conversa
        self.pending_conversations[conv_id] = {
            "original_message": original_message,
            "state": "awaiting_intent"
        }

        # Cria um prompt para o agente de IA classificar a intenção
        prompt = f"""
        Analise a seguinte pergunta de um usuário e classifique-a em uma das
        seguintes intenções: 'password_reset', 'billing_question', 'feature_info', 'greeting', 'unknown'.
        Pergunta do usuário: "{user_message}"
        Responda apenas com a intenção. Ex: password_reset
        """

        request_to_ai = self.create_message(
            recipient_id="ai_analyzer_001",
            message_type=MessageType.REQUEST,
            content={"request_type": "analyze_intent", "text": prompt}, # Assumindo que o AIAnalyzer tem esse handler
            callback_id=conv_id
        )
        await self.message_bus.publish(request_to_ai)

    async def continue_conversation_flow(self, response_message: AgentMessage) -> None:
        """
        Handles the continuation of a conversation by processing responses from support agents.

        This method validates the conversation context, checks the current state,
        logs all relevant events, and routes the conversation to the next step or finalizes it.
        Robust error handling is provided for diagnostics and production reliability.

        Args:
            response_message (AgentMessage): The message containing the response from a support agent.

        Returns:
            None
        """
        conv_id: str = response_message.callback_id
        if not conv_id or conv_id not in self.pending_conversations:
            logger.warning(f"[ChatbotAgent] Resposta recebida para conversa desconhecida ou já finalizada: {conv_id}")
            return

        conversation: Dict[str, Any] = self.pending_conversations[conv_id]

        # Passo 2: Resposta da IA com a intenção do usuário
        if conversation["state"] == "awaiting_intent":
            intent: str = response_message.content.get("result", {}).get("intent", "unknown")
            logger.info(f"[ChatbotAgent] Conversa [ID: {conv_id}]. Intenção detectada: {intent}. Buscando na base de conhecimento.")

            conversation["state"] = "awaiting_kb_article"  # Atualiza o estado

            # Passo 2.5: Com a intenção, busca a resposta na base de conhecimento
            request_to_kb = self.create_message(
                recipient_id="knowledge_base_001",
                message_type=MessageType.REQUEST,
                content={"request_type": "search_article", "query": intent},
                callback_id=conv_id
            )
            await self.message_bus.publish(request_to_kb)

        # Passo 3: Resposta da Base de Conhecimento com o artigo
        elif conversation["state"] == "awaiting_kb_article":
            articles: List[Dict[str, Any]] = response_message.content.get("found_articles", [])

            if articles:
                answer: str = articles[0].get("content", "Não encontrei um passo a passo, mas sei que a resposta está na nossa base de conhecimento.")
            else:
                answer: str = "Desculpe, não consegui encontrar uma resposta para sua pergunta. Vou transferir para um atendente humano."

            logger.info(f"[ChatbotAgent] Conversa [ID: {conv_id}]. Resposta encontrada. Enviando ao usuário.")

            # Passo 4: Enviar a resposta final ao solicitante original
            final_response: Dict[str, Any] = {
                "status": "completed",
                "response_text": answer
            }
            await self.publish_response(conversation["original_message"], final_response)

            # Limpa a conversa da memória
            del self.pending_conversations[conv_id]
