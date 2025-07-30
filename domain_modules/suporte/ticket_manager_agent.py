#!/usr/bin/env python3
"""
Módulo do Agente Gerenciador de Tickets - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida] - Integra-se com a API do Zendesk para criar tickets reais.
"""

import logging
import os
import httpx
import base64
from typing import Any, Dict, List

from suna_alsham_core.multi_agent_network import (
    AgentMessage, 
    AgentType,
    BaseNetworkAgent, 
    MessageType, 
    Priority
)

logger = logging.getLogger(__name__)


class TicketManagerAgent(BaseNetworkAgent):
    """
    Agente especialista em interagir com APIs de sistemas de tickets como o Zendesk.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o TicketManagerAgent."""
        super().__init__(agent_id, AgentType.BUSINESS_DOMAIN, message_bus)
        self.capabilities.extend([
            "ticket_creation",
            "ticket_update",
            "help_desk_integration"
        ])

        # Carrega as credenciais de forma segura do ambiente
        self.zendesk_domain = os.environ.get("ZENDESK_DOMAIN")
        self.zendesk_email = os.environ.get("ZENDESK_EMAIL")
        self.zendesk_token = os.environ.get("ZENDESK_API_TOKEN")

        if not all([self.zendesk_domain, self.zendesk_email, self.zendesk_token]):
            self.status = "degraded"
            logger.warning("Credenciais do Zendesk não configuradas. O TicketManagerAgent operará em modo degradado.")
        
        self.api_url = f"https://{self.zendesk_domain}.zendesk.com/api/v2/tickets.json"
        
        logger.info(f"🎫 Agente Gerenciador de Tickets ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para manipular tickets."""
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "create_ticket":
            result = await self.handle_create_ticket_request(message)
            await self.publish_response(message, result)

    async def handle_create_ticket_request(self, message: AgentMessage) -> Dict[str, Any]:
        """[LÓGICA REAL] Cria um novo ticket no Zendesk via API."""
        if self.status == "degraded":
            return {"status": "error", "message": "Serviço de tickets indisponível. Credenciais faltando."}

        ticket_data = message.content.get("ticket_data", {})
        subject = ticket_data.get("subject")
        comment_body = ticket_data.get("comment")
        requester_name = ticket_data.get("requester_name")
        requester_email = ticket_data.get("requester_email")

        if not all([subject, comment_body, requester_name, requester_email]):
            return {"status": "error", "message": "Dados insuficientes para criar o ticket (requer subject, comment, requester_name, requester_email)."}

        # Formata o payload para a API do Zendesk
        payload = {
            "ticket": {
                "subject": subject,
                "comment": { "body": comment_body },
                "requester": { "name": requester_name, "email": requester_email }
            }
        }
        
        # Monta o header de autenticação
        auth_str = f"{self.zendesk_email}/token:{self.zendesk_token}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_auth}"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status() # Lança uma exceção para respostas de erro (4xx ou 5xx)
                
                response_data = response.json()
                new_ticket_id = response_data.get("ticket", {}).get("id")

                logger.info(f"Ticket #{new_ticket_id} criado com sucesso no Zendesk.")
                return {
                    "status": "completed",
                    "ticket_id": new_ticket_id,
                    "external_url": f"https://{self.zendesk_domain}.zendesk.com/agent/tickets/{new_ticket_id}"
                }

        except httpx.HTTPStatusError as e:
            logger.error(f"Erro da API do Zendesk ao criar ticket: {e.response.status_code} - {e.response.text}")
            return {"status": "error", "message": f"Erro da API: {e.response.text}"}
        except Exception as e:
            logger.error(f"Erro inesperado ao criar ticket: {e}", exc_info=True)
            return {"status": "error", "message": f"Erro inesperado: {e}"}
