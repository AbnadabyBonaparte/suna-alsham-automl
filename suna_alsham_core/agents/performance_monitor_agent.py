#!/usr/bin/env python3
"""
Módulo do Agente de Monitoramento de Performance - SUNA-ALSHAM

[Versão Final Limpa]
"""

import asyncio
import logging
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, List

import psutil

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    cpu_usage_percent: float
    memory_usage_percent: float
    memory_usage_mb: float
    active_agents: int
    message_queue_depth: int
    average_latency_ms: float
    timestamp: float = field(default_factory=time.time)

class PerformanceMonitorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.extend(["performance_monitoring", "metric_collection"])
        self.monitoring_interval_seconds = 60
        self.latency_tracker = deque(maxlen=100)
        self.process = psutil.Process()
        logger.info(f"📊 {self.agent_id} (Monitor de Performance) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            if request_type == "get_performance_metrics":
                metrics = self.collect_metrics()
                await self.publish_response(message, {"status": "completed", "metrics": metrics.__dict__})
            elif request_type == "start_continuous_monitoring":
                interval = message.content.get("interval", self.monitoring_interval_seconds)
                asyncio.create_task(self.run_continuous_monitoring(interval))
                await self.publish_response(message, {"status": "acknowledged"})

    def collect_metrics(self) -> PerformanceMetrics:
        try:
            with self.process.oneshot():
                cpu_usage = self.process.cpu_percent()
                memory_info = self.process.memory_info()
                memory_usage_mb = memory_info.rss / (1024 * 1024)

            total_memory_percent = psutil.virtual_memory().percent
            network_metrics = self.message_bus.get_metrics()
            active_agents = network_metrics.get("subscribed_agents", 0)
            queue_depths = network_metrics.get("queue_depths", {})
            total_queue_depth = sum(queue_depths.values())
            avg_latency = sum(self.latency_tracker) / len(self.latency_tracker) if self.latency_tracker else 0

            return PerformanceMetrics(
                cpu_usage_percent=cpu_usage,
                memory_usage_percent=total_memory_percent,
                memory_usage_mb=memory_usage_mb,
                active_agents=active_agents,
                message_queue_depth=total_queue_depth,
                average_latency_ms=avg_latency,
            )
        except Exception as e:
            logger.error(f"Erro ao coletar métricas: {e}", exc_info=True)
            return PerformanceMetrics(0, 0, 0, 0, 0, -1.0)

    async def run_continuous_monitoring(self, interval: int):
        logger.info(f"Monitoramento contínuo iniciado com intervalo de {interval} segundos.")
        while self.status == "active":
            metrics = self.collect_metrics()
            log_message = self.create_message(
                recipient_id="logging_001",
                message_type=MessageType.NOTIFICATION,
                content={"event_type": "performance_metrics", "metrics": metrics.__dict__}
            )
            await self.message_bus.publish(log_message)
            await asyncio.sleep(interval)

    """
    Função fábrica para criar e inicializar o(s) PerformanceMonitorAgent(s) do sistema ALSHAM QUANTUM.

    Esta função instancia o PerformanceMonitorAgent, registra todos os eventos relevantes para diagnóstico
    e retorna em uma lista para registro no agent registry. Lida com erros de forma robusta
    e garante que o agente esteja pronto para operação.

    Args:
        message_bus (Any): O barramento de mensagens ou canal de comunicação para mensagens entre agentes.

    Returns:
        List[BaseNetworkAgent]: Uma lista contendo a(s) instância(s) inicializada(s) de PerformanceMonitorAgent.
    """
    agents: List[BaseNetworkAgent] = []
    logger.info("📊 [Factory] Criando PerformanceMonitorAgent...")
    try:
        agent = PerformanceMonitorAgent("performance_monitor_001", message_bus)
        agents.append(agent)
        logger.info(f"📊 PerformanceMonitorAgent criado com sucesso: {agent.agent_id}")
    except Exception as e:
        logger.critical(f"❌ Erro crítico ao criar PerformanceMonitorAgent: {e}", exc_info=True)
    return agents
