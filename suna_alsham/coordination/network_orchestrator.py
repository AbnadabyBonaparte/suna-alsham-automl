"""
🎼 SUNA-ALSHAM Network Orchestrator
Orquestrador avançado para coordenação da rede multi-agente

FUNCIONALIDADES:
✅ Coordenação inteligente de agentes
✅ Load balancing automático
✅ Fault tolerance e recovery
✅ Scaling automático baseado em carga
✅ Otimização de recursos
✅ Monitoramento em tempo real
✅ API REST para controle externo
✅ WebSocket para updates em tempo real
"""

import asyncio
import json
import time
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics
import heapq

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from multi_agent_network import (
    MultiAgentNetwork, BaseNetworkAgent, AgentType, MessageType, 
    Priority, NetworkMetrics
)
from specialized_agents import (
    OptimizationAgent, SecurityAgent, LearningAgent, 
    DataAgent, MonitoringAgent
)

logger = logging.getLogger(__name__)


@dataclass
class TaskRequest:
    """Requisição de tarefa para a rede"""
    id: str
    type: str
    priority: Priority
    data: Dict[str, Any]
    requester: str
    created_at: datetime
    deadline: Optional[datetime] = None
    required_capabilities: List[str] = None
    estimated_duration: Optional[float] = None


@dataclass
class AgentLoad:
    """Carga atual de um agente"""
    agent_id: str
    active_tasks: int
    queue_size: int
    cpu_usage: float
    memory_usage: float
    response_time_avg: float
    success_rate: float
    last_updated: datetime


@dataclass
class NetworkHealth:
    """Saúde geral da rede"""
    overall_score: float
    active_agents: int
    total_agents: int
    average_load: float
    response_time_p95: float
    error_rate: float
    uptime_percentage: float
    last_incident: Optional[datetime]


class LoadBalancer:
    """Sistema de balanceamento de carga inteligente"""
    
    def __init__(self):
        self.agent_loads: Dict[str, AgentLoad] = {}
        self.task_history: deque = deque(maxlen=1000)
        self.performance_weights = {
            "active_tasks": 0.3,
            "queue_size": 0.2,
            "cpu_usage": 0.2,
            "memory_usage": 0.15,
            "response_time": 0.1,
            "success_rate": 0.05
        }
    
    def update_agent_load(self, agent_id: str, load_data: Dict[str, Any]):
        """Atualiza informações de carga de um agente"""
        self.agent_loads[agent_id] = AgentLoad(
            agent_id=agent_id,
            active_tasks=load_data.get("active_tasks", 0),
            queue_size=load_data.get("queue_size", 0),
            cpu_usage=load_data.get("cpu_usage", 0.0),
            memory_usage=load_data.get("memory_usage", 0.0),
            response_time_avg=load_data.get("response_time_avg", 0.0),
            success_rate=load_data.get("success_rate", 1.0),
            last_updated=datetime.now()
        )
    
    def select_best_agent(self, task: TaskRequest, available_agents: List[str]) -> Optional[str]:
        """Seleciona o melhor agente para uma tarefa"""
        if not available_agents:
            return None
        
        agent_scores = {}
        
        for agent_id in available_agents:
            load = self.agent_loads.get(agent_id)
            if not load:
                # Agente sem dados de carga - assumir carga baixa
                agent_scores[agent_id] = 0.8
                continue
            
            # Calcular score baseado na carga (menor é melhor)
            score = 1.0
            
            # Penalizar por tarefas ativas
            score -= (load.active_tasks / 10) * self.performance_weights["active_tasks"]
            
            # Penalizar por fila
            score -= (load.queue_size / 20) * self.performance_weights["queue_size"]
            
            # Penalizar por uso de CPU
            score -= (load.cpu_usage / 100) * self.performance_weights["cpu_usage"]
            
            # Penalizar por uso de memória
            score -= (load.memory_usage / 100) * self.performance_weights["memory_usage"]
            
            # Penalizar por tempo de resposta
            score -= min(load.response_time_avg / 1000, 1.0) * self.performance_weights["response_time"]
            
            # Bonificar por taxa de sucesso
            score += load.success_rate * self.performance_weights["success_rate"]
            
            agent_scores[agent_id] = max(0.0, score)
        
        # Selecionar agente com melhor score
        best_agent = max(agent_scores.items(), key=lambda x: x[1])
        return best_agent[0]
    
    def get_load_distribution(self) -> Dict[str, float]:
        """Retorna distribuição de carga atual"""
        if not self.agent_loads:
            return {}
        
        distribution = {}
        for agent_id, load in self.agent_loads.items():
            # Calcular carga normalizada (0-1)
            load_score = (
                (load.active_tasks / 10) * 0.4 +
                (load.queue_size / 20) * 0.3 +
                (load.cpu_usage / 100) * 0.3
            )
            distribution[agent_id] = min(1.0, load_score)
        
        return distribution


