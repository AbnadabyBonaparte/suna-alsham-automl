#!/usr/bin/env python3
"""
Módulo dos Agentes com IA (AI-Powered) – SUNA-ALSHAM

[Versão Defensiva] – Valida entradas para evitar loops de fallback e
ajusta chamadas aos provedores para lidar com mudanças de API e parsing.
"""

import asyncio
import json
import logging
import os
from typing import Dict, List

# --- Importa as bibliotecas dos três provedores de IA ---
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

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

class AIAnalyzerAgent(BaseNetworkAgent):
    """
    Agente especialista que atua como um roteador de IA inteligente,
    selecionando o melhor LLM para a tarefa e usando um sistema de fallback.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.capabilities.extend(["intelligent_llm_routing", "multi_llm_fallback"])
        self.openai_client = None
        self.gemini_model = None
        self.claude_client = None

        # Configura OpenAI (GPT)
        if OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
            logger.info("Cérebro 1 (OpenAI/GPT) configurado e online.")

        # Configura Google (Gemini) — modelo pode não existir na versão usada
        if GEMINI_AVAILABLE and os.environ.get("GEMINI_API_KEY"):
            genai.configure(api_key=os.environ["GEMINI_API_KEY"])
            try:
                self.gemini_model = genai.GenerativeModel("gemini-pro")
                logger.info("Cérebro 2 (Google/Gemini) configurado e online.")
            except Exception as e:
                logger.error(f"Falha ao inicializar o modelo Gemini: {e}. Desativando este provedor.")
                self.gemini_model = None

        # Configura Anthropic (Claude)
        if CLAUDE_AVAILABLE and os.environ.get("CLAUDE_API_KEY"):
            self.claude_client = AsyncAnthropic(api_key=os.environ["CLAUDE_API_KEY"])
            logger.info("Cérebro 3 (Anthropic/Claude) configurado e online.")

        if not any([self.openai_client, self.gemini_model, self.claude_client]):
            self.status = "degraded"
            logger.critical("Nenhum cérebro de IA disponível. O AIAnalyzerAgent está offline.")

        logger.info(f"🧠 {self.agent_id} (Analisador Cérebro Triplo) evoluído e inicializado.")

    def _select_best_provider_order(self, request_content: Dict) -> List[str]:
        """Analisa a requisição e retorna a ordem de preferência dos cérebros."""
        request_type = request_content.get("request_type", "")
        prompt = request_content.get("text", "")

        if "generate_structured_text" in request_type:
            logger.info("Tarefa de dados estruturados detectada. Priorizando Gemini.")
            return ["gemini", "openai", "claude"]
        elif len(prompt) > 2000 or "resuma" in prompt.lower():
            logger.info("Tarefa de texto longo ou resumo detectada. Priorizando Claude.")
            return ["claude", "openai", "gemini"]
        else:
            logger.info("Tarefa de uso geral detectada. Priorizando OpenAI/GPT.")
            return ["openai", "gemini", "claude"]

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa a requisição usando o roteamento inteligente e o sistema de fallback."""
        # Ignora mensagens que não são requisições de trabalho
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

        provider_order = self._select_best_provider_order(message.content)
        last_error = None
        for i, provider in enumerate(provider_order):
            logger.info(f"Tentativa {i+1}/{len(provider_order)}: Usando o cérebro '{provider}'...")
            try:
                if provider == "openai" and self.openai_client:
                    result = await self._call_openai(message.content)
                elif provider == "gemini" and self.gemini_model:
                    result = await self._call_gemini(message.content)
                elif provider == "claude" and self.claude_client:
                    result = await self._call_claude(message.content)
                else:
                    continue

                response_content = {
                    "status": "completed",
                    "result": result,
                    "source": provider.capitalize(),
                }
                await self.publish_response(message, response_content)
                return  # Missão cumprida!
            except Exception as e:
                last_error = e
                logger.error(f"❌ Erro no cérebro '{provider}': {e}. Tentando o próximo cérebro...")

        logger.critical(f"Falha em todos os provedores de IA. Último erro: {last_error}")
        await self.publish_error_response(
            message,
            f"Falha em todos os provedores de IA disponíveis. Último erro: {last_error}",
        )

    async def _call_openai(self, content: Dict) -> Dict:
        """Chama a API da OpenAI e faz parsing robusto de JSON quando necessário."""
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
                try:
                    json_str = result_text[result_text.find("{") : result_text.rfind("}") + 1]
                    return {"structured_data": json.loads(json_str)}
                except json.JSONDecodeError:
                    # falhou novamente, retorna como texto simples
                    return {"text": result_text}
        return {"text": result_text}

    async def _call_gemini(self, content: Dict) -> Dict:
        """Chama a API Gemini sem usar parâmetros obsoletos."""
        prompt = content.get("text", "")
        if not prompt:
            raise ValueError("Prompt para Gemini não pode ser vazio.")

        response = await self.gemini_model.generate_content_async(prompt)
        if "generate_structured_text" in content.get("request_type", ""):
            return {"structured_data": json.loads(response.text)}
        else:
            return {"text": response.text.strip()}

    async def _call_claude(self, content: Dict) -> Dict:
        """Chama a API da Anthropic; requer créditos válidos na conta."""
        prompt = content.get("text", "")
        if not prompt:
            raise ValueError("Prompt para Claude não pode ser vazio.")

        is_structured = "generate_structured_text" in content.get("request_type", "")
        claude_prompt = f"Human: {prompt}\n\nAssistant:"
        if is_structured:
            claude_prompt += " Por favor, responda apenas com o JSON."

        response = await self.claude_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2048,
            messages=[{"role": "user", "content": claude_prompt}],
        )
        result_text = response.content[0].text
        if is_structured:
            json_str = result_text[result_text.find("{") : result_text.rfind("}") + 1]
            return {"structured_data": json.loads(json_str)}
        return {"text": result_text.strip()}

def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria os agentes com IA."""
    agents: List[BaseNetworkAgent] = []
    logger.info("🤖 Criando agentes com IA (Cérebro Triplo)...")
    try:
        agent = AIAnalyzerAgent("ai_analyzer_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro criando agente IA: {e}", exc_info=True)
    return agents
