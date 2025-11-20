"""
ALSHAM QUANTUM - Message System
Sistema de mensagens entre agentes
"""
import uuid
import time
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

class MessagePriority(Enum):
    """Prioridades de mensagem"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5

class MessageType(Enum):
    """Tipos de mensagem"""
    COMMAND = "command"
    REQUEST = "request" 
    RESPONSE = "response"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"
    ERROR = "error"
    BROADCAST = "broadcast"
    DIRECT = "direct"

class MessageStatus(Enum):
    """Status de mensagem"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    PROCESSED = "processed"
    FAILED = "failed"
    TIMEOUT = "timeout"

@dataclass
class Message:
    """Estrutura de mensagem base"""
    message_id: str
    from_agent: str
    to_agent: str
    message_type: MessageType
    payload: Dict[str, Any]
    timestamp: float
    priority: MessagePriority = MessagePriority.NORMAL
    status: MessageStatus = MessageStatus.PENDING
    requires_response: bool = False
    correlation_id: Optional[str] = None
    expires_at: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def __post_init__(self):
        """
        Inicializa campos obrigatórios e normaliza tipos.
        """
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = time.time()
        if isinstance(self.message_type, str):
            self.message_type = MessageType(self.message_type)
        if isinstance(self.priority, int):
            self.priority = MessagePriority(self.priority)
        if isinstance(self.priority, str):
            self.priority = MessagePriority[self.priority.upper()]
        if isinstance(self.status, str):
            self.status = MessageStatus(self.status)
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte mensagem para dicionário serializável.
        Returns:
            dict: Representação serializável da mensagem.
        """
        data = asdict(self)
        data['message_type'] = self.message_type.value
        data['priority'] = self.priority.value
        data['status'] = self.status.value
        return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """
        Cria mensagem a partir de dicionário.
        Args:
            data: Dicionário serializado.
        Returns:
            Message
        """
        data = dict(data)
        data['message_type'] = MessageType(data['message_type'])
        data['priority'] = MessagePriority(data['priority'])
        data['status'] = MessageStatus(data['status'])
        return cls(**data)
    def is_expired(self) -> bool:
        """
        Verifica se mensagem expirou.
        Returns:
            bool
        """
        if self.expires_at:
            return time.time() > self.expires_at
        return False
    def can_retry(self) -> bool:
        """
        Verifica se pode tentar reenviar.
        Returns:
            bool
        """
        return self.retry_count < self.max_retries
    def ack(self):
        """
        Marca mensagem como processada.
        """
        self.status = MessageStatus.PROCESSED
    def reply(self, payload: Dict[str, Any], success: bool = True, error: str = None) -> 'ResponseMessage':
        """
        Cria resposta para esta mensagem.
        Args:
            payload: Conteúdo da resposta.
            success: Se resposta é de sucesso.
            error: Mensagem de erro, se houver.
        Returns:
            ResponseMessage
        """
        return create_response(self, success=success, result=payload, error=error)

@dataclass
class CommandMessage(Message):
    """Mensagem de comando"""
    command: str = ""
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.parameters is None:
            self.parameters = {}
        self.message_type = MessageType.COMMAND

@dataclass  
class RequestMessage(Message):
    """Mensagem de requisição"""
    endpoint: str = ""
    method: str = "GET"
    headers: Dict[str, str] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.headers is None:
            self.headers = {}
        self.message_type = MessageType.REQUEST
        self.requires_response = True

@dataclass
class ResponseMessage(Message):
    """Mensagem de resposta"""
    success: bool = True
    result: Any = None
    error: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.message_type = MessageType.RESPONSE

class MessageBus:
    """Sistema de mensageria entre agentes"""
    
    def __init__(self):
        self.agents = {}
        self.message_queue = []
        self.message_history = []
        self.handlers = {}
        self._on_send_callbacks = []
        self._on_receive_callbacks = []
        import logging
        self.logger = logging.getLogger(__name__)

    def register_agent(self, agent_id: str, handler=None):
        """
        Registra um agente no message bus.
        Args:
            agent_id: ID do agente.
            handler: Função de callback para mensagens recebidas.
        """
        self.agents[agent_id] = {
            'handler': handler,
            'last_seen': time.time(),
            'messages_sent': 0,
            'messages_received': 0
        }
        self.logger.info(f"Agente registrado no bus: {agent_id}")

    def unregister_agent(self, agent_id: str):
        """
        Remove agente do message bus.
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.logger.info(f"Agente removido do bus: {agent_id}")

    def on_send(self, callback):
        """
        Registra callback para envio de mensagem.
        Args:
            callback: Função (message: Message) -> None
        """
        self._on_send_callbacks.append(callback)

    def on_receive(self, callback):
        """
        Registra callback para recebimento de mensagem.
        Args:
            callback: Função (message: Message) -> None
        """
        self._on_receive_callbacks.append(callback)

    def send_message(self, message: Message) -> bool:
        """
        Envia mensagem para agente.
        Args:
            message: Instância de Message.
        Returns:
            bool: True se enviado, False se falhou.
        """
        try:
            if message.to_agent not in self.agents:
                message.status = MessageStatus.FAILED
                self.logger.warning(f"Destino não encontrado: {message.to_agent}")
                return False
            self.message_queue.append(message)
            message.status = MessageStatus.SENT
            if message.from_agent in self.agents:
                self.agents[message.from_agent]['messages_sent'] += 1
            for cb in self._on_send_callbacks:
                try:
                    cb(message)
                except Exception as e:
                    self.logger.error(f"Erro em callback de envio: {e}")
            return True
        except Exception as e:
            message.status = MessageStatus.FAILED
            self.logger.error(f"Erro ao enviar mensagem: {e}")
            return False
    
    def send_to_agent(self, to_agent: str, from_agent: str, 
                     message_type: MessageType, payload: Dict[str, Any]) -> str:
        """Envia mensagem simples para agente"""
        message = Message(
            message_id=str(uuid.uuid4()),
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            timestamp=time.time()
        )
        
        self.send_message(message)
        return message.message_id
    
    def broadcast_message(self, from_agent: str, payload: Dict[str, Any]) -> List[str]:
        """Envia mensagem para todos os agentes"""
        message_ids = []
        
        for agent_id in self.agents:
            if agent_id != from_agent:
                msg_id = self.send_to_agent(
                    to_agent=agent_id,
                    from_agent=from_agent,
                    message_type=MessageType.BROADCAST,
                    payload=payload
                )
                message_ids.append(msg_id)
        
        return message_ids
    
    def get_messages_for_agent(self, agent_id: str) -> List[Message]:
        """
        Obtém mensagens pendentes para um agente.
        Args:
            agent_id: ID do agente.
        Returns:
            list[Message]
        """
        messages = []
        remaining_queue = []
        for message in self.message_queue:
            if message.to_agent == agent_id:
                if not message.is_expired():
                    messages.append(message)
                    message.status = MessageStatus.DELIVERED
                    self.agents[agent_id]['messages_received'] += 1
                    for cb in self._on_receive_callbacks:
                        try:
                            cb(message)
                        except Exception as e:
                            self.logger.error(f"Erro em callback de recebimento: {e}")
            else:
                remaining_queue.append(message)
        self.message_queue = remaining_queue
        return messages
    
    def get_agent_stats(self, agent_id: str) -> Dict[str, Any]:
        """Obtém estatísticas de um agente"""
        if agent_id in self.agents:
            return self.agents[agent_id].copy()
        return {}
    
    def cleanup_expired_messages(self):
        """Remove mensagens expiradas"""
        current_time = time.time()
        self.message_queue = [
            msg for msg in self.message_queue 
            if not msg.is_expired()
        ]

