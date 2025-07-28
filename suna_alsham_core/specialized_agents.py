#!/usr-bin/env python3
"""
Módulo dos Agentes Especializados - SUNA-ALSHAM

[Fase 2] - Revisão Final. Alinhado com a BaseNetworkAgent fortalecida.
Define agentes com capacidades focadas em domínios específicos como análise de dados,
otimização de processos e geração de relatórios.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import List

# Import alinhado com a Fase 1
from suna_alsham_core.multi_agent_network import (
    AgentType,
    BaseNetworkAgent,
)

logger = logging.getLogger(__name__)


class SpecialtyType(Enum):
    """Tipos de especialização dos agentes."""
    DATA_ANALYSIS = "data_analysis"
    REPORTING = "reporting"
    PREDICTION = "prediction"


@dataclass
class AgentConfig:
    """Configuração para criação de agentes especializados."""
    agent_class: type
    agent_id: str
    specialty: SpecialtyType


class AnalyticsAgent(BaseNetworkAgent):
    """
    Agente especializado em análise de dados e geração de relatórios.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o AnalyticsAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend(["data_analysis", "reporting"])
        self.specialty = SpecialtyType.DATA_ANALYSIS
        logger.info(f"✅ {self.agent_id} inicializado com especialização em {self.specialty.value}")


class PredictorAgent(BaseNetworkAgent):
    """
    Agente especializado em realizar predições e previsões (forecasting).
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o PredictorAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend(["prediction", "forecasting"])
        self.specialty = SpecialtyType.PREDICTION
        logger.info(f"✅ {self.agent_id} inicializado com especialização em {self.specialty.value}")


# Configuração centralizada para a criação dos agentes especializados.
# Isso torna a adição de novos agentes mais fácil no futuro.
AGENT_CONFIGURATIONS = [
    AgentConfig(AnalyticsAgent, "analytics_001", SpecialtyType.DATA_ANALYSIS),
    AgentConfig(PredictorAgent, "predictor_001", SpecialtyType.PREDICTION),
    AgentConfig(AnalyticsAgent, "analytics_002", SpecialtyType.REPORTING),
    # Agentes adicionais podem ser configurados aqui
]


def create_specialized_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Cria e inicializa os agentes especializados com base na configuração.

    Args:
        message_bus: O barramento de mensagens para a comunicação entre agentes.

    Returns:
        Uma lista de instâncias de agentes especializados prontos para operar.
    """
    agents = []
    logger.info("🎯 Criando agentes especializados...")

    existing_agents = set(message_bus.subscribers.keys())

    for config in AGENT_CONFIGURATIONS:
        if config.agent_id not in existing_agents:
            try:
                agent = config.agent_class(config.agent_id, message_bus)
                agents.append(agent)
            except Exception as e:
                logger.error(
                    f"❌ Erro criando agente especializado {config.agent_id}: {e}",
                    exc_info=True,
                )
        else:
            logger.warning(
                f"⚠️ Agente {config.agent_id} já existe - pulando criação para evitar duplicação."
            )

    logger.info(f"✅ {len(agents)} novos agentes especializados criados com sucesso.")
    return agents
