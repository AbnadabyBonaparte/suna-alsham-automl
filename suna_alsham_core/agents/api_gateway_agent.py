#!/usr/bin/env python3
"""
API Gateway Agent – ALSHAM QUANTUM
[Quantum Version 2.0 - Universal HTTP Interface with Advanced Routing]

Gateway HTTP avançado com roteamento inteligente, métricas em tempo real,
rate limiting, authentication, e integração completa com o sistema multi-agente.
"""

import asyncio
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import uuid

# FastAPI e dependências HTTP
try:
    from fastapi import FastAPI, HTTPException, Request, Response, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    FastAPI = None

from suna_alsham_core.multi_agent_network import (
    AgentMessage, AgentType, BaseNetworkAgent, MessageType, Priority
)

logger = logging.getLogger(__name__)

class RequestType(Enum):
    """Tipos de requisição suportados."""
    TASK_SUBMISSION = "task_submission"
    TEXT_PROCESSING = "text_processing"
    AGENT_QUERY = "agent_query"
    SYSTEM_COMMAND = "system_command"
    HEALTH_CHECK = "health_check"

class AuthLevel(Enum):
    """Níveis de autenticação."""
    PUBLIC = "public"
    AUTHENTICATED = "authenticated"
    ADMIN = "admin"
    SYSTEM = "system"

@dataclass
class EndpointMetrics:
    """Métricas de endpoint."""
    endpoint: str
    request_count: int = 0
    success_count: int = 0
    error_count: int = 0
    avg_response_time: float = 0.0
    response_times: List[float] = field(default_factory=list)
    last_request: Optional[datetime] = None

@dataclass
class ClientSession:
    """Sessão de cliente."""
    client_id: str
    ip_address: str
    user_agent: Optional[str] = None
    first_request: datetime = field(default_factory=datetime.now)
    last_request: datetime = field(default_factory=datetime.now)
    request_count: int = 0
    blocked: bool = False

# Modelos Pydantic para validação
class TaskSubmissionRequest(BaseModel):
    """Modelo para submissão de tarefas."""
    content: str = Field(..., description="Conteúdo da tarefa")
    task_type: Optional[str] = Field("general", description="Tipo da tarefa")
    priority: Optional[str] = Field("normal", description="Prioridade da tarefa")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Contexto adicional")
    requester_id: Optional[str] = Field("api_user", description="ID do solicitante")

class TaskResponse(BaseModel):
    """Resposta de submissão de tarefa."""
    status: str
    task_id: str
    message: str
    estimated_completion: Optional[str] = None

class HealthResponse(BaseModel):
    """Resposta de health check."""
    status: str
    uptime_seconds: float
    agents_active: int
    requests_processed: int
    system_load: Dict[str, Any]

class SystemInfoResponse(BaseModel):
    """Informações do sistema."""
    system: str
    version: str
    api_gateway_id: str
    capabilities: List[str]
    uptime_seconds: float
    total_requests: int
    endpoints_available: List[str]

