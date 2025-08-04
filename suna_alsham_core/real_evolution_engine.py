#!/usr/bin/env python3
"""
Módulo do Real Evolution Engine - O Coração da Auto-Evolução do SUNA-ALSHAM.
"""
import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import numpy as np
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.feature_extraction import DictVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentMessage, AgentType, MessageType

logger = logging.getLogger(__name__)

@dataclass
class TrainingDataPoint:
    agent_id: str
    state_features: Dict[str, Any]
    action_taken: Dict[str, Any]
    outcome_reward: float
    timestamp: datetime = field(default_factory=datetime.now)

class EvolutionEngineAgent(BaseNetworkAgent):
    """
    Agente que gerencia o ciclo de aprendizado e evolução do sistema.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.append("self_evolution_training")
        self.training_data: List[TrainingDataPoint] = []
        self.model_version = 0
        self.last_model_score = 0.0
        
        if not SKLEARN_AVAILABLE:
            self.status = "degraded"
            self.model, self.vectorizer = None, None
            logger.critical("Dependências de ML não encontradas. EvolutionEngine em modo degradado.")
        else:
            self.status = "active"
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.vectorizer = DictVectorizer(sparse=False)
            
        self.evolution_task = asyncio.create_task(self._evolution_loop())
        logger.info(f"🧠 {self.agent_id} (Evolution Engine) 100% real inicializado.")

    async def _evolution_loop(self):
        """Ciclo principal que treina e reporta a evolução a cada 10 minutos."""
        while True:
            await asyncio.sleep(600) # 10 minutos
            if self.status != "active": continue

            logger.info("="*50)
            logger.info(f"🧠 [Evolução] Iniciando ciclo de evolução. Versão do Modelo Atual: {self.model_version}")
            
            if len(self.training_data) < 5:
                logger.warning(f"[Evolução] Ciclo abortado. Pontos de dados insuficientes ({len(self.training_data)}/5).")
                logger.info("="*50)
                continue

            try:
                features = [dp.state_features for dp in self.training_data]
                rewards = [dp.outcome_reward for dp in self.training_data]
                X = self.vectorizer.fit_transform(features)
                y = np.array(rewards)
                self.model.fit(X, y)
                
                new_model_score = self.model.score(X, y)
                self.model_version += 1
                
                score_change = new_model_score - self.last_model_score
                change_percent = (score_change / self.last_model_score * 100) if self.last_model_score != 0 else float('inf')
                status_emoji = "🔼" if score_change > 0 else "🔽" if score_change < 0 else "⏸️"
                
                logger.info(f"{status_emoji} [Evolução] Performance do Modelo: {new_model_score:.4f} (Anterior: {self.last_model_score:.4f})")
                logger.info(f"{status_emoji} [Evolução] Mudança: {score_change:+.4f} ({change_percent:+.2f}%)")

                if score_change > 0.01:
                    logger.info("✅ [Evolução] Análise: O sistema está a aprender a executar missões de forma mais eficiente.")
                elif score_change < -0.01:
                    logger.warning("⚠️ [Evolução] Análise: A performance do modelo diminuiu.")
                else:
                    logger.info("ℹ️ [Evolução] Análise: A performance do modelo está estável.")

                self.last_model_score = new_model_score
                self.training_data.clear()
                logger.info(f"🧠 [Evolução] Ciclo concluído. Próximo ciclo em 10 minutos.")
                logger.info("="*50)

            except Exception as e:
                logger.error(f"❌ [Evolução] Falha crítica no ciclo de treinamento: {e}", exc_info=True)

    async def _internal_handle_message(self, message: AgentMessage):
        """Recebe os dados de treino do Orquestrador."""
        if message.message_type == MessageType.NOTIFICATION and message.content.get("event_type") == "training_data":
            try:
                data = message.content.get("data", {})
                
                if 'timestamp' in data and isinstance(data['timestamp'], str):
                    data['timestamp'] = datetime.fromisoformat(data['timestamp'])
                
                # A correção está aqui: o dicionário 'data' já contém todos os campos.
                data_point = TrainingDataPoint(**data)
                self.training_data.append(data_point)
                
            except Exception as e:
                logger.error(f"Erro ao processar ponto de treino: {e}")

def create_evolution_engine_agents(message_bus) -> List[BaseNetworkAgent]:
    return [EvolutionEngineAgent("evolution_engine_001", message_bus)]
