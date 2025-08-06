#!/usr/bin/env python3
"""
Módulo dos Agentes de Serviço - SUNA-ALSHAM

[Fase 2] - Revisão Final. Alinhado com a BaseNetworkAgent fortalecida.
Define agentes que fornecem serviços fundamentais para a própria rede,
como comunicação avançada e tomada de decisão complexa.
"""

import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Set, Optional

# Import alinhado com a Fase 1
from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


# --- Enums e Dataclasses (sem alteração) ---

class CommunicationProtocol(Enum):
    """Protocolos de comunicação suportados."""
    DIRECT = "direct"
    BROADCAST = "broadcast"
    REQUEST_RESPONSE = "request_response"


class DecisionStrategy(Enum):
    """Estratégias de tomada de decisão."""
    AUTONOMOUS = "autonomous"
    VOTING = "voting"


# --- Classes Principais dos Agentes ---

class CommunicationAgent(BaseNetworkAgent):
    """
    Agente responsável pela comunicação e roteamento de mensagens.
    Atua como um hub de comunicação, gerenciando canais e protocolos.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o CommunicationAgent."""
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.append("message_routing")
        logger.info(f"✅ {self.agent_id} (Comunicação) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de comunicação."""
        if message.message_type != MessageType.REQUEST:
            return

        request_type = message.content.get("request_type")
        if request_type == "route_message":
            result = await self._process_communication_request(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            await self.message_bus.publish(self.create_error_response(message, "Ação de comunicação desconhecida"))

    async def _process_communication_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """[AUTENTICIDADE] Processa e roteia uma requisição de comunicação."""
        logger.info(f"[Simulação] Roteando mensagem para {data.get('recipients')}")
        return {"status": "completed_simulated", "message": "Mensagem roteada (simulado)."}


class DecisionAgent(BaseNetworkAgent):
    """
    Agente responsável por tomada de decisões complexas e colaborativas.
    """

    def __init__(self, agent_id: str, message_bus):
        """Inicializa o DecisionAgent."""
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.append("decision_making")
        logger.info(f"✅ {self.agent_id} (Decisão) inicializado.")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de decisão."""
        if message.message_type != MessageType.REQUEST:
            return
            
        if message.content.get("request_type") == "make_decision":
            result = await self._process_decision_request(message.content)
            await self.message_bus.publish(self.create_response(message, result))
        else:
            await self.message_bus.publish(self.create_error_response(message, "Ação de decisão desconhecida"))

    async def _process_decision_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [LÓGICA REAL] Processa uma requisição de tomada de decisão.
        """
        strategy = DecisionStrategy(data.get("strategy", "autonomous"))
        options = data.get("options", [])
        
        if not options:
            return {"status": "error", "message": "Nenhuma opção fornecida para decisão."}

        best_option = max(options, key=lambda x: x.get("score", 0))
        
        return {
            "status": "completed",
            "selected_option": best_option,
            "confidence": best_option.get("score", 0) / 100.0,
            "rationale": f"Decisão autônoma baseada no maior score (Estratégia: {strategy.value})."
        }


def create_service_agents(message_bus) -> List[BaseNetworkAgent]:
    """
    Cria os agentes de serviço para o núcleo do sistema.
    """
    agents = []
    logger.info("🔧 Criando agentes de Serviço...")
    
    agent_configs = [
        {"id": "communication_001", "class": CommunicationAgent},
        {"id": "decision_001", "class": DecisionAgent},
    ]
    
    for config in agent_configs:
        try:
            agent = config["class"](config["id"], message_bus)
            agents.append(agent)
        except Exception as e:
            logger.error(f"❌ Erro criando agente de serviço {config['id']}: {e}", exc_info=True)
    
    return agents


# --- FACTORY FUNCTION OBRIGATÓRIA PARA O BOOTSTRAP ---

def create_agents():
    from suna_alsham_core.message_bus import global_message_bus
    return create_service_agents(global_message_bus)
