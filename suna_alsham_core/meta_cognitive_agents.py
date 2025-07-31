#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos – O Cérebro do SUNA-ALSHAM.

Versão Final Completa – Executa planos reais com buscas e e-mails.
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, List

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseNetworkAgent):
    """
    Agente Orquestrador Estratégico. Cria e executa planos de ação dinâmicos.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.capabilities.extend(["dynamic_planning", "complex_task_orchestration"])
        self.pending_missions: Dict[str, Dict] = {}
        logger.info(f"👑 {self.agent_id} inicializado com sucesso.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "execute_complex_task":
            await self.start_mission_planning(message)
        elif message.message_type == MessageType.RESPONSE:
            await self.continue_mission_execution(message)

    async def start_mission_planning(self, original_message: AgentMessage):
        mission_id = str(uuid.uuid4())
        goal = original_message.content.get("goal", {})
        goal_description = goal.get("description")
        goal_steps = goal.get("steps", [])

        if not goal_description or not goal_steps:
            error_msg = "A meta ou passos ('goal.description'/'goal.steps') estão ausentes ou inválidos."
            logger.error(f"Missão [ID: {mission_id}] abortada: {error_msg}")
            await self.publish_error_response(original_message, error_msg)
            return

        logger.info(f"Nova missão [ID: {mission_id}] recebida: '{goal_description}'")

        self.pending_missions[mission_id] = {
            "original_message": original_message,
            "state": "awaiting_plan",
            "goal": goal,
            "plan": None,
            "current_step": -1,
            "step_results": {}
        }

        prompt = f"""
        Crie um plano de ação detalhado e completo em formato JSON para realizar a seguinte meta:

        "{goal_description}"

        Os passos necessários são:
        {json.dumps(goal_steps, ensure_ascii=False)}

        Use obrigatoriamente os seguintes agentes disponíveis com seus IDs:

        - WebSearchAgent ('web_search_001'): Faz pesquisas reais na web. (request_type: "search", content: {{ "query": "<consulta>" }})
        - AIAnalyzerAgent ('ai_analyzer_001'): Analisa textos e seleciona informações úteis. (request_type: "analyze", content: {{ "text": "<texto_para_analise>", "instruction": "<instrução>" }})
        - NotificationAgent ('notification_001'): Envia e-mails. (request_type: "send_email", content: {{ "recipient": "casamondestore@gmail.com", "subject": "<assunto>", "body": "<conteudo>" }})

        Responda APENAS com o JSON estruturado contendo todos os passos acima.
        """

        request_to_ai = self.create_message(
            recipient_id="ai_analyzer_001",
            message_type=MessageType.REQUEST,
            content={"request_type": "generate_structured_text", "text": prompt},
            callback_id=mission_id
        )
        await self.message_bus.publish(request_to_ai)

    async def continue_mission_execution(self, response_message: AgentMessage):
        mission_id = response_message.callback_id
        if mission_id not in self.pending_missions:
            return

        mission = self.pending_missions[mission_id]

        if mission["state"] == "awaiting_plan":
            plan_json = response_message.content.get("result", {}).get("structured_data", [])
            if not isinstance(plan_json, list) or len(plan_json) == 0:
                error_msg = f"Plano inválido ou vazio para a missão [ID: {mission_id}]."
                logger.error(error_msg)
                await self.publish_error_response(mission["original_message"], error_msg)
                del self.pending_missions[mission_id]
                return

            mission["plan"] = plan_json
            mission["state"] = "executing"
            mission["current_step"] = 0
            logger.info(f"Missão [ID: {mission_id}] tem plano com {len(plan_json)} passos.")
            await self._execute_next_step(mission_id)

        elif mission["state"] == "executing":
            step_key = f"step_{mission['current_step'] + 1}_output"
            mission["step_results"][step_key] = response_message.content

            mission["current_step"] += 1
            if mission["current_step"] < len(mission["plan"]):
                await self._execute_next_step(mission_id)
            else:
                logger.info(f"Missão [ID: {mission_id}] concluída com sucesso.")
                await self.publish_response(mission["original_message"], {
                    "status": "completed",
                    "final_result": response_message.content
                })
                del self.pending_missions[mission_id]

    async def _execute_next_step(self, mission_id: str):
        mission = self.pending_missions[mission_id]
        step_info = mission["plan"][mission["current_step"]]

        content_str = json.dumps(step_info.get("content", {}))
        for key, value in mission["step_results"].items():
            content_str = content_str.replace(f"{{{{{key}}}}}", json.dumps(value))

        final_content = json.loads(content_str)
        final_content["request_type"] = step_info["request_type"]

        request_to_agent = self.create_message(
            recipient_id=step_info["agent_id"],
            message_type=MessageType.REQUEST,
            content=final_content,
            callback_id=mission_id,
        )
        logger.info(f"Executando passo {mission['current_step']+1}: Chamando agente {step_info['agent_id']}")
        await self.message_bus.publish(request_to_agent)


def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    agents = []
    logger.info("🧠 Criando agentes Meta-Cognitivos...")
    try:
        orchestrator = OrchestratorAgent("orchestrator_001", message_bus)
        agents.append(orchestrator)
    except Exception as e:
        logger.error(f"❌ Erro ao criar agentes Meta-Cognitivos: {e}", exc_info=True)
    return agents
