#!/usr/bin/env python3
"""
API Gateway – Entrada Universal do SUNA-ALSHAM.
Aceita JSON estruturado e texto livre.
"""

import logging
from typing import Any, Dict, List
from suna_alsham_core.multi_agent_network import AgentMessage, AgentType, BaseNetworkAgent, MessageType

logger = logging.getLogger(__name__)

class APIGatewayAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        logger.info(f"🚪 {self.agent_id} inicializado.")

    async def handle_incoming(self, payload: Dict[str, Any]):
        msg = self.create_message(
            recipient_id="orchestrator_001",
            message_type=MessageType.REQUEST,
            content=payload
        )
        await self.message_bus.publish(msg)

def create_api_gateway_agent(message_bus) -> List[BaseNetworkAgent]:
    return [APIGatewayAgent("api_gateway_001", message_bus)]
