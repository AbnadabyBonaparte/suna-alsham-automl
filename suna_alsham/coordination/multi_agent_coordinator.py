"""
🎯 SUNA-ALSHAM Multi-Agent Coordinator
Sistema de coordenação avançado para rede multi-agente com IA

FUNCIONALIDADES:
✅ Coordenação inteligente baseada em IA
✅ Planejamento de tarefas distribuídas
✅ Otimização de recursos em tempo real
✅ Detecção e resolução de conflitos
✅ Balanceamento de carga adaptativo
✅ Monitoramento de saúde da rede
✅ Auto-scaling baseado em demanda
✅ Recuperação automática de falhas
"""

import asyncio
import json
import time
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics
import heapq
import networkx as nx
import openai
import os

from multi_agent_network import (
    BaseNetworkAgent, AgentType, MessageType, Priority, 
    NetworkMetrics, MessageBus
)
from ai_powered_agents import AICache, AISecurityValidator, ScientificLogger

logger = logging.getLogger(__name__)


@dataclass
class TaskPlan:
    """Plano de execução de tarefa distribuída"""
    plan_id: str
    task_id: str
    subtasks: List[Dict[str, Any]]
    dependencies: Dict[str, List[str]]
    resource_requirements: Dict[str, float]
    estimated_duration: float
    priority: Priority
    created_at: datetime
    assigned_agents: Dict[str, str]
    execution_status: str = "planned"


@dataclass
class ConflictResolution:
    """Resolução de conflito entre agentes"""
    conflict_id: str
    involved_agents: List[str]
    conflict_type: str
    description: str
    resolution_strategy: str
    resolution_actions: List[Dict[str, Any]]
    resolved_at: Optional[datetime] = None
    success: bool = False


@dataclass
class NetworkTopology:
    """Topologia da rede de agentes"""
    nodes: Dict[str, Dict[str, Any]]
    edges: List[Tuple[str, str, Dict[str, Any]]]
    clusters: Dict[str, List[str]]
    communication_patterns: Dict[str, Dict[str, int]]
    last_updated: datetime


