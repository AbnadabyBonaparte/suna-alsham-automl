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

from typing import Any, Dict

async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    """
    Inicializa todos os agentes listados em agent_modules e os registra na rede fornecida.
    Para cada módulo, tenta importar e executar create_agents(message_bus), registrando cada agente retornado.
    Retorna um dicionário-resumo da operação, incluindo contagem de agentes carregados e módulos com falha.

    :param network: Instância da rede (deve possuir atributo message_bus e método register_agent).
    :return: Dicionário com resumo da operação.
    """
    agents_loaded: int = 0
    failed_modules: list = []
    detailed_failures: Dict[str, str] = {}

    for module_name in agent_modules:
        try:
            logger.info(f"🔍 Carregando módulo: {module_name}")
            imported_module = importlib.import_module(module_name)

            if hasattr(imported_module, "create_agents"):
                agents = imported_module.create_agents(network.message_bus)
                if not isinstance(agents, list):
                    logger.warning(f"⚠️ create_agents de {module_name} não retornou uma lista.")
                    failed_modules.append(module_name)
                    detailed_failures[module_name] = "create_agents não retornou lista"
                    continue
                for agent in agents:
                    try:
                        network.register_agent(agent)
                        agents_loaded += 1
                        logger.info(f"✅ Agente {getattr(agent, 'agent_id', str(agent))} registrado com sucesso.")
                    except Exception as agent_exc:
                        logger.error(f"❌ Erro ao registrar agente do módulo {module_name}: {agent_exc}", exc_info=True)
                        failed_modules.append(module_name)
                        detailed_failures[module_name] = f"Erro ao registrar agente: {agent_exc}"
            else:
                logger.warning(f"⚠️ Módulo {module_name} não possui create_agents()")
                failed_modules.append(module_name)
                detailed_failures[module_name] = "create_agents não encontrado"

        except Exception as e:
            logger.error(f"❌ Erro ao carregar {module_name}: {e}", exc_info=True)
            failed_modules.append(module_name)
            detailed_failures[module_name] = str(e)

    summary = {
        "agents_loaded": agents_loaded,
        "failed_modules_count": len(set(failed_modules)),
        "failed_modules": list(set(failed_modules)),
        "detailed_failures": detailed_failures
    }

    logger.info(f"✅ Agentes carregados: {agents_loaded}")
    if failed_modules:
        logger.warning(f"❌ Módulos com falha: {len(set(failed_modules))} - {set(failed_modules)}")
    else:
        logger.info("🎉 Todos os módulos carregados com sucesso!")

    return {"summary": summary}
