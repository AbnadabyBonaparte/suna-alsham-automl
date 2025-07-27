#!/usr/bin/env python3
"""
Módulo do Logging Agent - O Jornalista Inteligente do SUNA-ALSHAM.

Define o agente de logging centralizado, responsável por coletar, analisar,
e enriquecer os logs de todo o sistema para fornecer insights claros.
"""

import asyncio
import hashlib
import json
import logging
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

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
    dados estruturados e insights acionáveis sobre o estado do sistema.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o LoggingAgent."""
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend([
            "centralized_logging",
            "log_parsing",
            "pattern_detection",
            "real_time_analysis",
        ])
        
        self.log_buffer = deque(maxlen=5000)
        self.log_patterns = {} # Armazena padrões de log recorrentes
        
        # [AUTENTICIDADE] Na Fase 2, esta lógica será expandida para se conectar
        # ao DatabaseAgent e persistir os logs de forma estruturada.
        self.log_file_path = Path("./logs/suna_alsham_events.log")
        self.log_file_path.parent.mkdir(exist_ok=True)
        
        logger.info(f"📝 {self.agent_id} (Logging) inicializado.")

    async def handle_message(self, message: AgentMessage):
        """
        Processa mensagens recebidas, com foco em notificações para logging.
        """
        await super().handle_message(message)
        
        # O LoggingAgent pode escutar notificações para logar eventos importantes
        if message.message_type == MessageType.NOTIFICATION:
            await self._log_notification_event(message)

    async def _log_notification_event(self, message: AgentMessage):
        """
        Cria uma entrada de log estruturada a partir de uma notificação da rede.
        """
        log_entry = LogEntry(
            entry_id=f"log_{int(time.time()*1000)}",
            timestamp=datetime.now(),
            level=self._map_priority_to_log_level(message.priority),
            source_agent=message.sender_id,
            message=f"Notificação recebida: {message.content.get('notification_type', 'geral')}",
            metadata={
                "message_id": message.id,
                "correlation_id": message.correlation_id,
                "content_preview": str(message.content)[:200],
            },
        )
        self.log_buffer.append(log_entry)
        await self._write_log_to_file(log_entry)

    def _map_priority_to_log_level(self, priority: Priority) -> LogLevel:
        """Mapeia a prioridade da mensagem para um nível de log."""
        if priority == Priority.CRITICAL:
            return LogLevel.CRITICAL
        elif priority == Priority.HIGH:
            return LogLevel.ERROR
        elif priority == Priority.MEDIUM:
            return LogLevel.WARNING
        else:
            return LogLevel.INFO

    async def _write_log_to_file(self, log_entry: LogEntry):
        """
        Escreve uma entrada de log formatada em um arquivo.
        [AUTENTICIDADE] Esta é uma implementação real de logging em arquivo.
        """
        try:
            # Formato de log claro para leigos
            log_line = (
                f"[{log_entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"[{log_entry.level.value:^8}] "
                f"[{log_entry.source_agent:^25}] "
                f"- {log_entry.message}\n"
            )
            
            # Adiciona metadados se existirem
            if log_entry.metadata:
                meta_str = json.dumps(log_entry.metadata, default=str)
                log_line += f"  └─ METADADOS: {meta_str}\n"

            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception as e:
            logger.error(f"❌ Erro ao escrever no arquivo de log: {e}", exc_info=True)


def create_logging_agent(message_bus) -> List[BaseNetworkAgent]:
    """
    Cria o agente de Logging Inteligente.
    """
    agents = []
    logger.info("📝 Criando LoggingAgent...")
    try:
        agent = LoggingAgent("logging_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando LoggingAgent: {e}", exc_info=True)
    return agents
