#!/usr/bin/env python3
"""
Módulo do Database Agent - SUNA-ALSHAM

[Fase 2] - Fortalecido com lógica de execução de queries aprimorada,
melhor tratamento de erros e preparação para otimizações reais.
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

# [AUTENTICIDADE] As bibliotecas de banco de dados serão importadas
# condicionalmente para permitir que o agente funcione em modo de fallback.
try:
    import aiosqlite
except ImportError:
    aiosqlite = None

# --- Bloco de Importação Corrigido e Padronizado ---
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class DatabaseType(Enum):
    """Tipos de banco de dados suportados."""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MEMORY = "memory"


# --- Classe Principal do Agente ---

class DatabaseAgent(BaseNetworkAgent):
    """
    Agente de banco de dados com otimização automática.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DatabaseAgent."""
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend([
            "data_management",
            "query_execution",
            "intelligent_caching",
        ])

        self.connections: Dict[DatabaseType, Any] = {}
        self.db_path = "./suna_local_database.db"
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
            logger.info(f"✅ Conexão com o banco de dados local SQLite estabelecida: {self.db_path}")
        except Exception as e:
            logger.critical(f"❌ Falha catastrófica ao conectar ao banco de dados: {e}", exc_info=True)
            self.status = "error"

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições relacionadas ao banco de dados."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        handler = {
            "execute_query": self.execute_query,
        }.get(request_type)

        if handler:
            result = await handler(message.content)
            await self.publish_response(message, result)
        else:
            logger.warning(f"Ação de banco de dados desconhecida: {request_type}")
            await self.publish_error_response(message, "Ação de banco de dados desconhecida")

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
            conn = self.connections.get(DatabaseType.SQLITE)
            if not conn:
                return {"status": "error", "message": "Conexão com banco de dados não está ativa."}

            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                
                if query.strip().upper().startswith("SELECT"):
                    rows = await cursor.fetchall()
                    return {"status": "completed", "data": [tuple(row) for row in rows], "rows_affected": len(rows)}
                else:
                    await conn.commit()
                    return {"status": "completed", "rows_affected": cursor.rowcount}
        except Exception as e:
            logger.error(f"❌ Erro ao executar query: '{query[:100]}...' | Erro: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}


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
