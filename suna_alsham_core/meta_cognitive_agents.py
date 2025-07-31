#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos - O Cérebro do SUNA-ALSHAM.

[Versão Defensiva] - Adiciona validações extras no Orquestrador para
garantir que todas as tarefas delegadas sejam bem-formadas.
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
        # ... (código existente) ...
        pass

    async def start_mission_planning(self, original_message: AgentMessage):
        # ... (código existente) ...
        pass

    async def continue_mission_execution(self, response_message: AgentMessage):
        # ... (código existente) ...
        pass

    async def _execute_next_step(self, mission_id: str):
        """Lê o próximo passo do plano e o delega para o agente correto."""
        mission = self.pending_missions[mission_id]
        step_info = mission["plan"][mission["current_step"]]
    
        logger.info(
            f"Missão [ID: {mission_id}]. Executando Passo {step_info['step']}: "
            f"chamando agente '{step_info['agent_id']}'."
        )
    
        content_dict = step_info.get("content", {})
        content_str = json.dumps(content_dict)
    
        for key, value in mission["step_results"].items():
            placeholder = f"{{{{{key}}}}}"
            content_str = content_str.replace(placeholder, json.dumps(value))
    
        final_content = json.loads(content_str)
    
        req_type = step_info.get("request_type")
        if req_type:
            final_content["request_type"] = req_type
        else:
            logger.error(f"Passo {step_info['step']} do plano não contém 'request_type'.")
            await self.publish_error_response(mission["original_message"], f"O passo {step_info['step']} do plano não define 'request_type'.")
            del self.pending_missions[mission_id]
            return
    
        # --- VALIDAÇÕES DEFENSIVAS ADICIONADAS ---
        if step_info["agent_id"] == "ai_analyzer_001" and not final_content.get("text"):
            logger.error(f"Passo {step_info['step']} gerou um prompt vazio para o AIAnalyzer. Abortando.")
            await self.publish_error_response(mission["original_message"], "O plano de ação gerou um prompt vazio para o AIAnalyzer.")
            del self.pending_missions[mission_id]
            return
        
        if step_info["agent_id"] == "web_search_001" and not final_content.get("query"):
            logger.error(f"Passo {step_info['step']} gerou uma busca sem 'query'. Abortando.")
            await self.publish_error_response(mission["original_message"], "O plano de ação gerou uma busca sem definir 'query'.")
            del self.pending_missions[mission_id]
            return
        # --- FIM DAS VALIDAÇÕES ---
    
        request_to_agent = self.create_message(
            recipient_id=step_info["agent_id"],
            message_type=MessageType.REQUEST,
            content=final_content,
            callback_id=mission_id,
        )
        await self.message_bus.publish(request_to_agent)

class MetaCognitiveAgent(BaseNetworkAgent):
    # ... (código existente) ...
    pass

def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    # ... (código existente) ...
    pass
