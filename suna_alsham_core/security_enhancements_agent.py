#!/usr/-bin/env python3
"""
Módulo do Security Enhancements Agent - SUNA-ALSHAM

[Fase 2] - Fortalecido com lógica de rate limiting aprimorada e preparação
para integração real com Redis.
"""

import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

# [AUTENTICIDADE] A biblioteca do Redis é importada de forma segura.
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

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
            "performance_caching",
        ])
        
        # [LÓGICA REAL] Conexão com Redis
        self.redis_client = None
        if REDIS_AVAILABLE:
            try:
                # Na Fase 3, a URL virá das variáveis de ambiente
                self.redis_client = redis.Redis(decode_responses=True)
                self.redis_client.ping()
                logger.info("✅ Redis conectado para cache e rate limiting distribuído.")
            except redis.exceptions.ConnectionError:
                logger.warning("⚠️ Conexão com Redis falhou. Usando cache em memória.")
                self.redis_client = None
        else:
            logger.warning("⚠️ Biblioteca 'redis' não encontrada. Usando cache em memória.")

        # Fallback para cache em memória
        self.local_rate_limit_cache = defaultdict(lambda: defaultdict(deque))
        
        self.rate_limit_rules = {
            "default": {"requests": 100, "window": 60},
            "auth": {"requests": 10, "window": 300},
        }
        
        logger.info(f"🛡️ {self.agent_id} (Melhorias de Segurança) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de validação e otimização."""
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            handler = {
                "validate_request_security": self.validate_request_security,
            }.get(request_type)

            if handler:
                result = await handler(message.content)
                await self.message_bus.publish(self.create_response(message, result))

    async def validate_request_security(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa uma validação de segurança completa em uma requisição."""
        source_ip = request_data.get("source_ip", "unknown")
        
        # 1. Rate Limiting
        is_allowed, reason = await self._is_rate_limit_allowed(source_ip, "default")
        if not is_allowed:
            return {"status": "denied", "reason": f"Rate limit excedido: {reason}"}

        # 2. Validação de Input (Delegada ao ValidationSentinel)
        # [AUTENTICIDADE] A validação de input agora delega para o agente especialista.
        logger.info(f"Delegando validação de payload para o ValidationSentinelAgent...")
        validation_response = await self.send_request_and_wait(
            "validation_sentinel_001",
            {"request_type": "validate_content", "content": str(request_data.get("payload", {}))}
        )
        
        if validation_response.content.get("action_required") in ["blocked", "failed"]:
             return {"status": "denied", "reason": f"Validação de conteúdo falhou: {validation_response.content}"}

        return {"status": "approved", "message": "Requisição validada com sucesso."}

    async def _is_rate_limit_allowed(self, identifier: str, rule_type: str) -> (bool, str):
        """[LÓGICA REAL] Verifica se uma requisição está dentro do limite de taxa."""
        rule = self.rate_limit_rules.get(rule_type)
        if not rule: return True, "OK"
        
        # Tenta usar Redis primeiro, se não, usa o cache local
        if self.redis_client:
            return await self._check_redis_rate_limit(identifier, rule)
        else:
            return self._check_local_rate_limit(identifier, rule)

    async def _check_redis_rate_limit(self, identifier: str, rule: Dict) -> (bool, str):
        """Verifica o rate limit usando Redis com a técnica de sliding window."""
        try:
            key = f"rate_limit:{identifier}:{rule['window']}"
            current_time = time.time()
            window_start = current_time - rule["window"]
            
            pipe = self.redis_client.pipeline()
            pipe.zremrangebyscore(key, 0, window_start) # Remove timestamps antigos
            pipe.zadd(key, {str(current_time): current_time}) # Adiciona timestamp atual
            pipe.zcard(key) # Conta os timestamps na janela
            pipe.expire(key, rule["window"])
            
            results = await asyncio.to_thread(pipe.execute)
            request_count = results[2]
            
            if request_count > rule["requests"]:
                return False, f"Limite de {rule['requests']} reqs em {rule['window']}s atingido."
            return True, "OK"
        except Exception as e:
            logger.error(f"Erro no rate limit com Redis, usando fallback: {e}")
            return self._check_local_rate_limit(identifier, rule)

    def _check_local_rate_limit(self, identifier: str, rule: Dict) -> (bool, str):
        """Verifica o rate limit usando o cache local em memória."""
        current_time = time.time()
        window_start = current_time - rule["window"]

        requests = self.local_rate_limit_cache[identifier][rule["window"]]
        while requests and requests[0] < window_start:
            requests.popleft()
        
        if len(requests) >= rule["requests"]:
            return False, f"Limite de {rule['requests']} reqs em {rule['window']}s atingido."
        
        requests.append(current_time)
        return True, "OK"


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