class FaultTolerance:
    """Sistema de tolerância a falhas"""
    
    def __init__(self):
        self.failed_agents: Dict[str, datetime] = {}
        self.recovery_attempts: Dict[str, int] = defaultdict(int)
        self.circuit_breakers: Dict[str, Dict] = {}
        self.max_recovery_attempts = 3
        self.circuit_breaker_threshold = 5
        self.circuit_breaker_timeout = 300  # 5 minutos
    
    def mark_agent_failed(self, agent_id: str, error: str):
        """Marca um agente como falho"""
        self.failed_agents[agent_id] = datetime.now()
        self.recovery_attempts[agent_id] += 1
        
        logger.error(f"❌ Agente {agent_id} marcado como falho: {error}")
        
        # Verificar circuit breaker
        if self.recovery_attempts[agent_id] >= self.circuit_breaker_threshold:
            self.circuit_breakers[agent_id] = {
                "opened_at": datetime.now(),
                "reason": f"Too many failures: {self.recovery_attempts[agent_id]}"
            }
            logger.warning(f"🔌 Circuit breaker ativado para agente {agent_id}")
    
    def is_agent_available(self, agent_id: str) -> bool:
        """Verifica se um agente está disponível"""
        # Verificar circuit breaker
        if agent_id in self.circuit_breakers:
            breaker = self.circuit_breakers[agent_id]
            if (datetime.now() - breaker["opened_at"]).seconds < self.circuit_breaker_timeout:
                return False
            else:
                # Timeout expirou, remover circuit breaker
                del self.circuit_breakers[agent_id]
                self.recovery_attempts[agent_id] = 0
                logger.info(f"🔌 Circuit breaker removido para agente {agent_id}")
        
        # Verificar se está na lista de falhos
        if agent_id in self.failed_agents:
            failed_at = self.failed_agents[agent_id]
            if (datetime.now() - failed_at).seconds < 60:  # 1 minuto de cooldown
                return False
            else:
                # Remover da lista de falhos
                del self.failed_agents[agent_id]
        
        return True
    
    def mark_agent_recovered(self, agent_id: str):
        """Marca um agente como recuperado"""
        self.failed_agents.pop(agent_id, None)
        self.recovery_attempts[agent_id] = 0
        self.circuit_breakers.pop(agent_id, None)
        
        logger.info(f"✅ Agente {agent_id} marcado como recuperado")
    
    def get_fault_summary(self) -> Dict[str, Any]:
        """Retorna resumo de falhas"""
        return {
            "failed_agents": len(self.failed_agents),
            "circuit_breakers_active": len(self.circuit_breakers),
            "total_recovery_attempts": sum(self.recovery_attempts.values()),
            "failed_agent_details": {
                agent_id: {
                    "failed_at": failed_at.isoformat(),
                    "recovery_attempts": self.recovery_attempts[agent_id]
                }
                for agent_id, failed_at in self.failed_agents.items()
            }
        }


