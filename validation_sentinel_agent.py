#!/usr/bin/env python3
"""
ValidationSentinelAgent - Guardian Supremo de Qualidade do SUNA-ALSHAM
Valida TUDO que passa pelo sistema para garantir máxima qualidade
"""

import re
import json
import hashlib
import asyncio
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
import logging
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class ValidationType(Enum):
    """Tipos de validação"""
    INPUT_SANITIZATION = "input_sanitization"
    OUTPUT_VALIDATION = "output_validation"
    FACT_CHECKING = "fact_checking"
    HALLUCINATION_PREVENTION = "hallucination_prevention"
    DATA_INTEGRITY = "data_integrity_check"
    RESPONSE_VALIDATION = "response_validation"
    CONSISTENCY_VERIFICATION = "consistency_verification"
    SANITY_CHECKING = "sanity_checking"
    CODE_VALIDATION = "code_validation"
    SECURITY_VALIDATION = "security_validation"
    PERFORMANCE_VALIDATION = "performance_validation"
    LOGICAL_CONSISTENCY = "logical_consistency"

class ValidationSeverity(Enum):
    """Severidade da validação"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ValidationStatus(Enum):
    """Status da validação"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    NEEDS_REVIEW = "needs_review"
    BLOCKED = "blocked"

@dataclass
class ValidationResult:
    """Resultado de uma validação"""
    validation_id: str
    validation_type: ValidationType
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    details: Dict[str, Any]
    suggestions: List[str] = field(default_factory=list)
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationRule:
    """Regra de validação"""
    rule_id: str
    name: str
    description: str
    pattern: Optional[re.Pattern]
    validator_function: Optional[callable]
    severity: ValidationSeverity
    enabled: bool = True
    tags: List[str] = field(default_factory=list)

@dataclass
class ValidationReport:
    """Relatório completo de validação"""
    report_id: str
    subject: str
    total_checks: int
    passed: int
    failed: int
    warnings: int
    blocked: int
    overall_score: float
    critical_issues: List[ValidationResult]
    recommendations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

