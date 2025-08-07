#!/usr/bin/env python3
"""
Agent Loader - Sistema de Carregamento Dinâmico de Agentes
ALSHAM QUANTUM v2.0
Carrega os 36 agentes CORE + domain modules opcionais baseado na ESTRUTURA REAL
"""

import importlib
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# ==========================================
# CORE AGENTS - MAPEAMENTO REAL (36 agentes)
# ==========================================

core_agent_modules = [
    # ARQUIVOS AGRUPADOS (9 agentes confirmados)
    "suna_alsham_core.agents.system_agents",           # 3 agentes: monitor_001, control_001, recovery_001
    "suna_alsham_core.agents.service_agents",          # 2 agentes: communication_001, decision_001
    "suna_alsham_core.agents.specialized_agents",      # 2 agentes: task_delegator_001, onboarding_001
    "suna_alsham_core.agents.core_agents_v3",          # 2 agentes: core_v3_001, core_v3_002
    
    # ARQUIVOS INDIVIDUAIS CONFIRMADOS (~27 agentes)
    "suna_alsham_core.agents.agent_registry",          # 1 agente: agent_registry_001
    "suna_alsham_core.agents.ai_powered_agents",       # 1 agente: ai_powered_001
    "suna_alsham_core.agents.api_gateway_agent",       # 1 agente: api_gateway_001
    "suna_alsham_core.agents.backup_agent",            # 1 agente: backup_agent_001
    "suna_alsham_core.agents.code_analyzer_agent",     # 1 agente: code_analyzer_001
    "suna_alsham_core.agents.code_corrector_agent",    # 1 agente: code_corrector_001
    "suna_alsham_core.agents.computer_control_agent",  # 1 agente: computer_control_001
    "suna_alsham_core.agents.database_agent",          # 1 agente: database_001
    "suna_alsham_core.agents.debug_agent_creation",    # 1 agente: debug_001
    "suna_alsham_core.agents.deployment_agent",        # 1 agente: deployment_001
    "suna_alsham_core.agents.disaster_recovery_agent", # 1 agente: disaster_recovery_001
    "suna_alsham_core.agents.logging_agent",           # 1 agente: logging_001
    "suna_alsham_core.agents.meta_cognitive_agents",   # 3 agentes: orchestrator_001, meta_cognitive_001, meta_cognitive_002
    "suna_alsham_core.agents.notification_agent",      # 1 agente: notification_001
    "suna_alsham_core.agents.performance_monitor_agent", # 1 agente: performance_monitor_001
    "suna_alsham_core.agents.real_evolution_engine",   # 1 agente: evolution_engine_001
    "suna_alsham_core.agents.security_enhancements_agent", # 1 agente: security_enhancements_001
    "suna_alsham_core.agents.security_guardian_agent", # 1 agente: security_guardian
    "suna_alsham_core.agents.structure_analyzer_agent", # 1 agente: structure_analyzer_001
    "suna_alsham_core.agents.testing_agent",           # 1 agente: testing_001
    "suna_alsham_core.agents.validation_sentinel_agent", # 1 agente: validation_sentinel_001
    "suna_alsham_core.agents.visualization_agent",     # 1 agente: visualization_001
    "suna_alsham_core.agents.web_search_agent",        # 1 agente: web_search_001
]