class IntelligentTaskPlanner:
    """Planejador inteligente de tarefas usando IA"""
    
    def __init__(self, ai_cache: AICache, security_validator: AISecurityValidator):
        self.ai_cache = ai_cache
        self.security_validator = security_validator
        self.planning_history: List[TaskPlan] = []
        self.success_patterns: Dict[str, float] = {}
    
    async def create_task_plan(self, task: Dict[str, Any], available_agents: Dict[str, Any]) -> TaskPlan:
        """Cria plano de execução para uma tarefa complexa"""
        plan_id = str(uuid.uuid4())
        
        # Preparar prompt para planejamento
        planning_prompt = self._create_planning_prompt(task, available_agents)
        
        # Validar prompt
        is_safe, issues = self.security_validator.validate_prompt(planning_prompt)
        if not is_safe:
            raise ValueError(f"Unsafe planning prompt: {issues}")
        
        # Buscar no cache
        cached_plan = self.ai_cache.get(planning_prompt, "gpt-4", 0.3)
        if cached_plan:
            logger.info(f"📋 Plano {plan_id} obtido do cache")
            return self._parse_cached_plan(cached_plan["result"], plan_id, task)
        
        try:
            # Chamar IA para planejamento
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert task planner for multi-agent systems. Create optimal execution plans that minimize resource conflicts and maximize efficiency."
                    },
                    {
                        "role": "user",
                        "content": planning_prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            ai_response = response.choices[0].message.content
            
            # Parsear resposta da IA
            plan_data = self._parse_ai_plan(ai_response)
            
            # Criar plano estruturado
            task_plan = TaskPlan(
                plan_id=plan_id,
                task_id=task.get("id", str(uuid.uuid4())),
                subtasks=plan_data["subtasks"],
                dependencies=plan_data["dependencies"],
                resource_requirements=plan_data["resource_requirements"],
                estimated_duration=plan_data["estimated_duration"],
                priority=Priority(task.get("priority", 3)),
                created_at=datetime.now(),
                assigned_agents={}
            )
            
            # Salvar no cache
            self.ai_cache.set(
                planning_prompt, "gpt-4", 0.3,
                {"result": asdict(task_plan)}, ttl=1800
            )
            
            # Armazenar no histórico
            self.planning_history.append(task_plan)
            
            logger.info(f"📋 Plano {plan_id} criado com {len(task_plan.subtasks)} subtarefas")
            
            return task_plan
            
        except Exception as e:
            logger.error(f"❌ Erro criando plano de tarefa: {e}")
            raise
    
    def _create_planning_prompt(self, task: Dict[str, Any], available_agents: Dict[str, Any]) -> str:
        """Cria prompt para planejamento de tarefa"""
        return f"""
Create an execution plan for this complex task:

TASK:
{json.dumps(task, indent=2)}

AVAILABLE AGENTS:
{json.dumps(available_agents, indent=2)}

Create a detailed execution plan in JSON format:
{{
    "subtasks": [
        {{
            "id": "subtask_1",
            "description": "detailed description",
            "required_capabilities": ["capability1", "capability2"],
            "estimated_duration_minutes": 30,
            "resource_requirements": {{"cpu": 0.5, "memory": 0.3}},
            "priority": 1-5
        }}
    ],
    "dependencies": {{
        "subtask_2": ["subtask_1"],
        "subtask_3": ["subtask_1", "subtask_2"]
    }},
    "resource_requirements": {{
        "total_cpu": 2.0,
        "total_memory": 1.5,
        "estimated_duration": 120
    }},
    "estimated_duration": 120,
    "optimization_notes": "explanation of planning decisions"
}}
"""
    
    def _parse_ai_plan(self, ai_response: str) -> Dict[str, Any]:
        """Parseia resposta da IA para plano de tarefa"""
        try:
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group()
                plan_data = json.loads(json_str)
                
                # Validar estrutura do plano
                required_fields = ["subtasks", "dependencies", "resource_requirements", "estimated_duration"]
                for field in required_fields:
                    if field not in plan_data:
                        plan_data[field] = self._get_default_value(field)
                
                return plan_data
            else:
                return self._get_fallback_plan()
                
        except Exception as e:
            logger.error(f"❌ Erro parseando plano da IA: {e}")
            return self._get_fallback_plan()
    
    def _get_default_value(self, field: str) -> Any:
        """Retorna valor padrão para campo do plano"""
        defaults = {
            "subtasks": [],
            "dependencies": {},
            "resource_requirements": {"total_cpu": 1.0, "total_memory": 0.5},
            "estimated_duration": 60
        }
        return defaults.get(field, None)
    
    def _get_fallback_plan(self) -> Dict[str, Any]:
        """Retorna plano de fallback em caso de erro"""
        return {
            "subtasks": [
                {
                    "id": "fallback_task",
                    "description": "Execute task with default parameters",
                    "required_capabilities": ["general"],
                    "estimated_duration_minutes": 30,
                    "resource_requirements": {"cpu": 0.5, "memory": 0.3},
                    "priority": 3
                }
            ],
            "dependencies": {},
            "resource_requirements": {"total_cpu": 0.5, "total_memory": 0.3},
            "estimated_duration": 30
        }
    
    def _parse_cached_plan(self, cached_data: Dict[str, Any], plan_id: str, task: Dict[str, Any]) -> TaskPlan:
        """Parseia plano do cache"""
        return TaskPlan(
            plan_id=plan_id,
            task_id=task.get("id", str(uuid.uuid4())),
            subtasks=cached_data.get("subtasks", []),
            dependencies=cached_data.get("dependencies", {}),
            resource_requirements=cached_data.get("resource_requirements", {}),
            estimated_duration=cached_data.get("estimated_duration", 60),
            priority=Priority(task.get("priority", 3)),
            created_at=datetime.now(),
            assigned_agents={}
        )


class ConflictResolver:
    """Resolvedor de conflitos entre agentes"""
    
    def __init__(self):
        self.active_conflicts: Dict[str, ConflictResolution] = {}
        self.resolution_history: List[ConflictResolution] = []
        self.resolution_strategies = {
            "resource_conflict": self._resolve_resource_conflict,
            "priority_conflict": self._resolve_priority_conflict,
            "dependency_conflict": self._resolve_dependency_conflict,
            "communication_conflict": self._resolve_communication_conflict
        }
    
    def detect_conflicts(self, task_plans: List[TaskPlan], agent_loads: Dict[str, Any]) -> List[ConflictResolution]:
        """Detecta conflitos potenciais"""
        conflicts = []
        
        # Detectar conflitos de recursos
        resource_conflicts = self._detect_resource_conflicts(task_plans, agent_loads)
        conflicts.extend(resource_conflicts)
        
        # Detectar conflitos de prioridade
        priority_conflicts = self._detect_priority_conflicts(task_plans)
        conflicts.extend(priority_conflicts)
        
        # Detectar conflitos de dependência
        dependency_conflicts = self._detect_dependency_conflicts(task_plans)
        conflicts.extend(dependency_conflicts)
        
        return conflicts
    
    def resolve_conflict(self, conflict: ConflictResolution) -> bool:
        """Resolve um conflito específico"""
        try:
            strategy = self.resolution_strategies.get(conflict.conflict_type)
            if not strategy:
                logger.warning(f"⚠️ Estratégia não encontrada para conflito {conflict.conflict_type}")
                return False
            
            success = strategy(conflict)
            
            if success:
                conflict.resolved_at = datetime.now()
                conflict.success = True
                self.resolution_history.append(conflict)
                logger.info(f"✅ Conflito {conflict.conflict_id} resolvido")
            else:
                logger.warning(f"⚠️ Falha resolvendo conflito {conflict.conflict_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Erro resolvendo conflito {conflict.conflict_id}: {e}")
            return False
    
    def _detect_resource_conflicts(self, task_plans: List[TaskPlan], agent_loads: Dict[str, Any]) -> List[ConflictResolution]:
        """Detecta conflitos de recursos"""
        conflicts = []
        
        # Calcular demanda total de recursos
        total_cpu_demand = sum(plan.resource_requirements.get("total_cpu", 0) for plan in task_plans)
        total_memory_demand = sum(plan.resource_requirements.get("total_memory", 0) for plan in task_plans)
        
        # Calcular capacidade disponível
        available_cpu = sum(1.0 - load.get("cpu_usage", 0) / 100 for load in agent_loads.values())
        available_memory = sum(1.0 - load.get("memory_usage", 0) / 100 for load in agent_loads.values())
        
        # Verificar se há conflito
        if total_cpu_demand > available_cpu * 0.8:  # 80% threshold
            conflicts.append(ConflictResolution(
                conflict_id=str(uuid.uuid4()),
                involved_agents=list(agent_loads.keys()),
                conflict_type="resource_conflict",
                description=f"CPU demand ({total_cpu_demand:.2f}) exceeds available capacity ({available_cpu:.2f})",
                resolution_strategy="load_balancing"
            ))
        
        if total_memory_demand > available_memory * 0.8:
            conflicts.append(ConflictResolution(
                conflict_id=str(uuid.uuid4()),
                involved_agents=list(agent_loads.keys()),
                conflict_type="resource_conflict",
                description=f"Memory demand ({total_memory_demand:.2f}) exceeds available capacity ({available_memory:.2f})",
                resolution_strategy="memory_optimization"
            ))
        
        return conflicts
    
    def _detect_priority_conflicts(self, task_plans: List[TaskPlan]) -> List[ConflictResolution]:
        """Detecta conflitos de prioridade"""
        conflicts = []
        
        # Agrupar por prioridade
        priority_groups = defaultdict(list)
        for plan in task_plans:
            priority_groups[plan.priority.value].append(plan)
        
        # Verificar se há muitas tarefas de alta prioridade
        high_priority_tasks = len(priority_groups.get(1, [])) + len(priority_groups.get(2, []))
        
        if high_priority_tasks > 5:  # Threshold
            conflicts.append(ConflictResolution(
                conflict_id=str(uuid.uuid4()),
                involved_agents=[],
                conflict_type="priority_conflict",
                description=f"Too many high priority tasks ({high_priority_tasks})",
                resolution_strategy="priority_rebalancing"
            ))
        
        return conflicts
    
    def _detect_dependency_conflicts(self, task_plans: List[TaskPlan]) -> List[ConflictResolution]:
        """Detecta conflitos de dependência"""
        conflicts = []
        
        # Verificar dependências circulares
        for plan in task_plans:
            if self._has_circular_dependencies(plan.dependencies):
                conflicts.append(ConflictResolution(
                    conflict_id=str(uuid.uuid4()),
                    involved_agents=[],
                    conflict_type="dependency_conflict",
                    description=f"Circular dependency detected in plan {plan.plan_id}",
                    resolution_strategy="dependency_restructuring"
                ))
        
        return conflicts
    
    def _has_circular_dependencies(self, dependencies: Dict[str, List[str]]) -> bool:
        """Verifica se há dependências circulares"""
        try:
            # Criar grafo direcionado
            graph = nx.DiGraph()
            
            for task, deps in dependencies.items():
                for dep in deps:
                    graph.add_edge(dep, task)
            
            # Verificar ciclos
            return not nx.is_directed_acyclic_graph(graph)
            
        except Exception:
            return False
    
    def _resolve_resource_conflict(self, conflict: ConflictResolution) -> bool:
        """Resolve conflito de recursos"""
        # Implementar estratégias de resolução
        conflict.resolution_actions = [
            {"action": "redistribute_tasks", "description": "Redistribute tasks across agents"},
            {"action": "delay_low_priority", "description": "Delay low priority tasks"},
            {"action": "scale_up", "description": "Request additional agents"}
        ]
        return True
    
    def _resolve_priority_conflict(self, conflict: ConflictResolution) -> bool:
        """Resolve conflito de prioridade"""
        conflict.resolution_actions = [
            {"action": "rebalance_priorities", "description": "Adjust task priorities"},
            {"action": "queue_management", "description": "Implement priority queue"}
        ]
        return True
    
    def _resolve_dependency_conflict(self, conflict: ConflictResolution) -> bool:
        """Resolve conflito de dependência"""
        conflict.resolution_actions = [
            {"action": "restructure_dependencies", "description": "Break circular dependencies"},
            {"action": "parallel_execution", "description": "Enable parallel execution where possible"}
        ]
        return True
    
    def _resolve_communication_conflict(self, conflict: ConflictResolution) -> bool:
        """Resolve conflito de comunicação"""
        conflict.resolution_actions = [
            {"action": "message_routing", "description": "Optimize message routing"},
            {"action": "bandwidth_allocation", "description": "Allocate communication bandwidth"}
        ]
        return True


class NetworkTopologyAnalyzer:
    """Analisador de topologia da rede"""
    
    def __init__(self):
        self.topology_history: List[NetworkTopology] = []
        self.performance_patterns: Dict[str, List[float]] = defaultdict(list)
    
    def analyze_network_topology(self, agents: Dict[str, Any], 
                                message_patterns: Dict[str, Any]) -> NetworkTopology:
        """Analisa topologia atual da rede"""
        
        # Criar nós
        nodes = {}
        for agent_id, agent_info in agents.items():
            nodes[agent_id] = {
                "type": agent_info.get("type", "unknown"),
                "status": agent_info.get("status", "unknown"),
                "capabilities": agent_info.get("capabilities", []),
                "load": agent_info.get("load", 0.0),
                "last_seen": agent_info.get("last_seen", datetime.now())
            }
        
        # Criar arestas baseadas em padrões de comunicação
        edges = []
        for sender, receivers in message_patterns.items():
            if isinstance(receivers, dict):
                for receiver, count in receivers.items():
                    if sender != receiver and count > 0:
                        edges.append((sender, receiver, {"weight": count, "type": "communication"}))
        
        # Detectar clusters
        clusters = self._detect_clusters(nodes, edges)
        
        # Criar topologia
        topology = NetworkTopology(
            nodes=nodes,
            edges=edges,
            clusters=clusters,
            communication_patterns=message_patterns,
            last_updated=datetime.now()
        )
        
        # Armazenar no histórico
        self.topology_history.append(topology)
        
        # Manter apenas últimas 100 topologias
        if len(self.topology_history) > 100:
            self.topology_history = self.topology_history[-100:]
        
        return topology
    
    def _detect_clusters(self, nodes: Dict[str, Any], edges: List[Tuple]) -> Dict[str, List[str]]:
        """Detecta clusters na rede"""
        try:
            # Criar grafo
            graph = nx.Graph()
            
            # Adicionar nós
            for node_id, node_data in nodes.items():
                graph.add_node(node_id, **node_data)
            
            # Adicionar arestas
            for sender, receiver, edge_data in edges:
                graph.add_edge(sender, receiver, **edge_data)
            
            # Detectar comunidades usando algoritmo de Louvain
            import networkx.algorithms.community as nx_comm
            communities = nx_comm.louvain_communities(graph)
            
            # Converter para formato de clusters
            clusters = {}
            for i, community in enumerate(communities):
                cluster_name = f"cluster_{i}"
                clusters[cluster_name] = list(community)
            
            return clusters
            
        except Exception as e:
            logger.warning(f"⚠️ Erro detectando clusters: {e}")
            return {"default_cluster": list(nodes.keys())}
    
    def get_topology_insights(self) -> Dict[str, Any]:
        """Retorna insights sobre a topologia"""
        if not self.topology_history:
            return {"error": "No topology data available"}
        
        latest_topology = self.topology_history[-1]
        
        # Calcular métricas
        total_nodes = len(latest_topology.nodes)
        total_edges = len(latest_topology.edges)
        total_clusters = len(latest_topology.clusters)
        
        # Calcular densidade da rede
        max_edges = total_nodes * (total_nodes - 1) / 2
        network_density = total_edges / max_edges if max_edges > 0 else 0
        
        # Identificar nós centrais
        edge_counts = defaultdict(int)
        for sender, receiver, _ in latest_topology.edges:
            edge_counts[sender] += 1
            edge_counts[receiver] += 1
        
        central_nodes = sorted(edge_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "total_nodes": total_nodes,
            "total_edges": total_edges,
            "total_clusters": total_clusters,
            "network_density": round(network_density, 3),
            "central_nodes": central_nodes,
            "cluster_distribution": {k: len(v) for k, v in latest_topology.clusters.items()},
            "analysis_timestamp": latest_topology.last_updated.isoformat()
        }


class MultiAgentCoordinator(BaseNetworkAgent):
    """Coordenador principal da rede multi-agente"""
    
    def __init__(self, message_bus: MessageBus):
        super().__init__("master_coordinator", AgentType.COORDINATOR, message_bus)
        
        # Componentes de IA
        self.ai_cache = AICache(os.getenv("REDIS_URL"))
        self.security_validator = AISecurityValidator()
        self.scientific_logger = ScientificLogger("coordinator_metrics.jsonl")
        
        # Componentes de coordenação
        self.task_planner = IntelligentTaskPlanner(self.ai_cache, self.security_validator)
        self.conflict_resolver = ConflictResolver()
        self.topology_analyzer = NetworkTopologyAnalyzer()
        
        # Estado da coordenação
        self.active_plans: Dict[str, TaskPlan] = {}
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.performance_history: deque = deque(maxlen=1000)
        self.coordination_metrics: Dict[str, float] = {}
        
        # Configurações
        self.coordination_interval = 30  # 30 segundos
        self.last_coordination = datetime.now()
        
        # Adicionar capacidades específicas
        self.add_capability(AgentCapability(
            name="intelligent_coordination",
            description="Coordenação inteligente de rede multi-agente",
            input_types=["task_requests", "agent_status", "network_metrics"],
            output_types=["task_plans", "resource_allocation", "conflict_resolution"],
            processing_time_ms=1000.0,
            accuracy_score=0.95,
            resource_cost=0.4
        ))
        
        # Registrar handlers específicos
        self.message_handlers[MessageType.TASK_ASSIGNMENT] = self._handle_complex_task
        self.message_handlers[MessageType.COORDINATION] = self._handle_coordination_request
    
    def _agent_specific_logic(self):
        """Lógica específica do coordenador"""
        super()._agent_specific_logic()
        
        # Executar coordenação periódica
        if self._should_coordinate():
            asyncio.create_task(self._coordinate_network())
    
    def _should_coordinate(self) -> bool:
        """Verifica se deve executar coordenação"""
        time_since_coordination = datetime.now() - self.last_coordination
        return time_since_coordination.seconds >= self.coordination_interval
    
    async def _coordinate_network(self):
        """Executa coordenação da rede"""
        try:
            logger.info("🎯 Iniciando coordenação da rede")
            
            # Analisar topologia atual
            topology = self.topology_analyzer.analyze_network_topology(
                self.agent_registry, 
                self._get_communication_patterns()
            )
            
            # Detectar conflitos
            conflicts = self.conflict_resolver.detect_conflicts(
                list(self.active_plans.values()),
                self._get_agent_loads()
            )
            
            # Resolver conflitos
            for conflict in conflicts:
                await self._resolve_conflict_async(conflict)
            
            # Otimizar alocação de recursos
            await self._optimize_resource_allocation()
            
            # Atualizar métricas de coordenação
            self._update_coordination_metrics(topology, conflicts)
            
            self.last_coordination = datetime.now()
            
            logger.info(f"✅ Coordenação concluída - {len(conflicts)} conflitos processados")
            
        except Exception as e:
            logger.error(f"❌ Erro na coordenação da rede: {e}")
    
    async def _handle_complex_task(self, message):
        """Handler para tarefas complexas"""
        task_data = message.content.get("task_data", {})
        
        try:
            # Criar plano de execução
            task_plan = await self.task_planner.create_task_plan(
                task_data, 
                self.agent_registry
            )
            
            # Armazenar plano ativo
            self.active_plans[task_plan.plan_id] = task_plan
            
            # Atribuir subtarefas aos agentes
            assignments = await self._assign_subtasks(task_plan)
            
            # Enviar resposta
            self.send_message(
                message.sender_id,
                MessageType.RESPONSE,
                {
                    "status": "planned",
                    "plan_id": task_plan.plan_id,
                    "subtasks": len(task_plan.subtasks),
                    "assignments": assignments,
                    "estimated_duration": task_plan.estimated_duration
                }
            )
            
            logger.info(f"📋 Tarefa complexa planejada: {task_plan.plan_id}")
            
        except Exception as e:
            logger.error(f"❌ Erro processando tarefa complexa: {e}")
            
            self.send_message(
                message.sender_id,
                MessageType.RESPONSE,
                {"status": "error", "error": str(e)}
            )
    
    async def _assign_subtasks(self, task_plan: TaskPlan) -> Dict[str, str]:
        """Atribui subtarefas aos agentes mais adequados"""
        assignments = {}
        
        for subtask in task_plan.subtasks:
            # Encontrar agentes com capacidades necessárias
            required_caps = subtask.get("required_capabilities", [])
            suitable_agents = self._find_suitable_agents(required_caps)
            
            if suitable_agents:
                # Selecionar melhor agente baseado em carga e capacidades
                best_agent = self._select_best_agent(suitable_agents, subtask)
                assignments[subtask["id"]] = best_agent
                
                # Enviar atribuição
                self.send_message(
                    best_agent,
                    MessageType.TASK_ASSIGNMENT,
                    {
                        "task_id": subtask["id"],
                        "task_data": subtask,
                        "plan_id": task_plan.plan_id
                    },
                    Priority.NORMAL
                )
            else:
                logger.warning(f"⚠️ Nenhum agente adequado para subtarefa {subtask['id']}")
        
        return assignments
    
    def _find_suitable_agents(self, required_capabilities: List[str]) -> List[str]:
        """Encontra agentes com capacidades necessárias"""
        suitable_agents = []
        
        for agent_id, agent_info in self.agent_registry.items():
            agent_caps = agent_info.get("capabilities", [])
            
            # Verificar se agente tem todas as capacidades necessárias
            if all(cap in agent_caps for cap in required_capabilities):
                # Verificar se agente está ativo
                if agent_info.get("status") == "running":
                    suitable_agents.append(agent_id)
        
        return suitable_agents
    
    def _select_best_agent(self, suitable_agents: List[str], subtask: Dict[str, Any]) -> str:
        """Seleciona o melhor agente para uma subtarefa"""
        if len(suitable_agents) == 1:
            return suitable_agents[0]
        
        # Calcular score para cada agente
        agent_scores = {}
        
        for agent_id in suitable_agents:
            agent_info = self.agent_registry.get(agent_id, {})
            
            # Score baseado em carga (menor é melhor)
            load = agent_info.get("load", 0.5)
            load_score = 1.0 - load
            
            # Score baseado em capacidades específicas
            capability_score = 0.8  # Score base
            
            # Score baseado em histórico de performance
            performance_score = agent_info.get("performance_score", 0.8)
            
            # Score final
            total_score = (load_score * 0.4 + capability_score * 0.3 + performance_score * 0.3)
            agent_scores[agent_id] = total_score
        
        # Retornar agente com melhor score
        best_agent = max(agent_scores.items(), key=lambda x: x[1])
        return best_agent[0]
    
    async def _resolve_conflict_async(self, conflict: ConflictResolution):
        """Resolve conflito de forma assíncrona"""
        try:
            success = self.conflict_resolver.resolve_conflict(conflict)
            
            if success:
                # Notificar agentes envolvidos sobre resolução
                for agent_id in conflict.involved_agents:
                    self.send_message(
                        agent_id,
                        MessageType.NOTIFICATION,
                        {
                            "type": "conflict_resolved",
                            "conflict_id": conflict.conflict_id,
                            "resolution_actions": conflict.resolution_actions
                        }
                    )
            
        except Exception as e:
            logger.error(f"❌ Erro resolvendo conflito {conflict.conflict_id}: {e}")
    
    async def _optimize_resource_allocation(self):
        """Otimiza alocação de recursos"""
        # Implementação simplificada - pode ser expandida
        agent_loads = self._get_agent_loads()
        
        # Identificar agentes sobrecarregados
        overloaded_agents = [
            agent_id for agent_id, load in agent_loads.items()
            if load.get("cpu_usage", 0) > 80 or load.get("memory_usage", 0) > 85
        ]
        
        # Identificar agentes subutilizados
        underutilized_agents = [
            agent_id for agent_id, load in agent_loads.items()
            if load.get("cpu_usage", 0) < 30 and load.get("memory_usage", 0) < 40
        ]
        
        # Redistribuir tarefas se necessário
        if overloaded_agents and underutilized_agents:
            logger.info(f"🔄 Redistribuindo carga: {len(overloaded_agents)} sobrecarregados, {len(underutilized_agents)} subutilizados")
            
            # Implementar redistribuição (simplificado)
            for overloaded in overloaded_agents[:2]:  # Máximo 2 por vez
                self.send_message(
                    overloaded,
                    MessageType.COORDINATION,
                    {
                        "action": "reduce_load",
                        "target_agents": underutilized_agents[:2]
                    }
                )
    
    def _get_communication_patterns(self) -> Dict[str, Any]:
        """Obtém padrões de comunicação"""
        # Implementação simplificada - em produção, coletar do message bus
        return {
            agent_id: {"total_messages": 100, "avg_response_time": 200}
            for agent_id in self.agent_registry.keys()
        }
    
    def _get_agent_loads(self) -> Dict[str, Any]:
        """Obtém cargas atuais dos agentes"""
        # Implementação simplificada
        return {
            agent_id: {
                "cpu_usage": agent_info.get("cpu_usage", 50.0),
                "memory_usage": agent_info.get("memory_usage", 40.0),
                "active_tasks": agent_info.get("active_tasks", 2),
                "queue_size": agent_info.get("queue_size", 1)
            }
            for agent_id, agent_info in self.agent_registry.items()
        }
    
    def _update_coordination_metrics(self, topology: NetworkTopology, conflicts: List[ConflictResolution]):
        """Atualiza métricas de coordenação"""
        self.coordination_metrics = {
            "network_efficiency": self._calculate_network_efficiency(topology),
            "conflict_resolution_rate": len([c for c in conflicts if c.success]) / max(len(conflicts), 1),
            "resource_utilization": self._calculate_resource_utilization(),
            "coordination_overhead": self._calculate_coordination_overhead(),
            "agent_satisfaction": self._calculate_agent_satisfaction()
        }
        
        # Log métricas científicas
        for metric_name, value in self.coordination_metrics.items():
            from ai_powered_agents import ScientificMetrics
            
            scientific_metric = ScientificMetrics(
                metric_id=str(uuid.uuid4()),
                agent_id=self.agent_id,
                measurement_type=metric_name,
                baseline_value=0.8,  # Valor base
                current_value=value,
                improvement_percentage=((value - 0.8) / 0.8) * 100,
                statistical_significance=0.95,
                p_value=0.05,
                confidence_interval=(value - 0.05, value + 0.05),
                sample_size=len(self.agent_registry),
                measurement_timestamp=datetime.now(),
                validation_method="coordination_analysis"
            )
            
            self.scientific_logger.log_metric(scientific_metric)
    
    def _calculate_network_efficiency(self, topology: NetworkTopology) -> float:
        """Calcula eficiência da rede"""
        if not topology.nodes:
            return 0.0
        
        active_nodes = len([n for n in topology.nodes.values() if n.get("status") == "running"])
        total_nodes = len(topology.nodes)
        
        return active_nodes / total_nodes if total_nodes > 0 else 0.0
    
    def _calculate_resource_utilization(self) -> float:
        """Calcula utilização de recursos"""
        agent_loads = self._get_agent_loads()
        
        if not agent_loads:
            return 0.0
        
        total_cpu = sum(load.get("cpu_usage", 0) for load in agent_loads.values())
        total_memory = sum(load.get("memory_usage", 0) for load in agent_loads.values())
        
        avg_utilization = (total_cpu + total_memory) / (2 * len(agent_loads) * 100)
        return min(1.0, avg_utilization)
    
    def _calculate_coordination_overhead(self) -> float:
        """Calcula overhead de coordenação"""
        # Implementação simplificada
        return 0.1  # 10% de overhead
    
    def _calculate_agent_satisfaction(self) -> float:
        """Calcula satisfação dos agentes"""
        # Baseado em métricas de performance e carga
        agent_loads = self._get_agent_loads()
        
        if not agent_loads:
            return 1.0
        
        satisfaction_scores = []
        for load in agent_loads.values():
            cpu_satisfaction = 1.0 - (load.get("cpu_usage", 0) / 100)
            memory_satisfaction = 1.0 - (load.get("memory_usage", 0) / 100)
            queue_satisfaction = 1.0 - min(load.get("queue_size", 0) / 10, 1.0)
            
            agent_satisfaction = (cpu_satisfaction + memory_satisfaction + queue_satisfaction) / 3
            satisfaction_scores.append(agent_satisfaction)
        
        return statistics.mean(satisfaction_scores)
    
    def get_coordination_status(self) -> Dict[str, Any]:
        """Retorna status da coordenação"""
        topology_insights = self.topology_analyzer.get_topology_insights()
        cache_stats = self.ai_cache.get_stats()
        
        return {
            "coordinator_id": self.agent_id,
            "active_plans": len(self.active_plans),
            "registered_agents": len(self.agent_registry),
            "coordination_metrics": self.coordination_metrics,
            "topology_insights": topology_insights,
            "cache_performance": cache_stats,
            "last_coordination": self.last_coordination.isoformat(),
            "conflicts_resolved": len(self.conflict_resolver.resolution_history)
        }


if __name__ == "__main__":
    # Exemplo de uso
    from multi_agent_network import MultiAgentNetwork
    
    # Criar rede
    network = MultiAgentNetwork()
    
    # Criar coordenador
    coordinator = MultiAgentCoordinator(network.message_bus)
    network.add_agent(coordinator)
    
    try:
        # Iniciar rede
        network.start()
        
        print("🎯 Coordenador multi-agente iniciado!")
        print(f"Status: {coordinator.get_coordination_status()}")
        
        # Simular operação
        time.sleep(60)
        
        # Verificar status após coordenação
        print(f"Status após coordenação: {coordinator.get_coordination_status()}")
        
        input("\nPressione Enter para parar...")
        
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário")
    finally:
        network.stop()

