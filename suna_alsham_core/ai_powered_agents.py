#!/usr/bin/env python3
"""
Módulo dos Agentes com IA – SUNA-ALSHAM
[Versão 2.0 - Passagem de Contexto]
"""

import json
import logging
import os
from typing import Dict, List

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI = None

from suna_alsham_core.multi_agent_network import AgentMessage, AgentType, BaseNetworkAgent

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Você é o "Chief Planning Officer" (CPO) do SUNA-ALSHAM. Sua função é converter um objetivo em um plano JSON.

REGRAS CRÍTICAS:
1. A sua saída DEVE ser um objeto JSON com uma chave: "plan".
2. Cada passo no plano DEVE ter: "step", "description", "agent", e "task".
3. Para passar o resultado de um passo para o outro, use a sintaxe `{{output_step_N}}` no dicionário `task`. O sistema irá substituir isto pelo resultado real do passo N.

AGENTES DISPONÍVEIS:
- "web_search_001": Pesquisa na web. `task` deve ter `query`. Retorna `{"details": [...]}`.
- "content_creator_001": Cria texto. `task` deve ter `prompt_template` e `context_data`. Retorna `{"generated_text": "..."}`.
- "notification_001": Envia e-mails. `task` deve ter `recipient_email`, `subject`, e `body`.

Exemplo de Objetivo: "Pesquise sobre o Gemini da Google e envie um resumo por e-mail para test@example.com."

Sua saída JSON para este objetivo seria:
{
  "plan": [
    {
      "step": 1,
      "description": "Pesquisar informações sobre o Google Gemini.",
      "agent": "web_search_001",
      "task": { "query": "Google Gemini AI" }
    },
    {
      "step": 2,
      "description": "Criar um resumo conciso com base nos resultados da pesquisa.",
      "agent": "content_creator_001",
      "task": {
        "prompt_template": "Crie um resumo de um parágrafo sobre o Google Gemini.",
        "context_data": "{{output_step_1.result}}"
      }
    },
    {
      "step": 3,
      "description": "Enviar o resumo por e-mail.",
      "agent": "notification_001",
      "task": {
        "recipient_email": "test@example.com",
        "subject": "Resumo sobre o Google Gemini",
        "body": "{{output_step_2.result.generated_text}}"
      }
    }
  ]
}
"""

class AIAnalyzerAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.openai_client = None
        if OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
            logger.info(f"💡 {self.agent_id} (Analisador de IA) V2.0 pronto para criar planos com contexto.")
        else:
            self.status = "degraded"

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type != "REQUEST" or self.status == "degraded": return
        user_request = message.content.get("content")
        if not user_request: return
        try:
            plan_data = await self._create_structured_plan(user_request)
            response_content = {"status": "success", "plan": plan_data}
            await self.publish_response(message, response_content)
        except Exception as e:
            await self.publish_error_response(message, f"Erro no Analisador de IA: {e}")

    async def _create_structured_plan(self, user_prompt: str) -> List[Dict]:
        chat_completion = await self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        structured_response = json.loads(chat_completion.choices[0].message.content)
        if "plan" not in structured_response: raise ValueError("A resposta da IA não continha uma chave 'plan'.")
        return structured_response["plan"]

def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    return [AIAnalyzerAgent("ai_analyzer_001", message_bus)]
