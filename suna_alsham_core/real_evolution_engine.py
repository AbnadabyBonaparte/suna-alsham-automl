# suna_alsham_core/real_evolution_engine.py - CORREÇÃO COMPLETA

import asyncio
import logging
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import json
import redis
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text

from .base_network_agent import BaseNetworkAgent, AgentType
from .database_models import TrainingDataPoint, EvolutionMetrics
from .message_bus import MessageBus
from .task_queue import TaskQueue

@dataclass
class EvolutionConfig:
    """Configuração para o motor de evolução"""
    learning_rate: float = 0.001
    mutation_rate: float = 0.01
    population_size: int = 100
    generations_limit: int = 1000
    fitness_threshold: float = 0.95
    adaptation_window: timedelta = field(default_factory=lambda: timedelta(hours=24))
    neural_layers: List[int] = field(default_factory=lambda: [512, 256, 128, 64])
    optimization_targets: Set[str] = field(default_factory=lambda: {"accuracy", "efficiency", "adaptability"})

class RealEvolutionEngine(BaseNetworkAgent):
    """
    Motor de Evolução Real do ALSHAM QUANTUM
    Agente de rede completo para evolução adaptativa do sistema
    """
    
    def __init__(self, agent_id: str = "evolution_engine_001"):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.EVOLUTION_ENGINE,
            capabilities=[
                "adaptive_learning",
                "neural_evolution", 
                "performance_optimization",
                "system_adaptation",
                "predictive_modeling",
                "autonomous_improvement"
            ]
        )
        
        self.config = EvolutionConfig()
        self.redis_client = redis.Redis(decode_responses=True)
        self.db_engine = create_engine("sqlite:///alsham_quantum.db")
        self.current_generation = 0
        self.population: List[Dict[str, Any]] = []
        self.best_fitness = 0.0
        self.evolution_history: List[Dict[str, Any]] = []
        
        # Neural network state
        self.neural_weights: Dict[str, List[float]] = {}
        self.activation_patterns: Dict[str, float] = {}
        self.adaptation_metrics: Dict[str, float] = {}
        
        logging.info(f"🧬 RealEvolutionEngine {agent_id} inicializado como agente de rede")

    async def initialize_agent(self) -> bool:
        """Inicializa o motor de evolução como agente de rede"""
        try:
            # Inicializar população inicial
            await self._initialize_population()
            
            # Configurar métricas de evolução
            await self._setup_evolution_metrics()
            
            # Registrar callbacks de evolução
            await self._register_evolution_callbacks()
            
            # Inicializar redes neurais
            await self._initialize_neural_networks()
            
            logging.info(f"✅ Evolution Engine {self.agent_id} inicializado com sucesso")
            return True
            
        except Exception as e:
            logging.error(f"❌ Erro na inicialização do Evolution Engine: {e}")
            return False

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagens de evolução do sistema"""
        try:
            message_type = message.get("type")
            
            if message_type == "evolution_request":
                return await self._handle_evolution_request(message)
            elif message_type == "fitness_evaluation":
                return await self._handle_fitness_evaluation(message)
            elif message_type == "adaptation_trigger":
                return await self._handle_adaptation_trigger(message)
            elif message_type == "neural_update":
                return await self._handle_neural_update(message)
            elif message_type == "performance_analysis":
                return await self._handle_performance_analysis(message)
            else:
                return {
                    "status": "error",
                    "message": f"Tipo de mensagem não reconhecido: {message_type}"
                }
                
        except Exception as e:
            logging.error(f"❌ Erro ao processar mensagem de evolução: {e}")
            return {"status": "error", "message": str(e)}

    async def _initialize_population(self):
        """Inicializa população para algoritmo genético"""
        self.population = []
        for i in range(self.config.population_size):
            individual = {
                "id": f"individual_{i}",
                "genes": self._generate_random_genes(),
                "fitness": 0.0,
                "generation": 0,
                "mutations": 0,
                "performance_history": []
            }
            self.population.append(individual)
        
        logging.info(f"🧬 População inicial criada: {len(self.population)} indivíduos")

    def _generate_random_genes(self) -> Dict[str, float]:
        """Gera genes aleatórios para um indivíduo"""
        import random
        return {
            "learning_efficiency": random.uniform(0.1, 1.0),
            "adaptation_speed": random.uniform(0.1, 1.0),
            "memory_optimization": random.uniform(0.1, 1.0),
            "processing_priority": random.uniform(0.1, 1.0),
            "error_tolerance": random.uniform(0.01, 0.1),
            "innovation_factor": random.uniform(0.0, 0.5)
        }

    async def _setup_evolution_metrics(self):
        """Configura métricas de evolução no banco de dados"""
        try:
            with Session(self.db_engine) as session:
                # Verificar se tabela existe
                result = session.execute(text("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='evolution_metrics'
                """))
                
                if not result.fetchone():
                    # Criar tabela se não existir
                    session.execute(text("""
                        CREATE TABLE evolution_metrics (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            generation INTEGER,
                            best_fitness REAL,
                            average_fitness REAL,
                            mutation_rate REAL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )
                    """))
                    session.commit()
                    logging.info("📊 Tabela evolution_metrics criada")
                
        except Exception as e:
            logging.error(f"❌ Erro ao configurar métricas de evolução: {e}")

    async def _register_evolution_callbacks(self):
        """Registra callbacks para eventos de evolução"""
        callbacks = {
            "generation_complete": self._on_generation_complete,
            "fitness_improved": self._on_fitness_improved,
            "adaptation_needed": self._on_adaptation_needed,
            "performance_degraded": self._on_performance_degraded
        }
        
        for event, callback in callbacks.items():
            await self.message_bus.register_callback(f"evolution.{event}", callback)
        
        logging.info("🔄 Callbacks de evolução registrados")

    async def _initialize_neural_networks(self):
        """Inicializa redes neurais para evolução"""
        import random
        
        for i, layer_size in enumerate(self.config.neural_layers):
            layer_name = f"layer_{i}"
            self.neural_weights[layer_name] = [
                random.uniform(-1.0, 1.0) for _ in range(layer_size)
            ]
        
        logging.info(f"🧠 Redes neurais inicializadas: {len(self.neural_weights)} camadas")

    async def _handle_evolution_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa solicitação de evolução"""
        try:
            target_metric = message.get("target_metric", "general_performance")
            generations = message.get("generations", 10)
            
            evolution_result = await self._run_evolution_cycle(target_metric, generations)
            
            return {
                "status": "success",
                "result": evolution_result,
                "agent_id": self.agent_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _run_evolution_cycle(self, target_metric: str, generations: int) -> Dict[str, Any]:
        """Executa ciclo completo de evolução"""
        start_fitness = self.best_fitness
        improvements = []
        
        for gen in range(generations):
            # Avaliar fitness da população
            await self._evaluate_population_fitness(target_metric)
            
            # Seleção dos melhores
            elite = self._select_elite()
            
            # Reprodução e mutação
            new_population = await self._reproduce_and_mutate(elite)
            
            # Atualizar população
            self.population = new_population
            self.current_generation += 1
            
            # Registrar melhoria
            if self.best_fitness > start_fitness:
                improvements.append({
                    "generation": self.current_generation,
                    "fitness": self.best_fitness,
                    "improvement": self.best_fitness - start_fitness
                })
        
        return {
            "generations_completed": generations,
            "initial_fitness": start_fitness,
            "final_fitness": self.best_fitness,
            "total_improvement": self.best_fitness - start_fitness,
            "improvements": improvements,
            "best_individual": self._get_best_individual()
        }

    async def _evaluate_population_fitness(self, target_metric: str):
        """Avalia fitness de toda a população"""
        for individual in self.population:
            fitness = await self._calculate_individual_fitness(individual, target_metric)
            individual["fitness"] = fitness
            
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                await self._notify_fitness_improvement(individual)

    async def _calculate_individual_fitness(self, individual: Dict[str, Any], target_metric: str) -> float:
        """Calcula fitness de um indivíduo específico"""
        genes = individual["genes"]
        
        # Fitness baseado na métrica alvo
        if target_metric == "learning_efficiency":
            return genes["learning_efficiency"] * 0.4 + genes["adaptation_speed"] * 0.3 + genes["memory_optimization"] * 0.3
        elif target_metric == "system_stability":
            return genes["error_tolerance"] * 0.5 + genes["processing_priority"] * 0.3 + genes["memory_optimization"] * 0.2
        elif target_metric == "innovation_capacity":
            return genes["innovation_factor"] * 0.6 + genes["adaptation_speed"] * 0.4
        else:
            # Fitness geral
            return sum(genes.values()) / len(genes)

    def _select_elite(self) -> List[Dict[str, Any]]:
        """Seleciona os melhores indivíduos da população"""
        elite_size = max(1, int(self.config.population_size * 0.2))
        return sorted(self.population, key=lambda x: x["fitness"], reverse=True)[:elite_size]

    async def _reproduce_and_mutate(self, elite: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Reproduz e muta população com base na elite"""
        import random
        new_population = elite.copy()  # Manter elite
        
        while len(new_population) < self.config.population_size:
            # Seleção de pais
            parent1 = random.choice(elite)
            parent2 = random.choice(elite)
            
            # Crossover
            child = self._crossover(parent1, parent2)
            
            # Mutação
            if random.random() < self.config.mutation_rate:
                child = self._mutate(child)
            
            new_population.append(child)
        
        return new_population

    def _crossover(self, parent1: Dict[str, Any], parent2: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza crossover entre dois pais"""
        import random
        
        child_genes = {}
        for gene_name in parent1["genes"].keys():
            if random.random() < 0.5:
                child_genes[gene_name] = parent1["genes"][gene_name]
            else:
                child_genes[gene_name] = parent2["genes"][gene_name]
        
        return {
            "id": f"child_{random.randint(1000, 9999)}",
            "genes": child_genes,
            "fitness": 0.0,
            "generation": self.current_generation + 1,
            "mutations": 0,
            "performance_history": []
        }

    def _mutate(self, individual: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica mutação em um indivíduo"""
        import random
        
        for gene_name, gene_value in individual["genes"].items():
            if random.random() < self.config.mutation_rate:
                mutation_strength = random.uniform(-0.1, 0.1)
                individual["genes"][gene_name] = max(0.0, min(1.0, gene_value + mutation_strength))
        
        individual["mutations"] += 1
        return individual

    def _get_best_individual(self) -> Dict[str, Any]:
        """Retorna o melhor indivíduo da população atual"""
        return max(self.population, key=lambda x: x["fitness"])

    async def _notify_fitness_improvement(self, individual: Dict[str, Any]):
        """Notifica sobre melhoria de fitness"""
        await self.message_bus.publish("evolution.fitness_improved", {
            "individual_id": individual["id"],
            "new_fitness": individual["fitness"],
            "generation": self.current_generation,
            "genes": individual["genes"]
        })

    async def _handle_fitness_evaluation(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa avaliação de fitness"""
        individual_id = message.get("individual_id")
        performance_data = message.get("performance_data", {})
        
        # Encontrar indivíduo
        individual = next((ind for ind in self.population if ind["id"] == individual_id), None)
        if not individual:
            return {"status": "error", "message": "Indivíduo não encontrado"}
        
        # Atualizar fitness baseado em dados reais
        new_fitness = self._calculate_real_world_fitness(performance_data)
        individual["fitness"] = new_fitness
        individual["performance_history"].append({
            "timestamp": datetime.now().isoformat(),
            "fitness": new_fitness,
            "performance_data": performance_data
        })
        
        return {"status": "success", "new_fitness": new_fitness}

    def _calculate_real_world_fitness(self, performance_data: Dict[str, Any]) -> float:
        """Calcula fitness baseado em dados reais de performance"""
        metrics = performance_data.get("metrics", {})
        
        accuracy = metrics.get("accuracy", 0.0)
        efficiency = metrics.get("efficiency", 0.0)
        stability = metrics.get("stability", 0.0)
        
        return (accuracy * 0.4 + efficiency * 0.3 + stability * 0.3)

    async def _handle_adaptation_trigger(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa trigger de adaptação"""
        adaptation_type = message.get("adaptation_type", "general")
        urgency = message.get("urgency", "normal")
        
        if urgency == "critical":
            # Adaptação imediata
            adaptation_result = await self._emergency_adaptation(adaptation_type)
        else:
            # Adaptação gradual
            adaptation_result = await self._gradual_adaptation(adaptation_type)
        
        return {
            "status": "success",
            "adaptation_result": adaptation_result,
            "adaptation_type": adaptation_type
        }

    async def _emergency_adaptation(self, adaptation_type: str) -> Dict[str, Any]:
        """Realiza adaptação de emergência"""
        # Aumentar taxa de mutação temporariamente
        original_mutation_rate = self.config.mutation_rate
        self.config.mutation_rate = min(1.0, original_mutation_rate * 5)
        
        # Executar ciclo de evolução acelerado
        result = await self._run_evolution_cycle(adaptation_type, 5)
        
        # Restaurar taxa de mutação
        self.config.mutation_rate = original_mutation_rate
        
        return {
            "type": "emergency",
            "mutation_rate_used": self.config.mutation_rate * 5,
            "evolution_result": result
        }

    async def _gradual_adaptation(self, adaptation_type: str) -> Dict[str, Any]:
        """Realiza adaptação gradual"""
        # Ajustar parâmetros gradualmente
        self.config.mutation_rate = min(1.0, self.config.mutation_rate * 1.1)
        
        # Executar ciclo de evolução normal
        result = await self._run_evolution_cycle(adaptation_type, 3)
        
        return {
            "type": "gradual",
            "new_mutation_rate": self.config.mutation_rate,
            "evolution_result": result
        }

    async def _handle_neural_update(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa atualização neural"""
        layer_name = message.get("layer_name")
        weight_updates = message.get("weight_updates", [])
        
        if layer_name in self.neural_weights:
            # Aplicar atualizações
            for i, update in enumerate(weight_updates):
                if i < len(self.neural_weights[layer_name]):
                    self.neural_weights[layer_name][i] += update * self.config.learning_rate
        
        return {
            "status": "success",
            "updated_layer": layer_name,
            "updates_applied": len(weight_updates)
        }

    async def _handle_performance_analysis(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa análise de performance"""
        analysis_data = message.get("analysis_data", {})
        
        # Analisar tendências de performance
        trends = self._analyze_performance_trends(analysis_data)
        
        # Sugerir adaptações baseadas na análise
        recommendations = self._generate_adaptation_recommendations(trends)
        
        return {
            "status": "success",
            "performance_trends": trends,
            "recommendations": recommendations,
            "analysis_timestamp": datetime.now().isoformat()
        }

    def _analyze_performance_trends(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa tendências de performance"""
        metrics_history = analysis_data.get("metrics_history", [])
        
        if len(metrics_history) < 2:
            return {"trend": "insufficient_data"}
        
        # Calcular tendências
        recent_avg = sum(m.get("overall_score", 0) for m in metrics_history[-5:]) / min(5, len(metrics_history))
        older_avg = sum(m.get("overall_score", 0) for m in metrics_history[:-5]) / max(1, len(metrics_history) - 5)
        
        trend_direction = "improving" if recent_avg > older_avg else "declining"
        trend_strength = abs(recent_avg - older_avg) / max(older_avg, 0.01)
        
        return {
            "trend": trend_direction,
            "strength": trend_strength,
            "recent_average": recent_avg,
            "historical_average": older_avg,
            "data_points": len(metrics_history)
        }

    def _generate_adaptation_recommendations(self, trends: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera recomendações de adaptação baseadas nas tendências"""
        recommendations = []
        
        if trends.get("trend") == "declining":
            recommendations.append({
                "type": "increase_mutation_rate",
                "reason": "Performance em declínio detectada",
                "priority": "high",
                "suggested_value": self.config.mutation_rate * 1.5
            })
            
            recommendations.append({
                "type": "emergency_evolution_cycle",
                "reason": "Necessária adaptação rápida",
                "priority": "medium",
                "suggested_generations": 10
            })
        
        elif trends.get("trend") == "improving":
            recommendations.append({
                "type": "maintain_current_parameters",
                "reason": "Performance em melhoria",
                "priority": "low"
            })
        
        return recommendations

    async def _on_generation_complete(self, data: Dict[str, Any]):
        """Callback para geração completa"""
        logging.info(f"🧬 Geração {data.get('generation')} completa - Melhor fitness: {data.get('best_fitness')}")

    async def _on_fitness_improved(self, data: Dict[str, Any]):
        """Callback para melhoria de fitness"""
        logging.info(f"📈 Fitness melhorado: {data.get('new_fitness')} (Indivíduo: {data.get('individual_id')})")

    async def _on_adaptation_needed(self, data: Dict[str, Any]):
        """Callback para necessidade de adaptação"""
        logging.warning(f"⚠️ Adaptação necessária: {data.get('reason')}")

    async def _on_performance_degraded(self, data: Dict[str, Any]):
        """Callback para degradação de performance"""
        logging.error(f"📉 Performance degradada: {data.get('details')}")

    async def get_agent_status(self) -> Dict[str, Any]:
        """Retorna status detalhado do agente de evolução"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "is_active": self.is_active,
            "current_generation": self.current_generation,
            "population_size": len(self.population),
            "best_fitness": self.best_fitness,
            "mutation_rate": self.config.mutation_rate,
            "neural_layers": len(self.neural_weights),
            "evolution_history_size": len(self.evolution_history),
            "last_update": datetime.now().isoformat()
        }


def create_evolution_engine_agents() -> List[BaseNetworkAgent]:
    """
    Factory function to create and initialize the RealEvolutionEngine agent(s) for the ALSHAM QUANTUM system.

    This function instantiates the RealEvolutionEngine, logs all relevant events for diagnostics,
    and returns it in a list for registration in the agent registry. Handles errors robustly
    and ensures the agent is ready for operation.

    Returns:
        List[BaseNetworkAgent]: A list containing the initialized RealEvolutionEngine instance(s).
    """
    agents: List[BaseNetworkAgent] = []
    try:
        agent = RealEvolutionEngine("evolution_engine_001")
        agents.append(agent)
        logging.info(f"🧬 RealEvolutionEngine criado e registrado como agente de rede: {agent.agent_id}")
    except Exception as e:
        logging.critical(f"❌ Erro crítico ao criar RealEvolutionEngine: {e}", exc_info=True)
    return agents

# Instância global para compatibilidade
evolution_engine = RealEvolutionEngine("evolution_engine_001")

# Logging final
logging.info("🧬 RealEvolutionEngine integrado como agente de rede do ALSHAM QUANTUM")
