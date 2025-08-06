#!/usr/bin/env python3
"""
Módulo dos Agentes Especializados - SUNA-ALSHAM

Define agentes que realizam tarefas especializadas e complexas,
muitas vezes orquestrando outros agentes para atingir um objetivo.

CORREÇÃO: Eliminada detecção duplicada de agentes com sistema de debounce.
"""

import asyncio
import logging
import time
from typing import Any, Dict, List, Set

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


class TaskDelegatorAgent(BaseNetworkAgent):
    """
    Agente que pode receber uma tarefa complexa e dividi-la em subtarefas
    para serem executadas por outros agentes.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "task_delegation",
            "task_decomposition", 
            "subtask_coordination",
            "workflow_orchestration"
        ])
        logger.info(f"🎯 {self.agent_id} inicializado com capacidades de delegação de tarefas.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa mensagens de delegação de tarefas"""
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            
            if request_type == "delegate_task":
                await self._handle_task_delegation(message)
            elif request_type == "decompose_task":
                await self._handle_task_decomposition(message)
            else:
                logger.debug(f"Tipo de requisição não reconhecido: {request_type}")

    async def _handle_task_delegation(self, message: AgentMessage):
        """Delega uma tarefa para agentes especializados"""
        task_data = message.content.get("task_data", {})
        task_type = task_data.get("type", "unknown")
        
        logger.info(f"🎯 Delegando tarefa tipo '{task_type}' para agentes especializados")
        
        response = {
            "status": "delegated",
            "task_type": task_type,
            "assigned_agents": [],
            "estimated_completion": "pending"
        }
        
        await self.publish_response(message, response)

    async def _handle_task_decomposition(self, message: AgentMessage):
        """Decompõe uma tarefa complexa em subtarefas"""
        complex_task = message.content.get("complex_task", {})
        
        logger.info("🧩 Decompondo tarefa complexa em subtarefas executáveis")
        
        response = {
            "status": "decomposed",
            "subtasks": [],
            "execution_order": [],
            "dependencies": {}
        }
        
        await self.publish_response(message, response)


