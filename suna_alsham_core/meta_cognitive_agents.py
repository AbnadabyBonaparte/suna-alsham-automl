#!/usr/bin/env python3
"""
Módulo dos Agentes Meta-Cognitivos – O Cérebro do SUNA-ALSHAM.

[Versão Robusta 2.0] - Implementa o ciclo de vida completo da orquestração de missões,
com planejamento, execução passo a passo, monitoramento e tratamento de erros.
"""

import asyncio
import json
import logging
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
    É o cérebro operacional que gerencia missões do início ao fim.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.ORCHESTRATOR, message_bus)
        self.capabilities.extend(["dynamic_planning", "complex_task_orchestration", "mission_lifecycle_management"])
        self.pending_missions: Dict[str, Dict] = {}
        logger.info(f"👑 {self.agent_id} (Orquestrador Estratégico) evoluído e operacional.")

    async def _internal_handle_message(self, message: AgentMessage):
        """
        Ponto central de processamento de mensagens para o Orquestrador.
        Ele lida com novas requisições e com respostas de outros agentes.
        """
        if message.message_type == MessageType.REQUEST:
            await self._handle_new_request(message)
        elif message.message_type == MessageType.RESPONSE:
            await self._handle_response(message)

    async def _handle_new_request(self, message: AgentMessage):
        """ Lida com uma nova requisição de tarefa complexa. """
        mission_id = message.message_id
        logger.info(f"👑 [Orquestrador] Nova Missão '{mission_id}' recebida de '{message.sender_id}'.")

        self.pending_missions[mission_id] = {
            "original_request": message,
            "status": "planning",
            "plan": [],
            "current_step": 0
        }

        # PASSO 1: Delegar a criação do plano para o AIAnalyzerAgent.
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
        """ Lida com respostas do AIAnalyzer (plano) ou de agentes especialistas (resultado do passo). """
        if not message.callback_id:
            return

        # Cenário 1: É a resposta do AIAnalyzer com o plano de execução.
        if message.callback_id in self.pending_missions:
            mission_id = message.callback_id
            await self._handle_plan_response(mission_id, message)
        
        # Cenário 2: É a resposta de um agente especialista sobre um passo da execução.
        elif "_step_" in message.callback_id:
            mission_id, step_str = message.callback_id.rsplit("_step_", 1)
            if mission_id in self.pending_missions:
                await self._handle_step_response(mission_id, int(step_str), message)

    async def _handle_plan_response(self, mission_id: str, plan_message: AgentMessage):
        """ Processa o plano de execução recebido do AIAnalyzerAgent. """
        mission = self.pending_missions[mission_id]
        logger.info(f"👑 [Orquestrador] Plano para a Missão '{mission_id}' recebido de 'ai_analyzer_001'.")

        plan = plan_message.content.get("plan")
        if plan_message.content.get("status") != "success" or not isinstance(plan, list) or not plan:
            error_msg = f"Falha ao criar plano para Missão '{mission_id}'. Motivo: {plan_message.content.get('message', 'Plano inválido ou vazio.')}"
            logger.error(error_msg)
            await self._abort_mission(mission_id, error_msg)
            return

        mission["plan"] = plan
        mission["status"] = "executing"
        logger.info(f"👑 [Orquestrador] Plano para a Missão '{mission_id}' validado. Iniciando execução com {len(plan)} passos.")
        await self._execute_mission_step(mission_id)

    async def _handle_step_response(self, mission_id: str, step_index: int, step_message: AgentMessage):
        """ Processa a resposta de um agente especialista após executar um passo. """
        mission = self.pending_missions[mission_id]
        if mission["current_step"] != step_index:
            logger.warning(f"Recebida resposta para o passo {step_index} fora de ordem na missão {mission_id}.")
            return

        if step_message.content.get("status") != "success":
            error_msg = f"Falha no passo {step_index + 1} da Missão '{mission_id}'. Agente '{step_message.sender_id}' reportou erro: {step_message.content.get('message', 'Erro desconhecido.')}"
            logger.error(error_msg)
            await self._abort_mission(mission_id, error_msg)
            return
        
        logger.info(f"✅ [Orquestrador] Passo {step_index + 1}/{len(mission['plan'])} da Missão '{mission_id}' concluído com sucesso por '{step_message.sender_id}'.")
        mission["current_step"] += 1
        await self._execute_mission_step(mission_id)
        
    async def _execute_mission_step(self, mission_id: str):
        """ Executa o passo atual de uma missão. """
        if mission_id not in self.pending_missions:
            return

        mission = self.pending_missions[mission_id]
        
        # Se todos os passos foram concluídos
        if mission["current_step"] >= len(mission["plan"]):
            success_msg = f"Missão '{mission_id}' concluída com sucesso!"
            logger.info(f"🎉 [Orquestrador] {success_msg}")
            # Notificar o solicitante original
            await self.publish_response(mission["original_request"], {"status": "success", "message": success_msg})
            del self.pending_missions[mission_id]
            return

        # Executar o próximo passo
        step = mission["plan"][mission["current_step"]]
        step_index = mission["current_step"]
        
        try:
            target_agent = step["agent"]
            task_content = step["task"]
        except KeyError as e:
            error_msg = f"Passo {step_index + 1} do plano para a Missão '{mission_id}' é malformado. Chave ausente: {e}"
            await self._abort_mission(mission_id, error_msg)
            return

        logger.info(f"▶️ [Orquestrador] Executando passo {step_index + 1}/{len(mission['plan'])} da Missão '{mission_id}': Delegando para '{target_agent}'.")
        
        step_request = self.create_message(
            recipient_id=target_agent,
            message_type=MessageType.REQUEST,
            content=task_content,
            priority=Priority.NORMAL,
            callback_id=f"{mission_id}_step_{step_index}"
        )
        await self.message_bus.publish(step_request)

    async def _abort_mission(self, mission_id: str, reason: str):
        """ Cancela uma missão em andamento e notifica o solicitante. """
        logger.error(f"🛑 [Orquestrador] ABORTANDO Missão '{mission_id}'. Motivo: {reason}")
        if mission_id in self.pending_missions:
            mission = self.pending_missions[mission_id]
            await self.publish_error_response(mission["original_request"], reason)
            del self.pending_missions[mission_id]

