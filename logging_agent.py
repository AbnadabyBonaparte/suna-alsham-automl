#!/usr/bin/env python3
"""
Logging Agent - Análise inteligente de logs e detecção de anomalias
Sistema avançado de monitoramento e agregação de logs
"""

import logging
import re
import os
import asyncio
import json
import gzip
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
from pathlib import Path
import statistics
import hashlib
from multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class LogLevel(Enum):
    """Níveis de log"""
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"

class AnomalyType(Enum):
    """Tipos de anomalias detectadas"""
    ERROR_SPIKE = "error_spike"
    UNUSUAL_PATTERN = "unusual_pattern"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    SECURITY_THREAT = "security_threat"
    SYSTEM_OVERLOAD = "system_overload"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    COMMUNICATION_FAILURE = "communication_failure"
    DATA_CORRUPTION = "data_corruption"

class AlertSeverity(Enum):
    """Severidade de alertas"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class LogEntry:
    """Entrada de log processada"""
    timestamp: datetime
    level: LogLevel
    source: str
    message: str
    component: Optional[str] = None
    thread_id: Optional[str] = None
    user_id: Optional[str] = None
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    processed_at: datetime = field(default_factory=datetime.now)

@dataclass
class LogPattern:
    """Padrão de log identificado"""
    pattern_id: str
    pattern_type: str
    regex: str
    frequency: int
    last_seen: datetime
    severity: AlertSeverity
    description: str
    examples: List[str] = field(default_factory=list)

@dataclass
class LogAnomaly:
    """Anomalia detectada nos logs"""
    anomaly_id: str
    anomaly_type: AnomalyType
    severity: AlertSeverity
    description: str
    affected_components: List[str]
    time_window: Tuple[datetime, datetime]
    evidence: List[LogEntry]
    confidence: float
    recommended_actions: List[str]
    detected_at: datetime = field(default_factory=datetime.now)

@dataclass
class LogMetrics:
    """Métricas de logs"""
    total_entries: int
    entries_by_level: Dict[LogLevel, int]
    error_rate: float
    warning_rate: float
    top_sources: List[Tuple[str, int]]
    top_messages: List[Tuple[str, int]]
    time_range: Tuple[datetime, datetime]
    anomalies_detected: int

@dataclass
class LogReport:
    """Relatório de análise de logs"""
    report_id: str
    period_start: datetime
    period_end: datetime
    total_processed: int
    metrics: LogMetrics
    anomalies: List[LogAnomaly]
    patterns: List[LogPattern]
    recommendations: List[str]
    health_score: float
    generated_at: datetime = field(default_factory=datetime.now)

class LoggingAgent(BaseNetworkAgent):
    """Agente especializado em análise inteligente de logs"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'log_analysis',
            'anomaly_detection',
            'pattern_recognition',
            'log_aggregation',
            'intelligent_filtering',
            'real_time_monitoring',
            'predictive_alerting',
            'log_correlation',
            'security_analysis',
            'performance_tracking'
        ]
        self.status = 'active'
        
        # Estado do agente
        self.log_buffer = deque(maxlen=10000)  # Buffer circular
        self.processed_logs = deque(maxlen=50000)  # Histórico processado
        self.known_patterns = {}  # pattern_id -> LogPattern
        self.anomaly_history = deque(maxlen=1000)  # Histórico de anomalias
        self.component_baselines = {}  # Baselines por componente
        
        # Configurações
        self.log_sources = [
            "/var/log/syslog",
            "/var/log/application.log",
            "./logs/",
            "stdout",
            "stderr"
        ]
        self.anomaly_thresholds = {
            'error_rate_threshold': 0.05,  # 5% de erros
            'spike_multiplier': 3.0,  # 3x acima da média
            'time_window_minutes': 15,
            'min_samples': 10
        }
        
        # Padrões de segurança
        self.security_patterns = self._load_security_patterns()
        
        # Padrões de performance
        self.performance_patterns = self._load_performance_patterns()
        
        # Agregação inteligente
        self.aggregation_rules = self._setup_aggregation_rules()
        
        # Métricas
        self.processing_metrics = {
            'logs_processed': 0,
            'anomalies_detected': 0,
            'patterns_identified': 0,
            'alerts_generated': 0,
            'false_positives': 0,
            'processing_rate': 0.0
        }
        
        # Tasks de background
        self._monitoring_task = None
        self._analysis_task = None
        self._cleanup_task = None
        self._aggregation_task = None
        
        logger.info(f"📝 {self.agent_id} inicializado com análise avançada de logs")
    
    def _load_security_patterns(self) -> List[Dict[str, Any]]:
        """Carrega padrões de segurança para detecção"""
        return [
            {
                'name': 'brute_force_attempt',
                'pattern': re.compile(r'Failed login.*attempts.*IP:\s*(\d+\.\d+\.\d+\.\d+)'),
                'severity': AlertSeverity.HIGH,
                'description': 'Tentativa de força bruta detectada',
                'threshold': 5,  # 5 tentativas em 10 minutos
                'time_window': 600
            },
            {
                'name': 'privilege_escalation',
                'pattern': re.compile(r'sudo.*COMMAND|su\s+root|chmod\s+777'),
                'severity': AlertSeverity.CRITICAL,
                'description': 'Possível escalação de privilégios',
                'threshold': 1,
                'time_window': 300
            },
            {
                'name': 'suspicious_file_access',
                'pattern': re.compile(r'access.*(/etc/passwd|/etc/shadow|\.ssh/|\.aws/)'),
                'severity': AlertSeverity.HIGH,
                'description': 'Acesso suspeito a arquivos sensíveis',
                'threshold': 1,
                'time_window': 300
            },
            {
                'name': 'sql_injection_attempt',
                'pattern': re.compile(r"(UNION|SELECT|INSERT|DELETE|DROP).*('|\")", re.IGNORECASE),
                'severity': AlertSeverity.CRITICAL,
                'description': 'Possível tentativa de SQL injection',
                'threshold': 1,
                'time_window': 60
            },
            {
                'name': 'port_scan',
                'pattern': re.compile(r'Connection.*refused.*port\s+(\d+)'),
                'severity': AlertSeverity.MEDIUM,
                'description': 'Possível port scan detectado',
                'threshold': 10,
                'time_window': 300
            }
        ]
    
    def _load_performance_patterns(self) -> List[Dict[str, Any]]:
        """Carrega padrões de performance para detecção"""
        return [
            {
                'name': 'high_response_time',
                'pattern': re.compile(r'response_time[:\s]*(\d+(?:\.\d+)?).*ms'),
                'severity': AlertSeverity.MEDIUM,
                'description': 'Tempo de resposta elevado',
                'threshold_value': 5000,  # 5 segundos
                'extract_value': True
            },
            {
                'name': 'memory_pressure',
                'pattern': re.compile(r'(OutOfMemory|Memory.*exhausted|GC.*pressure)'),
                'severity': AlertSeverity.HIGH,
                'description': 'Pressão de memória detectada',
                'threshold': 3,
                'time_window': 600
            },
            {
                'name': 'cpu_spike',
                'pattern': re.compile(r'CPU.*usage[:\s]*(\d+(?:\.\d+)?)%'),
                'severity': AlertSeverity.MEDIUM,
                'description': 'Pico de CPU detectado',
                'threshold_value': 90,
                'extract_value': True
            },
            {
                'name': 'disk_full',
                'pattern': re.compile(r'(disk.*full|No space left|filesystem.*full)', re.IGNORECASE),
                'severity': AlertSeverity.CRITICAL,
                'description': 'Disco cheio detectado',
                'threshold': 1,
                'time_window': 300
            },
            {
                'name': 'connection_timeout',
                'pattern': re.compile(r'(Connection.*timeout|Read.*timeout|Socket.*timeout)'),
                'severity': AlertSeverity.MEDIUM,
                'description': 'Timeouts de conexão frequentes',
                'threshold': 5,
                'time_window': 300
            }
        ]
    
    def _setup_aggregation_rules(self) -> Dict[str, Any]:
        """Configura regras de agregação inteligente"""
        return {
            'duplicate_detection': {
                'enabled': True,
                'time_window': 60,  # segundos
                'similarity_threshold': 0.9
            },
            'noise_reduction': {
                'enabled': True,
                'ignore_patterns': [
                    r'DEBUG.*routine.*check',
                    r'INFO.*heartbeat',
                    r'TRACE.*',
                    r'.*health.*check.*ok'
                ],
                'rate_limit': {
                    'max_per_minute': 100,
                    'burst_threshold': 500
                }
            },
            'intelligent_grouping': {
                'enabled': True,
                'group_by': ['source', 'level', 'message_pattern'],
                'min_group_size': 3,
                'time_window': 300
            }
        }
    
    async def start_logging_service(self):
        """Inicia serviços de logging"""
        if not self._monitoring_task:
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            self._analysis_task = asyncio.create_task(self._analysis_loop())
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
            self._aggregation_task = asyncio.create_task(self._aggregation_loop())
            logger.info(f"📝 {self.agent_id} iniciou serviços de logging")
    
    async def stop_logging_service(self):
        """Para serviços de logging"""
        tasks = [self._monitoring_task, self._analysis_task, self._cleanup_task, self._aggregation_task]
        for task in tasks:
            if task:
                task.cancel()
        
        self._monitoring_task = None
        self._analysis_task = None
        self._cleanup_task = None
        self._aggregation_task = None
        
        logger.info(f"🛑 {self.agent_id} parou serviços de logging")
    
    async def _monitoring_loop(self):
        """Loop principal de monitoramento de logs"""
        while True:
            try:
                # Monitorar fontes de log
                for source in self.log_sources:
                    await self._monitor_log_source(source)
                
                # Processar buffer de logs
                await self._process_log_buffer()
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de monitoramento: {e}")
    
    async def _analysis_loop(self):
        """Loop de análise de logs"""
        while True:
            try:
                # Detectar anomalias
                anomalies = await self._detect_anomalies()
                
                if anomalies:
                    await self._handle_anomalies(anomalies)
                
                # Identificar novos padrões
                new_patterns = await self._identify_patterns()
                
                if new_patterns:
                    await self._update_patterns(new_patterns)
                
                # Gerar relatórios periódicos
                if len(self.processed_logs) >= 1000:
                    await self._generate_periodic_report()
                
                await asyncio.sleep(30)  # Análise a cada 30 segundos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de análise: {e}")
    
    async def _aggregation_loop(self):
        """Loop de agregação inteligente"""
        while True:
            try:
                # Aplicar regras de agregação
                await self._apply_aggregation_rules()
                
                # Reduzir ruído
                await self._noise_reduction()
                
                # Agrupar logs similares
                await self._intelligent_grouping()
                
                await asyncio.sleep(60)  # Agregação a cada minuto
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na agregação: {e}")
    
    async def _cleanup_loop(self):
        """Loop de limpeza de dados antigos"""
        while True:
            try:
                # Limpar logs antigos
                cutoff_time = datetime.now() - timedelta(hours=24)
                
                # Manter apenas logs das últimas 24 horas no buffer principal
                self.processed_logs = deque([
                    log for log in self.processed_logs 
                    if log.timestamp > cutoff_time
                ], maxlen=50000)
                
                # Comprimir e arquivar logs antigos
                await self._archive_old_logs()
                
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
            
            if request_type == 'analyze_logs':
                result = await self.analyze_logs(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'detect_anomalies':
                result = await self.detect_anomalies_request(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'search_logs':
                result = await self.search_logs(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'get_log_report':
                result = await self.get_log_report(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'monitor_component':
                result = await self.monitor_component(message.content)
                await self._send_response(message, result)
        
        elif message.message_type == MessageType.NOTIFICATION:
            # Processar notificações de outros agentes
            await self._process_notification(message.content)
    
    async def ingest_log(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ingere e processa um log"""
        try:
            # Parsear log
            log_entry = self._parse_log_entry(log_data)
            
            if log_entry:
                # Adicionar ao buffer
                self.log_buffer.append(log_entry)
                self.processing_metrics['logs_processed'] += 1
                
                # Análise em tempo real para logs críticos
                if log_entry.level in [LogLevel.CRITICAL, LogLevel.ERROR]:
                    await self._real_time_analysis(log_entry)
                
                return {
                    'status': 'ingested',
                    'log_id': f"{log_entry.timestamp.isoformat()}_{log_entry.source}",
                    'level': log_entry.level.value,
                    'processed_at': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'rejected',
                    'reason': 'Invalid log format'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro ingerindo log: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _parse_log_entry(self, log_data: Dict[str, Any]) -> Optional[LogEntry]:
        """Parseia entrada de log raw"""
        try:
            # Extrair timestamp
            timestamp_str = log_data.get('timestamp', log_data.get('time'))
            if timestamp_str:
                if isinstance(timestamp_str, str):
                    # Tentar vários formatos
                    formats = [
                        '%Y-%m-%d %H:%M:%S,%f',
                        '%Y-%m-%d %H:%M:%S.%f',
                        '%Y-%m-%dT%H:%M:%S.%fZ',
                        '%Y-%m-%d %H:%M:%S'
                    ]
                    timestamp = None
                    for fmt in formats:
                        try:
                            timestamp = datetime.strptime(timestamp_str, fmt)
                            break
                        except ValueError:
                            continue
                    
                    if not timestamp:
                        timestamp = datetime.now()
                else:
                    timestamp = timestamp_str
            else:
                timestamp = datetime.now()
            
            # Extrair nível
            level_str = log_data.get('level', log_data.get('severity', 'INFO')).upper()
            try:
                level = LogLevel(level_str)
            except ValueError:
                # Mapear níveis não padrão
                level_mapping = {
                    'FATAL': LogLevel.CRITICAL,
                    'ERR': LogLevel.ERROR,
                    'WARN': LogLevel.WARNING,
                    'NOTICE': LogLevel.INFO,
                    'TRACE': LogLevel.DEBUG
                }
                level = level_mapping.get(level_str, LogLevel.INFO)
            
            # Extrair fonte
            source = log_data.get('source', log_data.get('logger', log_data.get('component', 'unknown')))
            
            # Extrair mensagem
            message = log_data.get('message', log_data.get('msg', str(log_data)))
            
            # Metadata adicional
            metadata = {
                'raw_data': log_data,
                'parser_version': '1.0'
            }
            
            return LogEntry(
                timestamp=timestamp,
                level=level,
                source=source,
                message=message,
                component=log_data.get('component'),
                thread_id=log_data.get('thread_id'),
                user_id=log_data.get('user_id'),
                trace_id=log_data.get('trace_id'),
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"❌ Erro parseando log: {e}")
            return None
    
    async def _real_time_analysis(self, log_entry: LogEntry):
        """Análise em tempo real para logs críticos"""
        try:
            # Verificar padrões de segurança
            for security_pattern in self.security_patterns:
                if security_pattern['pattern'].search(log_entry.message):
                    await self._handle_security_alert(log_entry, security_pattern)
            
            # Verificar padrões de performance
            for perf_pattern in self.performance_patterns:
                if perf_pattern['pattern'].search(log_entry.message):
                    await self._handle_performance_alert(log_entry, perf_pattern)
            
            # Detectar cascata de erros
            if log_entry.level == LogLevel.ERROR:
                await self._check_error_cascade(log_entry)
                
        except Exception as e:
            logger.error(f"❌ Erro na análise em tempo real: {e}")
    
    async def _handle_security_alert(self, log_entry: LogEntry, pattern: Dict[str, Any]):
        """Trata alertas de segurança"""
        alert = {
            'alert_type': 'security',
            'pattern_name': pattern['name'],
            'severity': pattern['severity'].value,
            'description': pattern['description'],
            'log_entry': self._log_entry_to_dict(log_entry),
            'timestamp': datetime.now().isoformat(),
            'recommended_actions': [
                'Investigar atividade suspeita',
                'Verificar logs relacionados',
                'Considerar bloqueio de IP se aplicável'
            ]
        }
        
        # Notificar sistema de segurança
        await self._send_security_alert(alert)
    
    async def _handle_performance_alert(self, log_entry: LogEntry, pattern: Dict[str, Any]):
        """Trata alertas de performance"""
        alert = {
            'alert_type': 'performance',
            'pattern_name': pattern['name'],
            'severity': pattern['severity'].value,
            'description': pattern['description'],
            'log_entry': self._log_entry_to_dict(log_entry),
            'timestamp': datetime.now().isoformat(),
            'recommended_actions': [
                'Monitorar recursos do sistema',
                'Verificar gargalos',
                'Considerar escalonamento'
            ]
        }
        
        # Notificar sistema de monitoramento
        await self._send_performance_alert(alert)
    
    async def _check_error_cascade(self, log_entry: LogEntry):
        """Verifica se há cascata de erros"""
        # Contar erros recentes do mesmo componente
        recent_errors = [
            log for log in list(self.log_buffer)[-100:]  # Últimos 100 logs
            if log.level == LogLevel.ERROR 
            and log.source == log_entry.source
            and (datetime.now() - log.timestamp).total_seconds() < 300  # 5 minutos
        ]
        
        if len(recent_errors) >= 5:  # 5 erros em 5 minutos
            cascade_alert = {
                'alert_type': 'error_cascade',
                'component': log_entry.source,
                'error_count': len(recent_errors),
                'time_window': '5_minutes',
                'severity': 'high',
                'first_error': recent_errors[0].timestamp.isoformat(),
                'latest_error': log_entry.timestamp.isoformat()
            }
            
            await self._send_cascade_alert(cascade_alert)
    
    async def _detect_anomalies(self) -> List[LogAnomaly]:
        """Detecta anomalias nos logs"""
        anomalies = []
        
        try:
            # Análise de volume de logs
            volume_anomalies = await self._detect_volume_anomalies()
            anomalies.extend(volume_anomalies)
            
            # Análise de taxa de erro
            error_anomalies = await self._detect_error_rate_anomalies()
            anomalies.extend(error_anomalies)
            
            # Análise de padrões incomuns
            pattern_anomalies = await self._detect_pattern_anomalies()
            anomalies.extend(pattern_anomalies)
            
            # Análise de componentes silenciosos
            silence_anomalies = await self._detect_silence_anomalies()
            anomalies.extend(silence_anomalies)
            
            self.processing_metrics['anomalies_detected'] += len(anomalies)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"❌ Erro detectando anomalias: {e}")
            return []
    
    async def _detect_volume_anomalies(self) -> List[LogAnomaly]:
        """Detecta anomalias de volume de logs"""
        anomalies = []
        
        # Analisar logs da última hora
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_logs = [log for log in self.processed_logs if log.timestamp > one_hour_ago]
        
        if len(recent_logs) < 10:  # Muito poucos logs para análise
            return anomalies
        
        # Agrupar por fonte
        logs_by_source = defaultdict(list)
        for log in recent_logs:
            logs_by_source[log.source].append(log)
        
        # Analisar cada fonte
        for source, logs in logs_by_source.items():
            if source not in self.component_baselines:
                # Criar baseline
                self.component_baselines[source] = {
                    'normal_volume_per_hour': len(logs),
                    'normal_error_rate': sum(1 for log in logs if log.level == LogLevel.ERROR) / len(logs),
                    'last_updated': datetime.now()
                }
                continue
            
            baseline = self.component_baselines[source]
            current_volume = len(logs)
            baseline_volume = baseline['normal_volume_per_hour']
            
            # Detectar picos de volume
            if current_volume > baseline_volume * self.anomaly_thresholds['spike_multiplier']:
                anomaly = LogAnomaly(
                    anomaly_id=f"vol_spike_{source}_{datetime.now().timestamp()}",
                    anomaly_type=AnomalyType.SYSTEM_OVERLOAD,
                    severity=AlertSeverity.HIGH,
                    description=f"Pico de volume em {source}: {current_volume} vs baseline {baseline_volume}",
                    affected_components=[source],
                    time_window=(one_hour_ago, datetime.now()),
                    evidence=logs[-10:],  # Últimos 10 logs como evidência
                    confidence=0.85,
                    recommended_actions=[
                        "Investigar causa do aumento de logs",
                        "Verificar performance do sistema",
                        "Considerar ajustar rate limiting"
                    ]
                )
                anomalies.append(anomaly)
        
        return anomalies
    
    async def _detect_error_rate_anomalies(self) -> List[LogAnomaly]:
        """Detecta anomalias na taxa de erro"""
        anomalies = []
        
        # Analisar últimos 30 minutos
        window_start = datetime.now() - timedelta(minutes=30)
        recent_logs = [log for log in self.processed_logs if log.timestamp > window_start]
        
        if len(recent_logs) < self.anomaly_thresholds['min_samples']:
            return anomalies
        
        # Calcular taxa de erro atual
        error_logs = [log for log in recent_logs if log.level == LogLevel.ERROR]
        current_error_rate = len(error_logs) / len(recent_logs)
        
        # Comparar com threshold
        if current_error_rate > self.anomaly_thresholds['error_rate_threshold']:
            anomaly = LogAnomaly(
                anomaly_id=f"error_rate_{datetime.now().timestamp()}",
                anomaly_type=AnomalyType.ERROR_SPIKE,
                severity=AlertSeverity.CRITICAL if current_error_rate > 0.15 else AlertSeverity.HIGH,
                description=f"Taxa de erro elevada: {current_error_rate:.2%} (threshold: {self.anomaly_thresholds['error_rate_threshold']:.2%})",
                affected_components=list(set(log.source for log in error_logs)),
                time_window=(window_start, datetime.now()),
                evidence=error_logs[-20:],  # Últimos 20 erros como evidência
                confidence=0.90,
                recommended_actions=[
                    "Investigar causa dos erros",
                    "Verificar logs de aplicação",
                    "Considerar rollback se necessário"
                ]
            )
            anomalies.append(anomaly)
        
        return anomalies
    
    async def _detect_pattern_anomalies(self) -> List[LogAnomaly]:
        """Detecta padrões incomuns nos logs"""
        anomalies = []
        
        # Analisar mensagens únicas na última hora
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_logs = [log for log in self.processed_logs if log.timestamp > one_hour_ago]
        
        # Extrair padrões de mensagem
        message_patterns = defaultdict(int)
        for log in recent_logs:
            # Normalizar mensagem (remover números, IDs, etc.)
            normalized = re.sub(r'\d+', 'N', log.message)
            normalized = re.sub(r'[a-f0-9]{8,}', 'ID', normalized)  # Remover UUIDs/hashes
            message_patterns[normalized] += 1
        
        # Identificar padrões incomuns (que aparecem apenas uma vez)
        unusual_patterns = [
            pattern for pattern, count in message_patterns.items()
            if count == 1 and len(pattern) > 50  # Mensagens longas e únicas
        ]
        
        if len(unusual_patterns) > 10:  # Muitos padrões únicos podem indicar problema
            # Encontrar logs originais
            evidence_logs = []
            for log in recent_logs:
                normalized = re.sub(r'\d+', 'N', log.message)
                normalized = re.sub(r'[a-f0-9]{8,}', 'ID', normalized)
                if normalized in unusual_patterns[:5]:  # Top 5 padrões únicos
                    evidence_logs.append(log)
            
            anomaly = LogAnomaly(
                anomaly_id=f"unusual_patterns_{datetime.now().timestamp()}",
                anomaly_type=AnomalyType.UNUSUAL_PATTERN,
                severity=AlertSeverity.MEDIUM,
                description=f"{len(unusual_patterns)} padrões incomuns detectados",
                affected_components=list(set(log.source for log in evidence_logs)),
                time_window=(one_hour_ago, datetime.now()),
                evidence=evidence_logs,
                confidence=0.70,
                recommended_actions=[
                    "Analisar padrões incomuns",
                    "Verificar se há novos tipos de erro",
                    "Considerar atualizar filtros de log"
                ]
            )
            anomalies.append(anomaly)
        
        return anomalies
    
    async def _detect_silence_anomalies(self) -> List[LogAnomaly]:
        """Detecta componentes que pararam de gerar logs"""
        anomalies = []
        
        # Verificar componentes que deveriam estar logando
        now = datetime.now()
        silence_threshold = timedelta(minutes=30)
        
        # Obter componentes ativos nas últimas 24 horas
        day_ago = now - timedelta(hours=24)
        recent_sources = set()
        for log in self.processed_logs:
            if log.timestamp > day_ago:
                recent_sources.add(log.source)
        
        # Verificar cada fonte
        for source in recent_sources:
            # Encontrar último log desta fonte
            source_logs = [log for log in reversed(self.processed_logs) if log.source == source]
            
            if source_logs:
                last_log_time = source_logs[0].timestamp
                silence_duration = now - last_log_time
                
                if silence_duration > silence_threshold:
                    anomaly = LogAnomaly(
                        anomaly_id=f"silence_{source}_{now.timestamp()}",
                        anomaly_type=AnomalyType.COMMUNICATION_FAILURE,
                        severity=AlertSeverity.HIGH if silence_duration > timedelta(hours=1) else AlertSeverity.MEDIUM,
                        description=f"Componente {source} silencioso há {silence_duration}",
                        affected_components=[source],
                        time_window=(last_log_time, now),
                        evidence=[source_logs[0]] if source_logs else [],
                        confidence=0.80,
                        recommended_actions=[
                            f"Verificar status do componente {source}",
                            "Investigar possível falha de comunicação",
                            "Considerar restart se necessário"
                        ]
                    )
                    anomalies.append(anomaly)
        
        return anomalies
    
    async def _handle_anomalies(self, anomalies: List[LogAnomaly]):
        """Trata anomalias detectadas"""
        for anomaly in anomalies:
            # Adicionar ao histórico
            self.anomaly_history.append(anomaly)
            
            # Notificar baseado na severidade
            if anomaly.severity in [AlertSeverity.CRITICAL, AlertSeverity.HIGH]:
                await self._send_critical_anomaly_alert(anomaly)
            else:
                await self._send_anomaly_notification(anomaly)
    
    async def _send_critical_anomaly_alert(self, anomaly: LogAnomaly):
        """Envia alerta crítico de anomalia"""
        alert = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.CRITICAL,
            content={
                'notification_type': 'critical_log_anomaly',
                'anomaly': self._anomaly_to_dict(anomaly),
                'immediate_action_required': True
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(alert)
    
    async def _send_anomaly_notification(self, anomaly: LogAnomaly):
        """Envia notificação de anomalia"""
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="performance_monitor_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.MEDIUM,
            content={
                'notification_type': 'log_anomaly_detected',
                'anomaly': self._anomaly_to_dict(anomaly)
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)
    
    async def search_logs(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Busca logs baseado em critérios"""
        try:
            query = request_data.get('query', '')
            level = request_data.get('level')
            source = request_data.get('source')
            time_range = request_data.get('time_range', {})
            limit = request_data.get('limit', 100)
            
            # Filtrar logs
            filtered_logs = []
            
            for log in self.processed_logs:
                # Filtro de tempo
                if time_range:
                    start_time = datetime.fromisoformat(time_range.get('start', '1970-01-01'))
                    end_time = datetime.fromisoformat(time_range.get('end', '2099-12-31'))
                    if not (start_time <= log.timestamp <= end_time):
                        continue
                
                # Filtro de nível
                if level and log.level.value != level.upper():
                    continue
                
                # Filtro de fonte
                if source and log.source != source:
                    continue
                
                # Filtro de query
                if query and query.lower() not in log.message.lower():
                    continue
                
                filtered_logs.append(log)
                
                if len(filtered_logs) >= limit:
                    break
            
            return {
                'status': 'completed',
                'total_found': len(filtered_logs),
                'logs': [self._log_entry_to_dict(log) for log in filtered_logs],
                'query_info': {
                    'query': query,
                    'level': level,
                    'source': source,
                    'time_range': time_range,
                    'limit': limit
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erro buscando logs: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _log_entry_to_dict(self, log_entry: LogEntry) -> Dict[str, Any]:
        """Converte LogEntry para dicionário"""
        return {
            'timestamp': log_entry.timestamp.isoformat(),
            'level': log_entry.level.value,
            'source': log_entry.source,
            'message': log_entry.message,
            'component': log_entry.component,
            'thread_id': log_entry.thread_id,
            'user_id': log_entry.user_id,
            'trace_id': log_entry.trace_id
        }
    
    def _anomaly_to_dict(self, anomaly: LogAnomaly) -> Dict[str, Any]:
        """Converte LogAnomaly para dicionário"""
        return {
            'anomaly_id': anomaly.anomaly_id,
            'type': anomaly.anomaly_type.value,
            'severity': anomaly.severity.value,
            'description': anomaly.description,
            'affected_components': anomaly.affected_components,
            'time_window': [
                anomaly.time_window[0].isoformat(),
                anomaly.time_window[1].isoformat()
            ],
            'confidence': anomaly.confidence,
            'recommended_actions': anomaly.recommended_actions,
            'detected_at': anomaly.detected_at.isoformat()
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

def create_logging_agent(message_bus, num_instances=1) -> List[LoggingAgent]:
    """
    Cria agente de análise inteligente de logs
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de logging
    """
    agents = []
    
    try:
        logger.info("📝 Criando LoggingAgent para análise inteligente...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "logging_agent_001"
        
        if agent_id not in existing_agents:
            try:
                agent = LoggingAgent(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar serviços de logging
                asyncio.create_task(agent.start_logging_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com análise inteligente de logs")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de logging criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando LoggingAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
