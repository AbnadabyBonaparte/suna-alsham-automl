"""ALSHAM QUANTUM - Base Agent"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Classe base abstrata para todos os agentes ALSHAM QUANTUM"""
    
    def __init__(self, agent_id: str, name: str = None):
        """
        Inicializa o agente base.
        Args:
            agent_id: Identificador único do agente.
            name: Nome amigável do agente (opcional).
        """
        self.agent_id = agent_id
        self.name = name or agent_id
        self.status = "initialized"
        self.created_at = datetime.now()
        self.message_bus = None
        self.config = {}
        self.metrics = {}
        self._on_status_change_callbacks = []
        # Thread safety opcional
        try:
            from threading import Lock
            self._lock = Lock()
        except ImportError:
            self._lock = None
        
    def set_message_bus(self, bus):
        """
        Define o message bus do agente.
        Args:
            bus: Instância do message bus.
        """
        self.message_bus = bus
        
    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status do agente.
        Returns:
            dict: Informações de status do agente.
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "uptime": (datetime.now() - self.created_at).total_seconds()
        }
    def get_info(self) -> Dict[str, Any]:
        """
        Retorna informações detalhadas do agente.
        Returns:
            dict: Informações completas do agente.
        """
        return {
            **self.get_status(),
            "config": self.config,
            "metrics": self.metrics,
            "capabilities": self.get_capabilities() if hasattr(self, 'get_capabilities') else []
        }

    def update_config(self, config: Dict[str, Any]):
        """
        Atualiza a configuração do agente.
        Args:
            config: Dicionário de configurações a atualizar.
        """
        if self._lock:
            with self._lock:
                self.config.update(config)
        else:
            self.config.update(config)

    def update_metrics(self, metrics: Dict[str, Any]):
        """
        Atualiza as métricas do agente.
        Args:
            metrics: Dicionário de métricas a atualizar.
        """
        if self._lock:
            with self._lock:
                self.metrics.update(metrics)
        else:
            self.metrics.update(metrics)

    def set_status(self, status: str):
        """
        Atualiza o status do agente e dispara callbacks.
        Args:
            status: Novo status do agente.
        """
        self.status = status
        for cb in self._on_status_change_callbacks:
            try:
                cb(self.agent_id, status)
            except Exception as e:
                logger.error(f"Erro em callback de status: {e}")

    def on_status_change(self, callback):
        """
        Registra callback para mudança de status.
        Args:
            callback: Função (agent_id, status) -> None
        """
        self._on_status_change_callbacks.append(callback)

    def shutdown(self):
        """
        Realiza procedimentos de shutdown/cleanup do agente.
        Pode ser sobrescrito por subclasses.
        """
        self.set_status("shutdown")
        logger.info(f"Agente {self.agent_id} finalizado.")
    
    @abstractmethod
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma mensagem"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Retorna lista de capacidades do agente"""
        pass
