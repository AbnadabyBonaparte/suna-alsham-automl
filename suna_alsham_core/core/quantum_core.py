"""ALSHAM QUANTUM - Quantum Core"""
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
    
    def register_agent(self, agent_id: str, agent_info: Dict[str, Any]):
        """Registra um agente no core"""
        self.agents[agent_id] = agent_info
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do sistema"""
        return {
            "version": self.version,
            "status": self.status,
            "agents_count": len(self.agents)
        }

# Instância global
quantum_core = QuantumCore()

def get_core():
    return quantum_core

def initialize_core():
    return quantum_core
