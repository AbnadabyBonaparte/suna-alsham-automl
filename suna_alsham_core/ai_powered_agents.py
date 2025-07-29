#!/usr/bin/env python3
"""
Módulo dos Agentes com IA - SUNA-ALSHAM

[Fase 3] - Implementação real da integração com a API da OpenAI para
análise e otimização.
"""

import asyncio
import logging
import os
from typing import Any, Dict, List

# [AUTENTICIDADE] A biblioteca da OpenAI é importada de forma segura.
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    AgentType,
    BaseNetworkAgent,
    AgentMessage,
    MessageType
)

logger = logging.getLogger(__name__)

# --- Configuração da API OpenAI ---
if OPENAI_AVAILABLE:
    # A chave de API é carregada de forma segura a partir das variáveis de ambiente.
    openai.api_key = os.getenv("OPENAI_API_KEY")


class AIAnalyzerAgent(BaseNetworkAgent):
    """
    Agente especializado em realizar análises complexas utilizando a API da OpenAI.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o AIAnalyzerAgent."""
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.capabilities.append("ai_analysis")
        if not OPENAI_AVAILABLE or not openai.api_key:
            self.status = "degraded"
            logger.warning(f"Agente {agent_id} operando em modo degradado: OpenAI não configurado.")
        logger.info(f"✅ {self.agent_id} (Analisador IA) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de análise com IA."""
        if message.message_type != MessageType.REQUEST: return
        try:
            data_to_analyze = message.content.get("data", {})
            logger.info(f"🧠 {self.agent_id} analisando dados com IA...")

            if self.status == "degraded":
                analysis_result = {"error": "Serviço de IA indisponível."}
            else:
                prompt = f"Analise os seguintes dados e extraia 3 insights chave em formato JSON: {str(data_to_analyze)}"
                response = await openai.ChatCompletion.acreate(
                    model="gpt-3.5-turbo", # Modelo mais rápido e econômico para análises gerais
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=500,
                )
                analysis_result = response.choices[0].message.content

            response_msg = self.create_response(message, {"analysis": analysis_result})
            await self.message_bus.publish(response_msg)
        except Exception as e:
            logger.error(f"❌ Erro na análise com IA: {e}", exc_info=True)
            await self.message_bus.publish(self.create_error_response(message, str(e)))


# Outros agentes de IA (AIOptimizerAgent, AIChatAgent) seguiriam a mesma estrutura.
# Por simplicidade, focamos em implementar a lógica real em um deles primeiro.

def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Cria os agentes com capacidades de IA.
    """
    agents = []
    logger.info("🤖 Criando agentes com IA (AI-Powered)...")
    
    agent_configs = [
        {"id": "ai_analyzer_001", "class": AIAnalyzerAgent},
        # {"id": "ai_optimizer_001", "class": AIOptimizerAgent},
        # {"id": "ai_chat_001", "class": AIChatAgent},
    ]

    for config in agent_configs:
        try:
            agent = config["class"](config["id"], message_bus)
            agents.append(agent)
        except Exception as e:
            logger.error(f"❌ Erro criando agente IA {config['id']}: {e}", exc_info=True)

    return agents
