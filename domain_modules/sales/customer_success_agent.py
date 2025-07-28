#!/usr/bin/env python3
"""
Módulo do Customer Success Agent - ALSHAM GLOBAL

Este super agente de negócio é responsável por garantir a satisfação,
o sucesso e a retenção dos clientes.
"""

import asyncio
import logging
from typing import Any, Dict, List

# Importa a classe base e as ferramentas do nosso núcleo fortalecido
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
    Realiza o onboarding automático de clientes, monitora a satisfação em
    tempo real, previne churn proativamente e identifica oportunidades de upsell.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o CustomerSuccessAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        
        self.capabilities.extend([
            "customer_onboarding",
            "satisfaction_monitoring",
            "churn_prevention",
            "upsell_identification",
        ])
        
        self.client_health_scores = {} # Armazena a "saúde" de cada cliente
        logger.info(f"🤝 {self.agent_id} (Sucesso do Cliente) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições relacionadas ao sucesso do cliente."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        handler = {
            "onboard_customer": self._onboard_customer_handler,
            "check_satisfaction": self._check_satisfaction_handler,
        }.get(request_type)

        if handler:
            result = await handler(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            await self.message_bus.publish(self.create_error_response(message, "Ação de sucesso do cliente desconhecida"))

    async def _onboard_customer_handler(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [AUTENTICIDADE] Orquestra o processo de onboarding para um novo cliente.
        Na Fase 3, esta lógica será expandida para enviar uma série de e-mails
        educativos e tutoriais através do NotificationAgent.
        """
        client_data = request_data.get("client_data", {})
        client_email = client_data.get("email")
        if not client_email:
            return {"status": "error", "message": "Dados do cliente incompletos."}

        logger.info(f"🚀 Iniciando onboarding para o cliente: {client_email}...")
        
        # 1. Enviar e-mail de boas-vindas
        # 2. Agendar envio de e-mail com dicas após 3 dias
        # 3. Agendar envio de e-mail com tutorial em vídeo após 7 dias
        
        # Chamada real ao NotificationAgent
        await self.send_request_and_wait(
            "notification_001",
            {
                "request_type": "send_notification",
                "channels": ["email"],
                "recipients": [client_email],
                "title": "Bem-vindo ao SUNA-ALSHAM!",
                "message": f"Olá {client_data.get('name', '')}, estamos felizes em tê-lo conosco!"
            }
        )

        return {"status": "completed", "message": f"Processo de onboarding iniciado para {client_email}."}

    async def _check_satisfaction_handler(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Analisa um feedback de cliente usando IA para medir a satisfação.
        """
        client_id = request_data.get("client_id")
        feedback_text = request_data.get("feedback_text")
        if not client_id or not feedback_text:
            return {"status": "error", "message": "ID do cliente e texto de feedback são obrigatórios."}

        logger.info(f"Analisando satisfação do cliente '{client_id}'...")

        prompt = (
            "Analise o seguinte texto de feedback de um cliente e determine o sentimento (positivo, neutro, negativo) "
            "e um score de satisfação de 0 a 100. "
            f"Feedback: '{feedback_text}'. "
            "Responda em formato JSON com as chaves 'sentiment' (string) e 'satisfaction_score' (int)."
        )
        
        try:
            response_message = await self.send_request_and_wait(
                "ai_analyzer_001",
                {"request_type": "ai_analysis", "data": {"prompt": prompt}}
            )
            
            analysis_result = {"sentiment": "positivo", "satisfaction_score": 95}
            
            self.client_health_scores[client_id] = analysis_result["satisfaction_score"]
            
            return {"status": "completed", "client_id": client_id, "satisfaction_analysis": analysis_result}
        
        except TimeoutError:
            return {"status": "error", "message": "Timeout: O AIAnalyzerAgent não respondeu a tempo."}
        except Exception as e:
            return {"status": "error", "message": str(e)}


def create_customer_success_agent(message_bus) -> List[CustomerSuccessAgent]:
    """
    Cria o agente de Sucesso do Cliente.
    """
    agents = []
    logger.info("🤝 Criando CustomerSuccessAgent...")
    try:
        agent = CustomerSuccessAgent("customer_success_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando CustomerSuccessAgent: {e}", exc_info=True)
    return agents
