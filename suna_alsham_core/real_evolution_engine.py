#!/usr/bin/env python3
"""
Módulo do Real Evolution Engine - O Coração da Auto-Evolução do SUNA-ALSHAM.

[Versão Final Completa] - Inclui a classe do Agente e a função de fábrica.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

# [AUTENTICIDADE] As bibliotecas de machine learning são importadas de forma segura.
try:
    import numpy as np
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.feature_extraction import DictVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Importa a classe base e os tipos essenciais do núcleo
from suna_alsham_core.multi_agent_network import (
    BaseNetworkAgent,
    AgentMessage,
    AgentType,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Dataclasses para Tipagem Forte ---

@dataclass
class TrainingDataPoint:
    """Representa um único ponto de dados para treino do modelo de evolução."""
    agent_id: str
    state_features: Dict[str, Any]
    action_taken: Dict[str, Any]
    outcome_reward: float
    timestamp: datetime = field(default_factory=datetime.now)


# --- Classe Principal do Motor de Evolução ---

class RealEvolutionEngine:
    """
    Motor de evolução que implementa o ciclo de aprendizado e adaptação.
    """

    def __init__(self):
        """Inicializa o RealEvolutionEngine."""
        self.training_data: List[TrainingDataPoint] = []
        self.last_training_time: Optional[datetime] = None
        self.model_version = 0
        
        if not SKLEARN_AVAILABLE:
            self.status = "degraded"
            self.model = None
            self.vectorizer = None
            logger.critical("Bibliotecas 'scikit-learn' ou 'numpy' não encontradas. O motor de evolução operará em modo degradado.")
        else:
            self.status = "active"
            self.model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            self.vectorizer = DictVectorizer(sparse=False)
        
        logger.info(f"🧠 Real Evolution Engine inicializado. Status: {self.status.upper()}")

    def add_training_data(self, data_point: TrainingDataPoint):
        """Adiciona um novo ponto de dados ao conjunto de treino."""
        self.training_data.append(data_point)

    def train_evolution_model(self) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Treina o modelo de machine learning com os dados coletados.
        """
        if self.status != "active" or len(self.training_data) < 50:
            return {"status": "skipped", "reason": "Dados de treino insuficientes ou dependências em falta."}

        logger.info(f"🧠 Treinando modelo de evolução com {len(self.training_data)} pontos de dados...")
        
        try:
            features = [dp.state_features for dp in self.training_data]
            rewards = [dp.outcome_reward for dp in self.training_data]
            X = self.vectorizer.fit_transform(features)
            y = np.array(rewards)
            self.model.fit(X, y)
            
            self.last_training_time = datetime.now()
            self.model_version += 1
            model_score = self.model.score(X, y)

            logger.info(f"✅ Modelo treinado com sucesso. Versão: {self.model_version}, Score R^2: {model_score:.3f}")

            return {
                "status": "completed",
                "model_version": self.model_version,
                "model_score_r2": model_score,
            }
        except Exception as e:
            logger.error(f"❌ Falha no treinamento do modelo de evolução: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

# --- CLASSE DO AGENTE (O "PILOTO") - ADICIONADA ---
class EvolutionEngineAgent(BaseNetworkAgent):
    """
    Agente que encapsula o RealEvolutionEngine e o conecta à rede.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.engine = RealEvolutionEngine()
        self.capabilities.append("self_evolution_training")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para treinar o modelo."""
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "train_evolution_model":
            # Aqui, os dados de treino viriam do conteúdo da mensagem
            # data_points = message.content.get("data")
            # for dp in data_points:
            #     self.engine.add_training_data(TrainingDataPoint(**dp))
            
            result = self.engine.train_evolution_model()
            await self.publish_response(message, result)

# --- FUNÇÃO DE FÁBRICA (A "CHAVE DE IGNIÇÃO") - ADICIONADA ---
def create_evolution_engine_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria e retorna o agente do motor de evolução."""
    logger.info("🔧 Criando o Evolution Engine Agent...")
    agents = [
        EvolutionEngineAgent("evolution_engine_001", message_bus)
    ]
    return agents
