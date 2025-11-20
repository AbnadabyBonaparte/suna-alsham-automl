#!/usr/bin/env python3
"""
Structure Analyzer Agent - Analisador de Estruturas do ALSHAM QUANTUM
Agente especializado em análise estrutural de código, arquitetura e dependências.
Versão corrigida com implementação completa do BaseNetworkAgent.
"""

import ast
import os
import re
import logging
import importlib
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path

# Importações corrigidas para compatibilidade
from suna_alsham_core.multi_agent_network import (
    BaseNetworkAgent,
    AgentType,
    MessageType,
    Priority,
    AgentMessage
)

logger = logging.getLogger(__name__)

class AnalysisType(Enum):
    """Tipos de análise estrutural disponíveis."""
    CODE_STRUCTURE = "code_structure"
    DEPENDENCY_ANALYSIS = "dependency_analysis"
    ARCHITECTURE_REVIEW = "architecture_review"
    MODULE_MAPPING = "module_mapping"
    IMPORT_ANALYSIS = "import_analysis"
    COMPLEXITY_ANALYSIS = "complexity_analysis"
    PATTERN_DETECTION = "pattern_detection"

class ComplexityLevel(Enum):
    """Níveis de complexidade estrutural."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class StructuralIssue:
    """Representa um problema estrutural detectado."""
    issue_type: str
    severity: ComplexityLevel
    location: str
    description: str
    suggestions: List[str] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.now)

@dataclass
class ModuleInfo:
    """Informações detalhadas sobre um módulo."""
    name: str
    path: str
    lines_of_code: int
    functions: List[str]
    classes: List[str]
    imports: List[str]
    dependencies: Set[str]
    complexity_score: float
    last_analyzed: datetime = field(default_factory=datetime.now)

@dataclass
class StructuralAnalysis:
    """Resultado de uma análise estrutural completa."""
    analysis_id: str
    analysis_type: AnalysisType
    target_path: str
    modules_analyzed: int
    issues_found: List[StructuralIssue]
    module_info: List[ModuleInfo]
    architecture_score: float
    complexity_score: float
    recommendations: List[str]
    analyzed_at: datetime = field(default_factory=datetime.now)

class StructureAnalyzerAgent(BaseNetworkAgent):
    """
    Agente Analisador de Estrutura do ALSHAM QUANTUM.
    Especializado em análise de código, arquitetura e dependências.
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        
        # Configuração do agente
        self.capabilities.extend([
            "structural_analysis",
            "code_analysis", 
            "dependency_mapping",
            "architecture_review",
            "complexity_analysis",
            "pattern_detection",
            "import_analysis",
            "module_mapping",
            "issue_detection",
            "refactoring_suggestions"
        ])
        
        # Estado interno
        self.analysis_history: List[StructuralAnalysis] = []
        self.known_modules: Dict[str, ModuleInfo] = {}
        self.analysis_count = 0
        
        # Padrões conhecidos
        self.known_patterns = {
            "singleton": r"class\s+\w+.*:\s*\n.*_instance\s*=\s*None",
            "factory": r"def\s+create_\w+|def\s+\w+_factory",
            "observer": r"def\s+notify|def\s+subscribe|def\s+unsubscribe",
            "decorator": r"@\w+|def\s+\w+_decorator"
        }
        
        logger.info(f"🔍 {self.agent_id} (Structure Analyzer) inicializado")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas pelo agente analisador."""
        try:
            content = message.content
            message_type = content.get("type", "unknown")
            
            if message_type == "analyze_structure":
                await self._handle_analyze_structure(message)
            elif message_type == "analyze_code":
                await self._handle_analyze_code(message)
            elif message_type == "dependency_analysis":
                await self._handle_dependency_analysis(message)
            elif message_type == "complexity_analysis":
                await self._handle_complexity_analysis(message)
            elif message_type == "pattern_detection":
                await self._handle_pattern_detection(message)
            elif message_type == "get_analysis_history":
                await self._handle_get_analysis_history(message)
            elif message_type == "get_module_info":
                await self._handle_get_module_info(message)
            elif message_type == "architecture_review":
                await self._handle_architecture_review(message)
            else:
                logger.debug(f"🔍 Tipo de mensagem não reconhecido: {message_type}")
                await self.publish_error_response(message, f"Tipo não reconhecido: {message_type}")
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro interno: {str(e)}")

    async def _handle_analyze_structure(self, message: AgentMessage):
        """Realiza análise estrutural completa."""
        try:
            content = message.content
            target_path = content.get("target_path", ".")
            analysis_type = content.get("analysis_type", "code_structure")
            include_dependencies = content.get("include_dependencies", True)
            
            # Validar caminho
            if not os.path.exists(target_path):
                await self.publish_error_response(message, f"Caminho não encontrado: {target_path}")
                return
            
            # Executar análise
            analysis_result = await self._perform_structural_analysis(
                target_path, 
                AnalysisType(analysis_type),
                include_dependencies
            )
            
            self.analysis_count += 1
            self.analysis_history.append(analysis_result)
            
            await self.publish_response(message, {
                "analysis_id": analysis_result.analysis_id,
                "modules_analyzed": analysis_result.modules_analyzed,
                "issues_found": len(analysis_result.issues_found),
                "architecture_score": analysis_result.architecture_score,
                "complexity_score": analysis_result.complexity_score,
                "recommendations": analysis_result.recommendations,
                "analysis_complete": True
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na análise estrutural: {str(e)}")

    async def _handle_analyze_code(self, message: AgentMessage):
        """Analisa código específico."""
        try:
            content = message.content
            code_content = content.get("code_content")
            file_path = content.get("file_path")
            
            if not code_content and not file_path:
                await self.publish_error_response(message, "code_content ou file_path deve ser fornecido")
                return
            
            # Ler arquivo se necessário
            if file_path and not code_content:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code_content = f.read()
                except Exception as e:
                    await self.publish_error_response(message, f"Erro ao ler arquivo: {str(e)}")
                    return
            
            # Analisar código
            analysis_result = await self._analyze_code_content(code_content, file_path or "unknown")
            
            await self.publish_response(message, {
                "code_analysis": analysis_result,
                "file_path": file_path,
                "analysis_timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na análise de código: {str(e)}")

    async def _handle_dependency_analysis(self, message: AgentMessage):
        """Analisa dependências de módulos."""
        try:
            content = message.content
            module_path = content.get("module_path", ".")
            depth_limit = content.get("depth_limit", 3)
            
            dependency_map = await self._analyze_dependencies(module_path, depth_limit)
            
            await self.publish_response(message, {
                "dependency_map": dependency_map,
                "total_modules": len(dependency_map),
                "analysis_depth": depth_limit
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na análise de dependências: {str(e)}")

    async def _handle_complexity_analysis(self, message: AgentMessage):
        """Analisa complexidade de código."""
        try:
            content = message.content
            target_path = content.get("target_path", ".")
            
            complexity_report = await self._analyze_complexity(target_path)
            
            await self.publish_response(message, {
                "complexity_report": complexity_report,
                "average_complexity": complexity_report.get("average_complexity", 0),
                "high_complexity_modules": complexity_report.get("high_complexity_modules", [])
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na análise de complexidade: {str(e)}")

    async def _handle_pattern_detection(self, message: AgentMessage):
        """Detecta padrões de design no código."""
        try:
            content = message.content
            target_path = content.get("target_path", ".")
            patterns_to_find = content.get("patterns", list(self.known_patterns.keys()))
            
            detected_patterns = await self._detect_patterns(target_path, patterns_to_find)
            
            await self.publish_response(message, {
                "detected_patterns": detected_patterns,
                "patterns_count": len(detected_patterns),
                "searched_patterns": patterns_to_find
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na detecção de padrões: {str(e)}")

    async def _handle_get_analysis_history(self, message: AgentMessage):
        """Retorna histórico de análises."""
        try:
            content = message.content
            limit = content.get("limit", 10)
            
            recent_analyses = [
                {
                    "analysis_id": analysis.analysis_id,
                    "analysis_type": analysis.analysis_type.value,
                    "target_path": analysis.target_path,
                    "modules_analyzed": analysis.modules_analyzed,
                    "issues_found": len(analysis.issues_found),
                    "architecture_score": analysis.architecture_score,
                    "analyzed_at": analysis.analyzed_at.isoformat()
                }
                for analysis in self.analysis_history[-limit:]
            ]
            
            await self.publish_response(message, {
                "analysis_history": recent_analyses,
                "total_analyses": len(self.analysis_history),
                "returned_count": len(recent_analyses)
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao obter histórico: {str(e)}")

    async def _handle_get_module_info(self, message: AgentMessage):
        """Retorna informações sobre módulos conhecidos."""
        try:
            content = message.content
            module_name = content.get("module_name")
            
            if module_name:
                if module_name in self.known_modules:
                    module_info = self.known_modules[module_name]
                    module_data = {
                        "name": module_info.name,
                        "path": module_info.path,
                        "lines_of_code": module_info.lines_of_code,
                        "functions": module_info.functions,
                        "classes": module_info.classes,
                        "complexity_score": module_info.complexity_score,
                        "last_analyzed": module_info.last_analyzed.isoformat()
                    }
                    await self.publish_response(message, {"module_info": module_data})
                else:
                    await self.publish_error_response(message, f"Módulo não encontrado: {module_name}")
            else:
                # Retornar lista de todos os módulos
                modules_summary = [
                    {
                        "name": info.name,
                        "path": info.path,
                        "complexity_score": info.complexity_score,
                        "last_analyzed": info.last_analyzed.isoformat()
                    }
                    for info in self.known_modules.values()
                ]
                
                await self.publish_response(message, {
                    "known_modules": modules_summary,
                    "total_modules": len(modules_summary)
                })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao obter info do módulo: {str(e)}")

    async def _handle_architecture_review(self, message: AgentMessage):
        """Realiza revisão arquitetural completa."""
        try:
            content = message.content
            project_path = content.get("project_path", ".")
            
            architecture_review = await self._perform_architecture_review(project_path)
            
            await self.publish_response(message, {
                "architecture_review": architecture_review,
                "overall_score": architecture_review.get("overall_score", 0),
                "recommendations": architecture_review.get("recommendations", []),
                "critical_issues": architecture_review.get("critical_issues", [])
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na revisão arquitetural: {str(e)}")

    async def _perform_structural_analysis(self, target_path: str, analysis_type: AnalysisType, include_dependencies: bool) -> StructuralAnalysis:
        """Executa análise estrutural completa."""
        analysis_id = f"analysis_{int(datetime.now().timestamp())}"
        issues_found = []
        modules_info = []
        
        # Coletar arquivos Python
        python_files = []
        if os.path.isfile(target_path) and target_path.endswith('.py'):
            python_files = [target_path]
        else:
            python_files = list(Path(target_path).rglob("*.py"))
        
        total_complexity = 0
        total_modules = 0
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Analisar módulo
                module_info = await self._analyze_module(str(file_path), content)
                modules_info.append(module_info)
                self.known_modules[module_info.name] = module_info
                
                total_complexity += module_info.complexity_score
                total_modules += 1
                
                # Detectar problemas estruturais
                module_issues = await self._detect_structural_issues(str(file_path), content)
                issues_found.extend(module_issues)
                
            except Exception as e:
                logger.warning(f"Erro ao analisar {file_path}: {e}")
                issues_found.append(StructuralIssue(
                    issue_type="analysis_error",
                    severity=ComplexityLevel.MEDIUM,
                    location=str(file_path),
                    description=f"Erro na análise: {str(e)}",
                    suggestions=["Verificar sintaxe do arquivo", "Verificar encoding"]
                ))
        
        # Calcular scores
        avg_complexity = total_complexity / max(total_modules, 1)
        architecture_score = max(0, 1 - (len(issues_found) * 0.1))
        
        # Gerar recomendações
        recommendations = self._generate_recommendations(issues_found, avg_complexity)
        
        return StructuralAnalysis(
            analysis_id=analysis_id,
            analysis_type=analysis_type,
            target_path=target_path,
            modules_analyzed=total_modules,
            issues_found=issues_found,
            module_info=modules_info,
            architecture_score=architecture_score,
            complexity_score=avg_complexity,
            recommendations=recommendations
        )

    async def _analyze_module(self, file_path: str, content: str) -> ModuleInfo:
        """Analisa um módulo específico."""
        try:
            tree = ast.parse(content)
            
            # Extrair informações
            functions = []
            classes = []
            imports = []
            dependencies = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                        dependencies.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                        dependencies.add(node.module.split('.')[0])
            
            # Calcular complexidade (simplificada)
            lines_of_code = len([line for line in content.split('\n') if line.strip()])
            complexity_score = min(1.0, len(functions) * 0.1 + len(classes) * 0.2 + lines_of_code * 0.001)
            
            module_name = os.path.basename(file_path).replace('.py', '')
            
            return ModuleInfo(
                name=module_name,
                path=file_path,
                lines_of_code=lines_of_code,
                functions=functions,
                classes=classes,
                imports=imports,
                dependencies=dependencies,
                complexity_score=complexity_score
            )
            
        except SyntaxError as e:
            logger.warning(f"Erro de sintaxe em {file_path}: {e}")
            return ModuleInfo(
                name=os.path.basename(file_path).replace('.py', ''),
                path=file_path,
                lines_of_code=0,
                functions=[],
                classes=[],
                imports=[],
                dependencies=set(),
                complexity_score=0.0
            )

    async def _analyze_code_content(self, code_content: str, file_path: str) -> Dict[str, Any]:
        """Analisa conteúdo de código específico."""
        try:
            tree = ast.parse(code_content)
            
            analysis = {
                "functions": [],
                "classes": [],
                "imports": [],
                "complexity_metrics": {},
                "issues": [],
                "suggestions": []
            }
            
            # Analisar estrutura
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "args_count": len(node.args.args),
                        "is_async": isinstance(node, ast.AsyncFunctionDef)
                    })
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    analysis["classes"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": methods,
                        "base_classes": [base.id if hasattr(base, 'id') else str(base) for base in node.bases]
                    })
            
            # Métricas de complexidade
            lines_of_code = len([line for line in code_content.split('\n') if line.strip()])
            analysis["complexity_metrics"] = {
                "lines_of_code": lines_of_code,
                "function_count": len(analysis["functions"]),
                "class_count": len(analysis["classes"]),
                "cyclomatic_complexity": self._calculate_cyclomatic_complexity(tree)
            }
            
            return analysis
            
        except SyntaxError as e:
            return {
                "error": f"Erro de sintaxe: {str(e)}",
                "line": getattr(e, 'lineno', 0),
                "offset": getattr(e, 'offset', 0)
            }

    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calcula complexidade ciclomática simplificada."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += len(node.handlers)
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity

    async def _detect_structural_issues(self, file_path: str, content: str) -> List[StructuralIssue]:
        """Detecta problemas estruturais em um arquivo."""
        issues = []
        lines = content.split('\n')
        
        # Issue 1: Funções muito longas
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Calcular linhas da função (aproximado)
                    func_lines = 0
                    if hasattr(node, 'end_lineno') and node.end_lineno:
                        func_lines = node.end_lineno - node.lineno
                    
                    if func_lines > 50:
                        issues.append(StructuralIssue(
                            issue_type="long_function",
                            severity=ComplexityLevel.MEDIUM,
                            location=f"{file_path}:{node.lineno}",
                            description=f"Função '{node.name}' tem {func_lines} linhas",
                            suggestions=["Quebrar função em funções menores", "Aplicar princípio de responsabilidade única"]
                        ))
        except:
            pass
        
        # Issue 2: Muitas importações
        import_lines = [line for line in lines if line.strip().startswith(('import ', 'from '))]
        if len(import_lines) > 20:
            issues.append(StructuralIssue(
                issue_type="too_many_imports",
                severity=ComplexityLevel.LOW,
                location=file_path,
                description=f"Arquivo tem {len(import_lines)} importações",
                suggestions=["Reorganizar imports", "Considerar refatoração de módulos"]
            ))
        
        # Issue 3: Arquivo muito longo
        total_lines = len([line for line in lines if line.strip()])
        if total_lines > 500:
            issues.append(StructuralIssue(
                issue_type="large_file",
                severity=ComplexityLevel.MEDIUM,
                location=file_path,
                description=f"Arquivo tem {total_lines} linhas",
                suggestions=["Dividir em múltiplos módulos", "Extrair classes/funções"]
            ))
        
        return issues

    async def _analyze_dependencies(self, module_path: str, depth_limit: int) -> Dict[str, Any]:
        """Analisa dependências entre módulos."""
        dependency_map = {}
        
        # Implementação simplificada
        python_files = list(Path(module_path).rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                module_name = os.path.basename(file_path).replace('.py', '')
                dependencies = set()
                
                # Extrair imports
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('import '):
                        dep = line.replace('import ', '').split('.')[0]
                        dependencies.add(dep)
                    elif line.startswith('from '):
                        dep = line.split()[1].split('.')[0]
                        dependencies.add(dep)
                
                dependency_map[module_name] = {
                    "path": str(file_path),
                    "dependencies": list(dependencies),
                    "dependency_count": len(dependencies)
                }
                
            except Exception as e:
                logger.warning(f"Erro ao analisar dependências de {file_path}: {e}")
        
        return dependency_map

    async def _analyze_complexity(self, target_path: str) -> Dict[str, Any]:
        """Analisa complexidade de código."""
        python_files = list(Path(target_path).rglob("*.py"))
        complexity_data = []
        total_complexity = 0
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                file_complexity = self._calculate_cyclomatic_complexity(tree)
                
                complexity_data.append({
                    "file": str(file_path),
                    "complexity": file_complexity,
                    "functions": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
                    "classes": len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
                })
                
                total_complexity += file_complexity
                
            except Exception as e:
                logger.warning(f"Erro ao analisar complexidade de {file_path}: {e}")
        
        avg_complexity = total_complexity / max(len(complexity_data), 1)
        high_complexity = [item for item in complexity_data if item["complexity"] > 10]
        
        return {
            "files_analyzed": len(complexity_data),
            "total_complexity": total_complexity,
            "average_complexity": avg_complexity,
            "high_complexity_modules": high_complexity,
            "complexity_data": complexity_data
        }

    async def _detect_patterns(self, target_path: str, patterns_to_find: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Detecta padrões de design no código."""
        detected_patterns = {pattern: [] for pattern in patterns_to_find}
        python_files = list(Path(target_path).rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern_name in patterns_to_find:
                    if pattern_name in self.known_patterns:
                        pattern_regex = self.known_patterns[pattern_name]
                        matches = re.finditer(pattern_regex, content, re.MULTILINE | re.DOTALL)
                        
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            detected_patterns[pattern_name].append({
                                "file": str(file_path),
                                "line": line_num,
                                "match": match.group(),
                                "context": self._extract_context(content, match.start(), match.end())
                            })
                
            except Exception as e:
                logger.warning(f"Erro ao detectar padrões em {file_path}: {e}")
        
        return detected_patterns

    def _extract_context(self, content: str, start: int, end: int, context_lines: int = 2) -> str:
        """Extrai contexto ao redor de um match."""
        lines = content.split('\n')
        match_line = content[:start].count('\n')
        
        start_line = max(0, match_line - context_lines)
        end_line = min(len(lines), match_line + context_lines + 1)
        
        context_lines_list = lines[start_line:end_line]
        return '\n'.join(context_lines_list)

    async def _perform_architecture_review(self, project_path: str) -> Dict[str, Any]:
        """Realiza revisão arquitetural completa."""
        review_data = {
            "overall_score": 0.0,
            "module_structure": {},
            "dependency_issues": [],
            "complexity_issues": [],
            "recommendations": [],
            "critical_issues": []
        }
        
        # Analisar estrutura de módulos
        python_files = list(Path(project_path).rglob("*.py"))
        total_score = 0
        score_components = 0
        
        # Componente 1: Organização de arquivos
        if len(python_files) > 0:
            avg_file_size = sum(len(open(f, 'r', encoding='utf-8').read().split('\n')) 
                              for f in python_files) / len(python_files)
            
            if avg_file_size < 200:
                file_org_score = 1.0
            elif avg_file_size < 400:
                file_org_score = 0.7
            else:
                file_org_score = 0.4
            
            total_score += file_org_score
            score_components += 1
        
        # Componente 2: Estrutura de dependências
        dependency_map = await self._analyze_dependencies(project_path, 3)
        circular_deps = self._detect_circular_dependencies(dependency_map)
        
        if len(circular_deps) == 0:
            dep_score = 1.0
        elif len(circular_deps) < 3:
            dep_score = 0.6
        else:
            dep_score = 0.3
        
        total_score += dep_score
        score_components += 1
        
        review_data["dependency_issues"] = circular_deps
        
        # Calcular score geral
        if score_components > 0:
            review_data["overall_score"] = total_score / score_components
        
        # Gerar recomendações
        if avg_file_size > 300:
            review_data["recommendations"].append("Considere dividir arquivos grandes em módulos menores")
        
        if len(circular_deps) > 0:
            review_data["recommendations"].append("Resolver dependências circulares detectadas")
            review_data["critical_issues"].extend(circular_deps)
        
        return review_data

    def _detect_circular_dependencies(self, dependency_map: Dict[str, Any]) -> List[str]:
        """Detecta dependências circulares (implementação simplificada)."""
        circular_deps = []
        
        for module, info in dependency_map.items():
            deps = info.get("dependencies", [])
            for dep in deps:
                if dep in dependency_map:
                    dep_deps = dependency_map[dep].get("dependencies", [])
                    if module in dep_deps:
                        circular_deps.append(f"Circular dependency: {module} <-> {dep}")
        
        return circular_deps

    def _generate_recommendations(self, issues: List[StructuralIssue], avg_complexity: float) -> List[str]:
        """Gera recomendações baseadas nos problemas encontrados."""
        recommendations = []
        
        # Recomendações baseadas em tipos de issues
        issue_types = [issue.issue_type for issue in issues]
        
        if "long_function" in issue_types:
            recommendations.append("Refatorar funções longas em funções menores")
        
        if "too_many_imports" in issue_types:
            recommendations.append("Reorganizar estrutura de imports")
        
        if "large_file" in issue_types:
            recommendations.append("Dividir arquivos grandes em módulos menores")
        
        # Recomendações baseadas em complexidade
        if avg_complexity > 15:
            recommendations.append("Reduzir complexidade ciclomática do código")
            recommendations.append("Implementar padrões de design para simplificar lógica")
        
        # Issues críticos
        critical_issues = [issue for issue in issues if issue.severity == ComplexityLevel.CRITICAL]
        if critical_issues:
            recommendations.append("Resolver problemas críticos identificados imediatamente")
        
        return recommendations


def create_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Factory function para criar o StructureAnalyzerAgent.
    
    Cria e inicializa o agente analisador de estruturas do sistema ALSHAM QUANTUM.
    
    Args:
        message_bus: MessageBus para comunicação entre agentes.
        
    Returns:
        List[BaseNetworkAgent]: Lista contendo o StructureAnalyzerAgent.
    """
    agents: List[BaseNetworkAgent] = []
    
    try:
        logger.info("🔍 [Factory] Criando StructureAnalyzerAgent...")
        
        # Criar o agente
        agent = StructureAnalyzerAgent("structure_analyzer_001", message_bus)
        agents.append(agent)
        
        logger.info(f"✅ StructureAnalyzerAgent criado: {agent.agent_id}")
        logger.info(f"🔧 Capabilities: {', '.join(agent.capabilities)}")
        
    except Exception as e:
        logger.critical(f"❌ Erro ao criar StructureAnalyzerAgent: {e}", exc_info=True)
    
    return agents
