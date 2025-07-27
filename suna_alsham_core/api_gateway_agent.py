#!/usr/bin/env python3
"""
Módulo do API Gateway Agent - O Gateway Inteligente para o SUNA-ALSHAM.

Define o agente que atua como um API Gateway completo, gerenciando rotas,
autenticação (JWT), rate limiting, e roteamento de requisições para outros agentes.
"""

import asyncio
import logging
import time
import hashlib
import jwt
import json
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
from fastapi import FastAPI, Request, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from contextlib import asynccontextmanager
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class AuthLevel(Enum):
    """Níveis de autenticação."""
    PUBLIC = "public"
    AUTHENTICATED = "authenticated"
    PREMIUM = "premium"
    ADMIN = "admin"
    SYSTEM = "system"

class RateLimitType(Enum):
    """Tipos de rate limiting."""
    PER_SECOND = "per_second"
    PER_MINUTE = "per_minute"
    PER_HOUR = "per_hour"
    PER_DAY = "per_day"
    CONCURRENT = "concurrent"

class APIStatus(Enum):
    """Status das APIs."""
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"
    DISABLED = "disabled"

@dataclass
class RateLimit:
    """Configuração de rate limiting."""
    limit_type: RateLimitType
    max_requests: int
    window_seconds: int
    burst_allowance: int = 0
    cooldown_seconds: int = 60

@dataclass
class APIEndpoint:
    """Configuração de endpoint da API."""
    path: str
    methods: List[str]
    target_service: str
    auth_level: AuthLevel
    rate_limits: List[RateLimit]
    status: APIStatus = APIStatus.ACTIVE
    description: str = ""
    version: str = "v1"
    timeout_seconds: int = 30
    retry_attempts: int = 3
    cache_ttl: int = 0  # 0 = sem cache
    tags: List[str] = field(default_factory=list)

@dataclass
class ClientInfo:
    """Informações do cliente."""
    client_id: str
    api_key: str
    auth_level: AuthLevel
    rate_limits: Dict[str, int]
    created_at: datetime
    last_seen: datetime
    total_requests: int = 0
    failed_requests: int = 0
    banned_until: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RequestLog:
    """Log de requisição."""
    request_id: str
    client_id: str
    endpoint: str
    method: str
    status_code: int
    response_time_ms: float
    timestamp: datetime
    user_agent: str = ""
    ip_address: str = ""
    error_message: str = ""

# --- Classe Principal do Agente ---

