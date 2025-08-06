#!/usr/bin/env python3
"""
Módulo da Rede Multi-Agente - Coração do SUNA-ALSHAM
Versão corrigida com create_agents e NetworkManagerAgent implementado.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
import time
from datetime import datetime

logger = logging.getLogger(__name__)

# Tipos de Mensagem
class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"
    HEARTBEAT = "heartbeat"
    BROADCAST = "broadcast"
    STATUS_UPDATE = "status_update"
    NETWORK_EVENT = "network_event"

# Prioridade de Mensagem
class Priority(Enum):
    LOW = 3
    NORMAL = 2
    HIGH = 1
    CRITICAL = 0

# Tipos de Agentes
class AgentType(Enum):
    CORE = "core"
    SPECIALIZED = "specialized"
    SERVICE = "service"
    SYSTEM = "system"
    META_COGNITIVE = "meta_cognitive"
    BUSINESS_DOMAIN = "business_domain"
    AI_POWERED = "ai_powered"
    ORCHESTRATOR = "orchestrator"
    GUARD = "guard"
    AUTOMATOR = "automator"
    NETWORK_MANAGER = "network_manager"

# Estrutura da Mensagem de Agentes
@dataclass
class AgentMessage:
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = "system"
    recipient_id: str = "broadcast"
    message_type: MessageType = MessageType.NOTIFICATION
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    priority: Priority = Priority.NORMAL
    callback_id: Optional[str] = None

@dataclass
class NetworkStats:
    """Estatísticas da rede multi-agente."""
    total_agents: int = 0
    active_agents: int = 0
    messages_sent: int = 0
    messages_received: int = 0
    network_uptime: float = 0.0
    last_heartbeat: Optional[str] = None

@dataclass  
class AgentConnectionInfo:
    """Informações de conexão de um agente."""
    agent_id: str
    connected_at: datetime
    last_seen: datetime
    message_count: int = 0
    status: str = "active"
    agent_type: Optional[AgentType] = None

# Barramento de Mensagens
class MessageBus:
    """Sistema de mensageria assíncrono para comunicação entre agentes."""
    
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue] = {}
        self.running = False
        self.message_count = 0
        self.start_time = time.time()
        
    async def start(self):
        """Inicia o message bus."""
        self.running = True
        self.start_time = time.time()
        logger.info("📡 MessageBus iniciado")

    async def stop(self):
        """Para o message bus."""
        self.running = False
        logger.info("📡 MessageBus parado")

    async def publish(self, message: AgentMessage):
        """Publica uma mensagem no bus."""
        if not self.running:
            return
            
        self.message_count += 1
        
        try:
            # Lógica para broadcast
            if message.recipient_id == "broadcast":
                published_count = 0
                for agent_id in self.queues:
                    if agent_id != message.sender_id:
                        await self.queues[agent_id].put(message)
                        published_count += 1
                logger.debug(f"📡 Broadcast enviado para {published_count} agentes")
            # Lógica para mensagem direta
            elif message.recipient_id in self.queues:
                await self.queues[message.recipient_id].put(message)
                logger.debug(f"📡 Mensagem enviada: {message.sender_id} → {message.recipient_id}")
            else:
                logger.warning(f"⚠️ Destinatário não encontrado: {message.recipient_id}")
        except Exception as e:
            logger.error(f"❌ Erro ao publicar mensagem: {e}")

    def subscribe(self, agent_id: str) -> asyncio.Queue:
        """Subscreve um agente ao message bus."""
        if agent_id not in self.queues:
            self.queues[agent_id] = asyncio.Queue()
            logger.debug(f"📡 Agente subscrito: {agent_id}")
        return self.queues[agent_id]

    def unsubscribe(self, agent_id: str):
        """Remove um agente do message bus."""
        if agent_id in self.queues:
            del self.queues[agent_id]
            logger.debug(f"📡 Agente removido: {agent_id}")

    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas do message bus."""
        uptime = time.time() - self.start_time
        return {
            "running": self.running,
            "total_queues": len(self.queues),
            "messages_processed": self.message_count,
            "uptime_seconds": uptime,
            "messages_per_second": self.message_count / max(uptime, 1)
        }

