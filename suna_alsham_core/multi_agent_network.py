#!/usr/bin/env python3
"""
Módulo Core da Rede Multi-Agente - A Espinha Dorsal do SUNA-ALSHAM.

[Fase 2] - Este módulo foi fortalecido com lógica real para gerenciamento
de respostas e um sistema de tópicos (publish/subscribe).
"""

import asyncio
import logging
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# --- Enums Fundamentais (sem alteração) ---

class AgentType(Enum):
    """Define os tipos e categorias de todos os agentes do sistema."""
    CORE = "core"
    GUARD = "guard"
    LEARN = "learn"
    SERVICE = "service"
    SYSTEM = "system"
    SPECIALIZED = "specialized"
    AI_POWERED = "ai_powered"
    AUTOMATOR = "automator"
    ORCHESTRATOR = "orchestrator"
    META_COGNITIVE = "meta_cognitive"


class MessageType(Enum):
    """Define os tipos de mensagens que podem ser trocadas na rede."""
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"
    TASK_ASSIGNMENT = "task_assignment"
    EMERGENCY = "emergency"


class Priority(Enum):
    """Define a prioridade de processamento das mensagens."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


# --- Estruturas de Dados Core (sem alteração) ---

@dataclass
class AgentCapability:
    """Representa uma capacidade específica de um agente."""
    name: str
    description: str
    input_types: List[str]
    output_types: List[str]
    processing_time_ms: float
    accuracy_score: float
    resource_cost: float


@dataclass
class AgentMessage:
    """Representa uma única mensagem trocada na rede."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = "system"
    recipient_id: str = "broadcast"
    message_type: MessageType = MessageType.NOTIFICATION
    priority: Priority = Priority.MEDIUM
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None


# --- Componentes da Rede (Lógica Fortalecida) ---

class MessageBus:
    """
    O sistema nervoso central da rede. Gerencia a entrega de mensagens
    entre todos os agentes de forma assíncrona e priorizada.
    """

    def __init__(self):
        """Inicializa o MessageBus."""
        self.subscribers: Dict[str, "BaseNetworkAgent"] = {}
        self.topic_subscribers: Dict[str, List[str]] = defaultdict(list)
        self.priority_queues = {p: asyncio.Queue() for p in Priority}
        self._is_running = False
        self._processing_task = None
        logger.info("✅ MessageBus inicializado com filas priorizadas e sistema de tópicos.")

    async def start(self):
        """Inicia o processamento da fila de mensagens."""
        if not self._is_running:
            self._is_running = True
            self._processing_task = asyncio.create_task(self._process_queues())
            logger.info("MessageBus iniciado.")

    async def stop(self):
        """Para o processamento de mensagens."""
        self._is_running = False
        if self._processing_task:
            self._processing_task.cancel()
            self._processing_task = None
        logger.info("MessageBus parado.")

    def register_agent(self, agent_id: str, agent: "BaseNetworkAgent"):
        """Registra um agente para receber mensagens diretas."""
        self.subscribers[agent_id] = agent
        logger.debug(f"Agente {agent_id} registrado no MessageBus.")

    def subscribe_to_topic(self, agent_id: str, topic: str):
        """Inscreve um agente em um tópico para receber broadcasts."""
        if agent_id not in self.topic_subscribers[topic]:
            self.topic_subscribers[topic].append(agent_id)
            logger.info(f"Agente {agent_id} inscrito no tópico '{topic}'.")

    async def publish(self, message: AgentMessage):
        """Publica uma mensagem na fila de prioridade apropriada."""
        await self.priority_queues[message.priority].put(message)

    async def _process_queues(self):
        """Loop principal que processa mensagens de todas as filas por prioridade."""
        while self._is_running:
            try:
                message = await self._get_next_message()
                if message:
                    await self._deliver_message(message)
                else:
                    await asyncio.sleep(0.01) # Evita busy-waiting
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro crítico no MessageBus: {e}", exc_info=True)

    async def _get_next_message(self) -> Optional[AgentMessage]:
        """Obtém a próxima mensagem a ser processada, respeitando a prioridade."""
        for priority in sorted(Priority, key=lambda p: p.value):
            if not self.priority_queues[priority].empty():
                return await self.priority_queues[priority].get()
        return None

    async def _deliver_message(self, message: AgentMessage):
        """Entrega uma mensagem para o(s) destinatário(s) correto(s)."""
        if message.recipient_id == "broadcast":
            topic = message.content.get("topic", "general")
            recipients = self.topic_subscribers.get(topic, [])
            delivery_tasks = [
                self.subscribers[agent_id].handle_message(message)
                for agent_id in recipients
                if agent_id in self.subscribers and agent_id != message.sender_id
            ]
            await asyncio.gather(*delivery_tasks)
        elif message.recipient_id in self.subscribers:
            await self.subscribers[message.recipient_id].handle_message(message)
        else:
            logger.warning(f"Destinatário '{message.recipient_id}' não encontrado para a mensagem {message.id}.")


