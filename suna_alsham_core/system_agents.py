#!/usr/bin/env python3
"""
Módulo dos Agentes de Sistema - SUNA-ALSHAM

Define os agentes responsáveis por monitorar e controlar o próprio sistema.
"""

import asyncio
import logging
from typing import Any, Dict, List, Set

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Agentes de Sistema ---

class MonitorAgent(BaseNetworkAgent):
    """
    Agente que monitora a saúde de outros agentes e da rede.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.append("health_monitoring")

    async def start_monitoring(self, interval: int = 60):
        """Inicia o ciclo de monitoramento contínuo."""
        logger.info(f"📊 {self.agent_id} iniciou monitoramento contínuo.")
        while True:
            await self.check_agent_health()
            await asyncio.sleep(interval)

    async def check_agent_health(self):
        """Envia um 'heartbeat' para todos os agentes registrados."""
        # A CORREÇÃO ESTÁ AQUI:
        # Trocamos .subscribers por .queues para alinhar com a classe MessageBus
        agent_ids = self.message_bus.queues.keys()
        
        heartbeat_message = self.create_message(
            recipient_id="broadcast",
            message_type=MessageType.HEARTBEAT,
            content={"status": "ping"}
        )
        await self.message_bus.publish(heartbeat_message)
        logger.debug(f"Heartbeat enviado para {len(agent_ids) - 1} agentes.")

class ControlAgent(BaseNetworkAgent):
    """
    Agente que pode emitir comandos para o sistema (ex: shutdown).
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.append("system_control")

class RecoveryAgent(BaseNetworkAgent):
    """
    Agente que tenta recuperar outros agentes em caso de falha.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.append("agent_recovery")

# --- Função de Fábrica ---

def create_system_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria os agentes de Sistema."""
    logger.info("🖥️ Criando agentes de Sistema...")
    agents = [
        MonitorAgent("monitor_001", message_bus),
        ControlAgent("control_001", message_bus),
        RecoveryAgent("recovery_001", message_bus),
    ]
    # Inicia o monitoramento em background
    asyncio.create_task(agents[0].start_monitoring())
    return agents
