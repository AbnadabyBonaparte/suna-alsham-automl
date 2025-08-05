#!/usr/bin/env python3
"""
Módulo Carregador de Agentes - SUNA-ALSHAM

[Versão Final de Produção] - Carrega explicitamente TODOS os agentes do
núcleo e dos domínios para máxima robustez e funcionalidade completa.
"""
import logging
from typing import Any, Dict, List

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root.resolve()))

# --- IMPORTAÇÃO DE TODAS AS FÁBRICAS DE AGENTES ---
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
from suna_alsham_core.structure_analyzer_agent import create_structure_analyzer_agents

# --- DOMÍNIOS ---
from domain_modules.analytics.analytics_orchestrator_agent import create_analytics_agents
from domain_modules.sales.sales_orchestrator_agent import create_sales_agents
from domain_modules.social_media.social_media_orchestrator_agent import create_social_media_agents
from domain_modules.suporte.support_orchestrator_agent import create_suporte_agents

logger = logging.getLogger(__name__)

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    """Inicializa todos os agentes do sistema de forma explícita."""
    agents_loaded = 0
    failed_modules = []

    # CONFIGURAÇÃO CORRETA DAS FACTORY FUNCTIONS COM PARÂMETROS
    agent_factories_config = [
        # Factories que recebem message_bus
        {"factory": create_core_agents_v3, "params": [network.message_bus]},
        {"factory": create_specialized_agents, "params": [network.message_bus]},
        {"factory": create_ai_agents, "params": [network.message_bus]},
        {"factory": create_system_agents, "params": [network.message_bus]},
        {"factory": create_service_agents, "params": [network.message_bus]},
        {"factory": create_meta_cognitive_agents, "params": [network.message_bus]},
        
        # Factories que NÃO recebem parâmetros
        {"factory": create_code_analyzer_agent, "params": []},
        {"factory": create_performance_monitor_agent, "params": []},
        {"factory": create_computer_control_agent, "params": []},
        {"factory": create_web_search_agent, "params": []},
        {"factory": create_code_corrector_agent, "params": []},
        {"factory": create_debug_master_agent, "params": []},
        {"factory": create_security_guardian_agent, "params": []},
        {"factory": create_validation_sentinel_agent, "params": []},
        {"factory": create_disaster_recovery_agent, "params": []},
        {"factory": create_backup_agent, "params": []},
        {"factory": create_database_agent, "params": []},
        {"factory": create_logging_agent, "params": []},
        {"factory": create_api_gateway_agent, "params": []},
        {"factory": create_notification_agent, "params": []},
        {"factory": create_deployment_agent, "params": []},
        {"factory": create_testing_agent, "params": []},
        {"factory": create_visualization_agent, "params": []},
        {"factory": create_security_enhancements_agent, "params": []},
        {"factory": create_evolution_engine_agents, "params": []},
        {"factory": create_structure_analyzer_agents, "params": []},
        
        # Factories de domínio (recebem message_bus)
        {"factory": create_analytics_agents, "params": [network.message_bus]},
        {"factory": create_sales_agents, "params": [network.message_bus]},
        {"factory": create_social_media_agents, "params": [network.message_bus]},
        {"factory": create_suporte_agents, "params": [network.message_bus]},
    ]

    logger.info("--- INICIANDO AUDITORIA DE CARREGAMENTO DE AGENTES ---")

    for config in agent_factories_config:
        factory = config["factory"]
        params = config["params"]
        factory_name = factory.__name__
        
        logger.info(f"--> Chamando fábrica: {factory_name}...")
        try:
            # Chamar factory com parâmetros corretos
            if params:
                agents = factory(*params)
            else:
                agents = factory()
                
            if not isinstance(agents, list):
                agents = []
                
            num_created = len(agents)
            
            # Registrar cada agente
            for agent in agents:
                try:
                    network.register_agent(agent)
                    agents_loaded += 1
                    logger.info(f"    ✅ Agente registrado: {getattr(agent, 'agent_id', 'unknown')}")
                except Exception as reg_error:
                    logger.error(f"    ❌ Erro ao registrar agente: {reg_error}")
                    
            logger.info(f"<-- SUCESSO: {factory_name} retornou {num_created} agente(s).")
            
        except Exception as e:
            logger.error(f"<-- FALHA: {factory_name} falhou: {e}", exc_info=True)
            failed_modules.append(factory_name)

    logger.info(f"--- FIM DA AUDITORIA. Total: {agents_loaded} agentes carregados. ---")
    
    # Log detalhado dos resultados
    if failed_modules:
        logger.error(f"❌ FACTORY FUNCTIONS QUE FALHARAM ({len(failed_modules)}):")
        for failed in failed_modules:
            logger.error(f"    - {failed}")
    
    logger.info(f"✅ FACTORY FUNCTIONS EXECUTADAS COM SUCESSO: {len(agent_factories_config) - len(failed_modules)}")
    logger.info(f"📊 TOTAL DE AGENTES CARREGADOS: {agents_loaded}")
    
    return {
        "summary": {"agents_loaded": agents_loaded, "failed_modules_count": len(failed_modules)},
        "failed_modules": failed_modules,
        "total_factories": len(agent_factories_config),
        "successful_factories": len(agent_factories_config) - len(failed_modules)
    }
