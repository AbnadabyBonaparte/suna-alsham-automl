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

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa uma requisição para criar conteúdo.
        Espera receber um 'prompt_template' e 'context_data'.
        """
        if message.message_type != MessageType.REQUEST or self.status != "active":
            if self.status != "active":
                await self.publish_error_response(message, "Content Creator não está operacional.")
            return

        # Extrai os dados da tarefa enviados pelo Orquestrador
        prompt_template = message.content.get("prompt_template")
        context_data = message.content.get("context_data")

        if not prompt_template or not context_data:
            await self.publish_error_response(message, "A tarefa não continha 'prompt_template' ou 'context_data'.")
            return

        # Monta o prompt final para a IA
        prompt_final = f"{prompt_template}\n\nAqui estão os dados para usar como base:\n\n{context_data}"
        logger.info(f"✍️ [Content Creator] A gerar texto com base no prompt...")

        try:
            # Chama a API da OpenAI para fazer o trabalho real
            chat_completion = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt_final}],
                temperature=0.5,
            )
            texto_gerado = chat_completion.choices[0].message.content
            
            logger.info(f"✍️ [Content Creator] Texto gerado com sucesso.")
            
            # Envia a resposta de sucesso de volta para o orquestrador
            response_content = {
                "status": "success",
                "result": {"generated_text": texto_gerado}
            }
            await self.publish_response(message, response_content)

        except Exception as e:
            logger.error(f"✍️ [Content Creator] Erro ao chamar a API da OpenAI: {e}", exc_info=True)
            await self.publish_error_response(message, f"Falha ao gerar conteúdo: {e}")
