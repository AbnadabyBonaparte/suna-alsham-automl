#!/usr/bin/env python3
"""
Módulo Carregador de Agentes - SUNA-ALSHAM
"""
import logging
from typing import Any, Dict, List

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root.resolve()))

from suna_alsham_core.core_agents_v3 import create_core_agents_v3
from domain_modules.analytics.analytics_orchestrator_agent import create_analytics_agents
from domain_modules.sales.sales_orchestrator_agent import create_sales_agents
from domain_modules.social_media.social_media_orchestrator_agent import create_social_media_agents

logger = logging.getLogger(__name__)

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    agents_loaded = 0
    failed_modules = []
    
    agent_factories = {
        "core": [create_core_agents_v3],
        "domain": [create_analytics_agents, create_sales_agents, create_social_media_agents],
    }

    logger.info("Carregando agentes do Núcleo SUNA-ALSHAM...")
    for factory in agent_factories["core"]:
        try:
            agents = factory(network.message_bus)
            for agent in agents:
                network.register_agent(agent)
                agents_loaded += 1
        except Exception as e:
            failed_modules.append(factory.__name__)
            logger.error(f"Falha ao carregar agentes da fábrica '{factory.__name__}': {e}", exc_info=True)

    logger.info("Carregando agentes de Domínio ALSHAM GLOBAL...")
    for factory in agent_factories["domain"]:
        try:
            agents = factory(network.message_bus)
            for agent in agents:
                network.register_agent(agent)
                agents_loaded += 1
        except Exception as e:
            failed_modules.append(factory.__name__)
            logger.error(f"Falha ao carregar agentes da fábrica '{factory.__name__}': {e}", exc_info=True)
            
    logger.info(f"Carregamento de agentes concluído. Total: {agents_loaded} agentes carregados.")
    return {
        "summary": {"agents_loaded": agents_loaded, "failed_modules_count": len(failed_modules)},
        "failed_modules": failed_modules,
    }
