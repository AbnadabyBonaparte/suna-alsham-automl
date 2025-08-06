#!/usr/bin/env python3
"""
Módulo do Debug Master Agent - O Agente de Debug Supremo do SUNA-ALSHAM.
Versão corrigida e otimizada com implementação completa do BaseNetworkAgent.
"""

import asyncio
import logging
import sys
import traceback
import time
import re
import psutil
import gc
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# --- Bloco de Importação Corrigido e Padronizado ---
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Enums e Dataclasses ---

class IssueCategory(Enum):
    """Categorias de problemas detectados pelo debug agent."""
    RUNTIME_ERROR = "runtime_error"
    LOGIC_ERROR = "logic_error"
    PERFORMANCE_ISSUE = "performance_issue"
    MEMORY_LEAK = "memory_leak"
    DEPENDENCY_ISSUE = "dependency_issue"
    IMPORT_ERROR = "import_error"
    NETWORK_ERROR = "network_error"
    DATABASE_ERROR = "database_error"

class IssueSeverity(Enum):
    """Severidade dos problemas."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ResolutionStrategy(Enum):
    """Estratégias de resolução de problemas."""
    AUTO_FIX = "auto_fix"
    GUIDED_FIX = "guided_fix"
    MANUAL_INTERVENTION = "manual_intervention"
    RESTART_REQUIRED = "restart_required"

@dataclass
class DebugIssue:
    """Estrutura para armazenar informações detalhadas de um problema."""
    issue_id: str
    category: IssueCategory
    severity: IssueSeverity
    title: str
    description: str
    location: Dict[str, Any]
    stack_trace: Optional[str]
    suggested_fixes: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    affected_agents: List[str] = field(default_factory=list)
    resolution_strategy: ResolutionStrategy = ResolutionStrategy.MANUAL_INTERVENTION

@dataclass
class SystemMetrics:
    """Métricas do sistema para análise de performance."""
    cpu_percent: float
    memory_percent: float
    memory_available: int
    active_threads: int
    garbage_objects: int
    timestamp: datetime = field(default_factory=datetime.now)

# --- Classe Principal do Agente ---

class DebugMasterAgent(BaseNetworkAgent):
    """
    Agente supremo de debugging e diagnóstico do ALSHAM QUANTUM.
    Monitora erros, analisa performance e sugere correções automaticamente.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DebugMasterAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        
        # Capacidades do agente
        self.capabilities.extend([
            "error_detection",
            "automatic_debugging", 
            "issue_diagnosis",
            "performance_monitoring",
            "memory_analysis",
            "system_health_check",
            "auto_recovery",
            "log_analysis"
        ])
        
        # Base de dados de problemas
        self.issue_database = deque(maxlen=1000)
        self.resolved_issues = deque(maxlen=500)
        self.system_metrics_history = deque(maxlen=100)
        
        # Contadores
        self.issues_detected = 0
        self.issues_resolved = 0
        self.auto_fixes_applied = 0
        
        # Estado do monitoramento
        self.monitoring_active = False
        self.performance_monitoring_task = None
        
        # Setup inicial
        self._setup_exception_hook()
        logger.info(f"🐛 {self.agent_id} (Debug Master) inicializado com sucesso.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas pelo agente."""
        try:
            content = message.content
            message_type = content.get("type", "unknown")
            
            if message_type == "debug_request":
                await self._handle_debug_request(message)
            elif message_type == "system_health_check":
                await self._handle_health_check_request(message)
            elif message_type == "issue_report":
                await self._handle_issue_report(message)
            elif message_type == "start_monitoring":
                await self._start_performance_monitoring()
                await self.publish_response(message, {"status": "monitoring_started"})
            elif message_type == "stop_monitoring":
                await self._stop_performance_monitoring()
                await self.publish_response(message, {"status": "monitoring_stopped"})
            elif message_type == "get_statistics":
                stats = await self._get_debug_statistics()
                await self.publish_response(message, stats)
            else:
                await self.publish_error_response(message, f"Tipo de mensagem não reconhecido: {message_type}")
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro interno: {str(e)}")

    async def _handle_debug_request(self, message: AgentMessage):
        """Processa solicitação de debug de outro agente."""
        try:
            content = message.content
            target_agent = content.get("target_agent", "unknown")
            error_info = content.get("error_info", {})
            
            # Analisa o erro
            issue = await self._analyze_error(target_agent, error_info)
            self.issue_database.append(issue)
            self.issues_detected += 1
            
            # Tenta aplicar correção automática
            if issue.resolution_strategy == ResolutionStrategy.AUTO_FIX:
                fix_result = await self._attempt_auto_fix(issue)
                if fix_result["success"]:
                    self.auto_fixes_applied += 1
                    self.resolved_issues.append(issue)
                    
            response = {
                "issue_id": issue.issue_id,
                "severity": issue.severity.value,
                "suggested_fixes": issue.suggested_fixes,
                "auto_fix_applied": issue.resolution_strategy == ResolutionStrategy.AUTO_FIX
            }
            
            await self.publish_response(message, response)
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro no debug request: {str(e)}")

    async def _handle_health_check_request(self, message: AgentMessage):
        """Realiza verificação completa de saúde do sistema."""
        try:
            health_report = await self._comprehensive_health_check()
            await self.publish_response(message, health_report)
        except Exception as e:
            await self.publish_error_response(message, f"Erro no health check: {str(e)}")

    async def _handle_issue_report(self, message: AgentMessage):
        """Processa relatório de problema enviado por outro agente."""
        try:
            content = message.content
            issue = DebugIssue(
                issue_id=f"issue_{int(time.time())}_{len(self.issue_database)}",
                category=IssueCategory(content.get("category", "runtime_error")),
                severity=IssueSeverity(content.get("severity", "medium")),
                title=content.get("title", "Problema relatado"),
                description=content.get("description", ""),
                location=content.get("location", {}),
                stack_trace=content.get("stack_trace"),
                affected_agents=[message.sender_id]
            )
            
            self.issue_database.append(issue)
            self.issues_detected += 1
            
            # Notifica sobre problemas críticos
            if issue.severity == IssueSeverity.CRITICAL:
                await self._notify_critical_issue(issue)
            
            await self.publish_response(message, {"issue_recorded": issue.issue_id})
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao processar issue report: {str(e)}")

    async def _analyze_error(self, target_agent: str, error_info: Dict[str, Any]) -> DebugIssue:
        """Analisa um erro e cria um DebugIssue com sugestões de correção."""
        error_type = error_info.get("type", "unknown")
        error_message = error_info.get("message", "")
        stack_trace = error_info.get("stack_trace", "")
        
        # Determina categoria baseada no tipo de erro
        category = self._classify_error(error_type, error_message)
        severity = self._assess_severity(error_type, error_message, target_agent)
        
        # Gera sugestões de correção
        suggested_fixes = self._generate_fix_suggestions(category, error_type, error_message)
        
        # Determina estratégia de resolução
        resolution_strategy = self._determine_resolution_strategy(category, severity)
        
        issue = DebugIssue(
            issue_id=f"debug_{int(time.time())}_{target_agent}",
            category=category,
            severity=severity,
            title=f"{error_type} em {target_agent}",
            description=error_message,
            location=self._extract_location_from_stack(stack_trace),
            stack_trace=stack_trace,
            suggested_fixes=suggested_fixes,
            affected_agents=[target_agent],
            resolution_strategy=resolution_strategy
        )
        
        return issue

    def _classify_error(self, error_type: str, error_message: str) -> IssueCategory:
        """Classifica o tipo de erro baseado em padrões conhecidos."""
        error_type_lower = error_type.lower()
        error_message_lower = error_message.lower()
        
        if "import" in error_type_lower or "module" in error_message_lower:
            return IssueCategory.IMPORT_ERROR
        elif "memory" in error_message_lower or "outofmemory" in error_type_lower:
            return IssueCategory.MEMORY_LEAK
        elif "connection" in error_message_lower or "network" in error_message_lower:
            return IssueCategory.NETWORK_ERROR
        elif "database" in error_message_lower or "sql" in error_message_lower:
            return IssueCategory.DATABASE_ERROR
        elif "performance" in error_message_lower or "timeout" in error_message_lower:
            return IssueCategory.PERFORMANCE_ISSUE
        else:
            return IssueCategory.RUNTIME_ERROR

    def _assess_severity(self, error_type: str, error_message: str, target_agent: str) -> IssueSeverity:
        """Avalia a severidade de um erro."""
        # Erros críticos para agentes core
        critical_agents = ["orchestrator", "message_bus", "security", "api_gateway"]
        if any(agent in target_agent for agent in critical_agents):
            return IssueSeverity.CRITICAL
            
        # Padrões de alta severidade
        high_severity_patterns = ["fatal", "critical", "system", "crash", "abort"]
        if any(pattern in error_message.lower() for pattern in high_severity_patterns):
            return IssueSeverity.HIGH
            
        # Padrões de média severidade
        medium_severity_patterns = ["error", "exception", "failed", "timeout"]
        if any(pattern in error_message.lower() for pattern in medium_severity_patterns):
            return IssueSeverity.MEDIUM
            
        return IssueSeverity.LOW

    def _generate_fix_suggestions(self, category: IssueCategory, error_type: str, error_message: str) -> List[str]:
        """Gera sugestões específicas de correção baseadas no tipo de erro."""
        suggestions = []
        
        if category == IssueCategory.IMPORT_ERROR:
            suggestions.extend([
                "Verificar se o módulo está instalado no requirements.txt",
                "Verificar se o caminho de importação está correto",
                "Executar 'pip install -r requirements.txt'",
                "Verificar se há dependências circulares"
            ])
        elif category == IssueCategory.MEMORY_LEAK:
            suggestions.extend([
                "Implementar garbage collection explícito",
                "Verificar vazamentos de memória em loops",
                "Otimizar estruturas de dados grandes",
                "Usar weak references onde apropriado"
            ])
        elif category == IssueCategory.NETWORK_ERROR:
            suggestions.extend([
                "Verificar conectividade de rede",
                "Implementar retry logic com backoff",
                "Verificar configuração de timeout",
                "Validar URLs e endpoints"
            ])
        elif category == IssueCategory.DATABASE_ERROR:
            suggestions.extend([
                "Verificar string de conexão DATABASE_URL",
                "Verificar se o banco está acessível",
                "Implementar connection pooling",
                "Validar queries SQL"
            ])
        elif category == IssueCategory.PERFORMANCE_ISSUE:
            suggestions.extend([
                "Otimizar algoritmos críticos",
                "Implementar caching onde apropriado",
                "Usar processamento assíncrono",
                "Fazer profiling de performance"
            ])
        else:
            suggestions.extend([
                "Verificar logs detalhados",
                "Implementar try/catch apropriado",
                "Validar entrada de dados",
                "Testar cenários edge case"
            ])
            
        return suggestions

    def _determine_resolution_strategy(self, category: IssueCategory, severity: IssueSeverity) -> ResolutionStrategy:
        """Determina a estratégia de resolução baseada na categoria e severidade."""
        if severity == IssueSeverity.CRITICAL:
            return ResolutionStrategy.RESTART_REQUIRED
        elif category in [IssueCategory.IMPORT_ERROR, IssueCategory.DEPENDENCY_ISSUE]:
            return ResolutionStrategy.MANUAL_INTERVENTION
        elif severity == IssueSeverity.LOW:
            return ResolutionStrategy.AUTO_FIX
        else:
            return ResolutionStrategy.GUIDED_FIX

    async def _attempt_auto_fix(self, issue: DebugIssue) -> Dict[str, Any]:
        """Tenta aplicar correção automática para problemas simples."""
        try:
            if issue.category == IssueCategory.MEMORY_LEAK:
                # Force garbage collection
                gc.collect()
                return {"success": True, "action": "garbage_collection_forced"}
            elif issue.category == IssueCategory.PERFORMANCE_ISSUE:
                # Otimização básica
                return {"success": True, "action": "performance_optimization_suggested"}
            else:
                return {"success": False, "reason": "auto_fix_not_available"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _start_performance_monitoring(self):
        """Inicia monitoramento contínuo de performance do sistema."""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.performance_monitoring_task = asyncio.create_task(self._performance_monitoring_loop())
            logger.info("🔍 Performance monitoring iniciado")

    async def _stop_performance_monitoring(self):
        """Para o monitoramento de performance."""
        if self.monitoring_active:
            self.monitoring_active = False
            if self.performance_monitoring_task:
                self.performance_monitoring_task.cancel()
                try:
                    await self.performance_monitoring_task
                except asyncio.CancelledError:
                    pass
            logger.info("⏹️ Performance monitoring parado")

    async def _performance_monitoring_loop(self):
        """Loop principal de monitoramento de performance."""
        try:
            while self.monitoring_active:
                metrics = await self._collect_system_metrics()
                self.system_metrics_history.append(metrics)
                
                # Analisa métricas e detecta problemas
                await self._analyze_system_metrics(metrics)
                
                await asyncio.sleep(30)  # Coleta métricas a cada 30 segundos
        except asyncio.CancelledError:
            logger.info("Performance monitoring loop cancelado")
        except Exception as e:
            logger.error(f"Erro no monitoring loop: {e}", exc_info=True)

    async def _collect_system_metrics(self) -> SystemMetrics:
        """Coleta métricas atuais do sistema."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            process = psutil.Process()
            
            metrics = SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_available=memory.available,
                active_threads=process.num_threads(),
                garbage_objects=len(gc.get_objects())
            )
            
            return metrics
        except Exception as e:
            logger.error(f"Erro ao coletar métricas: {e}")
            return SystemMetrics(0, 0, 0, 0, 0)

    async def _analyze_system_metrics(self, metrics: SystemMetrics):
        """Analisa métricas e detecta problemas de performance."""
        issues_detected = []
        
        # Detecta high CPU usage
        if metrics.cpu_percent > 85:
            issue = DebugIssue(
                issue_id=f"perf_cpu_{int(time.time())}",
                category=IssueCategory.PERFORMANCE_ISSUE,
                severity=IssueSeverity.HIGH,
                title="Alto uso de CPU detectado",
                description=f"CPU usage: {metrics.cpu_percent:.1f}%",
                location={"component": "system", "metric": "cpu"},
                stack_trace=None,
                suggested_fixes=["Identificar processos com alto CPU", "Otimizar algoritmos", "Implementar rate limiting"]
            )
            issues_detected.append(issue)
        
        # Detecta high memory usage
        if metrics.memory_percent > 90:
            issue = DebugIssue(
                issue_id=f"perf_mem_{int(time.time())}",
                category=IssueCategory.MEMORY_LEAK,
                severity=IssueSeverity.HIGH,
                title="Alto uso de memória detectado",
                description=f"Memory usage: {metrics.memory_percent:.1f}%",
                location={"component": "system", "metric": "memory"},
                stack_trace=None,
                suggested_fixes=["Forçar garbage collection", "Identificar vazamentos", "Otimizar estruturas de dados"]
            )
            issues_detected.append(issue)
        
        # Registra issues detectados
        for issue in issues_detected:
            self.issue_database.append(issue)
            self.issues_detected += 1
            
            if issue.severity == IssueSeverity.HIGH:
                await self._notify_critical_issue(issue)

    async def _comprehensive_health_check(self) -> Dict[str, Any]:
        """Realiza verificação completa de saúde do sistema."""
        current_metrics = await self._collect_system_metrics()
        
        # Calcula scores de saúde
        cpu_score = max(0, 100 - current_metrics.cpu_percent)
        memory_score = max(0, 100 - current_metrics.memory_percent)
        
        # Score geral
        overall_score = (cpu_score + memory_score) / 2
        
        # Status baseado no score
        if overall_score >= 80:
            health_status = "healthy"
        elif overall_score >= 60:
            health_status = "warning"
        else:
            health_status = "critical"
        
        return {
            "health_status": health_status,
            "overall_score": f"{overall_score:.1f}%",
            "current_metrics": {
                "cpu_percent": current_metrics.cpu_percent,
                "memory_percent": current_metrics.memory_percent,
                "memory_available_mb": current_metrics.memory_available // (1024*1024),
                "active_threads": current_metrics.active_threads,
                "garbage_objects": current_metrics.garbage_objects
            },
            "statistics": await self._get_debug_statistics(),
            "recent_issues": len([i for i in self.issue_database if (datetime.now() - i.timestamp).seconds < 3600])
        }

    async def _get_debug_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas detalhadas do debug agent."""
        return {
            "issues_detected": self.issues_detected,
            "issues_resolved": self.issues_resolved,
            "auto_fixes_applied": self.auto_fixes_applied,
            "issues_in_database": len(self.issue_database),
            "monitoring_active": self.monitoring_active,
            "uptime": f"{(datetime.now() - datetime.now()).total_seconds():.0f}s",
            "issue_breakdown": {
                category.value: len([i for i in self.issue_database if i.category == category])
                for category in IssueCategory
            },
            "severity_breakdown": {
                severity.value: len([i for i in self.issue_database if i.severity == severity])
                for severity in IssueSeverity
            }
        }

    def _setup_exception_hook(self):
        """Configura hook global para capturar exceções não tratadas."""
        original_hook = sys.excepthook

        def exception_handler(exc_type, exc_value, exc_traceback):
            # Não intercepta KeyboardInterrupt e SystemExit
            if issubclass(exc_type, (KeyboardInterrupt, SystemExit)):
                original_hook(exc_type, exc_value, exc_traceback)
                return

            # Formata traceback
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            full_traceback = "".join(tb_lines)

            # Cria task assíncrona para processar exceção
            asyncio.create_task(
                self._process_uncaught_exception(exc_type, exc_value, full_traceback)
            )

            # Chama handler original também
            original_hook(exc_type, exc_value, exc_traceback)

        sys.excepthook = exception_handler
        logger.info("🔧 Hook de exceções global instalado com sucesso")

    async def _process_uncaught_exception(self, exc_type, exc_value, full_traceback: str):
        """Processa exceção não tratada capturada pelo hook."""
        try:
            issue = DebugIssue(
                issue_id=f"uncaught_{int(time.time())}",
                category=IssueCategory.RUNTIME_ERROR,
                severity=IssueSeverity.CRITICAL,
                title=f"Exceção não tratada: {exc_type.__name__}",
                description=str(exc_value),
                location=self._extract_location_from_stack(full_traceback),
                stack_trace=full_traceback,
                suggested_fixes=self._generate_fix_suggestions(IssueCategory.RUNTIME_ERROR, exc_type.__name__, str(exc_value))
            )
            
            self.issue_database.append(issue)
            self.issues_detected += 1
            
            await self._notify_critical_issue(issue)
            logger.critical(f"🚨 Exceção não tratada capturada: {issue.title}")
            
        except Exception as e:
            logger.error(f"Erro ao processar exceção não tratada: {e}")

    async def _notify_critical_issue(self, issue: DebugIssue):
        """Notifica sobre problema crítico para o orquestrador."""
        try:
            notification_content = {
                "type": "critical_issue",
                "issue_id": issue.issue_id,
                "title": issue.title,
                "severity": issue.severity.value,
                "category": issue.category.value,
                "affected_agents": issue.affected_agents,
                "suggested_fixes": issue.suggested_fixes[:3],  # Primeiras 3 sugestões
                "requires_immediate_attention": True
            }
            
            notification = self.create_message(
                recipient_id="orchestrator_001",
                message_type=MessageType.NOTIFICATION,
                priority=Priority.CRITICAL,
                content=notification_content,
            )
            
            await self.message_bus.publish(notification)
            logger.warning(f"🚨 Problema crítico notificado: {issue.title}")
            
        except Exception as e:
            logger.error(f"Erro ao notificar problema crítico: {e}")

    def _extract_location_from_stack(self, stack_trace: str) -> Dict[str, Any]:
        """Extrai informações de localização do stack trace."""
        try:
            # Procura por padrão: File "arquivo.py", line 123, in função
            match = re.search(r'File "(.+)", line (\d+), in (.+)', stack_trace)
            if match:
                return {
                    "file": match.group(1),
                    "line": int(match.group(2)),
                    "function": match.group(3).strip(),
                    "module": match.group(1).split("/")[-1].replace(".py", "")
                }
        except Exception as e:
            logger.debug(f"Erro ao extrair localização: {e}")
        
        return {
            "file": "unknown",
            "line": 0, 
            "function": "unknown",
            "module": "unknown"
        }


def create_agents(message_bus: Any) -> List[BaseNetworkAgent]:
    """
    Factory function para criar e inicializar o DebugMasterAgent.
    
    Esta função instancia o DebugMasterAgent, registra logs para diagnósticos,
    e o retorna em uma lista para registro no agent registry.
    
    Args:
        message_bus (Any): O message bus para comunicação entre agentes.
        
    Returns:
        List[BaseNetworkAgent]: Lista contendo a instância do DebugMasterAgent.
    """
    agents: List[BaseNetworkAgent] = []
    
    try:
        logger.info("🐛 [Factory] Criando DebugMasterAgent...")
        
        # Cria o agente
        agent = DebugMasterAgent("debug_master_001", message_bus)
        agents.append(agent)
        
        logger.info(f"✅ DebugMasterAgent criado com sucesso: {agent.agent_id}")
        logger.info(f"🔧 Capabilities: {', '.join(agent.capabilities)}")
        
    except Exception as e:
        logger.critical(f"❌ Erro crítico ao criar DebugMasterAgent: {e}", exc_info=True)
    
    return agents
