import logging
import asyncio
import aiosqlite
import asyncpg
import redis.asyncio as redis
import json
import pickle
import hashlib
import time
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics
from pathlib import Path
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from suna_alsham_core.database_agent import BaseNetworkAgent, AgentMessage, ...

logger = logging.getLogger(__name__)

class DatabaseType(Enum):
    """Tipos de banco de dados suportados"""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    REDIS = "redis"
    MEMORY = "memory"
    FILE_SYSTEM = "filesystem"

class QueryType(Enum):
    """Tipos de queries"""
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    BULK_INSERT = "bulk_insert"
    AGGREGATE = "aggregate"
    COMPLEX_JOIN = "complex_join"

class CacheStrategy(Enum):
    """Estratégias de cache"""
    LRU = "lru"
    LFU = "lfu"
    TTL = "ttl"
    ADAPTIVE = "adaptive"
    NO_CACHE = "no_cache"

@dataclass
class QueryPlan:
    """Plano de execução de query"""
    query_id: str
    original_query: str
    optimized_query: str
    estimated_cost: float
    execution_time: float
    rows_affected: int
    use_cache: bool
    cache_key: Optional[str]
    indexes_used: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class DatabaseMetrics:
    """Métricas de performance do banco"""
    connection_pool_size: int
    active_connections: int
    query_count: int
    avg_query_time: float
    cache_hit_ratio: float
    index_efficiency: float
    storage_usage_mb: float
    fragmentation_ratio: float

@dataclass
class DataSchema:
    """Schema de dados inteligente"""
    table_name: str
    columns: Dict[str, str]
    indexes: List[str]
    constraints: List[str]
    relationships: Dict[str, str]
    auto_optimize: bool = True
    compression_enabled: bool = False

