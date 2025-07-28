#!/usr/bin/env python3
"""
Módulo do Agente de Sucesso do Cliente - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente foca na retenção e satisfação do cliente. Ele usa IA para
analisar a saúde da conta de um cliente, prever o risco de churn e
sugerir ações proativas para garantir o sucesso e a longevidade do cliente.
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


class CustomerSuccessAgent(BaseNetworkAgent):
    """
    Agente especialista em garantir a retenção e o sucesso dos clientes.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o CustomerSuccessAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "customer_health_analysis",
            "churn_risk_prediction",
            "retention_strategy_suggestion",
            "proactive_outreach",
        ])
        # Armazena o estado das análises de clientes em andamento
        self.pending_assessments = {}
        logger.info(f"❤️ Agente de Sucesso do Cliente ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa requisições para avaliar o risco do cliente ou respostas do AIPoweredAgent.
        """
        if message.message_type == MessageType.RESPONSE:
            await self._handle_ai_response(message)
            return

        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "assess_customer_risk":
            await self.handle_assess_risk_request(message)

    async def handle_assess_risk_request(self, original_message: AgentMessage):
        """
        Recebe dados do cliente, cria um prompt e delega a análise de risco.
        """
        customer_data = original_message.content.get("customer_data", {})

        if not customer_data:
            await self.publish_error_response(original_message, "Dados do cliente não fornecidos para avaliação.")
            return

        logger.info(f"Iniciando avaliação de risco para o cliente: {customer_data.get('name', 'N/A')}")

        # 1. Engenharia de Prompt para análise de retenção
        prompt = (
            "Aja como um especialista em Sucesso do Cliente. Analise os dados do cliente abaixo. "
            "Avalie o risco de churn (Baixo, Médio, Alto) e sugira uma estratégia de retenção concreta e proativa.\n"
            f"Dados do Cliente: {customer_data}\n"
            "Responda em formato JSON com as chaves 'churn_risk' (string), 'risk_level' (int de 1 a 10) e 'retention_strategy' (string)."
        )
        
        # 2. Cria uma mensagem para o AIPoweredAgent
        assessment_id = str(uuid.uuid4())
        request_to_ai = self.create_message(
            recipient_id="ai_powered_001",
            message_type=MessageType.REQUEST,
            content={
                "request_type": "generate_structured_text",
                "prompt": prompt,
            },
            callback_id=assessment_id
        )

        # 3. Armazena o contexto da avaliação
        self.pending_assessments[assessment_id] = {
            "original_message": original_message,
            "customer_name": customer_data.get("name")
        }

        # 4. Envia a requisição para o agente de IA
        await self.message_bus.publish(request_to_ai)
        logger.info(f"Requisição de avaliação de risco enviada para ai_powered_001 com assessment_id: {assessment_id}")

    async def _handle_ai_response(self, response_message: AgentMessage):
        """
        Processa a resposta com a análise de risco vinda do AIPoweredAgent.
        """
        assessment_id = response_message.callback_id
        if assessment_id not in self.pending_assessments:
            return

        task_context = self.pending_assessments.pop(assessment_id)
        original_message = task_context["original_message"]
        
        if response_message.content.get("status") != "completed":
            logger.error(f"Avaliação de risco pela IA falhou para a tarefa {assessment_id}.")
            await self.publish_error_response(original_message, "Falha na avaliação de risco pela IA.")
            return

        risk_analysis = response_message.content.get("result", {}).get("structured_data", {})
        logger.info(f"Análise de risco recebida da IA para a tarefa {assessment_id}: {risk_analysis}")

        # 5. Enviar a resposta final para o solicitante original
        final_response_content = {
            "status": "completed",
            "customer_name": task_context["customer_name"],
            "assessment": risk_analysis
        }
        final_response = self.create_response(original_message, final_response_content)
        await self.message_bus.publish(final_response)
