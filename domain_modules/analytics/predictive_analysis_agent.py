#!/usr/bin/env python3
"""
Módulo do Agente de Análise Preditiva - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente utiliza técnicas de machine learning com Scikit-Learn para analisar
os dados processados. Ele é capaz de treinar modelos, salvá-los para uso
futuro e carregá-los para fazer previsões.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Importa a classe base e os tipos essenciais do núcleo do sistema
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)


class PredictiveAnalysisAgent(BaseNetworkAgent):
    """
    Agente especialista em aplicar modelos de machine learning com Scikit-Learn.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o PredictiveAnalysisAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "model_training",
            "model_prediction",
            "model_persistence",
        ])
        
        self.models_dir = Path("./trained_models")
        self.models_dir.mkdir(exist_ok=True)
        
        logger.info(f"📈 Agente de Análise Preditiva ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para treinar um modelo ou fazer uma previsão."""
        request_type = message.content.get("request_type")
        
        if request_type == "train_model":
            await self.handle_train_model_request(message)
        elif request_type == "predict_with_model":
            await self.handle_predict_request(message)
        else:
            await self.publish_error_response(message, f"Tipo de requisição desconhecido: {request_type}")

    async def handle_train_model_request(self, message: AgentMessage):
        """Lida com o treinamento e salvamento de um modelo de ML."""
        model_type = message.content.get("model_type", "linear_regression")
        dataset = message.content.get("dataset", [])
        target_column = message.content.get("target_column")
        feature_columns = message.content.get("feature_columns", [])

        if not all([dataset, target_column, feature_columns]):
            await self.publish_error_response(message, "Dados insuficientes para treinamento (requer dataset, target_column, feature_columns).")
            return
            
        model_filename = f"{model_type}_{target_column}_{self.timestamp}.joblib"
        model_path = self.models_dir / model_filename

        logger.info(f"Iniciando treinamento do modelo '{model_type}' para prever '{target_column}'.")

        try:
            df = pd.DataFrame(dataset)
            X = df[feature_columns]
            y = df[target_column]
            
            # TODO: Adicionar train_test_split para avaliação real
            # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            
            if model_type == "linear_regression":
                model = LinearRegression()
            else:
                # Placeholder para outros tipos de modelo
                await self.publish_error_response(message, f"Tipo de modelo '{model_type}' não suportado.")
                return

            model.fit(X, y)
            
            # Salva o modelo treinado
            joblib.dump(model, model_path)
            
            logger.info(f"Modelo treinado com sucesso e salvo em: {model_path}")
            
            response_content = {
                "status": "completed",
                "message": "Modelo treinado com sucesso.",
                "model_path": str(model_path),
                # TODO: Retornar métricas de avaliação do modelo (ex: R^2, MSE)
            }
            await self.publish_response(message, response_content)

        except Exception as e:
            logger.error(f"Erro ao treinar o modelo: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro interno durante o treinamento: {e}")

    async def handle_predict_request(self, message: AgentMessage) -> None:
        """
        Handles loading a trained model and performing a prediction on input data.

        This method validates the model path and input data, loads the model using joblib,
        prepares the input as a DataFrame, performs the prediction, and returns the result.
        Robust error handling and logging are provided for diagnostics and production reliability.

        Args:
            message (AgentMessage): The incoming message containing model path and input data.

        Returns:
            None
        """
        model_path_str: str = message.content.get("model_path")
        input_data: List[dict] = message.content.get("input_data", [])

        if not model_path_str or not Path(model_path_str).exists():
            logger.warning(f"[PredictiveAnalysisAgent] Arquivo do modelo não encontrado em: {model_path_str}")
            await self.publish_error_response(message, f"Arquivo do modelo não encontrado em: {model_path_str}")
            return

        logger.info(f"[PredictiveAnalysisAgent] Carregando modelo de '{model_path_str}' para fazer previsão.")

        try:
            model = joblib.load(model_path_str)

            # Prepara os dados de entrada
            input_df = pd.DataFrame(input_data)
            if input_df.empty:
                logger.warning("[PredictiveAnalysisAgent] Nenhum dado de entrada fornecido para previsão.")
                await self.publish_error_response(message, "Nenhum dado de entrada fornecido para previsão.")
                return

            prediction = model.predict(input_df)

            response_content: Dict[str, Any] = {
                "status": "completed",
                "prediction": prediction.tolist()  # Converte array numpy para lista
            }
            await self.publish_response(message, response_content)

        except Exception as e:
            logger.critical(f"[PredictiveAnalysisAgent] Erro ao fazer a previsão: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro interno durante a previsão: {e}")
