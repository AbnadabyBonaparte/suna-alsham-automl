"""
SUNA-ALSHAM Learn Agent - PyTorch Real Version
Meta-Learning com MAML genuíno usando learn2learn
Versão: 2.1.0 - PyTorch Real Edition
"""

import os
import uuid
import time
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
import logging
from dataclasses import dataclass

# Configurar logging
logger = logging.getLogger(__name__)

@dataclass
class LearnAgentConfig:
    """Configuração do Learn Agent PyTorch Real."""
    inner_lr: float = 0.01
    outer_lr: float = 0.001
    adaptation_steps: int = 5
    meta_batch_size: int = 16
    max_epochs: int = 50
    timeout_seconds: int = 180
    hidden_size: int = 64
    num_layers: int = 2

@dataclass
class TaskData:
    """Estrutura de dados para tarefas de meta-learning."""
    task_id: str
    X_support: np.ndarray
    y_support: np.ndarray
    X_query: np.ndarray
    y_query: np.ndarray
    task_type: str = "regression"

@dataclass
class MetaTrainingResults:
    """Resultados do meta-treinamento."""
    performance: float
    meta_loss: float
    adaptation_performance: Dict[str, float]
    training_time: float
    convergence_achieved: bool
    pytorch_used: bool

# Tentar importar PyTorch e learn2learn
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import learn2learn as l2l
    from learn2learn.algorithms import MAML
    PYTORCH_AVAILABLE = True
    logger.info("✅ PyTorch e learn2learn disponíveis - MAML real ativado!")
except ImportError as e:
    logger.warning(f"⚠️ PyTorch/learn2learn não disponível: {e}")
    PYTORCH_AVAILABLE = False

class BaseModel(nn.Module if PYTORCH_AVAILABLE else object):
    """
    Modelo base para MAML - Neural Network simples.
    """
    
    def __init__(self, input_size: int, hidden_size: int, output_size: int, num_layers: int = 2):
        if PYTORCH_AVAILABLE:
            super(BaseModel, self).__init__()
            
            layers = []
            current_size = input_size
            
            # Hidden layers
            for i in range(num_layers):
                layers.append(nn.Linear(current_size, hidden_size))
                layers.append(nn.ReLU())
                current_size = hidden_size
            
            # Output layer
            layers.append(nn.Linear(current_size, output_size))
            
            self.network = nn.Sequential(*layers)
        else:
            # Mock para quando PyTorch não está disponível
            self.input_size = input_size
            self.hidden_size = hidden_size
            self.output_size = output_size
            self.num_layers = num_layers
    
    def forward(self, x):
        if PYTORCH_AVAILABLE:
            return self.network(x)
        else:
            # Mock forward pass
            batch_size = x.shape[0] if hasattr(x, 'shape') else 1
            return np.random.randn(batch_size, self.output_size)

