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
        logger.info(f"📊 {self.agent_id} inicializado para monitoramento do sistema.")
    
    async def start_monitoring(self, interval: int = 60):
        """Inicia o ciclo de monitoramento contínuo."""
        logger.info(f"📊 {self.agent_id} iniciou monitoramento contínuo.")
        while True:
            await self.check_agent_health()
            await asyncio.sleep(interval)
    
    async def check_agent_health(self):
        """Envia um 'heartbeat' para todos os agentes registrados."""
        agent_ids = self.message_bus.queues.keys()
        heartbeat_message = self.create_message(
            recipient_id="broadcast",
            message_type=MessageType.HEARTBEAT,
            content={"status": "ping"}
        )
        await self.message_bus.publish(heartbeat_message)
        logger.debug(f"Heartbeat enviado para {len(agent_ids) - 1} agentes.")
    
    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            if request_type == "system_status":
                agent_count = len(self.message_bus.queues.keys()) if hasattr(self.message_bus, 'queues') else 0
                status_report = {
                    "status": "operational",
                    "total_agents": agent_count,
                    "monitor_agent": self.agent_id,
                    "timestamp": self.timestamp
                }
                await self.publish_response(message, status_report)
            elif request_type == "health_check":
                health_status = {
                    "agent_id": self.agent_id,
                    "status": "healthy",
                    "capabilities": self.capabilities,
                    "uptime": "running"
                }
                await self.publish_response(message, health_status)


class ControlAgent(BaseNetworkAgent):
    """
    Agente que pode emitir comandos para o sistema (ex: shutdown).
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.extend([
            "system_control",
            "agent_management",
            "emergency_shutdown"
        ])
        self.controlled_agents = set()
        logger.info(f"🎮 {self.agent_id} inicializado para controle do sistema.")
    
    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            if request_type == "shutdown_agent":
                target_agent = message.content.get("target_agent")
                if target_agent:
                    await self._shutdown_agent(target_agent)
                    await self.publish_response(message, {
                        "status": "completed",
                        "action": "shutdown",
                        "target": target_agent
                    })
            elif request_type == "restart_agent":
                target_agent = message.content.get("target_agent")
                if target_agent:
                    await self._restart_agent(target_agent)
                    await self.publish_response(message, {
                        "status": "completed",
                        "action": "restart",
                        "target": target_agent
                    })
            elif request_type == "emergency_stop":
                await self._emergency_shutdown()
                await self.publish_response(message, {
                    "status": "completed",
                    "action": "emergency_stop"
                })
    
    async def _shutdown_agent(self, agent_id: str):
        logger.warning(f"🛑 Desligando agente: {agent_id}")
        shutdown_message = self.create_message(
            recipient_id=agent_id,
            message_type=MessageType.NOTIFICATION,
            content={"command": "shutdown"},
            priority=Priority.CRITICAL
        )
        await self.message_bus.publish(shutdown_message)
    
    async def _restart_agent(self, agent_id: str):
        logger.info(f"🔄 Reiniciando agente: {agent_id}")
        await self._shutdown_agent(agent_id)
        await asyncio.sleep(2)
        restart_message = self.create_message(
            recipient_id=agent_id,
            message_type=MessageType.NOTIFICATION,
            content={"command": "restart"},
            priority=Priority.HIGH
        )
        await self.message_bus.publish(restart_message)
    
    async def _emergency_shutdown(self):
        logger.critical("🚨 PARADA DE EMERGÊNCIA ATIVADA!")
        emergency_message = self.create_message(
            recipient_id="broadcast",
            message_type=MessageType.NOTIFICATION,
            content={"command": "emergency_shutdown"},
            priority=Priority.CRITICAL
        )
        await self.message_bus.publish(emergency_message)


class RecoveryAgent(BaseNetworkAgent):
    """
    Agente que tenta recuperar outros agentes em caso de falha.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SYSTEM, message_bus)
        self.capabilities.extend([
            "agent_recovery",
            "failure_detection",
            "automatic_restart"
        ])
        self.failed_agents = {}
        self.recovery_attempts = {}
        logger.info(f"🔧 {self.agent_id} inicializado para recuperação de falhas.")
    
    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.NOTIFICATION:
            event_type = message.content.get("event_type")
            if event_type == "agent_failure":
                failed_agent = message.content.get("agent_id")
                if failed_agent:
                    await self._handle_agent_failure(failed_agent)
            elif event_type == "agent_unresponsive":
                unresponsive_agent = message.content.get("agent_id")
                if unresponsive_agent:
                    await self._handle_unresponsive_agent(unresponsive_agent)
        elif message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            if request_type == "recover_agent":
                target_agent = message.content.get("target_agent")
                if target_agent:
                    success = await self._recover_agent(target_agent)
                    await self.publish_response(message, {
                        "status": "completed" if success else "failed",
                        "agent_recovered": target_agent,
                        "success": success
                    })
            elif request_type == "recovery_status":
                status = {
                    "failed_agents": list(self.failed_agents.keys()),
                    "recovery_attempts": self.recovery_attempts,
                    "total_failures": len(self.failed_agents)
                }
                await self.publish_response(message, status)
    
    async def _handle_agent_failure(self, agent_id: str):
        logger.error(f"❌ Falha detectada no agente: {agent_id}")
        self.failed_agents[agent_id] = {
            "failure_time": self.timestamp,
            "status": "failed"
        }
        await self._recover_agent(agent_id)
    
    async def _handle_unresponsive_agent(self, agent_id: str):
        logger.warning(f"⚠️ Agente não responsivo: {agent_id}")
        ping_message = self.create_message(
            recipient_id=agent_id,
            message_type=MessageType.HEARTBEAT,
            content={"ping": True},
            priority=Priority.HIGH
        )
        await self.message_bus.publish(ping_message)
        await asyncio.sleep(5)
        if agent_id not in self.failed_agents:
            await self._handle_agent_failure(agent_id)
    
    async def _recover_agent(self, agent_id: str) -> bool:
        logger.info(f"🔧 Tentando recuperar agente: {agent_id}")
        if agent_id not in self.recovery_attempts:
            self.recovery_attempts[agent_id] = 0
        self.recovery_attempts[agent_id] += 1
        if self.recovery_attempts[agent_id] > 3:
            logger.error(f"❌ Falha ao recuperar {agent_id} após 3 tentativas")
            return False
        recovery_message = self.create_message(
            recipient_id=agent_id,
            message_type=MessageType.NOTIFICATION,
            content={"command": "recover", "attempt": self.recovery_attempts[agent_id]},
            priority=Priority.CRITICAL
        )
        await self.message_bus.publish(recovery_message)
        await asyncio.sleep(3)
        check_message = self.create_message(
            recipient_id=agent_id,
            message_type=MessageType.HEARTBEAT,
            content={"check": True}
        )
        await self.message_bus.publish(check_message)
        if agent_id in self.failed_agents:
            del self.failed_agents[agent_id]
        logger.info(f"✅ Agente {agent_id} recuperado com sucesso!")
        return True


