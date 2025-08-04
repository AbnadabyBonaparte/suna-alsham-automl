#!/usr/bin/env python3
"""
Agente Especialista: NotificationAgent - Responsável por enviar notificações.

[Versão 100% Real] - Usa 'smtplib' para enviar e-mails reais.
"""

import asyncio
import logging
import os
import smtplib
from email.message import EmailMessage
from typing import List

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)

class NotificationAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.append("real_email_notification")
        self.email_user = os.environ.get('EMAIL_USER')
        self.email_password = os.environ.get('EMAIL_APP_PASSWORD')
        if self.email_user and self.email_password:
            logger.info(f"📧 {self.agent_id} (Notification) especialista 100% real pronto para enviar e-mails.")
        else:
            self.status = "degraded"
            logger.warning(f"📧 {self.agent_id} em modo degradado. Variáveis de ambiente EMAIL_USER ou EMAIL_APP_PASSWORD não configuradas.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type != MessageType.REQUEST or self.status == "degraded":
            if self.status == "degraded": await self.publish_error_response(message, "Serviço de notificação não está operacional.")
            return

        destinatario = message.content.get("recipient_email")
        assunto = message.content.get("subject")
        corpo = message.content.get("body")

        if not all([destinatario, assunto, corpo]):
            await self.publish_error_response(message, "A tarefa não continha 'recipient_email', 'subject' ou 'body'.")
            return

        logger.info(f"📧 [Notification] A preparar e-mail para '{destinatario}'...")
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._send_real_email, destinatario, assunto, corpo)
            logger.info(f"📧 [Notification] E-mail para '{destinatario}' enviado com sucesso.")
            await self.publish_response(message, {"status": "success", "message": "Email enviado."})
        except Exception as e:
            logger.error(f"📧 [Notification] Erro inesperado ao enviar e-mail: {e}", exc_info=True)
            await self.publish_error_response(message, f"Falha interna no NotificationAgent: {e}")

    def _send_real_email(self, to: str, subject: str, body: str):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.email_user
        msg['To'] = to
        msg.set_content(body)

        # Assumindo Gmail. Mude 'smtp.gmail.com' se usar outro provedor.
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.email_user, self.email_password)
            smtp.send_message(msg)

def create_notification_agent(message_bus) -> List[BaseNetworkAgent]:
    try:
        return [NotificationAgent("notification_001", message_bus)]
    except Exception as e:
        logger.error(f"❌ Erro crítico criando NotificationAgent real: {e}", exc_info=True)
        return []
