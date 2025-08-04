#!/usr/bin/env python3
"""
Quantum Evolution Engine - O Coração da Auto-Evolução do ALSHAM QUANTUM.
[Quantum Version 2.0 - Advanced Self-Learning with Synthetic Intelligence]
"""
import asyncio
import json
import logging
import pickle
import random
import time
from collections import deque
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import numpy as np
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.model_selection import cross_val_score, GridSearchCV
    from sklearn.metrics import mean_squared_error, r2_score
    import joblib
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentMessage, AgentType, MessageType, Priority

logger = logging.getLogger(__name__)

class LearningPhase(Enum):
    """Fases do aprendizado quantum."""
    BOOTSTRAP = "bootstrap"
    ACTIVE_LEARNING = "active_learning"
    OPTIMIZATION = "optimization"
    MASTERY = "mastery"

class DataType(Enum):
    """Tipos de dados de treinamento."""
    REAL = "real"
    SYNTHETIC = "synthetic"
    HYBRID = "hybrid"

@dataclass
class TrainingDataPoint:
    agent_id: str
    state_features: Dict[str, Any]
    action_taken: Dict[str, Any]
    outcome_reward: float
    timestamp: datetime = field(default_factory=datetime.now)
    data_type: DataType = DataType.REAL
    confidence_score: float = 1.0
    context_metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ModelVersion:
    """Versão do modelo com métricas completas."""
    version: int
    model_path: str
    creation_time: datetime
    training_samples: int
    cross_val_score: float
    r2_score: float
    feature_importance: Dict[str, float]
    hyperparameters: Dict[str, Any]
    performance_trend: List[float]

@dataclass
class LearningMetrics:
    """Métricas completas de aprendizado."""
    total_samples: int = 0
    synthetic_samples: int = 0
    real_samples: int = 0
    current_phase: LearningPhase = LearningPhase.BOOTSTRAP
    model_versions: List[ModelVersion] = field(default_factory=list)
    learning_velocity: float = 0.0
    prediction_accuracy: float = 0.0
    adaptation_rate: float = 0.0
    quantum_coherence: float = 1.0

