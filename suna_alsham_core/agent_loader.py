#!/usr/bin/env python3
"""
Agent Loader - Sistema de Carregamento Dinâmico de Agentes
ALSHAM QUANTUM v2.0
Carrega todos os agentes do sistema (36 core + domain modules opcionais)
"""

import importlib
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# Lista COMPLETA de todos os módulos de agentes CORE (36 agentes)
core_agent_modules = [
    # ==========================================
    # CORE AGENTS - pasta agents/ (36 agentes)
    # ==========================================
    
    # 🧩 1. Orquestração Central (3 agentes)
    "suna_alsham_core.agents.meta_cognitive_agents",  # orchestrator_001 + meta_cognitive_001 + meta_cognitive_002
    
    # 🔐 2. Segurança e Monitoramento (7 agentes)
    "suna_alsham_core.agents.security_guardian_agent",  # security_guardian
    "suna_alsham_core.agents.security_enhancements_agent",  # security_enhancements_001
    "suna_alsham_core.agents.guard_agents_v3",  # guard_v3_001 + guard_v3_002
    "suna_alsham_core.agents.validation_sentinel_agent",  # validation_sentinel_001
    "suna_alsham_core.agents.monitor_agent",  # monitor_001
    "suna_alsham_core.agents.control_agent",  # control_001
    "suna_alsham_core.agents.recovery_agent",  # recovery_001
    
    # 🖥️ 3. Sistema Interno (3 agentes)
    "suna_alsham_core.agents.logging_agent",  # logging_001
    "suna_alsham_core.agents.performance_monitor_agent",  # performance_monitor_001
    "suna_alsham_core.agents.disaster_recovery_agent",  # disaster_recovery_001
    
    # 🔌 4. Serviços e Infraestrutura (8 agentes)
    "suna_alsham_core.agents.database_agent",  # database_001
    "suna_alsham_core.agents.api_gateway_agent",  # api_gateway_001
    "suna_alsham_core.agents.notification_agent",  # notification_001
    "suna_alsham_core.agents.backup_agent",  # backup_agent_001
    "suna_alsham_core.agents.deployment_agent",  # deployment_001
    "suna_alsham_core.agents.communication_agent",  # communication_001
    "suna_alsham_core.agents.decision_agent",  # decision_001
    "suna_alsham_core.agents.cache_agent",  # cache_001
    
    # 🧠 5. Especializados em IA (10 agentes)
    "suna_alsham_core.agents.ai_analyzer_agent",  # ai_analyzer_001
    "suna_alsham_core.agents.ai_powered_agents",  # ai_powered_001
    "suna_alsham_core.agents.web_search_agent",  # web_search_001
    "suna_alsham_core.agents.visualization_agent",  # visualization_001
    "suna_alsham_core.agents.testing_agent",  # testing_001
    "suna_alsham_core.agents.code_corrector_agent",  # code_corrector_001
    "suna_alsham_core.agents.task_delegator_agent",  # task_delegator_001
    "suna_alsham_core.agents.onboarding_agent",  # onboarding_001
    "suna_alsham_core.agents.evolution_engine_agent",  # evolution_engine_001
    "suna_alsham_core.agents.structure_analyzer_agent",  # structure_analyzer_001
    
    # ⚙️ 6. Núcleo Base V3 (3 agentes)
    "suna_alsham_core.agents.core_agents_v3",  # core_v3_001 + core_v3_002
    "suna_alsham_core.agents.learn_agents_v3",  # learn_v3_001
    
    # 🧭 7. Registry Central (1 agente)
    "suna_alsham_core.agents.agent_registry",  # agent_registry_001
]

