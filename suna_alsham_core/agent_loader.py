#!/usr/bin/env python3
"""
Módulo Carregador de Agentes - SUNA-ALSHAM

[Versão Final] - Utiliza carregamento explícito e força o sys.path para robustez.
"""
import logging
from typing import Any, Dict, List

# --- INÍCIO DA CORREÇÃO "FORÇA BRUTA" ---
import sys
from pathlib import Path
# Esta linha força a adição da pasta raiz do projeto (que contém 'suna_alsham_core'
# e 'domain_modules') ao "mapa" do Python.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root.resolve()))
# --- FIM DA CORREÇÃO ---


# --- CARREGAMENTO EXPLÍCITO ---
# Importamos diretamente cada função de fábrica de agentes.
# Agora, com o path corrigido acima, estes imports devem funcionar.

# Módulos do Núcleo
# NOTA: Se você tiver mais arquivos "create_..._agents" no core, adicione os imports aqui.
# Por enquanto, vamos assumir que o principal é o core_agents_v3
from suna_alsham_core.core_agents_v3 import create_core_agents_v3

# Módulos de Domínio
from domain_modules.analytics.analytics_orchestrator_agent import create_analytics_agents
from domain_modules.sales.sales_orchestrator_agent import create_sales_agents
from domain_modules.social_media.social_media_orchestrator_agent import create_social_media_agents


logger = logging.getLogger(__name__)

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    """
    Inicializa todos os agentes do sistema de forma explícita.
    """
    agents_loaded = 0
    failed_modules = []
    
    # Lista explícita de todas as funções de fábrica a serem chamadas
    agent_factories = {
        "core": [create_core_agents_v3], # Adicione outras do núcleo aqui se necessário
        "domain": [create_analytics_agents, create_sales_agents, create_social_media_agents],
    }

    # Carrega Agentes do Núcleo
    logger.info("Carregando agentes do Núcleo SUNA-ALSHAM...")
    for factory in agent_factories["core"]:
        try:
            agents = factory(network.message_bus)
            for agent in agents:
                network.register_agent(agent)
                agents_loaded += 1
        except Exception as e:
            logger.error(f"Falha ao carregar agentes da fábrica '{factory.__name__}': {e}", exc_info=True)
            failed_modules.append(factory.__name__)

    # Carrega Agentes de Domínio
    logger.info("Carregando agentes de Domínio ALSHAM GLOBAL...")
    for factory in agent_factories["domain"]:
        try:
            agents = factory(network.message_bus)
            for agent in agents:
                network.register_agent(agent)
                agents_loaded += 1
        except Exception as e:
            logger.error(f"Falha ao carregar agentes da fábrica '{factory.__name__}': {e}", exc_info=True)
            failed_modules.append(factory.__name__)
            
    logger.info(f"Carregamento de agentes concluído. Total: {agents_loaded} agentes carregados.")
    return {
        "summary": {"agents_loaded": agents_loaded, "failed_modules_count": len(failed_modules)},
        "failed_modules": failed_modules,
    }
