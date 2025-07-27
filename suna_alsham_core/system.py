#!/usr/bin/env python3
"""
Módulo Principal do Sistema SUNA-ALSHAM v2.0

[Fase 2] - Fortalecido com melhor tratamento de erros na inicialização
e relatórios de status mais detalhados.
"""

import asyncio
import logging
import time
from collections import defaultdict
from typing import Any, Dict, List

# Imports corrigidos para a nova estrutura
from suna_alsham_core.multi_agent_network import MultiAgentNetwork
from suna_alsham_core.agent_loader import initialize_all_agents

logger = logging.getLogger(__name__)

class SUNAAlshamSystemV2:
    """A classe principal que gerencia e orquestra o sistema multi-agente."""

    def __init__(self):
        """Inicializa o sistema."""
        self.network = MultiAgentNetwork()
        self.all_agents: Dict[str, Any] = {}
        self.agent_categories: Dict[str, int] = defaultdict(int)
        self.total_agents = 0
        self.system_status = "initializing"
        self.initialized = False
        self.start_time = time.time()
        self.failed_modules: List[str] = [] # Adicionado para rastrear falhas

    async def initialize_complete_system(self) -> bool:
        """
        Inicializa a rede e carrega todos os agentes do sistema de forma robusta.
        """
        try:
            logger.info("Inicializando a rede de comunicação (MessageBus)...")
            # Na Fase 2, o MessageBus agora tem um método start() explícito
            await self.network.message_bus.start()

            logger.info("Carregando todos os 39 agentes do núcleo...")
            load_result = await initialize_all_agents(self.network)
            
            self.all_agents = self.network.agents
            self.total_agents = load_result.get("summary", {}).get("agents_loaded", 0)
            self.failed_modules = load_result.get("failed_modules", [])
            self._categorize_agents()

            if self.failed_modules:
                logger.warning(f"{len(self.failed_modules)} módulos de agentes falharam ao carregar. Sistema em modo degradado.")
                self.system_status = "degraded"
            else:
                self.system_status = "active"
                
            self.initialized = True
            logger.info(f"Sistema completo inicializado. Status: {self.system_status.upper()}. {self.total_agents} agentes ativos.")
            return True
            
        except Exception as e:
            logger.critical(f"Falha catastrófica na inicialização do sistema: {e}", exc_info=True)
            self.system_status = "error"
            return False

    def _categorize_agents(self):
        """Categoriza os agentes carregados por tipo para relatórios."""
        for agent in self.all_agents.values():
            if hasattr(agent, 'agent_type') and hasattr(agent.agent_type, 'value'):
                self.agent_categories[agent.agent_type.value] += 1

    def get_uptime(self) -> float:
        """Retorna o tempo de atividade do sistema em segundos."""
        return time.time() - self.start_time

    def get_system_status(self) -> Dict[str, Any]:
        """Retorna um status detalhado e enriquecido do sistema."""
        network_status = self.network.get_network_status()
        return {
            "system_status": self.system_status,
            "total_agents": self.total_agents,
            "active_agents": network_status.get("active_agents", 0),
            "agent_categories": dict(self.agent_categories),
            "uptime_seconds": self.get_uptime(),
            "failed_modules": self.failed_modules,
            "network_metrics": network_status.get("message_bus_metrics", {})
        }

    async def execute_system_wide_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Envia uma tarefa para o orquestrador e aguarda uma resposta.
        """
        if not self.initialized or "orchestrator_001" not in self.all_agents:
            return {"status": "error", "message": "Orquestrador não está disponível."}
        
        orchestrator = self.all_agents["orchestrator_001"]
        
        try:
            logger.info(f"Enviando tarefa '{task.get('id')}' para o orquestrador e aguardando resposta...")
            response_message = await orchestrator.send_request_and_wait(
                recipient_id="orchestrator_001",
                content={"request_type": "submit_task", "task": task}
            )
            return response_message.content

        except TimeoutError:
            logger.error(f"Timeout ao aguardar resposta do orquestrador para a tarefa {task.get('id')}")
            return {"status": "error", "message": "Timeout: O orquestrador não respondeu a tempo."}
        except Exception as e:
            logger.error(f"Erro ao executar tarefa no sistema: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}
