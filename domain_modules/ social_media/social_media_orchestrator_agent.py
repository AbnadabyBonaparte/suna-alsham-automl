#!/usr/bin/env python3
"""
Módulo do Agente Orquestrador de Mídias Sociais - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente atua como o ponto central de entrada e coordenação (roteador)
para todas as tarefas relacionadas ao domínio de Mídias Sociais. Ele recebe
requisições de alto nível e as delega para os agentes especialistas apropriados.
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


class SocialMediaOrchestratorAgent(BaseNetworkAgent):
    """
    O agente orquestrador para o domínio de Mídias Sociais.
    Sua principal função é rotear tarefas para os agentes especialistas.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SocialMediaOrchestratorAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "social_media_orchestration",
            "task_routing",
            "workflow_management",
        ])
        # Mapeia o tipo de requisição ao agente especialista e seu ID
        self.specialist_map = {
            "create_post_text": "content_creator_001",
            "create_video_from_images": "video_automation_001",
            "analyze_and_engage_comment": "engagement_maximizer_001",
            "find_influencers": "influencer_network_001",
        }
        self.pending_delegations = {}
        logger.info(f"mgr 🧠 Agente Orquestrador de Mídias Sociais ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa mensagens recebidas, roteando requisições para especialistas
        ou encaminhando respostas de volta ao solicitante original.
        """
        if message.message_type == MessageType.RESPONSE:
            await self._handle_specialist_response(message)
            return
            
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            specialist_id = self.specialist_map.get(request_type)

            if specialist_id:
                await self.delegate_to_specialist(specialist_id, message)
            else:
                await self.publish_error_response(message, f"O tipo de requisição '{request_type}' não é suportado por este módulo.")

    async def delegate_to_specialist(self, specialist_id: str, original_message: AgentMessage):
        """
        Encaminha a requisição para o agente especialista apropriado.
        """
        delegation_id = str(uuid.uuid4())
        
        # Cria uma nova mensagem para o especialista, mantendo o conteúdo original
        delegated_request = self.create_message(
            recipient_id=specialist_id,
            message_type=MessageType.REQUEST,
            content=original_message.content,
            callback_id=delegation_id
        )
        
        # Armazena a mensagem original para poder responder a ela mais tarde
        self.pending_delegations[delegation_id] = original_message
        
        await self.message_bus.publish(delegated_request)
        logger.info(f"Orquestrador delegou tarefa '{original_message.content.get('request_type')}' para {specialist_id} (ID da delegação: {delegation_id})")

    async def _handle_specialist_response(self, response_from_specialist: AgentMessage):
        """
        Recebe a resposta do especialista e a encaminha para o solicitante original.
        """
        delegation_id = response_from_specialist.callback_id
        if delegation_id not in self.pending_delegations:
            logger.warning(f"Orquestrador recebeu resposta para uma delegação desconhecida: {delegation_id}")
            return
            
        original_message = self.pending_delegations.pop(delegation_id)
        
        # Cria a resposta final para o solicitante original,
        # repassando o conteúdo da resposta do especialista.
        final_response = self.create_response(
            original_message,
            response_from_specialist.content
        )
        
        await self.message_bus.publish(final_response)
        logger.info(f"Orquestrador encaminhou a resposta final da delegação {delegation_id} para {final_response.recipient_id}.")