class MetaCognitiveAgent(BaseNetworkAgent):
    """
    Agente Meta-Cognitivo - Analisa o sistema como um todo.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.META_COGNITIVE, message_bus)
        self.capabilities.append("system_analysis")
        self._analysis_task: Optional[asyncio.Task] = None
        logger.info(f"🧠 {self.agent_id} (Meta-Cognitivo) inicializado.")

    async def start_meta_cognition(self):
        """Inicia o loop de análise periódica em segundo plano."""
        if self._analysis_task is None or self._analysis_task.done():
            self._analysis_task = asyncio.create_task(self._analysis_loop())

    async def _analysis_loop(self):
        """Loop que executa a análise do sistema a cada 5 minutos."""
        logger.info(f"🧠 {self.agent_id} iniciou processos meta-cognitivos.")
        while True:
            await asyncio.sleep(300) # 5 minutos
            logger.info("[Meta-Cog] Analisando performance da rede...")
            # Aqui pode ser adicionada lógica para verificar a saúde dos agentes,
            # profundidade das filas, etc., e tomar ações se necessário.

def create_meta_cognitive_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria e retorna os agentes meta-cognitivos (Orquestrador e Meta-Cognitivo)."""
    agents: List[BaseNetworkAgent] = []
    logger.info("🧠 Criando agentes do Cérebro (Meta-Cognitivos)...")
    try:
        orchestrator = OrchestratorAgent("orchestrator_001", message_bus)
        meta_agent = MetaCognitiveAgent("metacognitive_001", message_bus)
        
        # Garante que o loop de análise do meta-agente seja iniciado
        asyncio.create_task(meta_agent.start_meta_cognition())
        
        agents.extend([orchestrator, meta_agent])
        logger.info("✅ Cérebro do sistema criado com sucesso.")
    except Exception as e:
        logger.critical(f"❌ Erro CRÍTICO criando agentes Meta-Cognitivos: {e}", exc_info=True)
    return agents