# Domain modules opcionais (carregam apenas se existirem)
optional_domain_modules = [
    # Analytics (5 agentes)
    "domain_modules.analytics.analytics_orchestrator_agent",
    "domain_modules.analytics.data_collector_agent", 
    "domain_modules.analytics.data_processing_agent",
    "domain_modules.analytics.predictive_analysis_agent",
    "domain_modules.analytics.reporting_visualization_agent",
    
    # Sales (6 agentes)
    "domain_modules.sales.sales_orchestrator_agent",
    "domain_modules.sales.sales_funnel_agent",
    "domain_modules.sales.pricing_optimizer_agent", 
    "domain_modules.sales.payment_processing_agent",
    "domain_modules.sales.customer_success_agent",
    "domain_modules.sales.revenue_optimization_agent",
    
    # Social Media (5 agentes)
    "domain_modules.social_media.social_media_orchestrator_agent",
    "domain_modules.social_media.content_creator_agent",
    "domain_modules.social_media.video_automation_agent",
    "domain_modules.social_media.engagement_maximizer_agent",
    "domain_modules.social_media.influencer_network_agent",
    
    # Suporte (5 agentes)  
    "domain_modules.suporte.support_orchestrator_agent",
    "domain_modules.suporte.chatbot_agent",
    "domain_modules.suporte.ticket_manager_agent", 
    "domain_modules.suporte.knowledge_base_agent",
    "domain_modules.suporte.satisfaction_analyzer_agent",
]

# Mapeamento esperado CORRETO
expected_core_agents_per_module = {
    # Arquivos agrupados
    "suna_alsham_core.agents.system_agents": 3,
    "suna_alsham_core.agents.service_agents": 2,
    "suna_alsham_core.agents.specialized_agents": 2,
    "suna_alsham_core.agents.core_agents_v3": 2,
    
    # Arquivos individuais
    "suna_alsham_core.agents.agent_registry": 1,
    "suna_alsham_core.agents.ai_powered_agents": 1,
    "suna_alsham_core.agents.api_gateway_agent": 1,
    "suna_alsham_core.agents.backup_agent": 1,
    "suna_alsham_core.agents.code_analyzer_agent": 1,
    "suna_alsham_core.agents.code_corrector_agent": 1,
    "suna_alsham_core.agents.computer_control_agent": 1,
    "suna_alsham_core.agents.database_agent": 1,
    "suna_alsham_core.agents.debug_agent_creation": 1,
    "suna_alsham_core.agents.deployment_agent": 1,
    "suna_alsham_core.agents.disaster_recovery_agent": 1,
    "suna_alsham_core.agents.logging_agent": 1,
    "suna_alsham_core.agents.meta_cognitive_agents": 3,
    "suna_alsham_core.agents.notification_agent": 1,
    "suna_alsham_core.agents.performance_monitor_agent": 1,
    "suna_alsham_core.agents.real_evolution_engine": 1,
    "suna_alsham_core.agents.security_enhancements_agent": 1,
    "suna_alsham_core.agents.security_guardian_agent": 1,
    "suna_alsham_core.agents.structure_analyzer_agent": 1,
    "suna_alsham_core.agents.testing_agent": 1,
    "suna_alsham_core.agents.validation_sentinel_agent": 1,
    "suna_alsham_core.agents.visualization_agent": 1,
    "suna_alsham_core.agents.web_search_agent": 1,
}

