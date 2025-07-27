#!/usr/bin/env python3
"""
DebugMasterAgent - O Agente de Debug Supremo
Especializado em detecção, diagnóstico e correção automática de problemas
"""

import logging
import sys
import traceback
import ast
import inspect
import gc
import threading
import time
import asyncio
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json
import re
from pathlib import Path
from suna_alsham_core.debug_agent_creation import BaseNetworkAgent, AgentMessage, ...

logger = logging.getLogger(__name__)

class DebugLevel(Enum):
    """Níveis de debug"""
    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    FATAL = "fatal"

class IssueCategory(Enum):
    """Categorias de problemas"""
    SYNTAX_ERROR = "syntax_error"
    RUNTIME_ERROR = "runtime_error"
    LOGIC_ERROR = "logic_error"
    PERFORMANCE_ISSUE = "performance_issue"
    MEMORY_LEAK = "memory_leak"
    CONCURRENCY_ISSUE = "concurrency_issue"
    INTEGRATION_ERROR = "integration_error"
    CONFIGURATION_ERROR = "configuration_error"
    DEPENDENCY_ISSUE = "dependency_issue"
    NETWORK_ERROR = "network_error"

class ResolutionStrategy(Enum):
    """Estratégias de resolução"""
    AUTO_FIX = "auto_fix"
    GUIDED_FIX = "guided_fix"
    MANUAL_INTERVENTION = "manual_intervention"
    ESCALATE = "escalate"
    IGNORE = "ignore"
    MONITOR = "monitor"

@dataclass
class DebugIssue:
    """Representa um problema detectado"""
    issue_id: str
    category: IssueCategory
    level: DebugLevel
    title: str
    description: str
    location: Dict[str, Any]  # file, line, function, etc.
    stack_trace: Optional[str]
    context: Dict[str, Any]
    resolution_strategy: ResolutionStrategy
    auto_fixable: bool
    impact_assessment: str
    suggested_fixes: List[str]
    related_issues: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class DebugSession:
    """Sessão de debug"""
    session_id: str
    target: str  # file, function, or system
    issues_found: List[DebugIssue]
    fixes_applied: List[Dict[str, Any]]
    session_duration: float
    success_rate: float
    status: str
    recommendations: List[str]

@dataclass
class SystemDiagnostic:
    """Diagnóstico completo do sistema"""
    diagnostic_id: str
    system_health: str
    critical_issues: int
    warning_issues: int
    performance_score: float
    reliability_score: float
    maintainability_score: float
    security_score: float
    recommendations: List[str]
    next_check_time: datetime

