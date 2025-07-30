#!/usr/bin/env python3
"""
Módulo do Agente Orquestrador de Suporte - SUNA-ALSHAM (ALSHAM GLOBAL)
"""

import logging
from typing import Any, Dict, List

from suna_alsham_core.multi_agent_network import (
    AgentMessage, 
    AgentType,
    BaseNetworkAgent, 
    MessageType, 
    Priority
)

# --- IMPORTAÇÕES ATUALIZADAS ---
from .ticket_manager_agent import TicketManagerAgent
from .chatbot_agent import ChatbotAgent
from .satisfaction_analyzer_agent import SatisfactionAnalyzerAgent
# -----------------------------

logger = logging.getLogger(__name__)


class SupportOrchestratorAgent(BaseNetworkAgent):
    """
    O agente orquestrador para o domínio de Suporte e Atendimento ao Cliente.
    """
    # ... (o resto da classe continua igual) ...
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SupportOrchestratorAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "support_orchestration",
            "ticket_routing",
            "sla_monitoring"
        ])
        logger.info(f"mgr 🎧 Agente Orquestrador de Suporte ({self.agent_id}) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        [LÓGICA FUTURA] Processa mensagens recebidas, roteando requisições
        para os agentes especialistas em suporte.
        """
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            logger.info(f"Orquestrador de Suporte recebeu a requisição '{request_type}'. Roteamento a ser implementado.")
            
            # Resposta temporária
            response_content = {
                "status": "received",
                "message": f"Requisição '{request_type}' recebida pelo Orquestrador de Suporte.",
            }
            await self.publish_response(message, response_content)


def create_suporte_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Função de fábrica para criar todos os agentes do módulo de Suporte.
    """
    logger.info("🔧 Criando agentes do domínio de Suporte...")
    
    # --- LISTA DE AGENTES ATUALIZADA ---
    agents = [
        SupportOrchestratorAgent("support_orchestrator_001", message_bus),
        TicketManagerAgent("ticket_manager_001", message_bus),
        ChatbotAgent("chatbot_001", message_bus),
        SatisfactionAnalyzerAgent("satisfaction_analyzer_001", message_bus)
    ]
    # ------------------------------------
    
    logger.info(f"✅ {len(agents)} agentes de Suporte criados.")
    return agents
