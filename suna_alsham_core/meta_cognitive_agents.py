#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos – O Cérebro do SUNA-ALSHAM.
"""

import asyncio
import logging
from typing import Dict, List, Optional

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseNetworkAgent):
    """
    Agente Orquestrador Estratégico. Gerencia missões do início ao fim.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.pending_missions: Dict[str, Dict] = {}
        logger.info(f"👑 {self.agent_id} (Orquestrador Estratégico) evoluído e operacional.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST:
            await self._handle_new_request(message)
        elif message.message_type == MessageType.RESPONSE:
            await self._handle_response(message)

    async def _handle_new_request(self, message: AgentMessage):
        mission_id = message.message_id
        logger.info(f"👑 [Orquestrador] Nova Missão '{mission_id}' recebida de '{message.sender_id}'.")
        self.pending_missions[mission_id] = {"original_request": message, "status": "planning", "plan": [], "current_step": 0}

        planning_request = self.create_message(
            recipient_id="ai_analyzer_001",
            message_type=MessageType.REQUEST,
            content={"task": "create_execution_plan", "user_request": message.content},
            priority=Priority.HIGH,
            callback_id=mission_id
        )
        await self.message_bus.publish(planning_request)
        logger.info(f"👑 [Orquestrador] Missão '{mission_id}' enviada para 'ai_analyzer_001' para planejamento.")

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
        logger.info(f"👑 [Orquestrador] Plano para a Missão '{mission_id}' recebido de 'ai_analyzer_001'.")

        plan = plan_message.content.get("plan")
        if plan_message.content.get("status") != "success" or not isinstance(plan, list) or not plan:
            error_msg = f"Falha ao criar plano para Missão '{mission_id}'. Motivo: {plan_message.content.get('message', 'Plano inválido.')}"
            await self._abort_mission(mission_id, error_msg)
            return

        mission["plan"] = plan
        mission["status"] = "executing"
        logger.info(f"👑 [Orquestrador] Plano validado. Iniciando execução da Missão '{mission_id}' com {len(plan)} passos.")
        await self._execute_mission_step(mission_id)

    async def _handle_step_response(self, mission_id: str, step_index: int, step_message: AgentMessage):
        mission = self.pending_missions[mission_id]
        if mission["current_step"] != step_index: return

        if step_message.content.get("status") != "success":
            error_msg = f"Falha no passo {step_index + 1} da Missão '{mission_id}'. Agente '{step_message.sender_id}' reportou erro."
            await self._abort_mission(mission_id, error_msg)
            return
        
        logger.info(f"✅ [Orquestrador] Passo {step_index + 1}/{len(mission['plan'])} da Missão '{mission_id}' concluído.")
        mission["current_step"] += 1
        await self._execute_mission_step(mission_id)
        
    async def _execute_mission_step(self, mission_id: str):
        if mission_id not in self.pending_missions: return
        mission = self.pending_missions[mission_id]
        
        if mission["current_step"] >= len(mission["plan"]):
            success_msg = f"Missão '{mission_id}' concluída com sucesso!"
            logger.info(f"🎉 [Orquestrador] {success_msg}")
            await self.publish_response(mission["original_request"], {"status": "success", "message": success_msg})
            del self.pending_missions[mission_id]
            return

        step = mission["plan"][mission["current_step"]]
        step_index = mission["current_step"]
        
        try:
            target_agent = step["agent"]
            task_content = step["task"]
        except KeyError as e:
            await self._abort_mission(mission_id, f"Passo {step_index + 1} do plano é malformado. Chave ausente: {e}")
            return

        logger.info(f"▶️ [Orquestrador] Executando passo {step_index + 1}: Delegando para '{target_agent}'.")
        step_request = self.create_message(recipient_id=target_agent, message_type=MessageType.REQUEST, content=task_content, callback_id=f"{mission_id}_step_{step_index}")
        await self.message_bus.publish(step_request)

    async def _abort_mission(self, mission_id: str, reason: str):
        logger.error(f"🛑 [Orquestrador] ABORTANDO Missão '{mission_id}'. Motivo: {reason}")
        if mission_id in self.pending_missions:
            mission = self.pending_missions[mission_id]
            await self.publish_error_response(mission["original_request"], reason)
            del self.pending_missions[mission_id]

class MetaCognitiveAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.META_COGNITIVE, message_bus)
        self._analysis_task: Optional[asyncio.Task] = None
        logger.info(f"🧠 {self.agent_id} (Meta-Cognitivo) inicializado.")

    async def start_meta_cognition(self):
        if self._analysis_task is None or self._analysis_task.done():
            self._analysis_task = asyncio.create_task(self._analysis_loop())

    async def _analysis_loop(self):
        logger.info(f"🧠 {self.agent_id} iniciou processos meta-cognitivos.")
        while True:
            await asyncio.sleep(300)
            logger.info("[Meta-Cog] Analisando performance da rede...")

def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    agents: List[BaseNetworkAgent] = []
    logger.info("🧠 Criando agentes do Cérebro (Meta-Cognitivos)...")
    try:
        orchestrator = OrchestratorAgent("orchestrator_001", message_bus)
        meta_agent = MetaCognitiveAgent("metacognitive_001", message_bus)
        asyncio.create_task(meta_agent.start_meta_cognition())
        agents.extend([orchestrator, meta_agent])
        logger.info("✅ Cérebro do sistema criado com sucesso.")
    except Exception as e:
        logger.critical(f"❌ Erro CRÍTICO criando agentes Meta-Cognitivos: {e}", exc_info=True)
    return agents
