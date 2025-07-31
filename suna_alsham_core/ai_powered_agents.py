#!/usr/bin/env python3
"""
Módulo dos Agentes com IA (AI-Powered) - SUNA-ALSHAM

[Versão Defensiva] - Adiciona validação de robustez na entrada para
recusar requisições malformadas imediatamente, evitando loops de fallback.
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
        # ... (código existente) ...
        pass

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa a requisição usando o roteamento inteligente e o sistema de fallback."""
        
        # --- VALIDAÇÃO DEFENSIVA ADICIONADA AQUI ---
        req_type = message.content.get("request_type")
        prompt = message.content.get("text")
        if not req_type:
            await self.publish_error_response(
                message,
                "Tipo de requisição ('request_type') ausente ou nulo ao acionar o AIAnalyzerAgent."
            )
            return
        if not prompt:
            await self.publish_error_response(
                message,
                "Campo 'text' ausente ou vazio ao acionar o AIAnalyzerAgent."
            )
            return
        # --- FIM DA VALIDAÇÃO ---

        if self.status == "degraded":
            await self.publish_error_response(message, "Serviço de IA indisponível.")
            return

        provider_order = self._select_best_provider_order(message.content)
        
        last_error = None
        for i, provider in enumerate(provider_order):
            logger.info(f"Tentativa {i+1}/{len(provider_order)}: Usando o cérebro '{provider}'...")
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
                last_error = e
                logger.error(f"❌ Erro no cérebro '{provider}': {e}. Tentando o próximo cérebro...")
        
        logger.critical(f"Falha em todos os provedores de IA. Último erro: {last_error}")
        await self.publish_error_response(message, f"Falha em todos os provedores de IA disponíveis. Último erro: {last_error}")

    # ... (resto do código, como _call_openai, _call_gemini, etc., permanece o mesmo) ...

def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    # ... (código existente) ...
    pass
