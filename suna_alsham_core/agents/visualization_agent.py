#!/usr/bin/env python3
"""
Módulo do Visualization Agent - SUNA-ALSHAM

[Fase 2] - Fortalecido com lógica real para solicitar dados de outros
agentes antes de gerar as visualizações.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

# [AUTENTICIDADE] As bibliotecas de visualização são importadas de forma segura.
try:
    import pandas as pd
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses para Tipagem Forte ---

class ChartType(Enum):
    """Tipos de gráficos suportados pelo agente."""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"


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
            "interactive_plots",
        ])
        
        if not PLOTLY_AVAILABLE:
            self.status = "degraded"
            logger.critical("Bibliotecas 'plotly' ou 'pandas' não encontradas. O VisualizationAgent operará em modo degradado.")
        
        logger.info(f"📊 {self.agent_id} (Visualização) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para criação de visualizações."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        if request_type == "create_chart":
            result = await self.create_chart(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            logger.warning(f"Ação de visualização desconhecida: {request_type}")
            await self.message_bus.publish(self.create_error_response(message, "Ação de visualização desconhecida"))

    async def create_chart(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um gráfico a partir de uma configuração, buscando os dados
        necessários de outros agentes.
        """
        if self.status == "degraded":
            return {"status": "error", "message": "Serviço de visualização indisponível (dependências faltando)."}
        
        chart_type = ChartType(request_data.get("chart_type", "line"))
        config = request_data.get("config", {})
        data_source_agent = config.get("data_source_agent")
        query = config.get("query")

        if not all([data_source_agent, query]):
            return {"status": "error", "message": "Fonte de dados ou query não especificadas na configuração."}

        try:
            # [LÓGICA REAL] Solicita os dados ao agente especificado.
            logger.info(f"Solicitando dados para o gráfico do agente '{data_source_agent}'...")
            response_message = await self.send_request_and_wait(
                recipient_id=data_source_agent,
                content={"request_type": "execute_query", "query": query}
            )

            data = response_message.content.get("data", [])
            if not data:
                return {"status": "completed", "message": "Nenhum dado retornado para visualização."}

            logger.info(f"🎨 Criando gráfico do tipo: {chart_type.value} com {len(data)} registros.")
            df = pd.DataFrame(data)
            fig = None

            # [AUTENTICIDADE] A lógica de criação de gráficos agora é real e baseada nos dados recebidos.
            if chart_type == ChartType.LINE:
                fig = px.line(df, x=config.get("x"), y=config.get("y"), title=config.get("title"))
            elif chart_type == ChartType.BAR:
                fig = px.bar(df, x=config.get("x"), y=config.get("y"), title=config.get("title"))
            elif chart_type == ChartType.PIE:
                fig = px.pie(df, names=config.get("names"), values=config.get("values"), title=config.get("title"))
            
            if fig:
                fig.update_layout(template="plotly_dark")
                return {"status": "completed", "chart_json": fig.to_json()}
            else:
                return {"status": "error", "message": f"Tipo de gráfico '{chart_type.value}' não suportado."}

        except TimeoutError:
            return {"status": "error", "message": f"Timeout: O agente '{data_source_agent}' não respondeu a tempo."}
        except Exception as e:
            logger.error(f"❌ Erro ao criar gráfico: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}


def create_visualization_agent(message_bus) -> List[BaseNetworkAgent]:
    """
    Factory function to create and initialize the VisualizationAgent(s) for the ALSHAM QUANTUM system.

    This function instantiates the VisualizationAgent, logs all relevant events for diagnostics,
    and returns it in a list for registration in the agent registry. Handles errors robustly
    and ensures the agent is ready for operation.

    Args:
        message_bus (Any): The message bus or communication channel for agent messaging.

    Returns:
        List[BaseNetworkAgent]: A list containing the initialized VisualizationAgent instance(s).
    """
    agents: List[BaseNetworkAgent] = []
    logger.info("📊 [Factory] Criando VisualizationAgent...")
    try:
        agent = VisualizationAgent("visualization_001", message_bus)
        agents.append(agent)
        logger.info(f"📊 VisualizationAgent criado com sucesso: {agent.agent_id}")
    except Exception as e:
        logger.critical(f"❌ Erro crítico ao criar VisualizationAgent: {e}", exc_info=True)
    return agents