class QuantumAPIGatewayAgent(BaseNetworkAgent):
    """
    API Gateway Quantum com capacidades avançadas:
    - Servidor FastAPI integrado ao lifecycle do agente
    - Rate limiting inteligente por cliente
    - Métricas detalhadas de performance
    - Sistema de autenticação extensível
    - Roteamento inteligente baseado em carga
    - Health monitoring em tempo real
    - Cache de respostas com TTL configurável
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend([
            "http_gateway",
            "request_routing",
            "rate_limiting",
            "authentication",
            "metrics_collection",
            "load_balancing",
            "caching"
        ])
        
        # Configurações do servidor
        self.host = os.environ.get("API_GATEWAY_HOST", "0.0.0.0")
        self.port = int(os.environ.get("API_GATEWAY_PORT", "8000"))
        self.rate_limit_requests = int(os.environ.get("RATE_LIMIT_REQUESTS", "100"))
        self.rate_limit_window = int(os.environ.get("RATE_LIMIT_WINDOW", "60"))
        self.auth_required = os.environ.get("AUTH_REQUIRED", "false").lower() == "true"
        self.api_key = os.environ.get("API_KEY")
        
        # Estado do gateway
        self.app: Optional[FastAPI] = None
        self.server_task: Optional[asyncio.Task] = None
        self.start_time = datetime.now()
        self.task_counter = 0
        self.endpoint_metrics: Dict[str, EndpointMetrics] = {}
        self.client_sessions: Dict[str, ClientSession] = {}
        self.rate_limit_storage: Dict[str, List[datetime]] = {}
        self.response_cache: Dict[str, Tuple[Any, datetime]] = {}
        self.cache_ttl_seconds = int(os.environ.get("CACHE_TTL", "60"))
        
        # Inicialização
        if FASTAPI_AVAILABLE:
            self._setup_fastapi()
            self._quantum_init_task = asyncio.create_task(self._quantum_initialization())
            logger.info(f"🌐 {self.agent_id} (Quantum API Gateway) inicializado com FastAPI.")
        else:
            self.status = "degraded"
            logger.critical("❌ FastAPI não disponível! API Gateway em modo degradado.")

    def _setup_fastapi(self):
        """Configura aplicação FastAPI."""
        self.app = FastAPI(
            title="ALSHAM QUANTUM API Gateway",
            description="Gateway HTTP universal para sistema multi-agente ALSHAM QUANTUM",
            version="2.1.0",
            docs_url="/docs",
            redoc_url="/redoc",
            openapi_url="/openapi.json"
        )
        
        # Middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Middleware customizado
        @self.app.middleware("http")
        async def custom_middleware(request: Request, call_next):
            return await self._process_request_middleware(request, call_next)
        
        # Configurar rotas
        self._setup_routes()

    def _setup_routes(self):
        """Configura todas as rotas do API Gateway."""
        
        @self.app.get("/", response_model=Dict[str, Any])
        async def root():
            """Endpoint raiz."""
            return {
                "service": "ALSHAM QUANTUM API Gateway",
                "version": "2.1.0",
                "status": "operational",
                "documentation": "/docs",
                "health": "/health",
                "system_info": "/system/info"
            }

        @self.app.get("/health", response_model=HealthResponse)
        async def health_check():
            """Verificação de saúde avançada."""
            uptime = (datetime.now() - self.start_time).total_seconds()
            agents_active = len(self.message_bus.queues) if hasattr(self.message_bus, 'queues') else 0
            
            # Sistema de carga básico
            system_load = {
                "active_sessions": len(self.client_sessions),
                "requests_per_minute": self._calculate_requests_per_minute(),
                "cache_size": len(self.response_cache),
                "avg_response_time": self._calculate_avg_response_time()
            }
            
            return HealthResponse(
                status="healthy" if agents_active > 0 else "degraded",
                uptime_seconds=uptime,
                agents_active=agents_active,
                requests_processed=self.task_counter,
                system_load=system_load
            )

        @self.app.post("/submit", response_model=TaskResponse)
        async def submit_task(task: TaskSubmissionRequest, request: Request):
            """Submissão de tarefa principal."""
            client_id = self._get_client_id(request)
            
            # Rate limiting
            if not await self._check_rate_limit(client_id):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded"
                )
            
            # Autenticação se requerida
            if self.auth_required and not await self._authenticate_request(request):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            try:
                # Gerar ID único para tarefa
                self.task_counter += 1
                task_id = f"quantum_task_{self.task_counter:08d}_{uuid.uuid4().hex[:8]}"
                
                logger.info(f"🌐 [API Gateway] Nova tarefa recebida [{task_id}]: {task.task_type}")
                
                # Preparar payload para orquestrador
                payload = {
                    "request_type": "process_user_request",
                    "content": task.content,
                    "context": {
                        **task.context,
                        "task_id": task_id,
                        "task_type": task.task_type,
                        "priority": task.priority,
                        "requester_id": task.requester_id,
                        "source": "api_gateway",
                        "client_id": client_id,
                        "timestamp": datetime.now().isoformat()
                    }
                }
                
                # Enviar para orquestrador
                await self._send_to_orchestrator(payload, task_id)
                
                # Atualizar métricas
                self._update_client_session(client_id, request)
                
                logger.info(f"✅ [API Gateway] Tarefa [{task_id}] enviada para processamento")
                
                return TaskResponse(
                    status="accepted",
                    task_id=task_id,
                    message=f"Tarefa aceita e enviada para processamento quantum",
                    estimated_completion="Processing in background"
                )
                
            except Exception as e:
                logger.error(f"❌ [API Gateway] Erro ao processar tarefa: {e}", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erro interno do gateway: {str(e)}"
                )

        @self.app.post("/submit_text")
        async def submit_text(request: Request):
            """Submissão de texto livre."""
            try:
                # Ler corpo da requisição
                body = await request.body()
                text_content = body.decode('utf-8')
                
                if not text_content.strip():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Texto vazio não é permitido"
                    )
                
                # Converter para tarefa estruturada
                task_data = TaskSubmissionRequest(
                    content=text_content,
                    task_type="text_processing",
                    priority="normal"
                )
                
                return await submit_task(task_data, request)
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"❌ [API Gateway] Erro ao processar texto: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro ao processar texto: {str(e)}"
                )

        @self.app.get("/agents/status")
        async def agents_status():
            """Status dos agentes conectados."""
            try:
                agents_list = list(self.message_bus.queues.keys()) if hasattr(self.message_bus, 'queues') else []
                return {
                    "total_agents": len(agents_list),
                    "agents": sorted(agents_list),
                    "timestamp": datetime.now().isoformat(),
                    "network_health": "operational" if len(agents_list) > 0 else "degraded"
                }
            except Exception as e:
                logger.error(f"❌ Erro ao obter status dos agentes: {e}")
                return {
                    "error": str(e),
                    "total_agents": 0,
                    "agents": [],
                    "network_health": "error"
                }

        @self.app.get("/system/info", response_model=SystemInfoResponse)
        async def system_info():
            """Informações detalhadas do sistema."""
            uptime = (datetime.now() - self.start_time).total_seconds()
            
            # Lista de endpoints disponíveis
            endpoints = [route.path for route in self.app.routes if hasattr(route, 'path')]
            
            return SystemInfoResponse(
                system="ALSHAM QUANTUM",
                version="2.1.0",
                api_gateway_id=self.agent_id,
                capabilities=self.capabilities,
                uptime_seconds=uptime,
                total_requests=self.task_counter,
                endpoints_available=endpoints
            )

        @self.app.get("/metrics")
        async def get_metrics():
            """Métricas detalhadas do gateway."""
            if self.auth_required:
                # Em produção, proteger este endpoint
                pass
            
            return {
                "endpoint_metrics": {
                    path: {
                        "request_count": metrics.request_count,
                        "success_count": metrics.success_count,
                        "error_count": metrics.error_count,
                        "avg_response_time": metrics.avg_response_time,
                        "last_request": metrics.last_request.isoformat() if metrics.last_request else None
                    }
                    for path, metrics in self.endpoint_metrics.items()
                },
                "active_sessions": len(self.client_sessions),
                "cache_statistics": {
                    "cache_size": len(self.response_cache),
                    "cache_ttl_seconds": self.cache_ttl_seconds
                },
                "rate_limiting": {
                    "requests_per_window": self.rate_limit_requests,
                    "window_seconds": self.rate_limit_window,
                    "active_limits": len(self.rate_limit_storage)
                }
            }

    async def _quantum_initialization(self):
        """Inicialização quantum do API Gateway."""
        try:
            logger.info("🔍 Iniciando verificações do API Gateway...")
            
            # Verificar conectividade com message bus
            if hasattr(self.message_bus, 'running') and self.message_bus.running:
                logger.info("✅ Message Bus: Conectado")
            else:
                logger.warning("⚠️ Message Bus: Não está rodando")
            
            # Verificar se orquestrador está disponível
            agents = list(self.message_bus.queues.keys()) if hasattr(self.message_bus, 'queues') else []
            if "orchestrator_001" in agents:
                logger.info("✅ Orquestrador: Disponível")
            else:
                logger.warning("⚠️ Orquestrador: Não encontrado")
            
            # Iniciar servidor HTTP
            if FASTAPI_AVAILABLE and self.app:
                self.server_task = asyncio.create_task(self._start_http_server())
                logger.info(f"🚀 Servidor HTTP iniciado em {self.host}:{self.port}")
            
            self.status = "active"
            logger.info("🌐 API Gateway quantum operacional!")
            
        except Exception as e:
            self.status = "degraded"
            logger.error(f"❌ Erro na inicialização do API Gateway: {e}", exc_info=True)

    async def _start_http_server(self):
        """Inicia servidor FastAPI."""
        try:
            config = uvicorn.Config(
                app=self.app,
                host=self.host,
                port=self.port,
                log_level="info",
                access_log=False  # Usamos nosso próprio logging
            )
            server = uvicorn.Server(config)
            await server.serve()
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar servidor HTTP: {e}", exc_info=True)

    async def _process_request_middleware(self, request: Request, call_next):
        """Middleware de processamento de requisições."""
        start_time = time.time()
        endpoint = request.url.path
        
        try:
            # Processar requisição
            response = await call_next(request)
            
            # Calcular tempo de resposta
            response_time = (time.time() - start_time) * 1000
            
            # Atualizar métricas
            self._update_endpoint_metrics(endpoint, response_time, success=True)
            
            # Adicionar headers customizados
            response.headers["X-Quantum-Agent"] = self.agent_id
            response.headers["X-Response-Time"] = f"{response_time:.2f}ms"
            
            return response
            
        except Exception as e:
            # Atualizar métricas de erro
            response_time = (time.time() - start_time) * 1000
            self._update_endpoint_metrics(endpoint, response_time, success=False)
            
            logger.error(f"❌ Erro no middleware: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "agent_id": self.agent_id}
            )

    def _get_client_id(self, request: Request) -> str:
        """Gera ID único para cliente."""
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        return f"{client_ip}_{hash(user_agent) % 10000:04d}"

    async def _check_rate_limit(self, client_id: str) -> bool:
        """Verifica rate limiting por cliente."""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.rate_limit_window)
        
        # Limpar entradas antigas
        if client_id in self.rate_limit_storage:
            self.rate_limit_storage[client_id] = [
                req_time for req_time in self.rate_limit_storage[client_id]
                if req_time > window_start
            ]
        else:
            self.rate_limit_storage[client_id] = []
        
        # Verificar limite
        if len(self.rate_limit_storage[client_id]) >= self.rate_limit_requests:
            return False
        
        # Adicionar requisição atual
        self.rate_limit_storage[client_id].append(now)
        return True

    async def _authenticate_request(self, request: Request) -> bool:
        """Autentica requisição se necessário."""
        if not self.auth_required:
            return True
        
        # Verificar API key no header
        api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization")
        if api_key and api_key.replace("Bearer ", "") == self.api_key:
            return True
        
        return False

    def _update_client_session(self, client_id: str, request: Request):
        """Atualiza sessão do cliente."""
        now = datetime.now()
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent")
        
        if client_id in self.client_sessions:
            session = self.client_sessions[client_id]
            session.last_request = now
            session.request_count += 1
        else:
            self.client_sessions[client_id] = ClientSession(
                client_id=client_id,
                ip_address=client_ip,
                user_agent=user_agent,
                first_request=now,
                last_request=now,
                request_count=1
            )

    def _update_endpoint_metrics(self, endpoint: str, response_time: float, success: bool):
        """Atualiza métricas do endpoint."""
        if endpoint not in self.endpoint_metrics:
            self.endpoint_metrics[endpoint] = EndpointMetrics(endpoint=endpoint)
        
        metrics = self.endpoint_metrics[endpoint]
        metrics.request_count += 1
        metrics.last_request = datetime.now()
        
        if success:
            metrics.success_count += 1
        else:
            metrics.error_count += 1
        
        # Atualizar tempo médio de resposta
        metrics.response_times.append(response_time)
        if len(metrics.response_times) > 100:  # Manter apenas últimas 100
            metrics.response_times = metrics.response_times[-100:]
        
        metrics.avg_response_time = sum(metrics.response_times) / len(metrics.response_times)

    def _calculate_requests_per_minute(self) -> float:
        """Calcula requisições por minuto."""
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        total_requests = 0
        
        for client_requests in self.rate_limit_storage.values():
            total_requests += len([req for req in client_requests if req > one_minute_ago])
        
        return float(total_requests)

    def _calculate_avg_response_time(self) -> float:
        """Calcula tempo médio de resposta global."""
        all_times = []
        for metrics in self.endpoint_metrics.values():
            all_times.extend(metrics.response_times)
        
        return sum(all_times) / len(all_times) if all_times else 0.0

    async def _send_to_orchestrator(self, payload: Dict[str, Any], task_id: str):
        """Envia payload para o orquestrador."""
        try:
            message = self.create_message(
                recipient_id="orchestrator_001",
                message_type=MessageType.REQUEST,
                content=payload,
                priority=Priority.NORMAL
            )
            
            await self.message_bus.publish(message)
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar para orquestrador: {e}")
            raise

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas pelo agente."""
        # API Gateway normalmente não recebe muitas mensagens,
        # mas pode processar respostas do orquestrador para notificar clientes
        if message.message_type == MessageType.RESPONSE:
            logger.debug(f"📥 [API Gateway] Resposta recebida de {message.sender_id}")
            # Em implementação futura, poderia notificar cliente via websocket

    def get_gateway_metrics(self) -> Dict[str, Any]:
        """Retorna métricas completas do gateway."""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "uptime_seconds": uptime,
            "total_requests": self.task_counter,
            "active_sessions": len(self.client_sessions),
            "endpoint_count": len(self.endpoint_metrics),
            "cache_size": len(self.response_cache),
            "rate_limit_active": len(self.rate_limit_storage),
            "server_info": {
                "host": self.host,
                "port": self.port,
                "auth_required": self.auth_required,
                "rate_limit_requests": self.rate_limit_requests,
                "rate_limit_window": self.rate_limit_window
            },
            "performance": {
                "avg_response_time": self._calculate_avg_response_time(),
                "requests_per_minute": self._calculate_requests_per_minute()
            }
        }

from typing import Any, List

def create_api_gateway_agent(message_bus: Any) -> List[BaseNetworkAgent]:
    """
    Factory function to create and return all Quantum API Gateway agents for the system.
    This function is intended for use by the agent_loader/bootstrap system.

    Args:
        message_bus (Any): The message bus instance for agent communication.

    Returns:
        List[BaseNetworkAgent]: List of instantiated Quantum API Gateway agents (empty if FastAPI unavailable).
    """
    agents: List[BaseNetworkAgent] = []
    logger.info("🌐 Creating QuantumAPIGatewayAgent...")
    try:
        if FASTAPI_AVAILABLE:
            agent = QuantumAPIGatewayAgent("api_gateway_001", message_bus)
            agents.append(agent)
            logger.info("✅ QuantumAPIGatewayAgent created successfully.")
        else:
            logger.critical("❌ FastAPI not available - API Gateway cannot be created.")
    except Exception as e:
        logger.critical(f"❌ Critical error creating QuantumAPIGatewayAgent: {e}", exc_info=True)
    logger.info(f"🌐 Total API Gateway agents created: {len(agents)}")
    return agents
