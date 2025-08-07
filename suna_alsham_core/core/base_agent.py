"""ALSHAM QUANTUM - Base Agent"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Classe base abstrata para todos os agentes ALSHAM QUANTUM"""
    
    def __init__(self, agent_id: str, name: str = None):
        self.agent_id = agent_id
        self.name = name or agent_id
        self.status = "initialized"
        self.created_at = datetime.now()
        self.message_bus = None
        self.config = {}
        self.metrics = {}
        
    def set_message_bus(self, bus):
        """Define o message bus"""
        self.message_bus = bus
        
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do agente"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "uptime": (datetime.now() - self.created_at).total_seconds()
        }
    
    @abstractmethod
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma mensagem"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Retorna lista de capacidades do agente"""
        pass
