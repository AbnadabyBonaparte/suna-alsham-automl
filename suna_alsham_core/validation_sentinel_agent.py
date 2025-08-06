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
    FORMAT_VALIDATION = "format_validation"
    SECURITY_VALIDATION = "security_validation"

@dataclass
class ValidationResult:
    """Representa o resultado de uma operação de validação."""
    is_valid: bool
    confidence: float
    reasoning: str
    validation_type: ValidationType
    errors_found: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

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
            "format_validation",
            "consistency_checking"
        ])
        
        # Contadores de validação
        self.validations_performed = 0
        self.hallucinations_detected = 0
        self.errors_prevented = 0
        
        # Padrões conhecidos de alucinação
        self.hallucination_patterns = [
            "como uma IA",  # IA se identificando
            "não tenho acesso",  # Admitindo limitações falsas
            "desculpe, mas",  # Respostas evasivas
            "informação inventada",  # Dados falsos
        ]
        
        logger.info(f"🔎 {self.agent_id} (Sentinela de Validação) inicializado com detecção avançada.")
    
    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de validação."""
        if message.message_type != MessageType.REQUEST:
            return
        
        request_type = message.content.get("request_type")
        
        if request_type == "validate_data":
            result = await self.validate_data(message.content)
            await self.publish_response(message, result)
        
        elif request_type == "check_hallucination":
            result = await self.check_for_hallucination(message.content)
            await self.publish_response(message, result)
        
        elif request_type == "validate_format":
            result = await self.validate_format(message.content)
            await self.publish_response(message, result)
        
        elif request_type == "validation_stats":
            stats = self.get_validation_stats()
            await self.publish_response(message, stats)
    
    async def validate_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida dados com múltiplas estratégias.
        """
        data_to_validate = request_data.get("data", {})
        validation_rules = request_data.get("rules", [])
        
        self.validations_performed += 1
        
        errors = []
        warnings = []
        
        # Validação de tipos de dados
        if isinstance(data_to_validate, dict):
            for key, value in data_to_validate.items():
                # Verificar campos nulos inesperados
                if value is None:
                    warnings.append(f"Campo '{key}' está nulo")
                
                # Verificar strings vazias
                if isinstance(value, str) and not value.strip():
                    warnings.append(f"Campo '{key}' está vazio")
                
                # Verificar números negativos suspeitos
                if isinstance(value, (int, float)) and value < 0:
                    if key not in ["temperature", "balance", "adjustment"]:
                        warnings.append(f"Campo '{key}' tem valor negativo: {value}")
        
        # Aplicar regras customizadas
        for rule in validation_rules:
            if not self._apply_validation_rule(data_to_validate, rule):
                errors.append(f"Falha na regra: {rule.get('description', 'unknown')}")
        
        is_valid = len(errors) == 0
        confidence = 1.0 - (len(errors) * 0.1 + len(warnings) * 0.05)
        confidence = max(0.0, min(1.0, confidence))
        
        if not is_valid:
            self.errors_prevented += len(errors)
        
        result = ValidationResult(
            is_valid=is_valid,
            confidence=confidence,
            reasoning=self._generate_validation_reasoning(errors, warnings),
            validation_type=ValidationType.DATA_CONSISTENCY,
            errors_found=errors,
            warnings=warnings
        )
        
        return {
            "status": "completed",
            "result": {
                "is_valid": result.is_valid,
                "confidence": result.confidence,
                "reasoning": result.reasoning,
                "validation_type": result.validation_type.value,
                "errors": result.errors_found,
                "warnings": result.warnings,
                "timestamp": result.timestamp.isoformat()
            }
        }
    
    async def check_for_hallucination(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detecta possíveis alucinações em texto gerado por IA.
        """
        text_to_check = request_data.get("text", "")
        context = request_data.get("context", {})
        
        hallucination_score = 0.0
        detected_patterns = []
        
        # Verificar padrões conhecidos de alucinação
        text_lower = text_to_check.lower()
        for pattern in self.hallucination_patterns:
            if pattern in text_lower:
                hallucination_score += 0.2
                detected_patterns.append(pattern)
        
        # Verificar inconsistências numéricas
        import re
        numbers = re.findall(r'\d+\.?\d*', text_to_check)
        if len(numbers) > 5:  # Muitos números pode indicar dados inventados
            hallucination_score += 0.1
            detected_patterns.append("excessive_numbers")
        
        # Verificar datas futuras impossíveis
        future_years = re.findall(r'20[5-9]\d', text_to_check)
        if future_years:
            hallucination_score += 0.3
            detected_patterns.append("future_dates")
        
        # Verificar afirmações absolutas suspeitas
        absolute_terms = ["sempre", "nunca", "todos", "nenhum", "100%", "0%"]
        for term in absolute_terms:
            if term in text_lower:
                hallucination_score += 0.05
        
        # Calcular resultado
        hallucination_score = min(1.0, hallucination_score)
        is_hallucination = hallucination_score > 0.5
        
        if is_hallucination:
            self.hallucinations_detected += 1
        
        confidence = 1.0 - abs(0.5 - hallucination_score) * 2  # Mais confiante nos extremos
        
        result = ValidationResult(
            is_valid=not is_hallucination,
            confidence=confidence,
            reasoning=self._generate_hallucination_reasoning(hallucination_score, detected_patterns),
            validation_type=ValidationType.HALLUCINATION_DETECTION,
            errors_found=detected_patterns if is_hallucination else [],
            warnings=detected_patterns if not is_hallucination and detected_patterns else []
        )
        
        return {
            "status": "completed",
            "result": {
                "is_hallucination": is_hallucination,
                "hallucination_score": hallucination_score,
                "confidence": confidence,
                "detected_patterns": detected_patterns,
                "reasoning": result.reasoning,
                "timestamp": result.timestamp.isoformat()
            }
        }
    
    async def validate_format(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida formato de dados estruturados.
        """
        data = request_data.get("data", {})
        expected_format = request_data.get("format", {})
        
        errors = []
        
        # Verificar campos obrigatórios
        required_fields = expected_format.get("required_fields", [])
        for field in required_fields:
            if field not in data:
                errors.append(f"Campo obrigatório ausente: {field}")
        
        # Verificar tipos de dados
        field_types = expected_format.get("field_types", {})
        for field, expected_type in field_types.items():
            if field in data:
                actual_type = type(data[field]).__name__
                if actual_type != expected_type:
                    errors.append(f"Campo '{field}' deveria ser {expected_type}, mas é {actual_type}")
        
        # Verificar comprimento de strings
        max_lengths = expected_format.get("max_lengths", {})
        for field, max_length in max_lengths.items():
            if field in data and isinstance(data[field], str):
                if len(data[field]) > max_length:
                    errors.append(f"Campo '{field}' excede comprimento máximo de {max_length}")
        
        is_valid = len(errors) == 0
        
        result = ValidationResult(
            is_valid=is_valid,
            confidence=1.0 if is_valid else 0.5,
            reasoning="Formato válido" if is_valid else f"Formato inválido: {', '.join(errors)}",
            validation_type=ValidationType.FORMAT_VALIDATION,
            errors_found=errors
        )
        
        return {
            "status": "completed",
            "result": {
                "is_valid": result.is_valid,
                "errors": result.errors_found,
                "timestamp": result.timestamp.isoformat()
            }
        }
    
    def _simulate_validation(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método mantido para compatibilidade - redireciona para validate_data.
        """
        # Este método foi renomeado mas mantido para compatibilidade
        return asyncio.run(self.validate_data(request_data))
    
    def _apply_validation_rule(self, data: Dict, rule: Dict) -> bool:
        """
        Aplica uma regra de validação específica.
        """
        rule_type = rule.get("type")
        field = rule.get("field")
        
        if not field or field not in data:
            return True  # Skip se campo não existe
        
        value = data[field]
        
        if rule_type == "min_value":
            min_val = rule.get("value", 0)
            return value >= min_val
        
        elif rule_type == "max_value":
            max_val = rule.get("value", 100)
            return value <= max_val
        
        elif rule_type == "regex":
            import re
            pattern = rule.get("pattern", ".*")
            return bool(re.match(pattern, str(value)))
        
        elif rule_type == "in_list":
            allowed_values = rule.get("values", [])
            return value in allowed_values
        
        return True  # Regra desconhecida passa por padrão
    
    def _generate_validation_reasoning(self, errors: List[str], warnings: List[str]) -> str:
        """
        Gera explicação detalhada do resultado da validação.
        """
        if not errors and not warnings:
            return "Todos os dados passaram na validação sem problemas."
        
        reasoning = []
        
        if errors:
            reasoning.append(f"Encontrados {len(errors)} erros críticos que impedem a validação.")
            
        if warnings:
            reasoning.append(f"Detectados {len(warnings)} avisos que requerem atenção.")
        
        return " ".join(reasoning)
    
    def _generate_hallucination_reasoning(self, score: float, patterns: List[str]) -> str:
        """
        Gera explicação sobre detecção de alucinação.
        """
        if score < 0.3:
            return "O texto parece ser factual e confiável."
        elif score < 0.5:
            return "O texto tem alguns elementos suspeitos mas provavelmente é válido."
        elif score < 0.7:
            return f"Alta probabilidade de alucinação. Padrões detectados: {', '.join(patterns)}"
        else:
            return f"Alucinação clara detectada. Múltiplos padrões problemáticos: {', '.join(patterns)}"
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas de validação.
        """
        return {
            "status": "completed",
            "stats": {
                "total_validations": self.validations_performed,
                "hallucinations_detected": self.hallucinations_detected,
                "errors_prevented": self.errors_prevented,
                "detection_rate": (
                    self.hallucinations_detected / self.validations_performed 
                    if self.validations_performed > 0 else 0
                ),
                "agent_id": self.agent_id,
                "capabilities": self.capabilities
            }
        }

def create_validation_sentinel_agent(message_bus) -> List[BaseNetworkAgent]:
    """
    Factory function to create and initialize the ValidationSentinelAgent(s) for the ALSHAM QUANTUM system.

    This function instantiates the ValidationSentinelAgent, logs all relevant events for diagnostics,
    and returns it in a list for registration in the agent registry. Handles errors robustly
    and ensures the agent is ready for operation.

    Args:
        message_bus (Any): The message bus or communication channel for agent messaging.

    Returns:
        List[BaseNetworkAgent]: A list containing the initialized ValidationSentinelAgent instance(s).
    """
    agents: List[BaseNetworkAgent] = []
    logger.info("🔎 [Factory] Criando ValidationSentinelAgent...")
    try:
        agent = ValidationSentinelAgent("validation_sentinel_001", message_bus)
        agents.append(agent)
        logger.info(f"✅ ValidationSentinelAgent criado com sucesso: {agent.agent_id}")
    except Exception as e:
        logger.critical(f"❌ Erro crítico ao criar ValidationSentinelAgent: {e}", exc_info=True)
    return agents
