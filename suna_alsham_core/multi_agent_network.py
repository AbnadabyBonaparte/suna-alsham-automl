#!/usr/bin/env python3
"""
Módulo da Rede Multi-Agente - Coração do SUNA-ALSHAM
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

# Tipos de Mensagem
class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"
    # --- LINHAS DA CORREÇÃO ADICIONADAS AQUI ---
    HEARTBEAT = "heartbeat"
    BROADCAST = "broadcast"

# Prioridade de Mensagem
class Priority(Enum):
    LOW = 3
    NORMAL = 2
    HIGH = 1
    CRITICAL = 0

# Tipos de Agentes
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

# Estrutura da Mensagem de Agentes
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

# Barramento de Mensagens
class MessageBus:
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue] = {}
        self.running = False

    async def start(self):
        self.running = True

    async def stop(self):
        self.running = False

    async def publish(self, message: AgentMessage):
        if not self.running: return
        # Lógica para broadcast
        if message.recipient_id == "broadcast":
            for agent_id in self.queues:
                if agent_id != message.sender_id:
                    await self.queues[agent_id].put(message)
        # Lógica para mensagem direta
        elif message.recipient_id in self.queues:
            await self.queues[message.recipient_id].put(message)

    def subscribe(self, agent_id: str) -> asyncio.Queue:
        if agent_id not in self.queues:
            self.queues[agent_id] = asyncio.Queue()
        return self.queues[agent_id]

# 🆕 CLASSE ADICIONADA - CORREÇÃO PRINCIPAL
class MultiAgentNetwork:
    """
    Rede Multi-Agente Principal - Classe que estava faltando
    Gerencia todo o sistema de agentes do ALSHAM QUANTUM
    """
    def __init__(self):
        self.message_bus = MessageBus()
        self.agents: Dict[str, Any] = {}
        self.agent_registry = {}
        self.running = False
        logger.info("🌐 MultiAgentNetwork inicializada")

    async def start(self):
        """Inicia a rede multi-agente"""
        await self.message_bus.start()
        self.running = True
        logger.info("✅ MultiAgentNetwork ativada")

    async def stop(self):
        """Para a rede multi-agente"""
        await self.message_bus.stop()
        self.running = False
        logger.info("⏹️ MultiAgentNetwork desativada")

    def register_agent(self, agent):
        """Registra um agente na rede"""
        if hasattr(agent, 'agent_id'):
            agent_id = agent.agent_id
            self.agents[agent_id] = agent
            self.agent_registry[agent_id] = {
                'agent': agent,
                'type': getattr(agent, 'agent_type', 'unknown'),
                'status': getattr(agent, 'status', 'active'),
                'capabilities': getattr(agent, 'capabilities', [])
            }
            logger.debug(f"📝 Agente registrado: {agent_id}")
        else:
            # Fallback para agentes sem agent_id
            agent_id = f"agent_{len(self.agents)}"
            self.agents[agent_id] = agent
            self.agent_registry[agent_id] = {
                'agent': agent,
                'type': 'unknown',
                'status': 'active',
                'capabilities': []
            }
            logger.debug(f"📝 Agente registrado (auto-ID): {agent_id}")

    def get_agent_count(self) -> int:
        """Retorna o número total de agentes registrados"""
        return len(self.agents)

    def get_active_agents(self) -> List[str]:
        """Retorna lista de IDs dos agentes ativos"""
        return [
            agent_id for agent_id, info in self.agent_registry.items()
            if info.get('status') == 'active'
        ]

    def get_agents_by_type(self, agent_type: str) -> List[str]:
        """Retorna agentes filtrados por tipo"""
        return [
            agent_id for agent_id, info in self.agent_registry.items()
            if info.get('type') == agent_type
        ]

# Classe Base para Agentes de Rede
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
                self.inbox.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Erro no loop do agente {self.agent_id}: {e}", exc_info=True)

    async def _internal_handle_message(self, message: AgentMessage):
        """ Deve ser implementado nas subclasses. """
        pass

    def create_message(self, recipient_id: str, message_type: MessageType, content: Dict, priority: Priority = Priority.NORMAL, callback_id: Optional[str] = None) -> AgentMessage:
        return AgentMessage(sender_id=self.agent_id, recipient_id=recipient_id, message_type=message_type, content=content, priority=priority, callback_id=callback_id)

    def create_response(self, original_message: AgentMessage, content: Dict) -> AgentMessage:
        """Cria uma mensagem de resposta baseada na mensagem original"""
        return self.create_message(
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            content=content,
            callback_id=original_message.callback_id
        )

    async def publish_response(self, original_message: AgentMessage, content: Dict):
        response = self.create_response(original_message, content)
        await self.message_bus.publish(response)

    async def publish_error_response(self, original_message: AgentMessage, error_message: str):
        error_content = {"status": "error", "message": error_message}
        response = self.create_response(original_message, error_content)
        await self.message_bus.publish(response)

    @property
    def timestamp(self) -> str:
        """Timestamp atual para logs e identificação"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