class AutoScaler:
    """Sistema de auto-scaling da rede"""
    
    def __init__(self, network: MultiAgentNetwork):
        self.network = network
        self.scaling_history: List[Dict] = []
        self.min_agents_per_type = {
            AgentType.OPTIMIZER: 1,
            AgentType.GUARD: 1,
            AgentType.LEARN: 1,
            AgentType.SPECIALIST: 2,
            AgentType.MONITOR: 1
        }
        self.max_agents_per_type = {
            AgentType.OPTIMIZER: 3,
            AgentType.GUARD: 2,
            AgentType.LEARN: 3,
            AgentType.SPECIALIST: 5,
            AgentType.MONITOR: 2
        }
    
    def evaluate_scaling_need(self, load_distribution: Dict[str, float], 
                            network_metrics: NetworkMetrics) -> List[Dict[str, Any]]:
        """Avalia necessidade de scaling"""
        scaling_actions = []
        
        # Analisar carga por tipo de agente
        agent_types_load = defaultdict(list)
        for agent_id, load in load_distribution.items():
            # Assumir que podemos determinar o tipo do agente pelo ID
            agent_type = self._get_agent_type_from_id(agent_id)
            if agent_type:
                agent_types_load[agent_type].append(load)
        
        # Verificar cada tipo de agente
        for agent_type, loads in agent_types_load.items():
            if not loads:
                continue
            
            avg_load = statistics.mean(loads)
            max_load = max(loads)
            agent_count = len(loads)
            
            # Scale up se carga alta
            if avg_load > 0.8 and agent_count < self.max_agents_per_type.get(agent_type, 5):
                scaling_actions.append({
                    "action": "scale_up",
                    "agent_type": agent_type,
                    "current_count": agent_count,
                    "reason": f"High average load: {avg_load:.2f}",
                    "priority": "high" if max_load > 0.9 else "medium"
                })
            
            # Scale down se carga baixa
            elif avg_load < 0.3 and agent_count > self.min_agents_per_type.get(agent_type, 1):
                scaling_actions.append({
                    "action": "scale_down",
                    "agent_type": agent_type,
                    "current_count": agent_count,
                    "reason": f"Low average load: {avg_load:.2f}",
                    "priority": "low"
                })
        
        return scaling_actions
    
    def execute_scaling_action(self, action: Dict[str, Any]) -> bool:
        """Executa uma ação de scaling"""
        try:
            agent_type = action["agent_type"]
            
            if action["action"] == "scale_up":
                new_agent = self._create_agent(agent_type)
                if new_agent:
                    self.network.add_agent(new_agent)
                    logger.info(f"📈 Scaled up: Adicionado agente {new_agent.agent_id} ({agent_type.value})")
                    return True
            
            elif action["action"] == "scale_down":
                agent_to_remove = self._find_least_loaded_agent(agent_type)
                if agent_to_remove:
                    self.network.remove_agent(agent_to_remove)
                    logger.info(f"📉 Scaled down: Removido agente {agent_to_remove} ({agent_type.value})")
                    return True
            
        except Exception as e:
            logger.error(f"❌ Erro executando scaling: {e}")
        
        return False
    
    def _get_agent_type_from_id(self, agent_id: str) -> Optional[AgentType]:
        """Determina tipo do agente pelo ID"""
        if "optimizer" in agent_id:
            return AgentType.OPTIMIZER
        elif "security" in agent_id or "guard" in agent_id:
            return AgentType.GUARD
        elif "learning" in agent_id or "learn" in agent_id:
            return AgentType.LEARN
        elif "data" in agent_id or "analytics" in agent_id:
            return AgentType.SPECIALIST
        elif "monitor" in agent_id:
            return AgentType.MONITOR
        return None
    
    def _create_agent(self, agent_type: AgentType) -> Optional[BaseNetworkAgent]:
        """Cria um novo agente do tipo especificado"""
        agent_id = f"{agent_type.value}_{uuid.uuid4().hex[:8]}"
        
        if agent_type == AgentType.OPTIMIZER:
            return OptimizationAgent(agent_id, self.network.message_bus)
        elif agent_type == AgentType.GUARD:
            return SecurityAgent(agent_id, self.network.message_bus)
        elif agent_type == AgentType.LEARN:
            return LearningAgent(agent_id, self.network.message_bus)
        elif agent_type == AgentType.SPECIALIST:
            return DataAgent(agent_id, self.network.message_bus)
        elif agent_type == AgentType.MONITOR:
            return MonitoringAgent(agent_id, self.network.message_bus)
        
        return None
    
    def _find_least_loaded_agent(self, agent_type: AgentType) -> Optional[str]:
        """Encontra o agente menos carregado de um tipo"""
        # Implementação simples - pode ser melhorada
        candidates = [
            agent_id for agent_id in self.network.agents.keys()
            if self._get_agent_type_from_id(agent_id) == agent_type
        ]
        
        return candidates[0] if candidates else None


