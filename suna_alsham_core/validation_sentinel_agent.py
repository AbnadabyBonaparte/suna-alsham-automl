#!/usr/bin/env python3
"""
Módulo do Validation Sentinel Agent - O Guardião Supremo de Qualidade.

[Fase 2] - Fortalecido com estrutura de regras aprimorada e preparação
para integração com IA para detecção de alucinações.
"""

import asyncio
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class ValidationType(Enum):
    """Tipos de validação que o Sentinel pode realizar."""
    INPUT_SANITIZATION = "input_sanitization"
    OUTPUT_VALIDATION = "output_validation"
    SECURITY_VALIDATION = "security_validation"
    LOGICAL_CONSISTENCY = "logical_consistency"
    HALLUCINATION_PREVENTION = "hallucination_prevention"


class ValidationStatus(Enum):
    """Status de um resultado de validação."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"


class ValidationSeverity(Enum):
    """Severidade de uma falha de validação."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ValidationResult:
    """Representa o resultado de uma única verificação de validação."""
    validation_type: ValidationType
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


# --- Classe Principal do Agente ---

class ValidationSentinelAgent(BaseNetworkAgent):
    """
    Guardião Supremo de Qualidade. Valida dados, respostas, código e mais,
    garantindo a integridade e a confiabilidade de todo o sistema.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o ValidationSentinelAgent."""
        super().__init__(agent_id, AgentType.GUARD, message_bus)
        self.capabilities.extend([
            "input_sanitization",
            "output_validation",
            "hallucination_prevention",
            "data_integrity_check",
        ])

        # Padrões para detecção de problemas de segurança
        self._suspicious_patterns = {
            "sql_injection": re.compile(r"(\b(UNION|SELECT|INSERT|DROP|DELETE|ALTER)\b)", re.IGNORECASE),
            "xss": re.compile(r"<script|javascript:|on\w+\s*=", re.IGNORECASE),
        }
        
        logger.info(f"🛡️ {self.agent_id} (Sentinela de Validação) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de validação."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        if request_type == "validate_content":
            result = self.validate_content(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            logger.warning(f"Ação de validação desconhecida: {request_type}")
            await self.message_bus.publish(self.create_error_response(message, "Ação de validação desconhecida"))

    def validate_content(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa uma validação completa em um bloco de conteúdo.
        """
        content = str(request_data.get("content", ""))
        logger.info(f"🛡️ Validando conteúdo: '{content[:50]}...'")

        validation_results: List[ValidationResult] = []

        # Executa todas as validações relevantes
        validation_results.extend(self._perform_security_validation(content))
        validation_results.extend(self._perform_quality_validation(content))
        
        # [AUTENTICIDADE] Placeholder para a integração com IA
        validation_results.extend(self._perform_hallucination_detection(content))

        # Calcula score e determina ação
        overall_score = self._calculate_validation_score(validation_results)
        action_required = self._determine_action(validation_results)
        
        return {
            "status": "completed",
            "overall_score": overall_score,
            "action_required": action_required.value,
            "validation_results": [res.__dict__ for res in validation_results],
        }

    def _perform_security_validation(self, content: str) -> List[ValidationResult]:
        """Verifica o conteúdo contra padrões de segurança."""
        results = []
        for pattern_name, pattern in self._suspicious_patterns.items():
            if pattern.search(content):
                results.append(
                    ValidationResult(
                        validation_type=ValidationType.SECURITY_VALIDATION,
                        status=ValidationStatus.BLOCKED,
                        severity=ValidationSeverity.CRITICAL,
                        message=f"Padrão de segurança suspeito detectado: {pattern_name}",
                    )
                )
        return results

    def _perform_quality_validation(self, content: str) -> List[ValidationResult]:
        """Verifica o conteúdo contra padrões de qualidade básicos."""
        results = []
        if len(content.strip()) < 10:
            results.append(
                ValidationResult(
                    validation_type=ValidationType.OUTPUT_VALIDATION,
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.LOW,
                    message="Conteúdo parece curto ou incompleto.",
                )
            )
        return results
        
    def _perform_hallucination_detection(self, content: str) -> List[ValidationResult]:
        """
        [AUTENTICIDADE] Placeholder para detecção de alucinações.
        Na Fase 3, este método será integrado com o `AIAnalyzerAgent` para uma
        análise semântica e factual muito mais sofisticada.
        """
        results = []
        # Simulação simples: verifica palavras que indicam incerteza.
        uncertainty_words = ["eu acho", "talvez", "possivelmente", "parece que"]
        if any(word in content.lower() for word in uncertainty_words):
            results.append(
                ValidationResult(
                    validation_type=ValidationType.HALLUCINATION_PREVENTION,
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.MEDIUM,
                    message="Conteúdo contém indicadores de incerteza, pode ser uma alucinação.",
                    details={"words_found": [word for word in uncertainty_words if word in content.lower()]}
                )
            )
        return results

    def _calculate_validation_score(self, results: List[ValidationResult]) -> float:
        """Calcula um score de 0 a 100 baseado nos resultados da validação."""
        score = 100.0
        for res in results:
            if res.status == ValidationStatus.BLOCKED: return 0.0
            if res.severity == ValidationSeverity.CRITICAL: score -= 50
            elif res.severity == ValidationSeverity.HIGH: score -= 25
            elif res.severity == ValidationSeverity.MEDIUM: score -= 10
            elif res.severity == ValidationSeverity.LOW: score -= 5
        return max(0.0, score)

    def _determine_action(self, results: List[ValidationResult]) -> ValidationStatus:
        """Determina a ação final baseada na severidade dos resultados."""
        if any(r.status == ValidationStatus.BLOCKED for r in results):
            return ValidationStatus.BLOCKED
        if any(r.severity == ValidationSeverity.CRITICAL for r in results):
            return ValidationStatus.FAILED
        if any(r.severity == ValidationSeverity.HIGH for r in results):
            return ValidationStatus.NEEDS_REVIEW
        if any(r.status == ValidationStatus.WARNING for r in results):
            return ValidationStatus.WARNING
        return ValidationStatus.PASSED


def create_validation_sentinel_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente Validation Sentinel."""
    agents = []
    logger.info("🛡️ Criando ValidationSentinelAgent...")
    try:
        agent = ValidationSentinelAgent("validation_sentinel_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando ValidationSentinelAgent: {e}", exc_info=True)
    return agents
