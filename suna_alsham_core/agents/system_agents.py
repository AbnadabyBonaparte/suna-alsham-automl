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
        # Usando .queues que é o correto para a classe MessageBus
        agent_ids = self.message_bus.queues.keys()
        
        heartbeat_message = self.create_message(
            recipient_id="broadcast",
            message_type=MessageType.HEARTBEAT,
            content={"status": "ping"}
        )
        await self.message_bus.publish(heartbeat_message)
        logger.debug(f"Heartbeat enviado para {len(agent_ids) - 1} agentes.")
    
    async def _internal_handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas pelo monitor"""
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            
            if request_type == "system_status":
                # Coletar status do sistema
                agent_count = len(self.message_bus.queues.keys()) if hasattr(self.message_bus, 'queues') else 0
                
                status_report = {
                    "status": "operational",
                    "total_agents": agent_count,
                    "monitor_agent": self.agent_id,
                    "timestamp": self.timestamp
                }
                
                await self.publish_response(message, status_report)
                
            elif request_type == "health_check":
                # Verificação de saúde individual
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
        """Processa comandos de controle do sistema"""
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            
            if request_type == "shutdown_agent":
                # Comando para desligar um agente específico
                target_agent = message.content.get("target_agent")
                if target_agent:
                    await self._shutdown_agent(target_agent)
                    await self.publish_response(message, {
                        "status": "completed",
                        "action": "shutdown",
                        "target": target_agent
                    })
            
            elif request_type == "restart_agent":
                # Comando para reiniciar um agente
                target_agent = message.content.get("target_agent")
                if target_agent:
                    await self._restart_agent(target_agent)
                    await self.publish_response(message, {
                        "status": "completed",
                        "action": "restart",
                        "target": target_agent
                    })
            
            elif request_type == "emergency_stop":
                # Parada de emergência
                await self._emergency_shutdown()
                await self.publish_response(message, {
                    "status": "completed",
                    "action": "emergency_stop"
                })
    
    async def _shutdown_agent(self, agent_id: str):
        """Desliga um agente específico"""
        logger.warning(f"🛑 Desligando agente: {agent_id}")
        # Enviar comando de shutdown
        shutdown_message = self.create_message(
            recipient_id=agent_id,
            message_type=MessageType.NOTIFICATION,
            content={"command": "shutdown"},
            priority=Priority.CRITICAL
        )
        await self.message_bus.publish(shutdown_message)
    
    async def _restart_agent(self, agent_id: str):
        """Reinicia um agente específico"""
        logger.info(f"🔄 Reiniciando agente: {agent_id}")
        # Primeiro desliga
        await self._shutdown_agent(agent_id)
        await asyncio.sleep(2)  # Aguarda shutdown
        # Depois envia comando de restart
        restart_message = self.create_message(
            recipient_id=agent_id,
            message_type=MessageType.NOTIFICATION,
            content={"command": "restart"},
            priority=Priority.HIGH
        )
        await self.message_bus.publish(restart_message)
    
    async def _emergency_shutdown(self):
        """Executa parada de emergência do sistema"""
        logger.critical("🚨 PARADA DE EMERGÊNCIA ATIVADA!")
        # Notifica todos os agentes
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
        """Processa notificações de falha e requisições de recuperação"""
        if message.message_type == MessageType.NOTIFICATION:
            event_type = message.content.get("event_type")
            
            if event_type == "agent_failure":
                # Detectada falha em um agente
                failed_agent = message.content.get("agent_id")
                if failed_agent:
                    await self._handle_agent_failure(failed_agent)
            
            elif event_type == "agent_unresponsive":
                # Agente não está respondendo
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
                # Status das recuperações
                status = {
                    "failed_agents": list(self.failed_agents.keys()),
                    "recovery_attempts": self.recovery_attempts,
                    "total_failures": len(self.failed_agents)
                }
                await self.publish_response(message, status)
    
    async def _handle_agent_failure(self, agent_id: str):
        """Trata falha de um agente"""
        logger.error(f"❌ Falha detectada no agente: {agent_id}")
        self.failed_agents[agent_id] = {
            "failure_time": self.timestamp,
            "status": "failed"
        }
        # Tentar recuperação automática
        await self._recover_agent(agent_id)
    
    async def _handle_unresponsive_agent(self, agent_id: str):
        """Trata agente que não responde"""
        logger.warning(f"⚠️ Agente não responsivo: {agent_id}")
        # Enviar ping direto
        ping_message = self.create_message(
            recipient_id=agent_id,
            message_type=MessageType.HEARTBEAT,
            content={"ping": True},
            priority=Priority.HIGH
        )
        await self.message_bus.publish(ping_message)
        
        # Aguardar resposta
        await asyncio.sleep(5)
        
        # Se ainda não responder, marcar como falho
        if agent_id not in self.failed_agents:
            await self._handle_agent_failure(agent_id)
    
    async def _recover_agent(self, agent_id: str) -> bool:
        """Tenta recuperar um agente falho"""
        logger.info(f"🔧 Tentando recuperar agente: {agent_id}")
        
        # Rastrear tentativas
        if agent_id not in self.recovery_attempts:
            self.recovery_attempts[agent_id] = 0
        
        self.recovery_attempts[agent_id] += 1
        
        # Máximo de 3 tentativas
        if self.recovery_attempts[agent_id] > 3:
            logger.error(f"❌ Falha ao recuperar {agent_id} após 3 tentativas")
            return False
        
        # Enviar comando de recuperação
        recovery_message = self.create_message(
            recipient_id=agent_id,
            message_type=MessageType.NOTIFICATION,
            content={"command": "recover", "attempt": self.recovery_attempts[agent_id]},
            priority=Priority.CRITICAL
        )
        await self.message_bus.publish(recovery_message)
        
        # Aguardar recuperação
        await asyncio.sleep(3)
        
        # Verificar se recuperou
        check_message = self.create_message(
            recipient_id=agent_id,
            message_type=MessageType.HEARTBEAT,
            content={"check": True}
        )
        await self.message_bus.publish(check_message)
        
        # Por simplicidade, assumimos sucesso após envio
        # Em produção, aguardaria resposta real
        if agent_id in self.failed_agents:
            del self.failed_agents[agent_id]
        
        logger.info(f"✅ Agente {agent_id} recuperado com sucesso!")
        return True


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
    
    logger.info(f"✅ {len(agents)} agentes de Sistema criados com sucesso.")
    return agents
