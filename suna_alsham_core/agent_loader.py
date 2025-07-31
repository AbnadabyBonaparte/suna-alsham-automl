#!/usr/bin/env python3
"""
Módulo Carregador de Agentes – SUNA-ALSHAM

[Versão Final Viva] – Carrega explicitamente todos os agentes centrais e de domínio
para máxima robustez e compatibilidade com entrada universal.
"""

import logging
from typing import Any, Dict, List

# 🔧 Garante que o path do projeto esteja correto para os imports
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root.resolve()))

# 🔗 Importação explícita de todas as fábricas de agentes
from suna_alsham_core.core_agents_v3 import create_core_agents_v3
from suna_alsham_core.specialized_agents import create_specialized_agents
from suna_alsham_core.ai_powered_agents import create_ai_agents
from suna_alsham_core.system_agents import create_system_agents
from suna_alsham_core.service_agents import create_service_agents
from suna_alsham_core.meta_cognitive_agents import create_meta_cognitive_agents
from suna_alsham_core.performance_monitor_agent import create_performance_monitor_agent
from suna_alsham_core.web_search_agent import create_web_search_agent
from suna_alsham_core.notification_agent import create_notification_agent
from suna_alsham_core.api_gateway_agent import create_api_gateway_agent

# ✅ Inclui todos os módulos de domínio
from domain_modules.analytics.analytics_orchestrator_agent import create_analytics_agents
from domain_modules.sales.sales_orchestrator_agent import create_sales_agents
from domain_modules.social_media.social_media_orchestrator_agent import create_social_media_agents
from domain_modules.suporte.support_orchestrator_agent import create_suporte_agents

logger = logging.getLogger(__name__)

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    """
    Inicializa todos os agentes do sistema com logs detalhados.
    Garante que todos os agentes centrais e de domínio sejam carregados.
    """
    agents_loaded = 0
    failed_modules: List[str] = []

    # Lista de todas as fábricas de agentes a serem chamadas
    agent_factories: List = [
        # Núcleo de comunicação e orquestração
        create_api_gateway_agent,
        create_meta_cognitive_agents,
        create_ai_agents,
        create_web_search_agent,
        create_notification_agent,

        # Agentes centrais do SUNA-ALSHAM
        create_core_agents_v3,
        create_specialized_agents,
        create_system_agents,
        create_service_agents,
        create_performance_monitor_agent,

        # Agentes de domínio (negócios)
        create_analytics_agents,
        create_sales_agents,
        create_social_media_agents,
        create_suporte_agents,
    ]

    logger.info("--- INICIANDO AUDITORIA DE CARREGAMENTO DE AGENTES ---")

    for factory in agent_factories:
        factory_name = factory.__name__
        logger.info(f"--> Chamando fábrica: {factory_name}")
        try:
            agents = factory(network.message_bus)
            num_created = len(agents)
            logger.info(f"<-- SUCESSO: {factory_name} carregou {num_created} agente(s).")

            for agent in agents:
                network.register_agent(agent)
                agents_loaded += 1

        except Exception as e:
            logger.error(f"❌ FALHA: {factory_name} não conseguiu carregar: {e}", exc_info=True)
            failed_modules.append(factory_name)

    logger.info(f"--- FIM DO CARREGAMENTO. Total: {agents_loaded} agentes ativos. ---")

    return {
        "summary": {
            "agents_loaded": agents_loaded,
            "failed_modules_count": len(failed_modules)
        },
        "failed_modules": failed_modules,
    }
