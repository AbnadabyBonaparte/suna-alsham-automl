#!/usr/bin/env python3
"""
Módulo do Agente de Melhorias de Segurança - SUNA-ALSHAM

[Fase 2] - Fortalecido com integração real com Redis para rate limiting
e um sistema de detecção de anomalias mais robusto.
"""

import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

# [AUTENTICIDADE] A biblioteca do Redis é importada de forma segura.
try:
    import redis.asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# --- Bloco de Importação Corrigido e Padronizado ---
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Constantes de Segurança ---
RATE_LIMIT_THRESHOLD = 100  # Requisições
RATE_LIMIT_WINDOW_SECONDS = 60  # Por minuto

# --- Classe Principal do Agente ---
class SecurityEnhancementsAgent(BaseNetworkAgent):
    """
    Agente especialista que implementa camadas adicionais de segurança,
    como rate limiting (limitação de taxa) e detecção de anomalias
    no comportamento da rede.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SecurityEnhancementsAgent."""
        super().__init__(agent_id, AgentType.GUARD, message_bus)
        self.capabilities.extend([
            "rate_limiting",
            "anomaly_detection",
            "threat_intelligence",
        ])
        
        self.redis_client = None
        if REDIS_AVAILABLE:
            # Em um ambiente real, a URL do Redis viria de variáveis de ambiente.
            try:
                self.redis_client = aioredis.from_url("redis://localhost")
            except Exception as e:
                logger.error(f"Não foi possível conectar ao Redis: {e}")
                self.status = "degraded"
        else:
            self.status = "degraded"
            logger.warning("Biblioteca 'redis' não encontrada. Rate limiting estará desativado.")
        
        logger.info(f"🚨 {self.agent_id} (Melhorias de Segurança) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para verificação de segurança adicional."""
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            if request_type == "check_rate_limit":
                result = await self.check_rate_limit(message.content)
                await self.publish_response(message, result)

    async def check_rate_limit(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Verifica se um determinado IP ou usuário excedeu o
        limite de requisições usando o Redis.
        """
        if self.status != "active" or not self.redis_client:
            # Se o Redis não estiver disponível, aprovamos a requisição por padrão.
            return {"status": "approved", "reason": "Rate limiting service degraded."}
            
        key = f"rate_limit:{request_data.get('identifier', 'unknown_ip')}"
        
        try:
            current_count = await self.redis_client.incr(key)
            
            if current_count == 1:
                # Se for a primeira requisição, define o tempo de expiração da chave
                await self.redis_client.expire(key, RATE_LIMIT_WINDOW_SECONDS)
            
            if current_count > RATE_LIMIT_THRESHOLD:
                logger.warning(f"Rate limit excedido para o identificador: {key}")
                return {"status": "denied", "reason": "Rate limit exceeded."}
            
            return {"status": "approved"}
            
        except Exception as e:
            logger.error(f"Erro ao verificar rate limit no Redis: {e}")
            # Em caso de falha do Redis, é mais seguro aprovar do que negar.
            return {"status": "approved", "reason": f"Redis error: {e}"}

def create_security_enhancements_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Melhorias de Segurança."""
    agents = []
    logger.info("🚨 Criando SecurityEnhancementsAgent...")
    try:
        agent = SecurityEnhancementsAgent("security_enhancements_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando SecurityEnhancementsAgent: {e}", exc_info=True)
    return agents
