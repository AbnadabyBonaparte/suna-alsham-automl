#!/usr/bin/env python3
"""
Real Evolution Engine - Motor de Evolução Adaptativa do ALSHAM QUANTUM
Agente especializado em evolução contínua e otimização adaptativa do sistema.
Versão corrigida com integração completa ao BaseNetworkAgent.
"""

import asyncio
import logging
import time
import random
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

# Importações corrigidas para compatibilidade
from suna_alsham_core.multi_agent_network import (
    BaseNetworkAgent,
    AgentType,
    MessageType,
    Priority,
    AgentMessage
)

logger = logging.getLogger(__name__)

class EvolutionStrategy(Enum):
    """Estratégias de evolução disponíveis."""
    GENETIC_ALGORITHM = "genetic_algorithm"
    NEURAL_EVOLUTION = "neural_evolution"
    ADAPTIVE_LEARNING = "adaptive_learning"
    GRADIENT_BASED = "gradient_based"
    SWARM_OPTIMIZATION = "swarm_optimization"

class FitnessMetric(Enum):
    """Métricas de fitness para avaliação."""
    PERFORMANCE = "performance"
    EFFICIENCY = "efficiency"
    ADAPTABILITY = "adaptability"
    STABILITY = "stability"
    INNOVATION = "innovation"

@dataclass
class EvolutionConfig:
    """Configuração para o motor de evolução."""
    learning_rate: float = 0.001
    mutation_rate: float = 0.01
    population_size: int = 50
    generations_limit: int = 100
    fitness_threshold: float = 0.95
    adaptation_window: timedelta = field(default_factory=lambda: timedelta(hours=1))
    neural_layers: List[int] = field(default_factory=lambda: [128, 64, 32])
    optimization_targets: Set[str] = field(default_factory=lambda: {"accuracy", "efficiency"})
    evolution_strategy: EvolutionStrategy = EvolutionStrategy.GENETIC_ALGORITHM

@dataclass
class Individual:
    """Representa um indivíduo na população evolutiva."""
    id: str
    genes: Dict[str, float]
    fitness: float = 0.0
    generation: int = 0
    mutations: int = 0
    performance_history: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class EvolutionMetrics:
    """Métricas de evolução para monitoramento."""
    generation: int
    best_fitness: float
    average_fitness: float
    population_diversity: float
    convergence_rate: float
    mutation_success_rate: float
    timestamp: datetime = field(default_factory=datetime.now)

