"""
ALSHAM QUANTUM - Core Module
Módulo central para coordenação do sistema
"""
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class QuantumCore:
    """Núcleo central do ALSHAM QUANTUM"""

    def __init__(self):
        """
        Inicializa o núcleo central do ALSHAM QUANTUM.
        """
        self.version = "2.0.0"
        self.status = "operational"
        self.agents = {}
        self.message_bus = None
        self.initialized_at = datetime.now()
        self.config = {}
        self._on_register_callbacks = []
        self._on_remove_callbacks = []
    def get_info(self) -> Dict[str, Any]:
        """
        Retorna informações detalhadas do core (status, config, agentes).
        Returns:
            dict: Informações completas do core.
        """
        return {
            **self.get_status(),
            "config": self.config,
            "agents": list(self.agents.keys())
        }

    def update_agent(self, agent_id: str, agent_info: Dict[str, Any]) -> bool:
        """
        Atualiza informações de um agente já registrado.
        Args:
            agent_id: Identificador do agente.
            agent_info: Novas informações do agente.
        Returns:
            bool: True se atualizado, False se não encontrado.
        """
        if agent_id in self.agents:
            self.agents[agent_id].update(agent_info)
            logger.info(f"🔄 Agente atualizado: {agent_id}")
            return True
        logger.warning(f"⚠️ Tentativa de atualizar agente inexistente: {agent_id}")
        return False
        # Thread safety opcional
        try:
            from threading import Lock
            self._lock = Lock()
        except ImportError:
            self._lock = None
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
        Dispara callbacks de registro.
        Args:
            agent_id: Identificador único do agente.
            agent_info: Dicionário com informações do agente.
        Raises:
            ValueError: Se o agente já estiver registrado.
        """
        if self._lock:
            with self._lock:
                self._register_agent(agent_id, agent_info)
        else:
            self._register_agent(agent_id, agent_info)

    def _register_agent(self, agent_id: str, agent_info: Dict[str, Any]):
        if agent_id in self.agents:
            logger.warning(f"⚠️ Agente já registrado: {agent_id}")
            raise ValueError(f"Agente já registrado: {agent_id}")
        self.agents[agent_id] = agent_info
        logger.info(f"✅ Agente registrado: {agent_id}")
        for cb in self._on_register_callbacks:
            try:
                cb(agent_id, agent_info)
            except Exception as e:
                logger.error(f"Erro em callback de registro: {e}")

    def remove_agent(self, agent_id: str) -> bool:
        """
        Remove um agente do core. Dispara callbacks de remoção.
        Args:
            agent_id: Identificador do agente a ser removido.
        Returns:
            bool: True se removido, False se não encontrado.
        """
        if self._lock:
            with self._lock:
                return self._remove_agent(agent_id)
        else:
            return self._remove_agent(agent_id)

    def _remove_agent(self, agent_id: str) -> bool:
        if agent_id in self.agents:
            agent_info = self.agents[agent_id]
            del self.agents[agent_id]
            logger.info(f"🗑️ Agente removido: {agent_id}")
            for cb in self._on_remove_callbacks:
                try:
                    cb(agent_id, agent_info)
                except Exception as e:
                    logger.error(f"Erro em callback de remoção: {e}")
            return True
        logger.warning(f"⚠️ Tentativa de remover agente inexistente: {agent_id}")
        return False
    def clear_agents(self):
        """
        Remove todos os agentes registrados do core.
        """
        if self._lock:
            with self._lock:
                self.agents.clear()
        else:
            self.agents.clear()
        logger.info("🧹 Todos os agentes removidos do core.")

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
        Salva o estado do core (agentes, status e config) em arquivo JSON.
        Args:
            path: Caminho do arquivo para salvar o estado.
        """
        state = {
            "version": self.version,
            "status": self.status,
            "agents": self.agents,
            "initialized_at": self.initialized_at.isoformat(),
            "config": self.config
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            logger.info(f"💾 Estado do core salvo em {path}")
        except Exception as e:
            logger.error(f"Erro ao salvar estado do core: {e}")

    def load_state(self, path: str = "core_state.json") -> None:
        """
        Restaura o estado do core a partir de arquivo JSON.
        Args:
            path: Caminho do arquivo de estado salvo.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                state = json.load(f)
            self.version = state.get("version", self.version)
            self.status = state.get("status", self.status)
            self.agents = state.get("agents", {})
            self.initialized_at = datetime.fromisoformat(state.get("initialized_at", datetime.now().isoformat()))
            self.config = state.get("config", {})
            logger.info(f"♻️ Estado do core restaurado de {path}")
        except Exception as e:
            logger.error(f"Erro ao restaurar estado do core: {e}")
    def on_register(self, callback):
        """
        Registra callback a ser chamado ao registrar agente.
        Args:
            callback: Função (agent_id, agent_info) -> None
        """
        self._on_register_callbacks.append(callback)

    def on_remove(self, callback):
        """
        Registra callback a ser chamado ao remover agente.
        Args:
            callback: Função (agent_id, agent_info) -> None
        """
        self._on_remove_callbacks.append(callback)

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