# Domain modules opcionais (carregam apenas se existirem)
optional_domain_modules = [
    # ==========================================
    # DOMAIN MODULES - Analytics (5 agentes)
    # ==========================================
    "domain_modules.analytics.analytics_orchestrator_agent",
    "domain_modules.analytics.data_collector_agent",
    "domain_modules.analytics.data_processing_agent",
    "domain_modules.analytics.predictive_analysis_agent",
    "domain_modules.analytics.reporting_visualization_agent",
    
    # ==========================================
    # DOMAIN MODULES - Sales (6 agentes)
    # ==========================================
    "domain_modules.sales.sales_orchestrator_agent",
    "domain_modules.sales.sales_funnel_agent",
    "domain_modules.sales.pricing_optimizer_agent",
    "domain_modules.sales.payment_processing_agent",
    "domain_modules.sales.customer_success_agent",
    "domain_modules.sales.revenue_optimization_agent",
    
    # ==========================================
    # DOMAIN MODULES - Social Media (5 agentes)
    # ==========================================
    "domain_modules.social_media.social_media_orchestrator_agent",
    "domain_modules.social_media.content_creator_agent",
    "domain_modules.social_media.video_automation_agent",
    "domain_modules.social_media.engagement_maximizer_agent",
    "domain_modules.social_media.influencer_network_agent",
    
    # ==========================================
    # DOMAIN MODULES - Support (5 agentes)
    # ==========================================
    "domain_modules.support.support_orchestrator_agent",
    "domain_modules.support.chatbot_agent",
    "domain_modules.support.ticket_manager_agent",
    "domain_modules.support.knowledge_base_agent",
    "domain_modules.support.satisfaction_analyzer_agent",
]

# Mapeamento CORRETO de quantos agentes cada módulo CORE deveria carregar
expected_core_agents_per_module = {
    # Orquestração Central
    "suna_alsham_core.agents.meta_cognitive_agents": 3,  # orchestrator + 2 meta_cognitive
    
    # Segurança e Monitoramento  
    "suna_alsham_core.agents.security_guardian_agent": 1,
    "suna_alsham_core.agents.security_enhancements_agent": 1,
    "suna_alsham_core.agents.guard_agents_v3": 2,  # guard_v3_001 + guard_v3_002
    "suna_alsham_core.agents.validation_sentinel_agent": 1,
    "suna_alsham_core.agents.monitor_agent": 1,
    "suna_alsham_core.agents.control_agent": 1,
    "suna_alsham_core.agents.recovery_agent": 1,
    
    # Sistema Interno
    "suna_alsham_core.agents.logging_agent": 1,
    "suna_alsham_core.agents.performance_monitor_agent": 1,
    "suna_alsham_core.agents.disaster_recovery_agent": 1,
    
    # Serviços e Infraestrutura
    "suna_alsham_core.agents.database_agent": 1,
    "suna_alsham_core.agents.api_gateway_agent": 1,
    "suna_alsham_core.agents.notification_agent": 1,
    "suna_alsham_core.agents.backup_agent": 1,
    "suna_alsham_core.agents.deployment_agent": 1,
    "suna_alsham_core.agents.communication_agent": 1,
    "suna_alsham_core.agents.decision_agent": 1,
    "suna_alsham_core.agents.cache_agent": 1,
    
    # IA Especializada
    "suna_alsham_core.agents.ai_analyzer_agent": 1,
    "suna_alsham_core.agents.ai_powered_agents": 1,
    "suna_alsham_core.agents.web_search_agent": 1,
    "suna_alsham_core.agents.visualization_agent": 1,
    "suna_alsham_core.agents.testing_agent": 1,
    "suna_alsham_core.agents.code_corrector_agent": 1,
    "suna_alsham_core.agents.task_delegator_agent": 1,
    "suna_alsham_core.agents.onboarding_agent": 1,
    "suna_alsham_core.agents.evolution_engine_agent": 1,
    "suna_alsham_core.agents.structure_analyzer_agent": 1,
    
    # Núcleo Base V3
    "suna_alsham_core.agents.core_agents_v3": 2,  # core_v3_001 + core_v3_002
    "suna_alsham_core.agents.learn_agents_v3": 1,
    
    # Registry Central
    "suna_alsham_core.agents.agent_registry": 1,
}

