#!/usr/bin/env python3
"""
Módulo do Agente de Relatórios e Visualização - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente é especializado em transformar dados e resultados de análises
em relatórios e visualizações compreensíveis. Ele usa Matplotlib e Seaborn
para gerar gráficos e salvá-los como imagens.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Importa a classe base e os tipos essenciais do núcleo do sistema
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)


class ReportingVisualizationAgent(BaseNetworkAgent):
    """
    Agente especialista em criar relatórios e visualizações de dados.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o ReportingVisualizationAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "chart_generation",
            "data_visualization",
            "pdf_export",
        ])
        
        self.output_dir = Path("./generated_reports")
        self.output_dir.mkdir(exist_ok=True)
        
        # Configura um estilo visual padrão para os gráficos
        sns.set_theme(style="whitegrid")
        
        logger.info(f"📊 Agente de Relatórios e Visualização ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para gerar uma visualização."""
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "generate_chart":
            await self.handle_generate_chart_request(message)

    async def handle_generate_chart_request(self, message: AgentMessage):
        """
        Lida com a lógica de gerar um arquivo de imagem de um gráfico.
        """
        chart_spec = message.content.get("chart_spec", {})
        dataset = message.content.get("dataset", [])

        if not chart_spec or not dataset:
            await self.publish_error_response(message, "Especificação do gráfico ou dados não fornecidos.")
            return

        chart_type = chart_spec.get("type")
        x_axis = chart_spec.get("x_axis")
        y_axis = chart_spec.get("y_axis")
        title = chart_spec.get("title", "Gráfico Gerado")
        
        output_filename = f"{title.replace(' ', '_').lower()}_{self.timestamp}.png"
        output_path = self.output_dir / output_filename

        logger.info(f"Gerando gráfico do tipo '{chart_type}' com título '{title}'.")

        try:
            df = pd.DataFrame(dataset)
            
            # Cria a figura do gráfico
            plt.figure(figsize=(10, 6))
            
            # Escolhe o tipo de gráfico
            if chart_type == "bar":
                sns.barplot(x=x_axis, y=y_axis, data=df)
            elif chart_type == "line":
                sns.lineplot(x=x_axis, y=y_axis, data=df)
            elif chart_type == "scatter":
                sns.scatterplot(x=x_axis, y=y_axis, data=df)
            else:
                await self.publish_error_response(message, f"Tipo de gráfico '{chart_type}' não suportado.")
                return

            plt.title(title)
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)
            plt.tight_layout()
            
            # Salva a figura em um arquivo
            plt.savefig(output_path)
            plt.close() # Libera a memória da figura

            logger.info(f"Gráfico salvo com sucesso em: {output_path}")

            response_content = {
                "status": "completed",
                "chart_path": str(output_path),
                "chart_type": chart_type,
            }
            await self.publish_response(message, response_content)

        except Exception as e:
            logger.error(f"Erro ao gerar o gráfico: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro interno durante a geração do gráfico: {e}")
