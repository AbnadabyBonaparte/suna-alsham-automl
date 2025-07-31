#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos – O Cérebro do SUNA-ALSHAM.
Versão Viva – Orquestra qualquer missão, entende texto livre e JSON.
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, List
from suna_alsham_core.multi_agent_network import AgentMessage, AgentType, BaseNetworkAgent, MessageType

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.capabilities.extend(["dynamic_planning", "complex_task_orchestration"])
        self.pending_missions: Dict[str, Dict] = {}
        logger.info(f"👑 {self.agent_id} inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST:
            req_type = message.content.get("request_type")
            if req_type == "execute_complex_task":
                await self.start_mission_planning(message)
            else:
                # Se não é estruturado, manda para AIAnalyzer traduzir
                text = message.content.get("text")
                if text:
                    await self._translate_free_text(message)
        elif message.message_type == MessageType.RESPONSE:
            await self.continue_mission_execution(message)

    async def _translate_free_text(self, original_message: AgentMessage):
        mission_id = str(uuid.uuid4())
        prompt = f"""
        Analise o texto abaixo e converta para um JSON estruturado com:
        - goal.description
        - goal.steps[] (lista de passos em linguagem natural)

        Texto: {original_message.content.get("text")}
        """
        msg = self.create_message(
            recipient_id="ai_analyzer_001",
            message_type=MessageType.REQUEST,
            content={"request_type": "generate_structured_text", "text": prompt},
            callback_id=mission_id
        )
        self.pending_missions[mission_id] = {"original_message": original_message, "state": "awaiting_translation"}
        await self.message_bus.publish(msg)

    async def start_mission_planning(self, original_message: AgentMessage):
        mission_id = str(uuid.uuid4())
        goal = original_message.content.get("goal", {})
        goal_description = goal.get("description")
        goal_steps = goal.get("steps", [])

        if not goal_description or not goal_steps:
            await self.publish_error_response(original_message, "Meta ou passos inválidos.")
            return

        logger.info(f"Nova missão [ID: {mission_id}]: '{goal_description}'")

        self.pending_missions[mission_id] = {
            "original_message": original_message,
            "state": "awaiting_plan",
            "goal": goal,
            "plan": None,
            "current_step": -1,
            "step_results": {}
        }

        prompt = f"""
        Crie um plano de execução em JSON para a meta:
        "{goal_description}"
        Passos: {json.dumps(goal_steps, ensure_ascii=False)}

        Agentes disponíveis:
        - web_search_001 (busca)
        - ai_analyzer_001 (análise)
        - notification_001 (e-mail)

        Responda apenas com JSON de passos.
        """

        req = self.create_message(
            recipient_id="ai_analyzer_001",
            message_type=MessageType.REQUEST,
            content={"request_type": "generate_structured_text", "text": prompt},
            callback_id=mission_id
        )
        await self.message_bus.publish(req)

    async def continue_mission_execution(self, response_message: AgentMessage):
        mission_id = response_message.callback_id
        if mission_id not in self.pending_missions:
            return

        mission = self.pending_missions[mission_id]

        # Tradução de texto livre para JSON de missão
        if mission["state"] == "awaiting_translation":
            data = response_message.content.get("result", {}).get("structured_data", {})
            if not data:
                await self.publish_error_response(mission["original_message"], "Falha na tradução do texto.")
                del self.pending_missions[mission_id]
                return
            # Reenvia como missão estruturada
            structured = self.create_message(
                recipient_id=self.agent_id,
                message_type=MessageType.REQUEST,
                content={"request_type": "execute_complex_task", "goal": data.get("goal")},
                callback_id=mission_id
            )
            await self._internal_handle_message(structured)
            return

        # Plano de missão
        if mission["state"] == "awaiting_plan":
            plan_json = response_message.content.get("result", {}).get("structured_data", [])
            if not isinstance(plan_json, list) or len(plan_json) == 0:
                await self.publish_error_response(mission["original_message"], "Plano inválido ou vazio.")
                del self.pending_missions[mission_id]
                return
            mission["plan"] = plan_json
            mission["state"] = "executing"
            mission["current_step"] = 0
            await self._execute_next_step(mission_id)
            return

        # Execução de passos
        if mission["state"] == "executing":
            mission["step_results"][f"step_{mission['current_step']+1}_output"] = response_message.content
            mission["current_step"] += 1
            if mission["current_step"] < len(mission["plan"]):
                await self._execute_next_step(mission_id)
            else:
                await self.publish_response(mission["original_message"], {"status": "completed"})
                del self.pending_missions[mission_id]

    async def _execute_next_step(self, mission_id: str):
        mission = self.pending_missions[mission_id]
        step_info = mission["plan"][mission["current_step"]]
        req = self.create_message(
            recipient_id=step_info["agent_id"],
            message_type=MessageType.REQUEST,
            content=step_info.get("content", {}),
            callback_id=mission_id
        )
        await self.message_bus.publish(req)

def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    agents = []
    orchestrator = OrchestratorAgent("orchestrator_001", message_bus)
    agents.append(orchestrator)
    return agents