expected_domain_agents_per_module = {module: 1 for module in optional_domain_modules}

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    """
    Inicializa CORE agents (obrigatórios) + domain modules (opcionais).
    Baseado na estrutura REAL dos arquivos mapeados.
    """
    agents_loaded = 0
    core_agents_loaded = 0
    domain_agents_loaded = 0
    agents_by_module = {}
    failed_modules = []
    detailed_failures = {}
    successful_agents = []
    
    # FASE 1: CARREGAMENTO CORE AGENTS (OBRIGATÓRIOS)
    logger.info("=" * 80)
    logger.info("🔱 FASE 1: CARREGANDO 36 AGENTES CORE (OBRIGATÓRIOS)")
    logger.info("=" * 80)
    
    total_core_modules = len(core_agent_modules)
    expected_core_agents = sum(expected_core_agents_per_module.values())
    
    logger.info(f"📊 EXPECTATIVA: {expected_core_agents} agentes CORE de {total_core_modules} módulos")
    
    for idx, module_name in enumerate(core_agent_modules, 1):
        logger.info(f"🔍 [{idx}/{total_core_modules}] Carregando CORE: {module_name}")
        
        success = await _load_module_safe(
            module_name, network, expected_core_agents_per_module,
            agents_by_module, failed_modules, detailed_failures, 
            successful_agents, is_core=True
        )
        
        if success:
            module_agents = agents_by_module.get(module_name, 0)
            core_agents_loaded += module_agents
            expected = expected_core_agents_per_module.get(module_name, 1)
            status = "✅" if module_agents >= expected else "⚠️"
            logger.info(f"  {status} {module_agents}/{expected} agente(s) carregado(s)")
        else:
            logger.error(f"  ❌ FALHA no módulo CORE: {module_name}")
    
    # Análise CORE
    core_success_rate = (core_agents_loaded / expected_core_agents * 100) if expected_core_agents > 0 else 0
    
    logger.info("=" * 80)
    logger.info("📊 RESULTADO CORE AGENTS:")
    logger.info(f"🔱 CORE agents carregados: {core_agents_loaded}/{expected_core_agents}")
    logger.info(f"📈 Taxa de sucesso CORE: {core_success_rate:.1f}%")
    
    if core_success_rate >= 90:
        logger.info("🚀 CORE SYSTEM: OPERACIONAL!")
    elif core_success_rate >= 70:
        logger.warning("⚠️ CORE SYSTEM: FUNCIONAL (algumas funcionalidades podem estar limitadas)")
    else:
        logger.critical("🔴 CORE SYSTEM: COMPROMETIDO!")
    
    # FASE 2: DOMAIN MODULES (OPCIONAIS)
    logger.info("=" * 80)
    logger.info("🔌 FASE 2: CARREGANDO DOMAIN MODULES (OPCIONAIS)")
    logger.info("=" * 80)
    
    total_domain_modules = len(optional_domain_modules)
    expected_domain_agents = len(optional_domain_modules)
    
    for idx, module_name in enumerate(optional_domain_modules, 1):
        logger.info(f"🔍 [{idx}/{total_domain_modules}] Carregando DOMAIN: {module_name}")
        
        success = await _load_module_safe(
            module_name, network, expected_domain_agents_per_module,
            agents_by_module, failed_modules, detailed_failures,
            successful_agents, is_core=False
        )
        
        if success:
            domain_agents_loaded += agents_by_module.get(module_name, 0)
    
    domain_success_rate = (domain_agents_loaded / expected_domain_agents * 100) if expected_domain_agents > 0 else 0
    
    logger.info("=" * 80)
    logger.info("📊 RESULTADO DOMAIN MODULES:")
    logger.info(f"🔌 Domain agents: {domain_agents_loaded}/{expected_domain_agents}")
    logger.info(f"📈 Taxa domain: {domain_success_rate:.1f}%")
    
    # RESUMO FINAL
    agents_loaded = core_agents_loaded + domain_agents_loaded
    total_expected = expected_core_agents + expected_domain_agents
    overall_success_rate = (agents_loaded / total_expected * 100) if total_expected > 0 else 0
    
    logger.info("=" * 80)
    logger.info("🎯 RESUMO FINAL ALSHAM QUANTUM")
    logger.info("=" * 80)
    logger.info(f"🔱 CORE agents: {core_agents_loaded}/{expected_core_agents}")
    logger.info(f"🔌 Domain agents: {domain_agents_loaded}/{expected_domain_agents}")
    logger.info(f"✅ TOTAL: {agents_loaded}/{total_expected}")
    logger.info(f"📈 Taxa geral: {overall_success_rate:.1f}%")
    
    # Status do sistema
    if core_agents_loaded >= expected_core_agents:
        logger.info("🚀 STATUS: CORE COMPLETO - SISTEMA OPERACIONAL!")
    elif core_agents_loaded >= (expected_core_agents * 0.9):
        logger.warning("⚠️ STATUS: CORE QUASE COMPLETO - FUNCIONAL")
    else:
        logger.critical("🔴 STATUS: CORE INCOMPLETO - VERIFICAR FALHAS!")
    
    # Detalhamento de falhas CORE
    core_failures = [m for m in failed_modules if m in core_agent_modules]
    if core_failures:
        logger.error("❌ CORE modules com falha:")
        for module in core_failures[:10]:
            error_detail = detailed_failures.get(module, "Erro desconhecido")
            logger.error(f"  ❌ {module}")
            logger.error(f"     → {error_detail}")
    
    # Summary estruturado
    summary = {
        "core_agents_loaded": core_agents_loaded,
        "domain_agents_loaded": domain_agents_loaded,
        "total_agents_loaded": agents_loaded,
        "expected_core_agents": expected_core_agents,
        "expected_domain_agents": expected_domain_agents,
        "core_success_rate": f"{core_success_rate:.1f}%",
        "domain_success_rate": f"{domain_success_rate:.1f}%",
        "overall_success_rate": f"{overall_success_rate:.1f}%",
        "system_status": "OPERATIONAL" if core_agents_loaded >= expected_core_agents else "DEGRADED",
        "agents_by_module": agents_by_module,
        "failed_modules": failed_modules,
        "detailed_failures": detailed_failures,
        "successful_agents": successful_agents[:20]  # Primeiros 20 para logging
    }
    
    logger.info("=" * 80)
    logger.info("Resumo detalhado disponível em 'summary' para diagnósticos automatizados.")
    
    return summary

