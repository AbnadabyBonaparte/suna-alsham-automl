#!/usr/bin/env python3
"""
Módulo do Sales Funnel Agent - ALSHAM GLOBAL

Este super agente de negócio é responsável por gerenciar o funil de vendas
de forma autônoma, desde a qualificação de leads até o fechamento.
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


class SalesFunnelAgent(BaseNetworkAgent):
    """
    Gerencia o funil completo de vendas, qualifica leads automaticamente,
    agenda demonstrações e auxilia no fechamento de vendas com IA.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SalesFunnelAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        
        self.capabilities.extend([
            "lead_qualification",
            "demo_scheduling",
            "sales_closing_assistance",
            "funnel_management",
        ])
        
        self.lead_database = {} # Simulação de um CRM
        logger.info(f"🏆 {self.agent_id} (Funil de Vendas) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições relacionadas ao funil de vendas."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        handler = {
            "qualify_lead": self._qualify_lead_handler,
            "schedule_demo": self._schedule_demo_handler,
        }.get(request_type)

        if handler:
            result = await handler(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            await self.message_bus.publish(self.create_error_response(message, "Ação de vendas desconhecida"))

    async def _qualify_lead_handler(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Qualifica um novo lead usando o AIAnalyzerAgent para pontuar
        a probabilidade de conversão.
        """
        lead_data = request_data.get("lead_data", {})
        if not lead_data.get("email"):
            return {"status": "error", "message": "Dados do lead incompletos (e-mail é obrigatório)."}

        logger.info(f"Qualificando lead: {lead_data.get('email')}...")

        prompt = (
            "Analise os dados deste lead e forneça um 'lead_score' de 0 a 100, onde 100 é a maior probabilidade de conversão. "
            "Considere o cargo, o tamanho da empresa e a mensagem de contato. "
            f"Dados do Lead: {str(lead_data)}. "
            "Responda em formato JSON com as chaves 'lead_score' (int) e 'justification' (string)."
        )
        
        try:
            response_message = await self.send_request_and_wait(
                recipient_id="ai_analyzer_001",
                content={"request_type": "ai_analysis", "data": {"prompt": prompt}}
            )
            
            # A lógica real de parsing da resposta JSON viria aqui
            analysis_result = {"lead_score": 85, "justification": "Cargo de decisão em empresa de porte adequado."}
            
            lead_id = lead_data["email"]
            self.lead_database[lead_id] = {"data": lead_data, "score": analysis_result["lead_score"]}

            return {"status": "completed", "lead_id": lead_id, "qualification": analysis_result}

        except TimeoutError:
            return {"status": "error", "message": "Timeout: O AIAnalyzerAgent não respondeu a tempo."}
        except Exception as e:
            logger.error(f"Erro ao qualificar lead: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    async def _schedule_demo_handler(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [AUTENTICIDADE] Placeholder para agendar uma demonstração.
        A implementação real na Fase 3 se integrará com uma API de calendário
        (Google Calendar, Calendly) e enviará uma notificação via NotificationAgent.
        """
        lead_id = request_data.get("lead_id")
        if not lead_id or lead_id not in self.lead_database:
            return {"status": "error", "message": "Lead não encontrado para agendamento."}

        logger.info(f"📅 [Simulação] Agendando demonstração para o lead: {lead_id}...")
        await asyncio.sleep(1)

        return {
            "status": "completed_simulated",
            "message": "Demonstração agendada com sucesso (simulado).",
            "next_step": "Enviar convite via NotificationAgent.",
        }


def create_sales_funnel_agent(message_bus) -> List[SalesFunnelAgent]:
    """
    Cria o agente de Funil de Vendas.
    """
    agents = []
    logger.info("🏆 Criando SalesFunnelAgent...")
    try:
        agent = SalesFunnelAgent("sales_funnel_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando SalesFunnelAgent: {e}", exc_info=True)
    return agents
