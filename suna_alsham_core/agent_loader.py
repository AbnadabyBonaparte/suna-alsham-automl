#!/usr/bin/env python3
"""
Agent Loader REAL - Chama as funções create_*_agents() dos arquivos
Sistema completo com 39 agentes poderosos do Núcleo.
Este módulo foi refatorado para refletir a nova estrutura de diretórios.
"""

import asyncio
import logging
from typing import List, Dict, Any

# Import corrigido, apontando para a nova estrutura
from suna_alsham_core.multi_agent_network import MultiAgentNetwork

# Imports explícitos para todos os módulos de agentes do núcleo
# Esta abordagem é mais clara e robusta do que imports dinâmicos.
from suna_alsham_core.core_agents_v3 import create_core_agents_v3
from suna_alsham_core.specialized_agents import create_specialized_agents
from suna_alsham_core.ai_powered_agents import create_ai_agents
from suna_alsham_core.system_agents import create_system_agents
from suna_alsham_core.service_agents import create_service_agents
from suna_alsham_core.meta_cognitive_agents import create_meta_cognitive_agents
from suna_alsham_core.code_analyzer_agent import create_code_analyzer_agent
from suna_alsham_core.performance_monitor_agent import create_performance_monitor_agent
from suna_alsham_core.computer_control_agent import create_computer_control_agent
from suna_alsham_core.web_search_agent import create_web_search_agent
from suna_alsham_core.code_corrector_agent import create_code_corrector_agent
from suna_alsham_core.debug_agent_creation import create_debug_master_agent
from suna_alsham_core.security_guardian_agent import create_security_guardian_agent
from suna_alsham_core.validation_sentinel_agent import create_validation_sentinel_agent
from suna_alsham_core.disaster_recovery_agent import create_disaster_recovery_agent
from suna_alsham_core.backup_agent import create_backup_agent
from suna_alsham_core.database_agent import create_database_agent
from suna_alsham_core.logging_agent import create_logging_agent
from suna_alsham_core.api_gateway_agent import create_api_gateway_agent
from suna_alsham_core.notification_agent import create_notification_agent
from suna_alsham_core.deployment_agent import create_deployment_agent
from suna_alsham_core.testing_agent import create_testing_agent
from suna_alsham_core.visualization_agent import create_visualization_agent


logger = logging.getLogger(__name__)

class RealAgentLoader:
    def __init__(self, network: MultiAgentNetwork):
        self.network = network
        self.loaded_agents: Dict[str, Any] = {}
        self.total_agents = 0
        
    async def load_all_agents(self) -> Dict[str, Any]:
        """Carrega TODOS os agentes do Núcleo SUNA-ALSHAM."""
        logger.info("🚀 Iniciando carregamento REAL de TODOS os agentes do núcleo...")
        
        results = {
            "status": "in_progress",
            "loaded_by_module": {},
            "total_agents": 0,
            "failed_modules": []
        }

        # Lista de todas as funções de criação de agentes para carregar
        agent_creation_functions = [
            ("core_agents_v3", create_core_agents_v3),
            ("specialized_agents", create_specialized_agents),
            ("ai_powered_agents", create_ai_agents),
            ("system_agents", create_system_agents),
            ("service_agents", create_service_agents),
            ("meta_cognitive_agents", create_meta_cognitive_agents),
            ("code_analyzer_agent", create_code_analyzer_agent),
            ("performance_monitor_agent", create_performance_monitor_agent),
            ("computer_control_agent", create_computer_control_agent),
            ("web_search_agent", create_web_search_agent),
            ("code_corrector_agent", create_code_corrector_agent),
            ("debug_master_agent", create_debug_master_agent),
            ("security_guardian_agent", create_security_guardian_agent),
            ("validation_sentinel_agent", create_validation_sentinel_agent),
            ("disaster_recovery_agent", create_disaster_recovery_agent),
            ("backup_agent", create_backup_agent),
            ("database_agent", create_database_agent),
            ("logging_agent", create_logging_agent),
            ("api_gateway_agent", create_api_gateway_agent),
            ("notification_agent", create_notification_agent),
            ("deployment_agent", create_deployment_agent),
            ("testing_agent", create_testing_agent),
            ("visualization_agent", create_visualization_agent),
        ]

        for module_name, create_function in agent_creation_functions:
            try:
                # A função já foi importada, agora apenas a chamamos.
                agents = create_function(self.network.message_bus)
                
                # Normalizar para lista se a função retornar um único agente
                if not isinstance(agents, list):
                    agents = [agents] if agents else []
                
                await self._add_agents_to_network(agents, module_name)
                results["loaded_by_module"][module_name] = len(agents)
                logger.info(f"✅ {module_name}: {len(agents)} agente(s) carregado(s)")
            except Exception as e:
                logger.error(f"❌ Erro carregando o módulo '{module_name}': {e}", exc_info=True)
                results["failed_modules"].append(f"{module_name}: {e}")
        
        # Resultado Final
        results["total_agents"] = self.total_agents
        results["status"] = "completed"
        results["summary"] = {
            "modules_attempted": len(agent_creation_functions),
            "modules_successful": len(results["loaded_by_module"]),
            "modules_failed": len(results["failed_modules"]),
            "agents_loaded": self.total_agents
        }
        
        logger.info("🎯 CARREGAMENTO DO NÚCLEO CONCLUÍDO!")
        logger.info(f"📊 Total de agentes de infraestrutura: {self.total_agents}")
        logger.info(f"✅ Módulos bem-sucedidos: {results['summary']['modules_successful']}")
        logger.info(f"❌ Módulos com falha: {results['summary']['modules_failed']}")
        
        return results
        
    async def _add_agents_to_network(self, agents: List, module_name: str):
        """Adiciona uma lista de agentes à rede."""
        if not agents:
            logger.warning(f"⚠️ Nenhum agente retornado de '{module_name}' para adicionar.")
            return
        
        for agent in agents:
            try:
                # O registro do agente já é feito no __init__ da BaseNetworkAgent
                if hasattr(agent, 'agent_id') and agent.agent_id in self.network.agents:
                    self.loaded_agents[agent.agent_id] = agent
                    self.total_agents += 1
                    logger.info(f"   -> Agente '{agent.agent_id}' confirmado na rede.")
                else:
                    logger.warning(f"   -> ⚠️ Falha ao confirmar o registro do agente de '{module_name}'")
            except Exception as e:
                logger.error(f"   -> ❌ Erro ao adicionar agente de '{module_name}': {e}")

async def initialize_all_agents(network: MultiAgentNetwork) -> Dict[str, Any]:
    """Função principal para carregar TODOS os agentes do núcleo."""
    loader = RealAgentLoader(network)
    return await loader.load_all_agents()
