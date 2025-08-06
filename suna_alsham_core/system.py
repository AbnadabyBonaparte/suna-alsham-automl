#!/usr/bin/env python3
"""
Sistema Principal SUNA-ALSHAM v2.1
[Versão Corrigida para eliminar importações circulares]
"""

import asyncio
import logging
import time
from collections import defaultdict
from typing import Any, Dict, List

# Importa apenas as classes essenciais do módulo de rede
from suna_alsham_core.multi_agent_network import MessageBus, BaseNetworkAgent
from suna_alsham_core.agent_loader import initialize_all_agents

logger = logging.getLogger(__name__)

class MultiAgentNetwork:
    """
    Gerencia a rede de agentes e o barramento de mensagens.
    Vive dentro de system.py para evitar importações circulares.
    """
    def __init__(self):
        self.message_bus = MessageBus()
        self.agents: Dict[str, BaseNetworkAgent] = {}

    def register_agent(self, agent: BaseNetworkAgent):
        self.agents[agent.agent_id] = agent
        logger.debug(f"Agente {agent.agent_id} registrado na rede.")

    def get_network_status(self) -> Dict[str, Any]:
        return {
            "active_agents": len(self.agents),
            "message_bus_metrics": self.message_bus.get_metrics()
        }

class SUNAAlshamSystemV2:
    """
    Classe principal que orquestra todo o sistema de agentes.
    """
    def __init__(self):
        self.network = MultiAgentNetwork()
        self.all_agents: Dict[str, Any] = {}
        self.agent_categories: Dict[str, int] = defaultdict(int)
        self.total_agents = 0
        self.system_status = "initializing"
        self.initialized = False
        self.start_time = time.time()
        self.failed_modules: List[str] = []

    async def initialize_complete_system(self) -> bool:
        try:
            logger.info("Inicializando MessageBus...")
            await self.network.message_bus.start()

            logger.info("Carregando agentes...")
            load_result = await initialize_all_agents(self.network)

            self.all_agents = self.network.agents
            self.total_agents = load_result.get("summary", {}).get("agents_loaded", 0)
            self.failed_modules = load_result.get("failed_modules", [])
            self._categorize_agents()

            if self.failed_modules:
                self.system_status = "degraded"
                logger.warning(f"{len(self.failed_modules)} módulos falharam.")
            else:
                self.system_status = "active"

            self.initialized = True
            logger.info(f"Sistema inicializado. Status: {self.system_status.upper()} - {self.total_agents} agentes ativos.")
            return True

        except Exception as e:
            logger.critical(f"Erro crítico na inicialização: {e}", exc_info=True)
            self.system_status = "error"
            return False

    def _categorize_agents(self):
        for agent in self.all_agents.values():
            if hasattr(agent, 'agent_type'):
                self.agent_categories[agent.agent_type.value] += 1

    def get_uptime(self) -> float:
        return time.time() - self.start_time

    def get_system_status(self) -> Dict[str, Any]:
        """
        Returns a detailed status report of the SUNA-ALSHAM v2.1 system, including agent counts, categories,
        uptime, failed modules, and network metrics. Handles errors robustly and logs for diagnostics.

        Returns:
            Dict[str, Any]: Dictionary with system status, agent stats, categories, uptime, failures, and metrics.
        """
        try:
            network_status = self.network.get_network_status()
            status_report = {
                "system_status": self.system_status,
                "total_agents": self.total_agents,
                "active_agents": network_status.get("active_agents", 0),
                "agent_categories": dict(self.agent_categories),
                "uptime_seconds": self.get_uptime(),
                "failed_modules": self.failed_modules,
                "network_metrics": network_status.get("message_bus_metrics", {})
            }
            logger.debug(f"[SystemStatus] Status report generated: {status_report}")
            return status_report
        except Exception as e:
            logger.error(f"Erro ao coletar system status: {e}", exc_info=True)
            return {
                "system_status": "error",
                "error": str(e),
                "uptime_seconds": self.get_uptime(),
                "failed_modules": self.failed_modules
            }
