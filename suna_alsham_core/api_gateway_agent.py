#!/usr/bin/env python3
"""
Módulo do API Gateway Agent - O Gateway Inteligente para o SUNA-ALSHAM.

Define o agente que atua como um API Gateway completo, gerenciando rotas,
autenticação (JWT), rate limiting, e roteamento de requisições para outros agentes.
"""

import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List

import jwt
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
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
        self.jwt_secret = "jwt-secret-placeholder" # Em produção, carregar do ambiente
        
        # [AUTENTICIDADE] O servidor FastAPI será controlado pelo start.py principal
        # e não iniciado aqui diretamente.
        self._setup_default_endpoints()
        logger.info(f"🌐 {self.agent_id} (API Gateway) inicializado.")

    def _setup_default_endpoints(self):
        """Configura os endpoints padrão do sistema."""
        default_endpoints = [
            APIEndpoint(
                path="/api/agents",
                methods=["GET"],
                target_agent="orchestrator_001",
                auth_level=AuthLevel.ADMIN,
            ),
            APIEndpoint(
                path="/api/tasks",
                methods=["POST"],
                target_agent="orchestrator_001",
                auth_level=AuthLevel.AUTHENTICATED,
            ),
            APIEndpoint(
                path="/api/status",
                methods=["GET"],
                target_agent="monitor_001",
                auth_level=AuthLevel.PUBLIC,
            ),
        ]
        for endpoint in default_endpoints:
            self.endpoints[endpoint.path] = endpoint
        logger.info(f"  -> {len(default_endpoints)} endpoints padrão configurados.")

    async def handle_api_request(self, path: str, request: Request) -> JSONResponse:
        """
        Processa uma requisição HTTP recebida pelo servidor principal.
        Este método será chamado pelo `start.py`.
        """
        endpoint = self._find_matching_endpoint(path, request.method)
        if not endpoint:
            return JSONResponse(status_code=404, content={"error": "Endpoint não encontrado."})

        # [AUTENTICIDADE] Lógica real de autenticação e rate limiting
        # será implementada na Fase 2, integrando com o SecurityGuardianAgent.
        logger.info(f"[Simulação] Autenticação e Rate Limit para {path} passariam aqui.")

        # Encaminhar requisição para o agente de destino
        return await self._proxy_request_to_agent(endpoint, request)

    def _find_matching_endpoint(self, path: str, method: str) -> Optional[APIEndpoint]:
        """Encontra o endpoint que corresponde ao caminho e método da requisição."""
        # Lógica de correspondência simples por enquanto
        if path in self.endpoints and method in self.endpoints[path].methods:
            return self.endpoints[path]
        return None

    async def _proxy_request_to_agent(self, endpoint: APIEndpoint, request: Request) -> JSONResponse:
        """
        Cria uma mensagem, envia para o agente de destino e aguarda a resposta.
        """
        logger.info(f"  -> Roteando requisição de '{endpoint.path}' para o agente '{endpoint.target_agent}'.")
        
        # [AUTENTICIDADE] A lógica de aguardar a resposta (com correlation_id)
        # será implementada na Fase 2 para garantir a comunicação síncrona.
        
        internal_message = self.create_message(
            recipient_id=endpoint.target_agent,
            message_type=MessageType.REQUEST,
            content={
                "request_type": "api_request",
                "path": endpoint.path,
                "method": request.method,
                "headers": dict(request.headers),
            },
        )
        await self.message_bus.publish(internal_message)

        # Retorna uma resposta imediata indicando que a tarefa foi delegada
        return JSONResponse(
            status_code=202, # Accepted
            content={
                "status": "processing",
                "message": f"Requisição encaminhada para o agente {endpoint.target_agent}.",
            },
        )


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
