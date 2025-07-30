#!/usr/bin/env python3
"""
Módulo dos Agentes com IA (AI-Powered) - SUNA-ALSHAM

[Versão Multi-Cérebro] - Evoluído para usar a API do Google Gemini como
cérebro principal e a API do Anthropic Claude como fallback automático,
garantindo alta resiliência e a melhor tecnologia disponível.
"""

import asyncio
import logging
import os
import json
from typing import Any, Dict, List

# --- Importa as bibliotecas dos provedores de IA ---
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from anthropic import AsyncAnthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False


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
    Agente especialista que interage com múltiplos modelos de linguagem (LLMs)
    com um sistema de fallback para garantir a continuidade da operação.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o AIAnalyzerAgent com múltiplos clientes de IA."""
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.capabilities.extend(["multi_llm_interaction", "structured_data_generation", "llm_fallback"])
        
        self.gemini_model = None
        self.claude_client = None

        # Configura o Gemini (Cérebro Principal)
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if GEMINI_AVAILABLE and gemini_api_key:
            try:
                genai.configure(api_key=gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                logger.info("Cérebro Principal (Gemini) configurado e online.")
            except Exception as e:
                 logger.error(f"Falha ao configurar Gemini: {e}")
        else:
            logger.warning("Cérebro Principal (Gemini) não disponível. Verifique a chave de API ou a biblioteca.")

        # Configura o Claude (Cérebro de Reserva)
        claude_api_key = os.environ.get("CLAUDE_API_KEY")
        if CLAUDE_AVAILABLE and claude_api_key:
            try:
                self.claude_client = AsyncAnthropic(api_key=claude_api_key)
                logger.info("Cérebro de Reserva (Claude) configurado e online.")
            except Exception as e:
                logger.error(f"Falha ao configurar Claude: {e}")
        else:
            logger.warning("Cérebro de Reserva (Claude) não disponível. Verifique a chave de API ou a biblioteca.")

        if not self.gemini_model and not self.claude_client:
            self.status = "degraded"
            logger.critical("Nenhum cérebro de IA disponível. O AIAnalyzerAgent está offline.")
        
        logger.info(f"🧠 {self.agent_id} (Analisador Multi-Cérebro) evoluído e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de análise de IA, tentando o Gemini primeiro e o Claude como fallback."""
        if self.status == "degraded":
            await self.publish_error_response(message, "Serviço de IA indisponível.")
            return

        prompt = message.content.get("text", "")
        is_structured = message.content.get("request_type") == "generate_structured_text"

        # --- TENTATIVA 1: CÉREBRO PRINCIPAL (GEMINI) ---
        if self.gemini_model:
            logger.info(f"🧠 {self.agent_id} analisando dados com o Cérebro Principal (Gemini)...")
            try:
                if is_structured:
                    generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
                    response = await self.gemini_model.generate_content_async(prompt, generation_config=generation_config)
                    result = {"structured_data": json.loads(response.text)}
                else:
                    response = await self.model.generate_content_async(prompt)
                    result_text = response.text.strip().lower()
                    intent_key = "intent" if "intent" in message.content.get("request_type", "") else "sentiment"
                    result = {intent_key: result_text}

                response_content = {"status": "completed", "result": result, "source": "Gemini"}
                await self.publish_response(message, response_content)
                return
            except Exception as e:
                logger.error(f"❌ Erro no Cérebro Principal (Gemini): {e}. Ativando fallback para o Cérebro de Reserva...")

        # --- TENTATIVA 2: CÉREBRO DE RESERVA (CLAUDE) ---
        if self.claude_client:
            logger.info(f"🧠 {self.agent_id} analisando dados com o Cérebro de Reserva (Claude)...")
            try:
                claude_prompt = f"Human: {prompt}\n\nAssistant:"
                if is_structured:
                    claude_prompt += " Por favor, responda apenas com o JSON."

                response = await self.claude_client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=2048,
                    messages=[{"role": "user", "content": claude_prompt}]
                )
                result_text = response.content[0].text
                
                if is_structured:
                    json_str = result_text[result_text.find('{'):result_text.rfind('}')+1]
                    result = {"structured_data": json.loads(json_str)}
                else:
                    result = {"text": result_text.strip()}

                response_content = {"status": "completed", "result": result, "source": "Claude"}
                await self.publish_response(message, response_content)
                return
            except Exception as e:
                logger.error(f"❌ Erro no Cérebro de Reserva (Claude): {e}. Falha total da IA.")
                await self.publish_error_response(message, f"Falha em ambos os provedores de IA: {e}")
        else:
            await self.publish_error_response(message, "Cérebro Principal falhou e não há Cérebro de Reserva disponível.")


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
