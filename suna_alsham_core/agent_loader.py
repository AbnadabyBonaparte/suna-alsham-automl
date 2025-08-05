#!/usr/bin/env python3
"""
Módulo Carregador de Agentes - SUNA-ALSHAM

[Versão Corrigida Completa] - Carrega todos os 56 agentes do sistema
CORREÇÃO: Adicionado o 56º agente à configuração de carregamento.
"""
import logging
from typing import Any, Dict, List
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root.resolve()))

logger = logging.getLogger(__name__)

async def initialize_all_agents(network) -> Dict[str, Any]:
    """
    Inicializa todos os agentes do sistema - CONFIGURAÇÃO COMPLETA DOS 56 AGENTES.
    
    Args:
        network: Instância de MultiAgentNetwork para registrar os agentes
    
    Returns:
        Dict com resumo do carregamento
    """
    agents_loaded = 0
    failed_modules = []

    # CONFIGURAÇÃO COMPLETA - TODOS OS 56 AGENTES
    agent_factories_config = [
        # ===== NÚCLEO SUNA-ALSHAM (35 AGENTES) =====
        
        # Arquivo: core_agents_v3.py (5 Agentes)
        {"factory_path": "suna_alsham_core.core_agents_v3", "factory_name": "create_core_agents_v3"},
        
        # Arquivo: specialized_agents.py (2 Agentes)
        {"factory_path": "suna_alsham_core.specialized_agents", "factory_name": "create_specialized_agents"},
        
        # Arquivo: system_agents.py (3 Agentes)
        {"factory_path": "suna_alsham_core.system_agents", "factory_name": "create_system_agents"},
        
        # Arquivo: service_agents.py (2 Agentes)
        {"factory_path": "suna_alsham_core.service_agents", "factory_name": "create_service_agents"},
        
        # Arquivo: meta_cognitive_agents.py (2 Agentes)
        {"factory_path": "suna_alsham_core.meta_cognitive_agents", "factory_name": "create_meta_cognitive_agents"},
        
        # Arquivo: ai_powered_agents.py (1 Agente)
        {"factory_path": "suna_alsham_core.ai_powered_agents", "factory_name": "create_ai_agents"},
        
        # Arquivo: api_gateway_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.api_gateway_agent", "factory_name": "create_api_gateway_agent"},
        
        # Arquivo: backup_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.backup_agent", "factory_name": "create_backup_agent"},
        
        # Arquivo: code_analyzer_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.code_analyzer_agent", "factory_name": "create_code_analyzer_agent"},
        
        # Arquivo: code_corrector_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.code_corrector_agent", "factory_name": "create_code_corrector_agent"},
        
        # Arquivo: computer_control_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.computer_control_agent", "factory_name": "create_computer_control_agent"},
        
        # Arquivo: database_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.database_agent", "factory_name": "create_database_agent"},
        
        # Arquivo: debug_agent_creation.py (1 Agente)
        {"factory_path": "suna_alsham_core.debug_agent_creation", "factory_name": "create_debug_master_agent"},
        
        # Arquivo: deployment_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.deployment_agent", "factory_name": "create_deployment_agent"},
        
        # Arquivo: disaster_recovery_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.disaster_recovery_agent", "factory_name": "create_disaster_recovery_agent"},
        
        # Arquivo: logging_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.logging_agent", "factory_name": "create_logging_agent"},
        
        # Arquivo: notification_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.notification_agent", "factory_name": "create_notification_agent"},
        
        # Arquivo: performance_monitor_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.performance_monitor_agent", "factory_name": "create_performance_monitor_agent"},
        
        # Arquivo: real_evolution_engine.py (1 Agente)
        {"factory_path": "suna_alsham_core.real_evolution_engine", "factory_name": "create_evolution_engine_agent"},

        # ====> NOVA LINHA ADICIONADA AQUI <====
        # Arquivo: resource_manager_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.resource_manager_agent", "factory_name": "create_resource_manager_agent"},
        
        # Arquivo: security_enhancements_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.security_enhancements_agent", "factory_name": "create_security_enhancements_agent"},
        
        # Arquivo: security_guardian_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.security_guardian_agent", "factory_name": "create_security_guardian_agent"},
        
        # Arquivo: testing_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.testing_agent", "factory_name": "create_testing_agent"},
        
        # Arquivo: validation_sentinel_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.validation_sentinel_agent", "factory_name": "create_validation_sentinel_agent"},
        
        # Arquivo: visualization_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.visualization_agent", "factory_name": "create_visualization_agent"},
        
        # Arquivo: web_search_agent.py (1 Agente)
        {"factory_path": "suna_alsham_core.web_search_agent", "factory_name": "create_web_search_agent"},
        
        # ===== MÓDULOS DE DOMÍNIO ALSHAM GLOBAL (21 AGENTES) =====
        
        # Módulo: Analytics (5 Agentes)
        {"factory_path": "domain_modules.analytics.analytics_orchestrator_agent", "factory_name": "create_analytics_agents"},
        
        # Módulo: Vendas (6 Agentes)
        {"factory_path": "domain_modules.sales.sales_orchestrator_agent", "factory_name": "create_sales_agents"},
        
        # Módulo: Mídias Sociais (5 Agentes)
        {"factory_path": "domain_modules.social_media.social_media_orchestrator_agent", "factory_name": "create_social_media_agents"},
        
        # Módulo: Suporte (5 Agentes)
        {"factory_path": "domain_modules.suporte.support_orchestrator_agent", "factory_name": "create_suporte_agents"},
    ]

    logger.info("--- INICIANDO CARREGAMENTO COMPLETO DE AGENTES (56 ESPERADOS) ---")

    for config in agent_factories_config:
        factory_path = config["factory_path"]
        factory_name = config["factory_name"]
        
        logger.info(f"--> Carregando módulo: {factory_path}.{factory_name}...")
        try:
            # Import dinâmico seguro
            module = __import__(factory_path, fromlist=[factory_name])
            factory = getattr(module, factory_name)
            
            # Chamar factory com message_bus do network
            if hasattr(network, 'message_bus'):
                agents = factory(network.message_bus)
            else:
                # Fallback se a estrutura for diferente
                agents = factory(network)
            
            if not isinstance(agents, list):
                # Se a factory não retornar uma lista (p.ex. erro silencioso), trata como lista vazia
                agents = []
                
            num_created = len(agents)
            
            # Registrar cada agente no network
            for agent in agents:
                try:
                    network.register_agent(agent)
                    agents_loaded += 1
                    logger.info(f"    ✅ Agente registrado: {getattr(agent, 'agent_id', 'unknown')}")
                except Exception as reg_error:
                    logger.error(f"    ❌ Erro ao registrar agente: {reg_error}")
                    
            logger.info(f"<-- SUCESSO: {factory_name} criou {num_created} agente(s).")
            
        except ImportError as e:
            logger.error(f"<-- IMPORT ERROR: {factory_path} não encontrado: {e}")
            failed_modules.append(f"{factory_path} (ImportError)")
        except AttributeError as e:
            logger.error(f"<-- ATTR ERROR: Função {factory_name} não encontrada: {e}")
            failed_modules.append(f"{factory_path}.{factory_name} (AttributeError)")
        except Exception as e:
            logger.error(f"<-- FALHA: {factory_path}.{factory_name} falhou: {e}", exc_info=True)
            failed_modules.append(f"{factory_path}.{factory_name}")

    logger.info(f"--- FIM DO CARREGAMENTO. Total: {agents_loaded} agentes carregados. ---")
    
    # Log detalhado dos resultados
    if failed_modules:
        logger.error(f"❌ MÓDULOS QUE FALHARAM ({len(failed_modules)}):")
        for failed in failed_modules:
            logger.error(f"    - {failed}")
    
    logger.info(f"✅ MÓDULOS EXECUTADOS COM SUCESSO: {len(agent_factories_config) - len(failed_modules)}")
    logger.info(f"📊 TOTAL DE AGENTES CARREGADOS: {agents_loaded}")
    
    return {
        "summary": {
            "agents_loaded": agents_loaded, 
            "expected_agents": len(agent_factories_config), # Ajustado para ser dinâmico
            "failed_modules_count": len(failed_modules)
        },
        "failed_modules": failed_modules,
        "total_factories": len(agent_factories_config),
        "successful_factories": len(agent_factories_config) - len(failed_modules),
        "agents_loaded_count": agents_loaded
    }
