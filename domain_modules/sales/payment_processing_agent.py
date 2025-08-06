#!/usr/bin/env python3
"""
Módulo do Agente de Processamento de Pagamentos - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida]
Este agente é um conector seguro para gateways de pagamento externos (ex: Stripe).
Ele lida com a criação de cobranças, gerenciamento de assinaturas e outras
operações financeiras, garantindo que dados sensíveis não sejam expostos.
"""

import logging
import os
from typing import Any, Dict

try:
    import stripe
    # Configura a chave de API do Stripe a partir de variáveis de ambiente
    stripe.api_key = os.environ.get("STRIPE_API_KEY")
    STRIPE_AVAILABLE = True
    if not stripe.api_key:
        logging.critical("A variável de ambiente STRIPE_API_KEY não está configurada!")
        STRIPE_AVAILABLE = False
except ImportError:
    STRIPE_AVAILABLE = False


# Importa a classe base e os tipos essenciais do núcleo do sistema
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)


class PaymentProcessingAgent(BaseNetworkAgent):
    """
    Agente especialista em interagir de forma segura com APIs de pagamento.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o PaymentProcessingAgent."""
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.BUSINESS_DOMAIN,
            message_bus=message_bus,
        )
        self.capabilities.extend([
            "charge_creation",
            "subscription_management",
            "secure_transaction_processing",
        ])
        
        if not STRIPE_AVAILABLE:
            self.status = "degraded"
            logger.critical(
                "Biblioteca 'stripe' ou a chave de API não estão disponíveis. "
                "O PaymentProcessingAgent operará em modo degradado."
            )

        logger.info(f"💳 Agente de Processamento de Pagamentos ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para realizar uma transação financeira."""
        if self.status == "degraded":
            await self.publish_error_response(message, "O serviço de pagamento está indisponível.")
            return

        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "process_payment":
            await self.handle_process_payment_request(message)

    async def handle_process_payment_request(self, message: AgentMessage) -> None:
        """
        Handles the logic for creating a charge using the payment gateway (Stripe).

        This method validates payment details, creates a charge via the Stripe API,
        logs all relevant events, and returns the transaction result. Robust error handling
        is provided for diagnostics and production reliability.

        Args:
            message (AgentMessage): The incoming message containing payment details.

        Returns:
            None
        """
        payment_details: Dict[str, Any] = message.content.get("payment_details", {})
        amount_cents: int = payment_details.get("amount_cents")  # O valor deve ser em centavos
        currency: str = payment_details.get("currency", "brl")
        token: str = payment_details.get("payment_token")  # Token seguro gerado pelo frontend
        description: str = payment_details.get("description", "Pagamento para SUNA-ALSHAM")

        if not all([amount_cents, token]):
            logger.warning("[PaymentProcessingAgent] Detalhes do pagamento incompletos (requer amount_cents e payment_token).")
            await self.publish_error_response(message, "Detalhes do pagamento incompletos (requer amount_cents e payment_token).")
            return

        logger.info(f"[PaymentProcessingAgent] Processando pagamento de {amount_cents} {currency.upper()}.")

        try:
            # Cria a cobrança na API do Stripe
            charge = stripe.Charge.create(
                amount=amount_cents,
                currency=currency,
                source=token,  # Usa o token seguro
                description=description,
            )

            logger.info(f"[PaymentProcessingAgent] Pagamento processado com sucesso. ID da transação: {charge.id}")

            # Responde com sucesso e o ID da transação
            response_content: Dict[str, Any] = {
                "status": "completed",
                "transaction_id": charge.id,
                "amount_charged": charge.amount,
                "currency": charge.currency,
                "receipt_url": charge.receipt_url,
            }
            await self.publish_response(message, response_content)

        except stripe.error.CardError as e:
            # Erro específico do cartão (ex: recusado)
            body = e.json_body
            err = body.get('error', {})
            logger.error(f"[PaymentProcessingAgent] Erro de cartão ao processar pagamento: {err.get('message')}")
            await self.publish_error_response(message, f"Erro de Cartão: {err.get('message')}")
        except stripe.error.StripeError as e:
            # Outros erros da API do Stripe
            logger.error(f"[PaymentProcessingAgent] Erro da API do Stripe: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro do Gateway de Pagamento: {e}")
        except Exception as e:
            # Erros inesperados
            logger.critical(f"[PaymentProcessingAgent] Erro inesperado no processamento de pagamento: {e}", exc_info=True)
            await self.publish_error_response(message, "Ocorreu um erro interno inesperado no serviço de pagamento.")
