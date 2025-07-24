import asyncio
import json
import time
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentType(Enum):
    CORE = "core"
    LEARN = "learn"
    GUARD = "guard"
    ANALYTICS = "analytics"
    OPTIMIZER = "optimizer"
    COORDINATOR = "coordinator"
    SPECIALIST = "specialist"
    MONITOR = "monitor"
    EVOLVER = "evolver"
    INTEGRATOR = "integrator"
    PREDICTOR = "predictor"
    AUTOMATOR = "automator"
    SPECIALIZED = "specialized"
    AI_POWERED = "ai_powered"
    SYSTEM = "system"
    SERVICE = "service"
    META_COGNITIVE = "meta_cognitive"
    ORCHESTRATOR = "orchestrator"
    CONVERSATIONAL = "conversational"

class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"
    TASK_ASSIGNMENT = "task_assignment"
    RESULT_SHARING = "result_sharing"
    COORDINATION = "coordination"
    EMERGENCY = "emergency"
    COMPLIANCE_CHECK = "compliance_check"
    USER_FEEDBACK = "user_feedback"
    PREDICTION_REQUEST = "prediction_request"

class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class AgentCapability:
    name: str
    description: str
    input_types: List[str]
    output_types: List[str]
    processing_time_ms: float
    accuracy_score: float
    resource_cost: float

@dataclass
class AgentMessage:
    id: str
    sender_id: str
    recipient_id: str
    message_type: MessageType
    priority: Priority
    content: Dict[str, Any]
    timestamp: datetime
    ttl: Optional[datetime] = None
    correlation_id: Optional[str] = None

class MessageBus:
    def __init__(self):
        self.subscribers = {}
        self.message_queue = asyncio.Queue()
        self.priority_queues = {
            Priority.CRITICAL: asyncio.Queue(),
            Priority.HIGH: asyncio.Queue(),
            Priority.MEDIUM: asyncio.Queue(),
            Priority.LOW: asyncio.Queue()
        }
        self.running = False
        self.metrics = {
            'messages_sent': 0,
            'messages_delivered': 0,
            'messages_failed': 0,
            'average_latency': 0.0
        }
        logger.info("✅ MessageBus inicializado com compatibilidade total")

    def subscribe(self, agent_id: str, agent: Any):
        try:
            self.subscribers[agent_id] = agent
            logger.info(f"📡 Agente {agent_id} inscrito no MessageBus")
            return True
        except Exception as e:
            logger.error(f"❌ Erro inscrevendo agente {agent_id}: {e}")
            return False

    def register_agent(self, agent_id: str, agent: Any):
        try:
            self.subscribers[agent_id] = agent
            logger.info(f"✅ Agente {agent_id} registrado no MessageBus via register_agent")
            return True
        except Exception as e:
            logger.error(f"❌ Erro registrando agente {agent_id}: {e}")
            return False

    async def publish(self, message: AgentMessage):
        try:
            start_time = time.time()
            self.metrics['messages_sent'] += 1
            await self.priority_queues[message.priority].put(message)
            await self._process_message(message)
            latency = (time.time() - start_time) * 1000
            self.metrics['average_latency'] = (
                (self.metrics['average_latency'] * (self.metrics['messages_sent'] - 1) + latency) 
                / self.metrics['messages_sent']
            )
            logger.info(f"📤 Mensagem {message.id} publicada com sucesso")
        except Exception as e:
            self.metrics['messages_failed'] += 1
            logger.error(f"❌ Falha publicando mensagem {message.id}: {e}")

    async def _process_message(self, message: AgentMessage):
        try:
            if message.recipient_id == "broadcast":
                for agent_id, agent in self.subscribers.items():
                    if agent_id != message.sender_id:
                        await self._deliver_message(message, agent_id, agent)
            else:
                if message.recipient_id in self.subscribers:
                    agent = self.subscribers[message.recipient_id]
                    await self._deliver_message(message, message.recipient_id, agent)
                else:
                    logger.warning(f"⚠️ Destinatário {message.recipient_id} não encontrado")
                    self.metrics['messages_failed'] += 1
        except Exception as e:
            logger.error(f"❌ Erro processando mensagem {message.id}: {e}")
            self.metrics['messages_failed'] += 1

    async def _deliver_message(self, message: AgentMessage, agent_id: str, agent: Any):
        try:
            if hasattr(agent, 'handle_message'):
                await agent.handle_message(message)
                self.metrics['messages_delivered'] += 1
                logger.info(f"✅ Mensagem {message.id} entregue para {agent_id}")
            else:
                logger.warning(f"⚠️ Agente {agent_id} não tem método handle_message")
                self.metrics['messages_failed'] += 1
        except Exception as e:
            logger.error(f"❌ Falha entregando mensagem {message.id} para {agent_id}: {e}")
            self.metrics['messages_failed'] += 1

    def get_metrics(self) -> Dict[str, Any]:
        return {
            'subscribers_count': len(self.subscribers),
            'messages_sent': self.metrics['messages_sent'],
            'messages_delivered': self.metrics['messages_delivered'],
            'messages_failed': self.metrics['messages_failed'],
            'average_latency_ms': round(self.metrics['average_latency'], 2),
            'success_rate': (
                self.metrics['messages_delivered'] / max(self.metrics['messages_sent'], 1) * 100
            )
        }

