#!/usr/bin/env python3
"""
Módulo do Database Agent - SUNA-ALSHAM

Define o agente de banco de dados com IA e otimização automática, responsável
por gerenciar a persistência, cache e análise de dados do sistema.
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
)

# [AUTENTICIDADE] As bibliotecas de banco de dados serão importadas
# condicionalmente para permitir que o agente funcione em modo de fallback.
try:
    import aiosqlite
except ImportError:
    aiosqlite = None

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class DatabaseType(Enum):
    """Tipos de banco de dados suportados."""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MEMORY = "memory"


class QueryType(Enum):
    """Tipos de queries que o agente pode executar."""
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"


# --- Classe Principal do Agente ---

class DatabaseAgent(BaseNetworkAgent):
    """
    Agente de banco de dados com otimização automática. Gerencia conexões,
    executa queries de forma segura e fornece uma camada de persistência
    inteligente para todo o sistema.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DatabaseAgent."""
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend([
            "data_management",
            "query_optimization",
            "intelligent_caching",
            "data_analytics",
        ])

        self.connections: Dict[DatabaseType, Any] = {}
        self.db_path = "./suna_database.db"
        self._db_init_task = asyncio.create_task(self._initialize_database())
        
        logger.info(f"🗄️ {self.agent_id} (Banco de Dados) inicializado.")

    async def _initialize_database(self):
        """Inicializa a conexão com o banco de dados de forma assíncrona."""
        if not aiosqlite:
            logger.critical("Biblioteca 'aiosqlite' não encontrada. O DatabaseAgent operará em modo degradado.")
            self.status = "degraded"
            return

        try:
            self.connections[DatabaseType.SQLITE] = await aiosqlite.connect(self.db_path)
            logger.info("✅ Conexão com o banco de dados SQLite estabelecida.")
            # Aqui poderíamos adicionar a criação de tabelas iniciais.
        except Exception as e:
            logger.critical(f"❌ Falha catastrófica ao conectar ao banco de dados: {e}", exc_info=True)
            self.status = "error"

    async def handle_message(self, message: AgentMessage):
        """Processa requisições relacionadas ao banco de dados."""
        await super().handle_message(message)
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            handler = {
                "execute_query": self.execute_query,
                "store_data": self.store_data,
            }.get(request_type)

            if handler:
                result = await handler(message.content)
                await self.message_bus.publish(self.create_response(message, result))
            else:
                logger.warning(f"Ação de banco de dados desconhecida: {request_type}")

    async def execute_query(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa uma query SQL de forma segura no banco de dados.
        """
        query = request_data.get("query")
        params = request_data.get("params", [])
        
        if not query:
            return {"status": "error", "message": "Query não fornecida."}
        if self.status != "active":
            return {"status": "error", "message": "Serviço de banco de dados indisponível."}

        try:
            conn = self.connections[DatabaseType.SQLITE]
            async with conn.execute(query, params) as cursor:
                # Para queries de leitura, retorna os resultados
                if query.strip().upper().startswith("SELECT"):
                    rows = await cursor.fetchall()
                    columns = [description[0] for description in cursor.description]
                    data = [dict(zip(columns, row)) for row in rows]
                    return {"status": "completed", "data": data, "rows_affected": len(data)}
                else:
                    # Para queries de escrita, confirma a transação
                    await conn.commit()
                    return {"status": "completed", "rows_affected": cursor.rowcount}
        except Exception as e:
            logger.error(f"❌ Erro ao executar query: {query} | Erro: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    async def store_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [AUTENTICIDADE] Armazena dados de forma estruturada.
        Na Fase 2, esta função será expandida para criar/atualizar tabelas
        dinamicamente e realizar inserções em lote (bulk inserts).
        """
        table_name = request_data.get("table")
        data = request_data.get("data")
        logger.info(f"[Simulação] Armazenando {len(data)} registros na tabela '{table_name}'.")
        # A lógica real usaria `execute_query` para construir e rodar um INSERT.
        return {"status": "completed_simulated", "records_stored": len(data)}


def create_database_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Banco de Dados Inteligente."""
    agents = []
    logger.info("🗄️ Criando DatabaseAgent...")
    try:
        agent = DatabaseAgent("database_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando DatabaseAgent: {e}", exc_info=True)
    return agents