class QuantumEvolutionEngine(BaseNetworkAgent):
    """
    Engine de Evolução Quântico - Superinteligência Auto-Adaptativa.
    
    Capacidades Quantum:
    - Geração sintética de dados de treinamento
    - Aprendizado multi-dimensional contínuo
    - Auto-otimização de hiperparâmetros
    - Predição de performance futura
    - Adaptação em tempo real
    - Manutenção de coerência quântica
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "quantum_self_evolution",
            "synthetic_data_generation", 
            "predictive_analytics",
            "auto_optimization",
            "meta_learning",
            "quantum_coherence"
        ])
        
        # Inicialização quantum
        self.training_data: deque = deque(maxlen=10000)  # Histórico expandido
        self.model_storage_path = Path("./quantum_models")
        self.model_storage_path.mkdir(exist_ok=True)
        
        self.learning_metrics = LearningMetrics()
        self.active_models: Dict[str, Any] = {}
        self.synthetic_generators: Dict[str, Any] = {}
        self.performance_history: deque = deque(maxlen=1000)
        
        # Configurações quantum
        self.min_samples_for_learning = 3  # Reduzido para bootstrap mais rápido
        self.synthetic_data_ratio = 0.3  # 30% dados sintéticos
        self.learning_cycle_interval = 300  # 5 minutos
        self.auto_optimization_threshold = 0.1  # 10% melhoria mínima
        
        if not SKLEARN_AVAILABLE:
            self.status = "degraded"
            self.model, self.vectorizer = None, None
            logger.critical("❌ Dependências de ML não encontradas. QuantumEvolutionEngine em modo degradado.")
        else:
            self.status = "active"
            self._initialize_quantum_models()
            
        # Iniciar ciclo de evolução quantum
        self.evolution_task = asyncio.create_task(self._quantum_evolution_loop())
        self.synthetic_task = asyncio.create_task(self._synthetic_data_generator())
        
        logger.info(f"🧬 {self.agent_id} (Quantum Evolution Engine) inicializado - Superinteligência ativa.")

    def _initialize_quantum_models(self):
        """Inicializa múltiplos modelos para aprendizado ensemble."""
        self.active_models = {
            "primary": RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            ),
            "secondary": GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            )
        }
        
        self.vectorizer = DictVectorizer(sparse=False)
        
        # Carrega modelos existentes se disponíveis
        self._load_existing_models()
        
        logger.info("🧬 Modelos quantum inicializados com arquitetura ensemble.")

    def _load_existing_models(self):
        """Carrega modelos pré-treinados se existirem."""
        try:
            model_files = list(self.model_storage_path.glob("quantum_model_v*.pkl"))
            if model_files:
                latest_model = max(model_files, key=lambda f: f.stat().st_mtime)
                
                with open(latest_model, 'rb') as f:
                    saved_data = pickle.load(f)
                
                self.active_models = saved_data['models']
                self.vectorizer = saved_data['vectorizer']
                self.learning_metrics = saved_data['metrics']
                
                logger.info(f"✅ Modelos quantum carregados: {latest_model.name}")
        except Exception as e:
            logger.warning(f"⚠️ Falha ao carregar modelos existentes: {e}")

    async def _quantum_evolution_loop(self):
        """Ciclo principal de evolução quantum com inteligência avançada."""
        cycle_count = 0
        
        while True:
            await asyncio.sleep(self.learning_cycle_interval)
            cycle_count += 1
            
            if self.status != "active":
                continue
                
            logger.info("=" * 60)
            logger.info(f"🧬 [Quantum Evolution] Iniciando Ciclo #{cycle_count}")
            logger.info(f"📊 Samples: {len(self.training_data)} | Fase: {self.learning_metrics.current_phase.value}")
            
            try:
                # Fase 1: Verificar se precisa de dados sintéticos
                if len(self.training_data) < self.min_samples_for_learning:
                    await self._generate_bootstrap_data()
                
                # Fase 2: Executar aprendizado quantum
                evolution_result = await self._execute_quantum_learning()
                
                # Fase 3: Avaliar e otimizar
                await self._evaluate_and_optimize(evolution_result)
                
                # Fase 4: Atualizar fase de aprendizado
                self._update_learning_phase()
                
                # Fase 5: Relatório de evolução
                self._log_evolution_report(cycle_count, evolution_result)
                
            except Exception as e:
                logger.error(f"❌ [Quantum Evolution] Erro crítico no ciclo: {e}", exc_info=True)
            
            logger.info("=" * 60)

    async def _generate_bootstrap_data(self):
        """Gera dados sintéticos para bootstrap do sistema."""
        logger.info("🔬 Gerando dados sintéticos para bootstrap...")
        
        # Templates de cenários comuns
        scenarios = [
            {
                "agent_type": "web_search",
                "task_complexity": "simple",
                "response_time": 2.5,
                "success_rate": 0.95,
                "outcome": 1.0
            },
            {
                "agent_type": "content_creation",
                "task_complexity": "moderate", 
                "response_time": 8.0,
                "success_rate": 0.85,
                "outcome": 0.8
            },
            {
                "agent_type": "notification",
                "task_complexity": "simple",
                "response_time": 1.5,
                "success_rate": 0.90,
                "outcome": 0.9
            },
            {
                "agent_type": "orchestration",
                "task_complexity": "complex",
                "response_time": 15.0,
                "success_rate": 0.75,
                "outcome": 0.7
            }
        ]
        
        synthetic_count = 0
        for _ in range(10):  # Gera 10 pontos sintéticos por ciclo
            scenario = random.choice(scenarios)
            
            # Adiciona variação realística
            noise_factor = random.uniform(0.8, 1.2)
            
            synthetic_point = TrainingDataPoint(
                agent_id=f"{scenario['agent_type']}_001",
                state_features={
                    "task_complexity": scenario["task_complexity"],
                    "system_load": random.uniform(0.3, 0.9),
                    "time_of_day": random.randint(0, 23),
                    "previous_success_rate": scenario["success_rate"],
                    "estimated_duration": scenario["response_time"] * noise_factor
                },
                action_taken={
                    "strategy_chosen": random.choice(["conservative", "aggressive", "balanced"]),
                    "retry_count": random.randint(0, 2),
                    "provider_used": random.choice(["primary", "secondary", "fallback"])
                },
                outcome_reward=scenario["outcome"] * noise_factor,
                data_type=DataType.SYNTHETIC,
                confidence_score=0.7,  # Menor confiança para dados sintéticos
                context_metadata={
                    "generated_by": "quantum_bootstrap",
                    "scenario_template": scenario["agent_type"],
                    "noise_factor": noise_factor
                }
            )
            
            self.training_data.append(synthetic_point)
            synthetic_count += 1
        
        self.learning_metrics.synthetic_samples += synthetic_count
        self.learning_metrics.total_samples = len(self.training_data)
        
        logger.info(f"✅ {synthetic_count} pontos sintéticos gerados para bootstrap.")

    async def _synthetic_data_generator(self):
        """Gerador contínuo de dados sintéticos baseado em padrões aprendidos."""
        while True:
            await asyncio.sleep(600)  # A cada 10 minutos
            
            if (self.status == "active" and 
                len(self.training_data) > 20 and 
                self.learning_metrics.current_phase != LearningPhase.BOOTSTRAP):
                
                try:
                    await self._generate_intelligent_synthetic_data()
                except Exception as e:
                    logger.error(f"❌ Erro na geração sintética inteligente: {e}")

    async def _generate_intelligent_synthetic_data(self):
        """Gera dados sintéticos baseados em padrões reais aprendidos."""
        real_data = [dp for dp in self.training_data if dp.data_type == DataType.REAL]
        if len(real_data) < 5:
            return
        
        logger.info("🧠 Gerando dados sintéticos baseados em padrões aprendidos...")
        
        # Analisa padrões dos dados reais
        patterns = self._analyze_real_data_patterns(real_data)
        
        # Gera variações inteligentes
        synthetic_count = 0
        target_synthetic = max(3, int(len(real_data) * self.synthetic_data_ratio))
        
        for _ in range(target_synthetic):
            synthetic_point = self._create_pattern_based_synthetic(patterns)
            self.training_data.append(synthetic_point)
            synthetic_count += 1
        
        self.learning_metrics.synthetic_samples += synthetic_count
        logger.info(f"🧠 {synthetic_count} pontos sintéticos inteligentes gerados.")

    def _analyze_real_data_patterns(self, real_data: List[TrainingDataPoint]) -> Dict[str, Any]:
        """Analisa padrões nos dados reais para geração sintética inteligente."""
        patterns = {
            "successful_features": {},
            "failure_features": {},
            "reward_correlations": {},
            "temporal_patterns": {}
        }
        
        # Separa sucessos e falhas
        successes = [dp for dp in real_data if dp.outcome_reward > 0.5]
        failures = [dp for dp in real_data if dp.outcome_reward <= 0.5]
        
        # Analisa características de sucesso
        if successes:
            success_features = {}
            for dp in successes:
                for key, value in dp.state_features.items():
                    if key not in success_features:
                        success_features[key] = []
                    success_features[key].append(value)
            
            patterns["successful_features"] = {
                k: {
                    "mean": np.mean(v) if isinstance(v[0], (int, float)) else v[0],
                    "std": np.std(v) if isinstance(v[0], (int, float)) else 0
                }
                for k, v in success_features.items()
            }
        
        return patterns

    def _create_pattern_based_synthetic(self, patterns: Dict[str, Any]) -> TrainingDataPoint:
        """Cria ponto sintético baseado em padrões analisados."""
        # Usa padrões de sucesso como base
        synthetic_features = {}
        
        for feature, stats in patterns.get("successful_features", {}).items():
            if isinstance(stats["mean"], (int, float)):
                # Adiciona variação baseada no desvio padrão
                value = np.random.normal(stats["mean"], max(stats["std"], 0.1))
                synthetic_features[feature] = value
            else:
                synthetic_features[feature] = stats["mean"]
        
        # Adiciona algumas características padrão se não existirem
        default_features = {
            "system_load": random.uniform(0.2, 0.8),
            "complexity_score": random.uniform(0.3, 0.9),
            "confidence_level": random.uniform(0.6, 0.95)
        }
        
        for key, value in default_features.items():
            if key not in synthetic_features:
                synthetic_features[key] = value
        
        return TrainingDataPoint(
            agent_id=f"synthetic_agent_{random.randint(1, 100):03d}",
            state_features=synthetic_features,
            action_taken={
                "strategy": "pattern_based",
                "confidence": random.uniform(0.7, 0.9)
            },
            outcome_reward=random.uniform(0.6, 0.95),  # Tendência para sucesso
            data_type=DataType.SYNTHETIC,
            confidence_score=0.8,
            context_metadata={
                "generated_by": "pattern_analysis",
                "pattern_source": "real_data_analysis"
            }
        )

    async def _execute_quantum_learning(self) -> Dict[str, Any]:
        """Executa ciclo de aprendizado quantum avançado."""
        if len(self.training_data) < self.min_samples_for_learning:
            return {"status": "insufficient_data", "samples": len(self.training_data)}
        
        logger.info(f"🧬 Executando aprendizado quantum com {len(self.training_data)} amostras...")
        
        try:
            # Prepara dados com pesos baseados na confiança
            features = []
            rewards = []
            weights = []
            
            for dp in self.training_data:
                features.append(dp.state_features)
                rewards.append(dp.outcome_reward)
                # Dados reais têm peso maior que sintéticos
                weight = 1.0 if dp.data_type == DataType.REAL else 0.7
                weight *= dp.confidence_score
                weights.append(weight)
            
            # Vetorização com validação
            X = self.vectorizer.fit_transform(features)
            y = np.array(rewards)
            sample_weights = np.array(weights)
            
            # Treinamento ensemble com validação cruzada
            results = {}
            for model_name, model in self.active_models.items():
                # Treinamento com pesos
                model.fit(X, y, sample_weight=sample_weights)
                
                # Validação cruzada
                cv_scores = cross_val_score(model, X, y, cv=min(5, len(self.training_data)), 
                                          scoring='r2', fit_params={'sample_weight': sample_weights})
                
                # Métricas detalhadas
                y_pred = model.predict(X)
                r2 = r2_score(y, y_pred, sample_weight=sample_weights)
                mse = mean_squared_error(y, y_pred, sample_weight=sample_weights)
                
                results[model_name] = {
                    "cv_score_mean": float(np.mean(cv_scores)),
                    "cv_score_std": float(np.std(cv_scores)),
                    "r2_score": float(r2),
                    "mse": float(mse),
                    "feature_importance": self._get_feature_importance(model)
                }
                
                logger.info(f"  {model_name}: R² = {r2:.4f}, CV = {np.mean(cv_scores):.4f} (±{np.std(cv_scores):.4f})")
            
            # Seleciona melhor modelo
            best_model_name = max(results.keys(), key=lambda k: results[k]["r2_score"])
            best_score = results[best_model_name]["r2_score"]
            
            # Salva modelo se houve melhoria significativa
            if self._should_save_model(best_score):
                await self._save_quantum_model(best_model_name, results[best_model_name])
            
            # Atualiza métricas
            self.learning_metrics.prediction_accuracy = best_score
            self.performance_history.append(best_score)
            
            return {
                "status": "success",
                "best_model": best_model_name,
                "best_score": best_score,
                "improvement": self._calculate_improvement(),
                "models_trained": len(results),
                "total_samples": len(self.training_data),
                "weighted_samples": sum(weights),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no aprendizado quantum: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}

    def _get_feature_importance(self, model) -> Dict[str, float]:
        """Extrai importância das features do modelo."""
        try:
            if hasattr(model, 'feature_importances_'):
                feature_names = self.vectorizer.get_feature_names_out()
                importances = model.feature_importances_
                return dict(zip(feature_names, importances.tolist()))
        except Exception:
            pass
        return {}

    def _should_save_model(self, current_score: float) -> bool:
        """Determina se o modelo atual deve ser salvo."""
        if not self.learning_metrics.model_versions:
            return True  # Primeiro modelo
        
        last_best = max(v.r2_score for v in self.learning_metrics.model_versions)
        improvement = current_score - last_best
        
        return improvement > self.auto_optimization_threshold

    async def _save_quantum_model(self, model_name: str, metrics: Dict[str, Any]):
        """Salva modelo quantum com versionamento."""
        try:
            version = len(self.learning_metrics.model_versions) + 1
            model_filename = f"quantum_model_v{version:03d}.pkl"
            model_path = self.model_storage_path / model_filename
            
            # Dados para salvar
            save_data = {
                'models': self.active_models,
                'vectorizer': self.vectorizer,
                'metrics': self.learning_metrics,
                'version': version,
                'best_model_name': model_name,
                'performance_metrics': metrics,
                'timestamp': datetime.now()
            }
            
            # Salva com compressão
            with open(model_path, 'wb') as f:
                pickle.dump(save_data, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            # Registra versão
            model_version = ModelVersion(
                version=version,
                model_path=str(model_path),
                creation_time=datetime.now(),
                training_samples=len(self.training_data),
                cross_val_score=metrics.get("cv_score_mean", 0.0),
                r2_score=metrics.get("r2_score", 0.0),
                feature_importance=metrics.get("feature_importance", {}),
                hyperparameters={"model_type": model_name},
                performance_trend=list(self.performance_history)[-10:]  # Últimas 10
            )
            
            self.learning_metrics.model_versions.append(model_version)
            
            logger.info(f"💾 Modelo quantum v{version} salvo: {model_filename}")
            
        except Exception as e:
            logger.error(f"❌ Erro salvando modelo: {e}", exc_info=True)

    def _calculate_improvement(self) -> float:
        """Calcula melhoria em relação ao modelo anterior."""
        if len(self.performance_history) < 2:
            return 0.0
        
        current = self.performance_history[-1]
        previous = self.performance_history[-2]
        
        return float(current - previous)

    async def _evaluate_and_optimize(self, evolution_result: Dict[str, Any]):
        """Avalia resultados e executa otimizações automáticas."""
        if evolution_result.get("status") != "success":
            return
        
        improvement = evolution_result.get("improvement", 0.0)
        current_score = evolution_result.get("best_score", 0.0)
        
        # Atualiza velocidade de aprendizado
        self.learning_metrics.learning_velocity = improvement
        
        # Auto-otimização de hiperparâmetros se necessário
        if len(self.performance_history) > 5:
            recent_performance = list(self.performance_history)[-5:]
            if max(recent_performance) - min(recent_performance) < 0.05:  # Stagnação
                await self._auto_optimize_hyperparameters()
        
        # Atualiza taxa de adaptação
        if len(self.training_data) > 0:
            real_data_ratio = len([dp for dp in self.training_data if dp.data_type == DataType.REAL]) / len(self.training_data)
            self.learning_metrics.adaptation_rate = real_data_ratio * current_score
        
        # Manutenção de coerência quântica
        self._maintain_quantum_coherence()

    async def _auto_optimize_hyperparameters(self):
        """Otimização automática de hiperparâmetros quando há estagnação."""
        if len(self.training_data) < 10:
            return
        
        logger.info("🔧 Executando auto-otimização de hiperparâmetros...")
        
        try:
            # Prepara dados
            features = [dp.state_features for dp in self.training_data]
            rewards = [dp.outcome_reward for dp in self.training_data]
            X = self.vectorizer.transform(features)
            y = np.array(rewards)
            
            # Grid search para RandomForest
            rf_params = {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 15, 20],
                'min_samples_split': [2, 5, 10]
            }
            
            grid_search = GridSearchCV(
                RandomForestRegressor(random_state=42, n_jobs=-1),
                rf_params,
                cv=3,
                scoring='r2',
                n_jobs=-1
            )
            
            grid_search.fit(X, y)
            
            # Atualiza modelo principal com melhores parâmetros
            self.active_models["primary"] = grid_search.best_estimator_
            
            logger.info(f"✅ Hiperparâmetros otimizados: {grid_search.best_params_}")
            logger.info(f"📈 Melhoria de score: {grid_search.best_score_:.4f}")
            
        except Exception as e:
            logger.error(f"❌ Erro na auto-otimização: {e}")

    def _maintain_quantum_coherence(self):
        """Mantém coerência quântica do sistema de aprendizado."""
        # Calcula coerência baseada na consistência das previsões
        if len(self.performance_history) > 3:
            recent_scores = list(self.performance_history)[-5:]
            coherence = 1.0 - (np.std(recent_scores) / (np.mean(recent_scores) + 0.001))
            self.learning_metrics.quantum_coherence = max(0.0, min(1.0, coherence))
        
        # Limpeza de dados antigos se necessário
        if len(self.training_data) > 8000:
            # Remove 20% dos dados mais antigos, priorizando manter dados reais
            removal_count = int(len(self.training_data) * 0.2)
            synthetic_data = [i for i, dp in enumerate(self.training_data) if dp.data_type == DataType.SYNTHETIC]
            
            if len(synthetic_data) >= removal_count:
                # Remove dados sintéticos antigos primeiro
                for i in sorted(synthetic_data[:removal_count], reverse=True):
                    del self.training_data[i]
            else:
                # Remove os mais antigos em geral
                for _ in range(removal_count):
                    self.training_data.popleft()

    def _update_learning_phase(self):
        """Atualiza a fase de aprendizado baseada no progresso."""
        total_samples = len(self.training_data)
        real_samples = len([dp for dp in self.training_data if dp.data_type == DataType.REAL])
        accuracy = self.learning_metrics.prediction_accuracy
        
        if total_samples < 10:
            self.learning_metrics.current_phase = LearningPhase.BOOTSTRAP
        elif real_samples < 5 or accuracy < 0.5:
            self.learning_metrics.current_phase = LearningPhase.ACTIVE_LEARNING
        elif accuracy < 0.8:
            self.learning_metrics.current_phase = LearningPhase.OPTIMIZATION
        else:
            self.learning_metrics.current_phase = LearningPhase.MASTERY

    def _log_evolution_report(self, cycle: int, result: Dict[str, Any]):
        """Gera relatório detalhado da evolução."""
        if result.get("status") == "success":
            improvement = result.get("improvement", 0.0)
            best_score = result.get("best_score", 0.0)
            change_percent = (improvement / best_score * 100) if best_score > 0 else 0
            
            status_emoji = "🔼" if improvement > 0 else "🔽" if improvement < 0 else "⏸️"
            
            logger.info(f"{status_emoji} [Quantum Evolution] Performance: {best_score:.4f}")
            logger.info(f"{status_emoji} [Quantum Evolution] Mudança: {improvement:+.4f} ({change_percent:+.2f}%)")
            logger.info(f"📊 [Quantum Evolution] Fase: {self.learning_metrics.current_phase.value}")
            logger.info(f"🧬 [Quantum Evolution] Coerência Quântica: {self.learning_metrics.quantum_coherence:.3f}")
            logger.info(f"📈 [Quantum Evolution] Velocidade: {self.learning_metrics.learning_velocity:.4f}")
            
            if improvement > 0.01:
                logger.info("✅ [Quantum Evolution] Sistema aprendendo e melhorando!")
            elif improvement < -0.01:
                logger.warning("⚠️ [Quantum Evolution] Degradação detectada - investigando...")
            else:
                logger.info("ℹ️ [Quantum Evolution] Performance estável.")
        else:
            logger.warning(f"⚠️ [Quantum Evolution] Ciclo falhou: {result.get('error', 'Erro desconhecido')}")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa dados de treinamento e consultas do sistema."""
        if message.message_type == MessageType.NOTIFICATION and message.content.get("event_type") == "training_data":
            try:
                data = message.content.get("data", {})
                
                # Corrige timestamp se necessário
                if 'timestamp' in data and isinstance(data['timestamp'], str):
                    data['timestamp'] = datetime.fromisoformat(data['timestamp'])
                
                # Cria ponto de treinamento
                data_point = TrainingDataPoint(**data)
                data_point.data_type = DataType.REAL  # Marca como dados reais
                
                self.training_data.append(data_point)
                self.learning_metrics.real_samples += 1
                self.learning_metrics.total_samples = len(self.training_data)
                
                logger.info(f"📊 Ponto de treinamento real recebido de {message.sender_id}")
                
            except Exception as e:
                logger.error(f"❌ Erro processando dados de treinamento: {e}")
        
        elif message.message_type == MessageType.REQUEST:
            # Consultas sobre métricas do sistema
            if message.content.get("request_type") == "get_evolution_metrics":
                metrics = self.get_quantum_evolution_metrics()
                await self.publish_response(message, {"status": "success", "metrics": metrics})

    def get_quantum_evolution_metrics(self) -> Dict[str, Any]:
        """Retorna métricas completas da evolução quântica."""
        uptime = datetime.now() - self.learning_metrics.uptime_start if hasattr(self.learning_metrics, 'uptime_start') else timedelta(0)
        
        return {
            "learning_metrics": asdict(self.learning_metrics),
            "performance_history": list(self.performance_history),
            "current_status": self.status,
            "uptime_seconds": uptime.total_seconds(),
            "model_count": len(self.active_models),
            "data_distribution": {
                "real": len([dp for dp in self.training_data if dp.data_type == DataType.REAL]),
                "synthetic": len([dp for dp in self.training_data if dp.data_type == DataType.SYNTHETIC]),
                "total": len(self.training_data)
            },
            "quantum_metrics": {
                "coherence": self.learning_metrics.quantum_coherence,
                "learning_velocity": self.learning_metrics.learning_velocity,
                "adaptation_rate": self.learning_metrics.adaptation_rate,
                "prediction_confidence": self.learning_metrics.prediction_accuracy
            }
        }

def create_evolution_engine_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria o Engine de Evolução Quântico."""
    agents = []
    logger.info("🧬 Criando QuantumEvolutionEngine...")
    try:
        agent = QuantumEvolutionEngine("evolution_engine_001", message_bus)
        agents.append(agent)
        logger.info("✅ QuantumEvolutionEngine criado com sucesso.")
    except Exception as e:
        logger.error(f"❌ Erro crítico criando QuantumEvolutionEngine: {e}", exc_info=True)
    return agents
