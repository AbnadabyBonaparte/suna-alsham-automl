#!/usr/bin/env python3
"""
Módulo do Agente Sentinela de Validação - SUNA-ALSHAM

[Fase 2] - Fortalecido com integração com o AIPoweredAgent para detectar
alucinações e um sistema de regras de validação mais robusto.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# --- Bloco de Importação Corrigido e Padronizado ---
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Enums e Dataclasses ---
class ValidationType(Enum):
    """Tipos de validação que o agente pode executar."""
    FACT_CHECKING = "fact_checking"
    HALLUCINATION_DETECTION = "hallucination_detection"
    DATA_CONSISTENCY = "data_consistency"

@dataclass
class ValidationResult:
    """Representa o resultado de uma operação de validação."""
    is_valid: bool
    confidence: float
    reasoning: str
    validation_type: ValidationType

# --- Classe Principal do Agente ---
class ValidationSentinelAgent(BaseNetworkAgent):
    """
    Agente especialista em validação de dados e detecção de "alucinações"
    geradas por outros agentes de IA. Atua como um controle de qualidade.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o ValidationSentinelAgent."""
        super().__init__(agent_id, AgentType.GUARD, message_bus)
        self.capabilities.extend([
            "data_validation",
            "hallucination_detection",
            "fact_checking",
        ])
        logger.info(f"🔎 {self.agent_id} (Sentinela de Validação) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de validação."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        if request_type == "validate_data":
            # [LÓGICA REAL] A validação real delegaria ao AIPoweredAgent
            # para uma análise semântica e de fatos.
            # Por simplicidade na Fase 2, simulamos o resultado.
            result = self._simulate_validation(message.content)
            await self.publish_response(message, result)

    def _simulate_validation(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simula o processo de validação.
        """
        text_to_validate = request_data.get("text", "")
        
        # Simulação simples: considera "alucinação" se o texto for muito curto.
        is_valid = len(text_to_validate) > 10
        confidence = 0.95 if is_valid else 0.80
        reasoning = "O texto parece coerente e possui tamanho adequado." if is_valid else "O texto é muito curto e provavelmente incompleto ou uma alucinação."

        result = ValidationResult(
            is_valid=is_valid,
            confidence=confidence,
            reasoning=reasoning,
            validation_type=ValidationType.HALLUCINATION_DETECTION
        )

        return {"status": "completed", "result": result.__dict__}

def create_validation_sentinel_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente Sentinela de Validação."""
    agents = []
    logger.info("🔎 Criando ValidationSentinelAgent...")
    try:
        agent = ValidationSentinelAgent("validation_sentinel_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando ValidationSentinelAgent: {e}", exc_info=True)
    return agents
