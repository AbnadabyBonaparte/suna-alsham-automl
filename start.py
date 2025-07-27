#!/usr/bin/env python3
"""
Módulo Principal do Sistema SUNA-ALSHAM v2.0

Este módulo define a classe principal que orquestra a inicialização e o estado
geral da rede de agentes.
"""

import logging
import time
from typing import Dict, Any, List

# Imports corrigidos para a nova estrutura
from suna_alsham_core.multi_agent_network import MultiAgentNetwork
from suna_alsham_core.agent_loader import initialize_all_agents

logger = logging.getLogger(__name__)

class SUNAAlshamSystemV2:
    """A classe principal que gerencia e orquestra o sistema multi-agente."""

    def __init__(self):
        self.network = MultiAgentNetwork()
        self.all_agents: Dict[str, Any] = {}
        self.agent_categories: Dict[str, int] = {}
        self.total_agents = 0
        self.system_status = "initializing"
        self.initialized = False
        self.start_time = time.time()

    async def initialize_complete_system(self) -> bool:
        """
        Inicializa a rede e carrega todos os agentes do sistema.
        """
        try:
            logger.info("Inicializando a rede de comunicação (MessageBus)...")
            await self.network.initialize()

            logger.info("Carregando todos os 59 agentes do sistema...")
            # A função initialize_all_agents agora retorna um dicionário com os resultados
            load_result = await initialize_all_agents(self.network)
            
            self.all_agents = self.network.agents
            self.total_agents = load_result.get('summary', {}).get('agents_loaded', 0)
            self._categorize_agents()

            self.system_status = "active"
            self.initialized = True
            logger.info(f"Sistema completo inicializado com {self.total_agents} agentes.")
            return True
        except Exception as e:
            logger.critical(f"Falha catastrófica na inicialização do sistema: {e}", exc_info=True)
            self.system_status = "error"
            return False

    def _categorize_agents(self):
        """Categoriza os agentes carregados por tipo para relatórios."""
        categories = defaultdict(int)
        for agent in self.all_agents.values():
            if hasattr(agent, 'agent_type') and hasattr(agent.agent_type, 'value'):
                categories[agent.agent_type.value] += 1
        self.agent_categories = dict(categories)

    def get_uptime(self) -> float:
        """Retorna o tempo de atividade do sistema em segundos."""
        return time.time() - self.start_time

    def get_system_status(self) -> Dict[str, Any]:
        """Retorna um status detalhado do sistema."""
        return {
            "system_status": self.system_status,
            "total_agents": self.total_agents,
            "agent_categories": self.agent_categories,
            "uptime_seconds": self.get_uptime(),
            "network_metrics": self.network.get_network_status().get('message_bus_metrics', {})
        }

    async def execute_system_wide_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envia uma tarefa para ser processada pelo agente orquestrador.
        """
        if not self.initialized or "orchestrator_001" not in self.all_agents:
            return {"status": "error", "message": "Orquestrador não está disponível."}
        
        # Este método precisará ser implementado no OrchestratorAgent
        # Por enquanto, é um placeholder.
        logger.info(f"Enviando tarefa para o orquestrador: {task.get('id')}")
        return {
            "status": "submitted",
            "task_id": task.get('id'),
            "orchestration_result": {
                "execution_status": "completed_simulated"
            }
        }
