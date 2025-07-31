#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos - O Cérebro do SUNA-ALSHAM.

[Versão Final Corrigida] - Adiciona validação de robustez para garantir
que os prompts gerados para a IA nunca sejam vazios.
"""

import asyncio
import logging
import uuid
import json
from typing import Any, Dict, List, Optional

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

# --- Classe Principal do Agente ---

class OrchestratorAgent(BaseNetworkAgent):
    """
    Agente Orquestrador Estratégico. Cria e executa planos de ação dinâmicos.
    """
    def __init__(self, agent_id: str, message_bus):
        """Inicializa o OrchestratorAgent."""
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.capabilities.extend(["dynamic_planning", "complex_task_orchestration"])
        self.pending_missions: Dict[str, Dict] = {}
        logger.info(f"👑 {self.agent_id} (Orquestrador Estratégico) evoluído e inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa novas missões ou respostas de agentes delegados."""
        if message.message_type == MessageType.REQUEST and message.content.get("request_type") == "execute_complex_task":
            await self.start_mission_planning(message)
        
        elif message.message_type == MessageType.RESPONSE:
            await self.continue_mission_execution(message)

    async def start_mission_planning(self, original_message: AgentMessage):
        """Passo 1: Recebe a meta e pede para a IA criar um plano de ação."""
        mission_id = str(uuid.uuid4())
        goal = original_message.content.get("goal", {})
        
        # --- CORREÇÃO DE ROBUSTEZ AQUI ---
        goal_description = goal.get("description")
        if not goal_description:
            logger.error(f"Missão [ID: {mission_id}] recebida sem uma descrição de objetivo ('goal.description'). Abortando.")
            await self.publish_error_response(original_message, "A meta da missão ('goal.description') não foi fornecida.")
            return
            
        logger.info(f"Nova missão [ID: {mission_id}] recebida. Gerando plano de ação para: '{goal_description}'")

        self.pending_missions[mission_id] = {
            "original_message": original_message, "state": "awaiting_plan", "goal": goal,
            "plan": None, "current_step": -1, "step_results": {}
        }

        # Cria um prompt para o agente de IA gerar o plano
        prompt = f"""
        Você é o cérebro de um sistema de IA. Sua tarefa é criar um plano de ação para atingir uma meta.
        Você tem acesso aos seguintes agentes:
        - WebSearchAgent (id: 'web_search_001'): Pode pesquisar na internet. request_type: 'search', content: {{'query': '...'}}
        - AIAnalyzerAgent (id: 'ai_analyzer_001'): Pode analisar ou gerar texto. request_type: 'generate_structured_text', content: {{'text': '...'}}
        - NotificationAgent (id: 'notification_001'): Pode enviar e-mails. request_type: 'send_email', content: {{'recipient': '...', 'subject': '...', 'body': '...'}}

        Meta do Usuário: "{goal_description}"

        Crie um plano de ação em formato JSON. O JSON deve ser uma lista de passos. Cada passo deve ter:
        - 'step': número do passo (começando em 1)
        - 'agent_id': o ID do agente a ser chamado
        - 'request_type': a ação que o agente deve executar
        - 'content': um dicionário com os parâmetros para a ação. Use placeholders como "{{{{step_1_output.results[0].snippet}}}}" para usar o resultado de um passo anterior.

        Responda APENAS com o JSON do plano.
        """

        request_to_ai = self.create_message(
            recipient_id="ai_analyzer_001",
            message_type=MessageType.REQUEST,
            content={"request_type": "generate_structured_text", "text": prompt},
            callback_id=mission_id
        )
        await self.message_bus.publish(request_to_ai)

    async def continue_mission_execution(self, response_message: AgentMessage):
        """Gerencia a execução do plano de ação, passo a passo."""
        mission_id = response_message.callback_id
        if mission_id not in self.pending_missions: return

        mission = self.pending_missions[mission_id]
        
        if mission["state"] == "awaiting_plan":
            plan_json = response_message.content.get("result", {}).get("structured_data", [])
            if not plan_json or not isinstance(plan_json, list):
                logger.error(f"Missão [ID: {mission_id}] falhou: A IA não retornou um plano válido.")
                await self.publish_error_response(mission["original_message"], "A IA falhou ao gerar um plano de ação.")
                del self.pending_missions[mission_id]
                return

            mission["plan"] = plan_json
            mission["state"] = "executing"
            mission["current_step"] = 0
            logger.info(f"Missão [ID: {mission_id}]. Plano de ação gerado pela IA com {len(mission['plan'])} passos.")
            await self._execute_next_step(mission_id)

        elif mission["state"] == "executing":
            mission["step_results"][f"step_{mission['current_step'] + 1}_output"] = response_message.content
            
            mission["current_step"] += 1
            if mission["current_step"] < len(mission["plan"]):
                await self._execute_next_step(mission_id)
            else:
                logger.info(f"Missão [ID: {mission_id}] concluída com sucesso!")
                await self.publish_response(mission["original_message"], {"status": "completed", "final_result": response_message.content})
                del self.pending_missions[mission_id]

    async def _execute_next_step(self, mission_id: str):
        """Lê o próximo passo do plano e o delega para o agente correto."""
        mission = self.pending_missions[mission_id]
        step_info = mission["plan"][mission["current_step"]]
        
        logger.info(f"Missão [ID: {mission_id}]. Executando Passo {step_info['step']}: chamando agente '{step_info['agent_id']}'.")

        content_str = json.dumps(step_info["content"])
        # Lógica de substituição de placeholder (simplificada)
        for key, value in mission["step_results"].items():
            placeholder = f"{{{{{key}}}}}"
            content_str = content_str.replace(placeholder, json.dumps(value))
        
        final_content = json.loads(content_str)

        request_to_agent = self.create_message(
            recipient_id=step_info["agent_id"],
            message_type=MessageType.REQUEST,
            content=final_content,
            callback_id=mission_id
        )
        await self.message_bus.publish(request_to_agent)


class MetaCognitiveAgent(BaseNetworkAgent):
    # ... (O código do MetaCognitiveAgent permanece o mesmo) ...
    pass

def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    # ... (O código da função de fábrica permanece o mesmo) ...
    pass
