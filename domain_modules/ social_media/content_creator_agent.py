#!/usr/bin/env python3
"""
Módulo do Agente Criador de Conteúdo - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente é responsável pela criação de conteúdo para as mídias sociais.
Ele se integra com o AIPoweredAgent do núcleo para gerar textos criativos,
roteiros e outras peças de conteúdo com base em um tópico fornecido.
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


class ContentCreatorAgent(BaseNetworkAgent):
    """
    Agente especialista em gerar conteúdo textual e criativo para posts.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o ContentCreatorAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "text_generation",
            "creative_writing",
            "hashtag_suggestion",
            "ai_prompt_engineering",
        ])
        # Armazena o estado das tarefas de criação em andamento
        self.pending_creations = {}
        logger.info(f"✍️ Agente Criador de Conteúdo ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa requisições para criar conteúdo ou respostas do AIPoweredAgent.
        """
        if message.message_type == MessageType.RESPONSE:
            await self._handle_ai_response(message)
            return

        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "create_post_text":
            await self.handle_create_text_request(message)

    async def handle_create_text_request(self, original_message: AgentMessage):
        """
        Recebe um tópico, cria um prompt para a IA e delega a geração de texto.
        """
        topic = original_message.content.get("topic")
        platform = original_message.content.get("platform", "Instagram")

        if not topic:
            await self.publish_error_response(original_message, "O tópico para a criação de conteúdo não foi fornecido.")
            return

        logger.info(f"Iniciando criação de conteúdo para a plataforma '{platform}' sobre o tópico: '{topic}'")

        # 1. Engenharia de Prompt: Cria um prompt mais detalhado para a IA
        prompt = (
            f"Crie um texto para um post de {platform} sobre o seguinte tópico: '{topic}'. "
            f"O tom deve ser engajador e informativo. "
            f"Inclua 3 a 5 hashtags relevantes no final."
        )
        
        # 2. Cria uma mensagem para o AIPoweredAgent
        creation_id = str(uuid.uuid4())
        request_to_ai = self.create_message(
            recipient_id="ai_powered_001",  # ID do agente de IA do núcleo
            message_type=MessageType.REQUEST,
            content={
                "request_type": "generate_text",
                "prompt": prompt,
                "max_tokens": 280  # Limite de caracteres para um post
            },
            callback_id=creation_id
        )

        # 3. Armazena o contexto da criação
        self.pending_creations[creation_id] = {
            "original_message": original_message,
            "topic": topic
        }

        # 4. Envia a requisição para o agente de IA
        await self.message_bus.publish(request_to_ai)
        logger.info(f"Requisição de geração de texto enviada para ai_powered_001 com creation_id: {creation_id}")

    async def _handle_ai_response(self, response_message: AgentMessage):
        """
        Processa a resposta com o texto gerado recebida do AIPoweredAgent.
        """
        creation_id = response_message.callback_id
        if creation_id not in self.pending_creations:
            return

        task_context = self.pending_creations.pop(creation_id)
        original_message = task_context["original_message"]
        
        if response_message.content.get("status") != "completed":
            logger.error(f"Geração de texto falhou para a tarefa {creation_id}.")
            await self.publish_error_response(original_message, "Falha na geração de conteúdo pela IA.")
            return

        generated_text = response_message.content.get("result", {}).get("text", "")
        logger.info(f"Texto gerado pela IA recebido para a tarefa {creation_id}.")

        # 5. Enviar a resposta final para o solicitante original
        final_response_content = {
            "status": "completed",
            "topic": task_context["topic"],
            "post_text": generated_text.strip()
        }
        final_response = self.create_response(original_message, final_response_content)
        await self.message_bus.publish(final_response)
