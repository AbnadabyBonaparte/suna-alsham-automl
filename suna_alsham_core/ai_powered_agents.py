#!/usr/bin/env python3
"""
Módulo dos Agentes com IA (AI-Powered) – SUNA-ALSHAM

Versão Viva – Tradutor Universal. Entende qualquer texto e converte em JSON de missão.
"""

import asyncio
import json
import logging
import os
from typing import Dict, List

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
)

logger = logging.getLogger(__name__)

class AIAnalyzerAgent(BaseNetworkAgent):
    """
    Tradutor Universal – Transforma texto em planos estruturados.
    Usa exclusivamente OpenAI.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.capabilities.extend(["intent_extraction", "universal_translation"])

        if OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
            logger.info("Cérebro (OpenAI) configurado e online.")
        else:
            self.openai_client = None
            self.status = "degraded"
            logger.critical("OpenAI não disponível. AIAnalyzerAgent em modo degradado.")

        logger.info(f"🧠 {self.agent_id} (Tradutor Universal) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type != MessageType.REQUEST:
            return

        req_type = message.content.get("request_type")
        prompt = message.content.get("text") or json.dumps(message.content)
        if not prompt:
            await self.publish_error_response(message, "Requisição sem conteúdo válido.")
            return

        if self.status == "degraded":
            await self.publish_error_response(message, "Serviço de IA indisponível.")
            return

        try:
            result = await self._call_openai(req_type, prompt)
            await self.publish_response(message, {
                "status": "completed",
                "result": result,
                "source": "OpenAI"
            })
        except Exception as e:
            logger.error(f"❌ Erro OpenAI: {e}")
            await self.publish_error_response(message, f"Falha no OpenAI: {e}")

    async def _call_openai(self, req_type: str, prompt: str) -> Dict:
        """
        Se for um pedido de missão, converte texto para JSON de missão.
        Caso contrário, responde texto livre.
        """
        model_to_use = "gpt-4.1-mini"

        chat_completion = await self.openai_client.chat.completions.create(
            model=model_to_use,
            messages=[{"role": "user", "content": prompt}]
        )
        result_text = chat_completion.choices[0].message.content

        # 🔥 Se a requisição for de geração estruturada, tenta extrair JSON
        if "generate_structured_text" in (req_type or "") or "execute_complex_task" in (req_type or ""):
            try:
                return {"structured_data": json.loads(result_text)}
            except json.JSONDecodeError:
                # Tenta limpar o JSON
                json_str = result_text[result_text.find("{"):result_text.rfind("}") + 1]
                try:
                    return {"structured_data": json.loads(json_str)}
                except json.JSONDecodeError:
                    # Se não for JSON, devolve texto puro
                    return {"text": result_text}

        return {"text": result_text}

def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    agents: List[BaseNetworkAgent] = []
    logger.info("🤖 Criando AIAnalyzerAgent (Tradutor Universal)...")
    try:
        agent = AIAnalyzerAgent("ai_analyzer_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro criando AIAnalyzerAgent: {e}", exc_info=True)
    return agents
