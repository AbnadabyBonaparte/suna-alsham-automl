"""
ALSHAM QUANTUM - Agent Types
Definições de tipos e enums para agentes
"""
from enum import Enum
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

class AgentType(Enum):
    """
    Tipos de agentes no sistema ALSHAM QUANTUM.
    Fornece métodos utilitários para conversão e validação.
    """
    @classmethod
    def from_str(cls, value: str) -> 'AgentType':
        """
        Converte string para AgentType (case-insensitive).
        Args:
            value: String do tipo de agente.
        Returns:
            AgentType correspondente.
        Raises:
            ValueError se não encontrado.
        """
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"Tipo de agente desconhecido: {value}")
    CORE = "core"
    SPECIALIZED = "specialized" 
    DOMAIN = "domain"
    ANALYTICS = "analytics"
    SALES = "sales"
    SOCIAL_MEDIA = "social_media"
    SUPPORT = "support"
    AI_POWERED = "ai_powered"
    SYSTEM = "system"
    SERVICE = "service"

class AgentStatus(Enum):
    """
    Status possíveis dos agentes ALSHAM QUANTUM.
    """
    @classmethod
    def from_str(cls, value: str) -> 'AgentStatus':
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"Status de agente desconhecido: {value}")
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    STOPPED = "stopped"
    MAINTENANCE = "maintenance"

class MessageType(Enum):
    """
    Tipos de mensagens trocadas entre agentes.
    """
    @classmethod
    def from_str(cls, value: str) -> 'MessageType':
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"Tipo de mensagem desconhecido: {value}")
    COMMAND = "command"
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"
    ERROR = "error"

class Priority(Enum):
    """
    Níveis de prioridade de mensagens e agentes.
    """
    @classmethod
    def from_str(cls, value: str) -> 'Priority':
        for member in cls:
            if str(member.value).lower() == str(value).lower() or member.name.lower() == str(value).lower():
                return member
        raise ValueError(f"Prioridade desconhecida: {value}")
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5

@dataclass
class AgentConfig:
    """
    Configuração base de um agente ALSHAM QUANTUM.
    Inclui métodos de serialização e validação.
    """
    agent_id: str
    name: str
    agent_type: AgentType
    priority: Priority = Priority.NORMAL
    max_retries: int = 3
    timeout: int = 30
    enabled: bool = True
    config: Dict[str, Any] = None

    def __init__(self, agent_id: str, name: str, agent_type: Union[AgentType, str], priority: Union[Priority, str] = Priority.NORMAL, max_retries: int = 3, timeout: int = 30, enabled: bool = True, config: Optional[Dict[str, Any]] = None):
        self.agent_id = agent_id
        self.name = name
        self.agent_type = AgentType(agent_type) if not isinstance(agent_type, AgentType) else agent_type
        self.priority = Priority(priority) if not isinstance(priority, Priority) else priority
        self.max_retries = max_retries
        self.timeout = timeout
        self.enabled = enabled
        self.config = config or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "agent_type": self.agent_type.value,
            "priority": self.priority.value,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "enabled": self.enabled,
            "config": self.config
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentConfig':
        return cls(
            agent_id=data["agent_id"],
            name=data["name"],
            agent_type=AgentType.from_str(data["agent_type"]),
            priority=Priority.from_str(data.get("priority", Priority.NORMAL)),
            max_retries=data.get("max_retries", 3),
            timeout=data.get("timeout", 30),
            enabled=data.get("enabled", True),
            config=data.get("config", {})
        )

@dataclass 
class AgentMessage:
    """
    Estrutura de mensagem entre agentes ALSHAM QUANTUM.
    Inclui métodos de serialização e validação.
    """
    def __init__(self, message_id: str, from_agent: str, to_agent: str, message_type: Union[MessageType, str], payload: Dict[str, Any], timestamp: float, priority: Union[Priority, str] = Priority.NORMAL, requires_response: bool = False, correlation_id: Optional[str] = None):
        self.message_id = message_id
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message_type = MessageType(message_type) if not isinstance(message_type, MessageType) else message_type
        self.payload = payload
        self.timestamp = timestamp
        self.priority = Priority(priority) if not isinstance(priority, Priority) else priority
        self.requires_response = requires_response
        self.correlation_id = correlation_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "message_type": self.message_type.value,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "priority": self.priority.value,
            "requires_response": self.requires_response,
            "correlation_id": self.correlation_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMessage':
        return cls(
            message_id=data["message_id"],
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            message_type=MessageType.from_str(data["message_type"]),
            payload=data["payload"],
            timestamp=data["timestamp"],
            priority=Priority.from_str(data.get("priority", Priority.NORMAL)),
            requires_response=data.get("requires_response", False),
            correlation_id=data.get("correlation_id")
        )

