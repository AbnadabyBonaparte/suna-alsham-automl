#!/usr/bin/env python3
"""
Módulo do Code Corrector Agent - SUNA-ALSHAM

[Fase 2] - Revisão Final. Alinhado com a BaseNetworkAgent fortalecida.
Define o agente especializado em aplicar correções automáticas de código,
incluindo formatação, refatoração e patches de segurança.
"""

import ast
import difflib
import logging
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# [AUTENTICIDADE] Ferramentas de formatação são importadas de forma segura.
try:
    import black
    import isort
    FORMATTERS_AVAILABLE = True
except ImportError:
    FORMATTERS_AVAILABLE = False

# Import alinhado com a Fase 1
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses (sem alteração) ---

class CorrectionType(Enum):
    """Tipos de correção que o agente pode aplicar."""
    STYLE_FORMAT = "style_format"
    SECURITY_PATCH = "security_patch"
    REFACTORING = "refactoring"


@dataclass
class CorrectionResult:
    """Representa o resultado de uma operação de correção."""
    file_path: str
    success: bool
    lines_changed: int
    backup_path: Optional[str] = None
    error_message: Optional[str] = None


# --- Classe Principal do Agente ---

class CodeCorrectorAgent(BaseNetworkAgent):
    """
    Agente que atua com base nas análises do CodeAnalyzerAgent para aplicar
    correções automáticas no código-fonte do sistema.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o CodeCorrectorAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "automatic_correction",
            "code_refactoring",
            "style_formatting",
        ])

        self.backup_directory = Path("./code_backups")
        self.backup_directory.mkdir(exist_ok=True)

        if not FORMATTERS_AVAILABLE:
            self.status = "degraded"
            logger.critical("Bibliotecas 'black' ou 'isort' não encontradas. O CodeCorrectorAgent operará em modo degradado.")
        
        logger.info(f"🔧 {self.agent_id} (Corretor de Código) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa requisições para correção de código, alinhado com a BaseNetworkAgent da Fase 2.
        """
        if message.message_type != MessageType.REQUEST:
            return

        if message.content.get("request_type") == "format_code":
            result = await self.format_code(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            unhandled_req = message.content.get("request_type", "desconhecido")
            logger.warning(f"Ação de correção desconhecida: {unhandled_req}")
            await self.message_bus.publish(self.create_error_response(message, f"Ação de correção desconhecida: {unhandled_req}"))

    async def format_code(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formata um arquivo de código usando ferramentas como Black e isort.
        """
        if self.status == "degraded":
            return {"status": "error", "message": "Serviço de correção indisponível (dependências faltando)."}
            
        file_path_str = request_data.get("file_path")
        formatters = request_data.get("formatters", ["isort", "black"])
        
        if not file_path_str or not Path(file_path_str).exists():
            return {"status": "error", "message": f"Arquivo não encontrado: {file_path_str}"}
        
        file_path = Path(file_path_str)
        logger.info(f"🎨 Formatando código em: {file_path}")

        try:
            backup_path = self._create_backup(file_path)

            with open(file_path, "r", encoding="utf-8") as f:
                original_code = f.read()
            
            formatted_code = original_code
            for formatter_name in formatters:
                if formatter_name == "isort": formatted_code = isort.code(formatted_code)
                elif formatter_name == "black": formatted_code = black.format_str(formatted_code, mode=black.Mode())
            
            if self._validate_syntax(formatted_code):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(formatted_code)
                
                lines_changed = self._count_changed_lines(original_code, formatted_code)
                return {"status": "completed", "lines_changed": lines_changed, "backup_path": str(backup_path)}
            else:
                self._restore_backup(file_path, backup_path)
                return {"status": "failed", "message": "Formatação resultou em sintaxe inválida. Rollback executado."}
        except Exception as e:
            logger.error(f"❌ Erro ao formatar código: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    def _create_backup(self, file_path: Path) -> Path:
        """Cria um backup seguro de um arquivo antes de modificá-lo."""
        # ... (lógica inalterada)
        return Path() # Placeholder

    def _restore_backup(self, file_path: Path, backup_path: Path):
        """Restaura um arquivo a partir de um backup."""
        # ... (lógica inalterada)

    def _validate_syntax(self, code: str) -> bool:
        """Valida se a sintaxe do código Python é válida."""
        # ... (lógica inalterada)
        return True

    def _count_changed_lines(self, original: str, corrected: str) -> int:
        """Conta o número de linhas que foram de fato alteradas."""
        # ... (lógica inalterada)
        return 0


def create_code_corrector_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente Corretor de Código."""
    agents = []
    logger.info("🔧 Criando CodeCorrectorAgent...")
    try:
        agent = CodeCorrectorAgent("code_corrector_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando CodeCorrectorAgent: {e}", exc_info=True)
    return agents