# Mapeamento para domain modules (1 agente por módulo)
expected_domain_agents_per_module = {
    module: 1 for module in optional_domain_modules
}

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    """
    Inicializa todos os agentes CORE + domain modules opcionais.
    
    ESTRATÉGIA:
    1. CORE agents são obrigatórios - se falharem, sistema reporta erro crítico
    2. Domain modules são opcionais - se falharem, sistema continua funcionando
    
    :param network: Instância da rede (deve possuir atributo message_bus e método register_agent).
    :return: Dicionário com resumo detalhado da operação.
    """
    agents_loaded: int = 0
    core_agents_loaded: int = 0
    domain_agents_loaded: int = 0
    agents_by_module: Dict[str, int] = {}
    failed_modules: List[str] = []
    detailed_failures: Dict[str, str] = {}
    successful_agents: List[str] = []
    
    # FASE 1: CARREGAMENTO DOS AGENTES CORE (OBRIGATÓRIOS)
    logger.info("🔱 FASE 1: CARREGANDO AGENTES CORE (OBRIGATÓRIOS)")
    logger.info("=" * 80)
    
    total_core_modules = len(core_agent_modules)
    expected_core_agents = sum(expected_core_agents_per_module.values())
    
    for idx, module_name in enumerate(core_agent_modules, 1):
        success = await _load_module(
            module_name, idx, total_core_modules, network,
            expected_core_agents_per_module, agents_by_module,
            failed_modules, detailed_failures, successful_agents,
            is_core=True
        )
        
        if success:
            core_agents_loaded += agents_by_module.get(module_name, 0)
    
    agents_loaded += core_agents_loaded
    
    # Análise do CORE
    core_success_rate = (core_agents_loaded / expected_core_agents * 100) if expected_core_agents > 0 else 0
    
    logger.info("=" * 80)
    logger.info("📊 RESULTADO DOS AGENTES CORE:")
    logger.info(f"✅ Agentes CORE carregados: {core_agents_loaded}/{expected_core_agents}")
    logger.info(f"📈 Taxa de sucesso CORE: {core_success_rate:.1f}%")
    
    if core_success_rate < 80:
        logger.critical(f"🔴 ATENÇÃO: Apenas {core_success_rate:.1f}% dos agentes CORE carregados!")
        logger.critical("🔴 Sistema pode não funcionar corretamente!")
    else:
        logger.info("✅ CORE system operacional!")
    
    # FASE 2: CARREGAMENTO DOS DOMAIN MODULES (OPCIONAIS)
    logger.info("=" * 80)
    logger.info("🔌 FASE 2: CARREGANDO DOMAIN MODULES (OPCIONAIS)")
    logger.info("=" * 80)
    
    total_domain_modules = len(optional_domain_modules)
    expected_domain_agents = len(optional_domain_modules)  # 1 agente por módulo
    
    for idx, module_name in enumerate(optional_domain_modules, 1):
        success = await _load_module(
            module_name, idx, total_domain_modules, network,
            expected_domain_agents_per_module, agents_by_module,
            failed_modules, detailed_failures, successful_agents,
            is_core=False
        )
        
        if success:
            domain_agents_loaded += agents_by_module.get(module_name, 0)
    
    agents_loaded += domain_agents_loaded
    
    # Análise dos DOMAIN MODULES
    domain_success_rate = (domain_agents_loaded / expected_domain_agents * 100) if expected_domain_agents > 0 else 0
    
    logger.info("=" * 80)
    logger.info("📊 RESULTADO DOS DOMAIN MODULES:")
    logger.info(f"🔌 Domain agents carregados: {domain_agents_loaded}/{expected_domain_agents}")
    logger.info(f"📈 Taxa de sucesso domain: {domain_success_rate:.1f}%")
    
    if domain_agents_loaded == 0:
        logger.warning("⚠️ Nenhum domain module carregado - apenas CORE funcionando")
    else:
        logger.info(f"✅ {domain_agents_loaded} domain modules ativos")
    
    # RESUMO FINAL
    total_expected = expected_core_agents + expected_domain_agents
    overall_success_rate = (agents_loaded / total_expected * 100) if total_expected > 0 else 0
    
    logger.info("=" * 80)
    logger.info("🎯 RESUMO FINAL DO SISTEMA ALSHAM QUANTUM")
    logger.info("=" * 80)
    logger.info(f"🔱 CORE agents: {core_agents_loaded}/{expected_core_agents}")
    logger.info(f"🔌 Domain agents: {domain_agents_loaded}/{expected_domain_agents}")
    logger.info(f"✅ TOTAL carregado: {agents_loaded}/{total_expected}")
    logger.info(f"📈 Taxa geral: {overall_success_rate:.1f}%")
    
    # Status do sistema
    if core_agents_loaded >= expected_core_agents:
        logger.info("🚀 STATUS: SISTEMA CORE OPERACIONAL!")
        if domain_agents_loaded > 0:
            logger.info(f"🔌 EXTRAS: {domain_agents_loaded} domain modules ativos")
    else:
        logger.critical("🔴 STATUS: SISTEMA CORE INCOMPLETO!")
    
    # Detalhamento de falhas se existirem
    if failed_modules:
        core_failures = [m for m in failed_modules if m in core_agent_modules]
        domain_failures = [m for m in failed_modules if m in optional_domain_modules]
        
        if core_failures:
            logger.error("❌ CORE modules com falha:")
            for module in core_failures[:5]:  # Mostra apenas os primeiros 5
                logger.error(f"  ❌ {module}")
        
        if domain_failures:
            logger.warning("⚠️ Domain modules com falha (opcional):")
            for module in domain_failures[:5]:
                logger.warning(f"  ⚠️ {module}")
    
    # Prepara summary
    summary = {
        "total_agents_loaded": agents_loaded,
        "core_agents_loaded": core_agents_loaded,
        "domain_agents_loaded": domain_agents_loaded,
        "expected_core_agents": expected_core_agents,
        "expected_domain_agents": expected_domain_agents,
        "core_success_rate": f"{core_success_rate:.1f}%",
        "domain_success_rate": f"{domain_success_rate:.1f}%",
        "overall_success_rate": f"{overall_success_rate:.1f}%",
        "agents_by_module": agents_by_module,
        "successful_agents": successful_agents[:10] + ["..."] if len(successful_agents) > 10 else successful_agents,
        "failed_modules": failed_modules,
        "detailed_failures": detailed_failures,
        "system_status": "OPERATIONAL" if core_agents_loaded >= expected_core_agents else "DEGRADED"
    }
    
    logger.info("=" * 80)
    logger.info("Resumo detalhado disponível em 'summary' para diagnósticos automatizados.")
    
    return summary

