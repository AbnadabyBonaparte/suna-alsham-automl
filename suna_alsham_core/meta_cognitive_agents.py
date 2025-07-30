#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos - O Cérebro do SUNA-ALSHAM.

[Versão Fortalecida] - O OrchestratorAgent agora pode executar missões
complexas de múltiplos passos, orquestrando a colaboração entre agentes.
"""

import asyncio
import logging
import uuid
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Classes Principais dos Agentes ---

class OrchestratorAgent(BaseNetworkAgent):
    """
    Agente Orquestrador Supremo. Executa planos de ação complexos que
    envolvem a colaboração de múltiplos agentes de diferentes domínios.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o OrchestratorAgent."""
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.capabilities.extend(["complex_task_orchestration", "workflow_management"])
        self.pending_missions: Dict[str, Dict] = {}
        logger.info(f"👑 {self.agent_id} (Orquestrador Supremo) fortalecido e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa novas missões ou respostas de agentes delegados."""
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "execute_complex_task":
            await self.start_mission(message)
        
        elif message.message_type == MessageType.RESPONSE:
            await self.continue_mission(message)

    async def start_mission(self, original_message: AgentMessage):
        """Passo 1: Inicia uma nova missão e delega a primeira tarefa (pesquisa)."""
        mission_id = str(uuid.uuid4())
        goal = original_message.content.get("goal", {})
        
        logger.info(f"Nova missão [ID: {mission_id}] recebida: {goal.get('description')}")

        # Armazena o estado da missão
        self.pending_missions[mission_id] = {
            "original_message": original_message,
            "state": "awaiting_bio_search",
            "goal": goal,
            "collected_data": {} # Para guardar os resultados de cada passo
        }

        # Delega a primeira subtarefa: pesquisar a biografia
        search_term = goal.get("steps", [""])[0] # Pega a primeira etapa da descrição
        request_to_searcher = self.create_message(
            recipient_id="web_search_001",
            message_type=MessageType.REQUEST,
            content={"request_type": "search", "query": search_term},
            callback_id=mission_id
        )
        await self.message_bus.publish(request_to_searcher)

    async def continue_mission(self, response_message: AgentMessage):
        """Gerencia os próximos passos da missão com base nas respostas recebidas."""
        mission_id = response_message.callback_id
        if mission_id not in self.pending_missions:
            return

        mission = self.pending_missions[mission_id]
        
        # Passo 2: Recebeu a biografia, agora busca a imagem.
        if mission["state"] == "awaiting_bio_search":
            bio_results = response_message.content.get("results", [])
            mission["collected_data"]["biography_text"] = " ".join([r.get('snippet', '') for r in bio_results])
            mission["state"] = "awaiting_image_search"
            
            image_search_term = mission["goal"].get("steps", ["", ""])[1]
            request_to_searcher = self.create_message(
                "web_search_001", MessageType.REQUEST,
                {"request_type": "search", "query": image_search_term},
                callback_id=mission_id
            )
            await self.message_bus.publish(request_to_searcher)

        # Passo 3: Recebeu a imagem, agora pede para a IA consolidar tudo.
        elif mission["state"] == "awaiting_image_search":
            image_results = response_message.content.get("results", [])
            mission["collected_data"]["image_url"] = image_results[0].get("link") if image_results else "N/A"
            mission["state"] = "awaiting_ai_analysis"

            prompt = f"""
            Com base na biografia a seguir, identifique a música mais famosa e escreva um resumo de um parágrafo.
            Biografia: {mission['collected_data']['biography_text']}
            Responda em JSON com as chaves 'musica_famosa' e 'resumo'.
            """
            request_to_ai = self.create_message(
                "ai_analyzer_001", MessageType.REQUEST,
                {"request_type": "generate_structured_text", "text": prompt},
                callback_id=mission_id
            )
            await self.message_bus.publish(request_to_ai)

        # Passo 4: Recebeu a análise da IA, agora envia o e-mail.
        elif mission["state"] == "awaiting_ai_analysis":
            ai_results = response_message.content.get("result", {}).get("structured_data", {})
            mission["collected_data"].update(ai_results)
            mission["state"] = "awaiting_notification"

            email_body = f"""
            Dossiê: Divino Arbués
            
            Resumo:
            {mission['collected_data'].get('resumo', 'Não foi possível gerar um resumo.')}
            
            Música Mais Famosa:
            {mission['collected_data'].get('musica_famosa', 'Não foi possível identificar.')}
            
            Foto Encontrada:
            {mission['collected_data'].get('image_url', 'Nenhuma foto encontrada.')}
            """
            
            email_target = mission["goal"].get("steps", ["", "", "", ""])[3].split(" para ")[-1]

            request_to_notifier = self.create_message(
                "notification_001", MessageType.REQUEST,
                {
                    "request_type": "send_email",
                    "recipient": email_target,
                    "subject": "Dossiê: Divino Arbués (Gerado por SUNA-ALSHAM)",
                    "body": email_body
                },
                callback_id=mission_id
            )
            await self.message_bus.publish(request_to_notifier)

        # Passo 5: E-mail enviado. Missão concluída.
        elif mission["state"] == "awaiting_notification":
            logger.info(f"Missão [ID: {mission_id}] concluída com sucesso!")
            # Limpa a missão da memória
            del self.pending_missions[mission_id]


class MetaCognitiveAgent(BaseNetworkAgent):
    """
    O Cérebro Estratégico. Analisa o comportamento da rede como um todo.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.META_COGNITIVE, message_bus)
        self.capabilities.append("system_analysis")
        self._analysis_task: Optional[asyncio.Task] = None
        logger.info(f"🧠 {self.agent_id} (Meta-Cognitivo) inicializado.")

    async def start_meta_cognition(self):
        if not self._analysis_task:
            self._analysis_task = asyncio.create_task(self._analysis_loop())
            logger.info(f"🧠 {self.agent_id} iniciou processos meta-cognitivos.")

    async def _analysis_loop(self):
        while True:
            await asyncio.sleep(300)
            logger.info("[Simulação] Analisando performance da rede...")


def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Cria os agentes de Meta-Cognição.
    """
    agents = []
    logger.info("🧠 Criando agentes Meta-Cognitivos...")
    
    orchestrator = OrchestratorAgent("orchestrator_001", message_bus)
    meta_agent = MetaCognitiveAgent("metacognitive_001", message_bus)
    
    asyncio.create_task(meta_agent.start_meta_cognition())
    
    agents.extend([orchestrator, meta_agent])
    return agents
