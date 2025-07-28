#!/usr/bin/env python3
"""
Módulo do Agente Coletor de Dados - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente é especializado em conectar-se a várias fontes de dados
para coletar as informações brutas necessárias para análise. Esta versão
inclui a capacidade real de se conectar a um banco de dados SQL via SQLAlchemy.
"""

import logging
import os
from typing import Any, Dict, List

# Importa as bibliotecas de banco de dados
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

# Importa a classe base e os tipos essenciais do núcleo do sistema
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)

# Carrega a URL do banco de dados do ambiente
DATABASE_URL = os.environ.get("DATABASE_URL")


class DataCollectorAgent(BaseNetworkAgent):
    """
    Agente especialista em coletar dados de fontes diversas, incluindo bancos SQL.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DataCollectorAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "data_collection",
            "sql_database_connection",
            "api_integration",
            "file_parsing",
        ])
        
        self.db_engine = None
        if DATABASE_URL:
            try:
                self.db_engine = create_engine(DATABASE_URL)
                logger.info("Motor de banco de dados inicializado com sucesso.")
            except Exception as e:
                logger.error(f"Falha ao criar o motor de banco de dados: {e}")
                self.status = "degraded"
        else:
            self.status = "degraded"
            logger.critical("A variável de ambiente DATABASE_URL não está configurada!")

        logger.info(f"🚚 Agente Coletor de Dados ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa requisições para coletar dados de uma fonte específica.
        """
        if self.status == "degraded":
            await self.publish_error_response(message, "O serviço de coleta de dados está indisponível (configuração de DB ausente).")
            return

        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "collect_sql_data":
            await self.handle_collect_sql_request(message)

    async def handle_collect_sql_request(self, message: AgentMessage):
        """
        Lida com a lógica de coletar dados de um banco de dados SQL.
        """
        query = message.content.get("query")
        if not query:
            await self.publish_error_response(message, "A query SQL não foi fornecida.")
            return

        logger.info(f"Executando a query: {query[:100]}...")

        try:
            with self.db_engine.connect() as connection:
                # Usando Pandas para executar a query e obter um DataFrame
                df = pd.read_sql_query(sql=text(query), con=connection)
                # Converte o DataFrame para uma lista de dicionários para ser serializável
                collected_data = df.to_dict(orient='records')

            logger.info(f"{len(collected_data)} registros coletados do banco de dados.")
            
            response_content = {
                "status": "completed",
                "source_type": "sql",
                "collected_rows": len(collected_data),
                "data_preview": collected_data[:5] # Envia uma amostra dos dados
            }
            await self.publish_response(message, response_content)

        except SQLAlchemyError as e:
            logger.error(f"Erro de banco de dados ao executar a query: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro de Banco de Dados: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado na coleta de dados: {e}", exc_info=True)
            await self.publish_error_response(message, "Ocorreu um erro interno inesperado na coleta de dados.")
