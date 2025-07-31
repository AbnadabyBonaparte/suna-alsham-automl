#!/usr/bin/env python3
"""
Módulo Carregador de Agentes – SUNA-ALSHAM

Versão Final Viva – Carrega todos os agentes centrais e de domínio
para máxima robustez e compatibilidade com entrada universal.
"""

import logging
from typing import Any, Dict, List

# 🔧 Garante path correto para imports
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root.resolve()))

# 🔗 Importa as fábricas de agentes
from suna_alsham_core.meta_cognitive_agents import create_meta_cognitive_agents
from suna_alsham_core.ai_powered_agents import create_ai_agents
from suna_alsham_core.web_search_agent import create_web_search_agent
from suna_alsham_core.notification_agent import create_notification_agent
from suna_alsham_core.api_gateway_agent import create_api_gateway_agent

# Outros módulos centrais
from suna_alsham_core.core_agents_v3 import create_core_agents_v3
from suna_alsham_core.specialized_agents import create_specialized_agents
from suna_alsham_core.system_agents import create_system_agents
from suna_alsham_core.service_agents import create_service_agents
from suna_alsham_core.performance_monitor_agent import create_performance_monitor_agent

# Módulos de domínio (exemplo)
from domain_modules.analytics.analytics_orchestrator_agent import create_analytics_agents
from domain_modules.sales.sales_orchestrator_agent import create_sales_agents
from domain_modules.social_media.social_media_orchestrator_agent import create_social_media_agents
from domain_modules.suporte.support_orchestrator_agent import create_suporte_agents

logger = logging.getLogger(__name__)

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    """
    Inicializa todos os agentes do sistema.
    """
    agents_loaded = 0
    failed_modules = []

    # Todas as fábricas a serem chamadas
    agent_factories: List = [
        create_api_gateway_agent,
        create_meta_cognitive_agents,
        create_ai_agents,
        create_web_search_agent,
        create_notification_agent,
        create_core_agents_v3,
        create_specialized_agents,
        create_system_agents,
        create_service_agents,
        create_performance_monitor_agent,
        create_analytics_agents,
        create_sales_agents,
        create_social_media_agents,
        create_suporte_agents,
    ]

    logger.info("--- INICIANDO CARREGAMENTO DE AGENTES ---")

    for factory in agent_factories:
        name = factory.__name__
        logger.info(f"--> Carregando: {name}")
        try:
            agents = factory(network.message_bus)
            for agent in agents:
                network.register_agent(agent)
                agents_loaded += 1
            logger.info(f"<-- SUCESSO: {name} carregou {len(agents)} agente(s).")
        except Exception as e:
            logger.error(f"❌ ERRO em {name}: {e}", exc_info=True)
            failed_modules.append(name)

    logger.info(f"--- FIM DO CARREGAMENTO. Total: {agents_loaded} agentes ativos. ---")
    return {
        "summary": {"agents_loaded": agents_loaded, "failed_modules_count": len(failed_modules)},
        "failed_modules": failed_modules,
    }