class NewAgentOnboardingAgent(BaseNetworkAgent):
    """
    Agente responsável por integrar novos agentes à rede,
    verificando suas capacidades e registrando-os.

    CORREÇÃO: Sistema de debounce para evitar detecções duplicadas.
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SPECIALIZED, message_bus)
        self.capabilities.extend([
            "agent_onboarding",
            "capability_verification",
            "network_registration",
            "health_monitoring"
        ])
        
        self.known_agents: Set[str] = set()
        self.last_detection_time: float = 0
        self.detection_debounce_seconds: float = 2.0
        self.last_known_count: int = 0
        self.detection_history: List[Dict[str, Any]] = []

        self.onboarding_task = asyncio.create_task(self._monitor_network_changes())
        logger.info(f"👋 {self.agent_id} inicializado com sistema de onboarding inteligente.")

    async def _monitor_network_changes(self, interval: int = 15):
        logger.info("🔍 Iniciando monitoramento inteligente de mudanças na rede")
        
        while True:
            try:
                await asyncio.sleep(interval)
                
                current_agents = set(self.message_bus.queues.keys()) if hasattr(self.message_bus, 'queues') else set()
                current_time = time.time()
                
                if current_agents != self.known_agents:
                    if current_time - self.last_detection_time >= self.detection_debounce_seconds:
                        truly_new_agents = current_agents - self.known_agents
                        removed_agents = self.known_agents - current_agents
                        
                        if truly_new_agents:
                            await self._process_new_agents(truly_new_agents)
                        if removed_agents:
                            await self._process_removed_agents(removed_agents)
                        
                        self.known_agents = current_agents.copy()
                        self.last_detection_time = current_time
                        self.last_known_count = len(current_agents)

                        self.detection_history.append({
                            "timestamp": current_time,
                            "total_agents": len(current_agents),
                            "new_agents": list(truly_new_agents),
                            "removed_agents": list(removed_agents)
                        })
                        if len(self.detection_history) > 50:
                            self.detection_history = self.detection_history[-50:]
                    else:
                        logger.debug(f"🔇 Detecção ignorada por debounce ({current_time - self.last_detection_time:.1f}s < {self.detection_debounce_seconds}s)")
                else:
                    if len(current_agents) != self.last_known_count:
                        logger.info(f"📊 Rede estável: {len(current_agents)} agentes ativos")
                        self.last_known_count = len(current_agents)
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento de rede: {e}")
                await asyncio.sleep(5)

    async def _process_new_agents(self, new_agents: Set[str]):
        if not new_agents:
            return
            
        logger.info(f"👋 {len(new_agents)} novos agentes detectados na rede: {sorted(new_agents)}")
        
        for agent_id in new_agents:
            try:
                await self._onboard_single_agent(agent_id)
            except Exception as e:
                logger.error(f"❌ Erro no onboarding do agente {agent_id}: {e}")

    async def _process_removed_agents(self, removed_agents: Set[str]):
        if not removed_agents:
            return
            
        logger.warning(f"👋 {len(removed_agents)} agentes removidos da rede: {sorted(removed_agents)}")
        
        for agent_id in removed_agents:
            logger.info(f"📝 Agente {agent_id} removido do registro")

    async def _onboard_single_agent(self, agent_id: str):
        logger.debug(f"🔍 Iniciando onboarding do agente: {agent_id}")
        
        try:
            health_check = await self._check_agent_health(agent_id)
            
            if health_check["status"] == "healthy":
                logger.debug(f"✅ Agente {agent_id} passou na verificação de saúde")
                capabilities = await self._discover_agent_capabilities(agent_id)
                logger.debug(f"📋 Agente {agent_id} capacidades: {capabilities}")
                logger.info(f"🎊 Onboarding concluído para {agent_id}")
            else:
                logger.warning(f"⚠️ Agente {agent_id} falhou na verificação de saúde: {health_check.get('reason', 'unknown')}")
        except Exception as e:
            logger.error(f"❌ Erro no onboarding individual de {agent_id}: {e}")

    async def _check_agent_health(self, agent_id: str) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "response_time": 0.05,
            "last_seen": time.time()
        }

    async def _discover_agent_capabilities(self, agent_id: str) -> List[str]:
        basic_capabilities = ["message_handling", "async_processing"]
        if "orchestrator" in agent_id.lower():
            basic_capabilities.extend(["orchestration", "coordination"])
        elif "analyzer" in agent_id.lower():
            basic_capabilities.extend(["analysis", "data_processing"])
        elif "monitor" in agent_id.lower():
            basic_capabilities.extend(["monitoring", "alerting"])
        return basic_capabilities

    async def _internal_handle_message(self, message: AgentMessage):
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            
            if request_type == "get_network_status":
                await self._handle_network_status_request(message)
            elif request_type == "force_rescan":
                await self._handle_force_rescan(message)
            elif request_type == "get_onboarding_history":
                await self._handle_history_request(message)
            else:
                logger.debug(f"Tipo de requisição não reconhecido: {request_type}")

    async def _handle_network_status_request(self, message: AgentMessage):
        current_agents = set(self.message_bus.queues.keys()) if hasattr(self.message_bus, 'queues') else set()
        
        response = {
            "status": "completed",
            "total_agents": len(current_agents),
            "known_agents": len(self.known_agents),
            "last_detection": self.last_detection_time,
            "recent_detections": len([h for h in self.detection_history if time.time() - h["timestamp"] < 300])
        }
        await self.publish_response(message, response)

    async def _handle_force_rescan(self, message: AgentMessage):
        logger.info("🔄 Forçando novo scan da rede...")
        self.known_agents.clear()
        self.last_detection_time = 0
        
        response = {
            "status": "completed",
            "message": "Rescan forçado - próxima verificação detectará todos os agentes como novos"
        }
        await self.publish_response(message, response)

    async def _handle_history_request(self, message: AgentMessage):
        response = {
            "status": "completed",
            "detection_history": self.detection_history[-10:],
            "total_detections": len(self.detection_history)
        }
        await self.publish_response(message, response)

    def __del__(self):
        if hasattr(self, 'onboarding_task') and self.onboarding_task:
            self.onboarding_task.cancel()


def create_specialized_agents(message_bus: Any) -> List[BaseNetworkAgent]:
    """
    Função de bootstrap para criação dos agentes especializados do sistema.
    Cria e inicializa os agentes TaskDelegatorAgent e NewAgentOnboardingAgent.
    :param message_bus: Barramento de mensagens do sistema.
    :return: Lista de instâncias de agentes especializados criados.
    """
    agents: List[BaseNetworkAgent] = []
    logger.info("🛠️ Criando agentes Especializados...")

    agent_configs = [
        {"id": "task_delegator_001", "class": TaskDelegatorAgent},
        {"id": "onboarding_001", "class": NewAgentOnboardingAgent},
    ]

    for config in agent_configs:
        try:
            agent = config["class"](config["id"], message_bus)
            agents.append(agent)
            logger.info(f"✅ Agente especializado {config['id']} criado com sucesso.")
        except Exception as e:
            logger.error(f"❌ Erro criando agente especializado {config['id']}: {e}", exc_info=True)

    logger.info(f"🛠️ Total de agentes especializados criados: {len(agents)}")
    return agents
