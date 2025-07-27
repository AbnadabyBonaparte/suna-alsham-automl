#!/usr/bin/env python3
"""
Módulo dos Agentes de Serviço - SUNA-ALSHAM

Define agentes que fornecem serviços fundamentais para a própria rede,
como comunicação avançada e tomada de decisão complexa.
"""

import asyncio
import logging
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set

# Import corrigido, apontando para o módulo central da rede
from suna_alsham_core.multi_agent_network import (
    BaseNetworkAgent,
    AgentMessage,
    AgentType,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)


class CommunicationProtocol(Enum):
    """Protocolos de comunicação suportados."""
    DIRECT = "direct"
    BROADCAST = "broadcast"
    REQUEST_RESPONSE = "request_response"


class DecisionStrategy(Enum):
    """Estratégias de tomada de decisão."""
    CONSENSUS = "consensus"
    VOTING = "voting"
    AUTONOMOUS = "autonomous"


class CommunicationAgent(BaseNetworkAgent):
    """
    Agente responsável pela comunicação e roteamento de mensagens.
    Atua como um hub de comunicação, gerenciando canais e protocolos.
    """

    def __init__(self, agent_id: str, agent_type: str, message_bus):
        """Inicializa o CommunicationAgent."""
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities.extend(["communication", "message_routing"])
        self.routing_table = defaultdict(list)
        logger.info(f"✅ {self.agent_id} inicializado com roteamento avançado.")

    async def _handle_request(self, message: AgentMessage):
        """Processa requisições de comunicação."""
        try:
            request_type = message.content.get("request_type")
            if request_type == "send_message":
                result = await self._process_communication_request(message.content)
                response = self.create_response(message, result)
                await self.message_bus.publish(response)
            else:
                await super()._handle_request(message)
        except Exception as e:
            logger.error(f"❌ Erro em {self.agent_id} ao processar requisição: {e}", exc_info=True)
            await self.message_bus.publish(self.create_error_response(message, str(e)))

    async def _process_communication_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa e roteia uma requisição de comunicação."""
        protocol = CommunicationProtocol(data.get("protocol", "direct"))
        message_content = data.get("message")
        sender = data.get("sender")
        recipients = data.get("recipients", [])

        if protocol == CommunicationProtocol.DIRECT:
            return await self._handle_direct_message(sender, recipients[0], message_content)
        elif protocol == CommunicationProtocol.BROADCAST:
            return await self._handle_broadcast_message(sender, message_content)
        
        return {"status": "error", "message": f"Protocolo {protocol.value} não suportado."}

    async def _handle_direct_message(self, sender: str, recipient: str, content: Dict) -> Dict:
        """Envia uma mensagem direta para um destinatário."""
        message_to_send = self.create_message(
            recipient_id=recipient,
            message_type=MessageType.NOTIFICATION,
            content=content,
        )
        await self.message_bus.publish(message_to_send)
        return {"status": "completed", "sent_to": 1}

    async def _handle_broadcast_message(self, sender: str, content: Dict) -> Dict:
        """Envia uma mensagem para todos os agentes conhecidos (exceto o remetente)."""
        broadcast_message = self.create_message(
            recipient_id="broadcast",
            message_type=MessageType.BROADCAST,
            content=content,
        )
        await self.message_bus.publish(broadcast_message)
        # O número real de agentes será determinado pelo MessageBus
        return {"status": "completed", "sent_to": "all"}


class DecisionAgent(BaseNetworkAgent):
    """
    Agente responsável por tomada de decisões complexas e colaborativas.
    """
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        """Inicializa o DecisionAgent."""
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities.extend(["decision_making", "consensus_building", "risk_assessment"])
        self.active_decisions = {}
        logger.info(f"✅ {self.agent_id} inicializado com estratégias de decisão.")

    async def _handle_request(self, message: AgentMessage):
        """Processa requisições de decisão."""
        try:
            request_type = message.content.get("request_type")
            if request_type == "make_decision":
                result = await self._process_decision_request(message.content)
                response = self.create_response(message, result)
                await self.message_bus.publish(response)
            else:
                await super()._handle_request(message)
        except Exception as e:
            logger.error(f"❌ Erro em {self.agent_id} ao processar decisão: {e}", exc_info=True)
            await self.message_bus.publish(self.create_error_response(message, str(e)))

    async def _process_decision_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma requisição de tomada de decisão."""
        strategy = DecisionStrategy(data.get("strategy", "autonomous"))
        options = data.get("options", [])
        
        if not options:
            return {"status": "error", "message": "Nenhuma opção fornecida para decisão."}

        if strategy == DecisionStrategy.AUTONOMOUS:
            # Lógica de decisão autônoma (ex: escolher a de maior score)
            best_option = max(options, key=lambda x: x.get("score", 0))
            confidence = best_option.get("score", 0) / 100.0
            rationale = "Decisão autônoma baseada no maior score."
        else:
            # Placeholder para outras estratégias mais complexas (votação, consenso)
            best_option = options[0]
            confidence = 0.75
            rationale = f"Decisão por estratégia {strategy.value} (implementação pendente)."
            
        return {
            "status": "completed",
            "selected_option": best_option,
            "confidence": confidence,
            "rationale": rationale
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
            agent = config["class"](config["id"], AgentType.SERVICE, message_bus)
            agents.append(agent)
        except Exception as e:
            logger.error(f"❌ Erro criando agente {config['id']}: {e}", exc_info=True)
    
    return agents
