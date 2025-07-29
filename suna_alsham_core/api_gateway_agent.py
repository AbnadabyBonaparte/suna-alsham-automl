#!/usr/bin/env python3
"""
Módulo do API Gateway Agent - O Gateway Inteligente para o SUNA-ALSHAM.

[Fase 2] - Fortalecido com lógica de rate limiting real e preparação para
autenticação robusta via SecurityGuardianAgent.
"""

import asyncio
import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from fastapi import Request
from fastapi.responses import JSONResponse

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class AuthLevel(Enum):
    """Níveis de autenticação para os endpoints."""
    PUBLIC = "public"
    AUTHENTICATED = "authenticated"
    ADMIN = "admin"


@dataclass
class APIEndpoint:
    """Configuração de um endpoint da API."""
    path: str
    methods: List[str]
    target_agent: str
    auth_level: AuthLevel


# --- Classe Principal do Agente ---

class APIGatewayAgent(BaseNetworkAgent):
    """
    Agente de Gateway API Inteligente. Serve como o ponto de entrada seguro e
    controlado para todas as interações externas com o sistema SUNA-ALSHAM.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o APIGatewayAgent."""
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend([
            "api_management",
            "rate_limiting",
            "authentication",
            "request_routing",
        ])
        
        self.endpoints: Dict[str, APIEndpoint] = {}
        self._setup_default_endpoints()
        
        # [LÓGICA REAL] Sistema de Rate Limiting
        self.rate_limit_cache = defaultdict(deque)
        self.rate_limit_rules = {
            "public": {"requests": 100, "window": 60},  # 100 req/minuto
            "authenticated": {"requests": 1000, "window": 60}, # 1000 req/minuto
        }
        
        logger.info(f"🌐 {self.agent_id} (API Gateway) inicializado.")

    def _setup_default_endpoints(self):
        """Configura os endpoints padrão do sistema."""
        default_endpoints = [
            APIEndpoint("/api/status", ["GET"], "performance_monitor_001", AuthLevel.PUBLIC),
            APIEndpoint("/api/tasks", ["POST"], "orchestrator_001", AuthLevel.AUTHENTICATED),
        ]
        for endpoint in default_endpoints:
            self.endpoints[endpoint.path] = endpoint
        logger.info(f"  -> {len(default_endpoints)} endpoints padrão configurados.")

    async def handle_api_request(self, path: str, request: Request) -> JSONResponse:
        """
        [LÓGICA REAL] Processa uma requisição HTTP recebida pelo servidor principal.
        Este método é chamado pelo `start.py` (ou um router FastAPI).
        """
        endpoint = self.endpoints.get(path)
        if not endpoint or request.method not in endpoint.methods:
            return JSONResponse(status_code=404, content={"error": "Endpoint não encontrado."})

        client_ip = request.client.host or "unknown"

        # 1. Rate Limiting Real
        auth_level = await self._authenticate_request(request, endpoint)
        if not auth_level:
             return JSONResponse(status_code=401, content={"error": "Autenticação falhou."})

        limit_type = auth_level.value
        if not self._is_rate_limit_allowed(client_ip, limit_type):
            return JSONResponse(status_code=429, content={"error": "Rate limit excedido."})

        # 2. Roteamento para o agente de destino
        return await self._proxy_request_to_agent(endpoint, request)

    async def _authenticate_request(self, request: Request, endpoint: APIEndpoint) -> Optional[AuthLevel]:
        """
        [AUTENTICIDADE] Autentica a requisição. Na Fase 3, esta função irá chamar
        o `SecurityGuardianAgent` para validar tokens JWT de forma robusta.
        """
        if endpoint.auth_level == AuthLevel.PUBLIC:
            return AuthLevel.PUBLIC

        # Simulação de validação de token
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            # A lógica real de validação do token com o SecurityGuardian viria aqui.
            logger.info("[Simulação] Token de autenticação validado com sucesso.")
            return AuthLevel.AUTHENTICATED # Assume que qualquer token é válido por enquanto
        
        logger.warning("Tentativa de acesso a endpoint protegido sem autenticação.")
        return None

    def _is_rate_limit_allowed(self, identifier: str, limit_type: str) -> bool:
        """[LÓGICA REAL] Verifica se uma requisição está dentro do limite de taxa."""
        rule = self.rate_limit_rules.get(limit_type)
        if not rule: return True # Sem regra, sem limite

        current_time = time.time()
        window_start = current_time - rule["window"]

        requests = self.rate_limit_cache[identifier]
        while requests and requests[0] < window_start:
            requests.popleft()
        
        if len(requests) >= rule["requests"]:
            return False
        
        requests.append(current_time)
        return True

    async def _proxy_request_to_agent(self, endpoint: APIEndpoint, request: Request) -> JSONResponse:
        """
        Cria uma mensagem, envia para o agente de destino e aguarda a resposta.
        """
        logger.info(f"  -> Roteando requisição de '{endpoint.path}' para o agente '{endpoint.target_agent}'.")
        
        try:
            body = await request.json() if request.method in ["POST", "PUT"] else None
            
            internal_message_content = {
                "request_type": "api_request",
                "path": endpoint.path,
                "method": request.method,
                "body": body,
            }
            
            response_message = await self.send_request_and_wait(
                recipient_id=endpoint.target_agent,
                content=internal_message_content,
                timeout=30
            )

            response_content = response_message.content.get("result", {})
            return JSONResponse(status_code=200, content=response_content)

        except TimeoutError:
            return JSONResponse(status_code=504, content={"error": "Gateway Timeout"})
        except Exception as e:
            logger.error(f"Erro no proxy para {endpoint.target_agent}: {e}", exc_info=True)
            return JSONResponse(status_code=502, content={"error": "Bad Gateway"})


def create_api_gateway_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente API Gateway."""
    agents = []
    logger.info("🌐 Criando APIGatewayAgent...")
    try:
        agent = APIGatewayAgent("api_gateway_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando APIGatewayAgent: {e}", exc_info=True)
    return agents