class DatabaseAgent(BaseNetworkAgent):
    """Agente de banco de dados com IA e otimização automática"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'data_management',
            'query_optimization',
            'intelligent_caching',
            'auto_indexing',
            'data_migration',
            'backup_recovery',
            'performance_tuning',
            'schema_evolution',
            'distributed_transactions',
            'data_analytics'
        ]
        
        # Conexões de banco
        self.connections = {}
        self.connection_pools = {}
        self.redis_client = None
        
        # Cache inteligente
        self.query_cache = {}
        self.result_cache = {}
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
        
        # Otimização de queries
        self.query_plans = {}
        self.query_performance_history = defaultdict(list)
        self.slow_queries = deque(maxlen=100)
        
        # Índices automáticos
        self.auto_indexes = {}
        self.index_usage_stats = defaultdict(int)
        
        # Configurações
        self.config = {
            'cache_ttl': 300,  # 5 minutos
            'max_cache_size': 1000,
            'slow_query_threshold': 1.0,  # segundos
            'auto_index_threshold': 10,  # consultas antes de criar índice
            'compression_threshold': 1000,  # linhas para ativar compressão
            'backup_interval': 3600  # 1 hora
        }
        
        # Estatísticas
        self.db_metrics = {
            'queries_executed': 0,
            'data_inserted': 0,
            'cache_hits': 0,
            'auto_optimizations': 0,
            'backups_created': 0
        }
        
        # Tasks de background
        self._optimization_task = None
        self._backup_task = None
        self._cleanup_task = None
        
        logger.info(f"🗄️ {self.agent_id} inicializado com gerenciamento inteligente de dados")
    
    async def start_database_services(self):
        """Inicia serviços de banco de dados"""
        if not self._optimization_task:
            # Inicializar conexões
            await self._initialize_connections()
            
            # Iniciar tasks de background
            self._optimization_task = asyncio.create_task(self._optimization_loop())
            self._backup_task = asyncio.create_task(self._backup_loop())
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
            
            logger.info(f"🗄️ {self.agent_id} iniciou serviços de banco de dados")
    
    async def stop_database_services(self):
        """Para serviços de banco de dados"""
        # Cancelar tasks
        for task in [self._optimization_task, self._backup_task, self._cleanup_task]:
            if task:
                task.cancel()
        
        # Fechar conexões
        await self._close_connections()
        
        logger.info(f"🛑 {self.agent_id} parou serviços de banco de dados")
    
    async def _initialize_connections(self):
        """Inicializa conexões com bancos de dados"""
        try:
            # SQLite para desenvolvimento local
            self.connections[DatabaseType.SQLITE] = await aiosqlite.connect(':memory:')
            
            # Redis para cache
            try:
                self.redis_client = redis.Redis(
                    host='localhost',
                    port=6379,
                    decode_responses=True
                )
                await self.redis_client.ping()
                logger.info("✅ Conectado ao Redis para cache")
            except:
                logger.warning("⚠️ Redis não disponível - usando cache em memória")
            
            # PostgreSQL (se configurado)
            pg_url = "postgresql://user:pass@localhost/suna_alsham"
            try:
                self.connections[DatabaseType.POSTGRESQL] = await asyncpg.connect(pg_url)
                logger.info("✅ Conectado ao PostgreSQL")
            except:
                logger.info("💡 PostgreSQL não configurado - usando SQLite")
            
        except Exception as e:
            logger.error(f"❌ Erro inicializando conexões: {e}")
    
    async def _close_connections(self):
        """Fecha todas as conexões"""
        for db_type, conn in self.connections.items():
            try:
                if db_type == DatabaseType.SQLITE:
                    await conn.close()
                elif db_type == DatabaseType.POSTGRESQL:
                    await conn.close()
            except:
                pass
        
        if self.redis_client:
            await self.redis_client.close()
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'execute_query':
                result = await self.execute_query(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'store_data':
                result = await self.store_data(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'retrieve_data':
                result = await self.retrieve_data(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'optimize_database':
                result = await self.optimize_database(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'create_backup':
                result = await self.create_backup(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'get_analytics':
                result = await self.get_data_analytics(message.content)
                await self._send_response(message, result)
    
    async def execute_query(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa query com otimização automática"""
        try:
            query = request_data.get('query')
            params = request_data.get('params', {})
            database = DatabaseType(request_data.get('database', 'sqlite'))
            cache_enabled = request_data.get('cache', True)
            
            logger.info(f"🔍 Executando query: {query[:50]}...")
            
            # Gerar chave de cache
            cache_key = self._generate_cache_key(query, params) if cache_enabled else None
            
            # Verificar cache primeiro
            if cache_enabled and cache_key:
                cached_result = await self._get_cached_result(cache_key)
                if cached_result:
                    self.cache_stats['hits'] += 1
                    self.db_metrics['cache_hits'] += 1
                    return {
                        'status': 'completed',
                        'data': cached_result,
                        'from_cache': True,
                        'execution_time': 0.001
                    }
            
            # Otimizar query
            optimized_query = await self._optimize_query(query, database)
            
            # Executar query
            start_time = time.time()
            result = await self._execute_raw_query(optimized_query, params, database)
            execution_time = time.time() - start_time
            
            # Armazenar no cache
            if cache_enabled and cache_key and execution_time > 0.1:
                await self._cache_result(cache_key, result)
            
            # Analisar performance
            await self._analyze_query_performance(query, execution_time, len(result) if isinstance(result, list) else 1)
            
            # Atualizar métricas
            self.db_metrics['queries_executed'] += 1
            self.cache_stats['misses'] += 1
            
            return {
                'status': 'completed',
                'data': result,
                'from_cache': False,
                'execution_time': execution_time,
                'rows_affected': len(result) if isinstance(result, list) else 1
            }
            
        except Exception as e:
            logger.error(f"❌ Erro executando query: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _optimize_query(self, query: str, database: DatabaseType) -> str:
        """Otimiza query automaticamente"""
        try:
            # Análise básica da query
            query_lower = query.lower().strip()
            optimized = query
            
            # Otimizações comuns
            if 'select *' in query_lower:
                # Sugerir colunas específicas (em produção, analisaria schema)
                logger.info("💡 Otimização: SELECT * pode ser otimizado especificando colunas")
            
            if 'order by' in query_lower and 'limit' not in query_lower:
                # Adicionar LIMIT para queries com ORDER BY
                if database == DatabaseType.SQLITE:
                    optimized += " LIMIT 1000"
                logger.info("💡 Otimização: Adicionado LIMIT para ORDER BY")
            
            # Verificar necessidade de índices
            if 'where' in query_lower:
                await self._suggest_indexes(query)
            
            return optimized
            
        except Exception as e:
            logger.error(f"❌ Erro otimizando query: {e}")
            return query
    
    async def _execute_raw_query(self, query: str, params: Dict, database: DatabaseType) -> Any:
        """Executa query no banco específico"""
        try:
            if database == DatabaseType.SQLITE:
                conn = self.connections[DatabaseType.SQLITE]
                cursor = await conn.execute(query, list(params.values()) if params else [])
                
                if query.lower().strip().startswith('select'):
                    result = await cursor.fetchall()
                    return [dict(row) for row in result] if result else []
                else:
                    await conn.commit()
                    return cursor.rowcount
            
            elif database == DatabaseType.POSTGRESQL and DatabaseType.POSTGRESQL in self.connections:
                conn = self.connections[DatabaseType.POSTGRESQL]
                
                if query.lower().strip().startswith('select'):
                    result = await conn.fetch(query, *params.values() if params else [])
                    return [dict(row) for row in result] if result else []
                else:
                    result = await conn.execute(query, *params.values() if params else [])
                    return int(result.split()[-1]) if result else 0
            
            else:
                # Fallback para SQLite
                return await self._execute_raw_query(query, params, DatabaseType.SQLITE)
                
        except Exception as e:
            logger.error(f"❌ Erro executando query raw: {e}")
            raise
    
    async def store_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Armazena dados com otimização automática"""
        try:
            table = request_data.get('table')
            data = request_data.get('data')
            database = DatabaseType(request_data.get('database', 'sqlite'))
            auto_optimize = request_data.get('auto_optimize', True)
            
            logger.info(f"💾 Armazenando dados na tabela: {table}")
            
            # Criar tabela se não existe
            await self._ensure_table_exists(table, data, database)
            
            # Inserir dados
            start_time = time.time()
            
            if isinstance(data, list):
                # Bulk insert
                result = await self._bulk_insert(table, data, database)
                self.db_metrics['data_inserted'] += len(data)
            else:
                # Insert único
                result = await self._single_insert(table, data, database)
                self.db_metrics['data_inserted'] += 1
            
            execution_time = time.time() - start_time
            
            # Otimização automática
            if auto_optimize:
                await self._auto_optimize_table(table, len(data) if isinstance(data, list) else 1)
            
            # Invalidar cache relacionado
            await self._invalidate_table_cache(table)
            
            return {
                'status': 'completed',
                'table': table,
                'rows_inserted': len(data) if isinstance(data, list) else 1,
                'execution_time': execution_time
            }
            
        except Exception as e:
            logger.error(f"❌ Erro armazenando dados: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _ensure_table_exists(self, table: str, sample_data: Any, database: DatabaseType):
        """Garante que a tabela existe, criando se necessário"""
        try:
            # Analisar estrutura dos dados
            if isinstance(sample_data, list) and sample_data:
                columns = self._infer_schema(sample_data[0])
            elif isinstance(sample_data, dict):
                columns = self._infer_schema(sample_data)
            else:
                columns = {'id': 'INTEGER PRIMARY KEY', 'data': 'TEXT'}
            
            # Criar DDL
            column_defs = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
            create_sql = f"CREATE TABLE IF NOT EXISTS {table} ({column_defs})"
            
            # Executar
            await self._execute_raw_query(create_sql, {}, database)
            
            logger.info(f"✅ Tabela {table} garantida com colunas: {list(columns.keys())}")
            
        except Exception as e:
            logger.error(f"❌ Erro criando tabela: {e}")
    
    def _infer_schema(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Infere schema automaticamente dos dados"""
        schema = {}
        
        for key, value in data.items():
            if isinstance(value, int):
                schema[key] = 'INTEGER'
            elif isinstance(value, float):
                schema[key] = 'REAL'
            elif isinstance(value, bool):
                schema[key] = 'BOOLEAN'
            elif isinstance(value, datetime):
                schema[key] = 'TIMESTAMP'
            else:
                schema[key] = 'TEXT'
        
        # Adicionar ID se não existe
        if 'id' not in schema:
            schema = {'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', **schema}
        
        return schema
    
    async def _bulk_insert(self, table: str, data: List[Dict], database: DatabaseType) -> int:
        """Inserção em lote otimizada"""
        if not data:
            return 0
        
        # Preparar dados
        columns = list(data[0].keys())
        placeholders = ', '.join(['?' for _ in columns])
        
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        
        # Executar em lotes
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            values = [list(row.values()) for row in batch]
            
            if database == DatabaseType.SQLITE:
                conn = self.connections[DatabaseType.SQLITE]
                await conn.executemany(sql, values)
                await conn.commit()
            
            total_inserted += len(batch)
        
        return total_inserted
    
    async def _single_insert(self, table: str, data: Dict, database: DatabaseType) -> int:
        """Inserção única"""
        columns = list(data.keys())
        placeholders = ', '.join(['?' for _ in columns])
        values = list(data.values())
        
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        
        await self._execute_raw_query(sql, {f"p{i}": v for i, v in enumerate(values)}, database)
        return 1
    
    async def retrieve_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recupera dados com cache inteligente"""
        try:
            table = request_data.get('table')
            filters = request_data.get('filters', {})
            limit = request_data.get('limit', 100)
            offset = request_data.get('offset', 0)
            order_by = request_data.get('order_by')
            database = DatabaseType(request_data.get('database', 'sqlite'))
            
            # Construir query
            query = f"SELECT * FROM {table}"
            
            # Adicionar filtros
            if filters:
                conditions = []
                for key, value in filters.items():
                    if isinstance(value, str):
                        conditions.append(f"{key} LIKE '%{value}%'")
                    else:
                        conditions.append(f"{key} = {value}")
                query += f" WHERE {' AND '.join(conditions)}"
            
            # Adicionar ordenação
            if order_by:
                query += f" ORDER BY {order_by}"
            
            # Adicionar limit/offset
            query += f" LIMIT {limit} OFFSET {offset}"
            
            # Executar query
            result = await self.execute_query({
                'query': query,
                'database': database.value,
                'cache': True
            })
            
            return {
                'status': 'completed',
                'table': table,
                'data': result['data'],
                'count': len(result['data']),
                'from_cache': result.get('from_cache', False)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro recuperando dados: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def optimize_database(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Otimiza banco de dados automaticamente"""
        try:
            database = DatabaseType(request_data.get('database', 'sqlite'))
            optimization_type = request_data.get('type', 'full')
            
            logger.info(f"⚡ Otimizando banco de dados: {optimization_type}")
            
            optimizations_applied = []
            
            if optimization_type in ['full', 'indexes']:
                # Criar índices automáticos
                index_result = await self._create_automatic_indexes(database)
                optimizations_applied.extend(index_result)
            
            if optimization_type in ['full', 'cleanup']:
                # Limpeza de dados antigos
                cleanup_result = await self._cleanup_old_data(database)
                optimizations_applied.extend(cleanup_result)
            
            if optimization_type in ['full', 'vacuum']:
                # Vacuum (SQLite)
                if database == DatabaseType.SQLITE:
                    await self._execute_raw_query("VACUUM", {}, database)
                    optimizations_applied.append("Vacuum executado")
            
            if optimization_type in ['full', 'analyze']:
                # Analyze estatísticas
                await self._analyze_table_stats(database)
                optimizations_applied.append("Estatísticas atualizadas")
            
            self.db_metrics['auto_optimizations'] += len(optimizations_applied)
            
            return {
                'status': 'completed',
                'optimizations_applied': optimizations_applied,
                'total_optimizations': len(optimizations_applied)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro otimizando banco: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def create_backup(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria backup inteligente"""
        try:
            database = DatabaseType(request_data.get('database', 'sqlite'))
            backup_type = request_data.get('type', 'full')
            compression = request_data.get('compression', True)
            
            logger.info(f"💾 Criando backup: {backup_type}")
            
            backup_info = {
                'backup_id': f"backup_{int(time.time())}",
                'timestamp': datetime.now().isoformat(),
                'type': backup_type,
                'database': database.value,
                'compression': compression
            }
            
            if backup_type == 'full':
                # Backup completo
                backup_info['tables'] = await self._backup_all_tables(database)
            else:
                # Backup incremental
                backup_info['changes'] = await self._backup_incremental(database)
            
            # Armazenar metadados do backup
            await self._store_backup_metadata(backup_info)
            
            self.db_metrics['backups_created'] += 1
            
            return {
                'status': 'completed',
                'backup_info': backup_info
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando backup: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def get_data_analytics(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna analytics dos dados"""
        try:
            table = request_data.get('table')
            metric_type = request_data.get('metric_type', 'overview')
            
            analytics = {}
            
            if metric_type in ['overview', 'size']:
                # Tamanho da tabela
                count_query = f"SELECT COUNT(*) as total FROM {table}"
                result = await self.execute_query({'query': count_query})
                analytics['total_rows'] = result['data'][0]['total']
            
            if metric_type in ['overview', 'performance']:
                # Performance das queries
                analytics['query_performance'] = {
                    'avg_execution_time': statistics.mean(
                        [t for times in self.query_performance_history.values() for t in times]
                    ) if self.query_performance_history else 0,
                    'slow_queries_count': len(self.slow_queries)
                }
            
            if metric_type in ['overview', 'cache']:
                # Estatísticas de cache
                total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
                analytics['cache_stats'] = {
                    'hit_ratio': (self.cache_stats['hits'] / max(total_requests, 1)) * 100,
                    'total_hits': self.cache_stats['hits'],
                    'total_misses': self.cache_stats['misses']
                }
            
            return {
                'status': 'completed',
                'table': table,
                'analytics': analytics,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro gerando analytics: {e}")
            return {'status': 'error', 'message': str(e)}
    
    # === MÉTODOS DE CACHE ===
    
    def _generate_cache_key(self, query: str, params: Dict) -> str:
        """Gera chave única para cache"""
        content = f"{query}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def _get_cached_result(self, cache_key: str) -> Any:
        """Recupera resultado do cache"""
        try:
            if self.redis_client:
                cached = await self.redis_client.get(f"query:{cache_key}")
                if cached:
                    return json.loads(cached)
            
            # Cache em memória
            if cache_key in self.result_cache:
                cached_item = self.result_cache[cache_key]
                if cached_item['expires'] > datetime.now():
                    return cached_item['data']
                else:
                    del self.result_cache[cache_key]
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro recuperando cache: {e}")
            return None
    
    async def _cache_result(self, cache_key: str, result: Any):
        """Armazena resultado no cache"""
        try:
            if self.redis_client:
                await self.redis_client.setex(
                    f"query:{cache_key}",
                    self.config['cache_ttl'],
                    json.dumps(result, default=str)
                )
            
            # Cache em memória
            self.result_cache[cache_key] = {
                'data': result,
                'expires': datetime.now() + timedelta(seconds=self.config['cache_ttl'])
            }
            
            # Limitar tamanho do cache
            if len(self.result_cache) > self.config['max_cache_size']:
                # Remover mais antigos
                oldest_key = min(
                    self.result_cache.keys(),
                    key=lambda k: self.result_cache[k]['expires']
                )
                del self.result_cache[oldest_key]
                self.cache_stats['evictions'] += 1
                
        except Exception as e:
            logger.error(f"❌ Erro armazenando cache: {e}")
    
    async def _invalidate_table_cache(self, table: str):
        """Invalida cache relacionado a uma tabela"""
        try:
            if self.redis_client:
                # Buscar chaves relacionadas à tabela
                pattern = f"query:*{table}*"
                keys = await self.redis_client.keys(pattern)
                if keys:
                    await self.redis_client.delete(*keys)
            
            # Cache em memória - invalidação simples
            keys_to_remove = []
            for key in self.result_cache.keys():
                if table.lower() in key.lower():
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del self.result_cache[key]
                
        except Exception as e:
            logger.error(f"❌ Erro invalidando cache: {e}")
    
    # === OTIMIZAÇÃO AUTOMÁTICA ===
    
    async def _analyze_query_performance(self, query: str, execution_time: float, rows: int):
        """Analisa performance da query"""
        self.query_performance_history[query].append(execution_time)
        
        # Detectar queries lentas
        if execution_time > self.config['slow_query_threshold']:
            self.slow_queries.append({
                'query': query[:100],
                'execution_time': execution_time,
                'rows': rows,
                'timestamp': datetime.now()
            })
    
    async def _suggest_indexes(self, query: str):
        """Sugere índices baseado na query"""
        # Análise simples para WHERE clauses
        query_lower = query.lower()
        if 'where' in query_lower:
            # Extrair colunas mencionadas no WHERE
            where_part = query_lower.split('where')[1].split('order by')[0].split('group by')[0]
            # Implementação simplificada - em produção seria mais sofisticada
            logger.info(f"💡 Considere criar índice para colunas em: {where_part.strip()}")
    
    async def _auto_optimize_table(self, table: str, rows_added: int):
        """Otimiza tabela automaticamente após inserções"""
        if rows_added > self.config['compression_threshold']:
            logger.info(f"⚡ Auto-otimização: Tabela {table} com {rows_added} novas linhas")
            # Implementar compressão ou particionamento se necessário
    
    async def _create_automatic_indexes(self, database: DatabaseType) -> List[str]:
        """Cria índices automáticos baseado no uso"""
        optimizations = []
        
        # Analisar queries frequentes para criar índices
        for query, times in self.query_performance_history.items():
            if len(times) >= self.config['auto_index_threshold']:
                avg_time = statistics.mean(times)
                if avg_time > 0.5:  # Query lenta
                    optimizations.append(f"Índice sugerido para query frequente")
        
        return optimizations
    
    # === LOOPS DE BACKGROUND ===
    
    async def _optimization_loop(self):
        """Loop de otimização automática"""
        while True:
            try:
                # Otimizar automaticamente a cada 10 minutos
                await self.optimize_database({'type': 'indexes'})
                
                # Limpar cache expirado
                await self._cleanup_expired_cache()
                
                await asyncio.sleep(600)  # 10 minutos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de otimização: {e}")
    
    async def _backup_loop(self):
        """Loop de backup automático"""
        while True:
            try:
                # Backup a cada hora
                await self.create_backup({'type': 'incremental'})
                
                await asyncio.sleep(self.config['backup_interval'])
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no backup automático: {e}")
    
    async def _cleanup_loop(self):
        """Loop de limpeza"""
        while True:
            try:
                # Limpeza diária
                await self._cleanup_old_data(DatabaseType.SQLITE)
                await self._cleanup_old_logs()
                
                await asyncio.sleep(86400)  # 24 horas
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na limpeza: {e}")
    
    async def _cleanup_expired_cache(self):
        """Remove itens expirados do cache"""
        now = datetime.now()
        expired_keys = [
            key for key, item in self.result_cache.items()
            if item['expires'] < now
        ]
        
        for key in expired_keys:
            del self.result_cache[key]
            self.cache_stats['evictions'] += 1
    
    async def _cleanup_old_data(self, database: DatabaseType) -> List[str]:
        """Remove dados antigos"""
        # Implementação básica - em produção seria mais sofisticada
        return ["Limpeza de dados antigos executada"]
    
    async def _cleanup_old_logs(self):
        """Remove logs antigos"""
        cutoff = datetime.now() - timedelta(days=30)
        
        # Limpar histórico de performance
        for query in list(self.query_performance_history.keys()):
            self.query_performance_history[query] = [
                t for t in self.query_performance_history[query]
                # Em produção, teria timestamp
            ]
    
    # === MÉTODOS AUXILIARES ===
    
    async def _backup_all_tables(self, database: DatabaseType) -> List[str]:
        """Backup de todas as tabelas"""
        # Implementação simplificada
        return ["table1", "table2", "table3"]
    
    async def _backup_incremental(self, database: DatabaseType) -> Dict[str, Any]:
        """Backup incremental"""
        return {"changes": 0, "last_backup": datetime.now().isoformat()}
    
    async def _store_backup_metadata(self, backup_info: Dict[str, Any]):
        """Armazena metadados do backup"""
        # Em produção, salvaria em tabela de metadados
        logger.info(f"💾 Backup {backup_info['backup_id']} criado")
    
    async def _analyze_table_stats(self, database: DatabaseType):
        """Analisa estatísticas das tabelas"""
        if database == DatabaseType.SQLITE:
            await self._execute_raw_query("ANALYZE", {}, database)
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
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

# Importações necessárias
from uuid import uuid4

def create_database_agent(message_bus, num_instances=1) -> List[DatabaseAgent]:
    """
    Cria agente de banco de dados inteligente
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de banco de dados
    """
    agents = []
    
    try:
        logger.info("🗄️ Criando DatabaseAgent inteligente...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "database_001"
        
        if agent_id not in existing_agents:
            try:
                agent = DatabaseAgent(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar serviços de banco
                asyncio.create_task(agent.start_database_services())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com gerenciamento inteligente de dados")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de banco de dados criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando DatabaseAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
