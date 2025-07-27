import logging
import os
import ast
import re
import shutil
import asyncio
import autopep8
import black
import isort
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import difflib
import json
from pathlib import Path
from collections import defaultdict
from suna_alsham_core.code_corrector_agent import BaseNetworkAgent, AgentMessage, ...

logger = logging.getLogger(__name__)

class CorrectionType(Enum):
    """Tipos de correção"""
    SYNTAX_FIX = "syntax_fix"
    STYLE_FORMAT = "style_format"
    SECURITY_PATCH = "security_patch"
    PERFORMANCE_OPT = "performance_optimization"
    BEST_PRACTICE = "best_practice"
    REFACTORING = "refactoring"
    DOCUMENTATION = "documentation"
    TYPE_HINTS = "type_hints"
    IMPORT_CLEANUP = "import_cleanup"

class CorrectionStatus(Enum):
    """Status da correção"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

@dataclass
class CodeCorrection:
    """Representa uma correção de código"""
    correction_id: str
    file_path: str
    correction_type: CorrectionType
    description: str
    line_start: int
    line_end: int
    original_code: str
    corrected_code: str
    confidence: float
    applied: bool = False
    status: CorrectionStatus = CorrectionStatus.PENDING
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class CorrectionPlan:
    """Plano de correção para um arquivo"""
    plan_id: str
    file_path: str
    corrections: List[CodeCorrection]
    priority: Priority
    total_confidence: float
    estimated_impact: str
    risks: List[str]
    backup_path: Optional[str] = None
    status: CorrectionStatus = CorrectionStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

@dataclass
class CorrectionResult:
    """Resultado de uma correção aplicada"""
    result_id: str
    plan_id: str
    file_path: str
    corrections_applied: int
    corrections_failed: int
    backup_path: str
    diff_summary: str
    validation_passed: bool
    rollback_performed: bool = False
    performance_impact: Optional[Dict[str, float]] = None
    timestamp: datetime = field(default_factory=datetime.now)

class CodeCorrectorAgent(BaseNetworkAgent):
    """Agente especializado em aplicar correções automáticas de código"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'automatic_correction',
            'code_refactoring',
            'backup_management',
            'style_formatting',
            'security_patching',
            'performance_optimization',
            'import_optimization',
            'documentation_generation',
            'validation_testing'
        ]
        self.status = 'active'
        
        # Estado do corretor
        self.correction_queue = asyncio.Queue()
        self.correction_history = []
        self.active_plans = {}  # plan_id -> CorrectionPlan
        self.backup_directory = Path('./backups')
        self.temp_directory = Path('./temp_corrections')
        
        # Configurações
        self.max_file_size = 1024 * 1024  # 1MB
        self.auto_approve_threshold = 0.85  # Confiança mínima para aprovação automática
        self.max_corrections_per_file = 50
        self.validation_timeout = 30  # segundos
        
        # Estatísticas
        self.correction_metrics = {
            'files_corrected': 0,
            'corrections_applied': 0,
            'corrections_failed': 0,
            'rollbacks_performed': 0,
            'total_lines_changed': 0,
            'average_confidence': 0.0
        }
        
        # Padrões de correção
        self.correction_patterns = self._load_correction_patterns()
        
        # Ferramentas de formatação
        self.formatters = {
            'black': self._format_with_black,
            'autopep8': self._format_with_autopep8,
            'isort': self._format_imports_with_isort
        }
        
        # Tasks de background
        self._correction_task = None
        self._validation_task = None
        
        # Criar diretórios necessários
        self._ensure_directories()
        
        logger.info(f"🔧 {self.agent_id} inicializado com correção automática avançada")
    
    def _ensure_directories(self):
        """Garante que os diretórios necessários existem"""
        try:
            self.backup_directory.mkdir(parents=True, exist_ok=True)
            self.temp_directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Diretórios de trabalho criados")
        except Exception as e:
            logger.error(f"❌ Erro criando diretórios: {e}")
    
    def _load_correction_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Carrega padrões de correção"""
        return {
            'syntax_fixes': [
                {
                    'pattern': re.compile(r'except\s*:'),
                    'replacement': 'except Exception:',
                    'description': 'Bare except clause replaced with Exception'
                },
                {
                    'pattern': re.compile(r'print\s+([^(])'),
                    'replacement': r'print(\1)',
                    'description': 'Print statement converted to function'
                }
            ],
            'best_practices': [
                {
                    'pattern': re.compile(r'if\s+(.+)\s*==\s*True:'),
                    'replacement': r'if \1:',
                    'description': 'Simplified boolean comparison'
                },
                {
                    'pattern': re.compile(r'if\s+(.+)\s*==\s*False:'),
                    'replacement': r'if not \1:',
                    'description': 'Simplified boolean comparison'
                }
            ],
            'performance': [
                {
                    'pattern': re.compile(r'for\s+\w+\s+in\s+range\(len\((.+)\)\):'),
                    'replacement': r'for i, _ in enumerate(\1):',
                    'description': 'Use enumerate instead of range(len())'
                }
            ],
            'security': [
                {
                    'pattern': re.compile(r'eval\(([^)]+)\)'),
                    'replacement': r'ast.literal_eval(\1)',
                    'description': 'Replace eval with ast.literal_eval for safety'
                },
                {
                    'pattern': re.compile(r'pickle\.load\('),
                    'replacement': '# SECURITY WARNING: pickle.load(',
                    'description': 'Flag unsafe pickle usage'
                }
            ]
        }
    
    async def start_correction_service(self):
        """Inicia serviço de correção"""
        if not self._correction_task:
            self._correction_task = asyncio.create_task(self._correction_loop())
            self._validation_task = asyncio.create_task(self._validation_loop())
            logger.info(f"🔧 {self.agent_id} iniciou serviço de correção")
    
    async def stop_correction_service(self):
        """Para serviço de correção"""
        if self._correction_task:
            self._correction_task.cancel()
            self._correction_task = None
        if self._validation_task:
            self._validation_task.cancel()
            self._validation_task = None
        logger.info(f"🛑 {self.agent_id} parou serviço de correção")
    
    async def _correction_loop(self):
        """Loop principal de correção"""
        while True:
            try:
                if not self.correction_queue.empty():
                    correction_request = await self.correction_queue.get()
                    await self._process_correction_request(correction_request)
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de correção: {e}")
    
    async def _validation_loop(self):
        """Loop de validação de correções"""
        while True:
            try:
                # Validar planos pendentes
                pending_plans = [
                    plan for plan in self.active_plans.values()
                    if plan.status == CorrectionStatus.PENDING
                ]
                
                for plan in pending_plans:
                    await self._validate_correction_plan(plan)
                
                await asyncio.sleep(5)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de validação: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'apply_corrections':
                result = await self.apply_corrections(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'create_correction_plan':
                result = await self.create_correction_plan(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'format_code':
                result = await self.format_code(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'rollback_changes':
                result = await self.rollback_changes(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'get_correction_history':
                result = self.get_correction_history()
                await self._send_response(message, result)
    
    async def create_correction_plan(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria plano de correção baseado nas sugestões"""
        try:
            file_path = request_data.get('file_path')
            issues = request_data.get('issues', [])
            solutions = request_data.get('solutions', [])
            
            if not file_path or not os.path.exists(file_path):
                return {
                    'status': 'error',
                    'message': f'Arquivo não encontrado: {file_path}'
                }
            
            logger.info(f"📋 Criando plano de correção para {file_path}")
            
            # Analisar issues e solutions para gerar correções
            corrections = []
            
            for i, issue in enumerate(issues):
                # Encontrar solução correspondente
                solution = solutions[i] if i < len(solutions) else None
                
                if solution and solution.get('confidence_score', 0) > 0.5:
                    correction = await self._generate_correction(file_path, issue, solution)
                    if correction:
                        corrections.append(correction)
            
            if not corrections:
                return {
                    'status': 'completed',
                    'message': 'Nenhuma correção aplicável encontrada',
                    'file_path': file_path
                }
            
            # Criar plano
            plan = CorrectionPlan(
                plan_id=f"plan_{len(self.correction_history)}",
                file_path=file_path,
                corrections=corrections,
                priority=self._determine_priority(corrections),
                total_confidence=sum(c.confidence for c in corrections) / len(corrections),
                estimated_impact=self._estimate_impact(corrections),
                risks=self._identify_risks(corrections)
            )
            
            self.active_plans[plan.plan_id] = plan
            
            # Se confiança alta, aprovar automaticamente
            if plan.total_confidence >= self.auto_approve_threshold:
                await self.correction_queue.put({
                    'type': 'execute_plan',
                    'plan_id': plan.plan_id
                })
            
            return {
                'status': 'completed',
                'plan_id': plan.plan_id,
                'file_path': file_path,
                'corrections_count': len(corrections),
                'total_confidence': plan.total_confidence,
                'auto_approved': plan.total_confidence >= self.auto_approve_threshold,
                'estimated_impact': plan.estimated_impact,
                'risks': plan.risks
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando plano de correção: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _generate_correction(self, file_path: str, issue: Dict[str, Any], solution: Dict[str, Any]) -> Optional[CodeCorrection]:
        """Gera correção específica para um issue"""
        try:
            issue_type = issue.get('type', '')
            line_number = issue.get('line', 0)
            
            # Ler código original
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if line_number <= 0 or line_number > len(lines):
                return None
            
            original_line = lines[line_number - 1]
            corrected_line = original_line
            correction_type = CorrectionType.BEST_PRACTICE
            confidence = 0.5
            
            # Aplicar correção baseada no tipo
            if issue_type == 'syntax_error':
                correction_type = CorrectionType.SYNTAX_FIX
                corrected_line = self._fix_syntax_error(original_line, issue)
                confidence = 0.9
                
            elif issue_type == 'style_violation':
                correction_type = CorrectionType.STYLE_FORMAT
                corrected_line = self._fix_style_violation(original_line, issue)
                confidence = 0.95
                
            elif issue_type == 'security':
                correction_type = CorrectionType.SECURITY_PATCH
                corrected_line = self._apply_security_fix(original_line, issue, solution)
                confidence = 0.8
                
            elif issue_type == 'performance':
                correction_type = CorrectionType.PERFORMANCE_OPT
                corrected_line = self._optimize_performance(original_line, issue, solution)
                confidence = 0.7
            
            if corrected_line != original_line:
                return CodeCorrection(
                    correction_id=f"corr_{issue.get('issue_id', 'unknown')}",
                    file_path=file_path,
                    correction_type=correction_type,
                    description=issue.get('message', 'Correção aplicada'),
                    line_start=line_number,
                    line_end=line_number,
                    original_code=original_line,
                    corrected_code=corrected_line,
                    confidence=confidence * solution.get('confidence_score', 1.0)
                )
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro gerando correção: {e}")
            return None
    
    def _fix_syntax_error(self, line: str, issue: Dict[str, Any]) -> str:
        """Corrige erro de sintaxe"""
        # Aplicar padrões de correção de sintaxe
        for pattern_group in self.correction_patterns['syntax_fixes']:
            pattern = pattern_group['pattern']
            replacement = pattern_group['replacement']
            
            if pattern.search(line):
                return pattern.sub(replacement, line)
        
        return line
    
    def _fix_style_violation(self, line: str, issue: Dict[str, Any]) -> str:
        """Corrige violação de estilo"""
        # Remover trailing whitespace
        line = line.rstrip() + '\n' if line.endswith('\n') else line.rstrip()
        
        # Aplicar outras correções de estilo
        if len(line) > 100:
            # Tentar quebrar linha longa (simplificado)
            if ',' in line:
                parts = line.split(',')
                if len(parts) > 1:
                    indent = len(line) - len(line.lstrip())
                    new_line = parts[0] + ',\n'
                    for part in parts[1:]:
                        new_line += ' ' * (indent + 4) + part.strip()
                        if part != parts[-1]:
                            new_line += ','
                        new_line += '\n'
                    return new_line
        
        return line
    
    def _apply_security_fix(self, line: str, issue: Dict[str, Any], solution: Dict[str, Any]) -> str:
        """Aplica correção de segurança"""
        # Aplicar padrões de segurança
        for pattern_group in self.correction_patterns['security']:
            pattern = pattern_group['pattern']
            replacement = pattern_group['replacement']
            
            if pattern.search(line):
                return pattern.sub(replacement, line)
        
        return line
    
    def _optimize_performance(self, line: str, issue: Dict[str, Any], solution: Dict[str, Any]) -> str:
        """Otimiza performance"""
        # Aplicar padrões de performance
        for pattern_group in self.correction_patterns['performance']:
            pattern = pattern_group['pattern']
            replacement = pattern_group['replacement']
            
            if pattern.search(line):
                return pattern.sub(replacement, line)
        
        return line
    
    async def apply_corrections(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica correções de um plano"""
        try:
            plan_id = request_data.get('plan_id')
            
            if plan_id not in self.active_plans:
                return {
                    'status': 'error',
                    'message': f'Plano não encontrado: {plan_id}'
                }
            
            plan = self.active_plans[plan_id]
            
            logger.info(f"🔧 Aplicando correções do plano {plan_id}")
            
            # Criar backup
            backup_path = await self._create_backup(plan.file_path)
            plan.backup_path = backup_path
            
            # Ler código original
            with open(plan.file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            # Aplicar correções
            corrected_code = original_code
            applied_corrections = []
            failed_corrections = []
            
            # Ordenar correções por linha (reverso para não afetar offsets)
            sorted_corrections = sorted(plan.corrections, key=lambda c: c.line_start, reverse=True)
            
            for correction in sorted_corrections:
                try:
                    corrected_code, applied = await self._apply_single_correction(
                        corrected_code, correction
                    )
                    
                    if applied:
                        correction.applied = True
                        correction.status = CorrectionStatus.COMPLETED
                        applied_corrections.append(correction)
                    else:
                        correction.status = CorrectionStatus.FAILED
                        failed_corrections.append(correction)
                        
                except Exception as e:
                    logger.error(f"❌ Erro aplicando correção {correction.correction_id}: {e}")
                    correction.status = CorrectionStatus.FAILED
                    correction.error_message = str(e)
                    failed_corrections.append(correction)
            
            # Validar código corrigido
            validation_passed = await self._validate_corrected_code(corrected_code, original_code)
            
            if validation_passed and applied_corrections:
                # Salvar código corrigido
                with open(plan.file_path, 'w', encoding='utf-8') as f:
                    f.write(corrected_code)
                
                # Gerar diff
                diff_summary = self._generate_diff_summary(original_code, corrected_code)
                
                # Criar resultado
                result = CorrectionResult(
                    result_id=f"result_{plan_id}",
                    plan_id=plan_id,
                    file_path=plan.file_path,
                    corrections_applied=len(applied_corrections),
                    corrections_failed=len(failed_corrections),
                    backup_path=backup_path,
                    diff_summary=diff_summary,
                    validation_passed=True
                )
                
                # Atualizar métricas
                self.correction_metrics['files_corrected'] += 1
                self.correction_metrics['corrections_applied'] += len(applied_corrections)
                self.correction_metrics['corrections_failed'] += len(failed_corrections)
                
                # Adicionar ao histórico
                self.correction_history.append(result)
                
                # Notificar sucesso
                await self._notify_correction_success(plan, result)
                
                return {
                    'status': 'completed',
                    'result_id': result.result_id,
                    'file_path': plan.file_path,
                    'corrections_applied': len(applied_corrections),
                    'corrections_failed': len(failed_corrections),
                    'backup_path': backup_path,
                    'diff_summary': diff_summary
                }
                
            else:
                # Rollback se validação falhou
                await self._restore_backup(plan.file_path, backup_path)
                
                return {
                    'status': 'failed',
                    'message': 'Validação falhou - backup restaurado',
                    'file_path': plan.file_path,
                    'validation_errors': self._get_validation_errors(corrected_code)
                }
                
        except Exception as e:
            logger.error(f"❌ Erro aplicando correções: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _apply_single_correction(self, code: str, correction: CodeCorrection) -> Tuple[str, bool]:
        """Aplica uma única correção"""
        try:
            lines = code.split('\n')
            
            # Verificar limites
            if correction.line_start <= 0 or correction.line_start > len(lines):
                return code, False
            
            # Aplicar correção
            line_idx = correction.line_start - 1
            original_line = lines[line_idx]
            
            # Verificar se a linha original corresponde
            if original_line.strip() != correction.original_code.strip():
                logger.warning(f"⚠️ Linha não corresponde ao esperado para correção {correction.correction_id}")
                return code, False
            
            # Substituir linha
            lines[line_idx] = correction.corrected_code.rstrip('\n')
            
            return '\n'.join(lines), True
            
        except Exception as e:
            logger.error(f"❌ Erro aplicando correção individual: {e}")
            return code, False
    
    async def format_code(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formata código usando ferramentas automatizadas"""
        try:
            file_path = request_data.get('file_path')
            formatters = request_data.get('formatters', ['black', 'isort'])
            
            if not os.path.exists(file_path):
                return {
                    'status': 'error',
                    'message': f'Arquivo não encontrado: {file_path}'
                }
            
            logger.info(f"🎨 Formatando código: {file_path}")
            
            # Criar backup
            backup_path = await self._create_backup(file_path)
            
            # Ler código original
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Aplicar formatadores
            formatted_code = code
            applied_formatters = []
            
            for formatter_name in formatters:
                if formatter_name in self.formatters:
                    try:
                        formatted_code = await self.formatters[formatter_name](formatted_code)
                        applied_formatters.append(formatter_name)
                    except Exception as e:
                        logger.error(f"❌ Erro com {formatter_name}: {e}")
            
            # Validar código formatado
            if self._validate_syntax(formatted_code):
                # Salvar código formatado
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_code)
                
                # Calcular mudanças
                lines_changed = self._count_changed_lines(code, formatted_code)
                
                return {
                    'status': 'completed',
                    'file_path': file_path,
                    'formatters_applied': applied_formatters,
                    'lines_changed': lines_changed,
                    'backup_path': backup_path
                }
            else:
                # Restaurar backup
                await self._restore_backup(file_path, backup_path)
                
                return {
                    'status': 'failed',
                    'message': 'Código formatado possui sintaxe inválida',
                    'file_path': file_path
                }
                
        except Exception as e:
            logger.error(f"❌ Erro formatando código: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _format_with_black(self, code: str) -> str:
        """Formata código com Black"""
        try:
            return black.format_str(code, mode=black.Mode())
        except Exception as e:
            logger.error(f"❌ Erro formatando com Black: {e}")
            return code
    
    async def _format_with_autopep8(self, code: str) -> str:
        """Formata código com autopep8"""
        try:
            return autopep8.fix_code(code, options={'aggressive': 1})
        except Exception as e:
            logger.error(f"❌ Erro formatando com autopep8: {e}")
            return code
    
    async def _format_imports_with_isort(self, code: str) -> str:
        """Organiza imports com isort"""
        try:
            return isort.code(code)
        except Exception as e:
            logger.error(f"❌ Erro organizando imports: {e}")
            return code
    
    async def rollback_changes(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Reverte mudanças para um backup"""
        try:
            file_path = request_data.get('file_path')
            backup_path = request_data.get('backup_path')
            
            if not backup_path:
                # Encontrar backup mais recente
                backup_path = self._find_latest_backup(file_path)
            
            if not backup_path or not os.path.exists(backup_path):
                return {
                    'status': 'error',
                    'message': 'Backup não encontrado'
                }
            
            await self._restore_backup(file_path, backup_path)
            
            self.correction_metrics['rollbacks_performed'] += 1
            
            return {
                'status': 'completed',
                'file_path': file_path,
                'restored_from': backup_path,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro revertendo mudanças: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _create_backup(self, file_path: str) -> str:
        """Cria backup do arquivo"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = Path(file_path).name
            backup_path = self.backup_directory / f"{filename}.backup_{timestamp}"
            
            shutil.copy2(file_path, backup_path)
            logger.info(f"💾 Backup criado: {backup_path}")
            
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"❌ Erro criando backup: {e}")
            raise
    
    async def _restore_backup(self, file_path: str, backup_path: str):
        """Restaura arquivo do backup"""
        try:
            shutil.copy2(backup_path, file_path)
            logger.info(f"🔄 Backup restaurado: {file_path} <- {backup_path}")
        except Exception as e:
            logger.error(f"❌ Erro restaurando backup: {e}")
            raise
    
    def _find_latest_backup(self, file_path: str) -> Optional[str]:
        """Encontra backup mais recente de um arquivo"""
        try:
            filename = Path(file_path).name
            pattern = f"{filename}.backup_*"
            
            backups = list(self.backup_directory.glob(pattern))
            if backups:
                # Ordenar por tempo de modificação
                latest = max(backups, key=lambda p: p.stat().st_mtime)
                return str(latest)
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro procurando backup: {e}")
            return None
    
    def _validate_syntax(self, code: str) -> bool:
        """Valida sintaxe do código Python"""
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            logger.warning(f"⚠️ Erro de sintaxe: {e}")
            return False
    
    async def _validate_corrected_code(self, corrected_code: str, original_code: str) -> bool:
        """Valida código corrigido com múltiplos critérios"""
        try:
            # 1. Validação de sintaxe
            if not self._validate_syntax(corrected_code):
                return False
            
            # 2. Verificar se não removeu código importante
            original_lines = original_code.split('\n')
            corrected_lines = corrected_code.split('\n')
            
            # Verificar se funções/classes não foram removidas
            original_defs = [l for l in original_lines if l.strip().startswith(('def ', 'class '))]
            corrected_defs = [l for l in corrected_lines if l.strip().startswith(('def ', 'class '))]
            
            if len(corrected_defs) < len(original_defs):
                logger.warning("⚠️ Correção removeu definições de função/classe")
                return False
            
            # 3. Verificar tamanho (não deve reduzir drasticamente)
            size_ratio = len(corrected_code) / max(1, len(original_code))
            if size_ratio < 0.5:
                logger.warning("⚠️ Código corrigido é muito menor que o original")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro validando código: {e}")
            return False
    
    def _get_validation_errors(self, code: str) -> List[str]:
        """Obtém erros de validação do código"""
        errors = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append(f"Syntax error at line {e.lineno}: {e.msg}")
        
        # Outras validações
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                errors.append(f"Line {i} exceeds 120 characters")
        
        return errors
    
    def _generate_diff_summary(self, original: str, corrected: str) -> str:
        """Gera resumo das diferenças"""
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            corrected.splitlines(keepends=True),
            fromfile='original',
            tofile='corrected',
            n=3
        )
        
        diff_lines = list(diff)
        
        # Contar mudanças
        additions = sum(1 for line in diff_lines if line.startswith('+') and not line.startswith('+++'))
        deletions = sum(1 for line in diff_lines if line.startswith('-') and not line.startswith('---'))
        
        return f"Adições: {additions}, Remoções: {deletions}, Total de mudanças: {additions + deletions}"
    
    def _count_changed_lines(self, original: str, corrected: str) -> int:
        """Conta número de linhas modificadas"""
        original_lines = original.splitlines()
        corrected_lines = corrected.splitlines()
        
        matcher = difflib.SequenceMatcher(None, original_lines, corrected_lines)
        changed = 0
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != 'equal':
                changed += max(i2 - i1, j2 - j1)
        
        return changed
    
    def _determine_priority(self, corrections: List[CodeCorrection]) -> Priority:
        """Determina prioridade do plano baseado nas correções"""
        # Verificar se há correções críticas
        critical_types = {CorrectionType.SECURITY_PATCH, CorrectionType.SYNTAX_FIX}
        
        if any(c.correction_type in critical_types for c in corrections):
            return Priority.CRITICAL
        
        # Verificar quantidade
        if len(corrections) > 10:
            return Priority.HIGH
        
        # Verificar confiança média
        avg_confidence = sum(c.confidence for c in corrections) / len(corrections)
        if avg_confidence > 0.8:
            return Priority.MEDIUM
        
        return Priority.LOW
    
    def _estimate_impact(self, corrections: List[CodeCorrection]) -> str:
        """Estima impacto das correções"""
        impact_score = 0
        
        for correction in corrections:
            if correction.correction_type == CorrectionType.SECURITY_PATCH:
                impact_score += 5
            elif correction.correction_type == CorrectionType.PERFORMANCE_OPT:
                impact_score += 3
            elif correction.correction_type == CorrectionType.SYNTAX_FIX:
                impact_score += 4
            else:
                impact_score += 1
        
        if impact_score > 20:
            return "high"
        elif impact_score > 10:
            return "medium"
        else:
            return "low"
    
    def _identify_risks(self, corrections: List[CodeCorrection]) -> List[str]:
        """Identifica riscos potenciais das correções"""
        risks = []
        
        # Verificar mudanças em massa
        if len(corrections) > 20:
            risks.append("Grande número de mudanças pode introduzir instabilidade")
        
        # Verificar correções de segurança
        security_corrections = [c for c in corrections if c.correction_type == CorrectionType.SECURITY_PATCH]
        if security_corrections:
            risks.append("Correções de segurança podem afetar funcionalidade")
        
        # Verificar refatorações
        refactoring_corrections = [c for c in corrections if c.correction_type == CorrectionType.REFACTORING]
        if len(refactoring_corrections) > 5:
            risks.append("Múltiplas refatorações podem alterar comportamento")
        
        # Verificar confiança baixa
        low_confidence = [c for c in corrections if c.confidence < 0.6]
        if len(low_confidence) > len(corrections) / 3:
            risks.append("Muitas correções com baixa confiança")
        
        return risks
    
    async def _validate_correction_plan(self, plan: CorrectionPlan):
        """Valida um plano de correção antes da execução"""
        try:
            # Simular aplicação para validar
            with open(plan.file_path, 'r', encoding='utf-8') as f:
                test_code = f.read()
            
            for correction in plan.corrections:
                # Verificar se correção ainda é aplicável
                lines = test_code.split('\n')
                if correction.line_start <= len(lines):
                    line = lines[correction.line_start - 1]
                    if line.strip() != correction.original_code.strip():
                        correction.status = CorrectionStatus.FAILED
                        correction.error_message = "Código original mudou"
            
            # Atualizar status do plano
            valid_corrections = [c for c in plan.corrections if c.status != CorrectionStatus.FAILED]
            if not valid_corrections:
                plan.status = CorrectionStatus.FAILED
            
        except Exception as e:
            logger.error(f"❌ Erro validando plano: {e}")
            plan.status = CorrectionStatus.FAILED
    
    async def _notify_correction_success(self, plan: CorrectionPlan, result: CorrectionResult):
        """Notifica sucesso da correção"""
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="performance_monitor_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.MEDIUM,
            content={
                'notification_type': 'correction_completed',
                'file_path': plan.file_path,
                'corrections_applied': result.corrections_applied,
                'plan_id': plan.plan_id,
                'result_id': result.result_id
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)
    
    async def _process_correction_request(self, request: Dict[str, Any]):
        """Processa requisição de correção da fila"""
        request_type = request.get('type')
        
        if request_type == 'execute_plan':
            plan_id = request.get('plan_id')
            if plan_id in self.active_plans:
                await self.apply_corrections({'plan_id': plan_id})
    
    def get_correction_history(self) -> Dict[str, Any]:
        """Retorna histórico de correções"""
        recent_results = self.correction_history[-10:]
        
        return {
            'status': 'completed',
            'total_corrections': len(self.correction_history),
            'recent_corrections': [
                {
                    'result_id': r.result_id,
                    'file_path': r.file_path,
                    'corrections_applied': r.corrections_applied,
                    'corrections_failed': r.corrections_failed,
                    'timestamp': r.timestamp.isoformat(),
                    'rollback_performed': r.rollback_performed
                }
                for r in recent_results
            ],
            'metrics': self.correction_metrics
        }
    
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

def create_code_corrector_agent(message_bus, num_instances=1) -> List[CodeCorrectorAgent]:
    """
    Cria agente de correção de código
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de correção
    """
    agents = []
    
    try:
        logger.info("🔧 Criando CodeCorrectorAgent para autoevolução...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "code_corrector_001"
        
        if agent_id not in existing_agents:
            try:
                agent = CodeCorrectorAgent(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar serviços de correção
                asyncio.create_task(agent.start_correction_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com correção automática avançada")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de correção criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando CodeCorrectorAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
