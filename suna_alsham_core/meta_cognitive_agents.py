#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos - O Cérebro Estratégico do SUNA-ALSHAM.

[Versão Final - Produção Robusta]

Capacidade:
- Receber qualquer missão complexa.
- Interpretar claramente a meta.
- Criar planos inteligentes usando IA.
- Delegar tarefas dinamicamente para agentes especialistas.
- Gerenciar resultados intermediários.
- Garantir tratamento robusto contra falhas e planos inválidos.
"""

import asyncio
import json
import logging
import uuid
from typing import Any, Dict, List

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
)

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseNetworkAgent):
    """
    Agente Orquestrador Estratégico. Cria e executa planos dinâmicos e robustos.
    """

    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.capabilities.extend(["dynamic_planning", "complex_task_orchestration"])
        self.pending_missions: Dict[str, Dict] = {}
        logger.info(f"👑 {self.agent_id} (Orquestrador Estratégico) evoluído e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "execute_complex_task":
            await self.start_mission_planning(message)
        elif message.message_type == MessageType.RESPONSE:
            await self.continue_mission_execution(message)

    async def start_mission_planning(self, original_message: AgentMessage):
        mission_id = str(uuid.uuid4())
        goal = original_message.content.get("goal", {})

        goal_description = goal.get("description")
        if not goal_description:
            logger.error(f"Missão [ID: {mission_id}] sem descrição do objetivo. Abortando.")
            await self.publish_error_response(original_message, "A meta ('goal.description') não foi fornecida.")
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
        Crie um plano de ação detalhado em formato JSON para cumprir a seguinte meta:
        "{goal_description}"

        Agentes disponíveis para delegação:
        - WebSearchAgent (web_search_001)
        - AIAnalyzerAgent (ai_analyzer_001)
        - NotificationAgent (notification_001)

        Cada passo deve ter a estrutura:
        {{
          "step": <número do passo>,
          "agent_id": "<ID do agente>",
          "request_type": "<tipo de requisição>",
          "content": {{<parâmetros da requisição>}}
        }}

        Responda APENAS com o JSON do plano, nada mais.
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
            logger.error(f"Missão desconhecida recebida: {mission_id}")
            return

        mission = self.pending_missions[mission_id]

        if mission["state"] == "awaiting_plan":
            plan_json = response_message.content.get("result", {}).get("structured_data", [])
            if not isinstance(plan_json, list) or not plan_json:
                logger.error(f"Missão [ID: {mission_id}] falhou: Plano inválido ou vazio.")
                await self.publish_error_response(mission["original_message"], "Plano de ação inválido ou vazio.")
                del self.pending_missions[mission_id]
                return

            mission["plan"] = plan_json
            mission["state"] = "executing"
            mission["current_step"] = 0
            logger.info(f"Missão [ID: {mission_id}] plano com {len(plan_json)} passos criado.")
            await self._execute_next_step(mission_id)

        elif mission["state"] == "executing":
            step_num = mission['current_step'] + 1
            mission["step_results"][f"step_{step_num}_output"] = response_message.content

            mission["current_step"] += 1
            if mission["current_step"] < len(mission["plan"]):
                await self._execute_next_step(mission_id)
            else:
                logger.info(f"Missão [ID: {mission_id}] concluída.")
                await self.publish_response(mission["original_message"], {"status": "completed", "final_result": response_message.content})
                del self.pending_missions[mission_id]

    async def _execute_next_step(self, mission_id: str):
        mission = self.pending_missions[mission_id]
        try:
            step_info = mission["plan"][mission["current_step"]]

            content_str = json.dumps(step_info.get("content", {}))
            for key, value in mission["step_results"].items():
                content_str = content_str.replace(f"{{{{{key}}}}}", json.dumps(value))

            final_content = json.loads(content_str)
            final_content["request_type"] = step_info.get("request_type")

            request_to_agent = self.create_message(
                recipient_id=step_info["agent_id"],
                message_type=MessageType.REQUEST,
                content=final_content,
                callback_id=mission_id,
            )
            await self.message_bus.publish(request_to_agent)
        except Exception as e:
            logger.error(f"Erro executando passo {mission['current_step']+1} da missão [ID: {mission_id}]: {e}", exc_info=True)
            await self.publish_error_response(mission["original_message"], f"Erro ao executar passo da missão: {e}")
            del self.pending_missions[mission_id]


def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    agents = []
    logger.info("🧠 Inicializando agentes Meta-Cognitivos...")
    try:
        orchestrator = OrchestratorAgent("orchestrator_001", message_bus)
        agents.append(orchestrator)
    except Exception as e:
        logger.critical(f"Falha crítica ao criar agentes Meta-Cognitivos: {e}", exc_info=True)
    return agents
