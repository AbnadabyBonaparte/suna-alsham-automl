#!/usr/bin/env python3
"""
Módulo do Agente Orquestrador de Vendas - SUNA-ALSHAM (ALSHAM GLOBAL)

Este agente atua como o ponto central de entrada e roteador para todas as
tarefas do domínio de Vendas e Conversão, delegando requisições
para o agente especialista apropriado.
"""

import logging
import uuid
from typing import List

# Importa a classe base e os tipos essenciais do núcleo
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

# Importa todos os agentes especialistas do módulo de Vendas
from .customer_success_agent import CustomerSuccessAgent
from .payment_processing_agent import PaymentProcessingAgent
from .pricing_optimizer_agent import PricingOptimizerAgent
from .revenue_optimization_agent import RevenueOptimizationAgent
from .sales_funnel_agent import SalesFunnelAgent

logger = logging.getLogger(__name__)


class SalesOrchestratorAgent(BaseNetworkAgent):
    """
    O agente orquestrador que gerencia o fluxo de trabalho do módulo de Vendas.
    """

    def __init__(self, agent_id: str, message_bus):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend(["sales_orchestration", "task_routing"])
        
        # Mapeia requisições para os IDs dos agentes especialistas
        self.specialist_map = {
            "analyze_lead_stage": "sales_funnel_001",
            "optimize_price": "pricing_optimizer_001",
            "assess_customer_risk": "customer_success_001",
            "process_payment": "payment_processing_001",
            "find_revenue_opportunity": "revenue_optimization_001",
        }
        self.pending_delegations = {}
        logger.info(f"mgr 🧠 Agente Orquestrador de Vendas ({self.agent_id}) inicializado e pronto para delegar.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.RESPONSE:
            await self._handle_specialist_response(message)
            return
            
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            specialist_id = self.specialist_map.get(request_type)

            if specialist_id:
                await self.delegate_to_specialist(specialist_id, message)
            else:
                await self.publish_error_response(message, f"O tipo de requisição de vendas '{request_type}' não é suportado.")

    async def delegate_to_specialist(self, specialist_id: str, original_message: AgentMessage):
        delegation_id = str(uuid.uuid4())
        delegated_request = self.create_message(
            recipient_id=specialist_id,
            message_type=MessageType.REQUEST,
            content=original_message.content,
            callback_id=delegation_id
        )
        self.pending_delegations[delegation_id] = original_message
        await self.message_bus.publish(delegated_request)
        logger.info(f"Orquestrador de Vendas delegou '{original_message.content.get('request_type')}' para {specialist_id}.")

    async def _handle_specialist_response(self, response_from_specialist: AgentMessage):
        delegation_id = response_from_specialist.callback_id
        if delegation_id in self.pending_delegations:
            original_message = self.pending_delegations.pop(delegation_id)
            final_response = self.create_response(original_message, response_from_specialist.content)
            await self.message_bus.publish(final_response)
            logger.info(f"Orquestrador de Vendas encaminhou resposta final da delegação {delegation_id}.")

# Função de fábrica que o agent_loader usará
def create_sales_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria e retorna todos os agentes do módulo de Vendas."""
    logger.info("🔧 Criando agentes do domínio de Vendas & Conversão...")
    agents = [
        SalesOrchestratorAgent("sales_orchestrator_001", message_bus),
        SalesFunnelAgent("sales_funnel_001", message_bus),
        PricingOptimizerAgent("pricing_optimizer_001", message_bus),
        CustomerSuccessAgent("customer_success_001", message_bus),
        PaymentProcessingAgent("payment_processing_001", message_bus),
        RevenueOptimizationAgent("revenue_optimization_001", message_bus),
    ]
    logger.info(f"✅ {len(agents)} agentes de Vendas criados.")
    return agents
