#!/usr/bin/env python3
"""
Módulo do Agente Guardião de Segurança - SUNA-ALSHAM

[Fase 2] - Fortalecido com lógica real de validação de JWT,
verificação de permissões e um sistema de regras de segurança.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

# [AUTENTICIDADE] Bibliotecas de segurança são importadas de forma segura.
try:
    import jwt
    from jwt import PyJWTError
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

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
# Em um ambiente de produção real, esta chave deve vir de uma variável de ambiente.
JWT_SECRET_KEY = "suna-alsham-super-secret-key-2024-production"
JWT_ALGORITHM = "HS256"

# --- Dataclasses ---
@dataclass
class SecurityRule:
    """Define uma regra de segurança para uma ação específica."""
    action: str
    required_permissions: List[str]
    allow_all: bool = False

# --- Classe Principal do Agente ---
class SecurityGuardianAgent(BaseNetworkAgent):
    """
    Agente especialista em segurança. Atua como um firewall para a rede,
    validando a autenticidade e as permissões de todas as requisições
    críticas que entram no sistema.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SecurityGuardianAgent."""
        # O tipo deste agente é GUARD, que precisa ser definido no AgentType Enum
        super().__init__(agent_id, AgentType.GUARD, message_bus)
        self.capabilities.extend([
            "request_validation",
            "permission_enforcement",
            "jwt_authentication",
        ])
        
        if not JWT_AVAILABLE:
            self.status = "degraded"
            logger.critical("Biblioteca 'PyJWT' não encontrada. O SecurityGuardianAgent operará em modo degradado.")
        
        self.security_rules = self._load_security_rules()
        logger.info(f"🛡️ {self.agent_id} (Guardião de Segurança) inicializado com {len(self.security_rules)} regras.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de validação de segurança."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        if request_type == "validate_request":
            result = self.validate_request(message.content)
            await self.publish_response(message, result)

    def _load_security_rules(self) -> List[SecurityRule]:
        """Carrega as regras de segurança do sistema."""
        # Em um sistema real, isso viria de um arquivo de configuração.
        return [
            SecurityRule(action="execute_shell_command", required_permissions=["admin", "system_control"]),
            SecurityRule(action="deploy", required_permissions=["admin", "deployment"]),
            SecurityRule(action="create_backup", required_permissions=["admin", "backup"]),
            SecurityRule(action="get_status", allow_all=True),
        ]

    def validate_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Valida um JWT e verifica se as permissões
        contidas nele são suficientes para executar a ação solicitada.
        """
        if self.status == "degraded":
            return {"status": "error", "message": "Serviço de segurança indisponível."}

        token = request_data.get("auth_token")
        action = request_data.get("action")
        
        if not token or not action:
            return {"status": "denied", "reason": "Token de autenticação ou ação não fornecidos."}

        # 1. Validar o Token JWT
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_permissions = payload.get("permissions", [])
        except PyJWTError as e:
            logger.warning(f"Tentativa de autenticação falhou com token inválido: {e}")
            return {"status": "denied", "reason": f"Token inválido: {e}"}

        # 2. Encontrar a regra de segurança para a ação
        rule = next((r for r in self.security_rules if r.action == action), None)
        if not rule:
            return {"status": "denied", "reason": f"Ação '{action}' desconhecida ou não permitida."}

        # 3. Verificar Permissões
        if rule.allow_all:
            return {"status": "approved", "user": payload.get("sub")}

        if all(perm in user_permissions for perm in rule.required_permissions):
            logger.info(f"Ação '{action}' aprovada para o usuário '{payload.get('sub')}'")
            return {"status": "approved", "user": payload.get("sub")}
        else:
            logger.warning(f"Ação '{action}' negada para '{payload.get('sub')}'. Permissões insuficientes.")
            return {"status": "denied", "reason": "Permissões insuficientes."}

def create_security_guardian_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente Guardião de Segurança."""
    agents = []
    logger.info("🛡️ Criando SecurityGuardianAgent...")
    try:
        agent = SecurityGuardianAgent("security_guardian_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando SecurityGuardianAgent: {e}", exc_info=True)
    return agents
