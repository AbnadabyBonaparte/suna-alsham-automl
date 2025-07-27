#!/usr/bin/env python3
"""
Módulo do Security Enhancements Agent - SUNA-ALSHAM

Define o agente responsável por melhorias de segurança robustas e otimizações
de performance, como rate limiting, validação de input e cache.
"""

import hashlib
import json
import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Dataclasses para Tipagem Forte ---

@dataclass
class SecurityEvent:
    """Representa um evento de segurança para auditoria."""
    event_type: str
    severity: str  # low, medium, high, critical
    source_ip: str
    details: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    blocked: bool = False


# --- Classe Principal do Agente ---

class SecurityEnhancementsAgent(BaseNetworkAgent):
    """
    Agente focado em segurança e otimização de performance. Atua como um
    Web Application Firewall (WAF) e um otimizador para a rede de agentes.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SecurityEnhancementsAgent."""
        super().__init__(agent_id, AgentType.GUARD, message_bus)
        self.capabilities.extend([
            "rate_limiting",
            "input_validation",
            "audit_logging",
            "performance_optimization",
        ])
        
        # [AUTENTICIDADE] A lógica real de cache e rate limit usaria Redis
        # para um ambiente distribuído. Para simplificar e manter a
        # portabilidade, usamos caches em memória.
        self.rate_limit_cache = defaultdict(lambda: defaultdict(deque))
        self.performance_cache = {} # Cache LRU simulado
        
        self.rate_limit_rules = {
            "default": {"requests": 100, "window": 60},  # 100 req/minuto
            "auth": {"requests": 10, "window": 300},     # 10 req/5 minutos
        }
        
        logger.info(f"🛡️ {self.agent_id} (Melhorias de Segurança) inicializado.")

    async def handle_message(self, message: AgentMessage):
        """Processa requisições de validação e otimização."""
        await super().handle_message(message)
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            handler = {
                "validate_request": self.validate_request,
                "get_cached_data": self.get_cached_data,
            }.get(request_type)

            if handler:
                result = await handler(message.content)
                await self.message_bus.publish(self.create_response(message, result))

    async def validate_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa uma validação de segurança completa em uma requisição.
        """
        source_ip = request_data.get("source_ip", "unknown")
        
        # 1. Rate Limiting
        is_allowed, reason = self._is_rate_limit_allowed(source_ip, "default")
        if not is_allowed:
            await self._log_security_event("rate_limit_exceeded", "medium", source_ip, {"reason": reason})
            return {"status": "denied", "reason": f"Rate limit excedido: {reason}"}

        # 2. Validação de Input
        # [AUTENTICIDADE] A lógica real usaria o ValidationSentinelAgent.
        # Esta é uma validação local simplificada.
        is_valid, error_msg = self._validate_input(request_data.get("payload", {}))
        if not is_valid:
            await self._log_security_event("input_validation_failed", "high", source_ip, {"error": error_msg})
            return {"status": "denied", "reason": f"Validação de input falhou: {error_msg}"}

        return {"status": "approved", "message": "Requisição validada com sucesso."}

    def _is_rate_limit_allowed(self, identifier: str, rule_type: str) -> (bool, str):
        """Verifica se uma requisição está dentro do limite de taxa."""
        rule = self.rate_limit_rules.get(rule_type, self.rate_limit_rules["default"])
        current_time = time.time()
        window_start = current_time - rule["window"]

        # Limpa timestamps antigos da janela
        requests = self.rate_limit_cache[rule_type][identifier]
        while requests and requests[0] < window_start:
            requests.popleft()
        
        if len(requests) >= rule["requests"]:
            return False, f"Limite de {rule['requests']} requisições em {rule['window']}s atingido."
        
        requests.append(current_time)
        return True, "OK"

    def _validate_input(self, payload: Dict[str, Any]) -> (bool, str):
        """[SIMULAÇÃO] Valida o payload da requisição contra ameaças comuns."""
        payload_str = str(payload).lower()
        if any(threat in payload_str for threat in ["<script>", "drop table", "select * from"]):
            return False, "Potencial de XSS ou SQL Injection detectado."
        return True, "Payload parece seguro."

    async def get_cached_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [AUTENTICIDADE] Retorna dados de um cache. Na Fase 2, esta lógica será
        expandida para um cache multi-camadas (memória, Redis, disco).
        """
        key = request_data.get("key")
        if key in self.performance_cache:
            return {"status": "hit", "data": self.performance_cache[key]}
        else:
            # Simula a busca e o armazenamento no cache
            data_to_cache = f"Dados para a chave '{key}' gerados em {datetime.now()}"
            self.performance_cache[key] = data_to_cache
            return {"status": "miss", "data": data_to_cache}

    async def _log_security_event(self, event_type: str, severity: str, source_ip: str, details: Dict):
        """Envia um evento de segurança para o LoggingAgent."""
        # A lógica real seria enviar uma mensagem para o LoggingAgent ou SecurityGuardian
        logger.warning(f"SECURITY EVENT [{severity.upper()}]: {event_type} | IP: {source_ip} | Detalhes: {details}")


def create_security_enhancements_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Melhorias de Segurança."""
    agents = []
    logger.info("🛡️ Criando SecurityEnhancementsAgent...")
    try:
        agent = SecurityEnhancementsAgent("security_enhancements_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando SecurityEnhancementsAgent: {e}", exc_info=True)
    return agents
