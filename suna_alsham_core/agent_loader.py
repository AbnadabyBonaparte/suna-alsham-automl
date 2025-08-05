#!/usr/bin/env python3
"""
Módulo Carregador de Agentes - SUNA-ALSHAM

[Versão Corrigida] - Carrega apenas os agentes que existem e funcionam
"""
import logging
from typing import Any, Dict, List
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root.resolve()))

logger = logging.getLogger(__name__)

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    """Inicializa todos os agentes do sistema de forma segura."""
    agents_loaded = 0
    failed_modules = []

    # CONFIGURAÇÃO APENAS DOS MÓDULOS QUE EXISTEM E FUNCIONAM
    agent_factories_config = [
        # Core agents que sabemos que existem
        {"factory_path": "suna_alsham_core.core_agents_v3", "factory_name": "create_core_agents_v3", "params": [network.message_bus]},
        
        # Domain modules que confirmamos que existem
        {"factory_path": "domain_modules.analytics.analytics_orchestrator_agent", "factory_name": "create_analytics_agents", "params": [network.message_bus]},
        {"factory_path": "domain_modules.sales.sales_orchestrator_agent", "factory_name": "create_sales_agents", "params": [network.message_bus]},
        {"factory_path": "domain_modules.social_media.social_media_orchestrator_agent", "factory_name": "create_social_media_agents", "params": [network.message_bus]},
        {"factory_path": "domain_modules.suporte.support_orchestrator_agent", "factory_name": "create_suporte_agents", "params": [network.message_bus]},
    ]

    logger.info("--- INICIANDO CARREGAMENTO SEGURO DE AGENTES ---")

    for config in agent_factories_config:
        factory_path = config["factory_path"]
        factory_name = config["factory_name"]
        params = config["params"]
        
        logger.info(f"--> Carregando módulo: {factory_path}.{factory_name}...")
        try:
            # Import dinâmico seguro
            module = __import__(factory_path, fromlist=[factory_name])
            factory = getattr(module, factory_name)
            
            # Chamar factory com parâmetros
            agents = factory(*params)
            
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
        "summary": {"agents_loaded": agents_loaded, "failed_modules_count": len(failed_modules)},
        "failed_modules": failed_modules,
        "total_factories": len(agent_factories_config),
        "successful_factories": len(agent_factories_config) - len(failed_modules)
    }
