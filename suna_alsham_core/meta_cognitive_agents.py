#!/usr/bin/env python3
"""
Módulo da Rede Multi-Agente - O Coração do Núcleo SUNA-ALSHAM
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

# ------------------------------
# TIPOS E ESTRUTURAS DE MENSAGEM
# ------------------------------

class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"
    BROADCAST = "broadcast"
    ERROR = "error"

class Priority(Enum):
    LOW = 3
    NORMAL = 2
    HIGH = 1
    CRITICAL = 0

class AgentType(Enum):
    CORE = "core"
    SPECIALIZED = "specialized"
    SERVICE = "service"
    SYSTEM = "system"
    META_COGNITIVE = "meta_cognitive"
    BUSINESS_DOMAIN = "business_domain"
    AI_POWERED = "ai_powered"
    ORCHESTRATOR = "orchestrator"
    GUARD = "guard"
    AUTOMATOR = "automator"

@dataclass
class AgentMessage:
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = "system"
    recipient_id: str = "broadcast"
    message_type: MessageType = MessageType.NOTIFICATION
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    priority: Priority = Priority.NORMAL
    callback_id: Optional[str] = None

# ------------------------------
# BARRAMENTO DE MENSAGENS
# ------------------------------

class MessageBus:
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue] = {}
        self.running = False
        logger.info("✅ MessageBus inicializado.")

    async def start(self):
        self.running = True
        logger.info("MessageBus iniciado.")

    async def stop(self):
        self.running = False
        logger.info("MessageBus finalizado.")

    async def publish(self, message: AgentMessage):
        if not self.running:
            return
        if message.recipient_id == "broadcast":
            for agent_id in self.queues:
                if agent_id != message.sender_id:
                    await self.queues[agent_id].put(message)
        elif message.recipient_id in self.queues:
            await self.queues[message.recipient_id].put(message)

    def subscribe(self, agent_id: str) -> asyncio.Queue:
        if agent_id not in self.queues:
            self.queues[agent_id] = asyncio.Queue()
        return self.queues[agent_id]

    def get_metrics(self) -> Dict[str, Any]:
        return {"subscribed_agents": len(self.queues)}

# ------------------------------
# CLASSE BASE DE AGENTES
# ------------------------------

class BaseNetworkAgent:
    def __init__(self, agent_id: str, agent_type: AgentType, message_bus: MessageBus):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_bus = message_bus
        self.inbox = self.message_bus.subscribe(self.agent_id)
        self.status = "active"
        self.capabilities: List[str] = []
        self.task = asyncio.create_task(self._run())

    async def _run(self):
        while True:
            try:
                message = await self.inbox.get()
                await self._internal_handle_message(message)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Erro no loop do agente {self.agent_id}: {e}", exc_info=True)

    async def _internal_handle_message(self, message: AgentMessage):
        pass

    def create_message(self, recipient_id: str, message_type: MessageType, content: Dict,
                       priority: Priority = Priority.NORMAL, callback_id: Optional[str] = None) -> AgentMessage:
        return AgentMessage(sender_id=self.agent_id, recipient_id=recipient_id,
                            message_type=message_type, content=content,
                            priority=priority, callback_id=callback_id)

    async def publish_response(self, original_message: AgentMessage, content: Dict):
        response = self.create_message(
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            content=content,
            callback_id=original_message.callback_id
        )
        await self.message_bus.publish(response)

    async def publish_error_response(self, original_message: AgentMessage, error_message: str):
        error_content = {"status": "error", "message": error_message}
        error_response = self.create_message(
            recipient_id=original_message.sender_id,
            message_type=MessageType.ERROR,
            content=error_content,
            callback_id=original_message.callback_id
        )
        await self.message_bus.publish(error_response)
