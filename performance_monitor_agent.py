import logging
import time
import asyncio
import psutil
import gc
import sys
import tracemalloc
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics
import json
from pathlib import Path
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Tipos de métricas monitoradas"""
    EXECUTION_TIME = "execution_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    CODE_COMPLEXITY = "code_complexity"
    RESPONSE_TIME = "response_time"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    RESOURCE_EFFICIENCY = "resource_efficiency"

class PerformanceStatus(Enum):
    """Status de performance"""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    NEEDS_IMPROVEMENT = "needs_improvement"
    CRITICAL = "critical"
    DEGRADED = "degraded"

@dataclass
class PerformanceMetric:
    """Métrica de performance individual"""
    metric_id: str
    metric_type: MetricType
    value: float
    unit: str
    file_path: Optional[str]
    function_name: Optional[str]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceSnapshot:
    """Snapshot de performance em um momento"""
    snapshot_id: str
    metrics: List[PerformanceMetric]
    overall_status: PerformanceStatus
    cpu_percent: float
    memory_mb: float
    active_threads: int
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class PerformanceComparison:
    """Comparação de performance antes/depois"""
    comparison_id: str
    file_path: str
    before_metrics: Dict[str, float]
    after_metrics: Dict[str, float]
    improvements: Dict[str, float]
    degradations: Dict[str, float]
    overall_improvement: float
    status: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class PerformanceReport:
    """Relatório completo de performance"""
    report_id: str
    period_start: datetime
    period_end: datetime
    total_measurements: int
    average_metrics: Dict[MetricType, float]
    peak_metrics: Dict[MetricType, float]
    bottlenecks: List[Dict[str, Any]]
    recommendations: List[str]
    overall_health: PerformanceStatus
    trends: Dict[str, str]

class PerformanceMonitorAgent(BaseNetworkAgent):
    """Agente especializado em monitoramento e validação de performance"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'performance_monitoring',
            'optimization_validation',
            'bottleneck_detection',
            'resource_tracking',
            'regression_detection',
            'benchmark_execution',
            'profiling',
            'trend_analysis'
        ]
        self.status = 'active'
        
        # Estado do monitor
        self.monitoring_queue = asyncio.Queue()
        self.metrics_history = defaultdict(lambda: deque(maxlen=1000))
        self.performance_snapshots = deque(maxlen=100)
        self.comparison_results = []
        self.active_monitors = {}  # file_path -> monitor_data
        
        # Configurações
        self.monitoring_interval = 5  # segundos
        self.profiling_enabled = True
        self.memory_tracking_enabled = True
        self.alert_thresholds = {
            'cpu_percent': 80,
            'memory_mb': 500,
            'execution_time': 5.0,  # segundos
            'error_rate': 0.05  # 5%
        }
        
        # Baselines de performance
        self.performance_baselines = {}
        self.regression_threshold = 0.2  # 20% de degradação
        
        # Estatísticas
        self.monitoring_metrics = {
            'files_monitored': 0,
            'metrics_collected': 0,
            'regressions_detected': 0,
            'improvements_validated': 0,
            'alerts_generated': 0
        }
        
        # Profiling
        if self.memory_tracking_enabled:
            tracemalloc.start()
        
        # Tasks de background
        self._monitoring_task = None
        self._analysis_task = None
        self._cleanup_task = None
        
        logger.info(f"📊 {self.agent_id} inicializado com monitoramento avançado")
    
    async def start_monitoring_service(self):
        """Inicia serviço de monitoramento"""
        if not self._monitoring_task:
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            self._analysis_task = asyncio.create_task(self._analysis_loop())
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
            logger.info(f"📊 {self.agent_id} iniciou serviços de monitoramento")
    
    async def stop_monitoring_service(self):
        """Para serviço de monitoramento"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
        if self._analysis_task:
            self._analysis_task.cancel()
            self._analysis_task = None
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None
        
        if self.memory_tracking_enabled:
            tracemalloc.stop()
        
        logger.info(f"🛑 {self.agent_id} parou serviços de monitoramento")
    
    async def _monitoring_loop(self):
        """Loop principal de monitoramento"""
        while True:
            try:
                # Coletar métricas do sistema
                await self._collect_system_metrics()
                
                # Processar fila de monitoramento
                if not self.monitoring_queue.empty():
                    monitor_request = await self.monitoring_queue.get()
                    await self._process_monitor_request(monitor_request)
                
                await asyncio.sleep(self.monitoring_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de monitoramento: {e}")
    
    async def _analysis_loop(self):
        """Loop de análise de tendências"""
        while True:
            try:
                # Analisar tendências
                trends = self._analyze_trends()
                
                # Detectar anomalias
                anomalies = self._detect_anomalies()
                
                if anomalies:
                    await self._handle_anomalies(anomalies)
                
                # Gerar relatórios periódicos
                if len(self.performance_snapshots) >= 20:
                    report = await self._generate_performance_report()
                    await self._send_report(report)
                
                await asyncio.sleep(60)  # Análise a cada minuto
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de análise: {e}")
    
    async def _cleanup_loop(self):
        """Loop de limpeza de dados antigos"""
        while True:
            try:
                # Limpar métricas antigas
                cutoff_time = datetime.now() - timedelta(hours=24)
                
                for metric_type, history in self.metrics_history.items():
                    # Remover métricas antigas
                    while history and history[0].timestamp < cutoff_time:
                        history.popleft()
                
                await asyncio.sleep(3600)  # Limpeza a cada hora
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no cleanup: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'monitor_performance':
                result = await self.monitor_performance(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'validate_optimization':
                result = await self.validate_optimization(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'profile_code':
                result = await self.profile_code(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'get_performance_report':
                result = await self.get_performance_report(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'detect_bottlenecks':
                result = await self.detect_bottlenecks(message.content)
                await self._send_response(message, result)
        
        elif message.message_type == MessageType.NOTIFICATION:
            # Processar notificações de correções
            if message.content.get('notification_type') == 'correction_completed':
                await self._handle_correction_notification(message.content)
    
    async def monitor_performance(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitora performance de um arquivo ou função"""
        try:
            file_path = request_data.get('file_path')
            function_name = request_data.get('function_name')
            duration = request_data.get('duration', 60)  # segundos
            
            logger.info(f"📊 Iniciando monitoramento: {file_path}")
            
            # Criar monitor
            monitor_id = f"monitor_{len(self.active_monitors)}"
            monitor_data = {
                'monitor_id': monitor_id,
                'file_path': file_path,
                'function_name': function_name,
                'start_time': datetime.now(),
                'end_time': datetime.now() + timedelta(seconds=duration),
                'metrics': []
            }
            
            self.active_monitors[file_path] = monitor_data
            
            # Coletar métricas iniciais
            initial_metrics = await self._collect_file_metrics(file_path, function_name)
            
            # Agendar monitoramento contínuo
            await self.monitoring_queue.put({
                'type': 'continuous_monitor',
                'monitor_data': monitor_data
            })
            
            self.monitoring_metrics['files_monitored'] += 1
            
            return {
                'status': 'started',
                'monitor_id': monitor_id,
                'file_path': file_path,
                'duration': duration,
                'initial_metrics': self._metrics_to_dict(initial_metrics)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro iniciando monitoramento: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _collect_file_metrics(self, file_path: str, function_name: Optional[str] = None) -> List[PerformanceMetric]:
        """Coleta métricas de um arquivo específico"""
        metrics = []
        
        try:
            # Métricas de execução (simuladas em produção real)
            if function_name:
                # Simular tempo de execução
                exec_time = await self._measure_execution_time(file_path, function_name)
                metrics.append(PerformanceMetric(
                    metric_id=f"exec_{len(metrics)}",
                    metric_type=MetricType.EXECUTION_TIME,
                    value=exec_time,
                    unit="seconds",
                    file_path=file_path,
                    function_name=function_name
                ))
            
            # Métricas de memória
            if self.memory_tracking_enabled:
                memory_usage = self._get_memory_usage()
                metrics.append(PerformanceMetric(
                    metric_id=f"mem_{len(metrics)}",
                    metric_type=MetricType.MEMORY_USAGE,
                    value=memory_usage,
                    unit="MB",
                    file_path=file_path
                ))
            
            # Métricas de CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            metrics.append(PerformanceMetric(
                metric_id=f"cpu_{len(metrics)}",
                metric_type=MetricType.CPU_USAGE,
                value=cpu_percent,
                unit="percent",
                file_path=file_path
            ))
            
            # Adicionar ao histórico
            for metric in metrics:
                self.metrics_history[metric.metric_type].append(metric)
                self.monitoring_metrics['metrics_collected'] += 1
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Erro coletando métricas: {e}")
            return []
    
    async def _measure_execution_time(self, file_path: str, function_name: str) -> float:
        """Mede tempo de execução de uma função"""
        # Em produção, isso seria feito com profiling real
        # Aqui simulamos com base no tamanho do arquivo
        try:
            file_size = Path(file_path).stat().st_size if Path(file_path).exists() else 1000
            # Simulação: tempo proporcional ao tamanho
            base_time = 0.1
            size_factor = file_size / 10000
            return base_time + (size_factor * 0.5)
        except:
            return 0.5
    
    def _get_memory_usage(self) -> float:
        """Obtém uso de memória atual"""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # MB
    
    async def validate_optimization(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida se uma otimização melhorou a performance"""
        try:
            file_path = request_data.get('file_path')
            optimization_type = request_data.get('optimization_type', 'general')
            before_metrics = request_data.get('before_metrics', {})
            
            logger.info(f"🔍 Validando otimização em {file_path}")
            
            # Coletar métricas atuais
            current_metrics = await self._collect_file_metrics(file_path)
            
            # Comparar com baseline ou métricas anteriores
            if file_path in self.performance_baselines:
                baseline = self.performance_baselines[file_path]
            else:
                baseline = before_metrics
            
            # Realizar comparação
            comparison = self._compare_metrics(baseline, current_metrics)
            
            # Determinar se houve melhoria
            validation_result = self._validate_improvement(comparison, optimization_type)
            
            # Registrar resultado
            self.comparison_results.append(comparison)
            
            if validation_result['improved']:
                self.monitoring_metrics['improvements_validated'] += 1
            
            return {
                'status': 'completed',
                'file_path': file_path,
                'optimization_type': optimization_type,
                'improved': validation_result['improved'],
                'improvement_percentage': validation_result['improvement_percentage'],
                'details': validation_result['details'],
                'comparison': self._comparison_to_dict(comparison)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro validando otimização: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _compare_metrics(self, before: Any, after: List[PerformanceMetric]) -> PerformanceComparison:
        """Compara métricas antes e depois"""
        # Converter métricas after para dict
        after_dict = {}
        for metric in after:
            key = f"{metric.metric_type.value}_{metric.function_name or 'general'}"
            after_dict[key] = metric.value
        
        # Converter before para dict se necessário
        if isinstance(before, list):
            before_dict = {}
            for metric in before:
                key = f"{metric.metric_type.value}_{metric.function_name or 'general'}"
                before_dict[key] = metric.value
        else:
            before_dict = before
        
        # Calcular melhorias e degradações
        improvements = {}
        degradations = {}
        
        for key in set(before_dict.keys()) | set(after_dict.keys()):
            before_val = before_dict.get(key, 0)
            after_val = after_dict.get(key, 0)
            
            if before_val > 0:
                change_percent = ((after_val - before_val) / before_val) * 100
                
                # Para tempo e uso de recursos, menor é melhor
                if 'time' in key or 'usage' in key:
                    if change_percent < -5:  # Melhoria de mais de 5%
                        improvements[key] = abs(change_percent)
                    elif change_percent > 5:  # Degradação de mais de 5%
                        degradations[key] = change_percent
                else:
                    # Para throughput, maior é melhor
                    if change_percent > 5:
                        improvements[key] = change_percent
                    elif change_percent < -5:
                        degradations[key] = abs(change_percent)
        
        # Calcular melhoria geral
        overall_improvement = 0
        if improvements:
            overall_improvement = statistics.mean(improvements.values())
        if degradations:
            overall_improvement -= statistics.mean(degradations.values())
        
        return PerformanceComparison(
            comparison_id=f"comp_{len(self.comparison_results)}",
            file_path="",  # Será preenchido pelo caller
            before_metrics=before_dict,
            after_metrics=after_dict,
            improvements=improvements,
            degradations=degradations,
            overall_improvement=overall_improvement,
            status="improved" if overall_improvement > 0 else "degraded"
        )
    
    def _validate_improvement(self, comparison: PerformanceComparison, optimization_type: str) -> Dict[str, Any]:
        """Valida se houve melhoria significativa"""
        result = {
            'improved': False,
            'improvement_percentage': comparison.overall_improvement,
            'details': {}
        }
        
        # Critérios específicos por tipo de otimização
        if optimization_type == 'performance':
            # Espera-se melhoria em tempo de execução
            exec_improvements = {k: v for k, v in comparison.improvements.items() if 'execution_time' in k}
            if exec_improvements:
                result['improved'] = statistics.mean(exec_improvements.values()) > 10
                result['details']['execution_time'] = f"Melhorou {statistics.mean(exec_improvements.values()):.1f}%"
        
        elif optimization_type == 'memory':
            # Espera-se redução no uso de memória
            mem_improvements = {k: v for k, v in comparison.improvements.items() if 'memory' in k}
            if mem_improvements:
                result['improved'] = statistics.mean(mem_improvements.values()) > 5
                result['details']['memory_usage'] = f"Reduziu {statistics.mean(mem_improvements.values()):.1f}%"
        
        else:
            # Otimização geral - qualquer melhoria significativa
            result['improved'] = comparison.overall_improvement > 5
        
        # Verificar degradações
        if comparison.degradations:
            result['details']['warnings'] = f"{len(comparison.degradations)} métricas pioraram"
        
        return result
    
    async def profile_code(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza profiling detalhado de código"""
        try:
            file_path = request_data.get('file_path')
            profile_type = request_data.get('profile_type', 'cpu')
            
            logger.info(f"🔬 Profiling {profile_type} em {file_path}")
            
            profile_result = {}
            
            if profile_type == 'cpu':
                profile_result = await self._profile_cpu(file_path)
            elif profile_type == 'memory':
                profile_result = await self._profile_memory(file_path)
            elif profile_type == 'io':
                profile_result = await self._profile_io(file_path)
            else:
                profile_result = await self._profile_comprehensive(file_path)
            
            return {
                'status': 'completed',
                'file_path': file_path,
                'profile_type': profile_type,
                'results': profile_result,
                'recommendations': self._generate_profiling_recommendations(profile_result)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no profiling: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _profile_cpu(self, file_path: str) -> Dict[str, Any]:
        """Profile de CPU"""
        # Simulação de profiling
        return {
            'hotspots': [
                {'function': 'process_data', 'time_percent': 45.2},
                {'function': 'calculate_metrics', 'time_percent': 23.8}
            ],
            'total_time': 2.5,
            'call_count': 1500
        }
    
    async def _profile_memory(self, file_path: str) -> Dict[str, Any]:
        """Profile de memória"""
        if self.memory_tracking_enabled:
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')[:10]
            
            return {
                'top_allocations': [
                    {
                        'file': stat.traceback.format()[0] if stat.traceback else 'unknown',
                        'size_mb': stat.size / 1024 / 1024,
                        'count': stat.count
                    }
                    for stat in top_stats
                ],
                'total_allocated_mb': sum(stat.size for stat in top_stats) / 1024 / 1024
            }
        
        return {'error': 'Memory tracking not enabled'}
    
    async def _profile_io(self, file_path: str) -> Dict[str, Any]:
        """Profile de I/O"""
        # Simulação
        return {
            'read_operations': 150,
            'write_operations': 75,
            'total_io_time': 0.8,
            'average_io_time': 0.0035
        }
    
    async def _profile_comprehensive(self, file_path: str) -> Dict[str, Any]:
        """Profile completo"""
        cpu = await self._profile_cpu(file_path)
        memory = await self._profile_memory(file_path)
        io = await self._profile_io(file_path)
        
        return {
            'cpu': cpu,
            'memory': memory,
            'io': io
        }
    
    def _generate_profiling_recommendations(self, profile_result: Dict[str, Any]) -> List[str]:
        """Gera recomendações baseadas no profiling"""
        recommendations = []
        
        # Análise de CPU
        if 'hotspots' in profile_result:
            hotspots = profile_result['hotspots']
            if hotspots and hotspots[0]['time_percent'] > 40:
                recommendations.append(
                    f"Função '{hotspots[0]['function']}' consome {hotspots[0]['time_percent']:.1f}% do tempo - considere otimizar"
                )
        
        # Análise de memória
        if 'total_allocated_mb' in profile_result:
            if profile_result['total_allocated_mb'] > 100:
                recommendations.append(
                    "Alto uso de memória detectado - verifique vazamentos ou estruturas desnecessárias"
                )
        
        # Análise de I/O
        if 'total_io_time' in profile_result:
            if profile_result['total_io_time'] > 1.0:
                recommendations.append(
                    "Tempo de I/O elevado - considere usar cache ou operações assíncronas"
                )
        
        if not recommendations:
            recommendations.append("Performance dentro dos parâmetros aceitáveis")
        
        return recommendations
    
    async def detect_bottlenecks(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detecta gargalos de performance"""
        try:
            scope = request_data.get('scope', 'system')  # system, file, function
            
            logger.info(f"🔍 Detectando gargalos no escopo: {scope}")
            
            bottlenecks = []
            
            # Analisar histórico de métricas
            for metric_type, history in self.metrics_history.items():
                if not history:
                    continue
                
                # Calcular estatísticas
                values = [m.value for m in history]
                if values:
                    avg_value = statistics.mean(values)
                    max_value = max(values)
                    
                    # Verificar limiares
                    if metric_type == MetricType.EXECUTION_TIME and avg_value > 2.0:
                        bottlenecks.append({
                            'type': 'slow_execution',
                            'metric': metric_type.value,
                            'average': avg_value,
                            'peak': max_value,
                            'severity': 'high' if avg_value > 5.0 else 'medium'
                        })
                    
                    elif metric_type == MetricType.MEMORY_USAGE and max_value > 500:
                        bottlenecks.append({
                            'type': 'high_memory',
                            'metric': metric_type.value,
                            'average': avg_value,
                            'peak': max_value,
                            'severity': 'high' if max_value > 1000 else 'medium'
                        })
                    
                    elif metric_type == MetricType.CPU_USAGE and avg_value > 70:
                        bottlenecks.append({
                            'type': 'cpu_intensive',
                            'metric': metric_type.value,
                            'average': avg_value,
                            'peak': max_value,
                            'severity': 'high' if avg_value > 85 else 'medium'
                        })
            
            # Ordenar por severidade
            bottlenecks.sort(key=lambda x: 0 if x['severity'] == 'high' else 1)
            
            return {
                'status': 'completed',
                'bottlenecks': bottlenecks,
                'total_found': len(bottlenecks),
                'recommendations': self._generate_bottleneck_recommendations(bottlenecks)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro detectando gargalos: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_bottleneck_recommendations(self, bottlenecks: List[Dict[str, Any]]) -> List[str]:
        """Gera recomendações para resolver gargalos"""
        recommendations = []
        
        for bottleneck in bottlenecks[:3]:  # Top 3 gargalos
            if bottleneck['type'] == 'slow_execution':
                recommendations.append(
                    "Otimizar algoritmos lentos ou considerar paralelização"
                )
            elif bottleneck['type'] == 'high_memory':
                recommendations.append(
                    "Implementar estratégias de gerenciamento de memória ou usar geradores"
                )
            elif bottleneck['type'] == 'cpu_intensive':
                recommendations.append(
                    "Considerar uso de multiprocessing ou otimizações de baixo nível"
                )
        
        return recommendations
    
    async def get_performance_report(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera relatório de performance"""
        try:
            period = request_data.get('period', 'last_hour')
            
            # Determinar período
            now = datetime.now()
            if period == 'last_hour':
                start_time = now - timedelta(hours=1)
            elif period == 'last_day':
                start_time = now - timedelta(days=1)
            else:
                start_time = now - timedelta(minutes=30)
            
            # Gerar relatório
            report = await self._generate_performance_report(start_time, now)
            
            return {
                'status': 'completed',
                'report': self._report_to_dict(report),
                'period': period
            }
            
        except Exception as e:
            logger.error(f"❌ Erro gerando relatório: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _collect_system_metrics(self):
        """Coleta métricas gerais do sistema"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memória
            memory = psutil.virtual_memory()
            memory_mb = memory.used / 1024 / 1024
            
            # Threads
            process = psutil.Process()
            thread_count = process.num_threads()
            
            # Criar snapshot
            snapshot = PerformanceSnapshot(
                snapshot_id=f"snap_{len(self.performance_snapshots)}",
                metrics=[],
                overall_status=self._determine_system_status(cpu_percent, memory.percent),
                cpu_percent=cpu_percent,
                memory_mb=memory_mb,
                active_threads=thread_count
            )
            
            self.performance_snapshots.append(snapshot)
            
            # Verificar alertas
            if cpu_percent > self.alert_thresholds['cpu_percent']:
                await self._generate_alert('high_cpu', cpu_percent)
            
            if memory_mb > self.alert_thresholds['memory_mb']:
                await self._generate_alert('high_memory', memory_mb)
                
        except Exception as e:
            logger.error(f"❌ Erro coletando métricas do sistema: {e}")
    
    def _determine_system_status(self, cpu: float, memory: float) -> PerformanceStatus:
        """Determina status geral do sistema"""
        if cpu > 90 or memory > 90:
            return PerformanceStatus.CRITICAL
        elif cpu > 80 or memory > 80:
            return PerformanceStatus.NEEDS_IMPROVEMENT
        elif cpu > 60 or memory > 60:
            return PerformanceStatus.ACCEPTABLE
        elif cpu > 40 or memory > 40:
            return PerformanceStatus.GOOD
        else:
            return PerformanceStatus.EXCELLENT
    
    async def _generate_alert(self, alert_type: str, value: float):
        """Gera alerta de performance"""
        self.monitoring_metrics['alerts_generated'] += 1
        
        alert = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.HIGH,
            content={
                'notification_type': 'performance_alert',
                'alert_type': alert_type,
                'value': value,
                'threshold': self.alert_thresholds.get(alert_type.replace('high_', '') + '_percent', 0),
                'timestamp': datetime.now().isoformat()
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(alert)
    
    def _analyze_trends(self) -> Dict[str, str]:
        """Analisa tendências de performance"""
        trends = {}
        
        for metric_type, history in self.metrics_history.items():
            if len(history) < 10:
                continue
            
            # Pegar últimos 10 valores
            recent_values = [m.value for m in list(history)[-10:]]
            
            # Calcular tendência simples
            if len(recent_values) >= 2:
                first_half = statistics.mean(recent_values[:5])
                second_half = statistics.mean(recent_values[5:])
                
                change = ((second_half - first_half) / first_half) * 100 if first_half > 0 else 0
                
                if change > 10:
                    trends[metric_type.value] = "increasing"
                elif change < -10:
                    trends[metric_type.value] = "decreasing"
                else:
                    trends[metric_type.value] = "stable"
        
        return trends
    
    def _detect_anomalies(self) -> List[Dict[str, Any]]:
        """Detecta anomalias nas métricas"""
        anomalies = []
        
        for metric_type, history in self.metrics_history.items():
            if len(history) < 20:
                continue
            
            values = [m.value for m in history]
            mean = statistics.mean(values)
            stdev = statistics.stdev(values) if len(values) > 1 else 0
            
            # Detectar outliers (valores além de 3 desvios padrão)
            for metric in list(history)[-5:]:  # Últimas 5 medições
                if abs(metric.value - mean) > 3 * stdev and stdev > 0:
                    anomalies.append({
                        'metric_type': metric_type.value,
                        'value': metric.value,
                        'expected_range': f"{mean - 2*stdev:.2f} - {mean + 2*stdev:.2f}",
                        'timestamp': metric.timestamp.isoformat()
                    })
        
        return anomalies
    
    async def _handle_anomalies(self, anomalies: List[Dict[str, Any]]):
        """Trata anomalias detectadas"""
        if not anomalies:
            return
        
        # Agrupar por tipo
        by_type = defaultdict(list)
        for anomaly in anomalies:
            by_type[anomaly['metric_type']].append(anomaly)
        
        # Notificar sobre anomalias críticas
        for metric_type, anomaly_list in by_type.items():
            if len(anomaly_list) >= 3:  # Múltiplas anomalias do mesmo tipo
                notification = AgentMessage(
                    id=str(uuid4()),
                    sender_id=self.agent_id,
                    recipient_id="code_analyzer_001",
                    message_type=MessageType.REQUEST,
                    priority=Priority.HIGH,
                    content={
                        'request_type': 'analyze_performance_issue',
                        'metric_type': metric_type,
                        'anomalies': anomaly_list,
                        'recommendation': 'Investigar causa de anomalias recorrentes'
                    },
                    timestamp=datetime.now()
                )
                await self.message_bus.publish(notification)
    
    async def _handle_correction_notification(self, notification_data: Dict[str, Any]):
        """Trata notificação de correção completada"""
        file_path = notification_data.get('file_path')
        corrections_applied = notification_data.get('corrections_applied', 0)
        
        logger.info(f"📊 Validando impacto de {corrections_applied} correções em {file_path}")
        
        # Agendar validação de performance
        await self.monitoring_queue.put({
            'type': 'validate_correction',
            'file_path': file_path,
            'delay': 5  # Aguardar 5 segundos antes de validar
        })
    
    async def _generate_performance_report(self, start_time: Optional[datetime] = None, 
                                         end_time: Optional[datetime] = None) -> PerformanceReport:
        """Gera relatório completo de performance"""
        if not start_time:
            start_time = datetime.now() - timedelta(hours=1)
        if not end_time:
            end_time = datetime.now()
        
        # Filtrar métricas no período
        period_metrics = []
        for metric_type, history in self.metrics_history.items():
            for metric in history:
                if start_time <= metric.timestamp <= end_time:
                    period_metrics.append(metric)
        
        # Calcular estatísticas
        avg_metrics = defaultdict(list)
        peak_metrics = {}
        
        for metric in period_metrics:
            avg_metrics[metric.metric_type].append(metric.value)
            
            if metric.metric_type not in peak_metrics or metric.value > peak_metrics[metric.metric_type]:
                peak_metrics[metric.metric_type] = metric.value
        
        # Calcular médias
        average_metrics = {
            k: statistics.mean(v) if v else 0
            for k, v in avg_metrics.items()
        }
        
        # Detectar gargalos
        bottlenecks = await self.detect_bottlenecks({'scope': 'system'})
        
        # Analisar tendências
        trends = self._analyze_trends()
        
        # Determinar saúde geral
        overall_health = self._determine_overall_health(average_metrics, bottlenecks['bottlenecks'])
        
        report = PerformanceReport(
            report_id=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            period_start=start_time,
            period_end=end_time,
            total_measurements=len(period_metrics),
            average_metrics=average_metrics,
            peak_metrics=peak_metrics,
            bottlenecks=bottlenecks['bottlenecks'],
            recommendations=self._generate_report_recommendations(average_metrics, bottlenecks['bottlenecks']),
            overall_health=overall_health,
            trends=trends
        )
        
        return report
    
    def _determine_overall_health(self, avg_metrics: Dict, bottlenecks: List) -> PerformanceStatus:
        """Determina saúde geral do sistema"""
        critical_bottlenecks = [b for b in bottlenecks if b.get('severity') == 'high']
        
        if critical_bottlenecks:
            return PerformanceStatus.CRITICAL
        
        # Verificar métricas médias
        issues = 0
        if MetricType.CPU_USAGE in avg_metrics and avg_metrics[MetricType.CPU_USAGE] > 70:
            issues += 1
        if MetricType.MEMORY_USAGE in avg_metrics and avg_metrics[MetricType.MEMORY_USAGE] > 500:
            issues += 1
        if MetricType.EXECUTION_TIME in avg_metrics and avg_metrics[MetricType.EXECUTION_TIME] > 2:
            issues += 1
        
        if issues >= 2:
            return PerformanceStatus.NEEDS_IMPROVEMENT
        elif issues == 1:
            return PerformanceStatus.ACCEPTABLE
        elif bottlenecks:
            return PerformanceStatus.GOOD
        else:
            return PerformanceStatus.EXCELLENT
    
    def _generate_report_recommendations(self, avg_metrics: Dict, bottlenecks: List) -> List[str]:
        """Gera recomendações para o relatório"""
        recommendations = []
        
        # Baseado em métricas médias
        if MetricType.CPU_USAGE in avg_metrics and avg_metrics[MetricType.CPU_USAGE] > 70:
            recommendations.append("CPU consistentemente alta - considere otimização de algoritmos ou paralelização")
        
        if MetricType.MEMORY_USAGE in avg_metrics and avg_metrics[MetricType.MEMORY_USAGE] > 500:
            recommendations.append("Uso elevado de memória - verifique vazamentos e otimize estruturas de dados")
        
        # Baseado em gargalos
        if len(bottlenecks) > 3:
            recommendations.append("Múltiplos gargalos detectados - considere revisão arquitetural")
        
        # Recomendação geral
        if not recommendations:
            recommendations.append("Sistema operando dentro dos parâmetros normais - continue monitorando")
        
        return recommendations[:5]  # Limitar a 5 recomendações
    
    async def _send_report(self, report: PerformanceReport):
        """Envia relatório de performance"""
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.MEDIUM,
            content={
                'notification_type': 'performance_report',
                'report': self._report_to_dict(report),
                'summary': {
                    'health': report.overall_health.value,
                    'bottlenecks': len(report.bottlenecks),
                    'period': f"{report.period_start.strftime('%H:%M')} - {report.period_end.strftime('%H:%M')}"
                }
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)
    
    async def _process_monitor_request(self, request: Dict[str, Any]):
        """Processa requisição de monitoramento da fila"""
        request_type = request.get('type')
        
        if request_type == 'continuous_monitor':
            monitor_data = request.get('monitor_data')
            # Implementar monitoramento contínuo
            
        elif request_type == 'validate_correction':
            file_path = request.get('file_path')
            delay = request.get('delay', 0)
            
            if delay > 0:
                await asyncio.sleep(delay)
            
            # Validar correção
            await self.validate_optimization({
                'file_path': file_path,
                'optimization_type': 'correction'
            })
    
    def _metrics_to_dict(self, metrics: List[PerformanceMetric]) -> List[Dict[str, Any]]:
        """Converte métricas para dicionário"""
        return [
            {
                'metric_id': m.metric_id,
                'type': m.metric_type.value,
                'value': m.value,
                'unit': m.unit,
                'timestamp': m.timestamp.isoformat()
            }
            for m in metrics
        ]
    
    def _comparison_to_dict(self, comparison: PerformanceComparison) -> Dict[str, Any]:
        """Converte comparação para dicionário"""
        return {
            'comparison_id': comparison.comparison_id,
            'improvements': comparison.improvements,
            'degradations': comparison.degradations,
            'overall_improvement': comparison.overall_improvement,
            'status': comparison.status
        }
    
    def _report_to_dict(self, report: PerformanceReport) -> Dict[str, Any]:
        """Converte relatório para dicionário"""
        return {
            'report_id': report.report_id,
            'period': f"{report.period_start.isoformat()} to {report.period_end.isoformat()}",
            'total_measurements': report.total_measurements,
            'average_metrics': {k.value: v for k, v in report.average_metrics.items()},
            'peak_metrics': {k.value: v for k, v in report.peak_metrics.items()},
            'bottlenecks': report.bottlenecks,
            'recommendations': report.recommendations,
            'overall_health': report.overall_health.value,
            'trends': report.trends
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

def create_performance_monitor_agent(message_bus, num_instances=1) -> List[PerformanceMonitorAgent]:
    """
    Cria agente de monitoramento de performance
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de monitoramento
    """
    agents = []
    
    try:
        logger.info("📊 Criando PerformanceMonitorAgent para autoevolução...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "performance_monitor_001"
        
        if agent_id not in existing_agents:
            try:
                agent = PerformanceMonitorAgent(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar serviços de monitoramento
                asyncio.create_task(agent.start_monitoring_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com monitoramento avançado")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de monitoramento criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando PerformanceMonitorAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
