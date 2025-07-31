#!/usr/bin/env python3
"""
Módulo dos Agentes com IA (AI-Powered) – SUNA-ALSHAM

[Versão simplificada] – Utiliza apenas a API da OpenAI para atender às requisições.
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
    Priority,
)

logger = logging.getLogger(__name__)

class AIAnalyzerAgent(BaseNetworkAgent):
    """
    Agente especialista que utiliza apenas o provedor OpenAI.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.capabilities.extend(["intelligent_llm_routing"])
        self.openai_client = None

        if OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
            logger.info("Cérebro (OpenAI/GPT) configurado e online.")
        else:
            self.status = "degraded"
            logger.critical("OpenAI não está disponível. O AIAnalyzerAgent está offline.")

        logger.info(f"🧠 {self.agent_id} (Analisador IA) inicializado.")

    def _select_best_provider_order(self, request_content: Dict) -> List[str]:
        # Sempre usa apenas o OpenAI
        return ["openai"]

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type != MessageType.REQUEST:
            return

        req_type = message.content.get("request_type")
        prompt = message.content.get("text")
        if not req_type:
            await self.publish_error_response(
                message,
                "Tipo de requisição ('request_type') ausente ou nulo ao acionar o AIAnalyzerAgent.",
            )
            return
        if not prompt:
            await self.publish_error_response(
                message,
                "Campo 'text' ausente ou vazio ao acionar o AIAnalyzerAgent.",
            )
            return

        if self.status == "degraded":
            await self.publish_error_response(message, "Serviço de IA indisponível.")
            return

        # Tenta somente o OpenAI
        try:
            result = await self._call_openai(message.content)
            response_content = {
                "status": "completed",
                "result": result,
                "source": "OpenAI",
            }
            await self.publish_response(message, response_content)
        except Exception as e:
            logger.error(f"❌ Erro no provedor OpenAI: {e}")
            await self.publish_error_response(
                message,
                f"Falha no provedor OpenAI: {e}",
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
                # Tenta recortar o JSON, caso o modelo envie texto extra
                try:
                    json_str = result_text[result_text.find("{") : result_text.rfind("}") + 1]
                    return {"structured_data": json.loads(json_str)}
                except json.JSONDecodeError:
                    # Se não conseguir interpretar como JSON, devolve como texto simples
                    return {"text": result_text}
        return {"text": result_text}

def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de IA usando apenas OpenAI."""
    agents: List[BaseNetworkAgent] = []
    logger.info("🤖 Criando agente de IA (somente OpenAI)...")
    try:
        agent = AIAnalyzerAgent("ai_analyzer_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro criando AIAnalyzerAgent: {e}", exc_info=True)
    return agents
