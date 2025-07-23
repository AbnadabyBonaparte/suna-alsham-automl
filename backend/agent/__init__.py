"""SUNA-ALSHAM Agent Package
Agentes Auto-Evolutivos com AutoML

Este pacote fornece uma estrutura para agentes de inteligência artificial auto-evolutivos
integrados com técnicas de AutoML, incluindo auto-reflexão, otimização e análise científica.

Versão: 2.1.0
"""

__version__ = "2.1.0"

from .ai_powered_agents import (
    SelfEvolvingAgent,
    AIOptimizationAgent,
    AIReflectionEngine,
    AISecurityValidator,
    ScientificLogger,
    AICache,
    AIReflectionResult,
    ScientificMetrics
)
from .multi_agent_network import (
    MultiAgentNetwork,
    NetworkCoordinator,
    BaseNetworkAgent,
    AnalyticsAgent,
    AgentType,
    MessageType,
    Priority,
    AgentMessage,
    AgentCapability,
    NetworkMetrics
)

__all__ = [
    "SelfEvolvingAgent",
    "AIOptimizationAgent",
    "AIReflectionEngine",
    "AISecurityValidator",
    "ScientificLogger",
    "AICache",
    "AIReflectionResult",
    "ScientificMetrics",
    "MultiAgentNetwork",
    "NetworkCoordinator",
    "BaseNetworkAgent",
    "AnalyticsAgent",
    "AgentType",
    "MessageType",
    "Priority",
    "AgentMessage",
    "AgentCapability",
    "NetworkMetrics"
]
