#!/usr/bin/env python3
"""
Módulo dos Agentes com IA (AI-Powered) – SUNA-ALSHAM

[Versão Final Limpa] – Utiliza exclusivamente a API da OpenAI.
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
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.capabilities.extend(["intelligent_llm_routing"])

        if OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
            logger.info("Cérebro (OpenAI/GPT) configurado e online.")
        else:
            self.openai_client = None
            self.status = "degraded"
            logger.critical("OpenAI não está disponível. O AIAnalyzerAgent está offline.")

        logger.info(f"🧠 {self.agent_id} (Analisador IA) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type != MessageType.REQUEST:
            return

        req_type = message.content.get("request_type")
        prompt = message.content.get("text")
        if not req_type or not prompt:
            await self.publish_error_response(
                message,
                "Requisição inválida: 'request_type' ou 'text' ausente.",
            )
            return

        if self.status == "degraded":
            await self.publish_error_response(message, "Serviço de IA indisponível.")
            return

        try:
            result = await self._call_openai(message.content)
            await self.publish_response(
                message, {"status": "completed", "result": result, "source": "OpenAI"}
            )
        except Exception as e:
            logger.error(f"❌ Erro no provedor OpenAI: {e}")
            await self.publish_error_response(
                message, f"Falha no provedor OpenAI: {e}"
            )

    async def _call_openai(self, content: Dict) -> Dict:
        prompt = content.get("text", "")
        if not prompt:
            raise ValueError("Prompt para OpenAI não pode ser vazio.")

        chat_completion = await self.openai_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4.1-mini",
        )
        result_text = chat_completion.choices[0].message.content

        if "generate_structured_text" in content.get("request_type", ""):
            try:
                return {"structured_data": json.loads(result_text)}
            except json.JSONDecodeError:
                json_str = result_text[result_text.find("{") : result_text.rfind("}") + 1]
                try:
                    return {"structured_data": json.loads(json_str)}
                except json.JSONDecodeError:
                    return {"text": result_text}

        return {"text": result_text}

def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    agents: List[BaseNetworkAgent] = []
    logger.info("🤖 Criando agente de IA (somente OpenAI)...")
    try:
        agent = AIAnalyzerAgent("ai_analyzer_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro criando AIAnalyzerAgent: {e}", exc_info=True)
    return agents
