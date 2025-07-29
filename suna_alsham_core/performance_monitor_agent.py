#!/usr/bin/env python3
"""
Módulo do Agente de Monitoramento de Performance - SUNA-ALSHAM

[Fase 2] - Fortalecido com lógica real de coleta e cálculo de métricas,
incluindo uso de CPU, memória e latência de mensagens.
"""

import asyncio
import logging
import time
from collections import deque # <-- LINHA ADICIONADA AQUI
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import psutil

# Importa a classe base e os tipos essenciais do núcleo do sistema
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Dataclasses para Tipagem Forte ---

@dataclass
class PerformanceMetrics:
    """Estrutura para armazenar as métricas de performance coletadas."""
    cpu_usage_percent: float
    memory_usage_percent: float
    memory_usage_mb: float
    active_agents: int
    message_queue_depth: int
    average_latency_ms: float
    timestamp: float = field(default_factory=time.time)


# --- Classe Principal do Agente ---

class PerformanceMonitorAgent(BaseNetworkAgent):
    """
    Agente especializado em monitorar a saúde e a performance do
    sistema de agentes em tempo real.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o PerformanceMonitorAgent."""
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.extend([
            "performance_monitoring",
            "metric_collection",
            "system_health_check",
            "alerting_trigger",
        ])
        self.monitoring_interval_seconds = 60
        self.latency_tracker = deque(maxlen=100) # Rastreia as últimas 100 latências
        
        self.process = psutil.Process()
        
        logger.info(f"📊 {self.agent_id} (Monitor de Performance) inicializado.")
        # O loop de monitoramento contínuo será iniciado pelo Orchestrator
        # através de uma mensagem de 'start_monitoring'.

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para coletar métricas ou iniciar monitoramento."""
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            
            if request_type == "get_performance_metrics":
                metrics = self.collect_metrics()
                response_content = {
                    "status": "completed",
                    "metrics": metrics.__dict__
                }
                await self.publish_response(message, response_content)
                
            elif request_type == "start_continuous_monitoring":
                interval = message.content.get("interval", self.monitoring_interval_seconds)
                asyncio.create_task(self.run_continuous_monitoring(interval))
                await self.publish_response(message, {"status": "acknowledged", "message": "Monitoramento contínuo iniciado."})

    def collect_metrics(self) -> PerformanceMetrics:
        """
        [LÓGICA REAL] Coleta as métricas de performance do sistema.
        """
        try:
            # Métricas de CPU e Memória do processo atual
            with self.process.oneshot():
                cpu_usage = self.process.cpu_percent()
                memory_info = self.process.memory_info()
                memory_usage_mb = memory_info.rss / (1024 * 1024)
            
            # Pega o uso total de memória do sistema para calcular o percentual
            total_memory_percent = psutil.virtual_memory().percent

            # Métricas da rede de agentes
            network_metrics = self.message_bus.get_metrics()
            active_agents = network_metrics.get("subscribed_agents", 0)
            
            # Calcula a profundidade total da fila de mensagens
            queue_depths = network_metrics.get("queue_depths", {})
            total_queue_depth = sum(queue_depths.values())
            
            # Calcula a latência média (simulada por enquanto)
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
            # Retorna um objeto de métricas vazio ou com valores de erro
            return PerformanceMetrics(0, 0, 0, 0, 0, -1.0)
            
    async def run_continuous_monitoring(self, interval: int):
        """Executa a coleta de métricas em um loop contínuo."""
        logger.info(f"Monitoramento contínuo iniciado com intervalo de {interval} segundos.")
        while self.status == "active":
            metrics = self.collect_metrics()
            
            # Notifica o LoggingAgent com as novas métricas
            log_message = self.create_message(
                recipient_id="logging_001",
                message_type=MessageType.NOTIFICATION,
                content={
                    "event_type": "performance_metrics",
                    "metrics": metrics.__dict__
                }
            )
            await self.message_bus.publish(log_message)
            
            await asyncio.sleep(interval)


def create_performance_monitor_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Monitoramento de Performance."""
    agents = []
    logger.info("📊 Criando PerformanceMonitorAgent...")
    try:
        agent = PerformanceMonitorAgent("performance_monitor_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando PerformanceMonitorAgent: {e}", exc_info=True)
    return agents
