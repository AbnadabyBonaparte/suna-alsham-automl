#!/usr/bin/env python3
"""
Módulo do Agente Orquestrador de Analytics - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Final Fortalecida]
Este agente atua como um gerente de pipeline, coordenando uma sequência de
tarefas entre os agentes especialistas para executar uma análise completa,
desde a coleta de dados até a geração do relatório final.
"""

import logging
import uuid
from typing import Any, Dict, List

# Importa a classe base e os tipos essenciais do núcleo
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

# Importa todos os agentes especialistas do módulo de Analytics
from .data_collector_agent import DataCollectorAgent
from .data_processing_agent import DataProcessingAgent
from .predictive_analysis_agent import PredictiveAnalysisAgent
from .reporting_visualization_agent import ReportingVisualizationAgent

logger = logging.getLogger(__name__)


class AnalyticsOrchestratorAgent(BaseNetworkAgent):
    """
    O agente orquestrador que gerencia o fluxo de trabalho do módulo de Analytics.
    """

    def __init__(self, agent_id: str, message_bus):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend(["analytics_pipeline_management", "workflow_coordination"])
        
        self.pending_pipelines = {}
        logger.info(f"mgr 🧠 Agente Orquestrador de Analytics ({self.agent_id}) fortalecido com lógica de pipeline.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.RESPONSE:
            await self._handle_pipeline_step_response(message)
            return
            
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "run_full_analysis_pipeline":
            await self.handle_run_pipeline_request(message)

    async def handle_run_pipeline_request(self, original_message: AgentMessage):
        """Inicia e executa o primeiro passo de um pipeline de análise completo."""
        pipeline_id = str(uuid.uuid4())
        params = original_message.content.get("params", {})
        
        # Armazena o estado completo do pipeline
        self.pending_pipelines[pipeline_id] = {
            "original_message": original_message,
            "params": params,
            "current_step": "collecting",
            "data": None, # Para armazenar os dados entre os passos
        }
        
        logger.info(f"Iniciando novo pipeline de análise [ID: {pipeline_id}]. Passo 1: Coleta de Dados.")
        
        # Passo 1: Chamar o DataCollectorAgent
        collect_request = self.create_message(
            recipient_id="data_collector_001",
            message_type=MessageType.REQUEST,
            content={
                "request_type": "collect_sql_data",
                "query": params.get("sql_query")
            },
            callback_id=pipeline_id
        )
        await self.message_bus.publish(collect_request)

    async def _handle_pipeline_step_response(self, response: AgentMessage):
        """
        Recebe a resposta de um passo do pipeline e dispara o próximo.
        """
        pipeline_id = response.callback_id
        if pipeline_id not in self.pending_pipelines:
            return

        pipeline_context = self.pending_pipelines[pipeline_id]
        
        if response.content.get("status") != "completed":
            logger.error(f"Pipeline [ID: {pipeline_id}] falhou no passo '{pipeline_context['current_step']}'.")
            await self.publish_error_response(pipeline_context["original_message"], f"Pipeline falhou: {response.content.get('message')}")
            del self.pending_pipelines[pipeline_id]
            return

        # --- Lógica de transição de estados do pipeline ---
        
        # Da Coleta para o Processamento
        if pipeline_context["current_step"] == "collecting":
            logger.info(f"Pipeline [ID: {pipeline_id}] Passo 1 concluído. Passo 2: Processamento de Dados.")
            pipeline_context["current_step"] = "processing"
            pipeline_context["data"] = response.content.get("data_preview", []) # Usamos o preview como dados
            
            process_request = self.create_message(
                "data_processing_001", MessageType.REQUEST,
                {"request_type": "process_data", "data": pipeline_context["data"], "steps": pipeline_context["params"].get("processing_steps")},
                callback_id=pipeline_id
            )
            await self.message_bus.publish(process_request)

        # Do Processamento para a Análise Preditiva
        elif pipeline_context["current_step"] == "processing":
            logger.info(f"Pipeline [ID: {pipeline_id}] Passo 2 concluído. Passo 3: Análise Preditiva.")
            pipeline_context["current_step"] = "predicting"
            pipeline_context["data"] = response.content.get("processed_data_preview", [])
            
            predict_request = self.create_message(
                "predictive_analysis_001", MessageType.REQUEST,
                {"request_type": "predict_with_model", "model_path": pipeline_context["params"].get("model_path"), "input_data": pipeline_context["data"]},
                callback_id=pipeline_id
            )
            await self.message_bus.publish(predict_request)

        # Da Análise para a Visualização
        elif pipeline_context["current_step"] == "predicting":
            logger.info(f"Pipeline [ID: {pipeline_id}] Passo 3 concluído. Passo 4: Geração de Relatório.")
            pipeline_context["current_step"] = "reporting"
            pipeline_context["data"]["prediction"] = response.content.get("prediction")

            # Prepara dados para o gráfico
            chart_data = [{"category": f"Item {i+1}", "value": val} for i, val in enumerate(response.content.get("prediction", []))]

            report_request = self.create_message(
                "reporting_visualization_001", MessageType.REQUEST,
                {"request_type": "generate_chart", "dataset": chart_data, "chart_spec": pipeline_context["params"].get("chart_spec")},
                callback_id=pipeline_id
            )
            await self.message_bus.publish(report_request)
            
        # Da Visualização para a Resposta Final
        elif pipeline_context["current_step"] == "reporting":
            logger.info(f"Pipeline [ID: {pipeline_id}] Passo 4 concluído. Finalizando pipeline.")
            final_report_path = response.content.get("chart_path")
            
            final_response = self.create_response(
                pipeline_context["original_message"],
                {"status": "completed", "message": "Pipeline de análise concluído com sucesso.", "report_path": final_report_path}
            )
            await self.message_bus.publish(final_response)
            del self.pending_pipelines[pipeline_id] # Limpa o estado

# Função de fábrica que o agent_loader usará
def create_analytics_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria e retorna todos os agentes do módulo de Analytics."""
    logger.info("🔧 Criando agentes do domínio de Analytics & Intelligence...")
    agents = [
        AnalyticsOrchestratorAgent("analytics_orchestrator_001", message_bus),
        DataCollectorAgent("data_collector_001", message_bus),
        DataProcessingAgent("data_processing_001", message_bus),
        PredictiveAnalysisAgent("predictive_analysis_001", message_bus),
        ReportingVisualizationAgent("reporting_visualization_001", message_bus),
    ]
    logger.info(f"✅ {len(agents)} agentes de Analytics criados.")
    return agents
