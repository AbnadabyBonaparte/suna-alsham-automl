#!/usr/bin/env python3
"""
Módulo dos Agentes com IA – SUNA-ALSHAM
Versão Viva – Usa exclusivamente OpenAI e retorna JSON robusto.
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

from suna_alsham_core.multi_agent_network import AgentMessage, AgentType, BaseNetworkAgent, MessageType

logger = logging.getLogger(__name__)

class AIAnalyzerAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        if OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        else:
            self.status = "degraded"
        logger.info(f"🧠 {self.agent_id} inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type != MessageType.REQUEST:
            return
        prompt = message.content.get("text", "")
        if not prompt:
            await self.publish_error_response(message, "Prompt vazio.")
            return
        try:
            result = await self._call_openai(prompt)
            await self.publish_response(message, {"status": "completed", "result": result})
        except Exception as e:
            await self.publish_error_response(message, f"Erro OpenAI: {e}")

    async def _call_openai(self, prompt: str) -> Dict:
        chat_completion = await self.openai_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4.1-mini"
        )
        result_text = chat_completion.choices[0].message.content
        try:
            return {"structured_data": json.loads(result_text)}
        except:
            return {"text": result_text}

def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    return [AIAnalyzerAgent("ai_analyzer_001", message_bus)]
