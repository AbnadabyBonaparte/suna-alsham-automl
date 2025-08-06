#!/usr/bin/env python3
"""
Módulo do Agente Orquestrador de Mídias Sociais - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Final Fortalecida]
Este agente atua como o ponto central de entrada e coordenação (roteador)
para todas as tarefas relacionadas ao domínio de Mídias Sociais.
"""

import logging
import uuid
from typing import List

# Importa a classe base e os tipos essenciais do núcleo
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

# --- INÍCIO DAS ADIÇÕES ---
# Importa todos os agentes especialistas deste módulo para a função de fábrica
from .content_creator_agent import ContentCreatorAgent
from .engagement_maximizer_agent import EngagementMaximizerAgent
from .influencer_network_agent import InfluencerNetworkAgent
from .video_automation_agent import VideoAutomationAgent
# --- FIM DAS ADIÇÕES ---

logger = logging.getLogger(__name__)


class SocialMediaOrchestratorAgent(BaseNetworkAgent):
    """
    O agente orquestrador para o domínio de Mídias Sociais.
    """

    def __init__(self, agent_id: str, message_bus):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend(["social_media_orchestration", "task_routing"])
        
        self.specialist_map = {
            "create_post_text": "content_creator_001",
            "create_video_from_images": "video_automation_001",
            "analyze_and_engage_comment": "engagement_maximizer_001",
            "find_influencers": "influencer_network_001",
        }
        self.pending_delegations = {}
        logger.info(f"mgr 🧠 Agente Orquestrador de Mídias Sociais ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.RESPONSE:
            await self._handle_specialist_response(message)
            return
            
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            specialist_id = self.specialist_map.get(request_type)
            if specialist_id:
                await self.delegate_to_specialist(specialist_id, message)
            else:
                await self.publish_error_response(message, f"O tipo de requisição '{request_type}' não é suportado.")

    async def delegate_to_specialist(self, specialist_id: str, original_message: AgentMessage):
        delegation_id = str(uuid.uuid4())
        delegated_request = self.create_message(
            recipient_id=specialist_id,
            message_type=MessageType.REQUEST,
            content=original_message.content,
            callback_id=delegation_id
        )
        self.pending_delegations[delegation_id] = original_message
        await self.message_bus.publish(delegated_request)
        logger.info(f"Orquestrador delegou tarefa '{original_message.content.get('request_type')}' para {specialist_id}")

    async def _handle_specialist_response(self, response_from_specialist: AgentMessage):
        delegation_id = response_from_specialist.callback_id
        if delegation_id in self.pending_delegations:
            original_message = self.pending_delegations.pop(delegation_id)
            final_response = self.create_response(original_message, response_from_specialist.content)
            await self.message_bus.publish(final_response)
            logger.info(f"Orquestrador encaminhou a resposta final da delegação {delegation_id}.")

# --- FUNÇÃO DE FÁBRICA ADICIONADA ---
def create_social_media_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Factory function to create and initialize all Social Media agents for the ALSHAM QUANTUM system.

    This function instantiates all Social Media module agents, logs all relevant events for diagnostics,
    and returns them in a list for registration in the agent registry. Handles errors robustly
    and ensures all agents are ready for operation.

    Args:
        message_bus (Any): The message bus or communication channel for agent messaging.

    Returns:
        List[BaseNetworkAgent]: A list containing all initialized Social Media module agent instances.
    """
    agents: List[BaseNetworkAgent] = []
    logger.info("🔧 [Factory] Criando agentes do domínio de Mídias Sociais...")
    try:
        agents.append(SocialMediaOrchestratorAgent("social_media_orchestrator_001", message_bus))
        agents.append(ContentCreatorAgent("content_creator_001", message_bus))
        agents.append(EngagementMaximizerAgent("engagement_maximizer_001", message_bus))
        agents.append(InfluencerNetworkAgent("influencer_network_001", message_bus))
        agents.append(VideoAutomationAgent("video_automation_001", message_bus))
        logger.info(f"✅ {len(agents)} agentes de Mídias Sociais criados.")
    except Exception as e:
        logger.critical(f"❌ Erro crítico ao criar agentes de Mídias Sociais: {e}", exc_info=True)
    return agents
