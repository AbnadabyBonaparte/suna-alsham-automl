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

core_agent_modules = [
    "suna_alsham_core.agents.system_agents",
    "suna_alsham_core.agents.service_agents",
    "suna_alsham_core.agents.specialized_agents",
    "suna_alsham_core.agents.core_agents_v3",
    "suna_alsham_core.agents.agent_registry",
    "suna_alsham_core.agents.ai_powered_agents",
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
    "suna_alsham_core.agents.meta_cognitive_agents",
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
]

expected_core_agents_per_module = {
    "suna_alsham_core.agents.system_agents": 3,
    "suna_alsham_core.agents.service_agents": 2,
    "suna_alsham_core.agents.specialized_agents": 2,
    "suna_alsham_core.agents.core_agents_v3": 2,
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

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    agents_loaded = 0
    agents_by_module = {}
    failed_modules = {}
    successful_agents = []
    total_expected = sum(expected_core_agents_per_module.values())

    for module_name in core_agent_modules:
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            failed_modules[module_name] = f"ImportError: {e}"
            continue

        if not hasattr(module, "create_agents"):
            failed_modules[module_name] = "Função create_agents não encontrada"
            continue

        try:
            result = module.create_agents(network.message_bus)
            if not isinstance(result, list):
                failed_modules[module_name] = f"create_agents retornou {type(result).__name__}, esperado list"
                continue
            if not result:
                failed_modules[module_name] = "create_agents retornou lista vazia"
                continue

            count = 0
            for agent in result:
                if hasattr(agent, "agent_id"):
                    network.register_agent(agent)
                    successful_agents.append(agent.agent_id)
                    count += 1
            agents_by_module[module_name] = count
            agents_loaded += count
        except Exception as e:
            failed_modules[module_name] = f"Erro em create_agents: {e}"

    success_rate = (agents_loaded / total_expected) * 100 if total_expected else 0
    logger.info("=" * 60)
    logger.info(f"🎯 CORE AGENTS ESPERADOS: {total_expected}")
    logger.info(f"✅ AGENTES CARREGADOS: {agents_loaded}")
    logger.info(f"📈 TAXA DE SUCESSO: {success_rate:.1f}%")

    if failed_modules:
        logger.warning("❌ MÓDULOS COM FALHA:")
        for mod, err in failed_modules.items():
            logger.warning(f"  {mod}: {err}")

    summary = {
        "total_expected": total_expected,
        "total_loaded": agents_loaded,
        "success_rate": f"{success_rate:.1f}%",
        "agents_by_module": agents_by_module,
        "failed_modules": failed_modules,
        "successful_agents": successful_agents[:20],
    }

    return summary
