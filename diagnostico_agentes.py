#!/usr/bin/env python3
"""
🔍 Diagnóstico de Agentes Quantum - ALSHAM v2.0
Verifica todos os módulos em 'suna_alsham_core/agents' e lista:
- Módulos com create_agents ausente
- Módulos com retorno vazio ou inválido
- Agentes efetivamente criados
"""

import os
import importlib
import inspect
import traceback

from typing import Any, List
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, MessageBus

# Caminho base dos módulos de agente
AGENT_BASE_PATH = "suna_alsham_core/agents"
AGENT_MODULE_PREFIX = "suna_alsham_core.agents"

# Resultado
summary = {
    "successfully_loaded": [],
    "missing_create_agents": [],
    "empty_return": [],
    "invalid_return": [],
    "exceptions": {},
    "agents_created": []
}

# Mock de message_bus só para teste
class DummyMessageBus(MessageBus):
    def publish(self, message): pass

dummy_bus = DummyMessageBus()

# Função para carregar e diagnosticar cada módulo
def diagnosticar_agentes():
    print("🔎 Iniciando diagnóstico...\n")
    for filename in os.listdir(AGENT_BASE_PATH):
        if not filename.endswith(".py") or filename.startswith("__"):
            continue
        
        module_name = filename[:-3]  # remove .py
        full_module_path = f"{AGENT_MODULE_PREFIX}.{module_name}"
        
        try:
            module = importlib.import_module(full_module_path)
            create_fn = getattr(module, "create_agents", None)

            if not create_fn or not callable(create_fn):
                summary["missing_create_agents"].append(full_module_path)
                print(f"⚠️ {full_module_path} não possui create_agents()")
                continue
            
            result = create_fn(dummy_bus)

            if result is None:
                summary["empty_return"].append(full_module_path)
                print(f"⚠️ {full_module_path} retornou None")
            elif isinstance(result, list):
                if not result:
                    summary["empty_return"].append(full_module_path)
                    print(f"⚠️ {full_module_path} retornou lista vazia")
                else:
                    valid_agents = [a for a in result if isinstance(a, BaseNetworkAgent)]
                    if valid_agents:
                        summary["successfully_loaded"].append(full_module_path)
                        for agent in valid_agents:
                            summary["agents_created"].append(agent.agent_id)
                            print(f"✅ {agent.agent_id} carregado de {full_module_path}")
                    else:
                        summary["invalid_return"].append(full_module_path)
                        print(f"❌ {full_module_path} retornou lista sem agentes válidos")
            else:
                summary["invalid_return"].append(full_module_path)
                print(f"❌ {full_module_path} retornou tipo inválido: {type(result)}")
        
        except Exception as e:
            summary["exceptions"][full_module_path] = traceback.format_exc()
            print(f"💥 ERRO ao importar {full_module_path}:\n{e}\n")

    print("\n🧾 Diagnóstico concluído.\n")
    print("📊 RESUMO FINAL:")
    print(f"✅ Módulos OK: {len(summary['successfully_loaded'])}")
    print(f"⚠️ Ausentes: {len(summary['missing_create_agents'])}")
    print(f"⚠️ Vazios: {len(summary['empty_return'])}")
    print(f"❌ Inválidos: {len(summary['invalid_return'])}")
    print(f"💥 Com erro: {len(summary['exceptions'])}")
    print(f"🤖 Agentes criados: {summary['agents_created']}")

if __name__ == "__main__":
    diagnosticar_agentes()
