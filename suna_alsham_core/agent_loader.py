#!/usr/bin/env python3
"""
Módulo Carregador de Agentes - SUNA-ALSHAM

[Versão Corrigida] - Utiliza injeção de dependência para evitar import circular.
"""
import importlib
import logging
import pkgutil
from pathlib import Path
from typing import Any, Dict, List

# A importação que causava o erro foi REMOVIDA.
# Importamos apenas a classe base, que não causa problemas.
from suna_alsham_core.multi_agent_network import BaseNetworkAgent

logger = logging.getLogger(__name__)

# A função agora espera receber o objeto 'network' completo.
async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    """
    Descobre e inicializa dinamicamente todos os agentes do núcleo e dos domínios.
    """
    agents_loaded = 0
    failed_modules = []
    
    # Caminhos para os módulos do núcleo e de domínio
    core_path = Path(__file__).parent
    domain_path = core_path.parent / "domain_modules"
    
    module_paths = [core_path, domain_path]
    
    for path in module_paths:
        for _, module_name, _ in pkgutil.iter_modules([str(path)]):
            # Ignora o próprio loader e o módulo de rede para evitar problemas
            if module_name in ["agent_loader", "multi_agent_network"]:
                continue
            
            try:
                # Constrói o caminho completo do módulo para importação
                full_module_name = f"{path.name}.{module_name}"
                if "suna_alsham_core" not in full_module_name:
                    full_module_name = f"suna_alsham_core.{module_name}" if path == core_path else f"domain_modules.{module_name}"

                module = importlib.import_module(full_module_name)
                
                # Procura por uma função 'create_*_agents' no módulo
                create_func_name = f"create_{module_name.replace('_agent', '').replace('_agents', '')}_agents"
                
                if hasattr(module, create_func_name):
                    create_func = getattr(module, create_func_name)
                    # Passa o message_bus da network para a função de criação
                    agents: List[BaseNetworkAgent] = create_func(network.message_bus)
                    
                    for agent in agents:
                        # Registra o agente DIRETAMENTE na network
                        network.register_agent(agent)
                        agents_loaded += 1
                        
            except Exception as e:
                logger.error(f"Falha ao carregar ou inicializar o módulo de agentes '{module_name}': {e}", exc_info=True)
                failed_modules.append(module_name)

    logger.info(f"Carregamento de agentes concluído. {agents_loaded} agentes carregados.")
    return {
        "summary": {"agents_loaded": agents_loaded, "failed_modules_count": len(failed_modules)},
        "failed_modules": failed_modules,
    }