class RealEvolutionEngine(BaseNetworkAgent):
    """
    Motor de Evolução Real do ALSHAM QUANTUM.
    Agente especializado em evolução adaptativa contínua do sistema.
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        
        # Configuração do agente
        self.capabilities.extend([
            "adaptive_learning",
            "neural_evolution",
            "performance_optimization",
            "system_adaptation",
            "predictive_modeling",
            "autonomous_improvement",
            "population_management",
            "fitness_evaluation",
            "genetic_operations"
        ])
        
        # Configuração de evolução
        self.config = EvolutionConfig()
        self.current_generation = 0
        self.population: List[Individual] = []
        self.best_individual: Optional[Individual] = None
        self.evolution_history: List[EvolutionMetrics] = []
        
        # Estado interno
        self.is_evolving = False
        self.evolution_task: Optional[asyncio.Task] = None
        self.last_evolution_time = datetime.now()
        
        # Estatísticas
        self.total_generations = 0
        self.total_mutations = 0
        self.successful_adaptations = 0
        
        logger.info(f"🧬 {self.agent_id} (Evolution Engine) inicializado")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas pelo agente de evolução."""
        try:
            content = message.content
            message_type = content.get("type", "unknown")
            
            if message_type == "start_evolution":
                await self._handle_start_evolution(message)
            elif message_type == "stop_evolution":
                await self._handle_stop_evolution(message)
            elif message_type == "evaluate_fitness":
                await self._handle_evaluate_fitness(message)
            elif message_type == "adaptation_request":
                await self._handle_adaptation_request(message)
            elif message_type == "get_evolution_status":
                await self._handle_get_evolution_status(message)
            elif message_type == "update_config":
                await self._handle_update_config(message)
            elif message_type == "force_mutation":
                await self._handle_force_mutation(message)
            elif message_type == "get_best_individual":
                await self._handle_get_best_individual(message)
            else:
                logger.debug(f"🧬 Tipo de mensagem não reconhecido: {message_type}")
                await self.publish_error_response(message, f"Tipo não reconhecido: {message_type}")
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro interno: {str(e)}")

    async def _handle_start_evolution(self, message: AgentMessage):
        """Inicia processo evolutivo."""
        try:
            content = message.content
            strategy = content.get("strategy", "genetic_algorithm")
            generations = content.get("generations", 10)
            target_fitness = content.get("target_fitness", 0.9)
            
            if self.is_evolving:
                await self.publish_response(message, {
                    "status": "already_running",
                    "current_generation": self.current_generation
                })
                return
            
            # Inicializar população se necessário
            if not self.population:
                await self._initialize_population()
            
            # Configurar parâmetros
            self.config.evolution_strategy = EvolutionStrategy(strategy)
            self.config.generations_limit = generations
            self.config.fitness_threshold = target_fitness
            
            # Iniciar evolução
            self.is_evolving = True
            self.evolution_task = asyncio.create_task(self._evolution_loop())
            
            await self.publish_response(message, {
                "status": "evolution_started",
                "strategy": strategy,
                "generations_limit": generations,
                "population_size": len(self.population),
                "target_fitness": target_fitness
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao iniciar evolução: {str(e)}")

    async def _handle_stop_evolution(self, message: AgentMessage):
        """Para processo evolutivo."""
        try:
            if not self.is_evolving:
                await self.publish_response(message, {"status": "not_running"})
                return
            
            self.is_evolving = False
            
            if self.evolution_task:
                self.evolution_task.cancel()
                try:
                    await self.evolution_task
                except asyncio.CancelledError:
                    pass
            
            await self.publish_response(message, {
                "status": "evolution_stopped",
                "final_generation": self.current_generation,
                "best_fitness": self.best_individual.fitness if self.best_individual else 0.0
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao parar evolução: {str(e)}")

    async def _handle_evaluate_fitness(self, message: AgentMessage):
        """Avalia fitness de indivíduos."""
        try:
            content = message.content
            individual_id = content.get("individual_id")
            performance_data = content.get("performance_data", {})
            
            individual = self._find_individual(individual_id)
            if not individual:
                await self.publish_error_response(message, "Indivíduo não encontrado")
                return
            
            # Calcular novo fitness
            new_fitness = await self._calculate_fitness(individual, performance_data)
            individual.fitness = new_fitness
            
            # Atualizar histórico
            individual.performance_history.append({
                "timestamp": datetime.now().isoformat(),
                "fitness": new_fitness,
                "performance_data": performance_data
            })
            
            # Verificar se é o melhor
            if not self.best_individual or new_fitness > self.best_individual.fitness:
                self.best_individual = individual
                await self._notify_fitness_improvement(individual)
            
            await self.publish_response(message, {
                "individual_id": individual_id,
                "new_fitness": new_fitness,
                "is_best": individual == self.best_individual
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na avaliação: {str(e)}")

    async def _handle_adaptation_request(self, message: AgentMessage):
        """Processa solicitação de adaptação."""
        try:
            content = message.content
            adaptation_type = content.get("adaptation_type", "performance")
            urgency = content.get("urgency", "normal")
            target_metrics = content.get("target_metrics", {})
            
            if urgency == "critical":
                result = await self._emergency_adaptation(adaptation_type, target_metrics)
            else:
                result = await self._gradual_adaptation(adaptation_type, target_metrics)
            
            self.successful_adaptations += 1
            
            await self.publish_response(message, {
                "adaptation_result": result,
                "adaptation_type": adaptation_type,
                "urgency": urgency,
                "successful_adaptations": self.successful_adaptations
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na adaptação: {str(e)}")

    async def _handle_get_evolution_status(self, message: AgentMessage):
        """Retorna status atual da evolução."""
        try:
            status = {
                "is_evolving": self.is_evolving,
                "current_generation": self.current_generation,
                "total_generations": self.total_generations,
                "population_size": len(self.population),
                "best_fitness": self.best_individual.fitness if self.best_individual else 0.0,
                "average_fitness": self._calculate_average_fitness(),
                "mutation_rate": self.config.mutation_rate,
                "evolution_strategy": self.config.evolution_strategy.value,
                "last_evolution_time": self.last_evolution_time.isoformat(),
                "successful_adaptations": self.successful_adaptations,
                "total_mutations": self.total_mutations,
                "population_diversity": self._calculate_population_diversity()
            }
            
            await self.publish_response(message, {"evolution_status": status})
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao obter status: {str(e)}")

    async def _handle_update_config(self, message: AgentMessage):
        """Atualiza configuração de evolução."""
        try:
            content = message.content
            config_updates = content.get("config_updates", {})
            
            # Atualizar configurações
            for key, value in config_updates.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                    logger.info(f"🔧 Config atualizada: {key} = {value}")
            
            await self.publish_response(message, {
                "status": "config_updated",
                "updated_fields": list(config_updates.keys()),
                "current_config": self._get_config_dict()
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao atualizar config: {str(e)}")

    async def _handle_force_mutation(self, message: AgentMessage):
        """Força mutação em indivíduos específicos."""
        try:
            content = message.content
            individual_ids = content.get("individual_ids", [])
            mutation_strength = content.get("mutation_strength", 0.1)
            
            mutations_applied = 0
            
            for individual_id in individual_ids:
                individual = self._find_individual(individual_id)
                if individual:
                    self._mutate_individual(individual, mutation_strength)
                    mutations_applied += 1
            
            self.total_mutations += mutations_applied
            
            await self.publish_response(message, {
                "mutations_applied": mutations_applied,
                "total_mutations": self.total_mutations,
                "mutation_strength": mutation_strength
            })
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro na mutação forçada: {str(e)}")

    async def _handle_get_best_individual(self, message: AgentMessage):
        """Retorna o melhor indivíduo atual."""
        try:
            if not self.best_individual:
                await self.publish_response(message, {"best_individual": None})
                return
            
            best_data = {
                "id": self.best_individual.id,
                "fitness": self.best_individual.fitness,
                "generation": self.best_individual.generation,
                "genes": self.best_individual.genes,
                "mutations": self.best_individual.mutations,
                "created_at": self.best_individual.created_at.isoformat(),
                "performance_history_size": len(self.best_individual.performance_history)
            }
            
            await self.publish_response(message, {"best_individual": best_data})
            
        except Exception as e:
            await self.publish_error_response(message, f"Erro ao obter melhor indivíduo: {str(e)}")

    async def _initialize_population(self):
        """Inicializa população evolutiva."""
        self.population = []
        
        for i in range(self.config.population_size):
            individual = Individual(
                id=f"individual_{self.current_generation}_{i}",
                genes=self._generate_random_genes(),
                generation=self.current_generation
            )
            self.population.append(individual)
        
        logger.info(f"🧬 População inicializada: {len(self.population)} indivíduos")

    def _generate_random_genes(self) -> Dict[str, float]:
        """Gera genes aleatórios para um indivíduo."""
        return {
            "learning_efficiency": random.uniform(0.1, 1.0),
            "adaptation_speed": random.uniform(0.1, 1.0),
            "memory_optimization": random.uniform(0.1, 1.0),
            "processing_priority": random.uniform(0.1, 1.0),
            "error_tolerance": random.uniform(0.01, 0.2),
            "innovation_factor": random.uniform(0.0, 0.8),
            "stability_factor": random.uniform(0.2, 1.0),
            "energy_efficiency": random.uniform(0.1, 1.0)
        }

    async def _evolution_loop(self):
        """Loop principal de evolução."""
        try:
            generation_count = 0
            
            while self.is_evolving and generation_count < self.config.generations_limit:
                start_time = time.time()
                
                # Avaliar fitness da população
                await self._evaluate_population()
                
                # Verificar critério de parada
                if self.best_individual and self.best_individual.fitness >= self.config.fitness_threshold:
                    logger.info(f"🎯 Fitness threshold atingido: {self.best_individual.fitness}")
                    break
                
                # Seleção, reprodução e mutação
                await self._evolve_generation()
                
                # Atualizar estatísticas
                self.current_generation += 1
                self.total_generations += 1
                generation_count += 1
                
                # Registrar métricas
                metrics = await self._calculate_generation_metrics()
                self.evolution_history.append(metrics)
                
                # Notificar progresso
                await self._notify_generation_complete(metrics)
                
                # Log de progresso
                elapsed = time.time() - start_time
                logger.info(f"🧬 Geração {self.current_generation} completa em {elapsed:.2f}s - Melhor fitness: {self.best_individual.fitness if self.best_individual else 0.0:.4f}")
                
                # Pequeno delay para não sobrecarregar
                await asyncio.sleep(0.1)
            
            self.is_evolving = False
            self.last_evolution_time = datetime.now()
            
            logger.info(f"🏁 Evolução completa: {generation_count} gerações, melhor fitness: {self.best_individual.fitness if self.best_individual else 0.0:.4f}")
            
        except asyncio.CancelledError:
            logger.info("🛑 Loop de evolução cancelado")
        except Exception as e:
            logger.error(f"❌ Erro no loop de evolução: {e}", exc_info=True)
            self.is_evolving = False

    async def _evaluate_population(self):
        """Avalia fitness de toda a população."""
        for individual in self.population:
            if individual.fitness == 0.0:  # Só avaliar se ainda não foi avaliado
                individual.fitness = await self._calculate_fitness(individual)
                
                # Atualizar melhor indivíduo
                if not self.best_individual or individual.fitness > self.best_individual.fitness:
                    self.best_individual = individual
                    await self._notify_fitness_improvement(individual)

    async def _calculate_fitness(self, individual: Individual, performance_data: Optional[Dict[str, Any]] = None) -> float:
        """Calcula fitness de um indivíduo."""
        genes = individual.genes
        
        # Fitness baseado nos genes (simulação)
        base_fitness = (
            genes.get("learning_efficiency", 0.5) * 0.25 +
            genes.get("adaptation_speed", 0.5) * 0.20 +
            genes.get("memory_optimization", 0.5) * 0.15 +
            genes.get("processing_priority", 0.5) * 0.15 +
            genes.get("stability_factor", 0.5) * 0.15 +
            genes.get("energy_efficiency", 0.5) * 0.10
        )
        
        # Penalidade por erro excessivo
        error_penalty = genes.get("error_tolerance", 0.1) * 0.5
        base_fitness = max(0.0, base_fitness - error_penalty)
        
        # Bônus por inovação (mas não muito)
        innovation_bonus = genes.get("innovation_factor", 0.0) * 0.05
        base_fitness += innovation_bonus
        
        # Se há dados de performance real, usar eles
        if performance_data:
            real_performance = (
                performance_data.get("accuracy", 0.5) * 0.4 +
                performance_data.get("efficiency", 0.5) * 0.3 +
                performance_data.get("stability", 0.5) * 0.3
            )
            # Média ponderada entre fitness simulado e real
            base_fitness = base_fitness * 0.3 + real_performance * 0.7
        
        return min(1.0, max(0.0, base_fitness))

    async def _evolve_generation(self):
        """Evolui uma geração através de seleção, reprodução e mutação."""
        # Ordenar por fitness
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # Selecionar elite (top 20%)
        elite_size = max(1, len(self.population) // 5)
        elite = self.population[:elite_size]
        
        # Gerar nova população
        new_population = elite.copy()  # Manter elite
        
        while len(new_population) < self.config.population_size:
            # Seleção de pais (torneio)
            parent1 = self._tournament_selection()
            parent2 = self._tournament_selection()
            
            # Crossover
            child = self._crossover(parent1, parent2)
            
            # Mutação
            if random.random() < self.config.mutation_rate:
                self._mutate_individual(child)
                self.total_mutations += 1
            
            new_population.append(child)
        
        self.population = new_population

    def _tournament_selection(self, tournament_size: int = 3) -> Individual:
        """Seleção por torneio."""
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=lambda x: x.fitness)

    def _crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        """Realiza crossover entre dois pais."""
        child_genes = {}
        
        for gene_name in parent1.genes.keys():
            # Crossover uniforme
            if random.random() < 0.5:
                child_genes[gene_name] = parent1.genes[gene_name]
            else:
                child_genes[gene_name] = parent2.genes[gene_name]
        
        return Individual(
            id=f"child_{self.current_generation}_{random.randint(1000, 9999)}",
            genes=child_genes,
            generation=self.current_generation + 1
        )

    def _mutate_individual(self, individual: Individual, mutation_strength: float = None):
        """Aplica mutação em um indivíduo."""
        if mutation_strength is None:
            mutation_strength = 0.1
        
        for gene_name in individual.genes.keys():
            if random.random() < self.config.mutation_rate:
                # Mutação gaussiana
                mutation = random.gauss(0, mutation_strength)
                individual.genes[gene_name] = max(0.0, min(1.0, individual.genes[gene_name] + mutation))
        
        individual.mutations += 1

    def _find_individual(self, individual_id: str) -> Optional[Individual]:
        """Encontra indivíduo por ID."""
        return next((ind for ind in self.population if ind.id == individual_id), None)

    def _calculate_average_fitness(self) -> float:
        """Calcula fitness médio da população."""
        if not self.population:
            return 0.0
        return sum(ind.fitness for ind in self.population) / len(self.population)

    def _calculate_population_diversity(self) -> float:
        """Calcula diversidade da população."""
        if len(self.population) < 2:
            return 0.0
        
        total_distance = 0.0
        comparisons = 0
        
        for i in range(len(self.population)):
            for j in range(i + 1, len(self.population)):
                distance = self._calculate_genetic_distance(self.population[i], self.population[j])
                total_distance += distance
                comparisons += 1
        
        return total_distance / comparisons if comparisons > 0 else 0.0

    def _calculate_genetic_distance(self, ind1: Individual, ind2: Individual) -> float:
        """Calcula distância genética entre dois indivíduos."""
        distance = 0.0
        gene_count = 0
        
        for gene_name in ind1.genes.keys():
            if gene_name in ind2.genes:
                distance += abs(ind1.genes[gene_name] - ind2.genes[gene_name])
                gene_count += 1
        
        return distance / gene_count if gene_count > 0 else 0.0

    async def _calculate_generation_metrics(self) -> EvolutionMetrics:
        """Calcula métricas da geração atual."""
        avg_fitness = self._calculate_average_fitness()
        diversity = self._calculate_population_diversity()
        
        # Calcular taxa de convergência (diferença entre melhor e médio)
        best_fitness = self.best_individual.fitness if self.best_individual else 0.0
        convergence_rate = best_fitness - avg_fitness
        
        # Taxa de sucesso de mutação (simplificada)
        mutation_success_rate = min(1.0, self.total_mutations / max(1, self.total_generations))
        
        return EvolutionMetrics(
            generation=self.current_generation,
            best_fitness=best_fitness,
            average_fitness=avg_fitness,
            population_diversity=diversity,
            convergence_rate=convergence_rate,
            mutation_success_rate=mutation_success_rate
        )

    async def _emergency_adaptation(self, adaptation_type: str, target_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza adaptação de emergência."""
        logger.warning(f"⚠️ Adaptação de emergência: {adaptation_type}")
        
        # Aumentar taxa de mutação temporariamente
        original_mutation_rate = self.config.mutation_rate
        self.config.mutation_rate = min(1.0, original_mutation_rate * 3)
        
        # Forçar mutação em toda a população
        for individual in self.population:
            self._mutate_individual(individual, 0.2)  # Mutação mais forte
        
        # Executar algumas gerações rapidamente
        if not self.is_evolving:
            for _ in range(5):
                await self._evolve_generation()
                self.current_generation += 1
        
        # Restaurar taxa de mutação
        self.config.mutation_rate = original_mutation_rate
        
        return {
            "type": "emergency",
            "mutation_rate_used": self.config.mutation_rate * 3,
            "generations_evolved": 5,
            "new_best_fitness": self.best_individual.fitness if self.best_individual else 0.0
        }

    async def _gradual_adaptation(self, adaptation_type: str, target_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza adaptação gradual."""
        logger.info(f"🔄 Adaptação gradual: {adaptation_type}")
        
        # Ajustar parâmetros gradualmente
        self.config.mutation_rate = min(0.5, self.config.mutation_rate * 1.2)
        
        # Se não estiver evoluindo, executar algumas gerações
        if not self.is_evolving:
            for _ in range(3):
                await self._evolve_generation()
                self.current_generation += 1
        
        return {
            "type": "gradual",
            "new_mutation_rate": self.config.mutation_rate,
            "generations_evolved": 3,
            "adaptation_type": adaptation_type
        }

    async def _notify_fitness_improvement(self, individual: Individual):
        """Notifica sobre melhoria de fitness."""
        try:
            notification = self.create_message(
                recipient_id="broadcast",
                message_type=MessageType.NOTIFICATION,
                content={
                    "type": "fitness_improved",
                    "individual_id": individual.id,
                    "new_fitness": individual.fitness,
                    "generation": individual.generation,
                    "genes": individual.genes
                },
                priority=Priority.NORMAL
            )
            
            await self.message_bus.publish(notification)
            
        except Exception as e:
            logger.error(f"Erro ao notificar melhoria de fitness: {e}")

    async def _notify_generation_complete(self, metrics: EvolutionMetrics):
        """Notifica sobre geração completa."""
        try:
            notification = self.create_message(
                recipient_id="broadcast",
                message_type=MessageType.NOTIFICATION,
                content={
                    "type": "generation_complete",
                    "generation": metrics.generation,
                    "best_fitness": metrics.best_fitness,
                    "average_fitness": metrics.average_fitness,
                    "population_diversity": metrics.population_diversity
                },
                priority=Priority.LOW
            )
            
            await self.message_bus.publish(notification)
            
        except Exception as e:
            logger.error(f"Erro ao notificar geração completa: {e}")

    def _get_config_dict(self) -> Dict[str, Any]:
        """Retorna configuração como dicionário."""
        return {
            "learning_rate": self.config.learning_rate,
            "mutation_rate": self.config.mutation_rate,
            "population_size": self.config.population_size,
            "generations_limit": self.config.generations_limit,
            "fitness_threshold": self.config.fitness_threshold,
            "evolution_strategy": self.config.evolution_strategy.value,
            "neural_layers": self.config.neural_layers,
            "optimization_targets": list(self.config.optimization_targets)
        }

def create_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Factory function para criar o RealEvolutionEngine.
    
    Cria e inicializa o agente de evolução adaptativa do sistema ALSHAM QUANTUM.
    
    Args:
        message_bus: MessageBus para comunicação entre agentes.
        
    Returns:
        List[BaseNetworkAgent]: Lista contendo o RealEvolutionEngine.
    """
    agents: List[BaseNetworkAgent] = []
    
    try:
        logger.info("🧬 [Factory] Criando RealEvolutionEngine...")
        
        # Criar o agente
        agent = RealEvolutionEngine("evolution_engine_001", message_bus)
        agents.append(agent)
        
        logger.info(f"✅ RealEvolutionEngine criado: {agent.agent_id}")
        logger.info(f"🔧 Capabilities: {', '.join(agent.capabilities)}")
        
    except Exception as e:
        logger.critical(f"❌ Erro ao criar RealEvolutionEngine: {e}", exc_info=True)
    
    return agents
