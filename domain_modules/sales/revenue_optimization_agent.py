#!/usr/bin/env python3
"""
Módulo do Agente de Otimização de Receita - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente analisa dados históricos de vendas e comportamento do cliente
para identificar oportunidades de aumento de receita, como cross-selling,
up-selling e pacotes de produtos.
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
)

logger = logging.getLogger(__name__)


class RevenueOptimizationAgent(BaseNetworkAgent):
    """
    Agente especialista em encontrar oportunidades para maximizar a receita.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o RevenueOptimizationAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "cross_sell_analysis",
            "up_sell_identification",
            "customer_ltv_prediction",
        ])
        # Armazena o estado das análises de otimização em andamento
        self.pending_optimizations = {}
        logger.info(f"📈 Agente de Otimização de Receita ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa requisições para otimizar a receita de um cliente ou respostas do AIPoweredAgent.
        """
        if message.message_type == MessageType.RESPONSE:
            await self._handle_ai_response(message)
            return

        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "find_revenue_opportunity":
            await self.handle_find_opportunity_request(message)

    async def handle_find_opportunity_request(self, original_message: AgentMessage):
        """
        Recebe dados do cliente, cria um prompt e delega a análise de oportunidade.
        """
        customer_history = original_message.content.get("customer_history", {})
        available_products = original_message.content.get("available_products", [])

        if not customer_history or not available_products:
            await self.publish_error_response(original_message, "Histórico do cliente ou produtos disponíveis não fornecidos.")
            return

        customer_id = customer_history.get('customer_id', 'N/A')
        logger.info(f"Buscando oportunidades de receita para o cliente: {customer_id}")

        # 1. Engenharia de Prompt para encontrar oportunidades
        prompt = (
            "Aja como um estrategista de vendas. Analise o histórico de compras do cliente abaixo, "
            "compare com a lista de produtos disponíveis e identifique a melhor oportunidade de "
            "cross-sell ou up-sell. Descreva a oportunidade e justifique sua escolha.\n"
            f"Histórico do Cliente: {customer_history}\n"
            f"Produtos Disponíveis: {available_products}\n"
            "Responda em formato JSON com as chaves 'opportunity_type' (cross-sell/up-sell), "
            "'suggested_product_id' (string) e 'justification' (string)."
        )
        
        # 2. Cria uma mensagem para o AIPoweredAgent
        optimization_id = str(uuid.uuid4())
        request_to_ai = self.create_message(
            recipient_id="ai_powered_001",
            message_type=MessageType.REQUEST,
            content={"request_type": "generate_structured_text", "prompt": prompt},
            callback_id=optimization_id
        )

        # 3. Armazena o contexto
        self.pending_optimizations[optimization_id] = {
            "original_message": original_message,
            "customer_id": customer_id
        }

        # 4. Envia a requisição
        await self.message_bus.publish(request_to_ai)
        logger.info(f"Requisição de otimização de receita enviada para ai_powered_001 com ID: {optimization_id}")

    async def _handle_ai_response(self, response_message: AgentMessage) -> None:
        """
        Handles the response containing the revenue opportunity suggestion from the AIPoweredAgent.

        This method validates the optimization context, checks the completion status,
        logs all relevant events, and sends the final response to the original requester.
        Robust error handling is provided for diagnostics and production reliability.

        Args:
            response_message (AgentMessage): The message containing the AI opportunity suggestion response.

        Returns:
            None
        """
        optimization_id: str = response_message.callback_id
        if optimization_id not in self.pending_optimizations:
            logger.warning(f"[RevenueOptimizationAgent] Optimization ID '{optimization_id}' não encontrado em pending_optimizations.")
            return

        task_context: Dict[str, Any] = self.pending_optimizations.pop(optimization_id)
        original_message: AgentMessage = task_context["original_message"]

        if response_message.content.get("status") != "completed":
            logger.error(f"[RevenueOptimizationAgent] Falha na análise de oportunidade pela IA para a tarefa {optimization_id}.")
            await self.publish_error_response(original_message, "Falha na análise de oportunidade pela IA.")
            return

        opportunity: Dict[str, Any] = response_message.content.get("result", {}).get("structured_data", {})
        logger.info(f"[RevenueOptimizationAgent] Oportunidade de receita encontrada pela IA: {opportunity}")

        # Envia a resposta final
        final_response_content: Dict[str, Any] = {
            "status": "completed",
            "customer_id": task_context["customer_id"],
            "opportunity": opportunity
        }
        final_response: AgentMessage = self.create_response(original_message, final_response_content)
        await self.message_bus.publish(final_response)