class BaseNetworkAgent:
    """
    A classe base para TODOS os agentes do sistema.
    Fornece a funcionalidade essencial de comunicação e ciclo de vida.
    """

    def __init__(self, agent_id: str, agent_type: AgentType, message_bus: MessageBus):
        """Inicializa um BaseNetworkAgent."""
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_bus = message_bus
        self.status = "active"
        self.capabilities: List[AgentCapability] = []
        self.performance_metrics = defaultdict(float)
        
        # [LÓGICA REAL] Sistema para aguardar respostas de requisições.
        self._pending_responses: Dict[str, asyncio.Future] = {}
        
        # Auto-registro no MessageBus
        self.message_bus.register_agent(self.agent_id, self)

    def add_capability(self, capability: AgentCapability):
        """Adiciona uma nova capacidade ao agente."""
        self.capabilities.append(capability)

    async def handle_message(self, message: AgentMessage):
        """
        Handler principal de mensagens. Delega para handlers específicos
        e resolve futuras para requisições/respostas.
        """
        logger.debug(f"Agente {self.agent_id} recebeu mensagem {message.id} do tipo {message.message_type.value}")
        self.performance_metrics["messages_processed"] += 1

        # [LÓGICA REAL] Se for uma resposta, resolve a "Future" pendente.
        if message.message_type == MessageType.RESPONSE and message.correlation_id in self._pending_responses:
            future = self._pending_responses.pop(message.correlation_id)
            future.set_result(message)
            return

        # Delega para handlers específicos de cada agente
        await self._internal_handle_message(message)

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Este método deve ser sobrescrito pelas subclasses para implementar
        a lógica de negócio específica do agente.
        """
        if message.message_type == MessageType.REQUEST:
            # Lógica de resposta padrão se a subclasse não implementar _handle_request
            logger.warning(f"Agente {self.agent_id} recebeu um REQUEST mas não tem _handle_request implementado.")
            response = self.create_error_response(message, "Request handler not implemented.")
            await self.message_bus.publish(response)

    # --- MÉTODOS HELPER FORTALECIDOS ---
    
    def create_message(
        self, recipient_id: str, message_type: MessageType,
        content: Dict, priority: Priority = Priority.MEDIUM,
        correlation_id: Optional[str] = None
    ) -> AgentMessage:
        """Cria uma nova AgentMessage a partir deste agente."""
        return AgentMessage(
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            message_type=message_type,
            content=content,
            priority=priority,
            correlation_id=correlation_id,
        )

    def create_response(
        self, original_message: AgentMessage, content: Dict,
        priority: Optional[Priority] = None
    ) -> AgentMessage:
        """Cria uma mensagem de RESPOSTA a uma mensagem original."""
        return self.create_message(
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            content=content,
            priority=priority or original_message.priority,
            correlation_id=original_message.id,
        )

    def create_error_response(
        self, original_message: AgentMessage, error_message: str
    ) -> AgentMessage:
        """Cria uma mensagem de RESPOSTA de erro."""
        return self.create_response(
            original_message,
            content={"status": "error", "message": error_message},
            priority=Priority.HIGH,
        )

    async def send_request_and_wait(
        self, recipient_id: str, content: Dict, timeout: int = 30
    ) -> AgentMessage:
        """
        [LÓGICA REAL] Envia uma requisição e aguarda a resposta de forma síncrona.
        """
        request_message = self.create_message(
            recipient_id=recipient_id,
            message_type=MessageType.REQUEST,
            content=content,
        )
        
        future = asyncio.get_event_loop().create_future()
        self._pending_responses[request_message.id] = future
        
        await self.message_bus.publish(request_message)
        
        try:
            return await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError:
            self._pending_responses.pop(request_message.id, None)
            raise TimeoutError(f"Resposta de {recipient_id} para a requisição {request_message.id} demorou mais de {timeout}s.")
