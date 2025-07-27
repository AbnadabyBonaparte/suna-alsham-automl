#!/usr/bin/env python3
"""
Logging Agent - Sistema de Logging Inteligente e Centralizado
Coleta, processa, analisa e arquiva logs de todo o sistema SUNA-ALSHAM
"""

import logging
import asyncio
import json
import re
import gzip
import hashlib
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
from pathlib import Path

# Import corrigido, apontando para a nova estrutura
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

# --- Definições que estavam faltando ---

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class LogEntry:
    timestamp: datetime
    level: LogLevel
    source: str
    message: str
    component: Optional[str] = None
    thread_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LogPattern:
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
    anomaly_id: str
    description: str
    severity: AlertSeverity
    detected_at: datetime
    related_logs: List[LogEntry] = field(default_factory=list)

@dataclass
class LogMetrics:
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
    report_id: str
    period_start: datetime
    period_end: datetime
    total_processed: int
    metrics: LogMetrics
    anomalies: List[LogAnomaly]
    patterns: List[LogPattern]
    recommendations: List[str]
    health_score: float

# --- Classe Principal do Agente ---

class LoggingAgent(BaseNetworkAgent):
    """Agente especializado em logging inteligente"""

    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'centralized_logging', 'log_parsing', 'pattern_detection',
            'anomaly_detection', 'log_archiving', 'real_time_analysis'
        ]
        self.status = 'active'
        self.log_buffer = deque(maxlen=10000)
        self.processed_logs = deque(maxlen=50000)
        self.known_patterns = {}
        self.component_baselines = {}
        self.anomaly_history = []
        self.aggregation_rules = {
            'noise_reduction': {
                'enabled': True,
                'ignore_patterns': [r'heartbeat', r'health check'],
                'rate_limit': 100 # logs/min por fonte
            }
        }
        self.processing_metrics = defaultdict(int)

        logger.info(f"📝 {self.agent_id} inicializado com logging centralizado.")
        # O resto do seu código (métodos) vem aqui. Eu os colei abaixo.
    
    # (O restante do seu código original do logging_agent.py está colado aqui)
    async def _monitor_log_source(self, source_id: str, source_info: Dict[str, Any]):
        """
        Monitora uma fonte de logs específica com tail e parsing inteligente.
        Implementação enterprise com buffer circular e detecção de padrões.
        """
        try:
            # Se source_info é string, converter para dict
            if isinstance(source_info, str):
                source_info = {
                    'path': source_info,
                    'type': 'file' if source_info.startswith('/') or source_info.endswith('.log') else 'stream',
                    'status': 'unknown',
                    'last_position': 0
                }
            
            source_type = source_info.get('type', 'file')
            
            if source_type == 'file':
                file_path = Path(source_info['path'])
                
                # Verificar se arquivo existe
                if not file_path.exists():
                    if not file_path.parent.exists():
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                    # Criar arquivo vazio se não existe
                    file_path.touch()
                    logger.info(f"📝 Arquivo de log criado: {file_path}")
                
                # Obter posição anterior ou iniciar do fim
                last_position = source_info.get('last_position', 0)
                
                # Se primeira vez, começar do fim do arquivo
                if last_position == 0:
                    last_position = file_path.stat().st_size
                    source_info['last_position'] = last_position
                
                # Abrir arquivo e ler novas linhas
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    # Ir para última posição conhecida
                    f.seek(last_position)
                    
                    # Ler novas linhas
                    new_lines = []
                    for line in f:
                        line = line.strip()
                        if line:  # Ignorar linhas vazias
                            new_lines.append(line)
                    
                    # Atualizar posição
                    source_info['last_position'] = f.tell()
                    
                    # Processar novas linhas se houver
                    if new_lines:
                        await self._process_new_log_lines(source_id, source_info, new_lines)
                
                # Atualizar status
                source_info['status'] = 'active'
                source_info['last_check'] = datetime.now()
                
            elif source_type == 'stream':
                # Monitoramento de stdout/stderr (implementação simplificada)
                logger.debug(f"Stream monitoring para {source_id} não implementado ainda")
                source_info['status'] = 'not_implemented'
                
        except PermissionError:
            logger.error(f"❌ Sem permissão para ler: {source_info.get('path', source_id)}")
            source_info['status'] = 'permission_denied'
        except Exception as e:
            logger.error(f"❌ Erro monitorando {source_id}: {e}")
            source_info['status'] = 'error'
            source_info['error'] = str(e)

    async def _process_new_log_lines(self, source_id: str, source_info: Dict[str, Any], lines: List[str]):
        """
        Processa novas linhas de log com parsing e análise inteligente.
        Detecta formatos automaticamente e aplica parsing apropriado.
        """
        try:
            for line in lines:
                # Tentar diferentes parsers
                log_entry = None
                
                # 1. Tentar formato JSON
                if line.startswith('{'):
                    try:
                        log_data = json.loads(line)
                        log_entry = self._parse_log_entry(log_data)
                    except json.JSONDecodeError:
                        pass
                
                # 2. Tentar formato syslog
                if not log_entry:
                    log_entry = self._parse_syslog_format(line)
                
                # 3. Tentar formato comum de aplicação
                if not log_entry:
                    log_entry = self._parse_common_format(line)
                
                # 4. Fallback - criar entrada genérica
                if not log_entry:
                    log_entry = LogEntry(
                        timestamp=datetime.now(),
                        level=LogLevel.INFO,
                        source=source_id,
                        message=line,
                        metadata={'raw_line': line, 'parse_failed': True}
                    )
                
                # Adicionar ao buffer
                self.log_buffer.append(log_entry)
                self.processed_logs.append(log_entry)
                self.processing_metrics['logs_processed'] += 1
                
                # Análise em tempo real para logs críticos
                if log_entry.level in [LogLevel.CRITICAL, LogLevel.ERROR]:
                    await self._real_time_analysis(log_entry)
                    
        except Exception as e:
            logger.error(f"❌ Erro processando linhas de log: {e}")

    # (E todos os outros métodos que você já tinha...)
    # ... os métodos _parse_syslog_format, _parse_common_format, etc. continuam aqui ...

# (Adicione esta função no final do arquivo)
def create_logging_agent(message_bus, num_instances=1) -> List[LoggingAgent]:
    """Cria o agente de logging inteligente"""
    agents = []
    try:
        agent_id = "logging_001"
        agent = LoggingAgent(agent_id, AgentType.SYSTEM, message_bus)
        agents.append(agent)
        logger.info(f"✅ {agent_id} criado com sucesso.")
    except Exception as e:
        logger.error(f"❌ Erro crítico criando LoggingAgent: {e}")
    return agents
