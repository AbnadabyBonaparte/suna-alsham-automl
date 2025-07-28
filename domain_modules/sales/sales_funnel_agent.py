#!/usr/bin/env python3
"""
Módulo do Agente de Funil de Vendas - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente é especializado em analisar e otimizar o funil de vendas.
Ele se integra com o AIPoweredAgent para analisar o comportamento dos leads,
identificar em qual estágio do funil eles estão e sugerir as próximas ações.
"""

import logging
import uuid
from typing import Any, Dict

# Importa a classe base e os tipos essenciais do núcleo do sistema
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


class SalesFunnelAgent(BaseNetworkAgent):
    """
    Agente especialista em analisar a jornada do cliente no funil de vendas.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SalesFunnelAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "sales_funnel_analysis",
            "lead_stage_identification",
            "next_best_action_suggestion",
            "conversion_optimization",
        ])
        # Armazena o estado das análises de funil em andamento
        self.pending_analyses = {}
        logger.info(f"💰 Agente de Funil de Vendas ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa requisições para analisar leads ou respostas do AIPoweredAgent.
        """
        if message.message_type == MessageType.RESPONSE:
            await self._handle_ai_response(message)
            return

        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "analyze_lead_stage":
            await self.handle_analyze_lead_request(message)

    async def handle_analyze_lead_request(self, original_message: AgentMessage):
        """
        Recebe os dados de um lead, cria um prompt para a IA e delega a análise.
        """
        lead_data = original_message.content.get("lead_data")
        if not lead_data or not isinstance(lead_data, dict):
            await self.publish_error_response(original_message, "Dados do lead inválidos ou não fornecidos.")
            return

        logger.info(f"Analisando lead ID: {lead_data.get('id', 'N/A')}")

        # 1. Engenharia de Prompt para análise de funil
        prompt = (
            "Analise os seguintes dados de um lead e determine seu estágio no funil de vendas "
            "(Topo, Meio ou Fundo) e sugira a 'próxima melhor ação'.\n"
            f"Dados do Lead: {lead_data}\n"
            "Responda em formato JSON com as chaves 'funnel_stage' e 'next_best_action'."
        )
        
        # 2. Cria uma mensagem para o AIPoweredAgent
        analysis_id = str(uuid.uuid4())
        request_to_ai = self.create_message(
            recipient_id="ai_powered_001",
            message_type=MessageType.REQUEST,
            content={
                "request_type": "generate_structured_text", # Pedido de JSON
                "prompt": prompt,
            },
            callback_id=analysis_id
        )

        # 3. Armazena o contexto da análise
        self.pending_analyses[analysis_id] = {
            "original_message": original_message,
            "lead_id": lead_data.get("id")
        }

        # 4. Envia a requisição para o agente de IA
        await self.message_bus.publish(request_to_ai)
        logger.info(f"Requisição de análise de lead enviada para ai_powered_001 com analysis_id: {analysis_id}")

    async def _handle_ai_response(self, response_message: AgentMessage):
        """
        Processa a resposta com a análise do lead vinda do AIPoweredAgent.
        """
        analysis_id = response_message.callback_id
        if analysis_id not in self.pending_analyses:
            return

        task_context = self.pending_analyses.pop(analysis_id)
        original_message = task_context["original_message"]
        
        if response_message.content.get("status") != "completed":
            logger.error(f"Análise de lead pela IA falhou para a tarefa {analysis_id}.")
            await self.publish_error_response(original_message, "Falha na análise do lead pela IA.")
            return

        analysis_result = response_message.content.get("result", {}).get("structured_data", {})
        logger.info(f"Análise de lead recebida da IA para a tarefa {analysis_id}: {analysis_result}")

        # 5. Enviar a resposta final para o solicitante original
        final_response_content = {
            "status": "completed",
            "lead_id": task_context["lead_id"],
            "analysis": analysis_result
        }
        final_response = self.create_response(original_message, final_response_content)
        await self.message_bus.publish(final_response)
