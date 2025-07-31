#!/usr/bin/env python3
"""
Módulo de Notificação – SUNA-ALSHAM
Versão Viva – Simula envio de e-mail.
"""

import logging
from typing import Any, Dict, List
from suna_alsham_core.multi_agent_network import AgentMessage, AgentType, BaseNetworkAgent, MessageType

logger = logging.getLogger(__name__)

class NotificationAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.append("send_email")
        logger.info(f"🔔 {self.agent_id} inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type != MessageType.REQUEST:
            return
        if message.content.get("request_type") == "send_email":
            recipient = message.content.get("recipient")
            subject = message.content.get("subject")
            body = message.content.get("body")
            logger.info(f"📧 Simulando envio de e-mail para {recipient} | Assunto: {subject}")
            await self.publish_response(message, {"status": "sent", "recipient": recipient})

def create_notification_agent(message_bus) -> List[BaseNetworkAgent]:
    return [NotificationAgent("notification_001", message_bus)]