async def _load_module(
    module_name: str, idx: int, total_modules: int, network: Any,
    expected_agents_map: Dict[str, int], agents_by_module: Dict[str, int],
    failed_modules: List[str], detailed_failures: Dict[str, str],
    successful_agents: List[str], is_core: bool = True
) -> bool:
    """
    Carrega um módulo específico de agentes.
    
    :param module_name: Nome do módulo a carregar
    :param is_core: Se True, trata como módulo core (falha é crítica)
    :return: True se sucesso, False se falha
    """
    module_type = "CORE" if is_core else "DOMAIN"
    
    try:
        logger.info(f"🔍 [{idx}/{total_modules}] Carregando {module_type}: {module_name}")
        
        # Tenta importar o módulo
        try:
            imported_module = importlib.import_module(module_name)
        except ImportError as ie:
            if is_core:
                logger.error(f"❌ CORE module {module_name} não encontrado: {ie}")
            else:
                logger.warning(f"⚠️ Domain module {module_name} não encontrado (opcional): {ie}")
            failed_modules.append(module_name)
            detailed_failures[module_name] = f"Módulo não encontrado: {ie}"
            return False
        
        # Verifica se tem a função create_agents
        if not hasattr(imported_module, "create_agents"):
            if is_core:
                logger.error(f"❌ CORE module {module_name} não possui função create_agents()")
            else:
                logger.warning(f"⚠️ Domain module {module_name} não possui create_agents() (opcional)")
            failed_modules.append(module_name)
            detailed_failures[module_name] = "Função create_agents não encontrada"
            return False
        
        try:
            # Suporte a kwargs avançados para create_agents
            import os
            advanced_kwargs = {}
            # Permite configuração global via env
            if hasattr(network, 'critical_event_callback'):
                advanced_kwargs['critical_event_callback'] = getattr(network, 'critical_event_callback')
            if hasattr(network, 'max_concurrent_missions'):
                advanced_kwargs['max_concurrent_missions'] = getattr(network, 'max_concurrent_missions')
            if hasattr(network, 'mission_history_limit'):
                advanced_kwargs['mission_history_limit'] = getattr(network, 'mission_history_limit')
            if hasattr(network, 'performance_analysis_interval'):
                advanced_kwargs['performance_analysis_interval'] = getattr(network, 'performance_analysis_interval')
            if hasattr(network, 'quantum_coherence_threshold'):
                advanced_kwargs['quantum_coherence_threshold'] = getattr(network, 'quantum_coherence_threshold')
            # Chama create_agents com message_bus e kwargs se suportado
            try:
                agents = imported_module.create_agents(network.message_bus, **advanced_kwargs)
            except TypeError:
                # Fallback para assinatura antiga
                agents = imported_module.create_agents(network.message_bus)
            # Valida o retorno
            if agents is None:
                error_msg = f"create_agents de {module_name} retornou None"
                if is_core:
                    logger.error(f"❌ {error_msg}")
                else:
                    logger.warning(f"⚠️ {error_msg}")
                failed_modules.append(module_name)
                detailed_failures[module_name] = "create_agents retornou None"
                return False
            if not isinstance(agents, list):
                error_msg = f"create_agents de {module_name} não retornou uma lista (retornou {type(agents).__name__})"
                if is_core:
                    logger.error(f"❌ {error_msg}")
                else:
                    logger.warning(f"⚠️ {error_msg}")
                failed_modules.append(module_name)
                detailed_failures[module_name] = f"create_agents retornou {type(agents).__name__}"
                return False
            # Registra cada agente
            module_agent_count = 0
            for agent in agents:
                try:
                    network.register_agent(agent)
                    agent_id = getattr(agent, 'agent_id', f'agent_{len(successful_agents)}')
                    module_agent_count += 1
                    successful_agents.append(agent_id)
                    logger.info(f"  ✅ Agente {agent_id} registrado com sucesso")
                except Exception as agent_exc:
                    logger.error(f"  ❌ Erro ao registrar agente: {agent_exc}")
            if module_agent_count > 0:
                agents_by_module[module_name] = module_agent_count
                expected = expected_agents_map.get(module_name, 1)
                status = "✅" if module_agent_count >= expected else "⚠️"
                logger.info(f"  {status} {module_agent_count}/{expected} agente(s) carregado(s) de {module_name}")
                return True
            else:
                error_msg = "Nenhum agente foi registrado"
                failed_modules.append(module_name)
                detailed_failures[module_name] = error_msg
                return False
        except Exception as create_exc:
            error_msg = f"Erro ao executar create_agents de {module_name}: {create_exc}"
            if is_core:
                logger.error(f"❌ {error_msg}")
            else:
                logger.warning(f"⚠️ {error_msg}")
            failed_modules.append(module_name)
            detailed_failures[module_name] = f"Erro em create_agents: {create_exc}"
            return False
            
    except Exception as e:
        error_msg = f"Erro inesperado ao processar {module_name}: {e}"
        if is_core:
            logger.error(f"❌ {error_msg}", exc_info=True)
        else:
            logger.warning(f"⚠️ {error_msg}", exc_info=True)
        failed_modules.append(module_name)
        detailed_failures[module_name] = f"Erro inesperado: {str(e)}"
        return False
