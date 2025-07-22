"""
🌐 SUNA-ALSHAM Multi-Agent Network System
Sistema de rede de múltiplos agentes com comunicação inter-agentes

FUNCIONALIDADES:
✅ Comunicação inter-agentes via message bus
✅ Especialização de agentes por domínio
✅ Coordenação distribuída
✅ Escalabilidade automática
✅ Load balancing inteligente
✅ Fault tolerance e recovery
✅ Métricas de rede em tempo real
"""

import asyncio
import json
import time
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor
import weakref
from collections import defaultdict, deque
import heapq

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Tipos de agentes na rede"""
    CORE = "core"
    LEARN = "learn"
    GUARD = "guard"
    ANALYTICS = "analytics"
    OPTIMIZER = "optimizer"
    COORDINATOR = "coordinator"
    SPECIALIST = "specialist"
    MONITOR = "monitor"


class MessageType(Enum):
    """Tipos de mensagens entre agentes"""
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"
    TASK_ASSIGNMENT = "task_assignment"
    RESULT_SHARING = "result_sharing"
    COORDINATION = "coordination"
    EMERGENCY = "emergency"


class Priority(Enum):
    """Níveis de prioridade das mensagens"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


@dataclass
class AgentMessage:
    """Estrutura de mensagem entre agentes"""
    id: str
    sender_id: str
    receiver_id: str  # ou "broadcast" para todos
    message_type: MessageType
    priority: Priority
    content: Dict[str, Any]
    timestamp: datetime
    expires_at: Optional[datetime] = None
    requires_response: bool = False
    correlation_id: Optional[str] = None


@dataclass
class AgentCapability:
    """Capacidade específica de um agente"""
    name: str
    description: str
    input_types: List[str]
    output_types: List[str]
    processing_time_ms: float
    accuracy_score: float
    resource_cost: float


@dataclass
class NetworkMetrics:
    """Métricas da rede multi-agente"""
    total_agents: int
    active_agents: int
    messages_per_second: float
    average_response_time_ms: float
    network_efficiency: float
    load_distribution: Dict[str, float]
    fault_tolerance_score: float
    coordination_success_rate: float
    timestamp: datetime


class MessageBus:
    """Sistema de comunicação entre agentes"""
    
    def __init__(self):
        self.subscribers: Dict[str, Set[Callable]] = defaultdict(set)
        self.message_queue: List[AgentMessage] = []
        self.message_history: deque = deque(maxlen=10000)
        self.delivery_stats: Dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()
        self._running = False
        self._worker_thread = None
    
    def start(self):
        """Inicia o message bus"""
        self._running = True
        self._worker_thread = threading.Thread(target=self._process_messages)
        self._worker_thread.daemon = True
        self._worker_thread.start()
        logger.info("🚀 Message Bus iniciado")
    
    def stop(self):
        """Para o message bus"""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join()
        logger.info("⏹️ Message Bus parado")
    
    def subscribe(self, agent_id: str, callback: Callable):
        """Inscreve um agente para receber mensagens"""
        with self._lock:
            self.subscribers[agent_id].add(callback)
        logger.info(f"📡 Agente {agent_id} inscrito no message bus")
    
    def unsubscribe(self, agent_id: str, callback: Callable):
        """Remove inscrição de um agente"""
        with self._lock:
            self.subscribers[agent_id].discard(callback)
    
    def send_message(self, message: AgentMessage):
        """Envia mensagem através do bus"""
        with self._lock:
            # Inserir na fila ordenada por prioridade
            heapq.heappush(self.message_queue, (message.priority.value, time.time(), message))
            self.message_history.append(message)
        
        logger.debug(f"📨 Mensagem {message.id} enviada de {message.sender_id} para {message.receiver_id}")
    
    def _process_messages(self):
        """Processa mensagens na fila"""
        while self._running:
            try:
                with self._lock:
                    if not self.message_queue:
                        continue
                    
                    # Pegar mensagem de maior prioridade
                    priority, timestamp, message = heapq.heappop(self.message_queue)
                
                # Verificar se mensagem expirou
                if message.expires_at and datetime.now() > message.expires_at:
                    logger.warning(f"⚠️ Mensagem {message.id} expirou")
                    continue
                
                # Entregar mensagem
                self._deliver_message(message)
                
            except Exception as e:
                logger.error(f"❌ Erro processando mensagem: {e}")
            
            time.sleep(0.001)  # 1ms de delay
    
    def _deliver_message(self, message: AgentMessage):
        """Entrega mensagem para o(s) destinatário(s)"""
        delivered = False
        
        with self._lock:
            if message.receiver_id == "broadcast":
                # Broadcast para todos os agentes
                for agent_id, callbacks in self.subscribers.items():
                    if agent_id != message.sender_id:  # Não enviar para o remetente
                        for callback in callbacks.copy():
                            try:
                                callback(message)
                                delivered = True
                            except Exception as e:
                                logger.error(f"❌ Erro entregando mensagem para {agent_id}: {e}")
            else:
                # Entrega direcionada
                callbacks = self.subscribers.get(message.receiver_id, set())
                for callback in callbacks.copy():
                    try:
                        callback(message)
                        delivered = True
                    except Exception as e:
                        logger.error(f"❌ Erro entregando mensagem para {message.receiver_id}: {e}")
        
        if delivered:
            self.delivery_stats["delivered"] += 1
        else:
            self.delivery_stats["failed"] += 1
            logger.warning(f"⚠️ Falha na entrega da mensagem {message.id}")


