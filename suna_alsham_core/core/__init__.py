"""
ALSHAM QUANTUM - Core Package
Módulo central para coordenação, tipos, agentes e mensageria do sistema ALSHAM QUANTUM.
Fornece todas as classes, enums, utilitários e instâncias globais para uso e integração.
"""

# Base agent classes
from .base_agent import BaseAgent, QuantumAgent
# Core system
from .quantum_core import QuantumCore, quantum_core, get_core, initialize_core
# Types, enums e estruturas
from .agent_types import (
    AgentType, AgentStatus, MessageType, Priority,
    AgentConfig, AgentMessage, AgentMetrics,
    get_agent_type_name, is_core_agent, is_domain_agent
)
# Message system
from .message import (
    Message, CommandMessage, RequestMessage, ResponseMessage,
    MessageBus, MessagePriority, MessageStatus,
    message_bus, get_message_bus, create_message,
    create_command, create_request, create_response
)

__all__ = [
    # Base classes
    'BaseAgent', 'QuantumAgent',
    # Core system
    'QuantumCore', 'quantum_core', 'get_core', 'initialize_core',
    # Types, enums e utilitários
    'AgentType', 'AgentStatus', 'MessageType', 'Priority',
    'AgentConfig', 'AgentMessage', 'AgentMetrics',
    'get_agent_type_name', 'is_core_agent', 'is_domain_agent',
    # Message system
    'Message', 'CommandMessage', 'RequestMessage', 'ResponseMessage',
    'MessageBus', 'MessagePriority', 'MessageStatus',
    'message_bus', 'get_message_bus', 'create_message',
    'create_command', 'create_request', 'create_response'
]
