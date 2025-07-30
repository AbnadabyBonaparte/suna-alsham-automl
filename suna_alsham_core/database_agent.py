#!/usr/bin/env python3
"""
Módulo do Database Agent - SUNA-ALSHAM
"""

import asyncio
import logging
import os
from typing import Any, Dict, List

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

class DatabaseAgent(BaseNetworkAgent):
    """
    Agente de banco de dados com otimização automática.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend(["data_management", "query_execution"])
        self.db_engine = None
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
            engine = create_engine(db_url)
            with engine.connect() as connection:
                trans = connection.begin()
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

                INSERT INTO knowledge_base (article_id, title, content, tags) VALUES
                ('KB001', 'Como resetar sua senha', 'Para resetar sua senha, vá até a página de login e clique em "Esqueci minha senha". Você receberá um e-mail com as instruções.', 'password_reset,account')
                ON CONFLICT (article_id) DO NOTHING;

                INSERT INTO knowledge_base (article_id, title, content, tags) VALUES
                ('KB002', 'Como atualizar informações de pagamento', 'Para atualizar seu cartão de crédito, acesse seu perfil, clique em "Faturamento" e depois em "Atualizar Pagamento".', 'billing_question,payment')
                ON CONFLICT (article_id) DO NOTHING;
                """
                
                # --- CORREÇÃO APLICADA AQUI ---
                # "Fatia" o script em comandos individuais e os executa um por um.
                statements = [s.strip() for s in bootstrap_script.split(';') if s.strip()]
                for statement in statements:
                    connection.execute(text(statement))
                
                trans.commit()
                logger.info("✅ Script de bootstrap executado com sucesso.")
                # -------------------------

            self.db_engine = engine
            self.status = "active"

        except Exception as e:
            logger.critical(f"❌ Falha catastrófica ao conectar/bootstrap do banco de dados: {e}", exc_info=True)
            self.status = "error"
            
    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "execute_query":
            result = await self.execute_query(message.content)
            await self.publish_response(message, result)

    async def execute_query(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        # ... (resto da função permanece o mesmo) ...
        pass

def create_database_agent(message_bus) -> List[BaseNetworkAgent]:
    agents = []
    logger.info("🗄️ Criando DatabaseAgent...")
    try:
        agent = DatabaseAgent("database_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando DatabaseAgent: {e}", exc_info=True)
    return agents
