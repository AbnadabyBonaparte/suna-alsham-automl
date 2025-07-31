#!/usr/bin/env python3
"""
Módulo dos Agentes com IA (AI-Powered) - SUNA-ALSHAM

[Versão Cérebro Triplo] - A versão mais avançada. Usa um sistema de
roteamento inteligente para escolher o melhor LLM (GPT, Gemini, Claude)
para cada tarefa, com um sistema de fallback triplo para máxima resiliência.
"""

import asyncio
import logging
import os
import json
from typing import Any, Dict, List

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
        """Inicializa o AIAnalyzerAgent com múltiplos clientes de IA."""
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.capabilities.extend(["intelligent_llm_routing", "multi_llm_fallback"])
        
        self.openai_client, self.gemini_model, self.claude_client = None, None, None

        # Configura OpenAI (GPT)
        if OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            logger.info("Cérebro 1 (OpenAI/GPT) configurado e online.")
        
        # Configura Google (Gemini)
        if GEMINI_AVAILABLE and os.environ.get("GEMINI_API_KEY"):
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            logger.info("Cérebro 2 (Google/Gemini) configurado e online.")

        # Configura Anthropic (Claude)
        if CLAUDE_AVAILABLE and os.environ.get("CLAUDE_API_KEY"):
            self.claude_client = AsyncAnthropic(api_key=os.environ.get("CLAUDE_API_KEY"))
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
            return ['gemini', 'openai', 'claude']
        elif len(prompt) > 2000 or "resuma" in prompt.lower():
            logger.info("Tarefa de texto longo ou resumo detectada. Priorizando Claude.")
            return ['claude', 'openai', 'gemini']
        else:
            logger.info("Tarefa de uso geral detectada. Priorizando OpenAI/GPT.")
            return ['openai', 'gemini', 'claude']

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa a requisição usando o roteamento inteligente e o sistema de fallback."""
        if self.status == "degraded":
            await self.publish_error_response(message, "Serviço de IA indisponível.")
            return

        provider_order = self._select_best_provider_order(message.content)
        
        for provider in provider_order:
            logger.info(f"Tentativa 1: Usando o cérebro '{provider}'...")
            success = False
            result = {}
            
            try:
                if provider == 'openai' and self.openai_client:
                    result = await self._call_openai(message.content)
                    success = True
                elif provider == 'gemini' and self.gemini_model:
                    result = await self._call_gemini(message.content)
                    success = True
                elif provider == 'claude' and self.claude_client:
                    result = await self._call_claude(message.content)
                    success = True

                if success:
                    response_content = {"status": "completed", "result": result, "source": provider.capitalize()}
                    await self.publish_response(message, response_content)
                    return # Missão cumprida!

            except Exception as e:
                logger.error(f"❌ Erro no cérebro '{provider}': {e}. Tentando o próximo cérebro...")
        
        # Se o loop terminar sem sucesso
        logger.critical("Falha em todos os provedores de IA. Missão de IA falhou.")
        await self.publish_error_response(message, "Falha em todos os provedores de IA disponíveis.")

    async def _call_openai(self, content: Dict) -> Dict:
        chat_completion = await self.openai_client.chat.completions.create(
            messages=[{"role": "user", "content": content.get("text", "")}],
            model="gpt-4", # ou "gpt-3.5-turbo"
        )
        result_text = chat_completion.choices[0].message.content
        if "generate_structured_text" in content.get("request_type", ""):
            return {"structured_data": json.loads(result_text)}
        return {"text": result_text}

    async def _call_gemini(self, content: Dict) -> Dict:
        prompt = content.get("text", "")
        if "generate_structured_text" in content.get("request_type", ""):
            config = genai.types.GenerationConfig(response_mime_type="application/json")
            response = await self.gemini_model.generate_content_async(prompt, generation_config=config)
            return {"structured_data": json.loads(response.text)}
        else:
            response = await self.gemini_model.generate_content_async(prompt)
            return {"text": response.text.strip()}

    async def _call_claude(self, content: Dict) -> Dict:
        prompt = content.get("text", "")
        is_structured = "generate_structured_text" in content.get("request_type", "")
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
            return {"structured_data": json.loads(json_str)}
        return {"text": result_text.strip()}


def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria os agentes com IA."""
    agents = []
    logger.info("🤖 Criando agentes com IA (Cérebro Triplo)...")
    try:
        agent = AIAnalyzerAgent("ai_analyzer_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro criando agente IA: {e}", exc_info=True)
    return agents
