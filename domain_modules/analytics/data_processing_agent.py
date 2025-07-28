#!/usr/bin/env python3
"""
Módulo do Agente de Processamento de Dados - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente é especializado em limpar, transformar, normalizar e enriquecer
os dados brutos coletados pelo DataCollectorAgent. Ele utiliza a biblioteca
Pandas para realizar operações de data wrangling de forma eficiente.
"""

import logging
from typing import Any, Dict, List

import pandas as pd

# Importa a classe base e os tipos essenciais do núcleo do sistema
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)


class DataProcessingAgent(BaseNetworkAgent):
    """
    Agente especialista em limpar e transformar dados usando Pandas.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DataProcessingAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "data_cleaning",
            "data_transformation",
            "feature_engineering",
            "data_normalization",
        ])
        logger.info(f"🧼 Agente de Processamento de Dados ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa requisições para limpar e transformar um conjunto de dados.
        """
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "process_data":
            await self.handle_process_data_request(message)

    async def handle_process_data_request(self, message: AgentMessage):
        """
        Executa um pipeline de processamento de dados usando Pandas.
        """
        raw_data = message.content.get("data", [])
        processing_steps = message.content.get("steps", [])

        if not raw_data:
            await self.publish_error_response(message, "Nenhum dado fornecido para processamento.")
            return
        
        if not processing_steps:
            await self.publish_error_response(message, "Nenhum passo de processamento foi especificado.")
            return

        logger.info(f"Iniciando processamento de {len(raw_data)} registros com os passos: {processing_steps}")

        try:
            # 1. Converte os dados brutos para um DataFrame do Pandas
            df = pd.DataFrame(raw_data)
            original_rows = len(df)

            # 2. Executa os passos de processamento em sequência
            for step in processing_steps:
                step_config = step if isinstance(step, dict) else {"name": step}
                step_name = step_config["name"]

                if step_name == "remove_duplicates":
                    df.drop_duplicates(inplace=True)
                elif step_name == "handle_missing_values":
                    # Exemplo: preenche valores nulos com uma string ou a média
                    fill_value = step_config.get("fill_value", 'N/A')
                    subset = step_config.get("subset") # colunas específicas
                    df.fillna(value=fill_value, subset=subset, inplace=True)
                elif step_name == "convert_data_types":
                    # Exemplo: {"name": "convert_data_types", "column": "price", "type": "float"}
                    column = step_config.get("column")
                    target_type = step_config.get("type")
                    if column and target_type:
                        df[column] = df[column].astype(target_type)
                # Outros passos podem ser adicionados aqui (ex: normalização, etc.)
            
            processed_rows = len(df)
            logger.info(f"Processamento concluído. Registros originais: {original_rows}, Registros processados: {processed_rows}.")

            # 3. Converte o DataFrame limpo de volta para o formato de dicionário
            processed_data = df.to_dict(orient='records')
            
            response_content = {
                "status": "completed",
                "original_rows": original_rows,
                "processed_rows": processed_rows,
                "steps_applied": [s if isinstance(s, str) else s.get("name") for s in processing_steps],
                "processed_data_preview": processed_data[:5]
            }
            await self.publish_response(message, response_content)

        except Exception as e:
            logger.error(f"Erro ao processar dados: {e}", exc_info=True)
            await self.publish_error_response(message, f"Ocorreu um erro interno durante o processamento dos dados: {e}")
