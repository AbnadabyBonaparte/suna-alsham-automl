#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos – O Cérebro do SUNA-ALSHAM.
[Versão 2.0 - Passagem de Contexto]
"""
import asyncio
import json
import logging
import re
from typing import Dict, List, Optional

# (o resto dos seus imports)
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

def _get_value_from_path(data: Dict, path: str):
    """Navega num dicionário usando um caminho de string como 'result.details'."""
    keys = path.split('.')
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data

class OrchestratorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.pending_missions: Dict[str, Dict] = {}
        logger.info(f"👑 {self.agent_id} (Orquestrador Estratégico) V2.0 com passagem de contexto.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST:
            await self._handle_new_request(message)
        elif message.message_type == MessageType.RESPONSE:
            await self._handle_response(message)

    async def _handle_new_request(self, message: AgentMessage):
        mission_id = message.message_id
        self.pending_missions[mission_id] = {"original_request": message, "status": "planning", "step_outputs": {}}
        planning_request = self.create_message(
            recipient_id="ai_analyzer_001", message_type=MessageType.REQUEST,
            content={"content": message.content.get("content")}, callback_id=mission_id
        )
        await self.message_bus.publish(planning_request)

    async def _handle_response(self, message: AgentMessage):
        if not message.callback_id: return
        if message.callback_id in self.pending_missions:
            await self._handle_plan_response(message.callback_id, message)
        elif "_step_" in message.callback_id:
            mission_id, step_str = message.callback_id.rsplit("_step_", 1)
            if mission_id in self.pending_missions:
                await self._handle_step_response(mission_id, int(step_str), message)

    async def _handle_plan_response(self, mission_id: str, plan_message: AgentMessage):
        mission = self.pending_missions[mission_id]
        plan = plan_message.content.get("plan")
        if plan_message.content.get("status") != "success" or not plan:
            await self._abort_mission(mission_id, f"Falha no planejamento: {plan_message.content.get('message')}")
            return
        mission["plan"] = plan
        mission["status"] = "executing"
        await self._execute_mission_step(mission_id)

    async def _handle_step_response(self, mission_id: str, step_index: int, step_message: AgentMessage):
        mission = self.pending_missions[mission_id]
        if mission.get("current_step", -1) != step_index: return
        if step_message.content.get("status") != "success":
            await self._abort_mission(mission_id, f"Falha no passo {step_index + 1}: {step_message.content.get('message')}")
            return
        mission["step_outputs"][step_index + 1] = step_message.content
        mission["current_step"] += 1
        await self._execute_mission_step(mission_id)

    def _resolve_context(self, task_content: Dict, step_outputs: Dict) -> Dict:
        """Substitui os placeholders {{...}} pelos dados dos passos anteriores."""
        resolved_content = json.dumps(task_content)
        placeholders = re.findall(r"\{\{output_step_(\d+)\.([^}]+)\}\}", resolved_content)
        for step_num, path in placeholders:
            step_output = step_outputs.get(int(step_num))
            if step_output:
                value = _get_value_from_path(step_output, path)
                # Substitui a string completa, incluindo as aspas
                placeholder_str = f"\"{{{{output_step_{step_num}.{path}}}}}\""
                resolved_content = resolved_content.replace(placeholder_str, json.dumps(value))
        return json.loads(resolved_content)

    async def _execute_mission_step(self, mission_id: str):
        if mission_id not in self.pending_missions: return
        mission = self.pending_missions[mission_id]
        
        if "current_step" not in mission: mission["current_step"] = 0
        step_index = mission["current_step"]

        if step_index >= len(mission.get("plan", [])):
            await self.publish_response(mission["original_request"], {"status": "success", "message": "Missão concluída."})
            del self.pending_missions[mission_id]
            return

        step = mission["plan"][step_index]
        try:
            resolved_task = self._resolve_context(step["task"], mission["step_outputs"])
            step_request = self.create_message(
                recipient_id=step["agent"], message_type=MessageType.REQUEST,
                content=resolved_task, callback_id=f"{mission_id}_step_{step_index}"
            )
            await self.message_bus.publish(step_request)
        except Exception as e:
            await self._abort_mission(mission_id, f"Erro ao executar passo {step_index + 1}: {e}")

    async def _abort_mission(self, mission_id: str, reason: str):
        if mission_id in self.pending_missions:
            mission = self.pending_missions[mission_id]
            await self.publish_error_response(mission["original_request"], reason)
            del self.pending_missions[mission_id]

# (O resto do ficheiro com MetaCognitiveAgent e a fábrica continua igual)
class MetaCognitiveAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.META_COGNITIVE, message_bus)
        self._analysis_task: Optional[asyncio.Task] = None
        logger.info(f"🧠 {self.agent_id} (Meta-Cognitivo) inicializado.")
    async def start_meta_cognition(self):
        if self._analysis_task is None or self._analysis_task.done():
            self._analysis_task = asyncio.create_task(self._analysis_loop())
    async def _analysis_loop(self):
        while True:
            await asyncio.sleep(300)
def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    agents: List[BaseNetworkAgent] = []
    try:
        orchestrator = OrchestratorAgent("orchestrator_001", message_bus)
        meta_agent = MetaCognitiveAgent("metacognitive_001", message_bus)
        asyncio.create_task(meta_agent.start_meta_cognition())
        agents.extend([orchestrator, meta_agent])
    except Exception as e:
        logger.critical(f"❌ Erro CRÍTICO criando agentes Meta-Cognitivos: {e}", exc_info=True)
    return agents