@dataclass
class AgentMetrics:
    """
    Métricas de performance de um agente ALSHAM QUANTUM.
    Inclui métodos de serialização.
    """
    def __init__(self, messages_processed: int = 0, messages_sent: int = 0, errors_count: int = 0, average_response_time: float = 0.0, uptime: float = 0.0, last_activity: Optional[float] = None):
        self.messages_processed = messages_processed
        self.messages_sent = messages_sent
        self.errors_count = errors_count
        self.average_response_time = average_response_time
        self.uptime = uptime
        self.last_activity = last_activity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "messages_processed": self.messages_processed,
            "messages_sent": self.messages_sent,
            "errors_count": self.errors_count,
            "average_response_time": self.average_response_time,
            "uptime": self.uptime,
            "last_activity": self.last_activity
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMetrics':
        return cls(
            messages_processed=data.get("messages_processed", 0),
            messages_sent=data.get("messages_sent", 0),
            errors_count=data.get("errors_count", 0),
            average_response_time=data.get("average_response_time", 0.0),
            uptime=data.get("uptime", 0.0),
            last_activity=data.get("last_activity")
        )

# Aliases para compatibilidade
AgentTypeDef = AgentType
AgentStatusType = AgentStatus
MessageTypeDef = MessageType

# Constantes úteis
CORE_AGENT_TYPES = [AgentType.CORE, AgentType.SYSTEM, AgentType.SERVICE]
DOMAIN_AGENT_TYPES = [AgentType.ANALYTICS, AgentType.SALES, AgentType.SOCIAL_MEDIA, AgentType.SUPPORT]
ALL_AGENT_TYPES = list(AgentType)

# Mapeamento de tipos para strings legíveis
AGENT_TYPE_NAMES = {
    AgentType.CORE: "Core Agent",
    AgentType.SPECIALIZED: "Specialized Agent", 
    AgentType.DOMAIN: "Domain Agent",
    AgentType.ANALYTICS: "Analytics Agent",
    AgentType.SALES: "Sales Agent",
    AgentType.SOCIAL_MEDIA: "Social Media Agent",
    AgentType.SUPPORT: "Support Agent",
    AgentType.AI_POWERED: "AI-Powered Agent",
    AgentType.SYSTEM: "System Agent",
    AgentType.SERVICE: "Service Agent"
}


def get_agent_type_name(agent_type: Union[AgentType, str]) -> str:
    """
    Retorna nome legível do tipo de agente.
    Args:
        agent_type: AgentType ou string.
    Returns:
        str: Nome legível.
    """
    if isinstance(agent_type, str):
        try:
            agent_type = AgentType.from_str(agent_type)
        except Exception:
            return "Unknown Agent"
    return AGENT_TYPE_NAMES.get(agent_type, "Unknown Agent")


def is_core_agent(agent_type: Union[AgentType, str]) -> bool:
    """
    Verifica se é um agente do core.
    Args:
        agent_type: AgentType ou string.
    Returns:
        bool
    """
    if isinstance(agent_type, str):
        try:
            agent_type = AgentType.from_str(agent_type)
        except Exception:
            return False
    return agent_type in CORE_AGENT_TYPES


def is_domain_agent(agent_type: Union[AgentType, str]) -> bool:
    """
    Verifica se é um agente de domínio.
    Args:
        agent_type: AgentType ou string.
    Returns:
        bool
    """
    if isinstance(agent_type, str):
        try:
            agent_type = AgentType.from_str(agent_type)
        except Exception:
            return False
    return agent_type in DOMAIN_AGENT_TYPES