# Instância global do message bus
message_bus = MessageBus()

def get_message_bus() -> MessageBus:
    """Retorna instância global do message bus"""
    return message_bus


def create_message(from_agent: str, to_agent: str, message_type: MessageType, 
                  payload: Dict[str, Any], priority: MessagePriority = MessagePriority.NORMAL, 
                  requires_response: bool = False, correlation_id: str = None, expires_at: float = None) -> Message:
    """
    Cria nova mensagem.
    Args:
        from_agent: ID do remetente.
        to_agent: ID do destinatário.
        message_type: Tipo de mensagem.
        payload: Conteúdo da mensagem.
        priority: Prioridade (opcional).
        requires_response: Se espera resposta (opcional).
        correlation_id: ID de correlação (opcional).
        expires_at: Timestamp de expiração (opcional).
    Returns:
        Message
    """
    return Message(
        message_id=str(uuid.uuid4()),
        from_agent=from_agent,
        to_agent=to_agent,
        message_type=message_type,
        payload=payload,
        timestamp=time.time(),
        priority=priority,
        requires_response=requires_response,
        correlation_id=correlation_id,
        expires_at=expires_at
    )

def create_command(from_agent: str, to_agent: str, command: str, 
                  parameters: Dict[str, Any] = None) -> CommandMessage:
    """Cria mensagem de comando"""
    return CommandMessage(
        message_id=str(uuid.uuid4()),
        from_agent=from_agent,
        to_agent=to_agent,
        message_type=MessageType.COMMAND,
        payload={'command': command, 'parameters': parameters or {}},
        timestamp=time.time(),
        command=command,
        parameters=parameters or {}
    )

def create_request(from_agent: str, to_agent: str, endpoint: str, 
                  method: str = "GET", headers: Dict[str, str] = None) -> RequestMessage:
    """Cria mensagem de requisição"""
    return RequestMessage(
        message_id=str(uuid.uuid4()),
        from_agent=from_agent,
        to_agent=to_agent,
        message_type=MessageType.REQUEST,
        payload={'endpoint': endpoint, 'method': method, 'headers': headers or {}},
        timestamp=time.time(),
        endpoint=endpoint,
        method=method,
        headers=headers or {}
    )

def create_response(original_message: Message, success: bool = True, 
                   result: Any = None, error: str = None) -> ResponseMessage:
    """Cria mensagem de resposta"""
    return ResponseMessage(
        message_id=str(uuid.uuid4()),
        from_agent=original_message.to_agent,
        to_agent=original_message.from_agent,
        message_type=MessageType.RESPONSE,
        payload={'success': success, 'result': result, 'error': error},
        timestamp=time.time(),
        correlation_id=original_message.message_id,
        success=success,
        result=result,
        error=error
    )