# Rede Multi-Agente Principal
class MultiAgentNetwork:
    """
    Rede Multi-Agente Principal do ALSHAM QUANTUM.
    Gerencia todo o sistema de agentes e sua comunicação.
    """
    
    def __init__(self):
        self.message_bus = MessageBus()
        self.agents: Dict[str, Any] = {}
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.connection_info: Dict[str, AgentConnectionInfo] = {}
        self.running = False
        self.stats = NetworkStats()
        self.heartbeat_task = None
        logger.info("🌐 MultiAgentNetwork inicializada")

    async def start(self):
        """Inicia a rede multi-agente."""
        await self.message_bus.start()
        self.running = True
        self.stats.network_uptime = time.time()
        
        # Inicia heartbeat em background
        self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
        logger.info("✅ MultiAgentNetwork ativada")

    async def stop(self):
        """Para a rede multi-agente."""
        self.running = False
        
        # Para heartbeat
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            
        await self.message_bus.stop()
        logger.info("⏹️ MultiAgentNetwork desativada")

    def register_agent(self, agent):
        """Registra um agente na rede."""
        now = datetime.now()
        
        if hasattr(agent, 'agent_id'):
            agent_id = agent.agent_id
        else:
            # Fallback para agentes sem agent_id
            agent_id = f"agent_{len(self.agents)}"
            
        # Registra o agente
        self.agents[agent_id] = agent
        
        # Atualiza registry
        self.agent_registry[agent_id] = {
            'agent': agent,
            'type': getattr(agent, 'agent_type', AgentType.SYSTEM),
            'status': getattr(agent, 'status', 'active'),
            'capabilities': getattr(agent, 'capabilities', [])
        }
        
        # Atualiza informações de conexão
        self.connection_info[agent_id] = AgentConnectionInfo(
            agent_id=agent_id,
            connected_at=now,
            last_seen=now,
            agent_type=getattr(agent, 'agent_type', None)
        )
        
        # Atualiza estatísticas
        self._update_stats()
        
        logger.info(f"📝 Agente registrado: {agent_id}")
        return agent_id

    def unregister_agent(self, agent_id: str):
        """Remove um agente da rede."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            del self.agent_registry[agent_id]
            if agent_id in self.connection_info:
                del self.connection_info[agent_id]
            
            # Remove do message bus
            self.message_bus.unsubscribe(agent_id)
            
            self._update_stats()
            logger.info(f"📝 Agente removido: {agent_id}")

    def _update_stats(self):
        """Atualiza estatísticas da rede."""
        self.stats.total_agents = len(self.agents)
        self.stats.active_agents = len([
            info for info in self.agent_registry.values()
            if info.get('status') == 'active'
        ])

    async def _heartbeat_loop(self):
        """Loop de heartbeat da rede."""
        try:
            while self.running:
                await self._send_heartbeat()
                await asyncio.sleep(30)  # Heartbeat a cada 30 segundos
        except asyncio.CancelledError:
            logger.info("🫀 Heartbeat loop cancelado")
        except Exception as e:
            logger.error(f"❌ Erro no heartbeat loop: {e}")

    async def _send_heartbeat(self):
        """Envia heartbeat para todos os agentes."""
        try:
            heartbeat_message = AgentMessage(
                sender_id="network_manager",
                recipient_id="broadcast",
                message_type=MessageType.HEARTBEAT,
                content={
                    "timestamp": datetime.now().isoformat(),
                    "network_stats": {
                        "active_agents": self.stats.active_agents,
                        "total_agents": self.stats.total_agents,
                        "uptime": time.time() - self.stats.network_uptime
                    }
                }
            )
            
            await self.message_bus.publish(heartbeat_message)
            self.stats.last_heartbeat = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar heartbeat: {e}")

    def get_agent_count(self) -> int:
        """Retorna o número total de agentes registrados."""
        return len(self.agents)

    def get_active_agents(self) -> List[str]:
        """Retorna lista de IDs dos agentes ativos."""
        return [
            agent_id for agent_id, info in self.agent_registry.items()
            if info.get('status') == 'active'
        ]

    def get_agents_by_type(self, agent_type: str) -> List[str]:
        """Retorna agentes filtrados por tipo."""
        return [
            agent_id for agent_id, info in self.agent_registry.items()
            if str(info.get('type', '')).split('.')[-1] == agent_type
        ]

    def get_network_status(self) -> Dict[str, Any]:
        """Retorna status completo da rede."""
        uptime = time.time() - self.stats.network_uptime if self.running else 0
        
        return {
            "running": self.running,
            "total_agents": self.stats.total_agents,
            "active_agents": self.stats.active_agents,
            "uptime_seconds": uptime,
            "last_heartbeat": self.stats.last_heartbeat,
            "message_bus_metrics": self.message_bus.get_metrics(),
            "agent_types_breakdown": self._get_agent_types_breakdown(),
            "connection_info": {
                agent_id: {
                    "connected_at": info.connected_at.isoformat(),
                    "last_seen": info.last_seen.isoformat(),
                    "status": info.status
                }
                for agent_id, info in self.connection_info.items()
            }
        }

    def _get_agent_types_breakdown(self) -> Dict[str, int]:
        """Retorna breakdown de agentes por tipo."""
        breakdown = {}
        for info in self.agent_registry.values():
            agent_type = str(info.get('type', 'unknown')).split('.')[-1]
            breakdown[agent_type] = breakdown.get(agent_type, 0) + 1
        return breakdown

# Classe Base para Agentes de Rede
class BaseNetworkAgent:
    """Classe base para todos os agentes da rede multi-agente."""
    
    def __init__(self, agent_id: str, agent_type: AgentType, message_bus: MessageBus):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_bus = message_bus
        self.inbox = self.message_bus.subscribe(self.agent_id)
        self.status = "active"
        self.capabilities: List[str] = []
        self.task = None
        self._start_message_loop()

    def _start_message_loop(self):
        """Inicia o loop de processamento de mensagens."""
        try:
            self.task = asyncio.create_task(self._run())
        except Exception as e:
            logger.error(f"Erro ao iniciar loop do agente {self.agent_id}: {e}")

    async def _run(self):
        """Loop principal de processamento de mensagens."""
        while True:
            try:
                message = await self.inbox.get()
                await self._internal_handle_message(message)
                self.inbox.task_done()
            except asyncio.CancelledError:
                logger.debug(f"Loop do agente {self.agent_id} cancelado")
                break
            except Exception as e:
                logger.error(f"Erro no loop do agente {self.agent_id}: {e}", exc_info=True)

    async def _internal_handle_message(self, message: AgentMessage):
        """Deve ser implementado nas subclasses."""
        logger.debug(f"Agente {self.agent_id} recebeu mensagem de {message.sender_id}")

    def create_message(
        self,
        recipient_id: str,
        message_type: MessageType,
        content: Dict[str, Any],
        priority: Priority = Priority.NORMAL,
        callback_id: Optional[str] = None
    ) -> AgentMessage:
        """Cria uma mensagem estruturada para comunicação entre agentes."""
        return AgentMessage(
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            message_type=message_type,
            content=content,
            priority=priority,
            callback_id=callback_id
        )

    def create_response(
        self,
        original_message: AgentMessage,
        content: Dict[str, Any]
    ) -> AgentMessage:
        """Cria uma mensagem de resposta baseada em uma mensagem original."""
        return self.create_message(
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            content=content,
            callback_id=original_message.callback_id
        )

    async def publish_response(
        self,
        original_message: AgentMessage,
        content: Dict[str, Any]
    ) -> None:
        """Publica uma resposta a partir de uma mensagem original."""
        response = self.create_response(original_message, content)
        await self.message_bus.publish(response)

    async def publish_error_response(
        self,
        original_message: AgentMessage,
        error_message: str
    ) -> None:
        """Publica uma resposta de erro padronizada."""
        error_content = {"status": "error", "message": error_message}
        response = self.create_response(original_message, error_content)
        await self.message_bus.publish(response)

    async def shutdown(self):
        """Desliga o agente graciosamente."""
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        self.status = "inactive"

    @property
    def timestamp(self) -> str:
        """Retorna o timestamp atual formatado."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

