#!/usr/bin/env python3
"""
Módulo do Agente Otimizador de Preços - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente usa IA para analisar dados de mercado, custos, características
do produto e preços de concorrentes para recomendar um preço de venda ótimo.
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


class PricingOptimizerAgent(BaseNetworkAgent):
    """
    Agente especialista em otimização de estratégia de preços.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o PricingOptimizerAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "dynamic_pricing",
            "competitor_price_analysis",
            "demand_forecasting",
            "margin_optimization",
        ])
        # Armazena o estado das otimizações em andamento
        self.pending_optimizations = {}
        logger.info(f"💲 Agente Otimizador de Preços ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa requisições para otimizar preços ou respostas do AIPoweredAgent.
        """
        if message.message_type == MessageType.RESPONSE:
            await self._handle_ai_response(message)
            return

        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "optimize_price":
            await self.handle_optimize_price_request(message)

    async def handle_optimize_price_request(self, original_message: AgentMessage):
        """
        Recebe dados do produto e do mercado, cria um prompt e delega a análise de preço.
        """
        product_data = original_message.content.get("product_data", {})
        market_data = original_message.content.get("market_data", {})

        if not product_data:
            await self.publish_error_response(original_message, "Dados do produto não fornecidos para otimização.")
            return

        logger.info(f"Iniciando otimização de preço para o produto: {product_data.get('name', 'N/A')}")

        # 1. Engenharia de Prompt para otimização de preço
        prompt = (
            "Aja como um especialista em precificação. Analise os dados do produto e do mercado abaixo. "
            "Sugira um preço de venda ótimo e forneça uma breve justificativa para sua recomendação.\n"
            f"Dados do Produto: {product_data}\n"
            f"Dados de Mercado e Concorrência: {market_data}\n"
            "Responda em formato JSON com as chaves 'suggested_price' (float), 'currency' (string) e 'rationale' (string)."
        )
        
        # 2. Cria uma mensagem para o AIPoweredAgent
        optimization_id = str(uuid.uuid4())
        request_to_ai = self.create_message(
            recipient_id="ai_powered_001",
            message_type=MessageType.REQUEST,
            content={
                "request_type": "generate_structured_text",
                "prompt": prompt,
            },
            callback_id=optimization_id
        )

        # 3. Armazena o contexto da otimização
        self.pending_optimizations[optimization_id] = {
            "original_message": original_message,
            "product_name": product_data.get("name")
        }

        # 4. Envia a requisição para o agente de IA
        await self.message_bus.publish(request_to_ai)
        logger.info(f"Requisição de otimização de preço enviada para ai_powered_001 com optimization_id: {optimization_id}")

    async def _handle_ai_response(self, response_message: AgentMessage):
        """
        Processa a resposta com a sugestão de preço vinda do AIPoweredAgent.
        """
        optimization_id = response_message.callback_id
        if optimization_id not in self.pending_optimizations:
            return

        task_context = self.pending_optimizations.pop(optimization_id)
        original_message = task_context["original_message"]
        
        if response_message.content.get("status") != "completed":
            logger.error(f"Otimização de preço pela IA falhou para a tarefa {optimization_id}.")
            await self.publish_error_response(original_message, "Falha na otimização de preço pela IA.")
            return

        price_suggestion = response_message.content.get("result", {}).get("structured_data", {})
        logger.info(f"Sugestão de preço recebida da IA para a tarefa {optimization_id}: {price_suggestion}")

        # 5. Enviar a resposta final para o solicitante original
        final_response_content = {
            "status": "completed",
            "product_name": task_context["product_name"],
            "suggestion": price_suggestion
        }
        final_response = self.create_response(original_message, final_response_content)
        await self.message_bus.publish(final_response)
