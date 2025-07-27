#!/usr/bin/env python3
"""
Módulo do Performance Monitor Agent - SUNA-ALSHAM

Define o agente especializado em monitoramento e validação de performance,
capaz de detectar gargalos, rastrear recursos e validar otimizações.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

import psutil

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class PerformanceStatus(Enum):
    """Status de performance de um componente."""
    EXCELLENT = "excellent"
    GOOD = "good"
    DEGRADED = "degraded"
    CRITICAL = "critical"


@dataclass
class PerformanceSnapshot:
    """Representa um snapshot de performance do sistema em um dado momento."""
    snapshot_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    overall_status: PerformanceStatus = PerformanceStatus.GOOD
    cpu_percent: float = 0.0
    memory_mb: float = 0.0


# --- Classe Principal do Agente ---

class PerformanceMonitorAgent(BaseNetworkAgent):
    """
    Agente especializado em monitorar a performance do sistema, detectar
    gargalos e validar o impacto de otimizações de código.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o PerformanceMonitorAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "performance_monitoring",
            "optimization_validation",
            "bottleneck_detection",
            "resource_tracking",
            "profiling",
        ])
        
        self.snapshots = deque(maxlen=100) # Mantém os últimos 100 snapshots
        self.alert_thresholds = {"cpu_percent": 85.0, "memory_mb": 1024.0} # Limite de 1GB de RAM

        self._monitoring_task = None
        logger.info(f"📊 {self.agent_id} (Monitor de Performance) inicializado.")

    async def start_monitoring_service(self):
        """Inicia os serviços de background do agente."""
        if not self._monitoring_task:
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            logger.info(f"📊 {self.agent_id} iniciou serviço de monitoramento.")

    async def _monitoring_loop(self):
        """Loop principal que coleta métricas de performance periodicamente."""
        while True:
            try:
                await self._collect_system_metrics()
                await asyncio.sleep(30) # Coleta a cada 30 segundos
            except asyncio.CancelledError:
                logger.info(f"Loop de monitoramento do {self.agent_id} cancelado.")
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de monitoramento: {e}", exc_info=True)

    async def handle_message(self, message: AgentMessage):
        """Processa requisições de monitoramento e validação."""
        await super().handle_message(message)
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            if request_type == "get_performance_report":
                result = self.get_performance_report()
                await self.message_bus.publish(self.create_response(message, result))
            else:
                logger.warning(f"Ação de performance desconhecida: {request_type}")
    
    async def _collect_system_metrics(self):
        """Coleta métricas gerais do sistema e cria um snapshot."""
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            mem_mb = mem.used / (1024 * 1024)

            status = self._determine_system_status(cpu, mem_mb)
            
            snapshot = PerformanceSnapshot(
                snapshot_id=f"snap_{int(time.time())}",
                overall_status=status,
                cpu_percent=cpu,
                memory_mb=mem_mb,
            )
            self.snapshots.append(snapshot)

            # Gera alerta se o status for crítico
            if status == PerformanceStatus.CRITICAL:
                await self._generate_performance_alert(snapshot)

        except Exception as e:
            logger.error(f"❌ Erro ao coletar métricas do sistema: {e}", exc_info=True)

    def _determine_system_status(self, cpu: float, memory_mb: float) -> PerformanceStatus:
        """Determina o status geral de performance com base nas métricas."""
        if cpu > self.alert_thresholds["cpu_percent"] or memory_mb > self.alert_thresholds["memory_mb"]:
            return PerformanceStatus.CRITICAL
        elif cpu > 70 or memory_mb > (self.alert_thresholds["memory_mb"] * 0.75):
            return PerformanceStatus.DEGRADED
        else:
            return PerformanceStatus.GOOD

    async def _generate_performance_alert(self, snapshot: PerformanceSnapshot):
        """Envia um alerta de performance para o orquestrador."""
        logger.critical(f"🚨 ALERTA DE PERFORMANCE CRÍTICA! CPU: {snapshot.cpu_percent}%, Memória: {snapshot.memory_mb:.2f} MB")
        
        alert_content = {
            "notification_type": "performance_alert",
            "severity": "critical",
            "details": {
                "cpu_percent": snapshot.cpu_percent,
                "memory_mb": snapshot.memory_mb,
                "status": snapshot.overall_status.value,
            }
        }
        alert = self.create_message(
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.CRITICAL,
            content=alert_content,
        )
        await self.message_bus.publish(alert)

    def get_performance_report(self) -> Dict[str, Any]:
        """Gera um relatório com o snapshot de performance mais recente."""
        if not self.snapshots:
            return {"status": "no_data", "message": "Nenhuma métrica coletada ainda."}

        latest_snapshot = self.snapshots[-1]
        
        return {
            "status": "completed",
            "report_generated_at": datetime.now().isoformat(),
            "latest_snapshot": {
                "timestamp": latest_snapshot.timestamp.isoformat(),
                "overall_status": latest_snapshot.overall_status.value,
                "cpu_percent": latest_snapshot.cpu_percent,
                "memory_mb": round(latest_snapshot.memory_mb, 2),
            }
        }


def create_performance_monitor_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Monitoramento de Performance."""
    agents = []
    logger.info("📊 Criando PerformanceMonitorAgent...")
    try:
        agent = PerformanceMonitorAgent("performance_monitor_001", message_bus)
        asyncio.create_task(agent.start_monitoring_service())
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando PerformanceMonitorAgent: {e}", exc_info=True)
    return agents
