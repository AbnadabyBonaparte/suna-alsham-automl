"""
ALSHAM QUANTUM - Base Agent
Classe base para todos os agentes do sistema
"""
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
        
        logger.info(f"🚀 BaseAgent {self.agent_id} inicializado")
    
    def set_message_bus(self, bus):
        """Define o message bus"""
        self.message_bus = bus
        
    def set_config(self, config: Dict[str, Any]):
        """Define configuração do agente"""
        self.config.update(config)
        
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do agente"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "uptime": (datetime.now() - self.created_at).total_seconds(),
            "metrics": self.metrics
        }
    
    def start(self):
        """Inicia o agente"""
        self.status = "running"
        logger.info(f"▶️ Agente {self.agent_id} iniciado")
        
    def stop(self):
        """Para o agente"""
        self.status = "stopped"
        logger.info(f"⏹️ Agente {self.agent_id} parado")
    
    def health_check(self) -> bool:
        """Verifica saúde do agente"""
        return self.status == "running"
    
    @abstractmethod
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma mensagem (deve ser implementado pelos agentes filhos)"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Retorna lista de capacidades do agente"""
        pass

class QuantumAgent(BaseAgent):
    """Agente quantum com funcionalidades estendidas"""
    
    def __init__(self, agent_id: str, name: str = None):
        super().__init__(agent_id, name)
        self.quantum_state = "superposition"
        self.entangled_agents = []
        self.quantum_properties = {
            "coherence_time": 1000.0,
            "fidelity": 0.99,
            "entanglement_strength": 0.8
        }
        
        logger.info(f"⚡ QuantumAgent {self.agent_id} inicializado com estado {self.quantum_state}")
    
    def entangle_with(self, other_agent_id: str):
        """Cria entrelaçamento quântico com outro agente"""
        if other_agent_id not in self.entangled_agents:
            self.entangled_agents.append(other_agent_id)
            logger.info(f"🔗 Agente {self.agent_id} entrelaçado com {other_agent_id}")
    
    def collapse_state(self, state: str):
        """Colapsa o estado quântico"""
        old_state = self.quantum_state
        self.quantum_state = state
        logger.info(f"⚡ Estado quântico de {self.agent_id}: {old_state} → {state}")
    
    def get_quantum_status(self) -> Dict[str, Any]:
        """Retorna status quântico do agente"""
        status = self.get_status()
        status.update({
            "quantum_state": self.quantum_state,
            "entangled_agents": self.entangled_agents,
            "quantum_properties": self.quantum_properties
        })
        return status
    
    def superposition(self, states: List[str]):
        """Coloca o agente em superposição de estados"""
        self.quantum_state = f"superposition({'+'.join(states)})"
        logger.info(f"🌀 Agente {self.agent_id} em superposição: {states}")
    
    def measure(self) -> str:
        """Realiza medição quântica colapsando o estado"""
        import random
        
        if "superposition" in self.quantum_state:
            # Extrair estados da superposição
            states_str = self.quantum_state.replace("superposition(", "").replace(")", "")
            possible_states = states_str.split("+")
            collapsed_state = random.choice(possible_states)
            self.collapse_state(collapsed_state)
            return collapsed_state
        
        return self.quantum_state
    
    def quantum_teleport(self, message: Dict[str, Any], target_agent_id: str):
        """Teleporte quântico de informação"""
        if target_agent_id in self.entangled_agents:
            logger.info(f"📡 Teleportando mensagem de {self.agent_id} para {target_agent_id}")
            # Implementar teleporte via entrelaçamento
            return True
        else:
            logger.warning(f"⚠️ Não é possível teleportar para {target_agent_id}: não entrelaçado")
            return False
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagem com lógica quântica"""
        # Implementação padrão - pode ser sobrescrita
        return {
            "status": "processed",
            "agent_id": self.agent_id,
            "quantum_state": self.quantum_state,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_capabilities(self) -> List[str]:
        """Retorna capacidades do agente quântico"""
        return [
            "quantum_processing",
            "entanglement",
            "superposition",
            "quantum_measurement",
            "quantum_teleportation"
        ]

class StandardAgent(BaseAgent):
    """Agente padrão não-quântico"""
    
    def __init__(self, agent_id: str, name: str = None):
        super().__init__(agent_id, name)
        self.processing_mode = "classical"
        
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagem com lógica clássica"""
        return {
            "status": "processed",
            "agent_id": self.agent_id,
            "processing_mode": self.processing_mode,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_capabilities(self) -> List[str]:
        """Retorna capacidades do agente padrão"""
        return [
            "message_processing",
            "task_execution",
            "status_reporting"
        ]

class ServiceAgent(BaseAgent):
    """Agente de serviço especializado"""
    
    def __init__(self, agent_id: str, name: str = None, service_type: str = "generic"):
        super().__init__(agent_id, name)
        self.service_type = service_type
        self.endpoints = {}
        
    def register_endpoint(self, endpoint: str, handler):
        """
        Registra um endpoint de serviço de forma segura.
        Args:
            endpoint (str): Nome do endpoint.
            handler (Callable): Função que processa mensagens para este endpoint.
        Raises:
            ValueError: Se o endpoint já estiver registrado.
        """
        if not callable(handler):
            logger.error(f"Handler para endpoint '{endpoint}' não é callable.")
            raise TypeError(f"Handler para endpoint '{endpoint}' deve ser callable.")
        if endpoint in self.endpoints:
            logger.warning(f"Endpoint '{endpoint}' já registrado no agente {self.agent_id}.")
            raise ValueError(f"Endpoint '{endpoint}' já registrado.")
        self.endpoints[endpoint] = handler
        logger.info(f"🔌 Endpoint '{endpoint}' registrado no agente {self.agent_id}")

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa mensagens de serviço, roteando para o endpoint correto.
        Args:
            message (dict): Mensagem recebida.
        Returns:
            dict: Resposta do endpoint ou mensagem padrão de erro.
        """
        endpoint = message.get("endpoint")
        if endpoint:
            handler = self.endpoints.get(endpoint)
            if handler:
                try:
                    # Suporte a handlers async e sync
                    if hasattr(handler, "__call__"):
                        import inspect
                        if inspect.iscoroutinefunction(handler):
                            import asyncio
                            return asyncio.run(handler(message))
                        else:
                            return handler(message)
                except Exception as e:
                    logger.error(f"Erro ao processar endpoint '{endpoint}' no agente {self.agent_id}: {e}")
                    return {
                        "status": "error",
                        "error": str(e),
                        "agent_id": self.agent_id,
                        "service_type": self.service_type,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                logger.warning(f"Endpoint '{endpoint}' não encontrado no agente {self.agent_id}.")
                return {
                    "status": "error",
                    "error": f"Endpoint '{endpoint}' não encontrado.",
                    "agent_id": self.agent_id,
                    "service_type": self.service_type,
                    "timestamp": datetime.now().isoformat()
                }
        else:
            logger.warning(f"Mensagem sem endpoint recebida pelo agente {self.agent_id}.")
            return {
                "status": "error",
                "error": "Mensagem sem endpoint especificado.",
                "agent_id": self.agent_id,
                "service_type": self.service_type,
                "timestamp": datetime.now().isoformat()
            }

    def get_capabilities(self) -> List[str]:
        """
        Retorna capacidades do agente de serviço, incluindo endpoints registrados.
        Returns:
            list: Lista de capacidades e endpoints.
        """
        return [
            "service_hosting",
            "endpoint_management",
            "request_routing",
            f"{self.service_type}_service"
        ] + [f"endpoint:{ep}" for ep in self.endpoints.keys()]