class ValidationSentinelAgent(BaseNetworkAgent):
    """Guardian Supremo de Qualidade - Valida TUDO no sistema"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'input_sanitization',
            'output_validation', 
            'fact_checking',
            'hallucination_prevention',
            'data_integrity_check',
            'response_validation',
            'consistency_verification',
            'sanity_checking',
            'code_validation',
            'security_validation',
            'performance_validation',
            'logical_consistency',
            'real_time_monitoring',
            'quality_scoring',
            'auto_correction',
            'pattern_detection'
        ]
        self.status = 'active'
        
        # Estado do Sentinel
        self.validation_queue = asyncio.Queue()
        self.validation_history = deque(maxlen=10000)
        self.validation_rules = self._load_validation_rules()
        self.fact_database = {}
        self.consistency_cache = {}
        self.performance_baselines = {}
        
        # Configurações avançadas
        self.real_time_monitoring = True
        self.auto_correction_enabled = True
        self.hallucination_threshold = 0.8
        self.consistency_threshold = 0.9
        self.security_level = "maximum"
        
        # Padrões de detecção
        self.suspicious_patterns = self._load_suspicious_patterns()
        self.quality_patterns = self._load_quality_patterns()
        self.security_patterns = self._load_security_patterns()
        
        # Métricas
        self.validation_metrics = {
            'total_validations': 0,
            'validations_passed': 0,
            'validations_failed': 0,
            'auto_corrections': 0,
            'blocked_dangerous_content': 0,
            'false_positives': 0,
            'system_quality_score': 100.0
        }
        
        # Cache de validações
        self.validation_cache = {}
        self.cache_ttl = 3600  # 1 hora
        
        # Tasks de background
        self._monitoring_task = None
        self._analysis_task = None
        self._cleanup_task = None
        
        logger.info(f"🛡️ {self.agent_id} inicializado como Guardian Supremo de Qualidade")
    
    def _load_validation_rules(self) -> Dict[str, ValidationRule]:
        """Carrega regras de validação avançadas"""
        rules = {}
        
        # Regras de INPUT SANITIZATION
        rules['input_sql_injection'] = ValidationRule(
            rule_id='input_sql_injection',
            name='SQL Injection Detection',
            description='Detecta tentativas de SQL injection',
            pattern=re.compile(r"(\bUNION\b|\bSELECT\b|\bINSERT\b|\bDROP\b|\bDELETE\b).*(\bFROM\b|\bWHERE\b)", re.IGNORECASE),
            validator_function=None,
            severity=ValidationSeverity.CRITICAL,
            tags=['security', 'input', 'sql']
        )
        
        rules['input_xss'] = ValidationRule(
            rule_id='input_xss',
            name='XSS Attack Detection',
            description='Detecta tentativas de Cross-Site Scripting',
            pattern=re.compile(r'<script[^>]*>.*?</script>|javascript:', re.IGNORECASE),
            validator_function=None,
            severity=ValidationSeverity.HIGH,
            tags=['security', 'input', 'xss']
        )
        
        rules['input_path_traversal'] = ValidationRule(
            rule_id='input_path_traversal',
            name='Path Traversal Detection',
            description='Detecta tentativas de path traversal',
            pattern=re.compile(r'\.\.[\\/]|[\\/]\.\.'),
            validator_function=None,
            severity=ValidationSeverity.HIGH,
            tags=['security', 'input', 'filesystem']
        )
        
        # Regras de OUTPUT VALIDATION
        rules['output_completeness'] = ValidationRule(
            rule_id='output_completeness',
            name='Response Completeness',
            description='Verifica se respostas estão completas',
            pattern=None,
            validator_function=self._validate_response_completeness,
            severity=ValidationSeverity.MEDIUM,
            tags=['quality', 'output']
        )
        
        rules['output_coherence'] = ValidationRule(
            rule_id='output_coherence',
            name='Response Coherence',
            description='Verifica coerência lógica das respostas',
            pattern=None,
            validator_function=self._validate_response_coherence,
            severity=ValidationSeverity.MEDIUM,
            tags=['quality', 'output', 'logic']
        )
        
        # Regras de FACT CHECKING
        rules['fact_consistency'] = ValidationRule(
            rule_id='fact_consistency',
            name='Fact Consistency Check',
            description='Verifica consistência com fatos conhecidos',
            pattern=None,
            validator_function=self._validate_fact_consistency,
            severity=ValidationSeverity.HIGH,
            tags=['facts', 'consistency']
        )
        
        # Regras de HALLUCINATION PREVENTION
        rules['hallucination_detection'] = ValidationRule(
            rule_id='hallucination_detection',
            name='Hallucination Detection',
            description='Detecta informações potencialmente alucinadas',
            pattern=None,
            validator_function=self._detect_hallucination,
            severity=ValidationSeverity.HIGH,
            tags=['hallucination', 'quality']
        )
        
        # Regras de CODE VALIDATION
        rules['code_safety'] = ValidationRule(
            rule_id='code_safety',
            name='Code Safety Check',
            description='Verifica segurança do código gerado',
            pattern=re.compile(r'(eval|exec|subprocess\.call|os\.system)\s*\(', re.IGNORECASE),
            validator_function=self._validate_code_safety,
            severity=ValidationSeverity.CRITICAL,
            tags=['security', 'code']
        )
        
        rules['code_quality'] = ValidationRule(
            rule_id='code_quality',
            name='Code Quality Check',
            description='Verifica qualidade do código gerado',
            pattern=None,
            validator_function=self._validate_code_quality,
            severity=ValidationSeverity.MEDIUM,
            tags=['quality', 'code']
        )
        
        return rules
    
    def _load_suspicious_patterns(self) -> Dict[str, re.Pattern]:
        """Carrega padrões suspeitos para detecção"""
        return {
            'credentials': re.compile(r'(password|passwd|pwd|token|key|secret)\s*[=:]\s*["\'][^"\']+["\']', re.IGNORECASE),
            'personal_data': re.compile(r'(\b\d{3}-\d{2}-\d{4}\b|\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b)', re.IGNORECASE),
            'malicious_urls': re.compile(r'https?://[^\s]+\.(tk|ml|ga|cf|bit\.ly)', re.IGNORECASE),
            'command_injection': re.compile(r'[;&|`$\(\){}]', re.IGNORECASE),
            'excessive_repetition': re.compile(r'(.{10,}?)\1{3,}', re.IGNORECASE)
        }
    
    def _load_quality_patterns(self) -> Dict[str, re.Pattern]:
        """Carrega padrões de qualidade"""
        return {
            'incomplete_response': re.compile(r'\b(incomplete|unfinished|todo|fixme|xxx)\b', re.IGNORECASE),
            'uncertainty_indicators': re.compile(r'\b(maybe|possibly|might|could be|uncertain|unclear)\b', re.IGNORECASE),
            'placeholder_text': re.compile(r'\b(placeholder|example|sample|dummy|test)\b', re.IGNORECASE),
            'error_indicators': re.compile(r'\b(error|fail|exception|crash|bug)\b', re.IGNORECASE)
        }
    
    def _load_security_patterns(self) -> Dict[str, re.Pattern]:
        """Carrega padrões de segurança"""
        return {
            'hardcoded_secrets': re.compile(r'(api_key|access_token|private_key)\s*=\s*["\'][^"\']{20,}["\']', re.IGNORECASE),
            'dangerous_functions': re.compile(r'\b(eval|exec|compile|__import__|getattr|setattr|delattr)\s*\(', re.IGNORECASE),
            'file_operations': re.compile(r'\b(open|file|read|write|delete|remove)\s*\([^)]*["\'][^"\']*\.\.[^"\']*["\']', re.IGNORECASE),
            'network_calls': re.compile(r'\b(requests|urllib|socket|http)\.[^(]*\([^)]*\)', re.IGNORECASE)
        }
    
    async def start_sentinel_service(self):
        """Inicia serviços do Sentinel"""
        if not self._monitoring_task:
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            self._analysis_task = asyncio.create_task(self._analysis_loop())
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
            logger.info(f"🛡️ {self.agent_id} iniciou serviços de validação suprema")
    
    async def stop_sentinel_service(self):
        """Para serviços do Sentinel"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
        if self._analysis_task:
            self._analysis_task.cancel()
            self._analysis_task = None
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None
        logger.info(f"🛑 {self.agent_id} parou serviços de validação")
    
    async def _monitoring_loop(self):
        """Loop de monitoramento em tempo real"""
        while True:
            try:
                # Processar fila de validação
                if not self.validation_queue.empty():
                    validation_request = await self.validation_queue.get()
                    await self._process_validation_request(validation_request)
                
                # Monitorar sistema
                if self.real_time_monitoring:
                    await self._monitor_system_quality()
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento: {e}")
    
    async def _analysis_loop(self):
        """Loop de análise de tendências"""
        while True:
            try:
                # Analisar padrões de qualidade
                await self._analyze_quality_trends()
                
                # Atualizar regras baseado em aprendizado
                await self._update_validation_rules()
                
                # Gerar relatórios
                if len(self.validation_history) > 100:
                    report = await self._generate_quality_report()
                    await self._send_quality_report(report)
                
                await asyncio.sleep(300)  # A cada 5 minutos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na análise: {e}")
    
    async def _cleanup_loop(self):
        """Loop de limpeza"""
        while True:
            try:
                # Limpar cache antigo
                await self._cleanup_cache()
                
                # Limpar histórico antigo
                await self._cleanup_history()
                
                await asyncio.sleep(3600)  # A cada hora
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na limpeza: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        # INTERCEPTAR TODAS AS MENSAGENS para validação
        if self.real_time_monitoring:
            await self._validate_message_real_time(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'validate_content':
                result = await self.validate_content(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'sanitize_input':
                result = await self.sanitize_input(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'validate_code':
                result = await self.validate_code(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'fact_check':
                result = await self.fact_check(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'quality_report':
                result = await self.get_quality_report()
                await self._send_response(message, result)
                
            elif request_type == 'update_rules':
                result = await self.update_validation_rules(message.content)
                await self._send_response(message, result)
    
    async def validate_content(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida conteúdo completo com TODAS as regras"""
        try:
            content = request_data.get('content', '')
            content_type = request_data.get('type', 'general')
            strict_mode = request_data.get('strict_mode', True)
            
            logger.info(f"🛡️ Validando conteúdo tipo: {content_type}")
            
            validation_results = []
            
            # 1. INPUT SANITIZATION
            sanitization_results = await self._perform_input_sanitization(content)
            validation_results.extend(sanitization_results)
            
            # 2. SECURITY VALIDATION
            security_results = await self._perform_security_validation(content)
            validation_results.extend(security_results)
            
            # 3. QUALITY VALIDATION
            quality_results = await self._perform_quality_validation(content, content_type)
            validation_results.extend(quality_results)
            
            # 4. CONSISTENCY CHECK
            consistency_results = await self._perform_consistency_check(content)
            validation_results.extend(consistency_results)
            
            # 5. FACT CHECKING (se aplicável)
            if content_type in ['factual', 'informational', 'response']:
                fact_results = await self._perform_fact_checking(content)
                validation_results.extend(fact_results)
            
            # 6. HALLUCINATION DETECTION
            hallucination_results = await self._perform_hallucination_detection(content)
            validation_results.extend(hallucination_results)
            
            # Calcular score geral
            overall_score = self._calculate_validation_score(validation_results)
            
            # Determinar ação
            action = self._determine_action(validation_results, strict_mode)
            
            # Auto-correção se habilitada
            corrected_content = content
            if self.auto_correction_enabled and action == 'needs_correction':
                corrected_content = await self._auto_correct_content(content, validation_results)
            
            # Atualizar métricas
            self.validation_metrics['total_validations'] += 1
            if overall_score >= 80:
                self.validation_metrics['validations_passed'] += 1
            else:
                self.validation_metrics['validations_failed'] += 1
            
            # Armazenar no histórico
            self.validation_history.append({
                'content': content[:100] + '...' if len(content) > 100 else content,
                'type': content_type,
                'score': overall_score,
                'results': validation_results,
                'timestamp': datetime.now()
            })
            
            return {
                'status': 'completed',
                'overall_score': overall_score,
                'action_required': action,
                'validation_results': [self._result_to_dict(r) for r in validation_results],
                'corrected_content': corrected_content if corrected_content != content else None,
                'summary': {
                    'total_checks': len(validation_results),
                    'passed': len([r for r in validation_results if r.status == ValidationStatus.PASSED]),
                    'failed': len([r for r in validation_results if r.status == ValidationStatus.FAILED]),
                    'warnings': len([r for r in validation_results if r.status == ValidationStatus.WARNING]),
                    'blocked': len([r for r in validation_results if r.status == ValidationStatus.BLOCKED])
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na validação: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _perform_input_sanitization(self, content: str) -> List[ValidationResult]:
        """Sanitização completa de input"""
        results = []
        
        # Verificar padrões suspeitos
        for pattern_name, pattern in self.suspicious_patterns.items():
            matches = pattern.findall(content)
            if matches:
                severity = ValidationSeverity.CRITICAL if pattern_name in ['credentials', 'command_injection'] else ValidationSeverity.HIGH
                
                result = ValidationResult(
                    validation_id=f"input_{pattern_name}_{len(results)}",
                    validation_type=ValidationType.INPUT_SANITIZATION,
                    status=ValidationStatus.FAILED,
                    severity=severity,
                    message=f"Padrão suspeito detectado: {pattern_name}",
                    details={'pattern': pattern_name, 'matches': matches[:5]},  # Limitar matches
                    suggestions=[f"Remover ou sanitizar conteúdo relacionado a {pattern_name}"]
                )
                results.append(result)
        
        # Verificar regras de sanitização
        for rule_id, rule in self.validation_rules.items():
            if 'input' in rule.tags and rule.enabled and rule.pattern:
                if rule.pattern.search(content):
                    result = ValidationResult(
                        validation_id=f"rule_{rule_id}_{len(results)}",
                        validation_type=ValidationType.INPUT_SANITIZATION,
                        status=ValidationStatus.FAILED,
                        severity=rule.severity,
                        message=f"Regra de sanitização violada: {rule.name}",
                        details={'rule_id': rule_id, 'description': rule.description},
                        suggestions=[f"Corrigir violação da regra: {rule.description}"]
                    )
                    results.append(result)
        
        return results
    
    async def _perform_security_validation(self, content: str) -> List[ValidationResult]:
        """Validação de segurança avançada"""
        results = []
        
        # Verificar padrões de segurança
        for pattern_name, pattern in self.security_patterns.items():
            matches = pattern.findall(content)
            if matches:
                result = ValidationResult(
                    validation_id=f"security_{pattern_name}_{len(results)}",
                    validation_type=ValidationType.SECURITY_VALIDATION,
                    status=ValidationStatus.BLOCKED,
                    severity=ValidationSeverity.CRITICAL,
                    message=f"Risco de segurança detectado: {pattern_name}",
                    details={'pattern': pattern_name, 'matches_count': len(matches)},
                    suggestions=[f"Revisar e remover código potencialmente perigoso relacionado a {pattern_name}"]
                )
                results.append(result)
                self.validation_metrics['blocked_dangerous_content'] += 1
        
        return results
    
    async def _perform_quality_validation(self, content: str, content_type: str) -> List[ValidationResult]:
        """Validação de qualidade"""
        results = []
        
        # Verificar completude
        if len(content.strip()) < 10:
            result = ValidationResult(
                validation_id=f"quality_length_{len(results)}",
                validation_type=ValidationType.OUTPUT_VALIDATION,
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.MEDIUM,
                message="Conteúdo muito curto ou vazio",
                details={'length': len(content)},
                suggestions=["Fornecer conteúdo mais detalhado e completo"]
            )
            results.append(result)
        
        # Verificar padrões de qualidade
        for pattern_name, pattern in self.quality_patterns.items():
            matches = pattern.findall(content)
            if matches:
                severity = ValidationSeverity.HIGH if pattern_name == 'error_indicators' else ValidationSeverity.MEDIUM
                
                result = ValidationResult(
                    validation_id=f"quality_{pattern_name}_{len(results)}",
                    validation_type=ValidationType.OUTPUT_VALIDATION,
                    status=ValidationStatus.WARNING,
                    severity=severity,
                    message=f"Problema de qualidade detectado: {pattern_name}",
                    details={'pattern': pattern_name, 'matches_count': len(matches)},
                    suggestions=[f"Revisar e melhorar conteúdo relacionado a {pattern_name}"]
                )
                results.append(result)
        
        # Validação específica por tipo
        if content_type == 'code':
            code_results = await self._validate_code_content(content)
            results.extend(code_results)
        
        return results
    
    async def _validate_code_content(self, code: str) -> List[ValidationResult]:
        """Validação específica para código"""
        results = []
        
        # Verificar sintaxe básica Python (se aplicável)
        if 'def ' in code or 'class ' in code or 'import ' in code:
            try:
                import ast
                ast.parse(code)
                
                result = ValidationResult(
                    validation_id=f"code_syntax_{len(results)}",
                    validation_type=ValidationType.CODE_VALIDATION,
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Sintaxe Python válida",
                    details={'language': 'python'},
                    suggestions=[]
                )
                results.append(result)
                
            except SyntaxError as e:
                result = ValidationResult(
                    validation_id=f"code_syntax_error_{len(results)}",
                    validation_type=ValidationType.CODE_VALIDATION,
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.HIGH,
                    message=f"Erro de sintaxe: {str(e)}",
                    details={'error': str(e), 'line': getattr(e, 'lineno', 'unknown')},
                    suggestions=["Corrigir erro de sintaxe no código"]
                )
                results.append(result)
        
        return results
    
    async def _perform_consistency_check(self, content: str) -> List[ValidationResult]:
        """Verificação de consistência"""
        results = []
        
        # Calcular hash do conteúdo
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Verificar consistência com cache
        if content_hash in self.consistency_cache:
            cached_data = self.consistency_cache[content_hash]
            if datetime.now() - cached_data['timestamp'] < timedelta(hours=1):
                # Conteúdo similar recente - verificar consistência
                similarity = self._calculate_similarity(content, cached_data['content'])
                
                if similarity > self.consistency_threshold:
                    result = ValidationResult(
                        validation_id=f"consistency_{len(results)}",
                        validation_type=ValidationType.CONSISTENCY_VERIFICATION,
                        status=ValidationStatus.PASSED,
                        severity=ValidationSeverity.INFO,
                        message="Conteúdo consistente com versões anteriores",
                        details={'similarity': similarity, 'cached_at': cached_data['timestamp'].isoformat()},
                        suggestions=[]
                    )
                else:
                    result = ValidationResult(
                        validation_id=f"consistency_warning_{len(results)}",
                        validation_type=ValidationType.CONSISTENCY_VERIFICATION,
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.MEDIUM,
                        message="Possível inconsistência detectada",
                        details={'similarity': similarity},
                        suggestions=["Verificar se mudanças são intencionais"]
                    )
                
                results.append(result)
        
        # Atualizar cache
        self.consistency_cache[content_hash] = {
            'content': content,
            'timestamp': datetime.now()
        }
        
        return results
    
    async def _perform_fact_checking(self, content: str) -> List[ValidationResult]:
        """Verificação de fatos"""
        results = []
        
        # Fact-checking básico (em produção seria mais sofisticado)
        suspicious_claims = [
            'sempre', 'nunca', '100%', 'impossível', 'todos', 'nenhum'
        ]
        
        for claim in suspicious_claims:
            if claim in content.lower():
                result = ValidationResult(
                    validation_id=f"fact_absolute_{len(results)}",
                    validation_type=ValidationType.FACT_CHECKING,
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.MEDIUM,
                    message=f"Afirmação absoluta detectada: '{claim}'",
                    details={'claim': claim},
                    suggestions=["Verificar se afirmações absolutas são precisas"]
                )
                results.append(result)
        
        return results
    
    async def _perform_hallucination_detection(self, content: str) -> List[ValidationResult]:
        """Detecção de alucinações"""
        results = []
        
        # Indicadores de possível alucinação
        hallucination_indicators = [
            'according to my knowledge',
            'i believe',
            'it seems that',
            'probably',
            'i think'
        ]
        
        confidence_score = 1.0
        detected_indicators = []
        
        for indicator in hallucination_indicators:
            if indicator in content.lower():
                detected_indicators.append(indicator)
                confidence_score -= 0.1
        
        if confidence_score < self.hallucination_threshold:
            result = ValidationResult(
                validation_id=f"hallucination_{len(results)}",
                validation_type=ValidationType.HALLUCINATION_PREVENTION,
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.HIGH,
                message="Possível alucinação detectada",
                details={
                    'confidence_score': confidence_score,
                    'indicators': detected_indicators
                },
                suggestions=["Verificar precisão das informações", "Buscar fontes confiáveis"]
            )
            results.append(result)
        
        return results
    
    def _calculate_validation_score(self, results: List[ValidationResult]) -> float:
        """Calcula score geral de validação"""
        if not results:
            return 100.0
        
        total_score = 100.0
        
        for result in results:
            if result.status == ValidationStatus.FAILED:
                if result.severity == ValidationSeverity.CRITICAL:
                    total_score -= 25
                elif result.severity == ValidationSeverity.HIGH:
                    total_score -= 15
                elif result.severity == ValidationSeverity.MEDIUM:
                    total_score -= 8
                else:
                    total_score -= 3
            elif result.status == ValidationStatus.WARNING:
                if result.severity == ValidationSeverity.HIGH:
                    total_score -= 5
                elif result.severity == ValidationSeverity.MEDIUM:
                    total_score -= 2
                else:
                    total_score -= 1
            elif result.status == ValidationStatus.BLOCKED:
                total_score = 0  # Conteúdo bloqueado = score zero
                break
        
        return max(0, min(100, total_score))
    
    def _determine_action(self, results: List[ValidationResult], strict_mode: bool) -> str:
        """Determina ação necessária baseada nos resultados"""
        blocked = any(r.status == ValidationStatus.BLOCKED for r in results)
        critical_failed = any(r.status == ValidationStatus.FAILED and r.severity == ValidationSeverity.CRITICAL for r in results)
        high_failed = any(r.status == ValidationStatus.FAILED and r.severity == ValidationSeverity.HIGH for r in results)
        
        if blocked:
            return 'blocked'
        elif critical_failed:
            return 'rejected'
        elif high_failed and strict_mode:
            return 'needs_review'
        elif any(r.status == ValidationStatus.FAILED for r in results):
            return 'needs_correction'
        elif any(r.status == ValidationStatus.WARNING for r in results):
            return 'warning'
        else:
            return 'approved'
    
    async def _auto_correct_content(self, content: str, results: List[ValidationResult]) -> str:
        """Auto-correção de conteúdo quando possível"""
        corrected = content
        
        for result in results:
            if result.status == ValidationStatus.FAILED and self.auto_correction_enabled:
                # Correções básicas
                if 'input_sanitization' in result.validation_type.value:
                    # Remover padrões perigosos
                    for pattern_name, pattern in self.suspicious_patterns.items():
                        corrected = pattern.sub('[REMOVIDO POR SEGURANÇA]', corrected)
                
                elif 'security' in result.validation_type.value:
                    # Comentar código perigoso
                    for pattern_name, pattern in self.security_patterns.items():
                        corrected = pattern.sub(lambda m: f'# {m.group(0)} # [COMENTADO POR SEGURANÇA]', corrected)
        
        if corrected != content:
            self.validation_metrics['auto_corrections'] += 1
            logger.info(f"🔧 Auto-correção aplicada pelo Sentinel")
        
        return corrected
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcula similaridade entre textos"""
        # Implementação básica - em produção usaria algoritmos mais sofisticados
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    # Funções específicas de validação
    def _validate_response_completeness(self, content: str) -> bool:
        """Valida se resposta está completa"""
        return len(content.strip()) > 20 and not content.endswith('...')
    
    def _validate_response_coherence(self, content: str) -> bool:
        """Valida coerência da resposta"""
        sentences = content.split('.')
        return len(sentences) > 1 and all(len(s.strip()) > 5 for s in sentences[:3])
    
    def _validate_fact_consistency(self, content: str) -> bool:
        """Valida consistência com fatos conhecidos"""
        # Implementação básica
        return 'flat earth' not in content.lower()
    
    def _detect_hallucination(self, content: str) -> bool:
        """Detecta possível alucinação"""
        uncertainty_count = sum(1 for word in ['maybe', 'possibly', 'might', 'could'] if word in content.lower())
        return uncertainty_count > 3
    
    def _validate_code_safety(self, content: str) -> bool:
        """Valida segurança do código"""
        dangerous_patterns = ['eval(', 'exec(', 'os.system(', '__import__']
        return not any(pattern in content for pattern in dangerous_patterns)
    
    def _validate_code_quality(self, content: str) -> bool:
        """Valida qualidade do código"""
        return len(content.strip()) > 10 and 'TODO' not in content
    
    async def sanitize_input(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitiza input de forma avançada"""
        try:
            raw_input = request_data.get('input', '')
            sanitization_level = request_data.get('level', 'standard')  # standard, strict, paranoid
            
            sanitized = raw_input
            changes_made = []
            
            # Nível 1: Sanitização básica
            if sanitization_level in ['standard', 'strict', 'paranoid']:
                # Remover scripts
                import html
                sanitized = html.escape(sanitized)
                if sanitized != raw_input:
                    changes_made.append('HTML entities escaped')
                
                # Remover padrões perigosos
                for pattern_name, pattern in self.suspicious_patterns.items():
                    original = sanitized
                    sanitized = pattern.sub('', sanitized)
                    if sanitized != original:
                        changes_made.append(f'Removed {pattern_name}')
            
            # Nível 2: Sanitização estrita
            if sanitization_level in ['strict', 'paranoid']:
                # Filtrar caracteres especiais
                import string
                allowed = string.ascii_letters + string.digits + ' .,!?-_'
                sanitized = ''.join(c for c in sanitized if c in allowed)
                if len(sanitized) != len(raw_input):
                    changes_made.append('Special characters filtered')
            
            # Nível 3: Sanitização paranóica
            if sanitization_level == 'paranoid':
                # Remover qualquer coisa suspeita
                suspicious_words = ['script', 'eval', 'exec', 'import', 'system']
                for word in suspicious_words:
                    if word in sanitized.lower():
                        sanitized = sanitized.replace(word, '[FILTERED]')
                        changes_made.append(f'Filtered suspicious word: {word}')
            
            return {
                'status': 'completed',
                'original_input': raw_input,
                'sanitized_input': sanitized,
                'changes_made': changes_made,
                'safety_score': self._calculate_safety_score(sanitized)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na sanitização: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _calculate_safety_score(self, content: str) -> float:
        """Calcula score de segurança do conteúdo"""
        score = 100.0
        
        # Verificar padrões perigosos
        for pattern in self.suspicious_patterns.values():
            if pattern.search(content):
                score -= 20
        
        for pattern in self.security_patterns.values():
            if pattern.search(content):
                score -= 30
        
        return max(0, score)
    
    async def validate_code(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validação completa de código"""
        try:
            code = request_data.get('code', '')
            language = request_data.get('language', 'python')
            
            validation_results = []
            
            # Validação de segurança
            security_results = await self._perform_security_validation(code)
            validation_results.extend(security_results)
            
            # Validação específica de código
            code_results = await self._validate_code_content(code)
            validation_results.extend(code_results)
            
            # Score de segurança
            security_score = self._calculate_safety_score(code)
            
            return {
                'status': 'completed',
                'code': code,
                'language': language,
                'security_score': security_score,
                'validation_results': [self._result_to_dict(r) for r in validation_results],
                'is_safe': security_score >= 80,
                'recommendations': self._generate_code_recommendations(validation_results)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro validando código: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_code_recommendations(self, results: List[ValidationResult]) -> List[str]:
        """Gera recomendações para código"""
        recommendations = []
        
        has_security_issues = any(r.validation_type == ValidationType.SECURITY_VALIDATION for r in results)
        has_syntax_errors = any('syntax' in r.message.lower() for r in results)
        
        if has_security_issues:
            recommendations.append("Revisar código para riscos de segurança")
        if has_syntax_errors:
            recommendations.append("Corrigir erros de sintaxe")
        if not recommendations:
            recommendations.append("Código validado com sucesso")
        
        return recommendations
    
    async def fact_check(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verificação de fatos avançada"""
        try:
            content = request_data.get('content', '')
            
            # Fact-checking básico (em produção seria integrado com bases de conhecimento)
            fact_results = await self._perform_fact_checking(content)
            
            # Análise de credibilidade
            credibility_score = self._calculate_credibility_score(content)
            
            return {
                'status': 'completed',
                'content': content,
                'credibility_score': credibility_score,
                'fact_check_results': [self._result_to_dict(r) for r in fact_results],
                'is_credible': credibility_score >= 70,
                'sources_needed': credibility_score < 80
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no fact-checking: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _calculate_credibility_score(self, content: str) -> float:
        """Calcula score de credibilidade"""
        score = 70.0  # Base score
        
        # Indicadores positivos
        if any(word in content.lower() for word in ['according to', 'research shows', 'study found']):
            score += 10
        
        # Indicadores negativos
        uncertainty_words = ['maybe', 'possibly', 'might', 'could be', 'i think']
        uncertainty_count = sum(1 for word in uncertainty_words if word in content.lower())
        score -= uncertainty_count * 5
        
        # Verificar absolutos
        absolute_words = ['always', 'never', 'all', 'none', '100%']
        absolute_count = sum(1 for word in absolute_words if word in content.lower())
        score -= absolute_count * 3
        
        return max(0, min(100, score))
    
    async def get_quality_report(self) -> Dict[str, Any]:
        """Gera relatório de qualidade do sistema"""
        try:
            # Analisar histórico recente
            recent_validations = list(self.validation_history)[-100:]
            
            if not recent_validations:
                return {
                    'status': 'completed',
                    'message': 'Nenhuma validação registrada ainda'
                }
            
            # Calcular estatísticas
            avg_score = sum(v['score'] for v in recent_validations) / len(recent_validations)
            
            score_distribution = {
                'excellent': len([v for v in recent_validations if v['score'] >= 90]),
                'good': len([v for v in recent_validations if 70 <= v['score'] < 90]),
                'acceptable': len([v for v in recent_validations if 50 <= v['score'] < 70]),
                'poor': len([v for v in recent_validations if v['score'] < 50])
            }
            
            # Problemas mais comuns
            all_results = []
            for validation in recent_validations:
                all_results.extend(validation.get('results', []))
            
            problem_types = defaultdict(int)
            for result in all_results:
                if hasattr(result, 'validation_type'):
                    problem_types[result.validation_type.value] += 1
                elif isinstance(result, dict):
                    problem_types[result.get('validation_type', 'unknown')] += 1
            
            return {
                'status': 'completed',
                'system_quality_score': avg_score,
                'total_validations': len(recent_validations),
                'score_distribution': score_distribution,
                'most_common_issues': dict(sorted(problem_types.items(), key=lambda x: x[1], reverse=True)[:5]),
                'metrics': self.validation_metrics,
                'recommendations': self._generate_system_recommendations(recent_validations)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro gerando relatório: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_system_recommendations(self, validations: List[Dict]) -> List[str]:
        """Gera recomendações para o sistema"""
        recommendations = []
        
        avg_score = sum(v['score'] for v in validations) / len(validations) if validations else 0
        
        if avg_score < 70:
            recommendations.append("Sistema com qualidade abaixo do ideal - implementar melhorias")
        
        low_quality_count = len([v for v in validations if v['score'] < 50])
        if low_quality_count > len(validations) * 0.2:
            recommendations.append("Alto número de validações com baixa qualidade - revisar processos")
        
        if self.validation_metrics['blocked_dangerous_content'] > 0:
            recommendations.append("Conteúdo perigoso detectado - manter vigilância alta")
        
        if not recommendations:
            recommendations.append("Sistema operando com qualidade adequada")
        
        return recommendations
    
    async def update_validation_rules(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza regras de validação"""
        try:
            new_rules = request_data.get('rules', {})
            updated_count = 0
            
            for rule_id, rule_data in new_rules.items():
                if rule_id in self.validation_rules:
                    # Atualizar regra existente
                    rule = self.validation_rules[rule_id]
                    
                    if 'enabled' in rule_data:
                        rule.enabled = rule_data['enabled']
                        updated_count += 1
                    
                    if 'severity' in rule_data:
                        rule.severity = ValidationSeverity(rule_data['severity'])
                        updated_count += 1
            
            return {
                'status': 'completed',
                'rules_updated': updated_count,
                'total_rules': len(self.validation_rules)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro atualizando regras: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _validate_message_real_time(self, message: AgentMessage):
        """Valida mensagem em tempo real"""
        try:
            content = str(message.content)
            
            # Validação rápida de segurança
            for pattern in self.security_patterns.values():
                if pattern.search(content):
                    logger.warning(f"🚨 Conteúdo suspeito detectado em mensagem de {message.sender_id}")
                    # Notificar sobre problema
                    await self._send_security_alert(message, "Suspicious content detected")
            
        except Exception as e:
            logger.error(f"❌ Erro na validação em tempo real: {e}")
    
    async def _send_security_alert(self, message: AgentMessage, alert_message: str):
        """Envia alerta de segurança"""
        alert = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.CRITICAL,
            content={
                'notification_type': 'security_alert',
                'original_sender': message.sender_id,
                'alert_message': alert_message,
                'timestamp': datetime.now().isoformat()
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(alert)
    
    async def _monitor_system_quality(self):
        """Monitora qualidade geral do sistema"""
        # Atualizar score geral do sistema
        if self.validation_history:
            recent_scores = [v['score'] for v in list(self.validation_history)[-50:]]
            self.validation_metrics['system_quality_score'] = sum(recent_scores) / len(recent_scores)
    
    async def _analyze_quality_trends(self):
        """Analisa tendências de qualidade"""
        if len(self.validation_history) < 20:
            return
        
        # Comparar últimas 10 vs 10 anteriores
        recent = list(self.validation_history)[-10:]
        previous = list(self.validation_history)[-20:-10]
        
        recent_avg = sum(v['score'] for v in recent) / len(recent)
        previous_avg = sum(v['score'] for v in previous) / len(previous)
        
        trend = (recent_avg - previous_avg) / previous_avg * 100
        
        if trend < -10:  # Degradação de mais de 10%
            await self._send_quality_degradation_alert(trend)
    
    async def _send_quality_degradation_alert(self, trend: float):
        """Envia alerta de degradação de qualidade"""
        alert = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="metacognitive_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.HIGH,
            content={
                'notification_type': 'quality_degradation',
                'trend_percentage': trend,
                'recommendation': 'Investigar causa da degradação de qualidade'
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(alert)
    
    async def _update_validation_rules(self):
        """Atualiza regras baseado em aprendizado"""
        # Análise de falsos positivos
        # Em produção, implementaria machine learning para ajustar regras
        pass
    
    async def _generate_quality_report(self) -> ValidationReport:
        """Gera relatório detalhado de qualidade"""
        recent = list(self.validation_history)[-100:]
        
        total_checks = len(recent)
        passed = len([v for v in recent if v['score'] >= 80])
        failed = len([v for v in recent if v['score'] < 50])
        warnings = len([v for v in recent if 50 <= v['score'] < 80])
        
        overall_score = sum(v['score'] for v in recent) / len(recent) if recent else 0
        
        report = ValidationReport(
            report_id=f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            subject="System Quality Analysis",
            total_checks=total_checks,
            passed=passed,
            failed=failed,
            warnings=warnings,
            blocked=self.validation_metrics['blocked_dangerous_content'],
            overall_score=overall_score,
            critical_issues=[],  # Seria populado com issues críticas
            recommendations=self._generate_system_recommendations(recent)
        )
        
        return report
    
    async def _send_quality_report(self, report: ValidationReport):
        """Envia relatório de qualidade"""
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.MEDIUM,
            content={
                'notification_type': 'quality_report',
                'report': {
                    'report_id': report.report_id,
                    'overall_score': report.overall_score,
                    'total_checks': report.total_checks,
                    'summary': f"{report.passed} passed, {report.failed} failed, {report.warnings} warnings"
                }
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)
    
    async def _cleanup_cache(self):
        """Limpa cache antigo"""
        cutoff = datetime.now() - timedelta(seconds=self.cache_ttl)
        
        # Limpar consistency cache
        expired_keys = [
            k for k, v in self.consistency_cache.items()
            if v['timestamp'] < cutoff
        ]
        for key in expired_keys:
            del self.consistency_cache[key]
        
        # Limpar validation cache
        expired_validation_keys = [
            k for k, v in self.validation_cache.items()
            if v.get('timestamp', datetime.min) < cutoff
        ]
        for key in expired_validation_keys:
            del self.validation_cache[key]
    
    async def _cleanup_history(self):
        """Limpa histórico antigo"""
        # Manter apenas últimas 10000 validações
        while len(self.validation_history) > 10000:
            self.validation_history.popleft()
    
    def _result_to_dict(self, result: ValidationResult) -> Dict[str, Any]:
        """Converte resultado para dicionário"""
        return {
            'validation_id': result.validation_id,
            'type': result.validation_type.value,
            'status': result.status.value,
            'severity': result.severity.value,
            'message': result.message,
            'details': result.details,
            'suggestions': result.suggestions,
            'confidence': result.confidence,
            'timestamp': result.timestamp.isoformat()
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

def create_validation_sentinel_agent(message_bus, num_instances=1) -> List[ValidationSentinelAgent]:
    """
    Cria o Guardian Supremo de Qualidade
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 ValidationSentinelAgent
    """
    agents = []
    
    try:
        logger.info("🛡️ Criando ValidationSentinelAgent - Guardian Supremo de Qualidade...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "validation_sentinel_001"
        
        if agent_id not in existing_agents:
            try:
                agent = ValidationSentinelAgent(agent_id, AgentType.GUARD, message_bus)
                
                # Iniciar serviços do Sentinel
                asyncio.create_task(agent.start_sentinel_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado como Guardian Supremo")
                logger.info(f"   🛡️ Capacidades: {len(agent.capabilities)} sistemas de validação")
                logger.info(f"   🔍 Regras: {len(agent.validation_rules)} regras ativas")
                logger.info(f"   ⚡ Modo: Monitoramento em tempo real {'ativo' if agent.real_time_monitoring else 'inativo'}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} ValidationSentinelAgent criado com sucesso")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando ValidationSentinelAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
