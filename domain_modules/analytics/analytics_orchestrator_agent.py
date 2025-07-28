#!/usr/bin/env python3
"""
Módulo do Agente Orquestrador de Analytics - SUNA-ALSHAM (ALSHAM GLOBAL)

Este agente atua como o ponto central de entrada e coordenação para todas
as tarefas relacionadas à análise de dados e inteligência de negócios. Ele recebe
requisições de alto nível e as delega para os agentes especialistas apropriados.
"""

import logging
from typing import Any, Dict, List

# Importa a classe base e os tipos essenciais do núcleo do sistema
from suna_alsham_core.multi_agent_network import (
    AgentMessage, 
    AgentType,
    BaseNetworkAgent, 
    MessageType, 
    Priority
)

# --- IMPORTAÇÕES ATUALIZADAS ---
from .data_collector_agent import DataCollectorAgent
from .data_processing_agent import DataProcessingAgent
from .predictive_analysis_agent import PredictiveAnalysisAgent
# -----------------------------

logger = logging.getLogger(__name__)


class AnalyticsOrchestratorAgent(BaseNetworkAgent):
    """
    O agente orquestrador para o domínio de Analytics.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o AnalyticsOrchestratorAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,  # Este é um agente de domínio de negócio
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "analytics_orchestration",
            "task_delegation",
            "data_aggregation",
            "report_generation"
        ])
        logger.info(f"🧠 Agente Orquestrador de Analytics ({self.agent_id}) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa mensagens recebidas, especificamente requisições de análise.
        """
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            
            # [LÓGICA FUTURA]
            # Aqui entrará a lógica para delegar a tarefa ao agente correto.
            # Ex: se request_type for "generate_sales_forecast", ele chamará o
            # "predictive_text_agent".
            
            logger.info(
                f"Orquestrador de Analytics recebeu a requisição '{request_type}'. "
                f"Delegação ainda não implementada."
            )
            
            # Por enquanto, apenas acusa o recebimento e conclui a tarefa.
            response_content = {
                "status": "received",
                "message": f"Requisição '{request_type}' recebida pelo orquestrador, aguardando implementação dos agentes especialistas.",
                "original_request": message.content
            }
            
            response = self.create_response(message, response_content)
            await self.message_bus.publish(response)
        else:
            # Ignora mensagens que não são requisições diretas por enquanto.
            pass

    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ponto de entrada para a execução de uma tarefa de análise completa.
        """
        logger.info(f"Executando tarefa de orquestração: {task_data.get('name')}")
        # [LÓGICA FUTURA]
        # A lógica principal de orquestração será implementada aqui.
        return {"status": "success", "result": "Orquestração concluída (simulação)."}


def create_analytics_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Função de fábrica para criar todos os agentes do módulo de Analytics.
    O agent_loader.py usará esta função para instanciar os agentes.
    """
    logger.info("🔧 Criando agentes do domínio de Analytics & Intelligence...")
    
    # --- LISTA DE AGENTES ATUALIZADA ---
    agents = [
        AnalyticsOrchestratorAgent("analytics_orchestrator_001", message_bus),
        DataCollectorAgent("data_collector_001", message_bus),
        DataProcessingAgent("data_processing_001", message_bus),
        PredictiveAnalysisAgent("predictive_analysis_001", message_bus)
    ]
    # ------------------------------------
    
    logger.info(f"✅ {len(agents)} agentes de Analytics criados.")
    return agents
