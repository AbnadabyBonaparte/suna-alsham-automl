#!/usr/bin/env python3
"""
Módulo do Database Agent - SUNA-ALSHAM
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
import os # Import adicionado

# Usaremos SQLAlchemy para o bootstrap para aproveitar a DATABASE_URL
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Classe Principal do Agente ---

class DatabaseAgent(BaseNetworkAgent):
    """
    Agente de banco de dados com otimização automática.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DatabaseAgent."""
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend(["data_management", "query_execution"])
        self.db_engine = None
        
        # Inicia a tarefa de bootstrap e inicialização
        self._db_init_task = asyncio.create_task(self._initialize_database_and_bootstrap())
        
        logger.info(f"🗄️ {self.agent_id} (Banco de Dados) inicializado.")

    async def _initialize_database_and_bootstrap(self):
        """Inicializa a conexão e executa o script de bootstrap UMA VEZ."""
        db_url = os.environ.get("DATABASE_URL")
        if not db_url:
            logger.critical("DATABASE_URL não configurada. DatabaseAgent em modo degradado.")
            self.status = "degraded"
            return

        try:
            # SQLAlchemy lida com diferentes dialetos de SQL (Postgres, etc)
            engine = create_engine(db_url)
            with engine.connect() as connection:
                logger.info("✅ Conexão com o banco de dados estabelecida.")
                
                # --- MISSÃO DE BOOTSTRAP ---
                logger.info("Executando script de bootstrap da tabela 'knowledge_base'...")
                bootstrap_script = """
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    article_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT
                );
                
                -- Inserindo artigos de exemplo (só serão inseridos se não existirem)
                INSERT INTO knowledge_base (article_id, title, content, tags) VALUES
                ('KB001', 'Como resetar sua senha', 'Para resetar sua senha, vá até a página de login e clique em "Esqueci minha senha". Você receberá um e-mail com as instruções.', 'password_reset,account')
                ON CONFLICT (article_id) DO NOTHING;

                INSERT INTO knowledge_base (article_id, title, content, tags) VALUES
                ('KB002', 'Como atualizar informações de pagamento', 'Para atualizar seu cartão de crédito, acesse seu perfil, clique em "Faturamento" e depois em "Atualizar Pagamento".', 'billing_question,payment')
                ON CONFLICT (article_id) DO NOTHING;
                """
                connection.execute(text(bootstrap_script))
                # Para SQLAlchemy < 2.0, pode ser necessário connection.commit()
                if hasattr(connection, 'commit'):
                    connection.commit()

                logger.info("✅ Script de bootstrap executado com sucesso.")
                # -------------------------

            self.db_engine = engine
            self.status = "active"

        except Exception as e:
            logger.critical(f"❌ Falha catastrófica ao conectar/bootstrap do banco de dados: {e}", exc_info=True)
            self.status = "error"

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições relacionadas ao banco de dados."""
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "execute_query":
            result = await self.execute_query(message.content)
            await self.publish_response(message, result)

    async def execute_query(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa uma query SQL de forma segura no banco de dados."""
        if self.status != "active" or not self.db_engine:
            return {"status": "error", "message": "Serviço de banco de dados indisponível."}
        
        query = request_data.get("query")
        params = request_data.get("params", [])
        
        try:
            with self.db_engine.connect() as connection:
                result = connection.execute(text(query), params)
                if query.strip().upper().startswith("SELECT"):
                    data = [dict(row._mapping) for row in result]
                    return {"status": "completed", "data": data}
                else:
                    if hasattr(connection, 'commit'):
                        connection.commit()
                    return {"status": "completed", "rows_affected": result.rowcount}
        except Exception as e:
            logger.error(f"❌ Erro ao executar query: {e}", exc_info=True)
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
