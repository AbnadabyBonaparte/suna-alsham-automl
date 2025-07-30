#!/usr/bin/env python3
"""
Módulo Carregador de Agentes - SUNA-ALSHAM

[Versão de Diagnóstico] - Loga o resultado de cada fábrica de agentes.
"""
import logging
from typing import Any, Dict, List

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root.resolve()))

# Adiciona explicitamente o diretório suna_alsham_core ao path
core_path = project_root / "suna_alsham_core"
if core_path.exists() and str(core_path) not in sys.path:
    sys.path.insert(0, str(core_path))

logger = logging.getLogger(__name__)
logger.info(f"Caminhos de busca Python configurados: {sys.path[:3]}...")

# --- IMPORTAÇÃO EXPLÍCITA DE TODAS AS FÁBRICAS DE AGENTES ---
try:
    # Módulos do Núcleo
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
    from suna_alsham_core.real_evolution_engine import create_evolution_engine_agents

    # Módulos de Domínio
    from domain_modules.analytics.analytics_orchestrator_agent import create_analytics_agents
    from domain_modules.sales.sales_orchestrator_agent import create_sales_agents
    from domain_modules.social_media.social_media_orchestrator_agent import create_social_media_agents
    from domain_modules.suporte.support_orchestrator_agent import create_suporte_agents # <-- MÓDULO NOVO IMPORTADO

    logger.info("✅ Todas as importações de fábricas de agentes bem-sucedidas.")
except ImportError as e:
    logger.critical(f"❌ Falha crítica na importação: {e}")

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    agents_loaded = 0
    failed_modules = []
    
    core_factories = [
        create_performance_monitor_agent, create_core_agents_v3, create_computer_control_agent,
        create_specialized_agents, create_web_search_agent, create_ai_agents, create_system_agents,
        create_service_agents, create_meta_cognitive_agents, create_code_corrector_agent,
        create_security_guardian_agent, create_security_enhancements_agent, create_testing_agent,
        create_visualization_agent, create_disaster_recovery_agent, create_debug_master_agent,
        create_code_analyzer_agent, create_validation_sentinel_agent, create_backup_agent,
        create_database_agent, create_logging_agent, create_api_gateway_agent,
        create_notification_agent, create_deployment_agent, create_evolution_engine_agents,
    ]
    
    domain_factories = [
        create_analytics_agents,
        create_sales_agents,
        create_social_media_agents,
        create_suporte_agents, # <-- MÓDULO NOVO NA LISTA DE CHAMADA
    ]

    logger.info("--- INICIANDO AUDITORIA DE CARREGAMENTO DE AGENTES ---")
    
    # ... (o resto do arquivo continua igual) ...
    # Carrega Agentes do Núcleo
    for factory in core_factories:
        factory_name = factory.__name__
        logger.info(f"--> Chamando fábrica de núcleo: {factory_name}...")
        try:
            agents = factory(network.message_bus)
            num_created = len(agents)
            logger.info(f"<-- SUCESSO: Fábrica '{factory_name}' retornou {num_created} agente(s).")
            for agent in agents:
                network.register_agent(agent)
                agents_loaded += 1
        except Exception as e:
            logger.error(f"<-- FALHA: Fábrica '{factory_name}' falhou: {e}", exc_info=True)
            failed_modules.append(factory_name)

    # Carrega Agentes de Domínio
    for factory in domain_factories:
        factory_name = factory.__name__
        logger.info(f"--> Chamando fábrica de domínio: {factory_name}...")
        try:
            agents = factory(network.message_bus)
            num_created = len(agents)
            logger.info(f"<-- SUCESSO: Fábrica '{factory_name}' retornou {num_created} agente(s).")
            for agent in agents:
                network.register_agent(agent)
                agents_loaded += 1
        except Exception as e:
            logger.error(f"<-- FALHA: Fábrica '{factory_name}' falhou: {e}", exc_info=True)
            failed_modules.append(factory_name)
            
    logger.info(f"--- FIM DA AUDITORIA. Total: {agents_loaded} agentes carregados. ---")
    return {
        "summary": {"agents_loaded": agents_loaded, "failed_modules_count": len(failed_modules)},
        "failed_modules": failed_modules,
    }
