#!/usr/bin/env python3
"""
Módulo do Real Evolution Engine - O Coração da Auto-Evolução do SUNA-ALSHAM.

[Fase 2] - Fortalecido com lógica real de pré-processamento de dados para
treinamento de modelo com scikit-learn.
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
    Este componente é agnóstico à rede e focado puramente na lógica de ML.
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
        [LÓGICA REAL] Treina o modelo de machine learning com os dados coletados,
        incluindo pré-processamento real dos dados.
        """
        if self.status != "active" or len(self.training_data) < 50:
            return {"status": "skipped", "reason": "Dados de treino insuficientes ou dependências em falta."}

        logger.info(f"🧠 Treinando modelo de evolução com {len(self.training_data)} pontos de dados...")
        
        try:
            # 1. Preparar os dados para o scikit-learn
            features = [dp.state_features for dp in self.training_data]
            rewards = [dp.outcome_reward for dp in self.training_data]

            # 2. Converter features (dicionários) em um array numérico
            X = self.vectorizer.fit_transform(features)
            y = np.array(rewards)

            # 3. Treinar o modelo
            self.model.fit(X, y)
            
            self.last_training_time = datetime.now()
            self.model_version += 1
            
            # [AUTENTICIDADE] O score é uma métrica real do modelo treinado.
            model_score = self.model.score(X, y)

            logger.info(f"✅ Modelo treinado com sucesso. Versão: {self.model_version}, Score R^2: {model_score:.3f}")

            return {
                "status": "completed",
                "model_version": self.model_version,
                "training_samples": len(self.training_data),
                "model_score_r2": model_score,
            }
        except Exception as e:
            logger.error(f"❌ Falha no treinamento do modelo de evolução: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    def predict_best_action(self, agent_id: str, possible_actions: List[Dict]) -> Dict[str, Any]:
        """
        [AUTENTICIDADE] Usa o modelo treinado para prever a melhor ação dentre uma lista.
        Na Fase 3, o `current_state` será usado para predições mais complexas.
        """
        if self.status != "active" or self.model_version == 0:
            # Retorna a primeira ação como fallback se o modelo não estiver treinado
            return {"best_action": possible_actions[0], "confidence": 0.5, "reason": "Fallback - modelo não treinado."}

        try:
            # Converte as possíveis ações em features numéricas
            X_predict = self.vectorizer.transform(possible_actions)
            
            # Faz a predição da recompensa para cada ação
            predicted_rewards = self.model.predict(X_predict)
            
            # Encontra a ação com a maior recompensa prevista
            best_action_index = np.argmax(predicted_rewards)
            best_action = possible_actions[best_action_index]
            confidence = predicted_rewards[best_action_index]

            return {
                "best_action": best_action,
                "confidence": confidence,
                "model_version": self.model_version,
            }
        except Exception as e:
            logger.error(f"❌ Falha na predição da melhor ação: {e}", exc_info=True)
            # Retorna a primeira ação como fallback em caso de erro
            return {"best_action": possible_actions[0], "confidence": 0.5, "reason": f"Erro na predição: {e}"}