class DebugMasterAgent(BaseNetworkAgent):
    """Agente supremo de debugging e diagnóstico"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'error_detection',
            'automatic_debugging',
            'issue_diagnosis',
            'auto_correction',
            'system_monitoring',
            'performance_debugging',
            'memory_analysis',
            'concurrency_debugging',
            'integration_testing',
            'regression_detection',
            'predictive_debugging',
            'intelligent_logging'
        ]
        self.status = 'active'
        
        # Estado do debug master
        self.debug_queue = asyncio.Queue()
        self.active_sessions = {}  # session_id -> DebugSession
        self.issue_database = defaultdict(list)  # category -> [issues]
        self.fix_patterns = self._load_fix_patterns()
        self.monitoring_targets = set()
        
        # Configurações avançadas
        self.auto_fix_enabled = True
        self.real_time_monitoring = True
        self.predictive_mode = True
        self.learning_mode = True
        self.max_auto_fixes_per_session = 5
        
        # Handlers especializados
        self.error_handlers = self._setup_error_handlers()
        self.fix_generators = self._setup_fix_generators()
        self.diagnostic_engines = self._setup_diagnostic_engines()
        
        # Métricas de debugging
        self.debug_metrics = {
            'issues_detected': 0,
            'auto_fixes_applied': 0,
            'success_rate': 0.0,
            'average_resolution_time': 0.0,
            'critical_issues_prevented': 0,
            'false_positives': 0
        }
        
        # Sistema de aprendizado
        self.pattern_database = defaultdict(list)
        self.solution_effectiveness = defaultdict(float)
        self.recurrent_issues = defaultdict(int)
        
        # Tasks de background
        self._monitoring_task = None
        self._diagnostic_task = None
        self._learning_task = None
        
        # Setup do sistema de debugging
        self._setup_exception_handlers()
        self._setup_real_time_monitoring()
        
        logger.info(f"🐛 {self.agent_id} inicializado como Debug Master Supremo")
    
    def _load_fix_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Carrega padrões de correção automática"""
        return {
            'import_error': [
                {
                    'pattern': r'ModuleNotFoundError: No module named \'(.+)\'',
                    'fix': 'pip install {module}',
                    'confidence': 0.9
                },
                {
                    'pattern': r'ImportError: cannot import name \'(.+)\' from \'(.+)\'',
                    'fix': 'Check import path and module structure',
                    'confidence': 0.7
                }
            ],
            'syntax_error': [
                {
                    'pattern': r'SyntaxError: invalid syntax.*line (\d+)',
                    'fix': 'Check syntax on line {line}',
                    'confidence': 0.8
                },
                {
                    'pattern': r'IndentationError: (.+)',
                    'fix': 'Fix indentation: {details}',
                    'confidence': 0.95
                }
            ],
            'type_error': [
                {
                    'pattern': r'TypeError: (.+) takes (\d+) positional arguments but (\d+) were given',
                    'fix': 'Adjust function call arguments',
                    'confidence': 0.85
                }
            ],
            'attribute_error': [
                {
                    'pattern': r'AttributeError: \'(.+)\' object has no attribute \'(.+)\'',
                    'fix': 'Check if attribute exists or use hasattr()',
                    'confidence': 0.8
                }
            ]
        }
    
    def _setup_error_handlers(self) -> Dict[IssueCategory, Callable]:
        """Configura handlers especializados por categoria"""
        return {
            IssueCategory.SYNTAX_ERROR: self._handle_syntax_error,
            IssueCategory.RUNTIME_ERROR: self._handle_runtime_error,
            IssueCategory.LOGIC_ERROR: self._handle_logic_error,
            IssueCategory.PERFORMANCE_ISSUE: self._handle_performance_issue,
            IssueCategory.MEMORY_LEAK: self._handle_memory_leak,
            IssueCategory.CONCURRENCY_ISSUE: self._handle_concurrency_issue,
            IssueCategory.INTEGRATION_ERROR: self._handle_integration_error,
            IssueCategory.CONFIGURATION_ERROR: self._handle_configuration_error,
            IssueCategory.DEPENDENCY_ISSUE: self._handle_dependency_issue,
            IssueCategory.NETWORK_ERROR: self._handle_network_error
        }
    
    def _setup_fix_generators(self) -> Dict[IssueCategory, Callable]:
        """Configura geradores de correção"""
        return {
            IssueCategory.SYNTAX_ERROR: self._generate_syntax_fix,
            IssueCategory.RUNTIME_ERROR: self._generate_runtime_fix,
            IssueCategory.LOGIC_ERROR: self._generate_logic_fix,
            IssueCategory.PERFORMANCE_ISSUE: self._generate_performance_fix,
            IssueCategory.MEMORY_LEAK: self._generate_memory_fix,
            IssueCategory.CONCURRENCY_ISSUE: self._generate_concurrency_fix
        }
    
    def _setup_diagnostic_engines(self) -> Dict[str, Callable]:
        """Configura engines de diagnóstico"""
        return {
            'static_analysis': self._static_code_analysis,
            'runtime_analysis': self._runtime_analysis,
            'memory_analysis': self._memory_analysis,
            'performance_analysis': self._performance_analysis,
            'dependency_analysis': self._dependency_analysis,
            'security_analysis': self._security_analysis
        }
    
    def _setup_exception_handlers(self):
        """Configura handlers globais de exceção"""
        def exception_handler(exc_type, exc_value, exc_traceback):
            """Handler customizado para exceções não capturadas"""
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            # Processar exceção através do debug master
            asyncio.create_task(self._process_uncaught_exception(
                exc_type, exc_value, exc_traceback
            ))
        
        sys.excepthook = exception_handler
    
    def _setup_real_time_monitoring(self):
        """Configura monitoramento em tempo real"""
        if self.real_time_monitoring:
            # Configurar logging handler personalizado
            class DebugLogHandler(logging.Handler):
                def __init__(self, debug_agent):
                    super().__init__()
                    self.debug_agent = debug_agent
                
                def emit(self, record):
                    if record.levelno >= logging.ERROR:
                        asyncio.create_task(
                            self.debug_agent._process_log_error(record)
                        )
            
            debug_handler = DebugLogHandler(self)
            debug_handler.setLevel(logging.WARNING)
            logging.getLogger().addHandler(debug_handler)
    
    async def start_debug_services(self):
        """Inicia todos os serviços de debug"""
        if not self._monitoring_task:
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            self._diagnostic_task = asyncio.create_task(self._diagnostic_loop())
            self._learning_task = asyncio.create_task(self._learning_loop())
            logger.info(f"🐛 {self.agent_id} iniciou serviços de debug avançado")
    
    async def stop_debug_services(self):
        """Para serviços de debug"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
        if self._diagnostic_task:
            self._diagnostic_task.cancel()
            self._diagnostic_task = None
        if self._learning_task:
            self._learning_task.cancel()
            self._learning_task = None
        logger.info(f"🛑 {self.agent_id} parou serviços de debug")
    
    async def _monitoring_loop(self):
        """Loop de monitoramento contínuo"""
        while True:
            try:
                # Processar fila de debug
                if not self.debug_queue.empty():
                    debug_request = await self.debug_queue.get()
                    await self._process_debug_request(debug_request)
                
                # Monitorar targets ativos
                for target in list(self.monitoring_targets):
                    await self._monitor_target(target)
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de monitoramento: {e}")
    
    async def _diagnostic_loop(self):
        """Loop de diagnóstico periódico"""
        while True:
            try:
                # Diagnóstico completo do sistema
                diagnostic = await self._perform_system_diagnostic()
                
                # Processar resultados
                if diagnostic.critical_issues > 0:
                    await self._handle_critical_issues(diagnostic)
                
                # Relatório periódico
                await self._send_diagnostic_report(diagnostic)
                
                await asyncio.sleep(300)  # A cada 5 minutos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no diagnóstico: {e}")
    
    async def _learning_loop(self):
        """Loop de aprendizado contínuo"""
        while True:
            try:
                # Analisar padrões de problemas
                await self._analyze_issue_patterns()
                
                # Atualizar eficácia de soluções
                await self._update_solution_effectiveness()
                
                # Detectar problemas recorrentes
                await self._detect_recurring_issues()
                
                await asyncio.sleep(600)  # A cada 10 minutos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no aprendizado: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'debug_issue':
                result = await self.debug_issue(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'system_diagnostic':
                result = await self.perform_diagnostic(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'auto_fix':
                result = await self.auto_fix_issue(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'start_monitoring':
                result = await self.start_monitoring(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'predictive_debug':
                result = await self.predictive_debug(message.content)
                await self._send_response(message, result)
        
        elif message.message_type == MessageType.NOTIFICATION:
            # Processar notificações de erros de outros agentes
            if message.content.get('notification_type') == 'error_occurred':
                await self._handle_external_error(message.content)
    
    async def debug_issue(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Debug principal de um problema"""
        try:
            issue_description = request_data.get('issue_description', '')
            file_path = request_data.get('file_path')
            error_details = request_data.get('error_details', {})
            
            logger.info(f"🐛 Debugando: {issue_description}")
            
            # Criar sessão de debug
            session = DebugSession(
                session_id=f"debug_{len(self.active_sessions)}",
                target=file_path or 'system',
                issues_found=[],
                fixes_applied=[],
                session_duration=0.0,
                success_rate=0.0,
                status='active',
                recommendations=[]
            )
            
            start_time = time.time()
            self.active_sessions[session.session_id] = session
            
            # Análise multi-dimensional
            issues = []
            
            # 1. Análise estática
            if file_path:
                static_issues = await self._static_code_analysis(file_path)
                issues.extend(static_issues)
            
            # 2. Análise de runtime
            if error_details:
                runtime_issues = await self._analyze_runtime_error(error_details)
                issues.extend(runtime_issues)
            
            # 3. Análise contextual
            contextual_issues = await self._analyze_context(request_data)
            issues.extend(contextual_issues)
            
            # 4. Análise preditiva
            if self.predictive_mode:
                predicted_issues = await self._predict_potential_issues(file_path, issues)
                issues.extend(predicted_issues)
            
            # Processar issues encontradas
            session.issues_found = issues
            auto_fixed = 0
            
            for issue in issues:
                self.debug_metrics['issues_detected'] += 1
                
                # Tentar correção automática
                if issue.auto_fixable and self.auto_fix_enabled:
                    if auto_fixed < self.max_auto_fixes_per_session:
                        fix_result = await self._attempt_auto_fix(issue)
                        if fix_result['success']:
                            session.fixes_applied.append(fix_result)
                            auto_fixed += 1
                            self.debug_metrics['auto_fixes_applied'] += 1
                
                # Adicionar ao banco de issues
                self.issue_database[issue.category].append(issue)
            
            # Finalizar sessão
            session.session_duration = time.time() - start_time
            session.success_rate = auto_fixed / max(1, len(issues))
            session.status = 'completed'
            session.recommendations = self._generate_session_recommendations(session)
            
            return {
                'status': 'completed',
                'session_id': session.session_id,
                'issues_found': len(issues),
                'auto_fixes_applied': auto_fixed,
                'success_rate': session.success_rate,
                'session_duration': session.session_duration,
                'issues': [self._issue_to_dict(issue) for issue in issues],
                'recommendations': session.recommendations
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no debug: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _static_code_analysis(self, file_path: str) -> List[DebugIssue]:
        """Análise estática avançada"""
        issues = []
        
        try:
            if not Path(file_path).exists():
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Parse AST para análise
            try:
                tree = ast.parse(code, filename=file_path)
            except SyntaxError as e:
                issue = DebugIssue(
                    issue_id=f"syntax_{len(issues)}",
                    category=IssueCategory.SYNTAX_ERROR,
                    level=DebugLevel.ERROR,
                    title="Syntax Error Detected",
                    description=str(e),
                    location={'file': file_path, 'line': e.lineno, 'column': e.offset},
                    stack_trace=None,
                    context={'error_text': e.text},
                    resolution_strategy=ResolutionStrategy.AUTO_FIX,
                    auto_fixable=True,
                    impact_assessment="Prevents code execution",
                    suggested_fixes=self._generate_syntax_fixes(e)
                )
                issues.append(issue)
                return issues
            
            # Análise de padrões problemáticos
            class IssueVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.issues = []
                
                def visit_FunctionDef(self, node):
                    # Função sem docstring
                    if not ast.get_docstring(node):
                        self.issues.append(DebugIssue(
                            issue_id=f"doc_{len(self.issues)}",
                            category=IssueCategory.LOGIC_ERROR,
                            level=DebugLevel.WARNING,
                            title="Missing Function Documentation",
                            description=f"Function '{node.name}' lacks documentation",
                            location={'file': file_path, 'line': node.lineno, 'function': node.name},
                            stack_trace=None,
                            context={'function_name': node.name},
                            resolution_strategy=ResolutionStrategy.AUTO_FIX,
                            auto_fixable=True,
                            impact_assessment="Reduces code maintainability",
                            suggested_fixes=[f"Add docstring to function '{node.name}'"]
                        ))
                    
                    # Função muito complexa
                    complexity = self._calculate_complexity(node)
                    if complexity > 10:
                        self.issues.append(DebugIssue(
                            issue_id=f"complex_{len(self.issues)}",
                            category=IssueCategory.PERFORMANCE_ISSUE,
                            level=DebugLevel.WARNING,
                            title="High Function Complexity",
                            description=f"Function '{node.name}' has complexity {complexity}",
                            location={'file': file_path, 'line': node.lineno, 'function': node.name},
                            stack_trace=None,
                            context={'complexity': complexity, 'function_name': node.name},
                            resolution_strategy=ResolutionStrategy.GUIDED_FIX,
                            auto_fixable=False,
                            impact_assessment="May cause performance and maintenance issues",
                            suggested_fixes=["Refactor into smaller functions", "Simplify logic flow"]
                        ))
                    
                    self.generic_visit(node)
                
                def visit_Try(self, node):
                    # Try sem except específico
                    for handler in node.handlers:
                        if not handler.type:  # bare except
                            self.issues.append(DebugIssue(
                                issue_id=f"bare_except_{len(self.issues)}",
                                category=IssueCategory.LOGIC_ERROR,
                                level=DebugLevel.WARNING,
                                title="Bare Except Clause",
                                description="Using bare 'except:' clause",
                                location={'file': file_path, 'line': handler.lineno},
                                stack_trace=None,
                                context={'line_content': 'except:'},
                                resolution_strategy=ResolutionStrategy.AUTO_FIX,
                                auto_fixable=True,
                                impact_assessment="May hide important errors",
                                suggested_fixes=["Use specific exception types", "Add Exception as e"]
                            ))
                    
                    self.generic_visit(node)
                
                def _calculate_complexity(self, node):
                    """Calcula complexidade ciclomática"""
                    complexity = 1
                    for child in ast.walk(node):
                        if isinstance(child, (ast.If, ast.While, ast.For)):
                            complexity += 1
                        elif isinstance(child, ast.BoolOp):
                            complexity += len(child.values) - 1
                    return complexity
            
            visitor = IssueVisitor()
            visitor.visit(tree)
            issues.extend(visitor.issues)
            
        except Exception as e:
            logger.error(f"❌ Erro na análise estática: {e}")
        
        return issues
    
    async def _analyze_runtime_error(self, error_details: Dict[str, Any]) -> List[DebugIssue]:
        """Analisa erro de runtime"""
        issues = []
        
        try:
            error_type = error_details.get('type', 'Unknown')
            error_message = error_details.get('message', '')
            stack_trace = error_details.get('stack_trace', '')
            
            # Determinar categoria
            category = self._categorize_error(error_type)
            level = self._determine_error_level(error_type, error_message)
            
            # Gerar correções sugeridas
            suggested_fixes = self._generate_error_fixes(error_type, error_message)
            
            issue = DebugIssue(
                issue_id=f"runtime_{len(issues)}",
                category=category,
                level=level,
                title=f"{error_type} Runtime Error",
                description=error_message,
                location=self._extract_location_from_stack(stack_trace),
                stack_trace=stack_trace,
                context={'error_type': error_type, 'message': error_message},
                resolution_strategy=self._determine_resolution_strategy(error_type),
                auto_fixable=self._is_auto_fixable(error_type),
                impact_assessment=self._assess_impact(error_type),
                suggested_fixes=suggested_fixes
            )
            
            issues.append(issue)
            
        except Exception as e:
            logger.error(f"❌ Erro analisando runtime error: {e}")
        
        return issues
    
    async def _analyze_context(self, request_data: Dict[str, Any]) -> List[DebugIssue]:
        """Analisa contexto adicional"""
        issues = []
        
        # Analisar ambiente
        environment_issues = await self._check_environment()
        issues.extend(environment_issues)
        
        # Analisar dependências
        dependency_issues = await self._check_dependencies()
        issues.extend(dependency_issues)
        
        # Analisar configuração
        config_issues = await self._check_configuration()
        issues.extend(config_issues)
        
        return issues
    
    async def _predict_potential_issues(self, file_path: str, current_issues: List[DebugIssue]) -> List[DebugIssue]:
        """Prediz problemas potenciais"""
        predicted_issues = []
        
        try:
            # Análise baseada em padrões históricos
            for category, historical_issues in self.issue_database.items():
                if len(historical_issues) > 5:  # Padrão estabelecido
                    # Verificar se condições similares existem
                    prediction_confidence = self._calculate_prediction_confidence(
                        file_path, current_issues, historical_issues
                    )
                    
                    if prediction_confidence > 0.7:
                        predicted_issue = DebugIssue(
                            issue_id=f"predicted_{len(predicted_issues)}",
                            category=category,
                            level=DebugLevel.INFO,
                            title=f"Predicted {category.value.title()} Issue",
                            description=f"High probability of {category.value} based on patterns",
                            location={'file': file_path, 'line': 0, 'type': 'prediction'},
                            stack_trace=None,
                            context={'prediction_confidence': prediction_confidence},
                            resolution_strategy=ResolutionStrategy.MONITOR,
                            auto_fixable=False,
                            impact_assessment="Potential future issue",
                            suggested_fixes=["Monitor for signs", "Implement preventive measures"]
                        )
                        predicted_issues.append(predicted_issue)
            
        except Exception as e:
            logger.error(f"❌ Erro na predição: {e}")
        
        return predicted_issues
    
    async def _attempt_auto_fix(self, issue: DebugIssue) -> Dict[str, Any]:
        """Tenta correção automática"""
        try:
            logger.info(f"🔧 Tentando auto-fix para: {issue.title}")
            
            # Usar gerador de fix específico
            if issue.category in self.fix_generators:
                fix_generator = self.fix_generators[issue.category]
                fix_result = await fix_generator(issue)
                
                if fix_result.get('success'):
                    # Aplicar correção
                    await self._apply_fix(issue, fix_result)
                    
                    # Verificar se correção funcionou
                    verification = await self._verify_fix(issue, fix_result)
                    
                    return {
                        'success': verification['success'],
                        'issue_id': issue.issue_id,
                        'fix_applied': fix_result['fix_description'],
                        'verification': verification
                    }
            
            return {'success': False, 'reason': 'No suitable fix generator'}
            
        except Exception as e:
            logger.error(f"❌ Erro no auto-fix: {e}")
            return {'success': False, 'reason': str(e)}
    
    async def _generate_syntax_fix(self, issue: DebugIssue) -> Dict[str, Any]:
        """Gera correção para erro de sintaxe"""
        try:
            # Análise específica do erro de sintaxe
            location = issue.location
            file_path = location.get('file')
            line_num = location.get('line', 0)
            
            if not file_path or not Path(file_path).exists():
                return {'success': False, 'reason': 'File not accessible'}
            
            # Ler arquivo e analisar linha problemática
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if line_num > len(lines):
                return {'success': False, 'reason': 'Line number out of range'}
            
            problematic_line = lines[line_num - 1] if line_num > 0 else ''
            
            # Gerar correção baseada no padrão do erro
            fix_description = "Syntax correction applied"
            corrected_line = problematic_line
            
            # Padrões comuns de correção
            if 'missing parenthesis' in issue.description.lower():
                corrected_line = self._fix_missing_parenthesis(problematic_line)
            elif 'indentation' in issue.description.lower():
                corrected_line = self._fix_indentation(problematic_line)
            elif 'quote' in issue.description.lower():
                corrected_line = self._fix_quotes(problematic_line)
            
            return {
                'success': True,
                'fix_description': fix_description,
                'original_line': problematic_line,
                'corrected_line': corrected_line,
                'line_number': line_num
            }
            
        except Exception as e:
            return {'success': False, 'reason': str(e)}
    
    def _fix_missing_parenthesis(self, line: str) -> str:
        """Corrige parênteses faltando"""
        # Contar parênteses
        open_count = line.count('(')
        close_count = line.count(')')
        
        if open_count > close_count:
            return line.rstrip() + ')' * (open_count - close_count) + '\n'
        elif close_count > open_count:
            return '(' * (close_count - open_count) + line
        
        return line
    
    def _fix_indentation(self, line: str) -> str:
        """Corrige indentação"""
        # Remover indentação incorreta e aplicar padrão
        content = line.lstrip()
        if content:
            return '    ' + content  # 4 espaços padrão
        return line
    
    def _fix_quotes(self, line: str) -> str:
        """Corrige aspas"""
        # Verificar se aspas estão balanceadas
        single_quotes = line.count("'")
        double_quotes = line.count('"')
        
        if single_quotes % 2 != 0:
            return line + "'"
        elif double_quotes % 2 != 0:
            return line + '"'
        
        return line
    
    async def _apply_fix(self, issue: DebugIssue, fix_result: Dict[str, Any]):
        """Aplica correção ao arquivo"""
        try:
            if fix_result.get('line_number') and fix_result.get('corrected_line'):
                file_path = issue.location.get('file')
                line_num = fix_result['line_number']
                
                # Backup do arquivo original
                backup_path = f"{file_path}.debug_backup"
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Aplicar correção
                lines = original_content.split('\n')
                if 0 < line_num <= len(lines):
                    lines[line_num - 1] = fix_result['corrected_line'].rstrip()
                    
                    # Escrever arquivo corrigido
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines))
                    
                    logger.info(f"✅ Correção aplicada em {file_path}:{line_num}")
                
        except Exception as e:
            logger.error(f"❌ Erro aplicando correção: {e}")
    
    async def _verify_fix(self, issue: DebugIssue, fix_result: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica se a correção funcionou"""
        try:
            file_path = issue.location.get('file')
            
            if not file_path:
                return {'success': False, 'reason': 'No file to verify'}
            
            # Tentar parse do arquivo corrigido
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                ast.parse(code, filename=file_path)
                
                return {
                    'success': True,
                    'message': 'Syntax validation passed',
                    'verification_type': 'syntax_check'
                }
                
            except SyntaxError as e:
                return {
                    'success': False,
                    'reason': f'Syntax error still present: {e}',
                    'verification_type': 'syntax_check'
                }
            
        except Exception as e:
            return {'success': False, 'reason': str(e)}
    
    # Implementar outros métodos necessários...
    def _categorize_error(self, error_type: str) -> IssueCategory:
        """Categoriza tipo de erro"""
        error_mapping = {
            'SyntaxError': IssueCategory.SYNTAX_ERROR,
            'TypeError': IssueCategory.RUNTIME_ERROR,
            'ValueError': IssueCategory.RUNTIME_ERROR,
            'AttributeError': IssueCategory.RUNTIME_ERROR,
            'ImportError': IssueCategory.DEPENDENCY_ISSUE,
            'ModuleNotFoundError': IssueCategory.DEPENDENCY_ISSUE,
            'ConnectionError': IssueCategory.NETWORK_ERROR,
            'TimeoutError': IssueCategory.NETWORK_ERROR,
            'MemoryError': IssueCategory.MEMORY_LEAK,
        }
        return error_mapping.get(error_type, IssueCategory.RUNTIME_ERROR)
    
    def _determine_error_level(self, error_type: str, message: str) -> DebugLevel:
        """Determina nível de severidade"""
        critical_errors = ['MemoryError', 'SystemExit', 'KeyboardInterrupt']
        if error_type in critical_errors:
            return DebugLevel.CRITICAL
        
        if 'fatal' in message.lower():
            return DebugLevel.FATAL
        elif any(word in message.lower() for word in ['critical', 'severe']):
            return DebugLevel.CRITICAL
        else:
            return DebugLevel.ERROR
    
    def _issue_to_dict(self, issue: DebugIssue) -> Dict[str, Any]:
        """Converte issue para dicionário"""
        return {
            'issue_id': issue.issue_id,
            'category': issue.category.value,
            'level': issue.level.value,
            'title': issue.title,
            'description': issue.description,
            'location': issue.location,
            'auto_fixable': issue.auto_fixable,
            'impact_assessment': issue.impact_assessment,
            'suggested_fixes': issue.suggested_fixes,
            'timestamp': issue.timestamp.isoformat()
        }
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta"""
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
    
    # Placeholder para outros métodos necessários
    async def _handle_syntax_error(self, issue): pass
    async def _handle_runtime_error(self, issue): pass
    async def _handle_logic_error(self, issue): pass
    async def _handle_performance_issue(self, issue): pass
    async def _handle_memory_leak(self, issue): pass
    async def _handle_concurrency_issue(self, issue): pass
    async def _handle_integration_error(self, issue): pass
    async def _handle_configuration_error(self, issue): pass
    async def _handle_dependency_issue(self, issue): pass
    async def _handle_network_error(self, issue): pass
    
    async def _generate_runtime_fix(self, issue): pass
    async def _generate_logic_fix(self, issue): pass
    async def _generate_performance_fix(self, issue): pass
    async def _generate_memory_fix(self, issue): pass
    async def _generate_concurrency_fix(self, issue): pass

# Importações necessárias
from uuid import uuid4

def create_debug_master_agent(message_bus, num_instances=1) -> List[DebugMasterAgent]:
    """
    Cria o agente Debug Master supremo
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente Debug Master
    """
    agents = []
    
    try:
        logger.info("🐛 Criando DebugMasterAgent para autoevolução suprema...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "debug_master_001"
        
        if agent_id not in existing_agents:
            try:
                agent = DebugMasterAgent(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar serviços de debug
                asyncio.create_task(agent.start_debug_services())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado como Debug Master Supremo")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} Debug Master Agent criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando DebugMasterAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
