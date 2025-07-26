"""
Motor de Evolução REAL - SUNA-ALSHAM
Implementação verdadeira com Machine Learning
SEM NÚMEROS FALSOS - TUDO MEDIDO E REAL
"""

import numpy as np
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Tuple
import logging
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import pickle
import os
from collections import deque
import hashlib

logger = logging.getLogger(__name__)

class RealEvolutionEngine:
    """Motor de evolução REAL com aprendizado de máquina verdadeiro"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.performance_history = deque(maxlen=1000)  # Últimas 1000 medições
        self.decision_history = deque(maxlen=1000)     # Últimas 1000 decisões
        self.model = None
        self.current_weights = np.random.rand(10)  # Pesos iniciais aleatórios
        self.generation = 0
        self.real_improvements = []
        
        # Métricas REAIS coletadas
        self.metrics = {
            'response_time': deque(maxlen=100),
            'accuracy': deque(maxlen=100),
            'resource_usage': deque(maxlen=100),
            'success_rate': deque(maxlen=100),
            'error_rate': deque(maxlen=100)
        }
        
        # Carregar modelo se existir
        self.load_model()
    
    def measure_real_performance(self, action_result: Dict[str, Any]) -> float:
        """
        Mede performance REAL baseada em resultados REAIS
        
        Args:
            action_result: Resultado real de uma ação executada
            
        Returns:
            Score de performance real (0-100)
        """
        # Componentes da performance REAL
        response_time = action_result.get('response_time', 1.0)
        success = action_result.get('success', False)
        error = action_result.get('error', None)
        output_quality = action_result.get('quality_score', 0.5)
        resource_used = action_result.get('resource_usage', 0.5)
        
        # Calcular score REAL
        score = 0.0
        
        # Sucesso/Falha (40% do score)
        if success and not error:
            score += 40.0
        elif success and error:
            score += 20.0  # Sucesso parcial
        
        # Tempo de resposta (20% do score)
        if response_time < 0.1:
            score += 20.0
        elif response_time < 0.5:
            score += 15.0
        elif response_time < 1.0:
            score += 10.0
        elif response_time < 2.0:
            score += 5.0
        
        # Qualidade do output (25% do score)
        score += output_quality * 25.0
        
        # Uso de recursos (15% do score)
        efficiency = 1.0 - resource_used
        score += efficiency * 15.0
        
        # Registrar métricas reais
        self.metrics['response_time'].append(response_time)
        self.metrics['success_rate'].append(1.0 if success else 0.0)
        self.metrics['error_rate'].append(1.0 if error else 0.0)
        self.metrics['resource_usage'].append(resource_used)
        self.metrics['accuracy'].append(output_quality)
        
        return score
    
    def collect_training_data(self, state: np.ndarray, action: int, result: Dict[str, Any]):
        """
        Coleta dados REAIS para treinamento
        
        Args:
            state: Estado do sistema quando decisão foi tomada
            action: Ação escolhida
            result: Resultado REAL da ação
        """
        performance = self.measure_real_performance(result)
        
        # Armazenar dados reais
        self.decision_history.append({
            'timestamp': datetime.now().isoformat(),
            'state': state.tolist(),
            'action': action,
            'performance': performance,
            'result': result
        })
        
        self.performance_history.append(performance)
    
    def train_model(self) -> bool:
        """
        Treina modelo com dados REAIS coletados
        
        Returns:
            True se treinou com sucesso
        """
        if len(self.decision_history) < 50:
            logger.warning(f"Poucos dados para treinar: {len(self.decision_history)}")
            return False
        
        try:
            # Preparar dados reais
            X = []
            y = []
            
            for decision in self.decision_history:
                features = decision['state'] + [decision['action']]
                target = decision['performance']
                X.append(features)
                y.append(target)
            
            X = np.array(X)
            y = np.array(y)
            
            # Treinar modelo real
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.model.fit(X, y)
            
            # Calcular melhoria REAL
            if len(self.performance_history) > 100:
                old_performance = np.mean(list(self.performance_history)[:50])
                new_performance = np.mean(list(self.performance_history)[-50:])
                real_improvement = ((new_performance - old_performance) / old_performance) * 100
                
                self.real_improvements.append({
                    'generation': self.generation,
                    'improvement': real_improvement,
                    'old_performance': old_performance,
                    'new_performance': new_performance,
                    'timestamp': datetime.now().isoformat()
                })
                
                logger.info(f"🎯 Melhoria REAL medida: {real_improvement:.2f}%")
            
            self.generation += 1
            self.save_model()
            return True
            
        except Exception as e:
            logger.error(f"Erro treinando modelo: {e}")
            return False
    
    def evolve_weights(self) -> np.ndarray:
        """
        Evolui pesos usando algoritmo genético REAL
        
        Returns:
            Novos pesos evoluídos
        """
        if len(self.performance_history) < 10:
            return self.current_weights
        
        # População inicial
        population_size = 50
        population = []
        
        # Criar população com mutações dos pesos atuais
        for _ in range(population_size):
            mutation = np.random.normal(0, 0.1, size=len(self.current_weights))
            new_weights = self.current_weights + mutation
            population.append(new_weights)
        
        # Avaliar cada indivíduo
        fitness_scores = []
        for weights in population:
            # Simular performance com esses pesos
            score = self._evaluate_weights(weights)
            fitness_scores.append(score)
        
        # Selecionar os melhores
        best_indices = np.argsort(fitness_scores)[-10:]  # Top 10
        
        # Criar nova geração
        new_population = []
        for _ in range(population_size):
            # Selecionar dois pais
            parent1_idx = np.random.choice(best_indices)
            parent2_idx = np.random.choice(best_indices)
            
            # Crossover
            crossover_point = np.random.randint(0, len(self.current_weights))
            child = np.concatenate([
                population[parent1_idx][:crossover_point],
                population[parent2_idx][crossover_point:]
            ])
            
            # Mutação
            if np.random.random() < 0.1:  # 10% chance
                mutation_idx = np.random.randint(0, len(child))
                child[mutation_idx] += np.random.normal(0, 0.1)
            
            new_population.append(child)
        
        # Selecionar o melhor da nova geração
        new_fitness = [self._evaluate_weights(w) for w in new_population]
        best_idx = np.argmax(new_fitness)
        
        self.current_weights = new_population[best_idx]
        return self.current_weights
    
    def _evaluate_weights(self, weights: np.ndarray) -> float:
        """Avalia performance de um conjunto de pesos"""
        # Usar últimas N decisões para avaliar
        recent_decisions = list(self.decision_history)[-20:]
        if not recent_decisions:
            return 0.0
        
        total_score = 0.0
        for decision in recent_decisions:
            # Simular decisão com esses pesos
            state = np.array(decision['state'])
            predicted_value = np.dot(weights[:len(state)], state)
            
            # Comparar com performance real
            actual_performance = decision['performance']
            error = abs(predicted_value - actual_performance)
            score = 100.0 - error
            total_score += max(0, score)
        
        return total_score / len(recent_decisions)
    
    def predict_best_action(self, state: np.ndarray, possible_actions: List[int]) -> Tuple[int, float]:
        """
        Prediz melhor ação baseada em aprendizado REAL
        
        Returns:
            (melhor_ação, confiança)
        """
        if self.model is None:
            # Sem modelo ainda, escolha aleatória
            return np.random.choice(possible_actions), 0.0
        
        best_action = None
        best_score = -float('inf')
        
        # Testar cada ação possível
        for action in possible_actions:
            features = np.concatenate([state, [action]]).reshape(1, -1)
            predicted_score = self.model.predict(features)[0]
            
            if predicted_score > best_score:
                best_score = predicted_score
                best_action = action
        
        # Calcular confiança baseada em dados reais
        confidence = min(len(self.decision_history) / 100.0, 1.0)
        
        return best_action, confidence
    
    def get_real_evolution_metrics(self) -> Dict[str, Any]:
        """Retorna métricas REAIS de evolução"""
        if not self.performance_history:
            return {
                'status': 'no_data',
                'message': 'Ainda coletando dados'
            }
        
        current_perf = np.mean(list(self.performance_history)[-10:]) if len(self.performance_history) >= 10 else 0
        initial_perf = np.mean(list(self.performance_history)[:10]) if len(self.performance_history) >= 10 else current_perf
        
        # Calcular tendência real
        if len(self.performance_history) >= 20:
            x = np.arange(len(self.performance_history)).reshape(-1, 1)
            y = np.array(list(self.performance_history))
            
            trend_model = LinearRegression()
            trend_model.fit(x, y)
            trend = trend_model.coef_[0]
        else:
            trend = 0.0
        
        return {
            'current_performance': float(current_perf),
            'initial_performance': float(initial_perf),
            'evolution_percentage': float(((current_perf - initial_perf) / max(initial_perf, 1)) * 100),
            'total_decisions': len(self.decision_history),
            'generation': self.generation,
            'trend': float(trend),
            'is_improving': trend > 0,
            'real_improvements': self.real_improvements[-5:],  # Últimas 5
            'metrics': {
                'avg_response_time': float(np.mean(self.metrics['response_time'])) if self.metrics['response_time'] else 0,
                'avg_success_rate': float(np.mean(self.metrics['success_rate'])) if self.metrics['success_rate'] else 0,
                'avg_accuracy': float(np.mean(self.metrics['accuracy'])) if self.metrics['accuracy'] else 0
            }
        }
    
    def save_model(self):
        """Salva modelo treinado"""
        if self.model is None:
            return
        
        model_dir = f"models/{self.agent_id}"
        os.makedirs(model_dir, exist_ok=True)
        
        # Salvar modelo
        with open(f"{model_dir}/model_gen_{self.generation}.pkl", 'wb') as f:
            pickle.dump(self.model, f)
        
        # Salvar histórico
        with open(f"{model_dir}/history.json", 'w') as f:
            json.dump({
                'performance_history': list(self.performance_history),
                'generation': self.generation,
                'real_improvements': self.real_improvements,
                'current_weights': self.current_weights.tolist()
            }, f)
    
    def load_model(self):
        """Carrega modelo salvo"""
        model_dir = f"models/{self.agent_id}"
        if not os.path.exists(model_dir):
            return
        
        # Encontrar modelo mais recente
        model_files = [f for f in os.listdir(model_dir) if f.startswith('model_gen_')]
        if not model_files:
            return
        
        latest_model = sorted(model_files)[-1]
        
        # Carregar modelo
        with open(f"{model_dir}/{latest_model}", 'rb') as f:
            self.model = pickle.load(f)
        
        # Carregar histórico
        history_path = f"{model_dir}/history.json"
        if os.path.exists(history_path):
            with open(history_path, 'r') as f:
                data = json.load(f)
                self.performance_history = deque(data['performance_history'], maxlen=1000)
                self.generation = data['generation']
                self.real_improvements = data['real_improvements']
                self.current_weights = np.array(data['current_weights'])
        
        logger.info(f"✅ Modelo carregado: geração {self.generation}")

# Integração com agentes existentes
class EvolvableAgent:
    """Mixin para tornar qualquer agente evoluível"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.evolution_engine = RealEvolutionEngine(self.agent_id)
        self.decisions_count = 0
    
    async def make_evolved_decision(self, state: Dict[str, Any], possible_actions: List[str]) -> str:
        """
        Toma decisão usando evolução real
        
        Args:
            state: Estado atual
            possible_actions: Ações possíveis
            
        Returns:
            Ação escolhida
        """
        # Converter estado para vetor
        state_vector = self._state_to_vector(state)
        
        # Mapear ações para índices
        action_map = {i: action for i, action in enumerate(possible_actions)}
        action_indices = list(range(len(possible_actions)))
        
        # Obter predição do modelo
        best_action_idx, confidence = self.evolution_engine.predict_best_action(
            state_vector, action_indices
        )
        
        # Executar ação
        chosen_action = action_map[best_action_idx]
        
        # Executar e medir resultado REAL
        start_time = datetime.now()
        result = await self._execute_action(chosen_action, state)
        end_time = datetime.now()
        
        # Coletar dados reais
        result['response_time'] = (end_time - start_time).total_seconds()
        self.evolution_engine.collect_training_data(state_vector, best_action_idx, result)
        
        # Treinar periodicamente
        self.decisions_count += 1
        if self.decisions_count % 50 == 0:
            asyncio.create_task(self._train_in_background())
        
        return chosen_action
    
    async def _train_in_background(self):
        """Treina modelo em background"""
        logger.info(f"🧠 {self.agent_id} iniciando treinamento...")
        success = self.evolution_engine.train_model()
        if success:
            # Evoluir pesos
            new_weights = self.evolution_engine.evolve_weights()
            logger.info(f"✅ {self.agent_id} evoluiu! Geração {self.evolution_engine.generation}")
    
    def _state_to_vector(self, state: Dict[str, Any]) -> np.ndarray:
        """Converte estado para vetor numérico"""
        # Implementar conversão específica para cada tipo de agente
        # Exemplo genérico:
        vector = []
        for key, value in sorted(state.items()):
            if isinstance(value, (int, float)):
                vector.append(value)
            elif isinstance(value, bool):
                vector.append(1.0 if value else 0.0)
            elif isinstance(value, str):
                # Hash da string para número
                vector.append(int(hashlib.md5(value.encode()).hexdigest()[:8], 16) / 1e9)
        
        return np.array(vector)
    
    async def _execute_action(self, action: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Executa ação e retorna resultado real"""
        # Implementar execução específica para cada agente
        # Deve retornar:
        # {
        #     'success': bool,
        #     'error': str or None,
        #     'quality_score': float (0-1),
        #     'resource_usage': float (0-1),
        #     'output': Any
        # }
        raise NotImplementedError("Cada agente deve implementar _execute_action")
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """Retorna status real da evolução"""
        return self.evolution_engine.get_real_evolution_metrics()
