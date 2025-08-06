#!/usr/bin/env python3
"""
Módulo do Debug Master Agent - O Agente de Debug Supremo do SUNA-ALSHAM.
"""

import asyncio
import logging
import sys
import traceback
import time
import re
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
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


# --- Enums e Dataclasses ---

class IssueCategory(Enum):
    RUNTIME_ERROR = "runtime_error"
    LOGIC_ERROR = "logic_error"
    PERFORMANCE_ISSUE = "performance_issue"
    MEMORY_LEAK = "memory_leak"
    DEPENDENCY_ISSUE = "dependency_issue"


class ResolutionStrategy(Enum):
    AUTO_FIX = "auto_fix"
    GUIDED_FIX = "guided_fix"
    MANUAL_INTERVENTION = "manual_intervention"


@dataclass
class DebugIssue:
    issue_id: str
    category: IssueCategory
    title: str
    description: str
    location: Dict[str, Any]
    stack_trace: Optional[str]
    suggested_fixes: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


# --- Classe Principal do Agente ---

class DebugMasterAgent(BaseNetworkAgent):
    """
    Agente supremo de debugging e diagnóstico.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DebugMasterAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "error_detection",
            "automatic_debugging",
            "issue_diagnosis",
        ])
        
        self.issue_database = deque(maxlen=1000)
        self._setup_exception_hook()
        logger.info(f"🐛 {self.agent_id} (Debug Master) inicializado.")

    def _setup_exception_hook(self):
        """Configura um hook global para capturar exceções não tratadas."""
        original_hook = sys.excepthook

        def exception_handler(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, (KeyboardInterrupt, SystemExit)):
                original_hook(exc_type, exc_value, exc_traceback)
                return

            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            full_traceback = "".join(tb_lines)

            asyncio.create_task(
                self._process_uncaught_exception(exc_type, exc_value, full_traceback)
            )

        sys.excepthook = exception_handler
        logger.info("  -> Hook de exceções global instalado.")

    async def _process_uncaught_exception(self, exc_type, exc_value, full_traceback: str):
        issue = DebugIssue(
            issue_id=f"issue_{int(time.time())}",
            category=IssueCategory.RUNTIME_ERROR,
            title=f"Exceção não tratada: {exc_type.__name__}",
            description=str(exc_value),
            location=self._extract_location_from_stack(full_traceback),
            stack_trace=full_traceback,
        )
        self.issue_database.append(issue)
        await self._notify_critical_issue(issue)

    async def _notify_critical_issue(self, issue: DebugIssue):
        """Notifica o orquestrador sobre um problema crítico."""
        notification_content = { "issue_id": issue.issue_id, "title": issue.title }
        notification = self.create_message(
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.CRITICAL,
            content=notification_content,
        )
        await self.message_bus.publish(notification)

    def _extract_location_from_stack(self, stack_trace: str) -> Dict[str, Any]:
        """Extrai a localização (arquivo, linha) do topo do stack trace."""
        try:
            match = re.search(r'File "(.+)", line (\d+), in (.+)', stack_trace)
            if match:
                return { "file": match.group(1), "line": int(match.group(2)), "function": match.group(3) }
        except Exception:
            pass
        return {"file": "unknown", "line": 0, "function": "unknown"}


def create_debug_master_agent(message_bus: Any) -> List[BaseNetworkAgent]:
    """
    Factory function to create and initialize the DebugMasterAgent(s) for the ALSHAM QUANTUM system.

    This function instantiates the DebugMasterAgent, logs all relevant events for diagnostics,
    and returns it in a list for registration in the agent registry. Handles errors robustly
    and ensures the agent is ready for operation.

    Args:
        message_bus (Any): The message bus or communication channel for agent messaging.

    Returns:
        List[BaseNetworkAgent]: A list containing the initialized DebugMasterAgent instance(s).
    """
    agents: List[BaseNetworkAgent] = []
    logger.info("🐛 [Factory] Criando DebugMasterAgent...")
    try:
        agent = DebugMasterAgent("debug_master_001", message_bus)
        agents.append(agent)
        logger.info(f"🐛 DebugMasterAgent criado com sucesso: {agent.agent_id}")
    except Exception as e:
        logger.critical(f"❌ Erro crítico ao criar DebugMasterAgent: {e}", exc_info=True)
    return agents
