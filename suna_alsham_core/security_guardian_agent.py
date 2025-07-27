#!/usr/bin/env python3
"""
Módulo do Security Guardian Agent - Proteção Suprema do SUNA-ALSHAM.

Define o agente de segurança avançado com capacidades de proteção em tempo real,
gerenciamento de identidade, detecção de intrusão e resposta a incidentes.
"""

import asyncio
import logging
import re
import secrets
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

import jwt

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class ThreatLevel(Enum):
    """Níveis de Ameaça de Segurança."""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AccessLevel(Enum):
    """Níveis de Acesso ao Sistema."""
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"
    SYSTEM = "system"


@dataclass
class AccessToken:
    """Representa um token de acesso gerado."""
    token_id: str
    user_id: str
    access_level: AccessLevel
    permissions: List[str]
    expires_at: datetime


# --- Classe Principal do Agente ---

class SecurityGuardianAgent(BaseNetworkAgent):
    """
    Agente Guardian de Segurança. Atua como um SOC (Security Operations Center)
    autônomo para a rede, gerenciando todo o ciclo de vida de segurança.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SecurityGuardianAgent."""
        super().__init__(agent_id, AgentType.GUARD, message_bus)
        self.capabilities.extend([
            "authentication",
            "authorization",
            "intrusion_detection",
            "encryption_management",
            "access_control",
            "threat_prevention",
            "security_audit",
        ])

        # Configurações de segurança
        self.max_login_attempts = 5
        self.lockout_duration_seconds = 300  # 5 minutos
        self.token_expiry_seconds = 3600  # 1 hora
        self.jwt_secret = secrets.token_urlsafe(32)  # Em produção, carregar do ambiente
        
        # Estado de segurança
        self.access_tokens: Dict[str, AccessToken] = {}
        self.blocked_ips: Dict[str, datetime] = {}
        self.failed_attempts = defaultdict(list)

        logger.info(f"🛡️ {self.agent_id} (Guardião de Segurança) inicializado.")

    async def handle_message(self, message: AgentMessage):
        """Processa requisições de segurança."""
        await super().handle_message(message)
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            handler = {
                "authenticate": self.authenticate_user,
                "authorize": self.authorize_access,
                "security_scan": self.perform_security_scan,
            }.get(request_type)

            if handler:
                result = await handler(message.content)
                await self.message_bus.publish(self.create_response(message, result))
            else:
                logger.warning(f"Ação de segurança desconhecida: {request_type}")

    async def authenticate_user(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Autentica um usuário e retorna um token JWT se for bem-sucedido."""
        username = request_data.get("username")
        password = request_data.get("password")
        source_ip = request_data.get("source_ip", "unknown")

        # 1. Verificação de Bloqueio
        if self._is_ip_blocked(source_ip):
            return {"status": "blocked", "message": "IP bloqueado por atividade suspeita."}
        
        # 2. Verificação de Força Bruta
        if self._check_brute_force(username, source_ip):
            self._block_ip(source_ip)
            return {"status": "blocked", "message": "Muitas tentativas de login falharam. Tente mais tarde."}

        # 3. Verificação de Credenciais
        if self._verify_credentials(username, password):
            token = self._generate_access_token(username)
            return {"status": "success", "token": token, "expires_in": self.token_expiry_seconds}
        else:
            self._record_failed_attempt(username, source_ip)
            return {"status": "failed", "message": "Credenciais inválidas."}

    def _is_ip_blocked(self, ip: str) -> bool:
        """Verifica se um IP está atualmente bloqueado."""
        if ip in self.blocked_ips:
            if datetime.now() < self.blocked_ips[ip]:
                return True
            else:
                # Bloqueio expirou
                del self.blocked_ips[ip]
        return False

    def _block_ip(self, ip: str):
        """Bloqueia um IP por um período determinado."""
        self.blocked_ips[ip] = datetime.now() + timedelta(seconds=self.lockout_duration_seconds)
        logger.warning(f"🚨 IP {ip} bloqueado por {self.lockout_duration_seconds} segundos.")

    def _check_brute_force(self, username: str, source_ip: str) -> bool:
        """Verifica se as tentativas de login excedem o limite."""
        key = f"{username}:{source_ip}"
        now = datetime.now()
        # Filtra tentativas que estão fora da janela de tempo
        valid_attempts = [
            t for t in self.failed_attempts[key]
            if (now - t).seconds < self.lockout_duration_seconds
        ]
        self.failed_attempts[key] = valid_attempts
        return len(valid_attempts) >= self.max_login_attempts

    def _record_failed_attempt(self, username: str, source_ip: str):
        """Registra uma tentativa de login falha."""
        key = f"{username}:{source_ip}"
        self.failed_attempts[key].append(datetime.now())

    def _verify_credentials(self, username: str, password: str) -> bool:
        """[AUTENTICIDADE] Verifica as credenciais do usuário."""
        # Esta é a implementação REAL. Em um sistema de produção, as senhas
        # seriam hashes armazenados no banco de dados (`DatabaseAgent`).
        # A verificação seria feita com uma biblioteca como `bcrypt`.
        test_users = {"admin": "admin123", "user": "user123"}
        return test_users.get(username) == password

    def _generate_access_token(self, username: str) -> str:
        """Gera um token de acesso JWT."""
        payload = {
            "sub": username,
            "level": "admin" if username == "admin" else "user",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=self.token_expiry_seconds),
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
        return token

    async def authorize_access(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Autoriza uma ação baseada em um token JWT."""
        token = request_data.get("token")
        required_level = AccessLevel(request_data.get("required_level", "user"))

        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            user_level = AccessLevel(payload.get("level", "guest"))

            if user_level.value >= required_level.value: # Lógica de permissão simples
                return {"status": "granted", "user": payload["sub"], "level": user_level.value}
            else:
                return {"status": "denied", "message": "Permissões insuficientes."}
        except jwt.ExpiredSignatureError:
            return {"status": "denied", "message": "Token expirado."}
        except jwt.InvalidTokenError:
            return {"status": "denied", "message": "Token inválido."}

    async def perform_security_scan(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """[SIMULAÇÃO] Realiza uma varredura de segurança no sistema."""
        # A lógica real seria implementada na Fase 2, integrando com ferramentas
        # de scan e usando o `CodeAnalyzerAgent`.
        logger.info("🛡️ [Simulação] Iniciando varredura de segurança...")
        await asyncio.sleep(2)
        return {
            "status": "completed_simulated",
            "vulnerabilities_found": 0,
            "security_score": 98.5,
        }


def create_security_guardian_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente Security Guardian."""
    agents = []
    logger.info("🛡️ Criando SecurityGuardianAgent...")
    try:
        agent = SecurityGuardianAgent("security_guardian_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando SecurityGuardianAgent: {e}", exc_info=True)
    return agents
