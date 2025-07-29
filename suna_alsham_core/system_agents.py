#!/usr/bin/env python3
"""
Módulo dos Agentes de Sistema - SUNA-ALSHAM

[Fase 2] - Revisão Final. Alinhado com a BaseNetworkAgent fortalecida.
Define agentes responsáveis por monitorar a saúde da infraestrutura (CPU, memória),
controlar serviços e executar planos de recuperação de baixo nível.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# [AUTENTICIDADE] psutil é a biblioteca padrão para métricas de sistema.
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Import alinhado com a Fase 1
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses (sem alteração) ---

class SystemStatus(Enum):
    """Status de saúde do sistema."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


class ControlAction(Enum):
    """Ações de controle do sistema."""
    CLEAR_CACHE = "clear_cache"
    OPTIMIZE_MEMORY = "optimize_memory"


@dataclass
class SystemMetrics:
    """Métricas de saúde do sistema."""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    status: SystemStatus


# --- Classes Principais dos Agentes ---

class SystemMonitorAgent(BaseNetworkAgent):
    """
    Agente que monitora ativamente as métricas de hardware do sistema (CPU, memória)
    e gera alertas quando os limiares são ultrapassados.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SystemMonitorAgent."""
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.append("system_monitoring")
        self.alert_thresholds = {"cpu": 85.0, "memory": 90.0}
        self._monitoring_task: Optional[asyncio.Task] = None
        if not PSUTIL_AVAILABLE: self.status = "degraded"
        logger.info(f"✅ {self.agent_id} (Monitor de Sistema) inicializado.")

    async def start_monitoring_service(self):
        """Inicia o loop de monitoramento contínuo."""
        if not self._monitoring_task and self.status == "active":
            self._monitoring_task = asyncio.create_task(self._continuous_monitoring())
            logger.info(f"📊 {self.agent_id} iniciou monitoramento contínuo.")

    async def _continuous_monitoring(self):
        """Executa a coleta e análise de métricas periodicamente."""
        while True:
            try:
                metrics = self._collect_metrics()
                if metrics.status == SystemStatus.CRITICAL:
                    await self._send_alert(metrics)
                await asyncio.sleep(60) # Monitora a cada 60 segundos
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de monitoramento: {e}", exc_info=True)

    def _collect_metrics(self) -> SystemMetrics:
        """Coleta métricas atuais do sistema usando psutil."""
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        status = SystemStatus.HEALTHY
        
        if cpu > self.alert_thresholds["cpu"] or mem.percent > self.alert_thresholds["memory"]:
            status = SystemStatus.CRITICAL
        elif cpu > 70 or mem.percent > 75:
            status = SystemStatus.WARNING
            
        return SystemMetrics(datetime.now(), cpu, mem.percent, status)

    async def _send_alert(self, metrics: SystemMetrics):
        """Envia um alerta para o agente de controle."""
        logger.warning(f"⚠️ Alerta de sistema gerado: {metrics.status.value}")
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
    para estabilizar o sistema.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SystemControlAgent."""
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.append("system_control")
        logger.info(f"✅ {self.agent_id} (Controle de Sistema) inicializado.")
    
    async def _internal_handle_message(self, message: AgentMessage):
        """Processa notificações de alerta e executa ações."""
        if message.message_type == MessageType.NOTIFICATION and message.content.get("notification_type") == "system_alert":
            await self._process_system_alert(message.content)

    async def _process_system_alert(self, alert_content: Dict[str, Any]):
        """Decide e executa uma ação de controle baseada em um alerta."""
        metrics = alert_content.get("metrics", {})
        if metrics.get("cpu_percent", 0) > self.alert_thresholds["cpu"]:
            await self._execute_control_action(ControlAction.OPTIMIZE_MEMORY, "CPU alta")
        if metrics.get("memory_percent", 0) > self.alert_thresholds["memory"]:
            await self._execute_control_action(ControlAction.CLEAR_CACHE, "Memória alta")

    async def _execute_control_action(self, action: ControlAction, reason: str):
        """[AUTENTICIDADE] Placeholder para execução real da ação."""
        logger.info(f"⚡ [Simulação] Executando ação: {action.value} | Razão: {reason}")


class SystemRecoveryAgent(BaseNetworkAgent):
    """
    Agente focado em planos de recuperação para falhas de componentes de software.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SystemRecoveryAgent."""
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.append("system_recovery")
        logger.info(f"✅ {self.agent_id} (Recuperação de Sistema) inicializado.")


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
            if isinstance(agent, SystemMonitorAgent):
                asyncio.create_task(agent.start_monitoring_service())
            agents.append(agent)
        except Exception as e:
            logger.error(f"❌ Erro criando agente de sistema {config['id']}: {e}", exc_info=True)

    return agents
