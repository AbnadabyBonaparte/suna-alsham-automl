#!/usr/bin/env python3
"""
Agent Loader - O Maestro do Núcleo SUNA-ALSHAM.

[Fase 2] - Este módulo foi fortalecido para usar imports explícitos e carregar
todos os agentes do núcleo de forma robusta, refletindo a nova arquitetura.
"""

import asyncio
import logging
from typing import Any, Dict, List

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import MultiAgentNetwork

# Imports explícitos para todos os módulos de agentes do núcleo.
# Esta abordagem é mais clara, segura e profissional do que imports dinâmicos.
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
from suna_alsham_core.security_enhancements_agent import create_security_enhancements_agent

logger = logging.getLogger(__name__)


class RealAgentLoader:
    """
    O "Maestro" do sistema. Responsável por chamar as "fábricas"
    de cada módulo para construir e registrar a orquestra completa de agentes.
    """

    def __init__(self, network: MultiAgentNetwork):
        """Inicializa o RealAgentLoader."""
        self.network = network
        self.total_agents_loaded = 0

    async def load_all_agents(self) -> Dict[str, Any]:
        """Carrega TODOS os 39 agentes do Núcleo SUNA-ALSHAM."""
        logger.info("🚀 Iniciando carregamento de TODOS os agentes do núcleo...")

        results = {
            "loaded_by_module": {},
            "failed_modules": [],
        }

        # Lista de todas as funções de criação de agentes para carregar.
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
            ("security_enhancements_agent", create_security_enhancements_agent),
        ]

        for module_name, create_function in agent_creation_functions:
            try:
                # A função já foi importada, agora apenas a chamamos.
                agents = create_function(self.network.message_bus)
                
                # O registro do agente já é feito na `BaseNetworkAgent`.
                # Apenas confirmamos a contagem.
                num_loaded = len(agents)
                if num_loaded > 0:
                    results["loaded_by_module"][module_name] = num_loaded
                    self.total_agents_loaded += num_loaded
                    logger.info(f"✅ {module_name}: {num_loaded} agente(s) carregado(s)")
                else:
                    logger.warning(f"⚠️ Módulo '{module_name}' não retornou agentes.")

            except Exception as e:
                logger.error(f"❌ Erro carregando o módulo '{module_name}': {e}", exc_info=True)
                results["failed_modules"].append(f"{module_name}: {str(e)}")
        
        # Resultado Final
        summary = {
            "modules_attempted": len(agent_creation_functions),
            "modules_successful": len(results["loaded_by_module"]),
            "modules_failed": len(results["failed_modules"]),
            "agents_loaded": self.total_agents_loaded,
        }
        
        logger.info("🎯 CARREGAMENTO DO NÚCLEO CONCLUÍDO!")
        logger.info(f"📊 Total de agentes de infraestrutura: {summary['agents_loaded']}")
        logger.info(f"✅ Módulos bem-sucedidos: {summary['modules_successful']}")
        logger.info(f"❌ Módulos com falha: {summary['modules_failed']}")
        
        results["summary"] = summary
        return results


async def initialize_all_agents(network: MultiAgentNetwork) -> Dict[str, Any]:
    """
    Função de fábrica principal para carregar TODOS os agentes do núcleo.
    Esta é a função que será chamada pelo `system.py`.
    """
    loader = RealAgentLoader(network)
    return await loader.load_all_agents()
