e ai esta bom assim?"#!/usr/bin/env python3
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
    "suna_alsham_core.agents.system_agents",
    "suna_alsham_core.agents.service_agents",
    "suna_alsham_core.agents.specialized_agents",
    "suna_alsham_core.agents.core_agents_v3",

    # ARQUIVOS INDIVIDUAIS CONFIRMADOS (~27 agentes)
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

def diagnostico_agentes_faltantes(summary: dict, expected_core: dict):
    print("\n\n" + "=" * 100)
    print("📊 DIAGNÓSTICO DE AGENTES CORE FALTANTES")
    print("=" * 100)

    agents_by_module = summary.get("agents_by_module", {})
    failed_modules = summary.get("failed_modules", [])
    detailed_failures = summary.get("detailed_failures", {})

    total_faltantes = 0

    for module, expected_qtd in expected_core.items():
        atual_qtd = agents_by_module.get(module, 0)
        status = "✅" if atual_qtd >= expected_qtd else "❌"
        msg = f"{status} {module:<65} → {atual_qtd}/{expected_qtd}"

        if status == "❌":
            total_faltantes += expected_qtd - atual_qtd
            if module in failed_modules:
                detalhe = detailed_failures.get(module, "Erro não especificado")
                msg += f"    ⚠️ {detalhe}"
            else:
                msg += f"    ⚠️ Agentes ausentes ou lista vazia"

        print(msg)

    print("-" * 100)
    print(f"🎯 TOTAL DE AGENTES CORE FALTANTES: {total_faltantes}")
    print("=" * 100 + "\n\n")"
