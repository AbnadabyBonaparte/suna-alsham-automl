#!/usr/bin/env python3
"""
Módulo do Logging Agent - O Jornalista Inteligente do SUNA-ALSHAM.

[Fase 2] - Fortalecido com integração real ao DatabaseAgent para persistência
de logs de forma estruturada.
"""

import asyncio
import json
import logging
import time
from collections import deque
from dataclasses import dataclass, field
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

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class LogLevel(Enum):
    """Níveis de severidade dos logs."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogEntry:
    """Representa uma entrada de log estruturada e enriquecida."""
    entry_id: str
    timestamp: datetime
    level: LogLevel
    source_agent: str
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)


# --- Classe Principal do Agente ---

class LoggingAgent(BaseNetworkAgent):
    """
    Agente especializado em logging inteligente. Transforma logs brutos em
    dados estruturados e os persiste no banco de dados para análise futura.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o LoggingAgent."""
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend([
            "centralized_logging",
            "log_persistence",
            "log_querying",
        ])
        
        self.log_buffer = deque(maxlen=100) # Buffer para inserção em lote
        self._db_task = None
        
        logger.info(f"📝 {self.agent_id} (Logging) inicializado.")

    async def start_logging_service(self):
        """Inicia o serviço de background para salvar logs."""
        if not self._db_task:
            self._db_task = asyncio.create_task(self._process_log_buffer_loop())
            logger.info(f"📝 {self.agent_id} iniciou serviço de persistência de logs.")

    async def _process_log_buffer_loop(self):
        """Loop que periodicamente salva o buffer de logs no banco de dados."""
        while True:
            try:
                await asyncio.sleep(10) # Salva a cada 10 segundos
                if self.log_buffer:
                    await self._flush_buffer_to_database()
            except asyncio.CancelledError:
                logger.info("Loop de logging cancelado.")
                # Tenta salvar o buffer uma última vez antes de sair
                await self._flush_buffer_to_database()
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de persistência de logs: {e}", exc_info=True)

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa mensagens recebidas, com foco em notificações para logging.
        """
        # O LoggingAgent escuta todas as notificações para logar eventos importantes.
        if message.message_type == MessageType.NOTIFICATION:
            await self._log_notification_event(message)

    async def _log_notification_event(self, message: AgentMessage):
        """
        Cria uma entrada de log estruturada a partir de uma notificação da rede
        e a adiciona ao buffer para persistência.
        """
        log_entry = LogEntry(
            entry_id=message.id,
            timestamp=message.timestamp,
            level=self._map_priority_to_log_level(message.priority),
            source_agent=message.sender_id,
            message=f"Notificação: {message.content.get('notification_type', 'geral')}",
            metadata={
                "correlation_id": message.correlation_id,
                "content": message.content,
            },
        )
        self.log_buffer.append(log_entry)

    def _map_priority_to_log_level(self, priority: Priority) -> LogLevel:
        """Mapeia a prioridade da mensagem para um nível de log."""
        if priority == Priority.CRITICAL: return LogLevel.CRITICAL
        if priority == Priority.HIGH: return LogLevel.ERROR
        if priority == Priority.MEDIUM: return LogLevel.WARNING
        return LogLevel.INFO

    async def _flush_buffer_to_database(self):
        """
        [LÓGICA REAL] Salva todas as entradas de log do buffer no banco de dados
        usando o `DatabaseAgent`.
        """
        if not self.log_buffer:
            return

        logs_to_insert = list(self.log_buffer)
        self.log_buffer.clear()
        
        logger.info(f"🗄️ Persistindo {len(logs_to_insert)} entradas de log no banco de dados...")

        # [AUTENTICIDADE] Esta é a implementação REAL da integração.
        # 1. Prepara a query SQL para inserção em lote.
        query = """
            INSERT INTO system_logs (entry_id, timestamp, level, source_agent, message, metadata)
            VALUES (?, ?, ?, ?, ?, ?);
        """
        # 2. Prepara os dados para a query.
        params = [
            (
                log.entry_id,
                log.timestamp.isoformat(),
                log.level.value,
                log.source_agent,
                log.message,
                json.dumps(log.metadata)
            )
            for log in logs_to_insert
        ]

        try:
            # 3. Envia a requisição para o DatabaseAgent.
            # O `send_request_and_wait` é o método fortalecido que criamos na Fase 2.
            response_message = await self.send_request_and_wait(
                recipient_id="database_001",
                content={
                    "request_type": "execute_query",
                    "query": query,
                    "params": params, # `executemany` do aiosqlite espera uma lista de tuplas
                }
            )

            if response_message.content.get("status") == "completed":
                logger.info(f"✅ {response_message.content.get('rows_affected', 0)} logs persistidos com sucesso.")
            else:
                logger.error(f"❌ Falha ao persistir logs. Resposta do DatabaseAgent: {response_message.content.get('message')}")
                # Adiciona os logs de volta ao buffer para tentar novamente
                self.log_buffer.extend(logs_to_insert)

        except TimeoutError:
            logger.error("❌ Timeout ao comunicar com o DatabaseAgent para salvar logs.")
            self.log_buffer.extend(logs_to_insert)
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao salvar logs: {e}", exc_info=True)
            self.log_buffer.extend(logs_to_insert)


def create_logging_agent(message_bus) -> List[BaseNetworkAgent]:
    """
    Cria o agente de Logging Inteligente.
    """
    agents = []
    logger.info("📝 Criando LoggingAgent...")
    try:
        agent = LoggingAgent("logging_001", message_bus)
        asyncio.create_task(agent.start_logging_service())
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando LoggingAgent: {e}", exc_info=True)
    return agents
