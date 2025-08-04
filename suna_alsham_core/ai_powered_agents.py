#!/usr/bin/env python3
"""
Módulo dos Agentes com IA – SUNA-ALSHAM
Versão Viva – Usa exclusivamente OpenAI e retorna JSON robusto e estruturado.
"""

import asyncio
import json
import logging
import os
from typing import Dict, List

try:
    from openai import AsyncOpenAI, RateLimitError, APIError
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI, RateLimitError, APIError = None, None, None

from suna_alsham_core.multi_agent_network import AgentMessage, AgentType, BaseNetworkAgent, MessageType

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Você é o "Chief Planning Officer" (CPO) do SUNA-ALSHAM, um sistema de múltiplos agentes de IA.
Sua única função é receber um objetivo de alto nível do "OrchestratorAgent" e convertê-lo em um plano de execução JSON estruturado.

REGRAS CRÍTICAS:
1.  A sua saída DEVE ser um objeto JSON válido contendo uma única chave: "plan".
2.  A chave "plan" DEVE conter uma lista de objetos, onde cada objeto representa um passo sequencial.
3.  Cada passo DEVE conter as seguintes chaves: "step" (int), "description" (str), "agent" (str), e "task" (dict).
4.  Use APENAS os agentes da lista de agentes disponíveis abaixo. Escolha o agente mais apropriado para cada tarefa.

AGENTES DISPONÍVEIS E SUAS FUNÇÕES:
- "web_search_001": Pesquisa na internet. 'task' deve ter uma chave 'query'.
- "content_creator_001": Cria conteúdo de texto. 'task' deve ter 'topic', 'format', etc.
- "social_media_orchestrator_001": Gerencia redes sociais (agendar, postar). 'task' deve ter 'action'.
- "sales_orchestrator_001": Gerencia funis de venda e otimização. 'task' deve ter 'action'.
- "analytics_orchestrator_001": Coleta e analisa dados. 'task' deve ter 'action'.
- "support_orchestrator_001": Gerencia tickets de suporte. 'task' deve ter 'action'.
- "code_analyzer_001": Analisa código fonte. 'task' deve ter 'code_path' ou 'code_string'.
- "database_001": Executa queries em base de dados. 'task' deve ter 'query'.
"""

class AIAnalyzerAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.openai_client = None
        if OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
            try:
                self.openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
                self.status = "active"
                logger.info(f"💡 {self.agent_id} (Analisador de IA) inicializado com a API da OpenAI.")
            except Exception as e:
                self.status = "error"
                logger.critical(f"Falha ao inicializar o cliente OpenAI: {e}")
        else:
            self.status = "degraded"
            logger.warning(f"💡 {self.agent_id} inicializado em modo degradado. API da OpenAI não disponível ou chave não configurada.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type != MessageType.REQUEST or self.status != "active":
            if self.status != "active":
                await self.publish_error_response(message, "Analisador de IA não está operacional.")
            return
        
        user_request = message.content.get("user_request", {}).get("content")
        if not user_request:
            await self.publish_error_response(message, "O pedido do utilizador está vazio.")
            return
            
        logger.info(f"💡 [Analisador IA] Recebido pedido de planejamento de '{message.sender_id}': '{user_request[:50]}...'")

        try:
            plan_data = await self._create_structured_plan(user_request)
            response_content = {"status": "success", "plan": plan_data}
            await self.publish_response(message, response_content)
            logger.info(f"💡 [Analisador IA] Plano gerado e enviado com sucesso para '{message.sender_id}'.")

        except (RateLimitError, APIError) as e:
            logger.error(f"Erro na API OpenAI: {e}")
            await self.publish_error_response(message, f"Erro na comunicação com a API OpenAI: {type(e).__name__}")
        except Exception as e:
            logger.error(f"Erro inesperado ao gerar plano: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro interno no Analisador de IA: {e}")

    async def _create_structured_plan(self, user_prompt: str) -> List[Dict]:
        logger.info("💡 [Analisador IA] A chamar a API da OpenAI para gerar o plano...")
        chat_completion = await self.openai_client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        result_text = chat_completion.choices[0].message.content
        structured_response = json.loads(result_text)
        
        if "plan" not in structured_response or not isinstance(structured_response["plan"], list):
            raise ValueError("A resposta da IA não continha uma chave 'plan' válida do tipo lista.")

        return structured_response["plan"]

def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    return [AIAnalyzerAgent("ai_analyzer_001", message_bus)]