class NetworkOrchestrator:
    """Orquestrador principal da rede multi-agente"""
    
    def __init__(self):
        self.network = MultiAgentNetwork()
        self.load_balancer = LoadBalancer()
        self.fault_tolerance = FaultTolerance()
        self.auto_scaler = AutoScaler(self.network)
        
        self.task_queue: List[TaskRequest] = []
        self.active_tasks: Dict[str, Dict] = {}
        self.completed_tasks: deque = deque(maxlen=1000)
        
        self.performance_metrics: Dict[str, Any] = {}
        self.network_health = NetworkHealth(
            overall_score=100.0,
            active_agents=0,
            total_agents=0,
            average_load=0.0,
            response_time_p95=0.0,
            error_rate=0.0,
            uptime_percentage=100.0,
            last_incident=None
        )
        
        self._running = False
        self._orchestrator_thread = None
        
        # FastAPI app
        self.app = FastAPI(
            title="SUNA-ALSHAM Network Orchestrator",
            description="Orquestrador da rede multi-agente",
            version="1.0.0"
        )
        self._setup_api_routes()
        
        # WebSocket connections
        self.websocket_connections: List[WebSocket] = []
    
    def _setup_api_routes(self):
        """Configura rotas da API"""
        
        # CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @self.app.get("/")
        async def root():
            return {"message": "SUNA-ALSHAM Network Orchestrator", "status": "running"}
        
        @self.app.get("/health")
        async def health():
            return asdict(self.network_health)
        
        @self.app.get("/network/status")
        async def network_status():
            return self.network.get_network_status()
        
        @self.app.get("/agents")
        async def list_agents():
            agents_info = {}
            for agent_id, agent in self.network.agents.items():
                agents_info[agent_id] = {
                    "type": agent.agent_type.value,
                    "status": agent.status,
                    "capabilities": [cap.name for cap in agent.capabilities]
                }
            return agents_info
        
        @self.app.post("/tasks")
        async def submit_task(task_data: Dict[str, Any]):
            task = TaskRequest(
                id=str(uuid.uuid4()),
                type=task_data.get("type", "generic"),
                priority=Priority(task_data.get("priority", 3)),
                data=task_data.get("data", {}),
                requester=task_data.get("requester", "api"),
                created_at=datetime.now(),
                required_capabilities=task_data.get("required_capabilities", [])
            )
            
            self.task_queue.append(task)
            return {"task_id": task.id, "status": "queued"}
        
        @self.app.get("/tasks/{task_id}")
        async def get_task_status(task_id: str):
            # Verificar tarefas ativas
            if task_id in self.active_tasks:
                return self.active_tasks[task_id]
            
            # Verificar tarefas concluídas
            for task in self.completed_tasks:
                if task.get("id") == task_id:
                    return task
            
            raise HTTPException(status_code=404, detail="Task not found")
        
        @self.app.get("/metrics")
        async def get_metrics():
            return {
                "performance": self.performance_metrics,
                "load_distribution": self.load_balancer.get_load_distribution(),
                "fault_summary": self.fault_tolerance.get_fault_summary(),
                "network_health": asdict(self.network_health)
            }
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self.websocket_connections.append(websocket)
            
            try:
                while True:
                    # Enviar updates periódicos
                    update = {
                        "timestamp": datetime.now().isoformat(),
                        "network_health": asdict(self.network_health),
                        "active_agents": len([a for a in self.network.agents.values() if a.status == "running"]),
                        "active_tasks": len(self.active_tasks),
                        "queued_tasks": len(self.task_queue)
                    }
                    
                    await websocket.send_json(update)
                    await asyncio.sleep(5)  # Update a cada 5 segundos
                    
            except WebSocketDisconnect:
                self.websocket_connections.remove(websocket)
    
    def start(self):
        """Inicia o orquestrador"""
        logger.info("🎼 Iniciando Network Orchestrator...")
        
        # Inicializar agentes padrão
        self._initialize_default_agents()
        
        # Iniciar rede
        self.network.start()
        
        # Iniciar thread do orquestrador
        self._running = True
        self._orchestrator_thread = threading.Thread(target=self._orchestration_loop)
        self._orchestrator_thread.daemon = True
        self._orchestrator_thread.start()
        
        logger.info("✅ Network Orchestrator iniciado!")
    
    def stop(self):
        """Para o orquestrador"""
        logger.info("⏹️ Parando Network Orchestrator...")
        
        self._running = False
        if self._orchestrator_thread:
            self._orchestrator_thread.join()
        
        self.network.stop()
        
        logger.info("✅ Network Orchestrator parado")
    
    def _initialize_default_agents(self):
        """Inicializa agentes padrão"""
        default_agents = [
            OptimizationAgent("optimizer_001", self.network.message_bus),
            SecurityAgent("security_001", self.network.message_bus),
            LearningAgent("learning_001", self.network.message_bus),
            DataAgent("data_001", self.network.message_bus),
            MonitoringAgent("monitor_001", self.network.message_bus)
        ]
        
        for agent in default_agents:
            self.network.add_agent(agent)
        
        logger.info(f"🤖 {len(default_agents)} agentes padrão inicializados")
    
    def _orchestration_loop(self):
        """Loop principal de orquestração"""
        last_health_check = time.time()
        last_scaling_check = time.time()
        
        while self._running:
            try:
                current_time = time.time()
                
                # Processar fila de tarefas
                self._process_task_queue()
                
                # Verificar saúde da rede (a cada 30 segundos)
                if current_time - last_health_check > 30:
                    self._update_network_health()
                    last_health_check = current_time
                
                # Verificar necessidade de scaling (a cada 60 segundos)
                if current_time - last_scaling_check > 60:
                    self._check_scaling_needs()
                    last_scaling_check = current_time
                
                # Broadcast updates via WebSocket
                if self.websocket_connections:
                    asyncio.create_task(self._broadcast_updates())
                
            except Exception as e:
                logger.error(f"❌ Erro no loop de orquestração: {e}")
            
            time.sleep(1)  # 1 segundo de delay
    
    def _process_task_queue(self):
        """Processa fila de tarefas"""
        if not self.task_queue:
            return
        
        # Ordenar por prioridade
        self.task_queue.sort(key=lambda t: t.priority.value)
        
        # Processar tarefas de alta prioridade primeiro
        tasks_to_process = self.task_queue[:5]  # Máximo 5 por vez
        
        for task in tasks_to_process:
            if self._assign_task_to_agent(task):
                self.task_queue.remove(task)
    
    def _assign_task_to_agent(self, task: TaskRequest) -> bool:
        """Atribui tarefa a um agente disponível"""
        # Encontrar agentes disponíveis
        available_agents = [
            agent_id for agent_id, agent in self.network.agents.items()
            if agent.status == "running" and self.fault_tolerance.is_agent_available(agent_id)
        ]
        
        if not available_agents:
            logger.warning(f"⚠️ Nenhum agente disponível para tarefa {task.id}")
            return False
        
        # Selecionar melhor agente
        selected_agent = self.load_balancer.select_best_agent(task, available_agents)
        
        if not selected_agent:
            return False
        
        # Atribuir tarefa
        try:
            task_assignment = self.network.assign_task(task.type, asdict(task))
            
            if task_assignment:
                self.active_tasks[task.id] = {
                    "id": task.id,
                    "type": task.type,
                    "assigned_agent": selected_agent,
                    "status": "running",
                    "started_at": datetime.now().isoformat(),
                    "priority": task.priority.value
                }
                
                logger.info(f"📋 Tarefa {task.id} atribuída ao agente {selected_agent}")
                return True
                
        except Exception as e:
            logger.error(f"❌ Erro atribuindo tarefa {task.id}: {e}")
            self.fault_tolerance.mark_agent_failed(selected_agent, str(e))
        
        return False
    
    def _update_network_health(self):
        """Atualiza métricas de saúde da rede"""
        network_status = self.network.get_network_status()
        load_distribution = self.load_balancer.get_load_distribution()
        
        # Calcular métricas
        active_agents = network_status["network_metrics"]["active_agents"]
        total_agents = network_status["network_metrics"]["total_agents"]
        
        average_load = statistics.mean(load_distribution.values()) if load_distribution else 0.0
        
        # Calcular score geral (0-100)
        health_score = 100.0
        
        # Penalizar por agentes inativos
        if total_agents > 0:
            agent_availability = active_agents / total_agents
            health_score *= agent_availability
        
        # Penalizar por alta carga
        if average_load > 0.8:
            health_score *= (1.0 - (average_load - 0.8) * 2)
        
        # Penalizar por falhas
        fault_summary = self.fault_tolerance.get_fault_summary()
        if fault_summary["failed_agents"] > 0:
            health_score *= (1.0 - fault_summary["failed_agents"] * 0.1)
        
        # Atualizar health
        self.network_health = NetworkHealth(
            overall_score=max(0.0, health_score),
            active_agents=active_agents,
            total_agents=total_agents,
            average_load=average_load,
            response_time_p95=0.0,  # TODO: Calcular baseado em métricas reais
            error_rate=0.0,  # TODO: Calcular baseado em métricas reais
            uptime_percentage=100.0,  # TODO: Calcular baseado em histórico
            last_incident=None  # TODO: Rastrear incidentes
        )
    
    def _check_scaling_needs(self):
        """Verifica necessidade de auto-scaling"""
        load_distribution = self.load_balancer.get_load_distribution()
        network_metrics = self.network.get_network_status()["network_metrics"]
        
        scaling_actions = self.auto_scaler.evaluate_scaling_need(
            load_distribution, 
            network_metrics
        )
        
        # Executar ações de scaling
        for action in scaling_actions:
            if action["priority"] == "high":
                success = self.auto_scaler.execute_scaling_action(action)
                if success:
                    logger.info(f"🔄 Scaling executado: {action}")
    
    async def _broadcast_updates(self):
        """Envia updates via WebSocket"""
        if not self.websocket_connections:
            return
        
        update = {
            "timestamp": datetime.now().isoformat(),
            "network_health": asdict(self.network_health),
            "active_agents": len([a for a in self.network.agents.values() if a.status == "running"]),
            "active_tasks": len(self.active_tasks),
            "queued_tasks": len(self.task_queue)
        }
        
        # Enviar para todas as conexões ativas
        disconnected = []
        for websocket in self.websocket_connections:
            try:
                await websocket.send_json(update)
            except:
                disconnected.append(websocket)
        
        # Remover conexões desconectadas
        for ws in disconnected:
            self.websocket_connections.remove(ws)


if __name__ == "__main__":
    # Inicializar orquestrador
    orchestrator = NetworkOrchestrator()
    
    try:
        # Iniciar orquestrador
        orchestrator.start()
        
        # Iniciar servidor FastAPI
        uvicorn.run(
            orchestrator.app,
            host="0.0.0.0",
            port=8001,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário")
    finally:
        orchestrator.stop()