class PyTorchMAML:
    """
    Implementação real do MAML usando PyTorch e learn2learn.
    """
    
    def __init__(self, config: LearnAgentConfig):
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if PYTORCH_AVAILABLE else None
        
        if PYTORCH_AVAILABLE:
            # Criar modelo base
            self.base_model = BaseModel(
                input_size=10,  # Será ajustado dinamicamente
                hidden_size=config.hidden_size,
                output_size=1,  # Regressão
                num_layers=config.num_layers
            )
            
            # Criar MAML wrapper
            self.maml = MAML(self.base_model, lr=config.inner_lr)
            self.meta_optimizer = optim.Adam(self.maml.parameters(), lr=config.outer_lr)
            self.loss_fn = nn.MSELoss()
            
            logger.info(f"🧠 PyTorch MAML inicializado - Device: {self.device}")
        else:
            logger.info("🔄 MAML Mock inicializado (PyTorch não disponível)")
        
        self.adaptation_history = []
        self.training_history = []
    
    def _prepare_task_data(self, task: TaskData) -> Tuple[Any, Any, Any, Any]:
        """Prepara dados da tarefa para PyTorch."""
        if not PYTORCH_AVAILABLE:
            return task.X_support, task.y_support, task.X_query, task.y_query
        
        # Converter para tensors PyTorch
        X_support = torch.FloatTensor(task.X_support).to(self.device)
        y_support = torch.FloatTensor(task.y_support.reshape(-1, 1)).to(self.device)
        X_query = torch.FloatTensor(task.X_query).to(self.device)
        y_query = torch.FloatTensor(task.y_query.reshape(-1, 1)).to(self.device)
        
        return X_support, y_support, X_query, y_query
    
    def meta_train(self, tasks: List[TaskData]) -> MetaTrainingResults:
        """
        Meta-treinamento usando MAML real com PyTorch.
        """
        start_time = time.time()
        
        if not PYTORCH_AVAILABLE:
            return self._mock_meta_train(tasks, start_time)
        
        # Ajustar tamanho do modelo baseado nos dados
        if tasks:
            sample_task = tasks[0]
            input_size = sample_task.X_support.shape[1]
            
            # Recriar modelo com tamanho correto
            self.base_model = BaseModel(
                input_size=input_size,
                hidden_size=self.config.hidden_size,
                output_size=1,
                num_layers=self.config.num_layers
            ).to(self.device)
            
            self.maml = MAML(self.base_model, lr=self.config.inner_lr)
            self.meta_optimizer = optim.Adam(self.maml.parameters(), lr=self.config.outer_lr)
        
        meta_losses = []
        performance_history = []
        
        logger.info(f"🔄 Iniciando meta-treinamento PyTorch MAML...")
        
        for epoch in range(self.config.max_epochs):
            epoch_meta_loss = 0.0
            epoch_performances = []
            
            # Selecionar batch de tarefas
            batch_tasks = np.random.choice(tasks, size=min(self.config.meta_batch_size, len(tasks)), replace=False)
            
            self.meta_optimizer.zero_grad()
            
            for task in batch_tasks:
                # Preparar dados
                X_support, y_support, X_query, y_query = self._prepare_task_data(task)
                
                # Clone do modelo para adaptação
                learner = self.maml.clone()
                
                # Inner loop - adaptação rápida
                for step in range(self.config.adaptation_steps):
                    support_pred = learner(X_support)
                    support_loss = self.loss_fn(support_pred, y_support)
                    learner.adapt(support_loss)
                
                # Outer loop - avaliação na query set
                query_pred = learner(X_query)
                query_loss = self.loss_fn(query_pred, y_query)
                
                # Calcular performance (R²)
                with torch.no_grad():
                    y_mean = torch.mean(y_query)
                    ss_tot = torch.sum((y_query - y_mean) ** 2)
                    ss_res = torch.sum((y_query - query_pred) ** 2)
                    r2_score = 1 - (ss_res / (ss_tot + 1e-8))
                    performance = max(0.0, min(1.0, r2_score.item()))
                    epoch_performances.append(performance)
                
                epoch_meta_loss += query_loss
            
            # Meta-update
            epoch_meta_loss = epoch_meta_loss / len(batch_tasks)
            epoch_meta_loss.backward()
            self.meta_optimizer.step()
            
            # Registrar progresso
            meta_losses.append(epoch_meta_loss.item())
            avg_performance = np.mean(epoch_performances) if epoch_performances else 0.5
            performance_history.append(avg_performance)
            
            # Log progresso
            if epoch % 10 == 0:
                logger.info(f"PyTorch MAML epoch {epoch}/{self.config.max_epochs} - Loss: {epoch_meta_loss.item():.4f}, Performance: {avg_performance:.4f}")
        
        training_time = time.time() - start_time
        final_performance = performance_history[-1] if performance_history else 0.5
        final_meta_loss = meta_losses[-1] if meta_losses else 1.0
        
        # Salvar histórico
        self.training_history.append({
            'timestamp': datetime.now(),
            'performance': final_performance,
            'meta_loss': final_meta_loss,
            'training_time': training_time,
            'epochs': self.config.max_epochs
        })
        
        logger.info(f"✅ Meta-treinamento PyTorch MAML concluído - Performance: {final_performance:.4f}")
        
        return MetaTrainingResults(
            performance=final_performance,
            meta_loss=final_meta_loss,
            adaptation_performance={
                "mean": np.mean(performance_history),
                "std": np.std(performance_history),
                "best": max(performance_history) if performance_history else 0.5,
                "final": final_performance
            },
            training_time=training_time,
            convergence_achieved=final_meta_loss < 0.1,
            pytorch_used=True
        )
    
    def _mock_meta_train(self, tasks: List[TaskData], start_time: float) -> MetaTrainingResults:
        """Meta-treinamento mock quando PyTorch não está disponível."""
        logger.info("🔄 Executando meta-treinamento mock (PyTorch não disponível)...")
        
        # Simular treinamento
        performance_history = []
        for epoch in range(self.config.max_epochs):
            # Simular melhoria gradual
            base_performance = 0.6
            improvement = (epoch / self.config.max_epochs) * 0.3
            noise = np.random.uniform(-0.02, 0.02)
            performance = min(0.95, base_performance + improvement + noise)
            performance_history.append(performance)
            
            if epoch % 10 == 0:
                logger.info(f"Mock MAML epoch {epoch}/{self.config.max_epochs}")
            
            time.sleep(0.01)  # Simular processamento
        
        training_time = time.time() - start_time
        final_performance = performance_history[-1]
        
        return MetaTrainingResults(
            performance=final_performance,
            meta_loss=1.0 - final_performance,
            adaptation_performance={
                "mean": np.mean(performance_history),
                "std": np.std(performance_history),
                "best": max(performance_history),
                "final": final_performance
            },
            training_time=training_time,
            convergence_achieved=final_performance > 0.8,
            pytorch_used=False
        )
    
    def adapt_to_task(self, task: TaskData) -> Dict[str, Any]:
        """Adapta rapidamente para uma nova tarefa usando MAML."""
        adaptation_start = time.time()
        
        if not PYTORCH_AVAILABLE:
            return self._mock_adapt_to_task(task, adaptation_start)
        
        # Preparar dados
        X_support, y_support, X_query, y_query = self._prepare_task_data(task)
        
        # Clone do modelo para adaptação
        learner = self.maml.clone()
        
        # Adaptação rápida (inner loop)
        for step in range(self.config.adaptation_steps):
            support_pred = learner(X_support)
            support_loss = self.loss_fn(support_pred, y_support)
            learner.adapt(support_loss)
        
        # Avaliar performance na query set
        with torch.no_grad():
            query_pred = learner(X_query)
            query_loss = self.loss_fn(query_pred, y_query)
            
            # Calcular R²
            y_mean = torch.mean(y_query)
            ss_tot = torch.sum((y_query - y_mean) ** 2)
            ss_res = torch.sum((y_query - query_pred) ** 2)
            r2_score = 1 - (ss_res / (ss_tot + 1e-8))
            performance = max(0.0, min(1.0, r2_score.item()))
        
        adaptation_time = time.time() - adaptation_start
        
        adaptation_result = {
            "task_id": task.task_id,
            "performance": performance,
            "adaptation_time": adaptation_time,
            "adaptation_steps": self.config.adaptation_steps,
            "query_loss": query_loss.item(),
            "pytorch_used": True
        }
        
        self.adaptation_history.append(adaptation_result)
        return adaptation_result
    
    def _mock_adapt_to_task(self, task: TaskData, adaptation_start: float) -> Dict[str, Any]:
        """Adaptação mock quando PyTorch não está disponível."""
        time.sleep(0.1)  # Simular processamento
        
        performance = np.random.uniform(0.7, 0.9)
        adaptation_time = time.time() - adaptation_start
        
        adaptation_result = {
            "task_id": task.task_id,
            "performance": performance,
            "adaptation_time": adaptation_time,
            "adaptation_steps": self.config.adaptation_steps,
            "query_loss": 1.0 - performance,
            "pytorch_used": False
        }
        
        self.adaptation_history.append(adaptation_result)
        return adaptation_result

