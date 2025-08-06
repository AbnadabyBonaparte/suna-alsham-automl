#!/usr/bin/env python3
"""
Database Agent – ALSHAM QUANTUM
[Quantum Version 2.0 - Multi-Provider Database Intelligence]

Sistema avançado de gerenciamento de banco de dados com suporte a múltiplos 
provedores, cache inteligente, connection pooling e auto-recovery.
"""

import asyncio
import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

# Multi-Provider Database Support
try:
    import asyncpg  # PostgreSQL
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False
    asyncpg = None

try:
    import aiomysql  # MySQL
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    aiomysql = None

try:
    import aiosqlite  # SQLite
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False
    aiosqlite = None

try:
    import motor.motor_asyncio  # MongoDB
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    motor = None

from suna_alsham_core.multi_agent_network import (
    AgentMessage, AgentType, BaseNetworkAgent, MessageType, Priority
)

logger = logging.getLogger(__name__)

class DatabaseProvider(Enum):
    """Provedores de banco de dados suportados."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"

class QueryType(Enum):
    """Tipos de query suportados."""
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    CREATE = "create"
    DROP = "drop"
    AGGREGATE = "aggregate"

@dataclass
class DatabaseConfig:
    """Configuração de provedor de banco de dados."""
    provider: DatabaseProvider
    connection_string: str
    max_connections: int = 10
    timeout_seconds: int = 30
    available: bool = True
    last_error: Optional[str] = None
    connection_pool: Optional[Any] = None
    response_times: List[float] = field(default_factory=list)
    query_count: int = 0
    error_count: int = 0

@dataclass
class QueryRequest:
    """Requisição de query estruturada."""
    request_id: str
    query: str
    params: Optional[List[Any]] = None
    query_type: QueryType = QueryType.SELECT
    cache_key: Optional[str] = None
    timeout: int = 30
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class QueryResponse:
    """Resposta de query com métricas."""
    request_id: str
    data: List[Dict[str, Any]]
    rows_affected: int
    provider_used: DatabaseProvider
    execution_time_ms: float
    from_cache: bool = False
    created_at: datetime = field(default_factory=datetime.now)

class QuantumDatabaseAgent(BaseNetworkAgent):
    """
    Agente de Banco de Dados Quantum com capacidades avançadas:
    - Múltiplos provedores de DB (PostgreSQL, MySQL, SQLite, MongoDB)
    - Connection pooling inteligente
    - Cache automático com TTL configurável
    - Auto-recovery em caso de falhas
    - Métricas detalhadas de performance
    - Query optimization automática
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend([
            "multi_provider_database",
            "connection_pooling",
            "intelligent_caching",
            "auto_recovery",
            "query_optimization",
            "performance_metrics",
            "schema_management"
        ])
        
        self.providers: Dict[DatabaseProvider, DatabaseConfig] = {}
        self.query_cache: Dict[str, Tuple[QueryResponse, datetime]] = {}
        self.active_queries: Dict[str, QueryRequest] = {}
        self.cache_ttl_seconds = int(os.environ.get("DB_CACHE_TTL", "300"))  # 5 minutos
        self.performance_metrics = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "avg_response_time": 0.0,
            "provider_usage": {},
            "uptime_start": datetime.now()
        }
        
        # Inicialização quantum
        self._initialize_database_providers()
        self._quantum_init_task = asyncio.create_task(self._quantum_initialization())
        self._cache_cleanup_task = asyncio.create_task(self._cache_cleanup_loop())
        
        logger.info(f"🗄️ {self.agent_id} (Quantum Database) inicializado com {len(self.providers)} provedores de DB.")

    def _initialize_database_providers(self):
        """Inicializa múltiplos provedores de banco de dados."""
        
        # PostgreSQL Provider
        postgres_url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRESQL_URL")
        if POSTGRESQL_AVAILABLE and postgres_url:
            self.providers[DatabaseProvider.POSTGRESQL] = DatabaseConfig(
                provider=DatabaseProvider.POSTGRESQL,
                connection_string=postgres_url,
                max_connections=int(os.environ.get("PG_MAX_CONNECTIONS", "10")),
                timeout_seconds=int(os.environ.get("PG_TIMEOUT", "30"))
            )
            logger.info("✅ Provedor PostgreSQL configurado.")
        
        # MySQL Provider
        mysql_url = os.environ.get("MYSQL_URL")
        if MYSQL_AVAILABLE and mysql_url:
            self.providers[DatabaseProvider.MYSQL] = DatabaseConfig(
                provider=DatabaseProvider.MYSQL,
                connection_string=mysql_url,
                max_connections=int(os.environ.get("MYSQL_MAX_CONNECTIONS", "10")),
                timeout_seconds=int(os.environ.get("MYSQL_TIMEOUT", "30"))
            )
            logger.info("✅ Provedor MySQL configurado.")
        
        # SQLite Provider (sempre disponível como fallback)
        if SQLITE_AVAILABLE:
            sqlite_path = os.environ.get("SQLITE_PATH", "./alsham_quantum.db")
            self.providers[DatabaseProvider.SQLITE] = DatabaseConfig(
                provider=DatabaseProvider.SQLITE,
                connection_string=f"sqlite:///{sqlite_path}",
                max_connections=1,  # SQLite é single-threaded
                timeout_seconds=10
            )
            logger.info("✅ Provedor SQLite configurado como fallback.")
        
        # MongoDB Provider
        mongodb_url = os.environ.get("MONGODB_URL")
        if MONGODB_AVAILABLE and mongodb_url:
            self.providers[DatabaseProvider.MONGODB] = DatabaseConfig(
                provider=DatabaseProvider.MONGODB,
                connection_string=mongodb_url,
                max_connections=int(os.environ.get("MONGODB_MAX_CONNECTIONS", "10")),
                timeout_seconds=int(os.environ.get("MONGODB_TIMEOUT", "30"))
            )
            logger.info("✅ Provedor MongoDB configurado.")
        
        if not self.providers:
            self.status = "degraded"
            logger.critical("❌ NENHUM provedor de banco de dados configurado!")

    async def _quantum_initialization(self):
        """Inicialização e teste de conexão quantum."""
        if not self.providers:
            self.status = "degraded"
            return
            
        logger.info("🔍 Testando conexões com provedores de banco de dados...")
        active_providers = []
        
        for provider_type, config in self.providers.items():
            try:
                if await self._test_database_connection(provider_type, config):
                    active_providers.append(provider_type)
                    logger.info(f"✅ Provedor {provider_type.value} validado com sucesso.")
                else:
                    config.available = False
                    logger.warning(f"⚠️ Provedor {provider_type.value} indisponível.")
            except Exception as e:
                config.available = False
                config.last_error = str(e)
                logger.error(f"❌ Erro testando provedor {provider_type.value}: {e}")
        
        if active_providers:
            self.status = "active"
            logger.info(f"🚀 {len(active_providers)} provedores ativos. Sistema database quantum operacional.")
        else:
            self.status = "degraded"
            logger.critical("❌ NENHUM provedor de banco disponível! Sistema em modo degradado.")

    async def _test_database_connection(self, provider_type: DatabaseProvider, config: DatabaseConfig) -> bool:
        """Testa conexão com um provedor específico."""
        try:
            if provider_type == DatabaseProvider.POSTGRESQL and POSTGRESQL_AVAILABLE:
                conn = await asyncpg.connect(config.connection_string, timeout=15.0)
                await conn.execute("SELECT 1")
                await conn.close()
                return True
                
            elif provider_type == DatabaseProvider.MYSQL and MYSQL_AVAILABLE:
                pool = await aiomysql.create_pool(
                    **self._parse_mysql_url(config.connection_string),
                    maxsize=1, timeout=15.0
                )
                async with pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute("SELECT 1")
                pool.close()
                await pool.wait_closed()
                return True
                
            elif provider_type == DatabaseProvider.SQLITE and SQLITE_AVAILABLE:
                db_path = config.connection_string.replace("sqlite:///", "")
                async with aiosqlite.connect(db_path, timeout=15.0) as conn:
                    await conn.execute("SELECT 1")
                return True
                
            elif provider_type == DatabaseProvider.MONGODB and MONGODB_AVAILABLE:
                client = motor.motor_asyncio.AsyncIOMotorClient(
                    config.connection_string, serverSelectionTimeoutMS=15000
                )
                await client.admin.command('ping')
                client.close()
                return True
                
        except Exception as e:
            logger.debug(f"Teste de conexão falhou para {provider_type.value}: {e}")
            
        return False

    def _parse_mysql_url(self, url: str) -> Dict[str, Any]:
        """Parse MySQL URL para parâmetros de conexão."""
        # Implementação básica - pode ser expandida
        return {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "",
            "db": "alsham_quantum"
        }

    async def _cache_cleanup_loop(self):
        """Loop de limpeza do cache baseado em TTL."""
        while True:
            await asyncio.sleep(60)  # Cleanup a cada minuto
            
            try:
                current_time = datetime.now()
                expired_keys = []
                
                for cache_key, (response, timestamp) in self.query_cache.items():
                    if (current_time - timestamp).total_seconds() > self.cache_ttl_seconds:
                        expired_keys.append(cache_key)
                
                for key in expired_keys:
                    del self.query_cache[key]
                
                if expired_keys:
                    logger.debug(f"🗑️ Cache cleanup: {len(expired_keys)} entradas expiradas removidas")
                    
            except Exception as e:
                logger.error(f"❌ Erro no cleanup do cache: {e}")

    def _generate_cache_key(self, query: str, params: Optional[List[Any]] = None) -> str:
        """Gera chave de cache para a query."""
        content = f"{query}_{json.dumps(params, sort_keys=True) if params else 'no_params'}"
        return hashlib.md5(content.encode()).hexdigest()

    def _select_optimal_provider(self, query_type: QueryType) -> Optional[DatabaseProvider]:
        """Seleciona o provedor optimal baseado no tipo de query e performance."""
        available_providers = [p for p, config in self.providers.items() if config.available]
        
        if not available_providers:
            return None
        
        # Prioridade para diferentes tipos de query
        if query_type in [QueryType.SELECT, QueryType.AGGREGATE]:
            # Para reads, prioriza providers mais rápidos
            if DatabaseProvider.POSTGRESQL in available_providers:
                return DatabaseProvider.POSTGRESQL
            elif DatabaseProvider.MYSQL in available_providers:
                return DatabaseProvider.MYSQL
        
        # Para writes, usa provider primário disponível
        priority_order = [
            DatabaseProvider.POSTGRESQL,
            DatabaseProvider.MYSQL,
            DatabaseProvider.SQLITE,
            DatabaseProvider.MONGODB
        ]
        
        for provider in priority_order:
            if provider in available_providers:
                return provider
        
        return available_providers[0]  # Fallback

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de banco de dados quantum."""
        if message.message_type != MessageType.REQUEST:
            return
        
        if self.status != "active":
            await self.publish_error_response(
                message, 
                f"Database Agent Quantum não está operacional. Status: {self.status.upper()}"
            )
            return
        
        request_type = message.content.get("request_type")
        
        if request_type == "execute_query":
            await self._handle_execute_query(message)
        elif request_type == "get_database_metrics":
            await self._handle_metrics_request(message)
        elif request_type == "clear_cache":
            await self._handle_clear_cache(message)
        else:
            await self.publish_error_response(message, f"Tipo de requisição não suportado: {request_type}")

    async def _handle_execute_query(self, message: AgentMessage):
        """Processa requisição de execução de query."""
        request_id = message.message_id
        query = message.content.get("query", "")
        params = message.content.get("params")
        
        if not query:
            await self.publish_error_response(message, "Query não especificada.")
            return
        
        logger.info(f"🗄️ [Quantum DB] Executando query '{request_id}': '{query[:100]}...'")
        
        try:
            # Determina tipo da query
            query_type = self._determine_query_type(query)
            
            # Cria estrutura de requisição
            query_request = QueryRequest(
                request_id=request_id,
                query=query,
                params=params,
                query_type=query_type,
                cache_key=self._generate_cache_key(query, params) if query_type == QueryType.SELECT else None
            )
            
            self.active_queries[request_id] = query_request
            
            # Verifica cache para queries SELECT
            if query_type == QueryType.SELECT and query_request.cache_key:
                cached_result = self._get_from_cache(query_request.cache_key)
                if cached_result:
                    self.performance_metrics["cache_hits"] += 1
                    await self.publish_response(message, {
                        "status": "success",
                        "data": cached_result.data,
                        "rows_affected": cached_result.rows_affected,
                        "execution_time_ms": cached_result.execution_time_ms,
                        "from_cache": True,
                        "provider_used": cached_result.provider_used.value
                    })
                    return
                else:
                    self.performance_metrics["cache_misses"] += 1
            
            # Executa query
            query_response = await self._execute_query_with_provider(query_request)
            
            # Cache resultado se for SELECT
            if query_type == QueryType.SELECT and query_request.cache_key:
                self._store_in_cache(query_request.cache_key, query_response)
            
            # Atualiza métricas
            self.performance_metrics["total_queries"] += 1
            self.performance_metrics["successful_queries"] += 1
            
            provider_used = query_response.provider_used.value
            self.performance_metrics["provider_usage"][provider_used] = (
                self.performance_metrics["provider_usage"].get(provider_used, 0) + 1
            )
            
            # Resposta de sucesso
            response_content = {
                "status": "success",
                "data": query_response.data,
                "rows_affected": query_response.rows_affected,
                "execution_time_ms": query_response.execution_time_ms,
                "from_cache": query_response.from_cache,
                "provider_used": provider_used
            }
            
            await self.publish_response(message, response_content)
            logger.info(f"🗄️ [Quantum DB] Query executada com sucesso usando {provider_used} ({query_response.execution_time_ms:.1f}ms)")
            
        except Exception as e:
            self.performance_metrics["failed_queries"] += 1
            logger.error(f"❌ [Quantum DB] Erro ao executar query: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro no Database Quantum: {e}")
        
        finally:
            # Cleanup
            if request_id in self.active_queries:
                del self.active_queries[request_id]

    def _determine_query_type(self, query: str) -> QueryType:
        """Determina o tipo da query baseado no SQL."""
        query_upper = query.strip().upper()
        
        if query_upper.startswith("SELECT"):
            if any(keyword in query_upper for keyword in ["COUNT(", "SUM(", "AVG(", "MAX(", "MIN(", "GROUP BY"]):
                return QueryType.AGGREGATE
            return QueryType.SELECT
        elif query_upper.startswith("INSERT"):
            return QueryType.INSERT
        elif query_upper.startswith("UPDATE"):
            return QueryType.UPDATE
        elif query_upper.startswith("DELETE"):
            return QueryType.DELETE
        elif query_upper.startswith("CREATE"):
            return QueryType.CREATE
        elif query_upper.startswith("DROP"):
            return QueryType.DROP
        else:
            return QueryType.SELECT  # Default

    def _get_from_cache(self, cache_key: str) -> Optional[QueryResponse]:
        """Recupera resultado do cache se não expirado."""
        if cache_key in self.query_cache:
            response, timestamp = self.query_cache[cache_key]
            if (datetime.now() - timestamp).total_seconds() <= self.cache_ttl_seconds:
                return response
            else:
                # Remove entrada expirada
                del self.query_cache[cache_key]
        return None

    def _store_in_cache(self, cache_key: str, response: QueryResponse):
        """Armazena resultado no cache."""
        self.query_cache[cache_key] = (response, datetime.now())
        
        # Limita tamanho do cache
        if len(self.query_cache) > 1000:
            # Remove as 100 entradas mais antigas
            sorted_cache = sorted(
                self.query_cache.items(),
                key=lambda x: x[1][1]  # Ordena por timestamp
            )
            for key, _ in sorted_cache[:100]:
                del self.query_cache[key]

    async def _execute_query_with_provider(self, request: QueryRequest) -> QueryResponse:
        """Executa query com o provedor optimal."""
        start_time = time.time()
        
        # Seleciona provedor optimal
        provider_type = self._select_optimal_provider(request.query_type)
        if not provider_type:
            raise Exception("Nenhum provedor de banco de dados disponível")
        
        provider_config = self.providers[provider_type]
        
        try:
            # Executa query com o provedor selecionado
            data, rows_affected = await self._execute_with_specific_provider(
                provider_type, provider_config, request.query, request.params
            )
            
            execution_time = (time.time() - start_time) * 1000
            
            response = QueryResponse(
                request_id=request.request_id,
                data=data,
                rows_affected=rows_affected,
                provider_used=provider_type,
                execution_time_ms=execution_time
            )
            
            # Atualiza métricas do provider
            provider_config.response_times.append(execution_time)
            if len(provider_config.response_times) > 100:
                provider_config.response_times = provider_config.response_times[-100:]
            
            provider_config.query_count += 1
            
            return response
            
        except Exception as e:
            provider_config.available = False
            provider_config.last_error = str(e)
            provider_config.error_count += 1
            logger.error(f"❌ Provedor {provider_type.value} falhou: {e}")
            
            # Tenta com próximo provedor disponível
            remaining_providers = [p for p, c in self.providers.items() if c.available and p != provider_type]
            if remaining_providers:
                # Recursão com próximo provider
                request.query_type = self._determine_query_type(request.query)  # Redefine tipo
                return await self._execute_query_with_provider(request)
            else:
                raise Exception(f"Todos os provedores falharam. Último erro: {e}")

    async def _execute_with_specific_provider(self, provider_type: DatabaseProvider, 
                                            config: DatabaseConfig, query: str, 
                                            params: Optional[List[Any]] = None) -> Tuple[List[Dict], int]:
        """Executa query com um provedor específico."""
        
        if provider_type == DatabaseProvider.POSTGRESQL:
            return await self._execute_postgresql(config, query, params)
        elif provider_type == DatabaseProvider.MYSQL:
            return await self._execute_mysql(config, query, params)
        elif provider_type == DatabaseProvider.SQLITE:
            return await self._execute_sqlite(config, query, params)
        elif provider_type == DatabaseProvider.MONGODB:
            return await self._execute_mongodb(config, query, params)
        else:
            raise Exception(f"Provedor {provider_type.value} não suportado")

    async def _execute_postgresql(self, config: DatabaseConfig, query: str, 
                                 params: Optional[List[Any]] = None) -> Tuple[List[Dict], int]:
        """Executa query no PostgreSQL."""
        conn = await asyncpg.connect(config.connection_string, timeout=config.timeout_seconds)
        try:
            if query.strip().upper().startswith("SELECT"):
                rows = await conn.fetch(query, *(params or []))
                data = [dict(row) for row in rows]
                return data, len(data)
            else:
                result = await conn.execute(query, *(params or []))
                # Parse do resultado para extrair número de linhas afetadas
                rows_affected = int(result.split()[-1]) if result and result.split()[-1].isdigit() else 0
                return [], rows_affected
        finally:
            await conn.close()

    async def _execute_mysql(self, config: DatabaseConfig, query: str, 
                            params: Optional[List[Any]] = None) -> Tuple[List[Dict], int]:
        """Executa query no MySQL."""
        pool = await aiomysql.create_pool(
            **self._parse_mysql_url(config.connection_string),
            maxsize=config.max_connections,
            timeout=config.timeout_seconds
        )
        try:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, params or [])
                    if query.strip().upper().startswith("SELECT"):
                        data = await cursor.fetchall()
                        return list(data), len(data)
                    else:
                        await conn.commit()
                        return [], cursor.rowcount
        finally:
            pool.close()
            await pool.wait_closed()

    async def _execute_sqlite(self, config: DatabaseConfig, query: str, 
                             params: Optional[List[Any]] = None) -> Tuple[List[Dict], int]:
        """Executa query no SQLite."""
        db_path = config.connection_string.replace("sqlite:///", "")
        async with aiosqlite.connect(db_path, timeout=config.timeout_seconds) as conn:
            conn.row_factory = aiosqlite.Row  # Para retornar dict-like rows
            async with conn.execute(query, params or []) as cursor:
                if query.strip().upper().startswith("SELECT"):
                    rows = await cursor.fetchall()
                    data = [dict(row) for row in rows]
                    return data, len(data)
                else:
                    await conn.commit()
                    return [], cursor.rowcount

    async def _execute_mongodb(self, config: DatabaseConfig, query: str, 
                              params: Optional[List[Any]] = None) -> Tuple[List[Dict], int]:
        """Executa operação no MongoDB."""
        # Implementação básica - MongoDB usa diferentes operações, não SQL
        client = motor.motor_asyncio.AsyncIOMotorClient(
            config.connection_string, serverSelectionTimeoutMS=config.timeout_seconds * 1000
        )
        try:
            # Esta é uma implementação simplificada
            # Em produção, seria necessário parser JSON/MongoDB operations
            db = client.get_default_database()
            collection = db.get_collection("default_collection")
            
            # Exemplo básico de find
            cursor = collection.find({})
            data = await cursor.to_list(length=100)
            
            # Converte ObjectId para string para serialização JSON
            for doc in data:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            
            return data, len(data)
        finally:
            client.close()

    async def _handle_metrics_request(self, message: AgentMessage):
        """Processa requisições de métricas do database."""
        metrics = self.get_database_metrics()
        await self.publish_response(message, {"status": "success", "metrics": metrics})

    async def _handle_clear_cache(self, message: AgentMessage):
        """Limpa o cache de queries."""
        cache_size = len(self.query_cache)
        self.query_cache.clear()
        
        await self.publish_response(message, {
            "status": "success",
            "message": f"Cache limpo. {cache_size} entradas removidas."
        })

    def get_database_metrics(self) -> Dict[str, Any]:
        """Retorna métricas completas do database quantum."""
        total_queries = self.performance_metrics["total_queries"]
        uptime = datetime.now() - self.performance_metrics["uptime_start"]
        
        # Calcula tempo médio de resposta
        all_response_times = []
        for config in self.providers.values():
            all_response_times.extend(config.response_times)
        
        avg_response_time = (
            sum(all_response_times) / len(all_response_times)
            if all_response_times else 0.0
        )
        
        return {
            **self.performance_metrics,
            "uptime_seconds": uptime.total_seconds(),
            "avg_response_time_ms": avg_response_time,
            "success_rate": (
                self.performance_metrics["successful_queries"] / total_queries
                if total_queries > 0 else 1.0
            ),
            "cache_hit_rate": (
                self.performance_metrics["cache_hits"] / 
                (self.performance_metrics["cache_hits"] + self.performance_metrics["cache_misses"])
                if (self.performance_metrics["cache_hits"] + self.performance_metrics["cache_misses"]) > 0 else 0.0
            ),
            "active_providers": len([p for p, c in self.providers.items() if c.available]),
            "total_providers": len(self.providers),
            "cache_size": len(self.query_cache),
            "active_queries": len(self.active_queries),
            "provider_details": {
                provider.value: {
                    "available": config.available,
                    "query_count": config.query_count,
                    "error_count": config.error_count,
                    "avg_response_time": (
                        sum(config.response_times) / len(config.response_times)
                        if config.response_times else 0.0
                    ),
                    "last_error": config.last_error
                }
                for provider, config in self.providers.items()
            }
        }

def create_database_agent(message_bus: Any) -> List[BaseNetworkAgent]:
    """
    Factory function to create and initialize the QuantumDatabaseAgent(s) for the ALSHAM QUANTUM system.

    This function instantiates the QuantumDatabaseAgent, logs all relevant events for diagnostics,
    and returns it in a list for registration in the agent registry. Handles errors robustly
    and ensures the agent is ready for operation.

    Args:
        message_bus (Any): The message bus or communication channel for agent messaging.

    Returns:
        List[BaseNetworkAgent]: A list containing the initialized QuantumDatabaseAgent instance(s).
    """
    agents: List[BaseNetworkAgent] = []
    logger.info("🗄️ [Factory] Creating QuantumDatabaseAgent...")
    try:
        agent = QuantumDatabaseAgent("database_001", message_bus)
        agents.append(agent)
        logger.info(f"✅ QuantumDatabaseAgent created successfully: {agent.agent_id}")
    except Exception as e:
        logger.critical(f"❌ Critical error creating QuantumDatabaseAgent: {e}", exc_info=True)
    return agents
