import importlib
import logging

logger = logging.getLogger(__name__)

# Lista de nomes dos módulos de agentes a serem carregados
agent_modules = [
    "suna_alsham_core.agents.core_agents_v3",
    "suna_alsham_core.agents.specialized_agents",
    "suna_alsham_core.agents.system_agents",
    "suna_alsham_core.agents.service_agents",
    "suna_alsham_core.agents.meta_cognitive_agents",
    "suna_alsham_core.agents.ai_powered_agents",
    # ... outros módulos se necessário
]

async def initialize_all_agents(network) -> dict:
    """
    Inicializa todos os agentes listados e os registra na rede.
    Retorna um resumo da operação.
    """
    agents_loaded = 0
    failed_modules = []

    for module_name in agent_modules:
        try:
            logger.info(f"🔍 Carregando módulo: {module_name}")
            imported_module = importlib.import_module(module_name)

            if hasattr(imported_module, "create_agents"):
                agents = imported_module.create_agents(network.message_bus)
                for agent in agents:
                    network.register_agent(agent)
                    agents_loaded += 1
            else:
                logger.warning(f"⚠️ Módulo {module_name} não possui create_agents()")
                failed_modules.append(module_name)

        except Exception as e:
            logger.error(f"❌ Erro ao carregar {module_name}: {e}")
            failed_modules.append(module_name)

    summary = {
        "agents_loaded": agents_loaded,
        "failed_modules_count": len(failed_modules),
        "failed_modules": failed_modules
    }

    logger.info(f"✅ Agentes carregados: {agents_loaded}")
    logger.info(f"❌ Módulos com falha: {len(failed_modules)}")

    return {"summary": summary}