class LearnAgentPyTorchReal:
    """
    Learn Agent SUNA-ALSHAM - Versão PyTorch Real
    Meta-Learning com MAML genuíno usando learn2learn
    """
    
    def __init__(self, config: Optional[LearnAgentConfig] = None):
        self.agent_id = str(uuid.uuid4())
        self.name = "Learn Agent PyTorch Real"
        self.version = "2.1.0"
        self.config = config or LearnAgentConfig()
        self.status = "initializing"
        self.created_at = datetime.now()
        
        # Inicializar componentes
        self.maml_engine = PyTorchMAML(self.config)
        self.meta_training_cycles = 0
        self.adaptation_strategies = []
        self.performance_history = []
        self.last_training_time = None
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        logger.info(f"🧠 Learn Agent PyTorch Real inicializado - ID: {self.agent_id}")
        logger.info(f"🔧 PyTorch disponível: {PYTORCH_AVAILABLE}")
        
        self.status = "ready"
    
    def execute_meta_training(self, num_tasks: int = 20) -> MetaTrainingResults:
        """Executa ciclo de meta-treinamento."""
        logger.info(f"🔄 Iniciando meta-treinamento {'PyTorch Real' if PYTORCH_AVAILABLE else 'Mock'}...")
        
        # Gerar tarefas sintéticas para treinamento
        tasks = self._generate_synthetic_tasks(num_tasks)
        
        # Executar meta-treinamento
        results = self.maml_engine.meta_train(tasks)
        
        # Atualizar estado
        self.meta_training_cycles += 1
        self.performance_history.append(results.performance)
        self.last_training_time = datetime.now()
        
        logger.info(f"✅ Meta-treinamento concluído - Performance: {results.performance:.4f} ({'PyTorch' if results.pytorch_used else 'Mock'})")
        
        return results
    
    def _generate_synthetic_tasks(self, num_tasks: int) -> List[TaskData]:
        """Gera tarefas sintéticas para meta-treinamento."""
        tasks = []
        
        for i in range(num_tasks):
            # Gerar dados sintéticos variados
            n_samples = np.random.randint(50, 200)
            n_features = np.random.randint(5, 15)
            
            # Diferentes tipos de funções para diversidade
            task_type = np.random.choice(['linear', 'quadratic', 'sinusoidal'])
            
            X = np.random.randn(n_samples, n_features)
            
            if task_type == 'linear':
                weights = np.random.randn(n_features)
                y = X @ weights + np.random.randn(n_samples) * 0.1
            elif task_type == 'quadratic':
                y = np.sum(X**2, axis=1) + np.random.randn(n_samples) * 0.1
            else:  # sinusoidal
                y = np.sin(np.sum(X, axis=1)) + np.random.randn(n_samples) * 0.1
            
            # Dividir em support e query sets
            split_idx = n_samples // 2
            
            task = TaskData(
                task_id=f"synthetic_task_{i}_{task_type}",
                X_support=X[:split_idx],
                y_support=y[:split_idx],
                X_query=X[split_idx:],
                y_query=y[split_idx:],
                task_type="regression"
            )
            
            tasks.append(task)
        
        return tasks
    
    def extract_strategies_for_core_agent(self) -> List[Dict[str, Any]]:
        """Extrai estratégias aprendidas para o Core Agent."""
        if not self.maml_engine.adaptation_history:
            return []
        
        # Analisar adaptações bem-sucedidas
        successful_adaptations = [
            adapt for adapt in self.maml_engine.adaptation_history
            if adapt["performance"] > 0.8
        ]
        
        strategies = []
        for adaptation in successful_adaptations[-5:]:  # Últimas 5 melhores
            strategy = {
                "strategy_id": str(uuid.uuid4()),
                "source": "learn_agent_pytorch_real",
                "performance": adaptation["performance"],
                "confidence": min(1.0, adaptation["performance"] * 1.1),
                "applicable_contexts": ["regression", "optimization", "few_shot_learning"],
                "meta_learned": True,
                "pytorch_based": adaptation.get("pytorch_used", False),
                "adaptation_time": adaptation["adaptation_time"],
                "hyperparameters": {
                    "inner_lr": self.config.inner_lr,
                    "adaptation_steps": self.config.adaptation_steps,
                    "hidden_size": self.config.hidden_size
                }
            }
            strategies.append(strategy)
        
        return strategies
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status detalhado do agente."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "type": "learn_agent_pytorch_real",
            "performance": np.mean(self.performance_history) if self.performance_history else 0.0,
            "pytorch_available": PYTORCH_AVAILABLE,
            "learn2learn_available": PYTORCH_AVAILABLE,  # Assume que se PyTorch está disponível, learn2learn também está
            "meta_training_cycles": self.meta_training_cycles,
            "adaptation_strategies_count": len(self.adaptation_strategies),
            "adaptation_history_count": len(self.maml_engine.adaptation_history),
            "config": {
                "inner_lr": self.config.inner_lr,
                "outer_lr": self.config.outer_lr,
                "adaptation_steps": self.config.adaptation_steps,
                "meta_batch_size": self.config.meta_batch_size,
                "hidden_size": self.config.hidden_size,
                "num_layers": self.config.num_layers
            },
            "created_at": self.created_at.isoformat(),
            "last_training": {
                "timestamp": self.last_training_time.isoformat() if self.last_training_time else None,
                "performance": self.performance_history[-1] if self.performance_history else 0.0,
                "pytorch_used": PYTORCH_AVAILABLE
            }
        }

# Teste standalone
if __name__ == "__main__":
    logger.info("🧪 Testing Learn Agent PyTorch Real...")
    
    # Criar e testar Learn Agent
    config = LearnAgentConfig()
    agent = LearnAgentPyTorchReal(config)
    
    # Executar meta-treinamento
    results = agent.execute_meta_training(num_tasks=10)
    
    logger.info(f"✅ Test completed - Performance: {results.performance:.4f} ({'PyTorch' if results.pytorch_used else 'Mock'})")
    print("Learn Agent Status:", agent.get_status())

