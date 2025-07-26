#!/usr/bin/env python3
"""
Testing Agent - Agente de Testes Automatizados Avançado
Executa testes, monitora cobertura e detecta regressões
"""

import logging
import ast
import os
import sys
import subprocess
import pytest
import coverage
import unittest
import time
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import importlib.util
import traceback
from multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class TestType(Enum):
    """Tipos de testes"""
    UNIT = "unit"
    INTEGRATION = "integration"
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    REGRESSION = "regression"
    SMOKE = "smoke"
    ACCEPTANCE = "acceptance"
    SECURITY = "security"

class TestStatus(Enum):
    """Status dos testes"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    TIMEOUT = "timeout"

class CoverageLevel(Enum):
    """Níveis de cobertura"""
    EXCELLENT = "excellent"    # > 90%
    GOOD = "good"             # 80-90%
    ACCEPTABLE = "acceptable"  # 70-80%
    POOR = "poor"             # 50-70%
    CRITICAL = "critical"     # < 50%

@dataclass
class TestCase:
    """Caso de teste individual"""
    test_id: str
    name: str
    test_type: TestType
    file_path: str
    function_name: str
    description: str
    status: TestStatus = TestStatus.PENDING
    execution_time: float = 0.0
    error_message: Optional[str] = None
    assertions: int = 0
    coverage_data: Dict[str, float] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_run: Optional[datetime] = None

@dataclass
class TestSuite:
    """Suíte de testes"""
    suite_id: str
    name: str
    test_cases: List[TestCase] = field(default_factory=list)
    status: TestStatus = TestStatus.PENDING
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    execution_time: float = 0.0
    coverage_percentage: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class CoverageReport:
    """Relatório de cobertura"""
    report_id: str
    file_path: str
    total_lines: int
    covered_lines: int
    missed_lines: int
    coverage_percentage: float
    uncovered_lines: List[int] = field(default_factory=list)
    branch_coverage: float = 0.0
    function_coverage: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class RegressionResult:
    """Resultado de teste de regressão"""
    regression_id: str
    baseline_version: str
    current_version: str
    regression_detected: bool
    failed_tests: List[str] = field(default_factory=list)
    performance_changes: Dict[str, float] = field(default_factory=dict)
    new_failures: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

class TestingAgent(BaseNetworkAgent):
    """Agente especializado em testes automatizados e validação"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'automated_testing',
            'code_coverage',
            'regression_testing',
            'performance_testing',
            'test_generation',
            'quality_assurance',
            'continuous_testing',
            'test_reporting'
        ]
        self.status = 'active'
        
        # Estado do agente
        self.test_queue = asyncio.Queue()
        self.test_suites = {}  # suite_id -> TestSuite
        self.test_history = []
        self.coverage_reports = {}  # file_path -> CoverageReport
        self.regression_baselines = {}  # version -> test results
        
        # Configurações
        self.test_timeout = 300  # 5 minutos
        self.coverage_threshold = 80.0  # 80% mínimo
        self.max_concurrent_tests = 5
        self.auto_generate_tests = True
        self.continuous_testing = True
        
        # Diretórios
        self.test_directory = Path('./tests')
        self.coverage_directory = Path('./coverage')
        self.reports_directory = Path('./test_reports')
        
        # Criar diretórios se não existirem
        for directory in [self.test_directory, self.coverage_directory, self.reports_directory]:
            directory.mkdir(exist_ok=True)
        
        # Configurar coverage
        self.coverage_instance = coverage.Coverage(
            source=['.'],
            omit=['*/tests/*', '*/venv/*', '*/__pycache__/*']
        )
        
        # Métricas
        self.testing_metrics = {
            'tests_executed': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'coverage_reports_generated': 0,
            'regressions_detected': 0,
            'auto_generated_tests': 0
        }
        
        # Tasks de background
        self._testing_task = None
        self._monitoring_task = None
        self._coverage_task = None
        
        logger.info(f"🧪 {self.agent_id} inicializado com testes automatizados")
    
    async def start_testing_service(self):
        """Inicia serviços de teste"""
        if not self._testing_task:
            self._testing_task = asyncio.create_task(self._testing_loop())
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            self._coverage_task = asyncio.create_task(self._coverage_loop())
            logger.info(f"🧪 {self.agent_id} iniciou serviços de teste")
    
    async def stop_testing_service(self):
        """Para serviços de teste"""
        if self._testing_task:
            self._testing_task.cancel()
            self._testing_task = None
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
        if self._coverage_task:
            self._coverage_task.cancel()
            self._coverage_task = None
        logger.info(f"🛑 {self.agent_id} parou serviços de teste")
    
    async def _testing_loop(self):
        """Loop principal de execução de testes"""
        while True:
            try:
                # Processar fila de testes
                if not self.test_queue.empty():
                    test_request = await self.test_queue.get()
                    await self._process_test_request(test_request)
                
                # Teste contínuo (se habilitado)
                if self.continuous_testing:
                    await self._run_continuous_tests()
                
                await asyncio.sleep(10)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de testes: {e}")
    
    async def _monitoring_loop(self):
        """Loop de monitoramento de arquivos para testes automáticos"""
        while True:
            try:
                # Monitorar mudanças em arquivos
                changed_files = await self._detect_file_changes()
                
                if changed_files:
                    await self._trigger_tests_for_files(changed_files)
                
                await asyncio.sleep(30)  # Verificar a cada 30 segundos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento: {e}")
    
    async def _coverage_loop(self):
        """Loop de análise de cobertura"""
        while True:
            try:
                # Gerar relatórios de cobertura periodicamente
                await self._generate_coverage_reports()
                
                # Verificar se cobertura está abaixo do threshold
                await self._check_coverage_thresholds()
                
                await asyncio.sleep(300)  # A cada 5 minutos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na análise de cobertura: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'run_tests':
                result = await self.run_tests(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'generate_tests':
                result = await self.generate_tests(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'coverage_report':
                result = await self.generate_coverage_report(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'regression_test':
                result = await self.run_regression_tests(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'test_status':
                result = self.get_test_status(message.content)
                await self._send_response(message, result)
        
        elif message.message_type == MessageType.NOTIFICATION:
            # Processar notificações de mudanças de código
            if message.content.get('notification_type') == 'code_changed':
                await self._handle_code_change_notification(message.content)
    
    async def run_tests(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa testes especificados"""
        try:
            test_pattern = request_data.get('pattern', 'test_*.py')
            test_type = TestType(request_data.get('type', 'unit'))
            timeout = request_data.get('timeout', self.test_timeout)
            
            logger.info(f"🧪 Executando testes: {test_pattern}")
            
            # Criar suíte de teste
            suite_id = f"suite_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            test_suite = TestSuite(
                suite_id=suite_id,
                name=f"Test Run - {test_pattern}"
            )
            
            # Descobrir testes
            test_files = await self._discover_tests(test_pattern)
            
            if not test_files:
                return {
                    'status': 'error',
                    'message': f'Nenhum teste encontrado para padrão: {test_pattern}'
                }
            
            # Executar testes com cobertura
            self.coverage_instance.start()
            
            execution_results = []
            start_time = time.time()
            
            for test_file in test_files:
                result = await self._execute_test_file(test_file, test_type, timeout)
                execution_results.append(result)
                
                # Criar casos de teste
                for test_case_data in result.get('test_cases', []):
                    test_case = TestCase(
                        test_id=f"test_{len(test_suite.test_cases)}",
                        name=test_case_data['name'],
                        test_type=test_type,
                        file_path=test_file,
                        function_name=test_case_data['function'],
                        description=test_case_data.get('description', ''),
                        status=TestStatus(test_case_data['status']),
                        execution_time=test_case_data['time'],
                        error_message=test_case_data.get('error'),
                        assertions=test_case_data.get('assertions', 0)
                    )
                    test_suite.test_cases.append(test_case)
            
            self.coverage_instance.stop()
            
            # Calcular estatísticas da suíte
            test_suite.total_tests = len(test_suite.test_cases)
            test_suite.passed_tests = sum(1 for tc in test_suite.test_cases if tc.status == TestStatus.PASSED)
            test_suite.failed_tests = sum(1 for tc in test_suite.test_cases if tc.status == TestStatus.FAILED)
            test_suite.execution_time = time.time() - start_time
            
            if test_suite.failed_tests == 0:
                test_suite.status = TestStatus.PASSED
            else:
                test_suite.status = TestStatus.FAILED
            
            # Salvar suíte
            self.test_suites[suite_id] = test_suite
            self.test_history.append(test_suite)
            
            # Atualizar métricas
            self.testing_metrics['tests_executed'] += test_suite.total_tests
            self.testing_metrics['tests_passed'] += test_suite.passed_tests
            self.testing_metrics['tests_failed'] += test_suite.failed_tests
            
            # Gerar relatório de cobertura
            coverage_report = await self._generate_coverage_for_suite(test_suite)
            
            return {
                'status': 'completed',
                'suite_id': suite_id,
                'total_tests': test_suite.total_tests,
                'passed': test_suite.passed_tests,
                'failed': test_suite.failed_tests,
                'execution_time': test_suite.execution_time,
                'coverage': coverage_report,
                'results': execution_results
            }
            
        except Exception as e:
            logger.error(f"❌ Erro executando testes: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _discover_tests(self, pattern: str) -> List[str]:
        """Descobre arquivos de teste"""
        test_files = []
        
        # Procurar no diretório de testes
        for test_file in self.test_directory.glob(pattern):
            if test_file.is_file() and test_file.suffix == '.py':
                test_files.append(str(test_file))
        
        # Procurar em outros diretórios
        for py_file in Path('.').rglob(pattern):
            if py_file.is_file() and 'test' in py_file.name:
                test_files.append(str(py_file))
        
        return list(set(test_files))  # Remover duplicatas
    
    async def _execute_test_file(self, test_file: str, test_type: TestType, timeout: int) -> Dict[str, Any]:
        """Executa um arquivo de teste específico"""
        try:
            logger.info(f"🔬 Executando teste: {test_file}")
            
            # Executar com pytest
            cmd = [
                sys.executable, '-m', 'pytest',
                test_file,
                '-v',
                '--tb=short',
                '--json-report',
                f'--json-report-file={self.reports_directory}/result_{Path(test_file).stem}.json'
            ]
            
            # Executar comando
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd='.'
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                return {
                    'file': test_file,
                    'status': 'timeout',
                    'error': f'Teste excedeu {timeout} segundos'
                }
            
            # Processar resultado
            return await self._parse_test_results(test_file, stdout, stderr, process.returncode)
            
        except Exception as e:
            logger.error(f"❌ Erro executando {test_file}: {e}")
            return {
                'file': test_file,
                'status': 'error',
                'error': str(e)
            }
    
    async def _parse_test_results(self, test_file: str, stdout: bytes, stderr: bytes, returncode: int) -> Dict[str, Any]:
        """Analisa resultados dos testes"""
        result = {
            'file': test_file,
            'test_cases': [],
            'summary': {},
            'output': stdout.decode('utf-8', errors='ignore'),
            'errors': stderr.decode('utf-8', errors='ignore')
        }
        
        # Tentar carregar relatório JSON do pytest
        json_report_file = self.reports_directory / f'result_{Path(test_file).stem}.json'
        
        if json_report_file.exists():
            try:
                with open(json_report_file, 'r') as f:
                    json_data = json.load(f)
                
                result['summary'] = json_data.get('summary', {})
                
                # Processar casos de teste
                for test in json_data.get('tests', []):
                    test_case = {
                        'name': test.get('nodeid', ''),
                        'function': test.get('name', ''),
                        'status': 'passed' if test.get('outcome') == 'passed' else 'failed',
                        'time': test.get('duration', 0),
                        'error': test.get('call', {}).get('longrepr') if test.get('outcome') == 'failed' else None,
                        'assertions': self._count_assertions(test_file, test.get('name', ''))
                    }
                    result['test_cases'].append(test_case)
                
                # Limpar arquivo temporário
                json_report_file.unlink()
                
            except Exception as e:
                logger.error(f"❌ Erro processando relatório JSON: {e}")
        
        # Fallback: análise manual da saída
        if not result['test_cases']:
            result['test_cases'] = self._parse_output_manually(result['output'])
        
        return result
    
    def _count_assertions(self, file_path: str, function_name: str) -> int:
        """Conta asserções em uma função de teste"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    assertions = 0
                    for child in ast.walk(node):
                        if isinstance(child, ast.Assert):
                            assertions += 1
                        elif isinstance(child, ast.Call):
                            # Contar chamadas assert_*
                            if hasattr(child.func, 'attr') and child.func.attr.startswith('assert'):
                                assertions += 1
                    return assertions
            
            return 0
        except:
            return 0
    
    def _parse_output_manually(self, output: str) -> List[Dict[str, Any]]:
        """Analisa saída manualmente quando JSON não está disponível"""
        test_cases = []
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            if '::' in line and ('PASSED' in line or 'FAILED' in line):
                parts = line.split('::')
                if len(parts) >= 2:
                    test_name = parts[-1].split()[0]
                    status = 'passed' if 'PASSED' in line else 'failed'
                    
                    test_case = {
                        'name': line,
                        'function': test_name,
                        'status': status,
                        'time': 0.0,
                        'error': None if status == 'passed' else 'Test failed',
                        'assertions': 1
                    }
                    test_cases.append(test_case)
        
        return test_cases
    
    async def generate_tests(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera testes automaticamente para um arquivo"""
        try:
            file_path = request_data.get('file_path')
            test_type = request_data.get('test_type', 'unit')
            
            if not file_path or not os.path.exists(file_path):
                return {
                    'status': 'error',
                    'message': 'Arquivo não encontrado'
                }
            
            logger.info(f"🤖 Gerando testes para: {file_path}")
            
            # Analisar código
            code_analysis = await self._analyze_code_for_testing(file_path)
            
            # Gerar testes
            generated_tests = await self._generate_test_code(file_path, code_analysis, test_type)
            
            # Salvar arquivo de teste
            test_file_path = await self._save_generated_tests(file_path, generated_tests)
            
            self.testing_metrics['auto_generated_tests'] += len(generated_tests.get('test_functions', []))
            
            return {
                'status': 'completed',
                'file_path': file_path,
                'test_file': test_file_path,
                'generated_tests': len(generated_tests.get('test_functions', [])),
                'test_functions': [t['name'] for t in generated_tests.get('test_functions', [])],
                'coverage_potential': generated_tests.get('coverage_estimate', 0)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro gerando testes: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _analyze_code_for_testing(self, file_path: str) -> Dict[str, Any]:
        """Analisa código para determinar que testes gerar"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            analysis = {
                'functions': [],
                'classes': [],
                'imports': [],
                'complexity': 0
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'returns': True if node.returns else False,
                        'docstring': ast.get_docstring(node),
                        'line_number': node.lineno,
                        'complexity': self._calculate_complexity(node)
                    }
                    analysis['functions'].append(func_info)
                    analysis['complexity'] += func_info['complexity']
                
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'methods': [],
                        'docstring': ast.get_docstring(node),
                        'line_number': node.lineno
                    }
                    
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_info['methods'].append(item.name)
                    
                    analysis['classes'].append(class_info)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis['imports'].append(alias.name)
                    else:
                        analysis['imports'].append(node.module)
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Erro analisando código: {e}")
            return {}
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calcula complexidade de uma função"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
        return complexity
    
    async def _generate_test_code(self, file_path: str, analysis: Dict[str, Any], test_type: str) -> Dict[str, Any]:
        """Gera código de teste baseado na análise"""
        test_functions = []
        imports_needed = set(['import unittest', 'import pytest'])
        
        # Adicionar import do módulo sendo testado
        module_name = Path(file_path).stem
        imports_needed.add(f'from {module_name} import *')
        
        # Gerar testes para funções
        for func in analysis.get('functions', []):
            if not func['name'].startswith('_'):  # Pular métodos privados
                test_func = await self._generate_function_test(func, test_type)
                if test_func:
                    test_functions.append(test_func)
        
        # Gerar testes para classes
        for cls in analysis.get('classes', []):
            test_class = await self._generate_class_test(cls, test_type)
            if test_class:
                test_functions.append(test_class)
        
        return {
            'imports': list(imports_needed),
            'test_functions': test_functions,
            'coverage_estimate': min(95, len(test_functions) * 10)  # Estimativa simples
        }
    
    async def _generate_function_test(self, func_info: Dict[str, Any], test_type: str) -> Dict[str, Any]:
        """Gera teste para uma função específica"""
        func_name = func_info['name']
        args = func_info['args']
        
        # Gerar valores de teste baseados nos argumentos
        test_args = []
        for arg in args:
            if arg == 'self':
                continue
            # Valores padrão baseados no nome do argumento
            if 'id' in arg.lower():
                test_args.append('1')
            elif 'name' in arg.lower() or 'str' in arg.lower():
                test_args.append('"test_value"')
            elif 'num' in arg.lower() or 'count' in arg.lower():
                test_args.append('10')
            elif 'list' in arg.lower():
                test_args.append('[1, 2, 3]')
            elif 'dict' in arg.lower():
                test_args.append('{"key": "value"}')
            else:
                test_args.append('None')
        
        # Template de teste
        test_code = f"""
def test_{func_name}():
    \"\"\"Test for {func_name} function\"\"\"
    # Arrange
    {', '.join(f'{args[i]} = {test_args[i]}' for i in range(len(args)) if args[i] != 'self')}
    
    # Act
    result = {func_name}({', '.join(arg for arg in args if arg != 'self')})
    
    # Assert
    assert result is not None
    # TODO: Add more specific assertions
"""
        
        return {
            'name': f'test_{func_name}',
            'code': test_code.strip(),
            'type': test_type,
            'target_function': func_name
        }
    
    async def _generate_class_test(self, class_info: Dict[str, Any], test_type: str) -> Dict[str, Any]:
        """Gera teste para uma classe"""
        class_name = class_info['name']
        methods = class_info['methods']
        
        test_code = f"""
class Test{class_name}:
    \"\"\"Test suite for {class_name} class\"\"\"
    
    def setup_method(self):
        \"\"\"Setup method called before each test\"\"\"
        self.instance = {class_name}()
    
    def test_{class_name.lower()}_initialization(self):
        \"\"\"Test {class_name} initialization\"\"\"
        assert self.instance is not None
        assert isinstance(self.instance, {class_name})
"""
        
        # Adicionar testes para métodos públicos
        for method in methods:
            if not method.startswith('_') and method != '__init__':
                test_code += f"""
    
    def test_{method}(self):
        \"\"\"Test {method} method\"\"\"
        # TODO: Implement test for {method}
        result = self.instance.{method}()
        assert result is not None
"""
        
        return {
            'name': f'Test{class_name}',
            'code': test_code.strip(),
            'type': 'class_test',
            'target_class': class_name
        }
    
    async def _save_generated_tests(self, original_file: str, generated_tests: Dict[str, Any]) -> str:
        """Salva testes gerados em arquivo"""
        # Determinar nome do arquivo de teste
        original_path = Path(original_file)
        test_filename = f"test_{original_path.stem}.py"
        test_file_path = self.test_directory / test_filename
        
        # Construir conteúdo do arquivo
        content = '#!/usr/bin/env python3\n'
        content += '"""\n'
        content += f'Testes gerados automaticamente para {original_file}\n'
        content += f'Gerado em: {datetime.now().isoformat()}\n'
        content += '"""\n\n'
        
        # Adicionar imports
        for imp in generated_tests.get('imports', []):
            content += f'{imp}\n'
        content += '\n'
        
        # Adicionar testes
        for test_func in generated_tests.get('test_functions', []):
            content += test_func['code'] + '\n\n'
        
        # Adicionar main
        content += '''
if __name__ == '__main__':
    pytest.main([__file__])
'''
        
        # Salvar arquivo
        with open(test_file_path, 'w') as f:
            f.write(content)
        
        logger.info(f"✅ Testes salvos em: {test_file_path}")
        return str(test_file_path)
    
    async def generate_coverage_report(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera relatório de cobertura"""
        try:
            target_files = request_data.get('files', [])
            format_type = request_data.get('format', 'json')  # json, html, xml
            
            logger.info(f"📊 Gerando relatório de cobertura")
            
            # Se não especificados, usar todos os arquivos Python
            if not target_files:
                target_files = list(Path('.').glob('**/*.py'))
                target_files = [str(f) for f in target_files if 'test' not in str(f)]
            
            # Executar testes com cobertura
            self.coverage_instance.start()
            
            # Descobrir e executar todos os testes
            test_files = await self._discover_tests('test_*.py')
            for test_file in test_files:
                await self._execute_test_file(test_file, TestType.UNIT, self.test_timeout)
            
            self.coverage_instance.stop()
            
            # Gerar relatório
            coverage_data = {}
            total_statements = 0
            total_missing = 0
            
            for file_path in target_files:
                try:
                    analysis = self.coverage_instance.analysis2(file_path)
                    statements, missing, excluded, missing_lines = analysis[:4]
                    
                    coverage_percentage = 0
                    if statements > 0:
                        coverage_percentage = ((statements - len(missing_lines)) / statements) * 100
                    
                    file_report = CoverageReport(
                        report_id=f"cov_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        file_path=file_path,
                        total_lines=statements,
                        covered_lines=statements - len(missing_lines),
                        missed_lines=len(missing_lines),
                        coverage_percentage=coverage_percentage,
                        uncovered_lines=list(missing_lines)
                    )
                    
                    coverage_data[file_path] = file_report
                    total_statements += statements
                    total_missing += len(missing_lines)
                    
                except Exception as e:
                    logger.error(f"❌ Erro analisando cobertura de {file_path}: {e}")
            
            # Calcular cobertura total
            overall_coverage = 0
            if total_statements > 0:
                overall_coverage = ((total_statements - total_missing) / total_statements) * 100
            
            # Salvar relatórios
            self.coverage_reports.update(coverage_data)
            self.testing_metrics['coverage_reports_generated'] += 1
            
            # Gerar arquivo de relatório
            report_file = await self._save_coverage_report(coverage_data, overall_coverage, format_type)
            
            return {
                'status': 'completed',
                'overall_coverage': round(overall_coverage, 2),
                'coverage_level': self._determine_coverage_level(overall_coverage).value,
                'files_analyzed': len(coverage_data),
                'report_file': report_file,
                'file_coverage': {
                    path: {
                        'coverage': round(report.coverage_percentage, 2),
                        'covered_lines': report.covered_lines,
                        'total_lines': report.total_lines,
                        'uncovered_lines': len(report.uncovered_lines)
                    }
                    for path, report in coverage_data.items()
                },
                'recommendations': self._generate_coverage_recommendations(coverage_data, overall_coverage)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro gerando relatório de cobertura: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _determine_coverage_level(self, coverage_percentage: float) -> CoverageLevel:
        """Determina nível de cobertura"""
        if coverage_percentage >= 90:
            return CoverageLevel.EXCELLENT
        elif coverage_percentage >= 80:
            return CoverageLevel.GOOD
        elif coverage_percentage >= 70:
            return CoverageLevel.ACCEPTABLE
        elif coverage_percentage >= 50:
            return CoverageLevel.POOR
        else:
            return CoverageLevel.CRITICAL
    
    def _generate_coverage_recommendations(self, coverage_data: Dict[str, CoverageReport], overall_coverage: float) -> List[str]:
        """Gera recomendações baseadas na cobertura"""
        recommendations = []
        
        # Recomendações gerais
        if overall_coverage < 70:
            recommendations.append("Cobertura geral baixa - adicionar mais testes")
        
        # Identificar arquivos com baixa cobertura
        low_coverage_files = [
            path for path, report in coverage_data.items()
            if report.coverage_percentage < 70
        ]
        
        if low_coverage_files:
            recommendations.append(f"Focar em {len(low_coverage_files)} arquivos com baixa cobertura")
            for file_path in low_coverage_files[:3]:  # Top 3
                recommendations.append(f"Aumentar cobertura de {Path(file_path).name}")
        
        # Recomendações específicas
        if overall_coverage > 90:
            recommendations.append("Excelente cobertura! Manter qualidade dos testes")
        elif overall_coverage > 80:
            recommendations.append("Boa cobertura - focar em casos edge")
        
        return recommendations[:5]
    
    async def _save_coverage_report(self, coverage_data: Dict[str, CoverageReport], overall_coverage: float, format_type: str) -> str:
        """Salva relatório de cobertura"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type == 'html':
            # Gerar relatório HTML
            html_dir = self.coverage_directory / f'html_{timestamp}'
            html_dir.mkdir(exist_ok=True)
            
            self.coverage_instance.html_report(directory=str(html_dir))
            return str(html_dir / 'index.html')
        
        elif format_type == 'xml':
            # Gerar relatório XML
            xml_file = self.coverage_directory / f'coverage_{timestamp}.xml'
            self.coverage_instance.xml_report(outfile=str(xml_file))
            return str(xml_file)
        
        else:
            # Relatório JSON
            json_file = self.coverage_directory / f'coverage_{timestamp}.json'
            
            report_data = {
                'timestamp': datetime.now().isoformat(),
                'overall_coverage': overall_coverage,
                'files': {
                    path: {
                        'coverage_percentage': report.coverage_percentage,
                        'total_lines': report.total_lines,
                        'covered_lines': report.covered_lines,
                        'missed_lines': report.missed_lines,
                        'uncovered_lines': report.uncovered_lines
                    }
                    for path, report in coverage_data.items()
                }
            }
            
            with open(json_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            return str(json_file)
    
    async def run_regression_tests(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa testes de regressão"""
        try:
            baseline_version = request_data.get('baseline_version', 'previous')
            current_version = request_data.get('current_version', 'current')
            
            logger.info(f"🔄 Executando testes de regressão: {baseline_version} vs {current_version}")
            
            # Executar testes atuais
            current_results = await self.run_tests({'pattern': 'test_*.py', 'type': 'regression'})
            
            # Comparar com baseline (se disponível)
            regression_result = RegressionResult(
                regression_id=f"regression_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                baseline_version=baseline_version,
                current_version=current_version,
                regression_detected=False
            )
            
            if baseline_version in self.regression_baselines:
                baseline_data = self.regression_baselines[baseline_version]
                
                # Comparar resultados
                regression_analysis = self._compare_test_results(baseline_data, current_results)
                regression_result.regression_detected = regression_analysis['regression_detected']
                regression_result.failed_tests = regression_analysis['new_failures']
                regression_result.new_failures = regression_analysis['newly_failing']
                regression_result.performance_changes = regression_analysis['performance_changes']
            
            # Salvar como nova baseline
            self.regression_baselines[current_version] = current_results
            
            if regression_result.regression_detected:
                self.testing_metrics['regressions_detected'] += 1
                await self._notify_regression_detected(regression_result)
            
            return {
                'status': 'completed',
                'regression_id': regression_result.regression_id,
                'regression_detected': regression_result.regression_detected,
                'failed_tests': regression_result.failed_tests,
                'new_failures': len(regression_result.new_failures),
                'performance_changes': regression_result.performance_changes,
                'current_results': current_results
            }
            
        except Exception as e:
            logger.error(f"❌ Erro em testes de regressão: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _compare_test_results(self, baseline: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
        """Compara resultados de testes para detectar regressões"""
        analysis = {
            'regression_detected': False,
            'new_failures': [],
            'newly_failing': [],
            'performance_changes': {}
        }
        
        baseline_failed = set()
        current_failed = set()
        
        # Extrair testes falhando
        for result in baseline.get('results', []):
            for test_case in result.get('test_cases', []):
                if test_case['status'] == 'failed':
                    baseline_failed.add(test_case['name'])
        
        for result in current.get('results', []):
            for test_case in result.get('test_cases', []):
                if test_case['status'] == 'failed':
                    current_failed.add(test_case['name'])
        
        # Detectar novos failures
        newly_failing = current_failed - baseline_failed
        if newly_failing:
            analysis['regression_detected'] = True
            analysis['newly_failing'] = list(newly_failing)
        
        # Comparar performance
        baseline_time = baseline.get('execution_time', 0)
        current_time = current.get('execution_time', 0)
        
        if baseline_time > 0:
            time_change = ((current_time - baseline_time) / baseline_time) * 100
            if abs(time_change) > 20:  # Mudança > 20%
                analysis['performance_changes']['execution_time'] = time_change
        
        analysis['new_failures'] = list(current_failed)
        
        return analysis
    
    async def _notify_regression_detected(self, regression_result: RegressionResult):
        """Notifica sobre regressão detectada"""
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.HIGH,
            content={
                'notification_type': 'regression_detected',
                'regression_id': regression_result.regression_id,
                'new_failures': len(regression_result.new_failures),
                'failed_tests': regression_result.failed_tests[:5],  # Top 5
                'recommendation': 'Investigar e corrigir regressões antes do deploy'
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)
    
    def get_test_status(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna status dos testes"""
        return {
            'status': 'active',
            'total_suites': len(self.test_suites),
            'recent_results': len(self.test_history),
            'metrics': self.testing_metrics,
            'coverage_reports': len(self.coverage_reports),
            'regression_baselines': len(self.regression_baselines),
            'last_test_run': self.test_history[-1].created_at.isoformat() if self.test_history else None
        }
    
    async def _detect_file_changes(self) -> List[str]:
        """Detecta mudanças em arquivos (simulado)"""
        # Em produção, isso seria implementado com watchdog ou similar
        return []
    
    async def _trigger_tests_for_files(self, changed_files: List[str]):
        """Aciona testes para arquivos modificados"""
        for file_path in changed_files:
            if file_path.endswith('.py') and 'test' not in file_path:
                # Procurar testes relacionados
                potential_test = f"test_{Path(file_path).stem}.py"
                if (self.test_directory / potential_test).exists():
                    await self.test_queue.put({
                        'type': 'file_change_test',
                        'file_path': file_path,
                        'test_file': str(self.test_directory / potential_test)
                    })
    
    async def _run_continuous_tests(self):
        """Executa testes contínuos"""
        # Executar smoke tests a cada ciclo
        if len(self.test_history) == 0 or (datetime.now() - self.test_history[-1].created_at).seconds > 600:
            await self.test_queue.put({
                'type': 'continuous_smoke',
                'pattern': 'test_smoke_*.py'
            })
    
    async def _process_test_request(self, request: Dict[str, Any]):
        """Processa requisição de teste da fila"""
        request_type = request.get('type')
        
        if request_type == 'file_change_test':
            # Executar teste específico
            test_file = request.get('test_file')
            await self._execute_test_file(test_file, TestType.UNIT, self.test_timeout)
        
        elif request_type == 'continuous_smoke':
            # Executar smoke tests
            pattern = request.get('pattern', 'test_*.py')
            await self.run_tests({'pattern': pattern, 'type': 'smoke'})
    
    async def _generate_coverage_reports(self):
        """Gera relatórios de cobertura periódicos"""
        if self.test_history:
            await self.generate_coverage_report({'format': 'json'})
    
    async def _check_coverage_thresholds(self):
        """Verifica se cobertura está abaixo dos thresholds"""
        for file_path, report in self.coverage_reports.items():
            if report.coverage_percentage < self.coverage_threshold:
                await self._generate_coverage_alert(file_path, report)
    
    async def _generate_coverage_alert(self, file_path: str, report: CoverageReport):
        """Gera alerta de cobertura baixa"""
        alert = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="code_analyzer_001",
            message_type=MessageType.REQUEST,
            priority=Priority.MEDIUM,
            content={
                'request_type': 'generate_tests',
                'file_path': file_path,
                'current_coverage': report.coverage_percentage,
                'target_coverage': self.coverage_threshold,
                'reason': 'low_coverage_alert'
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(alert)
    
    async def _handle_code_change_notification(self, notification_data: Dict[str, Any]):
        """Trata notificação de mudança de código"""
        file_path = notification_data.get('file_path')
        change_type = notification_data.get('change_type', 'modified')
        
        if change_type in ['modified', 'added']:
            # Agendar geração de testes se necessário
            await self.test_queue.put({
                'type': 'code_change',
                'file_path': file_path,
                'auto_generate': self.auto_generate_tests
            })
    
    async def _generate_coverage_for_suite(self, test_suite: TestSuite) -> Dict[str, Any]:
        """Gera relatório de cobertura para uma suíte específica"""
        try:
            coverage_data = self.coverage_instance.get_data()
            measured_files = coverage_data.measured_files()
            
            if not measured_files:
                return {'coverage_percentage': 0, 'files_covered': 0}
            
            total_statements = 0
            total_covered = 0
            
            for filename in measured_files:
                try:
                    analysis = self.coverage_instance.analysis2(filename)
                    statements, missing, excluded, missing_lines = analysis[:4]
                    
                    total_statements += statements
                    total_covered += (statements - len(missing_lines))
                except:
                    continue
            
            coverage_percentage = 0
            if total_statements > 0:
                coverage_percentage = (total_covered / total_statements) * 100
            
            test_suite.coverage_percentage = coverage_percentage
            
            return {
                'coverage_percentage': round(coverage_percentage, 2),
                'files_covered': len(measured_files),
                'total_statements': total_statements,
                'covered_statements': total_covered
            }
            
        except Exception as e:
            logger.error(f"❌ Erro gerando cobertura para suíte: {e}")
            return {'coverage_percentage': 0, 'files_covered': 0}
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
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

def create_testing_agent(message_bus, num_instances=1) -> List[TestingAgent]:
    """
    Cria agente de testes automatizados
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de testes
    """
    agents = []
    
    try:
        logger.info("🧪 Criando TestingAgent para autoevolução...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "testing_001"
        
        if agent_id not in existing_agents:
            try:
                agent = TestingAgent(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar serviços de teste
                asyncio.create_task(agent.start_testing_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com testes automatizados")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de testes criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando TestingAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
