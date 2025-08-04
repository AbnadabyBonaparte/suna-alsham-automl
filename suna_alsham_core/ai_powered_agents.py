#!/usr/bin/env python3
"""
Módulo dos Agentes com IA – SUNA-ALSHAM
[Versão 2.1 - Teste de Conexão]
"""

import asyncio
import json
import logging
import os
from typing import Dict, List

try:
    from openai import AsyncOpenAI, RateLimitError, APIError, APITimeoutError
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI, RateLimitError, APIError, APITimeoutError = None, None, None, None

from suna_alsham_core.multi_agent_network import AgentMessage, AgentType, BaseNetworkAgent, MessageType

logger = logging.getLogger(__name__)

# (O SYSTEM_PROMPT continua o mesmo)
SYSTEM_PROMPT = """
Você é o "Chief Planning Officer" (CPO) do SUNA-ALSHAM, um sistema de múltiplos agentes de IA.
Sua única função é receber um objetivo de alto nível do "OrchestratorAgent" e convertê-lo em um plano de execução JSON estruturado.

REGRAS CRÍTICAS:
1.  A sua saída DEVE ser um objeto JSON válido contendo uma única chave: "plan".
2.  A chave "plan" DEVE conter uma lista de objetos, onde cada objeto representa um passo sequencial.
3.  Cada passo DEVE conter as seguintes chaves: "step" (int), "description" (str), "agent" (str), e "task" (dict).
4.  Use APENAS os agentes da lista de agentes disponíveis abaixo. Escolha o agente mais apropriado para cada tarefa.
5.  Para passar o resultado de um passo para o outro, use a sintaxe `{{output_step_N.path.to.value}}` no dicionário `task`.

AGENTES DISPONÍVEIS:
- "web_search_001": Pesquisa na web. `task` deve ter `query`. Retorna `{"result": {"details": [...]}}`.
- "content_creator_001": Cria texto. `task` deve ter `prompt_template` e `context_data`. Retorna `{"result": {"generated_text": "..."}}`.
- "notification_001": Envia e-mails. `task` deve ter `recipient_email`, `subject`, e `body`.
"""

class AIAnalyzerAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.openai_client = None
        self.status = "initializing"  # Começa em modo de inicialização
        # Inicia a tarefa de inicialização e teste de conexão em background
        self._init_task = asyncio.create_task(self._initialize_and_test_connection())
        logger.info(f"💡 {self.agent_id} (Analisador de IA) a iniciar e a testar conexão com a OpenAI...")

    async def _initialize_and_test_connection(self):
        """Testa a conexão com a OpenAI no arranque para evitar congelamentos."""
        if not OPENAI_AVAILABLE or not os.environ.get("OPENAI_API_KEY"):
            self.status = "degraded"
            logger.warning(f"💡 {self.agent_id} em modo degradado. API da OpenAI não disponível ou chave não configurada.")
            return

        try:
            # Cria o cliente com um timeout de 15 segundos
            self.openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"], timeout=15.0)
            
            # Faz uma chamada de API leve e barata para testar a conexão
            await self.openai_client.models.list()
            
            self.status = "active"
            logger.info(f"✅ [Analisador IA] Conexão com a API da OpenAI verificada com sucesso. Agente está ativo.")
        
        except APITimeoutError:
            self.status = "error"
            logger.critical("❌ [Analisador IA] FALHA CRÍTICA: Timeout ao conectar à API da OpenAI. Verifique as configurações de rede/firewall do seu container no Railway.")
        except Exception as e:
            self.status = "error"
            logger.critical(f"❌ [Analisador IA] FALHA CRÍTICA ao conectar à API da OpenAI: {e}", exc_info=True)

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type != MessageType.REQUEST: return
        if self.status != "active":
            await self.publish_error_response(message, f"Analisador de IA não está operacional. Status atual: {self.status.upper()}")
            return
        
        user_request = message.content.get("content")
        if not user_request:
            await self.publish_error_response(message, "O pedido do utilizador está vazio.")
            return
            
        logger.info(f"💡 [Analisador IA] Recebido pedido de planejamento de '{message.sender_id}': '{user_request[:50]}...'")
        try:
            plan_data = await self._create_structured_plan(user_request)
            response_content = {"status": "success", "plan": plan_data}
            await self.publish_response(message, response_content)
            logger.info(f"💡 [Analisador IA] Plano gerado e enviado com sucesso para '{message.sender_id}'.")
        except Exception as e:
            await self.publish_error_response(message, f"Erro no Analisador de IA: {e}")

    async def _create_structured_plan(self, user_prompt: str) -> List[Dict]:
        logger.info("💡 [Analisador IA] A chamar a API da OpenAI para gerar o plano...")
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
