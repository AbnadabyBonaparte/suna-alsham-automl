#!/usr/bin/env python3
"""
Módulo do Code Analyzer Agent - SUNA-ALSHAM

Define o agente de análise estática de código, responsável por inspecionar o
código-fonte em busca de problemas de sintaxe, estilo, complexidade e segurança.
"""

import ast
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
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

class CodeIssueType(Enum):
    """Tipos de problemas de código que o agente pode detectar."""
    SYNTAX_ERROR = "syntax_error"
    STYLE_VIOLATION = "style_violation"
    COMPLEXITY = "complexity"
    SECURITY = "security"
    PERFORMANCE = "performance"


class SeverityLevel(Enum):
    """Níveis de severidade dos problemas encontrados."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class CodeIssue:
    """Representa um problema individual encontrado no código."""
    file_path: str
    line_number: int
    issue_type: CodeIssueType
    severity: SeverityLevel
    message: str
    suggestion: str


# --- Classe Principal do Agente ---

class CodeAnalyzerAgent(BaseNetworkAgent):
    """
    Agente especializado em análise de código. Utiliza AST (Abstract Syntax Tree)
    para uma análise profunda e estrutural do código-fonte.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o CodeAnalyzerAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "code_analysis",
            "complexity_analysis",
            "security_scanning",
            "style_checking",
        ])
        
        self.max_complexity_threshold = 10 # Limite de complexidade ciclomática
        logger.info(f"🔍 {self.agent_id} (Analisador de Código) inicializado.")

    async def handle_message(self, message: AgentMessage):
        """Processa requisições de análise de código."""
        await super().handle_message(message)
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            if request_type == "analyze_file":
                result = await self.analyze_file(message.content)
                await self.message_bus.publish(self.create_response(message, result))
            else:
                logger.warning(f"Ação de análise desconhecida: {request_type}")

    async def analyze_file(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa um único arquivo de código Python.

        Args:
            request_data: Dicionário contendo o 'file_path' a ser analisado.

        Returns:
            Um dicionário com o relatório da análise.
        """
        file_path = request_data.get("file_path")
        if not file_path or not Path(file_path).exists():
            return {"status": "error", "message": f"Arquivo não encontrado: {file_path}"}

        logger.info(f"🔍 Analisando arquivo: {file_path}")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            
            tree = ast.parse(code, filename=file_path)
            
            # Executa as várias análises
            complexity_issues = self._analyze_complexity(tree, file_path)
            security_issues = self._analyze_security(code, file_path)
            
            all_issues = complexity_issues + security_issues
            
            health_score = self._calculate_health_score(all_issues, code)

            return {
                "status": "completed",
                "file_path": file_path,
                "issues_found": len(all_issues),
                "health_score": health_score,
                "issues": [issue.__dict__ for issue in all_issues],
            }

        except SyntaxError as e:
            logger.error(f"❌ Erro de sintaxe em {file_path}: {e}")
            return {"status": "error", "message": f"Erro de sintaxe na linha {e.lineno}: {e.msg}"}
        except Exception as e:
            logger.error(f"❌ Erro ao analisar arquivo {file_path}: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    def _analyze_complexity(self, tree: ast.AST, file_path: str) -> List[CodeIssue]:
        """Analisa a complexidade ciclomática do código."""
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_cyclomatic_complexity(node)
                if complexity > self.max_complexity_threshold:
                    issues.append(
                        CodeIssue(
                            file_path=file_path,
                            line_number=node.lineno,
                            issue_type=CodeIssueType.COMPLEXITY,
                            severity=SeverityLevel.HIGH,
                            message=f"Função '{node.name}' tem complexidade ciclomática alta ({complexity}).",
                            suggestion=f"Refatore a função para reduzir sua complexidade (limite: {self.max_complexity_threshold})."
                        )
                    )
        return issues

    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calcula a complexidade ciclomática de uma função."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.BoolOp)):
                complexity += 1
        return complexity

    def _analyze_security(self, code: str, file_path: str) -> List[CodeIssue]:
        """Realiza uma varredura de segurança básica no código."""
        issues = []
        security_patterns = {
            "eval_usage": (re.compile(r'\beval\s*\('), SeverityLevel.CRITICAL, "Uso de 'eval' é extremamente perigoso."),
            "exec_usage": (re.compile(r'\bexec\s*\('), SeverityLevel.CRITICAL, "Uso de 'exec' pode levar a execução de código arbitrário."),
            "pickle_usage": (re.compile(r'\bpickle\.load'), SeverityLevel.HIGH, "Deserializar dados com 'pickle' de fontes não confiáveis é inseguro."),
            "shell_true": (re.compile(r'subprocess.*shell\s*=\s*True'), SeverityLevel.HIGH, "Usar 'shell=True' em subprocessos é um risco de shell injection."),
        }

        for name, (pattern, severity, message) in security_patterns.items():
            for match in pattern.finditer(code):
                line_number = code.count('\n', 0, match.start()) + 1
                issues.append(
                    CodeIssue(
                        file_path=file_path,
                        line_number=line_number,
                        issue_type=CodeIssueType.SECURITY,
                        severity=severity,
                        message=message,
                        suggestion="Use alternativas mais seguras (ex: ast.literal_eval, subprocess sem shell=True)."
                    )
                )
        return issues

    def _calculate_health_score(self, issues: List[CodeIssue], code: str) -> float:
        """Calcula um score de saúde para o código de 0 a 100."""
        score = 100.0
        for issue in issues:
            if issue.severity == SeverityLevel.CRITICAL:
                score -= 25
            elif issue.severity == SeverityLevel.HIGH:
                score -= 10
            elif issue.severity == SeverityLevel.MEDIUM:
                score -= 5
            elif issue.severity == SeverityLevel.LOW:
                score -= 2
        return max(0.0, score)


def create_code_analyzer_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente Analisador de Código."""
    agents = []
    logger.info("🔍 Criando CodeAnalyzerAgent...")
    try:
        agent = CodeAnalyzerAgent("code_analyzer_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando CodeAnalyzerAgent: {e}", exc_info=True)
    return agents
