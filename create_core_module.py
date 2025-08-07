# CRIE ESTE ARQUIVO: create_core_module.py
"""
ALSHAM QUANTUM - Criação do Módulo Core Final
Resolve o último erro restante
"""
import os
from pathlib import Path

def create_core_module():
    """Cria módulo suna_alsham_core.core"""
    print("🔧 Criando módulo suna_alsham_core.core...")
    
    # Criar diretório
    core_dir = Path("suna_alsham_core")
    core_dir.mkdir(exist_ok=True)
    
    # __init__.py
    with open(core_dir / "__init__.py", "w") as f:
        f.write('"""ALSHAM Quantum Core Package"""\n__version__ = "2.0.0"\n')
    
    # core.py - Módulo principal
    core_content = '''"""
ALSHAM QUANTUM - Core Module
Módulo central para coordenação do sistema
"""
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class QuantumCore:
    """Núcleo central do ALSHAM QUANTUM"""
    
    def __init__(self):
        self.version = "2.0.0"
        self.status = "operational"
        self.agents = {}
        self.message_bus = None
        self.initialized_at = datetime.now()
        logger.info("🚀 QuantumCore inicializado")
    
    def set_message_bus(self, bus):
        """
        Define o message bus do sistema.
        Args:
            bus: Instância do message bus a ser usada pelo core.
        """
        self.message_bus = bus

    def register_agent(self, agent_id: str, agent_info: Dict[str, Any]):
        """
        Registra um agente no core. Não sobrescreve se já existir.
        Args:
            agent_id: Identificador único do agente.
            agent_info: Dicionário com informações do agente.
        Raises:
            ValueError: Se o agente já estiver registrado.
        """
        if agent_id in self.agents:
            logger.warning(f"⚠️ Agente já registrado: {agent_id}")
            raise ValueError(f"Agente já registrado: {agent_id}")
        self.agents[agent_id] = agent_info
        logger.info(f"✅ Agente registrado: {agent_id}")

    def remove_agent(self, agent_id: str) -> bool:
        """
        Remove um agente do core.
        Args:
            agent_id: Identificador do agente a ser removido.
        Returns:
            bool: True se removido, False se não encontrado.
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            logger.info(f"🗑️ Agente removido: {agent_id}")
            return True
        logger.warning(f"⚠️ Tentativa de remover agente inexistente: {agent_id}")
        return False

    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status do sistema.
        Returns:
            dict: Informações de status do core.
        """
        return {
            "version": self.version,
            "status": self.status,
            "agents_count": len(self.agents),
            "uptime": (datetime.now() - self.initialized_at).total_seconds()
        }

    def list_agents(self) -> List[str]:
        """
        Lista todos os agentes registrados.
        Returns:
            list: Lista de agent_id registrados.
        """
        return list(self.agents.keys())

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de um agente específico.
        Args:
            agent_id: Identificador do agente.
        Returns:
            dict ou None: Informações do agente ou None se não encontrado.
        """
        return self.agents.get(agent_id)

    def save_state(self, path: str = "core_state.json") -> None:
        """
        Salva o estado do core (agentes e status) em arquivo JSON.
        Args:
            path: Caminho do arquivo para salvar o estado.
        """
        import json
        state = {
            "version": self.version,
            "status": self.status,
            "agents": self.agents,
            "initialized_at": self.initialized_at.isoformat()
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        logger.info(f"💾 Estado do core salvo em {path}")

    def load_state(self, path: str = "core_state.json") -> None:
        """
        Restaura o estado do core a partir de arquivo JSON.
        Args:
            path: Caminho do arquivo de estado salvo.
        """
        import json
        from datetime import datetime
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
        self.version = state.get("version", self.version)
        self.status = state.get("status", self.status)
        self.agents = state.get("agents", {})
        self.initialized_at = datetime.fromisoformat(state.get("initialized_at", datetime.now().isoformat()))
        logger.info(f"♻️ Estado do core restaurado de {path}")

# Instância global
quantum_core = QuantumCore()

def get_core():
    """
    Retorna a instância global do core.
    Returns:
        QuantumCore: Instância global do core.
    """
    return quantum_core

def initialize_core():
    """
    Inicializa o core se necessário (compatível com sistemas legados).
    Returns:
        QuantumCore: Instância global do core.
    """
    return quantum_core

# Esqueleto de testes unitários (pode ser expandido)
def _test_core():
    core = QuantumCore()
    core.register_agent("ag1", {"type": "test"})
    assert "ag1" in core.list_agents()
    assert core.get_agent("ag1") == {"type": "test"}
    assert core.remove_agent("ag1") is True
    assert core.remove_agent("ag1") is False
    core.save_state("_test_core_state.json")
    core2 = QuantumCore()
    core2.load_state("_test_core_state.json")
    assert core2.version == core.version
    import os
    os.remove("_test_core_state.json")
    print("All core tests passed.")
'''
    
    with open(core_dir / "core.py", "w", encoding='utf-8') as f:
        f.write(core_content)
    
    print("✅ suna_alsham_core/core.py criado com sucesso!")
    print("▶️  Execute: python agent_loader.py")

if __name__ == "__main__":
    create_core_module()
