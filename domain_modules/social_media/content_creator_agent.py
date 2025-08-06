#!/usr/bin/env python3
"""
Agente Especialista: ContentCreatorAgent - Responsável por criar conteúdo.

[Versão 100% Real] - Usa a API da OpenAI para gerar texto com base
nos dados recebidos de outros agentes.
"""

import logging
import os
from typing import List, Dict

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI = None

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)

class ContentCreatorAgent(BaseNetworkAgent):
    """
    Agente especialista que usa IA para gerar conteúdo de texto de alta qualidade.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.append("ai_text_generation")
        self.openai_client = None
        if OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
            self.status = "active"
            logger.info(f"✍️ {self.agent_id} (Content Creator) especialista 100% real pronto para criar.")
        else:
            self.status = "degraded"
            logger.warning(f"✍️ {self.agent_id} em modo degradado. API da OpenAI não configurada.")

    async def _internal_handle_message(self, message: AgentMessage) -> None:
        """
        Handles a request to generate content using the OpenAI API.

        This method validates the incoming request, builds the final prompt, calls the OpenAI API asynchronously,
        logs all relevant events, and returns the generated text. Robust error handling is provided for diagnostics
        and production reliability.

        Args:
            message (AgentMessage): The incoming message containing prompt_template and context_data.

        Returns:
            None
        """
        if message.message_type != MessageType.REQUEST or self.status != "active":
            if self.status != "active":
                logger.warning(f"[ContentCreatorAgent] Content Creator não está operacional.")
                await self.publish_error_response(message, "Content Creator não está operacional.")
            return

        # Extrai os dados da tarefa enviados pelo Orquestrador
        prompt_template: str = message.content.get("prompt_template")
        context_data: str = message.content.get("context_data")

        if not prompt_template or not context_data:
            logger.warning("[ContentCreatorAgent] A tarefa não continha 'prompt_template' ou 'context_data'.")
            await self.publish_error_response(message, "A tarefa não continha 'prompt_template' ou 'context_data'.")
            return

        # Monta o prompt final para a IA
        prompt_final: str = f"{prompt_template}\n\nAqui estão os dados para usar como base:\n\n{context_data}"
        logger.info(f"✍️ [ContentCreatorAgent] Gerando texto com base no prompt...")

        try:
            # Chama a API da OpenAI para fazer o trabalho real
            chat_completion = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt_final}],
                temperature=0.5,
            )
            texto_gerado: str = chat_completion.choices[0].message.content

            logger.info(f"✍️ [ContentCreatorAgent] Texto gerado com sucesso.")

            # Envia a resposta de sucesso de volta para o orquestrador
            response_content: Dict[str, str] = {
                "status": "success",
                "result": {"generated_text": texto_gerado}
            }
            await self.publish_response(message, response_content)

        except Exception as e:
            logger.critical(f"✍️ [ContentCreatorAgent] Erro ao chamar a API da OpenAI: {e}", exc_info=True)
            await self.publish_error_response(message, f"Falha ao gerar conteúdo: {e}")
