#!/usr/bin/env python3
"""
Agent Loader - Sistema de Carregamento Dinâmico de Agentes
ALSHAM QUANTUM v2.0
Carrega todos os 59 agentes do sistema (38 core + 21 domain)
"""

import importlib
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# Lista COMPLETA de todos os módulos de agentes
agent_modules = [
    # ==========================================
    # CORE AGENTS - pasta agents/ (38 agentes)
    # ==========================================
    
    # Agentes principais com create_agents implementado
    "suna_alsham_core.agents.core_agents_v3",
    "suna_alsham_core.agents.specialized_agents",
    "suna_alsham_core.agents.system_agents",
    "suna_alsham_core.agents.service_agents",
    "suna_alsham_core.agents.meta_cognitive_agents",
    "suna_alsham_core.agents.ai_powered_agents",
    
    # Agentes individuais que podem ter create_agents
    "suna_alsham_core.agents.agent_registry",
    "suna_alsham_core.agents.api_gateway_agent",
    "suna_alsham_core.agents.backup_agent",
    "suna_alsham_core.agents.code_analyzer_agent",
    "suna_alsham_core.agents.code_corrector_agent",
    "suna_alsham_core.agents.computer_control_agent",
    "suna_alsham_core.agents.database_agent",
    "suna_alsham_core.agents.debug_agent_creation",
    "suna_alsham_core.agents.deployment_agent",
    "suna_alsham_core.agents.disaster_recovery_agent",
    "suna_alsham_core.agents.logging_agent",
    "suna_alsham_core.agents.multi_agent_network",
    "suna_alsham_core.agents.notification_agent",
    "suna_alsham_core.agents.performance_monitor_agent",
    "suna_alsham_core.agents.real_evolution_engine",
    "suna_alsham_core.agents.security_enhancements_agent",
    "suna_alsham_core.agents.security_guardian_agent",
    "suna_alsham_core.agents.structure_analyzer_agent",
    "suna_alsham_core.agents.testing_agent",
    "suna_alsham_core.agents.validation_sentinel_agent",
    "suna_alsham_core.agents.visualization_agent",
    "suna_alsham_core.agents.web_search_agent",
    
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

# Mapeamento realista de quantos agentes cada módulo deveria carregar
expected_agents_per_module = {
    # Core agents
    "suna_alsham_core.agents.core_agents_v3": 2,
    "suna_alsham_core.agents.specialized_agents": 2,
    "suna_alsham_core.agents.system_agents": 3,
    "suna_alsham_core.agents.service_agents": 2,
    "suna_alsham_core.agents.meta_cognitive_agents": 2,
    "suna_alsham_core.agents.ai_powered_agents": 1,
    
    # Individual agents
    "suna_alsham_core.agents.agent_registry": 1,
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
    "suna_alsham_core.agents.multi_agent_network": 1,
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
    
    # Analytics domain
    "domain_modules.analytics.analytics_orchestrator_agent": 1,
    "domain_modules.analytics.data_collector_agent": 1,
    "domain_modules.analytics.data_processing_agent": 1,
    "domain_modules.analytics.predictive_analysis_agent": 1,
    "domain_modules.analytics.reporting_visualization_agent": 1,
    
    # Sales domain
    "domain_modules.sales.sales_orchestrator_agent": 1,
    "domain_modules.sales.sales_funnel_agent": 1,
    "domain_modules.sales.pricing_optimizer_agent": 1,
    "domain_modules.sales.payment_processing_agent": 1,
    "domain_modules.sales.customer_success_agent": 1,
    "domain_modules.sales.revenue_optimization_agent": 1,
    
    # Social Media domain
    "domain_modules.social_media.social_media_orchestrator_agent": 1,
    "domain_modules.social_media.content_creator_agent": 1,
    "domain_modules.social_media.video_automation_agent": 1,
    "domain_modules.social_media.engagement_maximizer_agent": 1,
    "domain_modules.social_media.influencer_network_agent": 1,
    
    # Support domain
    "domain_modules.support.support_orchestrator_agent": 1,
    "domain_modules.support.chatbot_agent": 1,
    "domain_modules.support.ticket_manager_agent": 1,
    "domain_modules.support.knowledge_base_agent": 1,
    "domain_modules.support.satisfaction_analyzer_agent": 1,
}

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    """
    Inicializa todos os agentes listados em agent_modules e os registra na rede fornecida.
    
    Para cada módulo, tenta importar e executar create_agents(message_bus), 
    registrando cada agente retornado.
    
    :param network: Instância da rede (deve possuir atributo message_bus e método register_agent).
    :return: Dicionário com resumo detalhado da operação.
    """
    agents_loaded: int = 0
    agents_by_module: Dict[str, int] = {}
    failed_modules: List[str] = []
    detailed_failures: Dict[str, str] = {}
    successful_agents: List[str] = []
    
    total_modules = len(agent_modules)
    logger.info(f"🚀 Iniciando carregamento de {total_modules} módulos de agentes...")
    
    for idx, module_name in enumerate(agent_modules, 1):
        try:
            logger.info(f"🔍 [{idx}/{total_modules}] Carregando módulo: {module_name}")
            
            # Tenta importar o módulo
            try:
                imported_module = importlib.import_module(module_name)
            except ImportError as ie:
                logger.warning(f"⚠️ Módulo {module_name} não encontrado: {ie}")
                failed_modules.append(module_name)
                detailed_failures[module_name] = f"Módulo não encontrado: {ie}"
                continue
            
            # Verifica se tem a função create_agents
            if hasattr(imported_module, "create_agents"):
                try:
                    # Chama create_agents com o message_bus
                    agents = imported_module.create_agents(network.message_bus)
                    
                    # Valida o retorno
                    if agents is None:
                        logger.warning(f"⚠️ create_agents de {module_name} retornou None")
                        failed_modules.append(module_name)
                        detailed_failures[module_name] = "create_agents retornou None"
                        continue
                    
                    if not isinstance(agents, list):
                        logger.warning(f"⚠️ create_agents de {module_name} não retornou uma lista")
                        failed_modules.append(module_name)
                        detailed_failures[module_name] = f"create_agents retornou {type(agents).__name__}"
                        continue
                    
                    # Registra cada agente
                    module_agent_count = 0
                    for agent in agents:
                        try:
                            network.register_agent(agent)
                            agent_id = getattr(agent, 'agent_id', f'agent_{agents_loaded}')
                            agents_loaded += 1
                            module_agent_count += 1
                            successful_agents.append(agent_id)
                            logger.info(f"  ✅ Agente {agent_id} registrado com sucesso")
                        except Exception as agent_exc:
                            logger.error(f"  ❌ Erro ao registrar agente: {agent_exc}")
                            # Não marca o módulo inteiro como falho se apenas um agente falhar
                    
                    if module_agent_count > 0:
                        agents_by_module[module_name] = module_agent_count
                        expected = expected_agents_per_module.get(module_name, 1)
                        status = "✅" if module_agent_count >= expected else "⚠️"
                        logger.info(f"  {status} {module_agent_count}/{expected} agente(s) carregado(s) de {module_name}")
                    else:
                        failed_modules.append(module_name)
                        detailed_failures[module_name] = "Nenhum agente foi registrado"
                        
                except Exception as create_exc:
                    logger.error(f"❌ Erro ao executar create_agents de {module_name}: {create_exc}")
                    failed_modules.append(module_name)
                    detailed_failures[module_name] = f"Erro em create_agents: {create_exc}"
            else:
                logger.warning(f"⚠️ Módulo {module_name} não possui função create_agents()")
                failed_modules.append(module_name)
                detailed_failures[module_name] = "Função create_agents não encontrada"
                
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao processar {module_name}: {e}", exc_info=True)
            failed_modules.append(module_name)
            detailed_failures[module_name] = f"Erro inesperado: {str(e)}"
    
    # Prepara resumo detalhado
    unique_failed_modules = list(set(failed_modules))
    success_rate = ((total_modules - len(unique_failed_modules)) / total_modules * 100) if total_modules > 0 else 0
    
    # Calcula dinamicamente o número esperado de agentes usando o mapeamento realista
    try:
        expected_agents = sum(expected_agents_per_module.get(mod, 1) for mod in agent_modules)
    except Exception as exc:
        logger.warning(f"Não foi possível calcular o número esperado de agentes dinamicamente: {exc}")
        expected_agents = 59  # fallback seguro
    
    summary = {
        "total_modules_attempted": total_modules,
        "agents_loaded": agents_loaded,
        "agents_expected": expected_agents,
        "modules_successful": len(agents_by_module),
        "modules_failed": len(unique_failed_modules),
        "success_rate": f"{success_rate:.1f}%",
        "agents_by_module": agents_by_module,
        "successful_agents": successful_agents[:10] + ["..."] if len(successful_agents) > 10 else successful_agents,
        "failed_modules": unique_failed_modules,
        "detailed_failures": detailed_failures
    }
    
    # Log do resumo final
    logger.info("=" * 80)
    logger.info("📊 RESUMO DO CARREGAMENTO DE AGENTES")
    logger.info("=" * 80)
    logger.info(f"✅ Agentes carregados com sucesso: {agents_loaded}/{expected_agents}")
    logger.info(f"📦 Módulos bem-sucedidos: {len(agents_by_module)}/{total_modules}")
    logger.info(f"📈 Taxa de sucesso: {success_rate:.1f}%")
    
    if unique_failed_modules:
        logger.warning(f"⚠️ Módulos com falha ({len(unique_failed_modules)}): {', '.join(unique_failed_modules[:5])}")
        if len(unique_failed_modules) > 5:
            logger.warning(f"   ... e mais {len(unique_failed_modules) - 5} módulos")
    else:
        logger.info("🎉 TODOS OS MÓDULOS CARREGADOS COM SUCESSO!")
    
    logger.info("=" * 80)
    
    # Protege contra divisão por zero
    if expected_agents == 0:
        logger.critical("🔴 Nenhum agente esperado definido! Verifique a configuração dos módulos.")
        expected_agents = 1
    
    # Mensagens de status conforme a proporção de agentes carregados
    percent_loaded = (agents_loaded / expected_agents) * 100
    if percent_loaded < 50:
        logger.critical(f"🔴 ATENÇÃO: Apenas {percent_loaded:.1f}% dos agentes carregados! Sistema pode não funcionar corretamente!")
    elif percent_loaded < 80:
        logger.warning(f"⚠️ {percent_loaded:.1f}% dos agentes carregados - Sistema parcialmente operacional")
    else:
        logger.info(f"✅ {percent_loaded:.1f}% dos agentes carregados - Sistema operacional!")
    
    # Detalhamento adicional se houver discrepâncias
    if agents_loaded != expected_agents:
        logger.info("📋 Análise de discrepâncias por módulo:")
        for module in agent_modules:
            expected = expected_agents_per_module.get(module, 1)
            actual = agents_by_module.get(module, 0)
            if actual != expected:
                emoji = "❌" if actual == 0 else "⚠️"
                logger.info(f"  {emoji} {module}: {actual}/{expected}")
    
    logger.info("=" * 80)
    logger.info("Resumo detalhado disponível em 'summary' para diagnósticos automatizados.")
    return summary
