#!/usr/bin/env python3
"""
Módulo Carregador de Agentes – SUNA-ALSHAM

Versão Restaurada – Garante o carregamento de TODOS os agentes (≈55)
com auditoria de IDs e logs detalhados.
"""

import logging
from typing import Any, Dict, List

# 🔧 Garante path correto para imports
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root.resolve()))

# 🔗 Importa as fábricas de agentes centrais
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

# Módulos de domínio
from domain_modules.analytics.analytics_orchestrator_agent import create_analytics_agents
from domain_modules.sales.sales_orchestrator_agent import create_sales_agents
from domain_modules.social_media.social_media_orchestrator_agent import create_social_media_agents
from domain_modules.suporte.support_orchestrator_agent import create_suporte_agents

logger = logging.getLogger(__name__)

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    """
    Inicializa todos os agentes do sistema e retorna um relatório detalhado.
    """
    agents_loaded = 0
    failed_modules = []
    all_agent_ids: List[str] = []

    # ✅ Lista completa das fábricas a serem carregadas
    agent_factories: List = [
        create_api_gateway_agent,         # 1
        create_meta_cognitive_agents,     # 1+
        create_ai_agents,                 # 1
        create_web_search_agent,          # 1
        create_notification_agent,        # 1
        create_core_agents_v3,            # 5
        create_specialized_agents,        # 2
        create_system_agents,             # 3+
        create_service_agents,            # 2+
        create_performance_monitor_agent, # 1
        create_analytics_agents,          # 5
        create_sales_agents,              # 6
        create_social_media_agents,       # 5
        create_suporte_agents,            # 5
    ]

    logger.info("🔒 --- INICIANDO CARREGAMENTO DE AGENTES ---")

    for factory in agent_factories:
        name = factory.__name__
        logger.info(f"--> Chamando fábrica: {name}")
        try:
            agents = factory(network.message_bus)
            for agent in agents:
                network.register_agent(agent)
                agents_loaded += 1
                all_agent_ids.append(agent.agent_id)
            logger.info(f"<-- SUCESSO: {name} criou {len(agents)} agente(s).")
        except Exception as e:
            logger.error(f"❌ ERRO em {name}: {e}", exc_info=True)
            failed_modules.append(name)

    # ✅ Log detalhado de todos os IDs carregados
    logger.info(f"📋 Auditoria de agentes: {all_agent_ids}")
    logger.info(f"🔒 --- FIM DO CARREGAMENTO. Total: {agents_loaded} agentes ativos. ---")

    return {
        "summary": {
            "agents_loaded": agents_loaded,
            "failed_modules_count": len(failed_modules)
        },
        "failed_modules": failed_modules,
        "loaded_agent_ids": all_agent_ids,
    }