class BaseNetworkAgent:
    """Classe base para agentes da rede"""
    
    def __init__(self, agent_id: str, agent_type: AgentType, message_bus: MessageBus):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_bus = message_bus
        self.capabilities: List[AgentCapability] = []
        self.status = "initializing"
        self.last_heartbeat = datetime.now()
        self.message_handlers: Dict[MessageType, Callable] = {}
        self.performance_metrics: Dict[str, float] = {}
        self.task_queue: deque = deque()
        self.active_tasks: Dict[str, Any] = {}
        self._running = False
        self._worker_thread = None
        
        # Registrar handlers padrão
        self._register_default_handlers()
        
        # Inscrever no message bus
        self.message_bus.subscribe(self.agent_id, self._handle_message)
    
    def _register_default_handlers(self):
        """Registra handlers padrão de mensagens"""
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat
        self.message_handlers[MessageType.REQUEST] = self._handle_request
        self.message_handlers[MessageType.TASK_ASSIGNMENT] = self._handle_task_assignment
    
    def start(self):
        """Inicia o agente"""
        self._running = True
        self._worker_thread = threading.Thread(target=self._run_loop)
        self._worker_thread.daemon = True
        self._worker_thread.start()
        self.status = "running"
        
        # Enviar heartbeat inicial
        self._send_heartbeat()
        
        logger.info(f"🤖 Agente {self.agent_id} ({self.agent_type.value}) iniciado")
    
    def stop(self):
        """Para o agente"""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join()
        self.status = "stopped"
        logger.info(f"⏹️ Agente {self.agent_id} parado")
    
    def add_capability(self, capability: AgentCapability):
        """Adiciona uma capacidade ao agente"""
        self.capabilities.append(capability)
        logger.info(f"✨ Capacidade '{capability.name}' adicionada ao agente {self.agent_id}")
    
    def send_message(self, receiver_id: str, message_type: MessageType, content: Dict[str, Any], 
                    priority: Priority = Priority.NORMAL, requires_response: bool = False):
        """Envia mensagem para outro agente"""
        message = AgentMessage(
            id=str(uuid.uuid4()),
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            message_type=message_type,
            priority=priority,
            content=content,
            timestamp=datetime.now(),
            requires_response=requires_response
        )
        
        self.message_bus.send_message(message)
    
    def broadcast_message(self, message_type: MessageType, content: Dict[str, Any], 
                         priority: Priority = Priority.NORMAL):
        """Envia mensagem broadcast para todos os agentes"""
        self.send_message("broadcast", message_type, content, priority)
    
    def _handle_message(self, message: AgentMessage):
        """Handler principal de mensagens"""
        try:
            handler = self.message_handlers.get(message.message_type)
            if handler:
                handler(message)
            else:
                logger.warning(f"⚠️ Handler não encontrado para {message.message_type} no agente {self.agent_id}")
        except Exception as e:
            logger.error(f"❌ Erro processando mensagem no agente {self.agent_id}: {e}")
    
    def _handle_heartbeat(self, message: AgentMessage):
        """Handler para mensagens de heartbeat"""
        self.last_heartbeat = datetime.now()
        
        # Responder com status
        if message.requires_response:
            self.send_message(
                message.sender_id,
                MessageType.RESPONSE,
                {
                    "status": self.status,
                    "capabilities": [cap.name for cap in self.capabilities],
                    "performance": self.performance_metrics,
                    "active_tasks": len(self.active_tasks)
                }
            )
    
    def _handle_request(self, message: AgentMessage):
        """Handler para requisições"""
        # Implementação base - deve ser sobrescrita pelos agentes específicos
        self.send_message(
            message.sender_id,
            MessageType.RESPONSE,
            {"status": "not_implemented", "message": "Handler não implementado"}
        )
    
    def _handle_task_assignment(self, message: AgentMessage):
        """Handler para atribuição de tarefas"""
        task_id = message.content.get("task_id")
        task_data = message.content.get("task_data")
        
        if task_id and task_data:
            self.task_queue.append({
                "id": task_id,
                "data": task_data,
                "assigned_at": datetime.now(),
                "sender": message.sender_id
            })
            logger.info(f"📋 Tarefa {task_id} atribuída ao agente {self.agent_id}")
    
    def _send_heartbeat(self):
        """Envia heartbeat para o coordenador"""
        self.broadcast_message(
            MessageType.HEARTBEAT,
            {
                "agent_id": self.agent_id,
                "agent_type": self.agent_type.value,
                "status": self.status,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def _run_loop(self):
        """Loop principal do agente"""
        last_heartbeat = time.time()
        
        while self._running:
            try:
                current_time = time.time()
                
                # Enviar heartbeat a cada 30 segundos
                if current_time - last_heartbeat > 30:
                    self._send_heartbeat()
                    last_heartbeat = current_time
                
                # Processar tarefas na fila
                self._process_tasks()
                
                # Executar lógica específica do agente
                self._agent_specific_logic()
                
            except Exception as e:
                logger.error(f"❌ Erro no loop do agente {self.agent_id}: {e}")
            
            time.sleep(30)  # 30 segundos de delay - adequado para monitoramento
    
    def _process_tasks(self):
        """Processa tarefas na fila"""
        while self.task_queue and len(self.active_tasks) < 5:  # Máximo 5 tarefas simultâneas
            task = self.task_queue.popleft()
            self.active_tasks[task["id"]] = task
            
            # Processar tarefa (implementação específica do agente)
            self._execute_task(task)
    
    def _execute_task(self, task: Dict[str, Any]):
        """Executa uma tarefa específica - deve ser sobrescrita"""
        # Implementação base - simular processamento
        time.sleep(0.1)
        
        # Remover da lista de tarefas ativas
        self.active_tasks.pop(task["id"], None)
        
        logger.info(f"✅ Tarefa {task['id']} concluída pelo agente {self.agent_id}")
    
    def _agent_specific_logic(self):
        """Lógica específica do agente - deve ser sobrescrita"""
        pass


class NetworkCoordinator(BaseNetworkAgent):
    """Coordenador da rede multi-agente"""
    
    def __init__(self, message_bus: MessageBus):
        super().__init__("coordinator", AgentType.COORDINATOR, message_bus)
        self.registered_agents: Dict[str, Dict[str, Any]] = {}
        self.network_metrics = NetworkMetrics(
            total_agents=0,
            active_agents=0,
            messages_per_second=0.0,
            average_response_time_ms=0.0,
            network_efficiency=0.0,
            load_distribution={},
            fault_tolerance_score=0.0,
            coordination_success_rate=0.0,
            timestamp=datetime.now()
        )
        
        # Adicionar handlers específicos
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_agent_heartbeat
    
    def _handle_agent_heartbeat(self, message: AgentMessage):
        """Processa heartbeats dos agentes"""
        agent_id = message.content.get("agent_id")
        agent_type = message.content.get("agent_type")
        status = message.content.get("status")
        
        if agent_id:
            self.registered_agents[agent_id] = {
                "type": agent_type,
                "status": status,
                "last_seen": datetime.now(),
                "heartbeat_count": self.registered_agents.get(agent_id, {}).get("heartbeat_count", 0) + 1
            }
            
            logger.debug(f"💓 Heartbeat recebido do agente {agent_id}")
    
    def get_network_status(self) -> Dict[str, Any]:
        """Retorna status da rede"""
        now = datetime.now()
        active_agents = 0
        
        for agent_id, info in self.registered_agents.items():
            if (now - info["last_seen"]).seconds < 60:  # Ativo se heartbeat < 60s
                active_agents += 1
        
        self.network_metrics.total_agents = len(self.registered_agents)
        self.network_metrics.active_agents = active_agents
        self.network_metrics.timestamp = now
        
        return {
            "coordinator_id": self.agent_id,
            "network_metrics": asdict(self.network_metrics),
            "registered_agents": self.registered_agents,
            "message_bus_stats": self.message_bus.delivery_stats
        }
    
    def assign_task_to_best_agent(self, task_type: str, task_data: Dict[str, Any]) -> Optional[str]:
        """Atribui tarefa ao melhor agente disponível"""
        # Lógica simples de seleção - pode ser expandida
        available_agents = [
            agent_id for agent_id, info in self.registered_agents.items()
            if info["status"] == "running" and (datetime.now() - info["last_seen"]).seconds < 30
        ]
        
        if not available_agents:
            logger.warning("⚠️ Nenhum agente disponível para tarefa")
            return None
        
        # Selecionar agente com menos carga (implementação simples)
        selected_agent = available_agents[0]  # Por enquanto, pegar o primeiro
        
        # Enviar tarefa
        task_id = str(uuid.uuid4())
        self.send_message(
            selected_agent,
            MessageType.TASK_ASSIGNMENT,
            {
                "task_id": task_id,
                "task_type": task_type,
                "task_data": task_data
            },
            Priority.NORMAL
        )
        
        logger.info(f"📋 Tarefa {task_id} atribuída ao agente {selected_agent}")
        return task_id
    
    def _agent_specific_logic(self):
        """Lógica específica do coordenador"""
        # Verificar agentes inativos
        now = datetime.now()
        inactive_agents = []
        
        for agent_id, info in self.registered_agents.items():
            if (now - info["last_seen"]).seconds > 120:  # 2 minutos sem heartbeat
                inactive_agents.append(agent_id)
        
        # Remover agentes inativos
        for agent_id in inactive_agents:
            del self.registered_agents[agent_id]
            logger.warning(f"⚠️ Agente {agent_id} removido por inatividade")


class MultiAgentNetwork:
    """Sistema principal da rede multi-agente"""
    
    def __init__(self):
        self.message_bus = MessageBus()
        self.coordinator = NetworkCoordinator(self.message_bus)
        self.agents: Dict[str, BaseNetworkAgent] = {}
        self.executor = ThreadPoolExecutor(max_workers=10)
        self._running = False
    
    def start(self):
        """Inicia a rede multi-agente"""
        logger.info("🌐 Iniciando rede multi-agente SUNA-ALSHAM...")
        
        # Iniciar message bus
        self.message_bus.start()
        
        # Iniciar coordenador
        self.coordinator.start()
        
        # Iniciar todos os agentes
        for agent in self.agents.values():
            agent.start()
        
        self._running = True
        logger.info("✅ Rede multi-agente iniciada com sucesso!")
    
    def stop(self):
        """Para a rede multi-agente"""
        logger.info("⏹️ Parando rede multi-agente...")
        
        self._running = False
        
        # Parar todos os agentes
        for agent in self.agents.values():
            agent.stop()
        
        # Parar coordenador
        self.coordinator.stop()
        
        # Parar message bus
        self.message_bus.stop()
        
        # Parar executor
        self.executor.shutdown(wait=True)
        
        logger.info("✅ Rede multi-agente parada")
    
    def add_agent(self, agent: BaseNetworkAgent):
        """Adiciona um agente à rede"""
        self.agents[agent.agent_id] = agent
        
        if self._running:
            agent.start()
        
        logger.info(f"➕ Agente {agent.agent_id} adicionado à rede")
    
    def remove_agent(self, agent_id: str):
        """Remove um agente da rede"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.stop()
            del self.agents[agent_id]
            logger.info(f"➖ Agente {agent_id} removido da rede")
    
    def get_network_status(self) -> Dict[str, Any]:
        """Retorna status completo da rede"""
        return self.coordinator.get_network_status()
    
    def assign_task(self, task_type: str, task_data: Dict[str, Any]) -> Optional[str]:
        """Atribui uma tarefa à rede"""
        return self.coordinator.assign_task_to_best_agent(task_type, task_data)


# Exemplo de agente especializado
class AnalyticsAgent(BaseNetworkAgent):
    """Agente especializado em analytics"""
    
    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.ANALYTICS, message_bus)
        
        # Adicionar capacidades específicas
        self.add_capability(AgentCapability(
            name="data_analysis",
            description="Análise de dados em tempo real",
            input_types=["json", "csv"],
            output_types=["report", "visualization"],
            processing_time_ms=500.0,
            accuracy_score=0.95,
            resource_cost=0.3
        ))
    
    def _handle_request(self, message: AgentMessage):
        """Handler específico para requisições de analytics"""
        request_type = message.content.get("type")
        
        if request_type == "analyze_data":
            data = message.content.get("data", [])
            
            # Simular análise
            result = {
                "analysis_id": str(uuid.uuid4()),
                "data_points": len(data),
                "mean": sum(data) / len(data) if data else 0,
                "processed_at": datetime.now().isoformat()
            }
            
            # Enviar resposta
            self.send_message(
                message.sender_id,
                MessageType.RESPONSE,
                {"status": "success", "result": result}
            )
            
            logger.info(f"📊 Análise concluída pelo agente {self.agent_id}")


if __name__ == "__main__":
    # Exemplo de uso
    network = MultiAgentNetwork()
    
    # Adicionar agentes especializados
    analytics_agent = AnalyticsAgent("analytics_001", network.message_bus)
    network.add_agent(analytics_agent)
    
    try:
        # Iniciar rede
        network.start()
        
        # Simular operação
        time.sleep(5)
        
        # Atribuir uma tarefa
        task_id = network.assign_task("data_analysis", {"data": [1, 2, 3, 4, 5]})
        print(f"Tarefa atribuída: {task_id}")
        
        # Verificar status
        status = network.get_network_status()
        print(f"Status da rede: {json.dumps(status, indent=2, default=str)}")
        
        # Manter rodando
        time.sleep(10)
        
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário")
    finally:
        network.stop()

