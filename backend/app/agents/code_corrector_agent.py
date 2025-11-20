#!/usr/bin/env python3
"""
Módulo do Code Corrector Agent - SUNA-ALSHAM
"""

import logging
import shutil
import difflib
import ast
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import black
    import isort
    FORMATTERS_AVAILABLE = True
except ImportError:
    FORMATTERS_AVAILABLE = False

# --- Bloco de Importação Corrigido e Padronizado ---
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

class CorrectionType(Enum):
    STYLE_FORMAT = "style_format"
    SECURITY_PATCH = "security_patch"
    REFACTORING = "refactoring"

@dataclass
class CorrectionResult:
    file_path: str
    success: bool
    lines_changed: int
    backup_path: Optional[str] = None
    error_message: Optional[str] = None

class CodeCorrectorAgent(BaseNetworkAgent):
    """
    Agente que atua com base nas análises do CodeAnalyzerAgent para aplicar
    correções automáticas no código-fonte do sistema.
    """
    def __init__(self, agent_id: str, message_bus):
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
        """Processa requisições para correção de código."""
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            handler = {
                "format_code": self.format_code,
            }.get(request_type)
            if handler:
                result = await handler(message.content)
                await self.publish_response(message, result)
            else:
                await self.publish_error_response(message, "Ação de correção desconhecida")

    async def format_code(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formata um arquivo de código usando ferramentas como Black e isort."""
        if self.status != "active":
            return {"status": "error", "message": "Serviço de correção indisponível."}
            
        file_path_str = request_data.get("file_path")
        if not file_path_str or not Path(file_path_str).exists():
            return {"status": "error", "message": f"Arquivo não encontrado: {file_path_str}"}
        
        file_path = Path(file_path_str)
        try:
            backup_path = self._create_backup(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                original_code = f.read()
            
            formatted_code = isort.code(original_code)
            formatted_code = black.format_str(formatted_code, mode=black.Mode())
            
            if self._validate_syntax(formatted_code):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(formatted_code)
                lines_changed = self._count_changed_lines(original_code, formatted_code)
                return {"status": "completed", "lines_changed": lines_changed}
            else:
                self._restore_backup(file_path, backup_path)
                return {"status": "failed", "message": "Formatação resultou em sintaxe inválida."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _create_backup(self, file_path: Path) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file_path = self.backup_directory / f"{file_path.name}.{timestamp}.bak"
        shutil.copy2(file_path, backup_file_path)
        return backup_file_path

    def _restore_backup(self, file_path: Path, backup_path: Path):
        shutil.copy2(backup_path, file_path)

    def _validate_syntax(self, code: str) -> bool:
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    def _count_changed_lines(self, original: str, corrected: str) -> int:
        diff = difflib.unified_diff(original.splitlines(), corrected.splitlines(), lineterm="")
        return sum(1 for line in diff if line.startswith(("+ ", "- ")))


def create_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Factory function padrão para integração com agent_loader.
    Cria e retorna todos os agentes Code Corrector deste módulo.
    """
    agents: List[BaseNetworkAgent] = []
    logger.info("🔧 Criando CodeCorrectorAgent...")
    try:
        agent = CodeCorrectorAgent("code_corrector_001", message_bus)
        agents.append(agent)
        logger.info(f"🔧 CodeCorrectorAgent criado com sucesso: {agent.agent_id}")
    except Exception as e:
        logger.critical(f"❌ Erro crítico ao criar CodeCorrectorAgent: {e}", exc_info=True)
    return agents
