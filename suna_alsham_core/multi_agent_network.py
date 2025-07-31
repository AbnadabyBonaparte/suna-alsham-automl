#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos – SUNA-ALSHAM.

Versão Viva – O agente entende qualquer missão e cria planos dinâmicos
sem depender de dados hardcoded.
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, List, Any

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseNetworkAgent):
    """
    Orquestrador Supremo – Cria planos inteligentes e executa missões complexas.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.capabilities.extend(["dynamic_planning", "complex_task_orchestration"])
        self.pending_missions: Dict[str, Dict[str, Any]] = {}
        logger.info(f"👑 {self.agent_id} inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "execute_complex_task":
            await self.start_mission_planning(message)
        elif message.message_type == MessageType.RESPONSE:
            await self.continue_mission_execution(message)

    async def start_mission_planning(self, original_message: AgentMessage):
        mission_id = str(uuid.uuid4())
        goal = original_message.content.get("goal", {})
        goal_description = goal.get("description", "Missão sem descrição")
        goal_steps = goal.get("steps", [])

        logger.info(f"Nova missão [ID: {mission_id}] → {goal_description}")

        self.pending_missions[mission_id] = {
            "original_message": original_message,
            "state": "awaiting_plan",
            "goal": goal,
            "plan": None,
            "current_step": -1,
            "step_results": {}
        }

        # 🔥 Prompt dinâmico: não define e-mail, pede para a IA decidir.
        prompt = f"""
        Você é um planejador de missões. Crie um plano de ação em JSON puro.

        Meta: "{goal_description}"
        Passos sugeridos: {json.dumps(goal_steps, ensure_ascii=False)}

        Agentes disponíveis:
        - web_search_001 (busca web)
        - ai_analyzer_001 (análise de dados/texto)
        - notification_001 (envio de mensagens/emails)

        Se a meta mencionar "enviar por e-mail" ou "notificar", descubra o destinatário
        a partir da descrição e inclua no passo de notificação.

        Responda somente com JSON: lista de passos contendo agent_id, request_type e content.
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
                await self.publish_error_response(mission["original_message"], "Plano de ação inválido ou vazio.")
                del self.pending_missions[mission_id]
                return

            mission["plan"] = plan_json
            mission["state"] = "executing"
            mission["current_step"] = 0
            logger.info(f"Missão [ID: {mission_id}] → Plano com {len(plan_json)} passos gerado.")
            await self._execute_next_step(mission_id)

        elif mission["state"] == "executing":
            step_key = f"step_{mission['current_step'] + 1}_output"
            mission["step_results"][step_key] = response_message.content

            mission["current_step"] += 1
            if mission["current_step"] < len(mission["plan"]):
                await self._execute_next_step(mission_id)
            else:
                logger.info(f"Missão [ID: {mission_id}] concluída.")
                await self.publish_response(mission["original_message"], {
                    "status": "completed",
                    "final_result": mission["step_results"]
                })
                del self.pending_missions[mission_id]

    async def _execute_next_step(self, mission_id: str):
        mission = self.pending_missions[mission_id]
        step_info = mission["plan"][mission["current_step"]]

        content = step_info.get("content", {})
        # Substitui variáveis com outputs anteriores
        content_str = json.dumps(content)
        for key, value in mission["step_results"].items():
            content_str = content_str.replace(f"{{{{{key}}}}}", json.dumps(value))
        final_content = json.loads(content_str)

        request_to_agent = self.create_message(
            recipient_id=step_info["agent_id"],
            message_type=MessageType.REQUEST,
            content=final_content,
            callback_id=mission_id
        )
        logger.info(f"➡️ Executando passo {mission['current_step']+1}: {step_info['agent_id']} -> {final_content}")
        await self.message_bus.publish(request_to_agent)

def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    agents = []
    logger.info("🧠 Criando OrchestratorAgent vivo...")
    try:
        agents.append(OrchestratorAgent("orchestrator_001", message_bus))
    except Exception as e:
        logger.error(f"❌ Erro ao criar OrchestratorAgent: {e}", exc_info=True)
    return agents
