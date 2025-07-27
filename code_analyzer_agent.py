import logging
import ast
import os
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import asyncio
from pathlib import Path
from collections import defaultdict
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class CodeIssueType(Enum):
    """Tipos de problemas de código"""
    SYNTAX_ERROR = "syntax_error"
    STYLE_VIOLATION = "style_violation"
    COMPLEXITY = "complexity"
    SECURITY = "security"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    DUPLICATION = "duplication"
    DEPRECATED = "deprecated"
    BUG_RISK = "bug_risk"

class SeverityLevel(Enum):
    """Níveis de severidade"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class CodeIssue:
    """Representa um problema encontrado no código"""
    issue_id: str
    file_path: str
    line_number: int
    column: int
    issue_type: CodeIssueType
    severity: SeverityLevel
    message: str
    suggestion: str
    code_snippet: Optional[str] = None
    rule_id: Optional[str] = None
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class CodeMetrics:
    """Métricas de código"""
    file_path: str
    lines_of_code: int
    cyclomatic_complexity: int
    maintainability_index: float
    coupling: int
    cohesion: float
    test_coverage: float = 0.0
    documentation_coverage: float = 0.0
    duplicate_lines: int = 0
    technical_debt_minutes: int = 0

@dataclass
class AnalysisReport:
    """Relatório completo de análise"""
    report_id: str
    analyzed_files: List[str]
    total_issues: int
    issues_by_severity: Dict[SeverityLevel, int]
    issues_by_type: Dict[CodeIssueType, int]
    overall_health_score: float
    recommendations: List[str]
    metrics: List[CodeMetrics]
    timestamp: datetime = field(default_factory=datetime.now)

class CodeAnalyzerAgent(BaseNetworkAgent):
    """Agente especializado em análise de código e detecção de problemas"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'code_analysis',
            'error_detection',
            'suggestion_generation',
            'complexity_analysis',
            'security_scanning',
            'performance_analysis',
            'style_checking',
            'metrics_calculation'
        ]
        self.status = 'active'
        
        # Estado do analisador
        self.analysis_queue = asyncio.Queue()
        self.analysis_history = []
        self.issue_patterns = self._load_issue_patterns()
        self.code_rules = self._load_code_rules()
        
        # Configurações
        self.max_complexity_threshold = 10
        self.max_line_length = 100
        self.min_maintainability_index = 60
        self.security_patterns = self._load_security_patterns()
        
        # Métricas
        self.analysis_metrics = {
            'files_analyzed': 0,
            'issues_found': 0,
            'critical_issues': 0,
            'suggestions_generated': 0,
            'average_health_score': 0.0
        }
        
        # Tasks de background
        self._analysis_task = None
        self._monitoring_task = None
        
        logger.info(f"🔍 {self.agent_id} inicializado com análise avançada de código")
    
    def _load_issue_patterns(self) -> Dict[str, Any]:
        """Carrega padrões de problemas conhecidos"""
        return {
            'exception_handling': {
                'bare_except': re.compile(r'except\s*:'),
                'broad_except': re.compile(r'except\s+Exception\s*:'),
                'empty_except': re.compile(r'except.*:\s*pass')
            },
            'security': {
                'hardcoded_password': re.compile(r'(password|passwd|pwd)\s*=\s*["\'].*["\']'),
                'sql_injection': re.compile(r'(execute|query)\s*\(.*%.*\)'),
                'eval_usage': re.compile(r'eval\s*\('),
                'exec_usage': re.compile(r'exec\s*\(')
            },
            'performance': {
                'nested_loops': re.compile(r'for.*:\s*\n\s*for.*:'),
                'repeated_append': re.compile(r'\.append\(.*\).*\.append\(.*\)'),
                'inefficient_lookup': re.compile(r'if.*in.*list\(')
            },
            'style': {
                'multiple_imports': re.compile(r'import.*,.*'),
                'wildcard_import': re.compile(r'from.*import\s*\*'),
                'missing_docstring': re.compile(r'def\s+\w+\(.*\):\s*\n\s*[^"\']')
            }
        }
    
    def _load_code_rules(self) -> Dict[str, Any]:
        """Carrega regras de código"""
        return {
            'naming': {
                'function': re.compile(r'^[a-z_][a-z0-9_]*$'),
                'class': re.compile(r'^[A-Z][a-zA-Z0-9]*$'),
                'constant': re.compile(r'^[A-Z_][A-Z0-9_]*$')
            },
            'complexity': {
                'max_function_length': 50,
                'max_parameters': 5,
                'max_branches': 10,
                'max_nesting': 4
            },
            'documentation': {
                'require_docstring': True,
                'min_docstring_length': 10,
                'require_type_hints': True
            }
        }
    
    def _load_security_patterns(self) -> List[Dict[str, Any]]:
        """Carrega padrões de segurança"""
        return [
            {
                'pattern': re.compile(r'pickle\.loads?\('),
                'severity': SeverityLevel.HIGH,
                'message': 'Uso inseguro de pickle - vulnerável a execução de código'
            },
            {
                'pattern': re.compile(r'subprocess.*shell\s*=\s*True'),
                'severity': SeverityLevel.CRITICAL,
                'message': 'Shell injection vulnerability - shell=True em subprocess'
            },
            {
                'pattern': re.compile(r'random\.random\(\)'),
                'severity': SeverityLevel.MEDIUM,
                'message': 'Uso de random não criptográfico para segurança'
            },
            {
                'pattern': re.compile(r'hashlib\.md5\('),
                'severity': SeverityLevel.HIGH,
                'message': 'MD5 é inseguro para hashing - use SHA256 ou superior'
            }
        ]
    
    async def start_analysis_service(self):
        """Inicia serviço de análise"""
        if not self._analysis_task:
            self._analysis_task = asyncio.create_task(self._analysis_loop())
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            logger.info(f"🔍 {self.agent_id} iniciou serviço de análise")
    
    async def stop_analysis_service(self):
        """Para serviço de análise"""
        if self._analysis_task:
            self._analysis_task.cancel()
            self._analysis_task = None
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
        logger.info(f"🛑 {self.agent_id} parou serviço de análise")
    
    async def _analysis_loop(self):
        """Loop principal de análise"""
        while True:
            try:
                # Processar fila de análise
                if not self.analysis_queue.empty():
                    analysis_request = await self.analysis_queue.get()
                    await self._process_analysis_request(analysis_request)
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de análise: {e}")
    
    async def _monitoring_loop(self):
        """Loop de monitoramento do sistema"""
        while True:
            try:
                # Monitorar arquivos do sistema para mudanças
                await self._scan_system_files()
                
                # Gerar relatórios periódicos
                if len(self.analysis_history) > 10:
                    await self._generate_system_report()
                
                await asyncio.sleep(60)  # Verificar a cada minuto
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'analyze_file':
                result = await self.analyze_file(message.content.get('file_path'))
                await self._send_response(message, result)
                
            elif request_type == 'analyze_directory':
                result = await self.analyze_directory(message.content.get('directory_path'))
                await self._send_response(message, result)
                
            elif request_type == 'get_metrics':
                result = await self.calculate_metrics(message.content.get('file_path'))
                await self._send_response(message, result)
                
            elif request_type == 'security_scan':
                result = await self.security_scan(message.content.get('file_path'))
                await self._send_response(message, result)
                
            elif request_type == 'get_report':
                result = self._get_latest_report()
                await self._send_response(message, result)
    
    async def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analisa um arquivo Python"""
        try:
            logger.info(f"🔍 Analisando arquivo: {file_path}")
            
            if not os.path.exists(file_path):
                return {
                    'status': 'error',
                    'message': f'Arquivo não encontrado: {file_path}'
                }
            
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
            
            # Parse AST
            try:
                tree = ast.parse(code, filename=file_path)
            except SyntaxError as e:
                return {
                    'status': 'error',
                    'syntax_error': {
                        'line': e.lineno,
                        'message': str(e)
                    }
                }
            
            # Análises
            issues = []
            
            # Análise de complexidade
            complexity_issues = self._analyze_complexity(tree, file_path, code)
            issues.extend(complexity_issues)
            
            # Análise de estilo
            style_issues = self._analyze_style(code, file_path)
            issues.extend(style_issues)
            
            # Análise de segurança
            security_issues = self._analyze_security(code, file_path)
            issues.extend(security_issues)
            
            # Análise de performance
            performance_issues = self._analyze_performance(tree, file_path, code)
            issues.extend(performance_issues)
            
            # Análise de manutenibilidade
            maintainability_issues = self._analyze_maintainability(tree, file_path, code)
            issues.extend(maintainability_issues)
            
            # Calcular métricas
            metrics = await self.calculate_metrics(file_path)
            
            # Gerar relatório
            health_score = self._calculate_health_score(issues, metrics)
            
            self.analysis_metrics['files_analyzed'] += 1
            self.analysis_metrics['issues_found'] += len(issues)
            self.analysis_metrics['critical_issues'] += sum(
                1 for issue in issues if issue.severity == SeverityLevel.CRITICAL
            )
            
            result = {
                'status': 'completed',
                'file_path': file_path,
                'issues': [self._issue_to_dict(issue) for issue in issues],
                'metrics': metrics,
                'health_score': health_score,
                'suggestions': self._generate_suggestions(issues, metrics)
            }
            
            # Adicionar ao histórico
            self.analysis_history.append(result)
            
            # Notificar sobre problemas críticos
            critical_issues = [i for i in issues if i.severity == SeverityLevel.CRITICAL]
            if critical_issues:
                await self._notify_critical_issues(file_path, critical_issues)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro analisando {file_path}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _analyze_complexity(self, tree: ast.AST, file_path: str, code: str) -> List[CodeIssue]:
        """Analisa complexidade do código"""
        issues = []
        analyzer_self = self  # Referência para usar dentro da classe interna
        
        class ComplexityVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current_function = None
                self.complexity_stack = []
            
            def visit_FunctionDef(self, node):
                self.current_function = node.name
                complexity = self._calculate_cyclomatic_complexity(node)
                
                if complexity > analyzer_self.max_complexity_threshold:
                    issue = CodeIssue(
                        issue_id=f"complexity_{len(analyzer_self.analysis_history)}_{len(issues)}",
                        file_path=file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        issue_type=CodeIssueType.COMPLEXITY,
                        severity=SeverityLevel.HIGH if complexity > 15 else SeverityLevel.MEDIUM,
                        message=f"Função '{node.name}' tem complexidade ciclomática {complexity}",
                        suggestion=f"Refatore a função para reduzir complexidade (máximo recomendado: {analyzer_self.max_complexity_threshold})",
                        rule_id="C901"
                    )
                    issues.append(issue)
                
                # Verificar número de parâmetros
                if len(node.args.args) > analyzer_self.code_rules['complexity']['max_parameters']:
                    issue = CodeIssue(
                        issue_id=f"params_{len(analyzer_self.analysis_history)}_{len(issues)}",
                        file_path=file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        issue_type=CodeIssueType.COMPLEXITY,
                        severity=SeverityLevel.MEDIUM,
                        message=f"Função '{node.name}' tem {len(node.args.args)} parâmetros",
                        suggestion="Considere usar um objeto de configuração ou reduzir parâmetros",
                        rule_id="C902"
                    )
                    issues.append(issue)
                
                self.generic_visit(node)
            
            def _calculate_cyclomatic_complexity(self, node):
                """Calcula complexidade ciclomática"""
                complexity = 1
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For)):
                        complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        complexity += len(child.values) - 1
                return complexity
        
        visitor = ComplexityVisitor()
        visitor.visit(tree)
        
        return issues
    
    def _analyze_style(self, code: str, file_path: str) -> List[CodeIssue]:
        """Analisa estilo do código"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Verificar comprimento da linha
            if len(line) > self.max_line_length:
                issue = CodeIssue(
                    issue_id=f"line_length_{len(self.analysis_history)}_{len(issues)}",
                    file_path=file_path,
                    line_number=i,
                    column=self.max_line_length,
                    issue_type=CodeIssueType.STYLE_VIOLATION,
                    severity=SeverityLevel.LOW,
                    message=f"Linha muito longa ({len(line)} caracteres)",
                    suggestion=f"Mantenha linhas com no máximo {self.max_line_length} caracteres",
                    code_snippet=line[:50] + "...",
                    rule_id="E501"
                )
                issues.append(issue)
            
            # Verificar trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                issue = CodeIssue(
                    issue_id=f"trailing_ws_{len(self.analysis_history)}_{len(issues)}",
                    file_path=file_path,
                    line_number=i,
                    column=len(line),
                    issue_type=CodeIssueType.STYLE_VIOLATION,
                    severity=SeverityLevel.INFO,
                    message="Espaço em branco no final da linha",
                    suggestion="Remova espaços em branco desnecessários",
                    rule_id="W291"
                )
                issues.append(issue)
        
        # Verificar padrões de estilo
        for pattern_type, patterns in self.issue_patterns['style'].items():
            for match in patterns.finditer(code):
                line_num = code[:match.start()].count('\n') + 1
                
                if pattern_type == 'wildcard_import':
                    issue = CodeIssue(
                        issue_id=f"wildcard_{len(self.analysis_history)}_{len(issues)}",
                        file_path=file_path,
                        line_number=line_num,
                        column=match.start() - code.rfind('\n', 0, match.start()),
                        issue_type=CodeIssueType.STYLE_VIOLATION,
                        severity=SeverityLevel.MEDIUM,
                        message="Import com wildcard (*) detectado",
                        suggestion="Importe apenas os símbolos necessários explicitamente",
                        code_snippet=match.group(),
                        rule_id="F403"
                    )
                    issues.append(issue)
        
        return issues
    
    def _analyze_security(self, code: str, file_path: str) -> List[CodeIssue]:
        """Analisa segurança do código"""
        issues = []
        
        # Verificar padrões de segurança conhecidos
        for security_check in self.security_patterns:
            for match in security_check['pattern'].finditer(code):
                line_num = code[:match.start()].count('\n') + 1
                
                issue = CodeIssue(
                    issue_id=f"security_{len(self.analysis_history)}_{len(issues)}",
                    file_path=file_path,
                    line_number=line_num,
                    column=match.start() - code.rfind('\n', 0, match.start()),
                    issue_type=CodeIssueType.SECURITY,
                    severity=security_check['severity'],
                    message=security_check['message'],
                    suggestion="Revise e use alternativas seguras",
                    code_snippet=match.group(),
                    rule_id="SEC001",
                    confidence=0.9
                )
                issues.append(issue)
        
        # Verificar padrões específicos
        for pattern_type, pattern in self.issue_patterns['security'].items():
            for match in pattern.finditer(code):
                line_num = code[:match.start()].count('\n') + 1
                
                severity = SeverityLevel.HIGH
                message = ""
                suggestion = ""
                
                if pattern_type == 'hardcoded_password':
                    message = "Possível senha hardcoded detectada"
                    suggestion = "Use variáveis de ambiente ou gerenciamento seguro de credenciais"
                    severity = SeverityLevel.CRITICAL
                elif pattern_type == 'sql_injection':
                    message = "Possível vulnerabilidade de SQL injection"
                    suggestion = "Use prepared statements ou query builders"
                elif pattern_type == 'eval_usage':
                    message = "Uso de eval() detectado - risco de segurança"
                    suggestion = "Evite eval() e use alternativas seguras como ast.literal_eval()"
                
                if message:
                    issue = CodeIssue(
                        issue_id=f"security_{pattern_type}_{len(self.analysis_history)}_{len(issues)}",
                        file_path=file_path,
                        line_number=line_num,
                        column=match.start() - code.rfind('\n', 0, match.start()),
                        issue_type=CodeIssueType.SECURITY,
                        severity=severity,
                        message=message,
                        suggestion=suggestion,
                        code_snippet=match.group()[:50],
                        rule_id="SEC002"
                    )
                    issues.append(issue)
        
        return issues
    
    def _analyze_performance(self, tree: ast.AST, file_path: str, code: str) -> List[CodeIssue]:
        """Analisa performance do código"""
        issues = []
        analyzer_self = self  # Referência para usar dentro da classe interna
        
        class PerformanceVisitor(ast.NodeVisitor):
            def __init__(self):
                self.loop_depth = 0
            
            def visit_For(self, node):
                self.loop_depth += 1
                
                # Detectar loops aninhados profundos
                if self.loop_depth > 2:
                    issue = CodeIssue(
                        issue_id=f"nested_loops_{len(analyzer_self.analysis_history)}_{len(issues)}",
                        file_path=file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        issue_type=CodeIssueType.PERFORMANCE,
                        severity=SeverityLevel.MEDIUM,
                        message=f"Loop aninhado com profundidade {self.loop_depth}",
                        suggestion="Considere refatorar para reduzir aninhamento de loops",
                        rule_id="PERF001"
                    )
                    issues.append(issue)
                
                self.generic_visit(node)
                self.loop_depth -= 1
            
            def visit_ListComp(self, node):
                # Verificar list comprehensions complexas
                if self._count_comprehension_complexity(node) > 3:
                    issue = CodeIssue(
                        issue_id=f"complex_comp_{len(analyzer_self.analysis_history)}_{len(issues)}",
                        file_path=file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        issue_type=CodeIssueType.PERFORMANCE,
                        severity=SeverityLevel.LOW,
                        message="List comprehension muito complexa",
                        suggestion="Considere usar um loop regular para melhor legibilidade",
                        rule_id="PERF002"
                    )
                    issues.append(issue)
                
                self.generic_visit(node)
            
            def _count_comprehension_complexity(self, node):
                """Conta complexidade de comprehension"""
                complexity = 0
                for generator in node.generators:
                    complexity += 1
                    complexity += len(generator.ifs)
                return complexity
        
        visitor = PerformanceVisitor()
        visitor.visit(tree)
        
        # Verificar padrões de performance no código
        for pattern_type, pattern in self.issue_patterns['performance'].items():
            for match in pattern.finditer(code):
                line_num = code[:match.start()].count('\n') + 1
                
                if pattern_type == 'inefficient_lookup':
                    issue = CodeIssue(
                        issue_id=f"inefficient_{len(self.analysis_history)}_{len(issues)}",
                        file_path=file_path,
                        line_number=line_num,
                        column=0,
                        issue_type=CodeIssueType.PERFORMANCE,
                        severity=SeverityLevel.MEDIUM,
                        message="Lookup ineficiente em lista - O(n) complexidade",
                        suggestion="Use set ou dict para lookups O(1)",
                        code_snippet=match.group(),
                        rule_id="PERF003"
                    )
                    issues.append(issue)
        
        return issues
    
    def _analyze_maintainability(self, tree: ast.AST, file_path: str, code: str) -> List[CodeIssue]:
        """Analisa manutenibilidade do código"""
        issues = []
        analyzer_self = self  # Referência para usar dentro da classe interna
        
        class MaintainabilityVisitor(ast.NodeVisitor):
            def __init__(self):
                pass
            
            def visit_FunctionDef(self, node):
                # Verificar docstring
                if not ast.get_docstring(node):
                    issue = CodeIssue(
                        issue_id=f"no_docstring_{len(analyzer_self.analysis_history)}_{len(issues)}",
                        file_path=file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        issue_type=CodeIssueType.MAINTAINABILITY,
                        severity=SeverityLevel.MEDIUM,
                        message=f"Função '{node.name}' sem docstring",
                        suggestion="Adicione uma docstring descrevendo a função",
                        rule_id="D103"
                    )
                    issues.append(issue)
                
                # Verificar tamanho da função
                function_lines = node.end_lineno - node.lineno
                if function_lines > analyzer_self.code_rules['complexity']['max_function_length']:
                    issue = CodeIssue(
                        issue_id=f"long_function_{len(analyzer_self.analysis_history)}_{len(issues)}",
                        file_path=file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        issue_type=CodeIssueType.MAINTAINABILITY,
                        severity=SeverityLevel.MEDIUM,
                        message=f"Função '{node.name}' muito longa ({function_lines} linhas)",
                        suggestion="Considere dividir em funções menores",
                        rule_id="M001"
                    )
                    issues.append(issue)
                
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                # Verificar docstring de classe
                if not ast.get_docstring(node):
                    issue = CodeIssue(
                        issue_id=f"class_no_doc_{len(analyzer_self.analysis_history)}_{len(issues)}",
                        file_path=file_path,
                        line_number=node.lineno,
                        column=node.col_offset,
                        issue_type=CodeIssueType.MAINTAINABILITY,
                        severity=SeverityLevel.MEDIUM,
                        message=f"Classe '{node.name}' sem docstring",
                        suggestion="Adicione uma docstring descrevendo a classe",
                        rule_id="D101"
                    )
                    issues.append(issue)
                
                self.generic_visit(node)
        
        visitor = MaintainabilityVisitor()
        visitor.visit(tree)
        
        # Verificar duplicação de código (simplificado)
        lines = code.split('\n')
        seen_lines = defaultdict(list)
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if len(stripped) > 20 and not stripped.startswith('#'):
                seen_lines[stripped].append(i)
        
        for line_text, occurrences in seen_lines.items():
            if len(occurrences) > 2:
                issue = CodeIssue(
                    issue_id=f"duplicate_{len(self.analysis_history)}_{len(issues)}",
                    file_path=file_path,
                    line_number=occurrences[0],
                    column=0,
                    issue_type=CodeIssueType.DUPLICATION,
                    severity=SeverityLevel.LOW,
                    message=f"Código duplicado detectado ({len(occurrences)} ocorrências)",
                    suggestion="Extraia código duplicado para uma função",
                    code_snippet=line_text[:50],
                    rule_id="DUP001"
                )
                issues.append(issue)
                break  # Reportar apenas uma vez
        
        return issues
    
    async def calculate_metrics(self, file_path: str) -> Dict[str, Any]:
        """Calcula métricas do arquivo"""
        try:
            if not os.path.exists(file_path):
                return {'error': 'Arquivo não encontrado'}
            
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
            
            lines = code.split('\n')
            
            # Métricas básicas
            total_lines = len(lines)
            code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            blank_lines = sum(1 for line in lines if not line.strip())
            
            # Parse AST para métricas avançadas
            try:
                tree = ast.parse(code)
                
                # Contar elementos
                functions = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
                classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
                imports = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)))
                
                # Complexidade ciclomática média
                total_complexity = 0
                function_count = 0
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        function_count += 1
                        # Calcular complexidade
                        complexity = 1
                        for child in ast.walk(node):
                            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                                complexity += 1
                        total_complexity += complexity
                
                avg_complexity = total_complexity / max(1, function_count)
                
                # Índice de manutenibilidade (simplificado)
                # MI = 171 - 5.2 * ln(V) - 0.23 * CC - 16.2 * ln(LOC)
                import math
                volume = code_lines * math.log(max(1, functions + classes))
                maintainability_index = max(0, min(100, 
                    171 - 5.2 * math.log(max(1, volume)) - 
                    0.23 * avg_complexity - 
                    16.2 * math.log(max(1, code_lines))
                ))
                
                return {
                    'total_lines': total_lines,
                    'code_lines': code_lines,
                    'comment_lines': comment_lines,
                    'blank_lines': blank_lines,
                    'functions': functions,
                    'classes': classes,
                    'imports': imports,
                    'average_complexity': round(avg_complexity, 2),
                    'maintainability_index': round(maintainability_index, 2),
                    'comment_ratio': round(comment_lines / max(1, code_lines), 2)
                }
                
            except SyntaxError:
                return {
                    'total_lines': total_lines,
                    'code_lines': code_lines,
                    'comment_lines': comment_lines,
                    'blank_lines': blank_lines,
                    'error': 'Erro de sintaxe no arquivo'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro calculando métricas: {e}")
            return {'error': str(e)}
    
    async def analyze_directory(self, directory_path: str) -> Dict[str, Any]:
        """Analisa todos os arquivos Python em um diretório"""
        try:
            if not os.path.exists(directory_path):
                return {
                    'status': 'error',
                    'message': f'Diretório não encontrado: {directory_path}'
                }
            
            python_files = []
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
            
            if not python_files:
                return {
                    'status': 'completed',
                    'message': 'Nenhum arquivo Python encontrado',
                    'files_analyzed': 0
                }
            
            results = []
            total_issues = 0
            total_health_score = 0
            
            for file_path in python_files:
                result = await self.analyze_file(file_path)
                if result['status'] == 'completed':
                    results.append(result)
                    total_issues += len(result.get('issues', []))
                    total_health_score += result.get('health_score', 0)
            
            average_health = total_health_score / max(1, len(results))
            
            # Gerar relatório agregado
            report = AnalysisReport(
                report_id=f"report_{len(self.analysis_history)}",
                analyzed_files=[r['file_path'] for r in results],
                total_issues=total_issues,
                issues_by_severity=self._count_issues_by_severity(results),
                issues_by_type=self._count_issues_by_type(results),
                overall_health_score=average_health,
                recommendations=self._generate_directory_recommendations(results),
                metrics=[r.get('metrics', {}) for r in results]
            )
            
            return {
                'status': 'completed',
                'directory': directory_path,
                'files_analyzed': len(results),
                'total_issues': total_issues,
                'average_health_score': round(average_health, 2),
                'report': self._report_to_dict(report),
                'file_results': results
            }
            
        except Exception as e:
            logger.error(f"❌ Erro analisando diretório: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def security_scan(self, file_path: str) -> Dict[str, Any]:
        """Realiza scan focado em segurança"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
            
            security_issues = self._analyze_security(code, file_path)
            
            # Análises adicionais de segurança
            additional_checks = [
                {
                    'pattern': re.compile(r'os\.system\('),
                    'message': 'os.system() pode ser vulnerável a command injection',
                    'severity': SeverityLevel.HIGH
                },
                {
                    'pattern': re.compile(r'yaml\.load\('),
                    'message': 'yaml.load() inseguro - use yaml.safe_load()',
                    'severity': SeverityLevel.HIGH
                },
                {
                    'pattern': re.compile(r'input\(.*\).*exec|eval'),
                    'message': 'Input do usuário sendo executado - extremamente perigoso',
                    'severity': SeverityLevel.CRITICAL
                }
            ]
            
            for check in additional_checks:
                for match in check['pattern'].finditer(code):
                    line_num = code[:match.start()].count('\n') + 1
                    issue = CodeIssue(
                        issue_id=f"sec_scan_{len(security_issues)}",
                        file_path=file_path,
                        line_number=line_num,
                        column=0,
                        issue_type=CodeIssueType.SECURITY,
                        severity=check['severity'],
                        message=check['message'],
                        suggestion="Revise e implemente alternativa segura",
                        code_snippet=match.group()
                    )
                    security_issues.append(issue)
            
            # Classificar por severidade
            security_issues.sort(key=lambda x: [
                SeverityLevel.CRITICAL,
                SeverityLevel.HIGH,
                SeverityLevel.MEDIUM,
                SeverityLevel.LOW,
                SeverityLevel.INFO
            ].index(x.severity))
            
            return {
                'status': 'completed',
                'file_path': file_path,
                'security_issues': [self._issue_to_dict(issue) for issue in security_issues],
                'critical_count': sum(1 for i in security_issues if i.severity == SeverityLevel.CRITICAL),
                'high_count': sum(1 for i in security_issues if i.severity == SeverityLevel.HIGH),
                'risk_assessment': self._assess_security_risk(security_issues)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no scan de segurança: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _calculate_health_score(self, issues: List[CodeIssue], metrics: Dict[str, Any]) -> float:
        """Calcula score de saúde do código"""
        score = 100.0
        
        # Penalizar por issues
        for issue in issues:
            if issue.severity == SeverityLevel.CRITICAL:
                score -= 10
            elif issue.severity == SeverityLevel.HIGH:
                score -= 5
            elif issue.severity == SeverityLevel.MEDIUM:
                score -= 2
            elif issue.severity == SeverityLevel.LOW:
                score -= 0.5
        
        # Considerar métricas
        if isinstance(metrics, dict):
            # Complexidade
            avg_complexity = metrics.get('average_complexity', 0)
            if avg_complexity > 10:
                score -= (avg_complexity - 10) * 2
            
            # Manutenibilidade
            mi = metrics.get('maintainability_index', 100)
            if mi < 60:
                score -= (60 - mi) / 2
            
            # Ratio de comentários
            comment_ratio = metrics.get('comment_ratio', 0)
            if comment_ratio < 0.1:
                score -= 5
        
        return max(0, min(100, score))
    
    def _generate_suggestions(self, issues: List[CodeIssue], metrics: Dict[str, Any]) -> List[str]:
        """Gera sugestões baseadas nos problemas encontrados"""
        suggestions = []
        
        # Agrupar issues por tipo
        issue_types = defaultdict(int)
        for issue in issues:
            issue_types[issue.issue_type] += 1
        
        # Sugestões por tipo de problema
        if issue_types[CodeIssueType.COMPLEXITY] > 2:
            suggestions.append("Refatore funções complexas em unidades menores e mais simples")
        
        if issue_types[CodeIssueType.SECURITY] > 0:
            suggestions.append("Realize uma revisão de segurança completa e implemente práticas seguras")
        
        if issue_types[CodeIssueType.PERFORMANCE] > 3:
            suggestions.append("Considere otimizar algoritmos e estruturas de dados")
        
        if issue_types[CodeIssueType.MAINTAINABILITY] > 5:
            suggestions.append("Melhore documentação e estrutura do código para facilitar manutenção")
        
        # Sugestões baseadas em métricas
        if isinstance(metrics, dict):
            if metrics.get('average_complexity', 0) > 10:
                suggestions.append("Reduza complexidade ciclomática através de refatoração")
            
            if metrics.get('comment_ratio', 1) < 0.1:
                suggestions.append("Adicione mais comentários e documentação ao código")
            
            if metrics.get('maintainability_index', 100) < 60:
                suggestions.append("Melhore índice de manutenibilidade seguindo boas práticas")
        
        self.analysis_metrics['suggestions_generated'] += len(suggestions)
        
        return suggestions[:5]  # Limitar a 5 sugestões principais
    
    async def _scan_system_files(self):
        """Escaneia arquivos do sistema para análise proativa"""
        try:
            # Diretórios padrão para monitorar
            monitored_dirs = [
                ".",
                "./src",
                "./lib",
                "./app"
            ]
            
            for directory in monitored_dirs:
                if os.path.exists(directory):
                    # Verificar arquivos modificados recentemente
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            if file.endswith('.py'):
                                file_path = os.path.join(root, file)
                                
                                # Verificar tempo de modificação
                                try:
                                    mtime = os.path.getmtime(file_path)
                                    if time.time() - mtime < 3600:  # Modificado na última hora
                                        await self.analysis_queue.put({
                                            'type': 'auto_scan',
                                            'file_path': file_path
                                        })
                                except:
                                    pass
        except Exception as e:
            logger.error(f"❌ Erro no scan de arquivos do sistema: {e}")
    
    async def _generate_system_report(self):
        """Gera relatório do sistema"""
        recent_analyses = self.analysis_history[-50:]
        
        total_issues = sum(len(a.get('issues', [])) for a in recent_analyses)
        avg_health = sum(a.get('health_score', 0) for a in recent_analyses) / max(1, len(recent_analyses))
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'files_analyzed': self.analysis_metrics['files_analyzed'],
            'total_issues': total_issues,
            'critical_issues': self.analysis_metrics['critical_issues'],
            'average_health_score': avg_health,
            'top_problems': self._identify_top_problems(recent_analyses),
            'improvement_trends': self._calculate_trends()
        }
        
        # Notificar sobre tendências negativas
        if avg_health < 70:
            await self._notify_poor_code_health(report)
    
    async def _process_analysis_request(self, request: Dict[str, Any]):
        """Processa requisição de análise da fila"""
        request_type = request.get('type')
        
        if request_type == 'auto_scan':
            result = await self.analyze_file(request['file_path'])
            logger.info(f"✅ Auto-scan completo: {request['file_path']}")
    
    def _issue_to_dict(self, issue: CodeIssue) -> Dict[str, Any]:
        """Converte issue para dicionário"""
        return {
            'issue_id': issue.issue_id,
            'line': issue.line_number,
            'column': issue.column,
            'type': issue.issue_type.value,
            'severity': issue.severity.value,
            'message': issue.message,
            'suggestion': issue.suggestion,
            'code_snippet': issue.code_snippet,
            'rule_id': issue.rule_id,
            'confidence': issue.confidence
        }
    
    def _report_to_dict(self, report: AnalysisReport) -> Dict[str, Any]:
        """Converte relatório para dicionário"""
        return {
            'report_id': report.report_id,
            'timestamp': report.timestamp.isoformat(),
            'files_analyzed': len(report.analyzed_files),
            'total_issues': report.total_issues,
            'issues_by_severity': {k.value: v for k, v in report.issues_by_severity.items()},
            'issues_by_type': {k.value: v for k, v in report.issues_by_type.items()},
            'health_score': round(report.overall_health_score, 2),
            'recommendations': report.recommendations
        }
    
    def _count_issues_by_severity(self, results: List[Dict]) -> Dict[SeverityLevel, int]:
        """Conta issues por severidade"""
        counts = defaultdict(int)
        for result in results:
            for issue in result.get('issues', []):
                severity = SeverityLevel(issue['severity'])
                counts[severity] += 1
        return dict(counts)
    
    def _count_issues_by_type(self, results: List[Dict]) -> Dict[CodeIssueType, int]:
        """Conta issues por tipo"""
        counts = defaultdict(int)
        for result in results:
            for issue in result.get('issues', []):
                issue_type = CodeIssueType(issue['type'])
                counts[issue_type] += 1
        return dict(counts)
    
    def _generate_directory_recommendations(self, results: List[Dict]) -> List[str]:
        """Gera recomendações para o diretório"""
        all_suggestions = []
        for result in results:
            all_suggestions.extend(result.get('suggestions', []))
        
        # Contar sugestões mais comuns
        suggestion_counts = defaultdict(int)
        for suggestion in all_suggestions:
            suggestion_counts[suggestion] += 1
        
        # Retornar top 5 mais comuns
        sorted_suggestions = sorted(
            suggestion_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [suggestion for suggestion, count in sorted_suggestions[:5]]
    
    def _assess_security_risk(self, issues: List[CodeIssue]) -> str:
        """Avalia nível de risco de segurança"""
        if any(i.severity == SeverityLevel.CRITICAL for i in issues):
            return "CRÍTICO - Ação imediata necessária"
        elif any(i.severity == SeverityLevel.HIGH for i in issues):
            return "ALTO - Correções urgentes recomendadas"
        elif any(i.severity == SeverityLevel.MEDIUM for i in issues):
            return "MÉDIO - Revisar e planejar correções"
        elif issues:
            return "BAIXO - Melhorias recomendadas"
        else:
            return "SEGURO - Nenhum problema detectado"
    
    def _identify_top_problems(self, analyses: List[Dict]) -> List[Dict[str, Any]]:
        """Identifica principais problemas recorrentes"""
        problem_counts = defaultdict(int)
        
        for analysis in analyses:
            for issue in analysis.get('issues', []):
                problem_key = f"{issue['type']}:{issue['message'][:30]}"
                problem_counts[problem_key] += 1
        
        top_problems = sorted(
            problem_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return [
            {'problem': problem, 'occurrences': count}
            for problem, count in top_problems
        ]
    
    def _calculate_trends(self) -> Dict[str, str]:
        """Calcula tendências de melhoria/piora"""
        if len(self.analysis_history) < 10:
            return {'status': 'insufficient_data'}
        
        # Comparar últimas 5 análises com 5 anteriores
        recent = self.analysis_history[-5:]
        previous = self.analysis_history[-10:-5]
        
        recent_health = sum(a.get('health_score', 0) for a in recent) / 5
        previous_health = sum(a.get('health_score', 0) for a in previous) / 5
        
        if recent_health > previous_health + 5:
            trend = "improving"
        elif recent_health < previous_health - 5:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            'trend': trend,
            'recent_average': round(recent_health, 2),
            'previous_average': round(previous_health, 2)
        }
    
    async def _notify_critical_issues(self, file_path: str, issues: List[CodeIssue]):
        """Notifica sobre issues críticas"""
        from uuid import uuid4
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.CRITICAL,
            content={
                'notification_type': 'critical_code_issues',
                'file_path': file_path,
                'issues': [self._issue_to_dict(issue) for issue in issues],
                'recommendation': 'Revisão urgente necessária'
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)
    
    async def _notify_poor_code_health(self, report: Dict[str, Any]):
        """Notifica sobre saúde ruim do código"""
        from uuid import uuid4
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="web_search_001",  # Solicitar busca por soluções
            message_type=MessageType.REQUEST,
            priority=Priority.HIGH,
            content={
                'request_type': 'search_solutions',
                'problems': report['top_problems'],
                'context': 'poor_code_health'
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)
    
    def _get_latest_report(self) -> Dict[str, Any]:
        """Retorna relatório mais recente"""
        if not self.analysis_history:
            return {
                'status': 'no_data',
                'message': 'Nenhuma análise realizada ainda'
            }
        
        return {
            'status': 'completed',
            'latest_analysis': self.analysis_history[-1],
            'total_analyses': len(self.analysis_history),
            'metrics': self.analysis_metrics
        }
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
        from uuid import uuid4
        response = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            priority=original_message.priority,
            content=response_data,
            timestamp=datetime.now(),
            correlation_id=original_message.id
        )
        await self.message_bus.publish(response)

# Importações necessárias
from uuid import uuid4
import time

def create_code_analyzer_agent(message_bus, num_instances=1) -> List[CodeAnalyzerAgent]:
    """
    Cria agente de análise de código
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de análise de código
    """
    agents = []
    
    try:
        logger.info("🔍 Criando CodeAnalyzerAgent para autoevolução...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "code_analyzer_001"
        
        if agent_id not in existing_agents:
            try:
                agent = CodeAnalyzerAgent(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar serviços de análise
                asyncio.create_task(agent.start_analysis_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com análise avançada de código")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de análise de código criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando CodeAnalyzerAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
