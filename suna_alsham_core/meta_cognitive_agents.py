#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos – O Cérebro do SUNA-ALSHAM.
[Versão 2.1 - Coleta de Dados para Evolução]
"""
import asyncio
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional

# Importa o Dataclass de treino do motor de evolução
from suna_alsham_core.real_evolution_engine import TrainingDataPoint
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

def _get_value_from_path(data: Dict, path: str):
    keys = path.split('.')
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else: return None
    return data

class OrchestratorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.pending_missions: Dict[str, Dict] = {}
        logger.info(f"👑 {self.agent_id} (Orquestrador Estratégico) V2.1 com coleta de dados.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST:
            await self._handle_new_request(message)
        elif message.message_type == MessageType.RESPONSE:
            await self._handle_response(message)

    async def _handle_new_request(self, message: AgentMessage):
        mission_id = message.message_id
        logger.info(f"👑 [Orquestrador] Nova Missão '{mission_id}' recebida. Iniciando planejamento.")
        self.pending_missions[mission_id] = {
            "original_request": message,
            "status": "planning",
            "step_outputs": {},
            "start_time": datetime.now() # Adiciona o tempo de início
        }
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
            error_msg = f"Falha no planejamento: {plan_message.content.get('message', 'Plano inválido.')}"
            await self._conclude_mission(mission_id, "failed", error_msg)
            return
        mission["plan"] = plan
        mission["status"] = "executing"
        await self._execute_mission_step(mission_id)

    async def _handle_step_response(self, mission_id: str, step_index: int, step_message: AgentMessage):
        mission = self.pending_missions[mission_id]
        if mission.get("current_step", -1) != step_index: return
        if step_message.content.get("status") != "success":
            error_msg = f"Falha no passo {step_index + 1}: {step_message.content.get('message')}"
            await self._conclude_mission(mission_id, "failed", error_msg)
            return
        mission["step_outputs"][step_index + 1] = step_message.content
        mission["current_step"] += 1
        await self._execute_mission_step(mission_id)

    def _resolve_context(self, task_content: Dict, step_outputs: Dict) -> Dict:
        resolved_content = json.dumps(task_content)
        placeholders = re.findall(r"\{\{output_step_(\d+)\.([^}]+)\}\}", resolved_content)
        for step_num, path in placeholders:
            step_output = step_outputs.get(int(step_num))
            if step_output:
                value = _get_value_from_path(step_output, path)
                placeholder_str = f"\"{{{{output_step_{step_num}.{path}}}}}\""
                resolved_content = resolved_content.replace(placeholder_str, json.dumps(value))
        return json.loads(resolved_content)

    async def _execute_mission_step(self, mission_id: str):
        if mission_id not in self.pending_missions: return
        mission = self.pending_missions[mission_id]
        if "current_step" not in mission: mission["current_step"] = 0
        step_index = mission["current_step"]

        if step_index >= len(mission.get("plan", [])):
            success_msg = "Missão concluída com sucesso."
            await self._conclude_mission(mission_id, "success", success_msg)
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
            await self._conclude_mission(mission_id, "failed", f"Erro ao executar passo {step_index + 1}: {e}")

    # --- NOVAS FUNÇÕES ADICIONADAS ---
    async def _conclude_mission(self, mission_id: str, final_status: str, message: str):
        if mission_id not in self.pending_missions: return
        mission = self.pending_missions[mission_id]
        response_content = {"status": final_status, "message": message}
        if final_status == "success":
            await self.publish_response(mission["original_request"], response_content)
        else:
            await self.publish_error_response(mission["original_request"], message)
        await self._send_training_data(mission, final_status)
        del self.pending_missions[mission_id]

    async def _send_training_data(self, mission: Dict, final_status: str):
        duration = (datetime.now() - mission.get("start_time", datetime.now())).total_seconds()
        reward = 1.0 if final_status == "success" else -1.0
        data_point = TrainingDataPoint(
            agent_id="orchestrator_001",
            state_features={"num_steps": len(mission.get("plan", [])), "duration_seconds": duration},
            action_taken={"plan_hash": hash(str(mission.get("plan", [])))},
            outcome_reward=reward
        )
        training_message = self.create_message(
            recipient_id="evolution_engine_001",
            message_type=MessageType.NOTIFICATION,
            content={"event_type": "training_data", "data": data_point.__dict__}
        )
        await self.message_bus.publish(training_message)
        logger.info(f"👑 [Orquestrador] Dados de treino da missão enviados para o Evolution Engine.")

# O resto do ficheiro (MetaCognitiveAgent e a fábrica) continua igual
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
