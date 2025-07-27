#!/usr/bin/env python3
"""
Módulo do Code Corrector Agent - SUNA-ALSHAM

Define o agente especializado em aplicar correções automáticas de código,
incluindo formatação, refatoração e patches de segurança.
"""

import asyncio
import logging
import shutil
import difflib
import ast
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

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

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
            "backup_management",
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
                await self.message_bus.publish(self.create_response(message, result))
            else:
                logger.warning(f"Ação de correção desconhecida: {request_type}")
                await self.message_bus.publish(self.create_error_response(message, "Ação de correção desconhecida"))

    async def format_code(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formata um arquivo de código usando ferramentas como Black e isort.

        Args:
            request_data: Dicionário contendo 'file_path' e 'formatters'.

        Returns:
            Um dicionário com o resultado da formatação.
        """
        if self.status != "active":
            return {"status": "error", "message": "Serviço de correção indisponível (dependências faltando)."}
            
        file_path_str = request_data.get("file_path")
        formatters = request_data.get("formatters", ["isort", "black"])
        
        if not file_path_str or not Path(file_path_str).exists():
            return {"status": "error", "message": f"Arquivo não encontrado: {file_path_str}"}
        
        file_path = Path(file_path_str)
        logger.info(f"🎨 Formatando código em: {file_path}")

        try:
            # 1. Criar backup antes de qualquer modificação
            backup_path = self._create_backup(file_path)

            # 2. Ler o código original
            with open(file_path, "r", encoding="utf-8") as f:
                original_code = f.read()
            
            # 3. Aplicar formatadores em sequência
            formatted_code = original_code
            for formatter_name in formatters:
                if formatter_name == "isort":
                    formatted_code = isort.code(formatted_code)
                elif formatter_name == "black":
                    formatted_code = black.format_str(formatted_code, mode=black.Mode())
            
            # 4. Validar e Salvar
            if self._validate_syntax(formatted_code):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(formatted_code)
                
                lines_changed = self._count_changed_lines(original_code, formatted_code)
                
                return {
                    "status": "completed",
                    "file_path": str(file_path),
                    "lines_changed": lines_changed,
                    "backup_path": str(backup_path),
                }
            else:
                # 5. Rollback em caso de falha
                self._restore_backup(file_path, backup_path)
                return {
                    "status": "failed",
                    "message": "Formatação resultou em sintaxe inválida. Rollback executado.",
                }
        except Exception as e:
            logger.error(f"❌ Erro ao formatar código: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    def _create_backup(self, file_path: Path) -> Path:
        """Cria um backup seguro de um arquivo antes de modificá-lo."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file_path = self.backup_directory / f"{file_path.name}.{timestamp}.bak"
        shutil.copy2(file_path, backup_file_path)
        logger.info(f"  -> Backup criado em: {backup_file_path}")
        return backup_file_path

    def _restore_backup(self, file_path: Path, backup_path: Path):
        """Restaura um arquivo a partir de um backup."""
        shutil.copy2(backup_path, file_path)
        logger.warning(f"  -> Rollback: Arquivo restaurado de {backup_path}")

    def _validate_syntax(self, code: str) -> bool:
        """Valida se a sintaxe do código Python é válida."""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    def _count_changed_lines(self, original: str, corrected: str) -> int:
        """Conta o número de linhas que foram de fato alteradas."""
        diff = difflib.unified_diff(
            original.splitlines(), corrected.splitlines(), lineterm=""
        )
        # Contar apenas as linhas que começam com '+' ou '-'
        return sum(1 for line in diff if line.startswith(("+ ", "- ")))


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
