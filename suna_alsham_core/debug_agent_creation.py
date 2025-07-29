#!/usr/bin/env python3
"""
Módulo do Debug Master Agent - O Agente de Debug Supremo do SUNA-ALSHAM.

Especializado em detecção, diagnóstico e sugestão de correção automática
para problemas em tempo de execução.
"""

import asyncio
import logging
import sys
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
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

class IssueCategory(Enum):
    """Categorias de problemas que o agente pode diagnosticar."""
    RUNTIME_ERROR = "runtime_error"
    LOGIC_ERROR = "logic_error"
    PERFORMANCE_ISSUE = "performance_issue"
    MEMORY_LEAK = "memory_leak"
    DEPENDENCY_ISSUE = "dependency_issue"


class ResolutionStrategy(Enum):
    """Estratégias de resolução sugeridas."""
    AUTO_FIX = "auto_fix"
    GUIDED_FIX = "guided_fix"
    MANUAL_INTERVENTION = "manual_intervention"


@dataclass
class DebugIssue:
    """Representa um problema diagnosticado pelo agente."""
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
    Agente supremo de debugging e diagnóstico. Atua como a primeira linha de
    defesa contra erros inesperados em tempo de execução, fornecendo análises
    detalhadas e sugestões de correção.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DebugMasterAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "error_detection",
            "automatic_debugging",
            "issue_diagnosis",
            "system_monitoring",
        ])
        
        self.issue_database = deque(maxlen=1000)
        self._setup_exception_hook()
        logger.info(f"🐛 {self.agent_id} (Debug Master) inicializado e pronto para depurar.")

    def _setup_exception_hook(self):
        """
        Configura um hook global para capturar exceções não tratadas em todo o sistema.
        Esta é uma capacidade poderosa para diagnóstico em tempo real.
        """
        original_hook = sys.excepthook

        def exception_handler(exc_type, exc_value, exc_traceback):
            """Processa exceções não capturadas e as envia para o agente."""
            if issubclass(exc_type, (KeyboardInterrupt, SystemExit)):
                original_hook(exc_type, exc_value, exc_traceback)
                return

            logger.critical("--- EXCEÇÃO GLOBAL NÃO TRATADA CAPTURADA PELO DEBUG MASTER ---")
            
            # Formata o traceback para análise
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            full_traceback = "".join(tb_lines)

            # Envia a exceção para o loop de eventos do asyncio para ser processada pelo agente
            asyncio.create_task(
                self._process_uncaught_exception(exc_type, exc_value, full_traceback)
            )

        sys.excepthook = exception_handler
        logger.info("  -> Hook de exceções global instalado.")

    async def _process_uncaught_exception(self, exc_type, exc_value, full_traceback: str):
        """Processa uma exceção capturada pelo hook."""
        issue = DebugIssue(
            issue_id=f"issue_{int(time.time())}",
            category=IssueCategory.RUNTIME_ERROR,
            title=f"Exceção não tratada: {exc_type.__name__}",
            description=str(exc_value),
            location=self._extract_location_from_stack(full_traceback),
            stack_trace=full_traceback,
            suggested_fixes=["Analisar stack trace", "Implementar bloco try...except no local da falha."]
        )
        self.issue_database.append(issue)
        await self._notify_critical_issue(issue)

    async def _notify_critical_issue(self, issue: DebugIssue):
        """Notifica o orquestrador sobre um problema crítico."""
        notification_content = {
            "notification_type": "critical_issue_detected",
            "issue_id": issue.issue_id,
            "title": issue.title,
            "location": issue.location,
            "severity": "critical",
        }
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
            # Padrão para encontrar a última chamada de arquivo no traceback
            match = re.search(r'File "(.+)", line (\d+), in (.+)', stack_trace)
            if match:
                return {
                    "file": match.group(1),
                    "line": int(match.group(2)),
                    "function": match.group(3),
                }
        except Exception:
            pass
        return {"file": "unknown", "line": 0, "function": "unknown"}


def create_debug_master_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente Debug Master."""
    agents = []
    logger.info("🐛 Criando DebugMasterAgent...")
    try:
        agent = DebugMasterAgent("debug_master_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando DebugMasterAgent: {e}", exc_info=True)
    return agents
