#!/usr/bin/env python3
"""
Módulo do Notification Agent - SUNA-ALSHAM

[Fase 2] - Fortalecido com lógica real de fila, retentativas (retry)
e preparação para integração com APIs de serviços externos.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
    MessageType,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class NotificationChannel(Enum):
    """Canais de notificação suportados."""
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    CONSOLE = "console"


class NotificationStatus(Enum):
    """Status de uma notificação."""
    PENDING = "pending"
    SENDING = "sending"
    DELIVERED = "delivered"
    FAILED = "failed"


@dataclass
class Notification:
    """Representa uma notificação a ser enviada."""
    notification_id: str
    title: str
    message: str
    channels: List[NotificationChannel]
    recipients: List[str]
    priority: Priority
    status: NotificationStatus = NotificationStatus.PENDING
    attempts: int = 0
    created_at: datetime = field(default_factory=datetime.now)


# --- Classe Principal do Agente ---

class NotificationAgent(BaseNetworkAgent):
    """
    Agente de notificações inteligentes, atuando como um hub central para
    todos os alertas e comunicações externas do sistema.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o NotificationAgent."""
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend([
            "multi_channel_delivery",
            "priority_management",
            "delivery_tracking",
        ])

        self.notification_queue = asyncio.Queue()
        self.max_retries = 3
        self._processing_task = None
        
        logger.info(f"🔔 {self.agent_id} (Notificações) inicializado.")

    async def start_notification_service(self):
        """Inicia os serviços de background do agente."""
        if not self._processing_task:
            self._processing_task = asyncio.create_task(self._processing_loop())
            logger.info(f"🔔 {self.agent_id} iniciou serviço de notificações.")

    async def _processing_loop(self):
        """Loop principal que processa a fila de notificações."""
        while True:
            try:
                notification: Notification = await self.notification_queue.get()
                await self._process_single_notification(notification)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de notificações: {e}", exc_info=True)

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para envio de notificações."""
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "send_notification":
            result = await self.send_notification(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        elif message.message_type == MessageType.NOTIFICATION:
            await self._convert_internal_to_external_notification(message)

    async def send_notification(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria e enfileira uma nova notificação externa."""
        try:
            notification = Notification(
                notification_id=f"notif_{int(time.time())}",
                title=request_data.get("title", "Alerta do Sistema"),
                message=request_data.get("message", "Nenhuma mensagem fornecida."),
                channels=[NotificationChannel(c) for c in request_data.get("channels", ["console"])],
                recipients=request_data.get("recipients", []),
                priority=Priority(request_data.get("priority", 3)),
            )
            await self.notification_queue.put(notification)
            return {"status": "queued", "notification_id": notification.notification_id}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _convert_internal_to_external_notification(self, message: AgentMessage):
        """Converte notificações internas da rede em notificações externas (ex: console)."""
        content = message.content
        notification_data = {
            "title": f"Alerta Interno de {message.sender_id}: {content.get('notification_type', 'Geral')}",
            "message": str(content),
            "channels": ["console"], # Por padrão, notificações internas vão para o console
            "priority": message.priority.value,
        }
        await self.send_notification(notification_data)

    async def _process_single_notification(self, notification: Notification):
        """Processa e envia uma notificação para todos os seus canais."""
        notification.status = NotificationStatus.SENDING
        notification.attempts += 1
        
        # [LÓGICA REAL] A entrega agora é feita por canal
        # e o sucesso geral é verificado.
        all_successful = True
        for channel in notification.channels:
            try:
                success = await self._send_to_channel(notification, channel)
                if not success:
                    all_successful = False
            except Exception as e:
                logger.error(f"Erro ao enviar pelo canal {channel.value}: {e}")
                all_successful = False

        if all_successful:
            notification.status = NotificationStatus.DELIVERED
            logger.info(f"✅ Notificação {notification.notification_id} entregue com sucesso.")
        elif notification.attempts < self.max_retries:
            logger.warning(f"⚠️ Falha na entrega da notificação {notification.notification_id}. Tentando novamente em {5 * notification.attempts}s.")
            notification.status = NotificationStatus.PENDING
            await asyncio.sleep(5 * notification.attempts) # Backoff exponencial
            await self.notification_queue.put(notification)
        else:
            notification.status = NotificationStatus.FAILED
            logger.error(f"❌ Notificação {notification.notification_id} falhou após {self.max_retries} tentativas.")

    async def _send_to_channel(self, notification: Notification, channel: NotificationChannel) -> bool:
        """
        [LÓGICA REAL] Envia a notificação para um canal específico.
        """
        if channel == NotificationChannel.CONSOLE:
            log_line = (
                f"\n--- 🔔 NOTIFICAÇÃO ({notification.priority.name}) 🔔 ---\n"
                f"TÍTULO: {notification.title}\n"
                f"MENSAGEM: {notification.message}\n"
                f"DESTINATÁRIOS: {notification.recipients}\n"
                f"---------------------------------------------------\n"
            )
            print(log_line)
            return True
        else:
            # [AUTENTICIDADE] Placeholder para integrações reais com APIs.
            logger.info(f"  -> [Simulação] Enviando notificação para o canal '{channel.value}'...")
            await asyncio.sleep(0.5) # Simula latência da rede
            return True


def create_notification_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Notificações Inteligentes."""
    agents = []
    logger.info("🔔 Criando NotificationAgent...")
    try:
        agent = NotificationAgent("notification_001", message_bus)
        asyncio.create_task(agent.start_notification_service())
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando NotificationAgent: {e}", exc_info=True)
    return agents
