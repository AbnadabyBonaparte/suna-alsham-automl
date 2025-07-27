#!/usr/bin/env python3
"""
Módulo dos Agentes de Sistema - SUNA-ALSHAM

Define agentes responsáveis por monitorar a saúde da infraestrutura (CPU, memória),
controlar serviços e executar planos de recuperação de baixo nível.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
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


class SystemStatus(Enum):
    """Status de saúde do sistema."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class ControlAction(Enum):
    """Ações de controle do sistema."""
    RESTART_SERVICE = "restart_service"
    CLEAR_CACHE = "clear_cache"
    OPTIMIZE_MEMORY = "optimize_memory"


@dataclass
class SystemMetrics:
    """Métricas de saúde do sistema."""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    status: SystemStatus
    alerts: List[Dict[str, Any]] = field(default_factory=list)


class SystemMonitorAgent(BaseNetworkAgent):
    """
    Agente que monitora ativamente as métricas de hardware do sistema (CPU, memória, disco)
    usando psutil e gera alertas quando os limiares são ultrapassados.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SystemMonitorAgent."""
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.extend(["system_monitoring", "metrics_collection"])
        self.metrics_history = []
        self.alert_thresholds = {"cpu": 85.0, "memory": 90.0, "disk": 95.0}
        self.monitoring_interval = 60  # segundos
        self._monitoring_task = None
        logger.info(f"✅ {self.agent_id} inicializado com monitoramento de sistema.")

    async def start_monitoring(self):
        """Inicia o loop de monitoramento contínuo."""
        if not self._monitoring_task:
            self._monitoring_task = asyncio.create_task(self._continuous_monitoring())
            logger.info(f"📊 {self.agent_id} iniciou monitoramento contínuo.")

    async def _continuous_monitoring(self):
        """Executa a coleta e análise de métricas periodicamente."""
        while True:
            try:
                metrics = self._collect_metrics()
                if metrics.alerts:
                    await self._send_alert(metrics)
                await asyncio.sleep(self.monitoring_interval)
            except asyncio.CancelledError:
                logger.info(f"Monitoramento do {self.agent_id} cancelado.")
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de monitoramento do {self.agent_id}: {e}", exc_info=True)
                await asyncio.sleep(self.monitoring_interval * 2) # Espera mais em caso de erro

    def _collect_metrics(self) -> SystemMetrics:
        """Coleta métricas atuais do sistema usando psutil."""
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        status = SystemStatus.HEALTHY
        alerts = []

        if cpu > self.alert_thresholds["cpu"]:
            status = SystemStatus.WARNING
            alerts.append({"type": "cpu_high", "value": cpu})
        if mem.percent > self.alert_thresholds["memory"]:
            status = SystemStatus.CRITICAL if status == SystemStatus.WARNING else SystemStatus.WARNING
            alerts.append({"type": "memory_high", "value": mem.percent})
        
        return SystemMetrics(datetime.now(), cpu, mem.percent, disk.percent, status, alerts)

    async def _send_alert(self, metrics: SystemMetrics):
        """Envia um alerta para o agente de controle."""
        logger.warning(f"⚠️ Alerta de sistema gerado: {metrics.status.value} - {metrics.alerts}")
        alert_message = self.create_message(
            recipient_id="control_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.HIGH,
            content={"notification_type": "system_alert", "metrics": metrics.__dict__},
        )
        await self.message_bus.publish(alert_message)


class SystemControlAgent(BaseNetworkAgent):
    """
    Agente que recebe alertas do SystemMonitor e executa ações de controle
    para estabilizar o sistema, como limpar caches ou reiniciar serviços.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SystemControlAgent."""
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.extend(["system_control", "resource_management"])
        logger.info(f"✅ {self.agent_id} inicializado com controle de sistema.")
    
    async def handle_message(self, message: AgentMessage):
        """Processa notificações de alerta e executa ações."""
        await super().handle_message(message)
        if message.message_type == MessageType.NOTIFICATION:
            if message.content.get("notification_type") == "system_alert":
                await self._process_system_alert(message.content)

    async def _process_system_alert(self, alert_content: Dict[str, Any]):
        """Decide e executa uma ação de controle baseada em um alerta."""
        alerts = alert_content.get("metrics", {}).get("alerts", [])
        for alert in alerts:
            action_to_take = None
            if alert.get("type") == "cpu_high":
                action_to_take = ControlAction.OPTIMIZE_MEMORY
            elif alert.get("type") == "memory_high":
                action_to_take = ControlAction.CLEAR_CACHE
            
            if action_to_take:
                await self._execute_control_action(action_to_take, f"Alerta automático: {alert.get('type')}")

    async def _execute_control_action(self, action: ControlAction, reason: str):
        """Simula a execução de uma ação de controle."""
        logger.info(f"⚡ Executando ação de controle: {action.value} | Razão: {reason}")
        # Lógica de execução real iria aqui (ex: limpar cache do Redis)
        await asyncio.sleep(1) # Simula tempo de execução
        logger.info(f"✅ Ação {action.value} concluída.")


class SystemRecoveryAgent(BaseNetworkAgent):
    """
    Agente focado em planos de recuperação para falhas de componentes do sistema.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SystemRecoveryAgent."""
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.append("system_recovery")
        logger.info(f"✅ {self.agent_id} inicializado com planos de recuperação.")

    # A lógica mais complexa de recuperação de desastres foi movida para o DisasterRecoveryAgent.
    # Este agente pode ser usado para recuperações mais simples e focadas em software.
    async def _handle_emergency(self, emergency_message: AgentMessage):
        """Trata situações de emergência de software."""
        issue = emergency_message.content.get("issue_type", "unknown_failure")
        logger.critical(f"🚨 EMERGÊNCIA DE SOFTWARE DETECTADA: {issue}")
        # Lógica para reiniciar um agente específico ou reverter uma configuração.


def create_system_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Cria os 3 agentes de sistema: Monitor, Controle e Recuperação.
    """
    agents = []
    logger.info("🖥️ Criando agentes de Sistema...")
    
    agent_configs = [
        {"id": "monitor_001", "class": SystemMonitorAgent},
        {"id": "control_001", "class": SystemControlAgent},
        {"id": "recovery_001", "class": SystemRecoveryAgent},
    ]
    
    for config in agent_configs:
        try:
            agent = config["class"](config["id"], message_bus)
            # Iniciar monitoramento automático para o monitor
            if isinstance(agent, SystemMonitorAgent):
                asyncio.create_task(agent.start_monitoring())
            agents.append(agent)
        except Exception as e:
            logger.error(f"❌ Erro criando agente {config['id']}: {e}", exc_info=True)

    return agents
