#!/usr/bin/env python3
"""
Módulo do Agente Analisador de Satisfação - SUNA-ALSHAM (ALSHAM GLOBAL)

[Versão Fortalecida] - Integra-se com o AIPoweredAgent para realizar
análise de sentimento real e calcular um score de satisfação.
"""

import logging
import uuid
from typing import Any, Dict, List

from suna_alsham_core.multi_agent_network import (
    AgentMessage, 
    AgentType,
    BaseNetworkAgent, 
    MessageType, 
    Priority
)

logger = logging.getLogger(__name__)


class SatisfactionAnalyzerAgent(BaseNetworkAgent):
    """
    Agente especialista em análise de sentimento e satisfação do cliente.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SatisfactionAnalyzerAgent."""
        super().__init__(agent_id, AgentType.BUSINESS_DOMAIN, message_bus)
        self.capabilities.extend([
            "sentiment_analysis",
            "customer_satisfaction_scoring",
            "emotion_detection"
        ])
        self.pending_analyses = {}
        logger.info(f"😊 Agente Analisador de Satisfação ({self.agent_id}) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Processa uma requisição para analisar um texto ou uma resposta da IA.
        """
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "analyze_satisfaction":
            await self.handle_analysis_request(message)
        
        elif message.message_type == MessageType.RESPONSE:
            await self.handle_ai_response(message)

    async def handle_analysis_request(self, original_message: AgentMessage):
        """Recebe um texto e delega a análise de sentimento para a IA."""
        text_to_analyze = original_message.content.get("text", "")
        if not text_to_analyze:
            await self.publish_error_response(original_message, "Nenhum texto fornecido para análise.")
            return

        analysis_id = str(uuid.uuid4())
        logger.info(f"Nova análise [ID: {analysis_id}]. Analisando sentimento do texto: '{text_to_analyze[:50]}...'")

        self.pending_analyses[analysis_id] = {
            "original_message": original_message
        }

        prompt = f"""
        Analise o sentimento do texto a seguir. O sentimento é 'positive',
        'negative' ou 'neutral'? Responda apenas com a palavra.
        Texto: "{text_to_analyze}"
        """

        request_to_ai = self.create_message(
            recipient_id="ai_analyzer_001",
            message_type=MessageType.REQUEST,
            content={"request_type": "analyze_sentiment", "text": prompt},
            callback_id=analysis_id
        )
        await self.message_bus.publish(request_to_ai)

    async def handle_ai_response(self, response_message: AgentMessage):
        """Recebe a análise da IA e calcula o score de satisfação."""
        analysis_id = response_message.callback_id
        if not analysis_id or analysis_id not in self.pending_analyses:
            return

        conversation = self.pending_analyses.pop(analysis_id)
        original_message = conversation["original_message"]

        sentiment = response_message.content.get("result", {}).get("sentiment", "neutral").lower()

        # Converte o sentimento em um score numérico (simples)
        if sentiment == "positive":
            csat_score = 0.95
        elif sentiment == "negative":
            csat_score = 0.15
        else:
            csat_score = 0.60
            
        logger.info(f"Análise [ID: {analysis_id}] concluída. Sentimento: {sentiment}, Score: {csat_score}")

        final_response = {
            "status": "completed",
            "sentiment": sentiment,
            "csat_score": csat_score
        }
        await self.publish_response(original_message, final_response)
