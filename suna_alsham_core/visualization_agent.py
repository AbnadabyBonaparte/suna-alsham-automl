#!/usr/bin/env python3
"""
Módulo do Visualization Agent - SUNA-ALSHAM

Define o agente especializado na criação de dashboards e gráficos avançados,
utilizando bibliotecas como Plotly para visualizações interativas.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# [AUTENTICIDADE] As bibliotecas de visualização são importações pesadas.
# Em uma implementação futura, podem ser carregadas dinamicamente para otimizar o startup.
try:
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class ChartType(Enum):
    """Tipos de gráficos suportados pelo agente."""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    GAUGE = "gauge"
    TIME_SERIES = "time_series"


@dataclass
class ChartConfig:
    """Representa a configuração para a criação de um gráfico."""
    chart_id: str
    chart_type: ChartType
    title: str
    data_source_agent: str  # Agente que fornecerá os dados
    query: Dict[str, Any]    # Pergunta a ser feita ao agente de dados


# --- Classe Principal do Agente ---

class VisualizationAgent(BaseNetworkAgent):
    """
    Agente especializado em criar visualizações de dados e dashboards.
    Ele consome dados de outros agentes e os transforma em gráficos interativos.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o VisualizationAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "chart_generation",
            "dashboard_creation",
            "real_time_visualization",
            "interactive_plots",
        ])
        
        if not PLOTLY_AVAILABLE:
            self.status = "degraded"
            logger.critical("Biblioteca 'plotly' ou 'pandas' não encontrada. O VisualizationAgent operará em modo degradado.")
        
        self.chart_cache: Dict[str, Any] = {}
        logger.info(f"📊 {self.agent_id} (Visualização) inicializado.")

    async def handle_message(self, message: AgentMessage):
        """Processa requisições para criação de visualizações."""
        await super().handle_message(message)
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            if request_type == "create_chart":
                result = await self.create_chart(message.content)
                await self.message_bus.publish(self.create_response(message, result))
            else:
                logger.warning(f"Ação de visualização desconhecida: {request_type}")

    async def create_chart(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um gráfico a partir de uma configuração e dados fornecidos.

        Args:
            request_data: Dicionário com 'chart_type', 'data' e 'config'.

        Returns:
            Um dicionário contendo o gráfico em formato JSON (Plotly) ou um erro.
        """
        if self.status != "active":
            return {"status": "error", "message": "Serviço de visualização indisponível (dependências faltando)."}
        
        chart_type = ChartType(request_data.get("chart_type", "line"))
        data = request_data.get("data", [])
        config = request_data.get("config", {})
        
        if not data:
            return {"status": "error", "message": "Nenhum dado fornecido para criar o gráfico."}
        
        try:
            logger.info(f"🎨 Criando gráfico do tipo: {chart_type.value}")
            df = pd.DataFrame(data)
            fig = None

            if chart_type == ChartType.LINE:
                fig = px.line(df, x=config.get("x"), y=config.get("y"), title=config.get("title"))
            elif chart_type == ChartType.BAR:
                fig = px.bar(df, x=config.get("x"), y=config.get("y"), title=config.get("title"))
            elif chart_type == ChartType.PIE:
                fig = px.pie(df, names=config.get("names"), values=config.get("values"), title=config.get("title"))
            
            if fig:
                # Aplica um tema padrão para consistência visual
                fig.update_layout(template="plotly_dark")
                return {"status": "completed", "chart_json": fig.to_json()}
            else:
                return {"status": "error", "message": f"Tipo de gráfico '{chart_type.value}' não suportado."}

        except Exception as e:
            logger.error(f"❌ Erro ao criar gráfico: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}


def create_visualization_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Visualização."""
    agents = []
    logger.info("📊 Criando VisualizationAgent...")
    try:
        agent = VisualizationAgent("visualization_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando VisualizationAgent: {e}", exc_info=True)
    return agents