class APIGatewayAgent(BaseNetworkAgent):
    """
    Agente de Gateway API Inteligente. Serve como o ponto de entrada seguro e
    controlado para todas as interações externas com o sistema SUNA-ALSHAM.
    """

    def __init__(self, agent_id: str, agent_type: str, message_bus):
        """Inicializa o APIGatewayAgent."""
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'api_management',
            'rate_limiting',
            'authentication',
            'authorization',
            'request_routing',
            'load_balancing',
            'caching',
            'monitoring',
            'security',
            'analytics'
        ]
        self.status = 'active'
        
        # Estado do gateway
        self.endpoints = {}  # path -> APIEndpoint
        self.clients = {}  # client_id -> ClientInfo
        self.rate_limit_cache = defaultdict(lambda: defaultdict(deque))
        self.request_logs = deque(maxlen=10000)
        self.active_connections = {}
        
        # Cache Redis (opcional)
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            self.redis_available = True
            logger.info("✅ Redis conectado para cache distribuído")
        except:
            self.redis_client = None
            self.redis_available = False
            logger.warning("⚠️ Redis não disponível - usando cache local")
        
        # Configurações
        self.default_rate_limits = {
            AuthLevel.PUBLIC: [
                RateLimit(RateLimitType.PER_MINUTE, 60, 60),
                RateLimit(RateLimitType.PER_HOUR, 1000, 3600)
            ],
            AuthLevel.AUTHENTICATED: [
                RateLimit(RateLimitType.PER_MINUTE, 300, 60),
                RateLimit(RateLimitType.PER_HOUR, 10000, 3600)
            ],
            AuthLevel.PREMIUM: [
                RateLimit(RateLimitType.PER_MINUTE, 1000, 60),
                RateLimit(RateLimitType.PER_HOUR, 50000, 3600)
            ],
            AuthLevel.ADMIN: [
                RateLimit(RateLimitType.PER_MINUTE, 5000, 60)
            ],
            AuthLevel.SYSTEM: []  # Sem limites para sistema
        }
        
        # Segurança
        self.jwt_secret = "suna_alsham_secret_key_2025"  # Em produção, usar variável de ambiente
        self.security_rules = self._load_security_rules()
        self.blocked_ips = set()
        self.suspicious_patterns = self._load_suspicious_patterns()
        
        # Métricas
        self.gateway_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'blocked_requests': 0,
            'average_response_time': 0.0,
            'active_clients': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        # FastAPI instance
        self.app = self._create_fastapi_app()
        
        # Tasks de background
        self._cleanup_task = None
        self._analytics_task = None
        self._security_task = None
        
        # Inicializar endpoints padrão
        self._setup_default_endpoints()
        
        logger.info(f"🌐 {self.agent_id} inicializado como API Gateway Inteligente")
    
    def _create_fastapi_app(self) -> FastAPI:
        """Cria aplicação FastAPI para o gateway."""
        app = FastAPI(
            title="SUNA-ALSHAM API Gateway",
            description="Gateway Inteligente para Sistema Multi-Agente",
            version="2.0.0",
            docs_url="/gateway/docs",
            redoc_url="/gateway/redoc"
        )
        
        # Middleware CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Middleware customizado
        app.middleware("http")(self._gateway_middleware)
        
        # Rotas do gateway
        self._setup_gateway_routes(app)
        
        return app
    
    async def _gateway_middleware(self, request: Request, call_next):
        """Middleware principal do gateway."""
        start_time = time.time()
        request_id = self._generate_request_id()
        
        # Adicionar request ID no header
        request.state.request_id = request_id
        
        try:
            # Verificar IP bloqueado
            client_ip = self._get_client_ip(request)
            if client_ip in self.blocked_ips:
                return JSONResponse(
                    status_code=403,
                    content={"error": "IP blocked", "request_id": request_id}
                )
            
            # Detectar padrões suspeitos
            if await self._detect_suspicious_activity(request):
                return JSONResponse(
                    status_code=429,
                    content={"error": "Suspicious activity detected", "request_id": request_id}
                )
            
            # Processar requisição
            response = await call_next(request)
            
            # Calcular tempo de resposta
            response_time = (time.time() - start_time) * 1000
            
            # Log da requisição
            await self._log_request(request, response, response_time, request_id)
            
            # Adicionar headers de resposta
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Gateway-Agent"] = self.agent_id
            response.headers["X-Response-Time"] = f"{response_time:.2f}ms"
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro no middleware: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal gateway error", "request_id": request_id}
            )
    
    def _setup_gateway_routes(self, app: FastAPI):
        """Configura rotas do gateway."""
        
        @app.get("/gateway/health")
        async def health_check():
            """Health check do gateway."""
            return {
                "status": "healthy",
                "agent_id": self.agent_id,
                "uptime": time.time(),
                "active_endpoints": len(self.endpoints),
                "active_clients": len(self.clients),
                "metrics": self.gateway_metrics
            }
        
        @app.get("/gateway/metrics")
        async def get_metrics():
            """Métricas detalhadas do gateway."""
            return await self._get_detailed_metrics()
        
        @app.post("/gateway/auth/token")
        async def generate_token(credentials: Dict[str, str]):
            """Gera token JWT para autenticação."""
            return await self._generate_auth_token(credentials)
        
        @app.get("/gateway/endpoints")
        async def list_endpoints():
            """Lista todos os endpoints disponíveis."""
            return await self._list_endpoints()
        
        @app.post("/gateway/endpoints")
        async def register_endpoint(endpoint_data: Dict[str, Any]):
            """Registra novo endpoint."""
            return await self._register_endpoint(endpoint_data)
        
        # Rota catch-all para proxy
        @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
        async def proxy_request(request: Request, path: str):
            """Proxy principal para todas as requisições."""
            return await self._handle_proxy_request(request, path)
    
    def _setup_default_endpoints(self):
        """Configura endpoints padrão do sistema."""
        default_endpoints = [
            APIEndpoint(
                path="/api/agents",
                methods=["GET", "POST"],
                target_service="orchestrator_001",
                auth_level=AuthLevel.AUTHENTICATED,
                rate_limits=self.default_rate_limits[AuthLevel.AUTHENTICATED],
                description="Gerenciamento de agentes",
                tags=["agents", "management"]
            ),
            APIEndpoint(
                path="/api/tasks",
                methods=["GET", "POST", "PUT"],
                target_service="orchestrator_001",
                auth_level=AuthLevel.AUTHENTICATED,
                rate_limits=self.default_rate_limits[AuthLevel.AUTHENTICATED],
                description="Gerenciamento de tarefas",
                tags=["tasks", "orchestration"]
            ),
            APIEndpoint(
                path="/api/analysis",
                methods=["POST"],
                target_service="code_analyzer_001",
                auth_level=AuthLevel.PREMIUM,
                rate_limits=self.default_rate_limits[AuthLevel.PREMIUM],
                description="Análise de código",
                timeout_seconds=60,
                tags=["analysis", "code"]
            ),
            APIEndpoint(
                path="/api/performance",
                methods=["GET", "POST"],
                target_service="performance_monitor_001",
                auth_level=AuthLevel.AUTHENTICATED,
                rate_limits=self.default_rate_limits[AuthLevel.AUTHENTICATED],
                description="Monitoramento de performance",
                cache_ttl=30,
                tags=["performance", "monitoring"]
            ),
            APIEndpoint(
                path="/api/public/status",
                methods=["GET"],
                target_service="internal",
                auth_level=AuthLevel.PUBLIC,
                rate_limits=self.default_rate_limits[AuthLevel.PUBLIC],
                description="Status público do sistema",
                cache_ttl=60,
                tags=["public", "status"]
            )
        ]
        
        for endpoint in default_endpoints:
            self.endpoints[endpoint.path] = endpoint
        
        logger.info(f"✅ {len(default_endpoints)} endpoints padrão configurados")
    
    async def start_gateway_service(self):
        """Inicia serviços do gateway."""
        if not self._cleanup_task:
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
            self._analytics_task = asyncio.create_task(self._analytics_loop())
            self._security_task = asyncio.create_task(self._security_loop())
            logger.info(f"🌐 {self.agent_id} iniciou serviços do gateway")
    
    async def stop_gateway_service(self):
        """Para serviços do gateway."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None
        if self._analytics_task:
            self._analytics_task.cancel()
            self._analytics_task = None
        if self._security_task:
            self._security_task.cancel()
            self._security_task = None
        logger.info(f"🛑 {self.agent_id} parou serviços do gateway")
    
    async def _cleanup_loop(self):
        """Loop de limpeza de dados antigos."""
        while True:
            try:
                # Limpar rate limits expirados
                await self._cleanup_rate_limits()
                
                # Limpar logs antigos
                await self._cleanup_old_logs()
                
                # Limpar clientes inativos
                await self._cleanup_inactive_clients()
                
                await asyncio.sleep(300)  # Limpeza a cada 5 minutos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na limpeza: {e}")
    
    async def _analytics_loop(self):
        """Loop de análise de métricas."""
        while True:
            try:
                # Calcular métricas
                await self._calculate_metrics()
                
                # Detectar anomalias
                anomalies = await self._detect_anomalies()
                if anomalies:
                    await self._handle_anomalies(anomalies)
                
                # Gerar relatórios
                if len(self.request_logs) > 1000:
                    await self._generate_analytics_report()
                
                await asyncio.sleep(60)  # Análise a cada minuto
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na análise: {e}")
    
    async def _security_loop(self):
        """Loop de monitoramento de segurança."""
        while True:
            try:
                # Verificar padrões de ataque
                await self._check_attack_patterns()
                
                # Atualizar regras de segurança
                await self._update_security_rules()
                
                # Limpar IPs bloqueados expirados
                await self._cleanup_blocked_ips()
                
                await asyncio.sleep(30)  # Verificação a cada 30 segundos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento de segurança: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas."""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'register_endpoint':
                result = await self._register_endpoint(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'create_client':
                result = await self._create_client(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'update_rate_limits':
                result = await self._update_rate_limits(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'get_analytics':
                result = await self._get_analytics_report(message.content)
                await self._send_response(message, result)
    
    async def _handle_proxy_request(self, request: Request, path: str) -> JSONResponse:
        """Processa requisição de proxy."""
        try:
            # Encontrar endpoint correspondente
            endpoint = self._find_matching_endpoint(path, request.method)
            if not endpoint:
                return JSONResponse(
                    status_code=404,
                    content={"error": "Endpoint not found", "path": path}
                )
            
            # Verificar status do endpoint
            if endpoint.status != APIStatus.ACTIVE:
                return JSONResponse(
                    status_code=503,
                    content={"error": f"Endpoint {endpoint.status.value}", "path": path}
                )
            
            # Autenticação
            client = await self._authenticate_request(request, endpoint)
            if not client:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Authentication required"}
                )
            
            # Rate limiting
            if not await self._check_rate_limits(client, endpoint):
                return JSONResponse(
                    status_code=429,
                    content={"error": "Rate limit exceeded"}
                )
            
            # Verificar cache
            cache_key = f"{path}:{request.method}:{hash(str(request.query_params))}"
            cached_response = await self._get_cached_response(cache_key)
            if cached_response:
                self.gateway_metrics['cache_hits'] += 1
                return JSONResponse(content=cached_response)
            
            self.gateway_metrics['cache_misses'] += 1
            
            # Fazer proxy da requisição
            response = await self._proxy_to_service(request, endpoint, path)
            
            # Cache da resposta
            if endpoint.cache_ttl > 0 and response.status_code == 200:
                await self._cache_response(cache_key, response.content, endpoint.cache_ttl)
            
            # Atualizar métricas do cliente
            client.total_requests += 1
            client.last_seen = datetime.now()
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro no proxy: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal gateway error"}
            )
    
    def _find_matching_endpoint(self, path: str, method: str) -> Optional[APIEndpoint]:
        """Encontra endpoint correspondente ao path."""
        # Busca exata primeiro
        if path in self.endpoints and method in self.endpoints[path].methods:
            return self.endpoints[path]
        
        # Busca por padrão (wildcards, parâmetros)
        for endpoint_path, endpoint in self.endpoints.items():
            if self._path_matches(path, endpoint_path) and method in endpoint.methods:
                return endpoint
        
        return None
    
    def _path_matches(self, request_path: str, endpoint_path: str) -> bool:
        """Verifica se o path da requisição corresponde ao endpoint."""
        # Suporte a wildcards e parâmetros
        if "*" in endpoint_path:
            pattern = endpoint_path.replace("*", ".*")
            import re
            return bool(re.match(pattern, request_path))
        
        if "{" in endpoint_path:
            # Suporte a parâmetros como /api/users/{user_id}
            pattern = endpoint_path
            import re
            pattern = re.sub(r'\{[^}]+\}', '[^/]+', pattern)
            return bool(re.match(f"^{pattern}$", request_path))
        
        return request_path == endpoint_path
    
    async def _authenticate_request(self, request: Request, endpoint: APIEndpoint) -> Optional[ClientInfo]:
        """Autentica requisição."""
        if endpoint.auth_level == AuthLevel.PUBLIC:
            # Criar cliente temporário para requisições públicas
            return ClientInfo(
                client_id="public",
                api_key="",
                auth_level=AuthLevel.PUBLIC,
                rate_limits={},
                created_at=datetime.now(),
                last_seen=datetime.now()
            )
        
        # Verificar API Key no header
        api_key = request.headers.get("X-API-Key")
        if api_key:
            client = self._find_client_by_api_key(api_key)
            if client and client.auth_level.value >= endpoint.auth_level.value:
                return client
        
        # Verificar JWT Token
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            client = await self._validate_jwt_token(token)
            if client and client.auth_level.value >= endpoint.auth_level.value:
                return client
        
        return None
    
    def _find_client_by_api_key(self, api_key: str) -> Optional[ClientInfo]:
        """Encontra cliente por API key."""
        for client in self.clients.values():
            if client.api_key == api_key:
                return client
        return None
    
    async def _validate_jwt_token(self, token: str) -> Optional[ClientInfo]:
        """Valida token JWT."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            
            client_id = payload.get("client_id")
            
            if client_id in self.clients:
                client = self.clients[client_id]
                
                # Verificar expiração
                exp = payload.get("exp", 0)
                if exp > time.time():
                    return client
            
        except jwt.InvalidTokenError:
            pass
        
        return None
    
    async def _check_rate_limits(self, client: ClientInfo, endpoint: APIEndpoint) -> bool:
        """Verifica rate limits."""
        if client.auth_level == AuthLevel.SYSTEM:
            return True  # Sistema sem limites
        
        current_time = time.time()
        
        # Verificar cada rate limit do endpoint
        for rate_limit in endpoint.rate_limits:
            key = f"{client.client_id}:{endpoint.path}:{rate_limit.limit_type.value}"
            
            # Usar Redis se disponível
            if self.redis_available:
                current_count = await self._check_redis_rate_limit(key, rate_limit, current_time)
            else:
                current_count = self._check_local_rate_limit(key, rate_limit, current_time)
            
            if current_count > rate_limit.max_requests:
                return False
        
        return True
    
    async def _check_redis_rate_limit(self, key: str, rate_limit: RateLimit, current_time: float) -> int:
        """Verifica rate limit usando Redis."""
        try:
            pipe = self.redis_client.pipeline()
            
            # Sliding window com sorted sets
            window_start = current_time - rate_limit.window_seconds
            
            # Remover requisições antigas
            pipe.zremrangebyscore(key, 0, window_start)
            
            # Adicionar requisição atual
            pipe.zadd(key, {str(current_time): current_time})
            
            # Contar requisições na janela
            pipe.zcard(key)
            
            # Definir expiração
            pipe.expire(key, rate_limit.window_seconds)
            
            results = pipe.execute()
            return results[2]  # Resultado do zcard
            
        except Exception as e:
            logger.error(f"❌ Erro no Redis rate limit: {e}")
            return 0
    
    def _check_local_rate_limit(self, key: str, rate_limit: RateLimit, current_time: float) -> int:
        """Verifica rate limit usando cache local."""
        window_start = current_time - rate_limit.window_seconds
        
        # Limpar requisições antigas
        requests = self.rate_limit_cache[key][rate_limit.limit_type.value]
        while requests and requests[0] < window_start:
            requests.popleft()
        
        # Adicionar requisição atual
        requests.append(current_time)
        
        return len(requests)
    
    async def _proxy_to_service(self, request: Request, endpoint: APIEndpoint, path: str) -> JSONResponse:
        """Faz proxy da requisição para o serviço de destino."""
        if endpoint.target_service == "internal":
            # Requisições internas
            return await self._handle_internal_request(request, path)
        
        # Proxy para agente específico
        try:
            # Ler body da requisição
            body = await request.body()
            
            # Criar mensagem para o agente
            agent_request = AgentMessage(
                id=str(uuid4()),
                sender_id=self.agent_id,
                recipient_id=endpoint.target_service,
                message_type=MessageType.REQUEST,
                priority=Priority.MEDIUM,
                content={
                    'request_type': 'api_request',
                    'path': path,
                    'method': request.method,
                    'headers': dict(request.headers),
                    'query_params': dict(request.query_params),
                    'body': body.decode() if body else None
                },
                timestamp=datetime.now()
            )
            
            # Enviar mensagem e aguardar resposta
            await self.message_bus.publish(agent_request)
            
            # TODO: Implementar espera por resposta com timeout
            # Por ora, retorna resposta simulada
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": f"Request proxied to {endpoint.target_service}",
                    "path": path,
                    "method": request.method
                }
            )
            
        except Exception as e:
            logger.error(f"❌ Erro no proxy para {endpoint.target_service}: {e}")
            return JSONResponse(
                status_code=502,
                content={"error": "Service unavailable"}
            )
    
    async def _handle_internal_request(self, request: Request, path: str) -> JSONResponse:
        """Trata requisições internas."""
        if path == "/api/public/status":
            return JSONResponse(content={
                "status": "operational",
                "system": "SUNA-ALSHAM v2.0",
                "agents": len(self.message_bus.subscribers) if hasattr(self.message_bus, 'subscribers') else 0,
                "gateway": {
                    "endpoints": len(self.endpoints),
                    "clients": len(self.clients),
                    "requests_today": self.gateway_metrics['total_requests']
                },
                "timestamp": datetime.now().isoformat()
            })
        
        return JSONResponse(
            status_code=404,
            content={"error": "Internal endpoint not found"}
        )
    
    async def _get_cached_response(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Obtém resposta do cache."""
        if self.redis_available:
            try:
                cached = self.redis_client.get(f"cache:{cache_key}")
                return json.loads(cached) if cached else None
            except:
                pass
        
        return None
    
    async def _cache_response(self, cache_key: str, content: Any, ttl: int):
        """Armazena resposta no cache."""
        if self.redis_available:
            try:
                self.redis_client.setex(
                    f"cache:{cache_key}",
                    ttl,
                    json.dumps(content)
                )
            except:
                pass
    
    def _generate_request_id(self) -> str:
        """Gera ID único para a requisição."""
        return f"req_{int(time.time())}_{hash(time.time()) % 1000000}"
    
    def _get_client_ip(self, request: Request) -> str:
        """Obtém IP do cliente."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    
    async def _detect_suspicious_activity(self, request: Request) -> bool:
        """Detecta atividade suspeita."""
        # Verificar padrões suspeitos
        user_agent = request.headers.get("User-Agent", "")
        
        for pattern in self.suspicious_patterns:
            if pattern in user_agent.lower():
                return True
        
        # Verificar frequência de requisições
        client_ip = self._get_client_ip(request)
        recent_requests = [
            log for log in list(self.request_logs)[-100:]
            if log.ip_address == client_ip and 
            (datetime.now() - log.timestamp).seconds < 60
        ]
        
        if len(recent_requests) > 100:  # Mais de 100 req/min
            return True
        
        return False
    
    async def _log_request(self, request: Request, response, response_time: float, request_id: str):
        """Log da requisição."""
        log = RequestLog(
            request_id=request_id,
            client_id=getattr(request.state, 'client_id', 'unknown'),
            endpoint=request.url.path,
            method=request.method,
            status_code=response.status_code,
            response_time_ms=response_time,
            timestamp=datetime.now(),
            user_agent=request.headers.get("User-Agent", ""),
            ip_address=self._get_client_ip(request)
        )
        
        self.request_logs.append(log)
        
        # Atualizar métricas
        self.gateway_metrics['total_requests'] += 1
        if response.status_code < 400:
            self.gateway_metrics['successful_requests'] += 1
        else:
            self.gateway_metrics['failed_requests'] += 1
        
        # Calcular tempo médio de resposta
        total_time = (self.gateway_metrics['average_response_time'] * (self.gateway_metrics['total_requests'] - 1) + response_time)
        self.gateway_metrics['average_response_time'] = total_time / self.gateway_metrics['total_requests']
    
    def _load_security_rules(self) -> List[Dict[str, Any]]:
        """Carrega regras de segurança."""
        return [
            {
                'name': 'sql_injection',
                'pattern': r'(union|select|insert|delete|drop|alter)',
                'action': 'block'
            },
            {
                'name': 'xss_attempt',
                'pattern': r'(<script|javascript:|onload=)',
                'action': 'block'
            },
            {
                'name': 'path_traversal',
                'pattern': r'(\.\./|\.\.\\)',
                'action': 'block'
            }
        ]
    
    def _load_suspicious_patterns(self) -> List[str]:
        """Carrega padrões suspeitos."""
        return [
            'bot', 'crawler', 'spider', 'scraper',
            'python-requests', 'curl', 'wget',
            'sqlmap', 'nikto', 'burp'
        ]
    
    async def _register_endpoint(self, endpoint_data: Dict[str, Any]) -> Dict[str, Any]:
        """Registra novo endpoint."""
        try:
            endpoint = APIEndpoint(
                path=endpoint_data['path'],
                methods=endpoint_data['methods'],
                target_service=endpoint_data['target_service'],
                auth_level=AuthLevel(endpoint_data.get('auth_level', 'authenticated')),
                rate_limits=self.default_rate_limits[AuthLevel(endpoint_data.get('auth_level', 'authenticated'))],
                description=endpoint_data.get('description', ''),
                version=endpoint_data.get('version', 'v1'),
                tags=endpoint_data.get('tags', [])
            )
            
            self.endpoints[endpoint.path] = endpoint
            
            logger.info(f"✅ Endpoint registrado: {endpoint.path}")
            
            return {
                'status': 'success',
                'endpoint': endpoint.path,
                'methods': endpoint.methods,
                'target_service': endpoint.target_service
            }
            
        except Exception as e:
            logger.error(f"❌ Erro registrando endpoint: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria novo cliente."""
        try:
            client_id = client_data.get('client_id', f"client_{len(self.clients)}")
            api_key = self._generate_api_key(client_id)
            
            client = ClientInfo(
                client_id=client_id,
                api_key=api_key,
                auth_level=AuthLevel(client_data.get('auth_level', 'authenticated')),
                rate_limits=client_data.get('rate_limits', {}),
                created_at=datetime.now(),
                last_seen=datetime.now(),
                metadata=client_data.get('metadata', {})
            )
            
            self.clients[client_id] = client
            
            logger.info(f"✅ Cliente criado: {client_id}")
            
            return {
                'status': 'success',
                'client_id': client_id,
                'api_key': api_key,
                'auth_level': client.auth_level.value
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando cliente: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_api_key(self, client_id: str) -> str:
        """Gera API key para cliente."""
        data = f"{client_id}:{time.time()}:{self.jwt_secret}"
        return hashlib.sha256(data.encode()).hexdigest()[:32]
    
    async def _generate_auth_token(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Gera token JWT."""
        try:
            client_id = credentials.get('client_id')
            api_key = credentials.get('api_key')
            
            client = self._find_client_by_api_key(api_key)
            if not client or client.client_id != client_id:
                return {'status': 'error', 'message': 'Invalid credentials'}
            
            # Gerar token JWT
            payload = {
                'client_id': client_id,
                'auth_level': client.auth_level.value,
                'exp': time.time() + 3600,  # 1 hora
                'iat': time.time()
            }
            
            token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
            
            return {
                'status': 'success',
                'token': token,
                'expires_in': 3600,
                'token_type': 'Bearer'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro gerando token: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _list_endpoints(self) -> Dict[str, Any]:
        """Lista endpoints disponíveis."""
        endpoints_list = []
        
        for path, endpoint in self.endpoints.items():
            endpoints_list.append({
                'path': path,
                'methods': endpoint.methods,
                'auth_level': endpoint.auth_level.value,
                'status': endpoint.status.value,
                'description': endpoint.description,
                'version': endpoint.version,
                'tags': endpoint.tags
            })
        
        return {
            'status': 'success',
            'total_endpoints': len(endpoints_list),
            'endpoints': endpoints_list
        }
    
    async def _get_detailed_metrics(self) -> Dict[str, Any]:
        """Obtém métricas detalhadas."""
        # Métricas por endpoint
        endpoint_metrics = {}
        for log in list(self.request_logs)[-1000:]:  # Últimas 1000 requisições
            if log.endpoint not in endpoint_metrics:
                endpoint_metrics[log.endpoint] = {
                    'requests': 0,
                    'errors': 0,
                    'avg_response_time': 0
                }
            
            endpoint_metrics[log.endpoint]['requests'] += 1
            if log.status_code >= 400:
                endpoint_metrics[log.endpoint]['errors'] += 1
        
        # Métricas por cliente
        client_metrics = {}
        for client_id, client in self.clients.items():
            client_metrics[client_id] = {
                'total_requests': client.total_requests,
                'failed_requests': client.failed_requests,
                'auth_level': client.auth_level.value,
                'last_seen': client.last_seen.isoformat()
            }
        
        return {
            'gateway_metrics': self.gateway_metrics,
            'endpoint_metrics': endpoint_metrics,
            'client_metrics': client_metrics,
            'system_info': {
                'total_endpoints': len(self.endpoints),
                'active_clients': len(self.clients),
                'blocked_ips': len(self.blocked_ips),
                'redis_available': self.redis_available
            }
        }
    
    # ... (continuar com outros métodos como cleanup, security, etc.)
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original."""
        response = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            priority=original_message.priority,
            content=response_data,
            timestamp=datetime.now(),
            correlation_id=original_message.id
        )
        await self.message_bus.publish(response)

}