# Agente Gerenciador da Rede
class NetworkManagerAgent(BaseNetworkAgent):
    """
    Agente especializado para gerenciar a rede multi-agente.
    Monitora conectividade, estatísticas e saúde da rede.
    """
    
    def __init__(self, message_bus: MessageBus, network: MultiAgentNetwork):
        super().__init__(
            agent_id="network_manager_001",
            agent_type=AgentType.NETWORK_MANAGER,
            message_bus=message_bus
        )
        
        self.network = network
        self.capabilities = [
            "network_monitoring",
            "agent_discovery",
            "connection_management", 
            "network_diagnostics",
            "heartbeat_monitoring",
            "network_statistics"
        ]
        
        logger.info(f"🌐 {self.agent_id} (Network Manager) inicializado")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa mensagens do network manager."""
        try:
            content = message.content
            message_type = content.get("type", message.message_type.value)
            
            if message_type == "get_network_status":
                await self._handle_network_status_request(message)
            elif message_type == "get_agent_list":
                await self._handle_agent_list_request(message)
            elif message_type == "network_diagnostics":
                await self._handle_diagnostics_request(message)
            elif message_type == "agent_discovery":
                await self._handle_agent_discovery_request(message)
            else:
                # Log mensagens recebidas para debug
                logger.debug(f"🌐 NetworkManager recebeu: {message_type} de {message.sender_id}")
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem no NetworkManager: {e}")
            await self.publish_error_response(message, f"Erro interno: {str(e)}")

    async def _handle_network_status_request(self, message: AgentMessage):
        """Processa solicitação de status da rede."""
        try:
            status = self.network.get_network_status()
            await self.publish_response(message, {
                "type": "network_status_response",
                "network_status": status
            })
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao obter status: {str(e)}")

    async def _handle_agent_list_request(self, message: AgentMessage):
        """Processa solicitação de lista de agentes."""
        try:
            active_agents = self.network.get_active_agents()
            agent_details = {}
            
            for agent_id in active_agents:
                if agent_id in self.network.agent_registry:
                    info = self.network.agent_registry[agent_id]
                    agent_details[agent_id] = {
                        "type": str(info.get("type", "unknown")).split('.')[-1],
                        "status": info.get("status", "unknown"),
                        "capabilities": info.get("capabilities", [])
                    }
            
            await self.publish_response(message, {
                "type": "agent_list_response",
                "active_agents": active_agents,
                "agent_details": agent_details,
                "total_count": len(active_agents)
            })
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao obter lista: {str(e)}")

    async def _handle_diagnostics_request(self, message: AgentMessage):
        """Realiza diagnósticos da rede."""
        try:
            diagnostics = {
                "network_health": "healthy" if self.network.running else "offline",
                "message_bus_status": "operational" if self.network.message_bus.running else "offline",
                "agent_connectivity": await self._test_agent_connectivity(),
                "performance_metrics": self.network.message_bus.get_metrics(),
                "issues_detected": []
            }
            
            # Detecta problemas
            if self.network.stats.active_agents < self.network.stats.total_agents * 0.8:
                diagnostics["issues_detected"].append("Baixa conectividade de agentes")
                
            if not self.network.message_bus.running:
                diagnostics["issues_detected"].append("MessageBus offline")
            
            await self.publish_response(message, {
                "type": "diagnostics_response", 
                "diagnostics": diagnostics
            })
        except Exception as e:
            await self.publish_error_response(message, f"Erro em diagnósticos: {str(e)}")

    async def _handle_agent_discovery_request(self, message: AgentMessage):
        """Processa solicitação de descoberta de agentes por tipo."""
        try:
            requested_type = message.content.get("agent_type", "all")
            
            if requested_type == "all":
                agents = list(self.network.agents.keys())
            else:
                agents = self.network.get_agents_by_type(requested_type)
            
            await self.publish_response(message, {
                "type": "agent_discovery_response",
                "requested_type": requested_type,
                "found_agents": agents,
                "count": len(agents)
            })
        except Exception as e:
            await self.publish_error_response(message, f"Erro na descoberta: {str(e)}")

    async def _test_agent_connectivity(self) -> Dict[str, str]:
        """Testa conectividade básica dos agentes."""
        connectivity = {}
        
        for agent_id in self.network.agents.keys():
            if agent_id in self.network.connection_info:
                info = self.network.connection_info[agent_id]
                # Simples teste baseado no last_seen
                time_diff = (datetime.now() - info.last_seen).total_seconds()
                if time_diff < 60:
                    connectivity[agent_id] = "connected"
                elif time_diff < 300:
                    connectivity[agent_id] = "idle"
                else:
                    connectivity[agent_id] = "disconnected"
            else:
                connectivity[agent_id] = "unknown"
        
        return connectivity

def create_agents(message_bus: MessageBus) -> List[BaseNetworkAgent]:
    """
    Factory function para criar o NetworkManagerAgent.
    
    Args:
        message_bus (MessageBus): O message bus para comunicação.
        
    Returns:
        List[BaseNetworkAgent]: Lista contendo o NetworkManagerAgent.
    """
    agents: List[BaseNetworkAgent] = []
    
    try:
        logger.info("🌐 [Factory] Criando NetworkManagerAgent...")
        
        # Cria uma instância de rede para o agente gerenciar
        network = MultiAgentNetwork()
        network.message_bus = message_bus  # Usa o mesmo message_bus
        
        # Cria o agente gerenciador
        agent = NetworkManagerAgent(message_bus, network)
        agents.append(agent)
        
        logger.info(f"✅ NetworkManagerAgent criado: {agent.agent_id}")
        logger.info(f"🔧 Capabilities: {', '.join(agent.capabilities)}")
        
    except Exception as e:
        logger.critical(f"❌ Erro ao criar NetworkManagerAgent: {e}", exc_info=True)
    
    return agents

# Para compatibilidade e importações externas
__all__ = [
    'MessageType', 'Priority', 'AgentType', 'AgentMessage', 'MessageBus',
    'MultiAgentNetwork', 'BaseNetworkAgent', 'NetworkManagerAgent', 'create_agents'
]
