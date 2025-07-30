#!/usr/bin/env python3
"""
Módulo dos Agentes com IA (AI-Powered) - SUNA-ALSHAM

[Versão Modernizada] - Atualizado para usar a biblioteca OpenAI v1.0+
e com tratamento de erros aprimorado.
"""

import asyncio
import logging
import os
import json
from typing import Any, Dict, List, Optional

# [AUTENTICIDADE] A biblioteca da OpenAI é importada de forma segura.
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Classe Principal do Agente ---

class AIAnalyzerAgent(BaseNetworkAgent):
    """
    Agente especialista em interagir com modelos de linguagem da OpenAI
    para análise de texto, geração de conteúdo e outras tarefas de IA.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o AIAnalyzerAgent."""
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.capabilities.extend(["natural_language_processing", "text_generation", "sentiment_analysis"])
        
        if not OPENAI_AVAILABLE or not os.environ.get("OPENAI_API_KEY"):
            self.status = "degraded"
            logger.critical("Biblioteca 'openai' ou a chave de API OPENAI_API_KEY não estão disponíveis.")
            self.client = None
        else:
            # --- CORREÇÃO PRINCIPAL: Usa a nova sintaxe da API ---
            self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        logger.info(f"🧠 {self.agent_id} (Analisador IA) modernizado e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de análise de IA."""
        if self.status == "degraded":
            await self.publish_error_response(message, "Serviço de IA indisponível.")
            return

        logger.info(f"🧠 {self.agent_id} analisando dados com IA...")
        
        try:
            prompt = message.content.get("text", "")
            
            # --- CORREÇÃO PRINCIPAL: Nova forma de chamar a API ---
            chat_completion = await self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-3.5-turbo",
            )
            
            result_text = chat_completion.choices[0].message.content
            
            # Tenta interpretar o resultado como JSON se for uma requisição estruturada
            if message.content.get("request_type") == "generate_structured_text":
                result = {"structured_data": json.loads(result_text)}
            else:
                # Para outras requisições, o resultado é o texto ou a intenção
                # Isso é um pouco simplista e pode ser melhorado
                intent_key = "intent" if "intent" in message.content.get("request_type", "") else "sentiment"
                result = {intent_key: result_text.strip().lower()}

            response_content = {"status": "completed", "result": result}
            await self.publish_response(message, response_content)

        except Exception as e:
            logger.error(f"❌ Erro na análise com IA: {e}", exc_info=True)
            # --- CORREÇÃO SECUNDÁRIA: Usa o nome correto da função de erro ---
            await self.publish_error_response(message, str(e))


def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria os agentes com IA."""
    agents = []
    logger.info("🤖 Criando agentes com IA (AI-Powered)...")
    try:
        agent = AIAnalyzerAgent("ai_analyzer_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro criando agente IA: {e}", exc_info=True)
    return agents