class BaseNetworkAgent:
    def __init__(self, agent_id: str, agent_type: AgentType, message_bus: MessageBus):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_bus = message_bus
        self.status = "active"
        self.capabilities = []
        self.performance_metrics = {
            'messages_processed': 0,
            'tasks_completed': 0,
            'average_response_time': 0.0,
            'success_rate': 1.0
        }
        self.created_at = datetime.now()
        if message_bus:
            message_bus.register_agent(self.agent_id, self)
        logger.info(f"🤖 Agente {agent_id} inicializado como {agent_type.value}")

    def add_capability(self, capability: AgentCapability):
        self.capabilities.append(capability)
        logger.info(f"✨ Capacidade '{capability.name}' adicionada ao agente {self.agent_id}")

    async def handle_message(self, message: AgentMessage):
        try:
            start_time = time.time()
            logger.info(f"📩 {self.agent_id} processando mensagem {message.id} de {message.sender_id}")
            if message.message_type == MessageType.REQUEST:
                await self._handle_request(message)
            elif message.message_type == MessageType.HEARTBEAT:
                await self._handle_heartbeat(message)
            elif message.message_type == MessageType.TASK_ASSIGNMENT:
                await self._handle_task_assignment(message)
            else:
                await self._handle_generic_message(message)
            response_time = (time.time() - start_time) * 1000
            self.performance_metrics['messages_processed'] += 1
            self.performance_metrics['average_response_time'] = (
                (self.performance_metrics['average_response_time'] * 
                 (self.performance_metrics['messages_processed'] - 1) + response_time) 
                / self.performance_metrics['messages_processed']
            )
            self.performance_metrics['success_rate'] = (
                self.performance_metrics['tasks_completed'] / 
                max(self.performance_metrics['messages_processed'], 1)
            ) if self.performance_metrics['messages_processed'] > 0 else 1.0
        except Exception as e:
            logger.error(f"❌ Erro processando mensagem em {self.agent_id}: {e}")

    async def receive_message(self, message: AgentMessage):
        await self.handle_message(message)

    async def _handle_request(self, message: AgentMessage):
        response = AgentMessage(
            id=str(uuid.uuid4()),
            sender_id=self.agent_id,
            recipient_id=message.sender_id,
            message_type=MessageType.RESPONSE,
            priority=message.priority,
            content={"status": "processed", "original_request": message.id},
            timestamp=datetime.now(),
            correlation_id=message.id
        )
        await self.message_bus.publish(response)

    async def _handle_heartbeat(self, message: AgentMessage):
        logger.info(f"💓 {self.agent_id} recebeu heartbeat de {message.sender_id}")

    async def _handle_task_assignment(self, message: AgentMessage):
        logger.info(f"📋 {self.agent_id} recebeu tarefa: {message.content}")
        self.performance_metrics['tasks_completed'] += 1

    async def _handle_generic_message(self, message: AgentMessage):
        logger.info(f"📨 {self.agent_id} processou mensagem genérica: {message.message_type.value}")

    def send_message(self, recipient_id: str, message_type: MessageType, content: Dict[str, Any], priority: Priority = Priority.MEDIUM):
        message = AgentMessage(
            id=str(uuid.uuid4()),
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            message_type=message_type,
            priority=priority,
            content=content,
            timestamp=datetime.now()
        )
        asyncio.create_task(self.message_bus.publish(message))

    def get_status(self) -> Dict[str, Any]:
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type.value,
            'status': self.status,
            'capabilities_count': len(self.capabilities),
            'performance_metrics': self.performance_metrics,
            'created_at': self.created_at.isoformat()
        }

