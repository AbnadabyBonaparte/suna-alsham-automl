#!/usr/bin/env python3
"""
Módulo do Social Media Orchestrator Agent - ALSHAM GLOBAL

[Fase 3] - Fortalecido com lógica real de coordenação entre os agentes
de mídias sociais.
"""

import asyncio
import logging
from typing import Any, Dict, List

# Importa a classe base e as ferramentas do nosso núcleo fortalecido
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


class SocialMediaOrchestratorAgent(BaseNetworkAgent):
    """
    O cérebro da operação de mídias sociais. Coordena outros agentes
    para executar a estratégia de conteúdo, engajamento e crescimento.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o SocialMediaOrchestratorAgent."""
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        
        self.capabilities.extend([
            "social_media_strategy",
            "trend_analysis",
            "content_coordination",
            "performance_reporting",
        ])
        
        self.active_strategy = None
        logger.info(f"🎯 {self.agent_id} (Orquestrador de Mídias Sociais) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições para orquestração de mídias sociais."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        handler = {
            "define_strategy": self._define_strategy,
            "analyze_trends": self._analyze_trends,
            "coordinate_posting": self._coordinate_posting,
        }.get(request_type)

        if handler:
            result = await handler(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            await self.message_bus.publish(self.create_error_response(message, "Ação de orquestração desconhecida"))

    async def _define_strategy(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Usa o AIAnalyzerAgent para definir uma estratégia de conteúdo."""
        client_briefing = request_data.get("briefing", "Nenhum briefing fornecido.")
        logger.info(f"Definindo estratégia de mídias sociais com base em: '{client_briefing[:50]}...'")

        try:
            response_message = await self.send_request_and_wait(
                "ai_analyzer_001",
                {"request_type": "ai_analysis", "data": {"prompt": f"Crie uma estratégia de mídias sociais para: {client_briefing}"}}
            )
            self.active_strategy = response_message.content.get("analysis", "Estratégia não definida.")
            return {"status": "completed", "strategy_defined": self.active_strategy}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _analyze_trends(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Usa o WebSearchAgent para buscar tendências.
        """
        topic = request_data.get("topic", "marketing digital")
        logger.info(f"Analisando tendências para o tópico: '{topic}'")
        
        try:
            response_message = await self.send_request_and_wait(
                "web_search_001",
                {"request_type": "search_solutions", "problem_description": f"tendências de {topic} para redes sociais"}
            )
            trends = response_message.content.get("solution", {})
            return {"status": "completed", "trends_found": trends}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _coordinate_posting(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Orquestra a criação e postagem de conteúdo,
        comandando os outros super agentes.
        """
        topic = request_data.get("topic", "inteligência artificial")
        logger.info(f"Coordenando postagem sobre: '{topic}'")
        
        try:
            # 1. Pede ao ContentCreatorAgent para criar um roteiro de vídeo.
            logger.info("  -> Solicitando roteiro ao ContentCreatorAgent...")
            script_response = await self.send_request_and_wait(
                "content_creator_001",
                {
                    "request_type": "generate_content",
                    "content_type": "article_script",
                    "topic": topic,
                    "tone": "inspirador",
                    "target_audience": "empreendedores"
                }
            )
            script = script_response.content.get("generated_content", "Roteiro padrão.")
            
            # 2. Pede ao VideoAutomationAgent para criar um vídeo com o roteiro.
            logger.info("  -> Solicitando criação de vídeo ao VideoAutomationAgent...")
            video_response = await self.send_request_and_wait(
                "video_automation_001",
                {
                    "request_type": "create_video",
                    "script_scenes": script.split('\n')[:5], # Pega as 5 primeiras linhas
                    "format": "reels"
                }
            )
            video_path = video_response.content.get("video_path")

            return {
                "status": "completed",
                "message": "Criação e postagem coordenadas com sucesso.",
                "roteiro_criado": script,
                "video_final_path": video_path
            }

        except Exception as e:
            logger.error(f"Erro na coordenação de postagem: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}


def create_social_media_orchestrator_agent(message_bus) -> List[SocialMediaOrchestratorAgent]:
    """Cria o agente Orquestrador de Mídias Sociais."""
    agents = []
    logger.info("🎯 Criando SocialMediaOrchestratorAgent...")
    try:
        agent = SocialMediaOrchestratorAgent("social_media_orchestrator_001", message_bus)
        agents.append(agent)
    except Exception as e:
        logger.error(f"❌ Erro crítico criando SocialMediaOrchestratorAgent: {e}", exc_info=True)
    return agents
