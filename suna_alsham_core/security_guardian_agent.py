#!/usr/bin/env python3
"""
Módulo do Security Guardian Agent - Proteção Suprema do SUNA-ALSHAM.

[Fase 2] - Fortalecido com lógica real de JWT, proteção contra força bruta
e regras de segurança aprimoradas.
"""

import asyncio
import logging
import os
import secrets
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

# [AUTENTICIDADE] As bibliotecas de segurança são importadas de forma segura.
try:
    import jwt
    from passlib.context import CryptContext
    SECURITY_LIBS_AVAILABLE = True
except ImportError:
    SECURITY_LIBS_AVAILABLE = False

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
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AccessLevel(Enum):
    """Níveis de Acesso ao Sistema."""
    GUEST = 0
    USER = 1
    ADMIN = 2
    SYSTEM = 3


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
            "access_control",
            "security_audit",
        ])

        if not SECURITY_LIBS_AVAILABLE:
            self.status = "degraded"
            logger.critical("Bibliotecas 'jwt' ou 'passlib' não encontradas. O SecurityGuardianAgent operará em modo degradado.")
        
        # --- Configurações de segurança ---
        self.jwt_secret = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
        self.jwt_algorithm = "HS256"
        self.token_expiry_minutes = int(os.getenv("TOKEN_EXPIRY_MINUTES", 60))
        self.max_login_attempts = 5
        self.lockout_duration_seconds = 300  # 5 minutos
        
        if self.status != "degraded":
            self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        # --- Estado de segurança ---
        self.blocked_ips: Dict[str, datetime] = {}
        self.failed_attempts = defaultdict(deque)
        
        logger.info(f"🛡️ {self.agent_id} (Guardião de Segurança) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de segurança."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        handler = {
            "authenticate": self.authenticate_user,
            "authorize": self.authorize_access,
        }.get(request_type)

        if handler:
            result = await handler(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            logger.warning(f"Ação de segurança desconhecida: {request_type}")
            await self.message_bus.publish(self.create_error_response(message, "Ação de segurança desconhecida"))

    async def authenticate_user(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """[LÓGICA REAL] Autentica um usuário e retorna um token JWT."""
        username = request_data.get("username")
        password = request_data.get("password")
        source_ip = request_data.get("source_ip", "unknown")

        if self.status == "degraded":
            return {"status": "error", "message": "Serviço de segurança indisponível (dependências faltando)."}

        # 1. Verificação de Bloqueio de IP e Força Bruta
        if self._is_ip_blocked(source_ip) or self._check_brute_force(username, source_ip):
            self._block_ip(source_ip)
            return {"status": "blocked", "message": "Muitas tentativas de login falharam. IP bloqueado temporariamente."}
        
        # 2. Verificação de Credenciais
        user_data = self._verify_credentials(username, password)
        if user_data:
            token = self._generate_access_token(user_data)
            return {"status": "success", "token": token, "expires_in": self.token_expiry_minutes * 60}
        else:
            self._record_failed_attempt(username, source_ip)
            return {"status": "failed", "message": "Credenciais inválidas."}

    def _is_ip_blocked(self, ip: str) -> bool:
        """Verifica se um IP está atualmente bloqueado."""
        if ip in self.blocked_ips:
            if datetime.now(timezone.utc) < self.blocked_ips[ip]:
                return True
            else: # Bloqueio expirou
                del self.blocked_ips[ip]
        return False

    def _block_ip(self, ip: str):
        """Bloqueia um IP por um período determinado."""
        self.blocked_ips[ip] = datetime.now(timezone.utc) + timedelta(seconds=self.lockout_duration_seconds)
        logger.warning(f"🚨 IP {ip} bloqueado por {self.lockout_duration_seconds} segundos devido a atividade suspeita.")

    def _check_brute_force(self, username: str, source_ip: str) -> bool:
        """Verifica se as tentativas de login excedem o limite."""
        key = f"{username}:{source_ip}"
        now = datetime.now(timezone.utc)
        
        # Limpa timestamps antigos da janela de observação
        while self.failed_attempts[key] and self.failed_attempts[key][0] < (now - timedelta(seconds=self.lockout_duration_seconds)):
            self.failed_attempts[key].popleft()
        
        return len(self.failed_attempts[key]) >= self.max_login_attempts

    def _record_failed_attempt(self, username: str, source_ip: str):
        """Registra uma tentativa de login falha."""
        key = f"{username}:{source_ip}"
        self.failed_attempts[key].append(datetime.now(timezone.utc))

    def _verify_credentials(self, username: str, password: str) -> Optional[Dict]:
        """[AUTENTICIDADE] Verifica as credenciais do usuário."""
        # Na Fase 3, esta lógica será integrada com o DatabaseAgent para buscar
        # usuários e hashes de senha reais.
        test_users = {
            "admin": {"password_hash": self.pwd_context.hash("admin123"), "level": AccessLevel.ADMIN, "permissions": ["*"]},
            "user": {"password_hash": self.pwd_context.hash("user123"), "level": AccessLevel.USER, "permissions": ["read", "write"]},
        }
        user = test_users.get(username)
        if user and self.pwd_context.verify(password, user["password_hash"]):
            return {"user_id": username, "level": user["level"], "permissions": user["permissions"]}
        return None

    def _generate_access_token(self, user_data: Dict) -> str:
        """[LÓGICA REAL] Gera um token de acesso JWT."""
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.token_expiry_minutes)
        payload = {
            "sub": user_data["user_id"],
            "level": user_data["level"].value,
            "permissions": user_data["permissions"],
            "iat": datetime.now(timezone.utc),
            "exp": expire,
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return token

    async def authorize_access(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """[LÓGICA REAL] Autoriza uma ação baseada em um token JWT."""
        token = request_data.get("token")
        required_level = AccessLevel(request_data.get("required_level", 1)) # Default USER

        if self.status == "degraded":
            return {"status": "error", "message": "Serviço de autorização indisponível."}

        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            user_level = AccessLevel(payload.get("level", AccessLevel.GUEST.value))

            if user_level.value >= required_level.value:
                return {"status": "granted", "user": payload["sub"], "level": user_level.name}
            else:
                return {"status": "denied", "message": "Permissões insuficientes."}
        except jwt.ExpiredSignatureError:
            return {"status": "denied", "message": "Token expirado."}
        except jwt.InvalidTokenError:
            return {"status": "denied", "message": "Token inválido."}
        except Exception as e:
            logger.error(f"Erro inesperado na autorização: {e}", exc_info=True)
            return {"status": "error", "message": "Erro interno de autorização."}


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