class NetworkCoordinator:
    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus
        self.agents = {}
        self.load_balancer = {}
        self.health_monitor = {}
        self.running = False
    
    def register_agent(self, agent: BaseNetworkAgent):
        self.agents[agent.agent_id] = agent
        self.load_balancer[agent.agent_id] = 0
        self.health_monitor[agent.agent_id] = {
            'last_heartbeat': datetime.now(),
            'status': 'healthy'
        }
        logger.info(f"✅ Agente {agent.agent_id} registrado no coordenador")

    async def start_coordination(self):
        self.running = True
        logger.info("🎯 Coordenação de rede iniciada")
        asyncio.create_task(self._health_check_loop())
        asyncio.create_task(self._load_balancing_loop())

    async def _health_check_loop(self):
        while self.running:
            try:
                for agent_id in self.agents:
                    heartbeat = AgentMessage(
                        id=str(uuid.uuid4()),
                        sender_id="coordinator",
                        recipient_id=agent_id,
                        message_type=MessageType.HEARTBEAT,
                        priority=Priority.LOW,
                        content={"timestamp": datetime.now().isoformat()},
                        timestamp=datetime.now()
                    )
                    await self.message_bus.publish(heartbeat)
                await asyncio.sleep(30)
            except Exception as e:
                logger.error(f"❌ Erro no health check: {e}")

    async def _load_balancing_loop(self):
        while self.running:
            try:
                for agent_id, agent in self.agents.items():
                    if hasattr(agent, 'performance_metrics'):
                        self.load_balancer[agent_id] = agent.performance_metrics.get('messages_processed', 0)
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"❌ Erro no load balancing: {e}")

class MultiAgentNetwork:
    def __init__(self):
        self.message_bus = MessageBus()
        self.coordinator = NetworkCoordinator(self.message_bus)
        self.agents = {}
        self._running = False
        self.metrics_update_interval = 10
        self.last_metrics_update = time.time()
        logger.info("🌐 MultiAgentNetwork inicializada - VERSÃO FINAL")

    async def initialize(self):
        try:
            self._running = True
            await self.coordinator.start_coordination()
            asyncio.create_task(self._metrics_update_loop())
            logger.info("✅ MultiAgentNetwork inicializada com sucesso - SEM FALLBACK")
            return True
        except Exception as e:
            logger.error(f"❌ Erro inicializando MultiAgentNetwork: {e}")
            self._running = False
            return False

    def add_agent(self, agent):
        try:
            if hasattr(agent, 'agent_id'):
                agent_id = agent.agent_id
                self.agents[agent_id] = agent
                if agent_id not in self.message_bus.subscribers:
                    self.message_bus.register_agent(agent_id, agent)
                if isinstance(agent, BaseNetworkAgent):
                    self.coordinator.register_agent(agent)
                logger.info(f"✅ Agente {agent_id} adicionado à rede MultiAgentNetwork")
                return True
            else:
                logger.error(f"❌ Agente sem agent_id não pode ser adicionado: {agent}")
                return False
        except Exception as e:
            logger.error(f"❌ Erro adicionando agente à rede: {e}")
            return False

    async def _metrics_update_loop(self):
        while self._running:
            try:
                current_time = time.time()
                if current_time - self.last_metrics_update >= self.metrics_update_interval:
                    active_agents = len([a for a in self.agents.values() if getattr(a, 'status', 'inactive') == 'active'])
                    logger.info(f"📊 Métricas da rede atualizadas: {active_agents} agentes ativos")
                    self.last_metrics_update = current_time
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"❌ Erro no loop de métricas: {e}")

    def get_network_status(self) -> Dict[str, Any]:
        try:
            active_agents = len([a for a in self.agents.values() if getattr(a, 'status', 'inactive') == 'active'])
            return {
                'network_running': self._running,
                'total_agents': len(self.agents),
                'active_agents': active_agents,
                'message_bus_metrics': self.message_bus.get_metrics(),
                'agents': {agent_id: agent.get_status() if hasattr(agent, 'get_status') else {'status': 'unknown'} 
                          for agent_id, agent in self.agents.items()}
            }
        except Exception as e:
            logger.error(f"❌ Erro obtendo status da rede: {e}")
            return {'error': str(e)}

    def stop(self):
        try:
            self._running = False
            self.coordinator.running = False
            logger.info("🛑 MultiAgentNetwork parada")
        except Exception as e:
            logger.error(f"❌ Erro parando rede: {e}")

def create_network() -> MultiAgentNetwork:
    return MultiAgentNetwork()

if __name__ == "__main__":
    async def test_network():
        network = MultiAgentNetwork()
        await network.initialize()
        test_agent = BaseNetworkAgent("test_001", AgentType.CORE, network.message_bus)
        network.add_agent(test_agent)
        await asyncio.sleep(15)
        status = network.get_network_status()
        logger.info(f"Status da rede: {json.dumps(status, indent=2)}")
        network.stop()
    asyncio.run(test_network())