async def _load_module_safe(
    module_name: str, network: Any, expected_map: Dict[str, int],
    agents_by_module: Dict[str, int], failed_modules: List[str],
    detailed_failures: Dict[str, str], successful_agents: List[str],
    is_core: bool = True
) -> bool:
    """
    Carrega módulo com tratamento robusto de erros.
    """
    try:
        # Import do módulo
        try:
            imported_module = importlib.import_module(module_name)
        except ImportError as ie:
            error_msg = f"Módulo não encontrado: {ie}"
            failed_modules.append(module_name)
            detailed_failures[module_name] = error_msg
            if is_core:
                logger.error(f"❌ {error_msg}")
            else:
                logger.warning(f"⚠️ {error_msg} (opcional)")
            return False
        
        # Verifica create_agents
        if not hasattr(imported_module, "create_agents"):
            error_msg = "Função create_agents não encontrada"
            failed_modules.append(module_name)
            detailed_failures[module_name] = error_msg
            if is_core:
                logger.error(f"❌ {error_msg}")
            else:
                logger.warning(f"⚠️ {error_msg} (opcional)")
            return False
        
        # Executa create_agents
        try:
            agents = imported_module.create_agents(network.message_bus)
            
            if not agents or not isinstance(agents, list):
                error_msg = f"create_agents retornou {type(agents).__name__} em vez de lista"
                failed_modules.append(module_name)
                detailed_failures[module_name] = error_msg
                return False
            
            # Registra agentes
            module_agent_count = 0
            for agent in agents:
                try:
                    network.register_agent(agent)
                    agent_id = getattr(agent, 'agent_id', f'agent_{len(successful_agents)}')
                    successful_agents.append(agent_id)
                    module_agent_count += 1
                    logger.debug(f"    ✅ {agent_id}")
                except Exception as e:
                    logger.error(f"    ❌ Erro registrando agente: {e}")
            
            if module_agent_count > 0:
                agents_by_module[module_name] = module_agent_count
                return True
            else:
                error_msg = "Nenhum agente registrado com sucesso"
                failed_modules.append(module_name)
                detailed_failures[module_name] = error_msg
                return False
                
        except Exception as e:
            error_msg = f"Erro em create_agents: {e}"
            failed_modules.append(module_name)
            detailed_failures[module_name] = error_msg
            if is_core:
                logger.error(f"❌ {error_msg}")
            else:
                logger.warning(f"⚠️ {error_msg}")
            return False
            
    except Exception as e:
        error_msg = f"Erro inesperado: {e}"
        failed_modules.append(module_name)
        detailed_failures[module_name] = error_msg
        logger.error(f"❌ {error_msg}", exc_info=True)
        return False
