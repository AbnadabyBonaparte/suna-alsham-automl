#!/usr/bin/env python3
"""
Módulo do Agente de Logging - SUNA-ALSHAM

[Fase 2] - Fortalecido com integração com o DatabaseAgent para persistência
de logs estruturados, permitindo análises e auditorias futuras.
"""

import asyncio
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

# --- Bloco de Importação Corrigido e Padronizado ---
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Dataclasses para Tipagem Forte ---

@dataclass
class LogEntry:
    """Representa uma entrada de log estruturada a ser persistida."""
    log_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    source_agent: str = "unknown"
    log_level: str = "INFO"
    message: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)

# --- Classe Principal do Agente ---

class LoggingAgent(BaseNetworkAgent):
    """
    Agente centralizado de logging. Coleta, estrutura e persiste
    logs de todo o sistema para análise e auditoria.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o LoggingAgent."""
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend([
            "structured_logging",
            "log_persistence",
            "log_querying"
        ])
        self.log_queue = asyncio.Queue()
        self.persistence_task = asyncio.create_task(self._persist_logs_loop())
        
        logger.info(f"📝 {self.agent_id} (Logging) inicializado.")

    async def _persist_logs_loop(self):
        """Loop que consome a fila e persiste logs no banco de dados."""
        while True:
            try:
                log_entry: LogEntry = await self.log_queue.get()
                
                # [LÓGICA REAL] Na Fase 3, esta query será otimizada e
                # a lógica de gravação em lote será implementada.
                query = "INSERT INTO system_logs (log_id, timestamp, source_agent, log_level, message, payload) VALUES (?, ?, ?, ?, ?, ?)"
                params = (
                    log_entry.log_id,
                    log_entry.timestamp.isoformat(),
                    log_entry.source_agent,
                    log_entry.log_level,
                    log_entry.message,
                    str(log_entry.payload) # Simplificado para texto
                )

                db_request = self.create_message(
                    recipient_id="database_001",
                    message_type=MessageType.REQUEST,
                    content={"request_type": "execute_query", "query": query, "params": params}
                )
                await self.message_bus.publish(db_request)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Erro no loop de persistência de logs: {e}", exc_info=True)

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Recebe notificações de log de outros agentes e as enfileira.
        """
        if message.message_type == MessageType.NOTIFICATION:
            log_content = message.content
            if "event_type" in log_content: # Filtra para apenas eventos de log
                log_entry = LogEntry(
                    log_id=message.message_id,
                    source_agent=message.sender_id,
                    log_level=log_content.get("log_level", "INFO"),
                    message=log_content.get("message", "Evento de log recebido."),
                    payload=log_content
                )
                await self.log_queue.put(log_entry)

def create_logging_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Logging."""
    agents = []
    logger.info("📝 Criando LoggingAgent...")
    try:
        agent = LoggingAgent("logging_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando LoggingAgent: {e}", exc_info=True)
    return agents