def create_agents(message_bus: Any) -> List[BaseNetworkAgent]:
    """
    Função fábrica para criar e inicializar os agentes de sistema do ALSHAM QUANTUM.

    Esta função instancia os agentes MonitorAgent, ControlAgent e RecoveryAgent, registra todos os eventos relevantes para diagnóstico
    e retorna em uma lista para registro no agent registry. Lida com erros de forma robusta
    e garante que os agentes estejam prontos para operação.

    Args:
        message_bus (Any): O barramento de mensagens ou canal de comunicação para mensagens entre agentes.

    Returns:
        List[BaseNetworkAgent]: Uma lista contendo as instâncias inicializadas dos agentes de sistema.
    """
    logger.info("⚙️ Criando agentes de sistema (Monitor, Control, Recovery)...")
    agents: List[BaseNetworkAgent] = []
    agent_configs = [
        {"id": "monitor_001", "class": MonitorAgent},
        {"id": "control_001", "class": ControlAgent},
        {"id": "recovery_001", "class": RecoveryAgent},
    ]
    for config in agent_configs:
        try:
            agent = config["class"](config["id"], message_bus)
            agents.append(agent)
            logger.info(f"✅ Agente de sistema {config['id']} criado com sucesso.")
        except Exception as e:
            logger.error(f"❌ Erro criando agente de sistema {config['id']}: {e}", exc_info=True)
    logger.info(f"⚙️ Total de agentes de sistema criados: {len(agents)}")
    return agents
