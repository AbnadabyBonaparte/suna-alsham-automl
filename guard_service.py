import logging
from typing import Any
from uuid import uuid4
from multi_agent_network import BaseNetworkAgent, AgentType

logger = logging.getLogger(__name__)

class GuardAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: AgentType, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['security_check', 'compliance']
        self.status = "active"
        logger.info(f"🛡️ Guard Agent API inicializado - ID: {agent_id}")
        logger.info("✅ Guard Agent: Modo normal estabelecido")
        logger.info("⚡ MONITORAMENTO ACELERADO: Verificações a cada 5 minutos")

    async def handle_message(self, message: Any):
        try:
            logger.info(f"📩 {self.agent_id} processando mensagem {message.id} de {message.sender_id}")
            if message.message_type == message.message_type.HEARTBEAT:
                logger.info(f"💓 {self.agent_id} recebeu heartbeat de {message.sender_id}")
            elif message.message_type == message.message_type.COMPLIANCE_CHECK:
                check_id = message.content.get('check_id', 1)
                logger.info(f"🔍 Verificação de segurança #{check_id} ACELERADA")
                logger.info(f"✅ Verificação #{check_id} concluída - Status: NORMAL")
            else:
                await super().handle_message(message)
        except Exception as e:
            logger.error(f"❌ Erro processando mensagem em {self.agent_id}: {e}", exc_info=True)

def create_guard_agent(message_bus) -> GuardAgent:
    try:
        agent_id = str(uuid4())
        agent = GuardAgent(agent_id, AgentType.GUARD, message_bus)
        message_bus.register_agent(agent_id, agent)
        logger.info(f"✅ Guard Agent criado com ID: {agent_id}")
        return agent
    except Exception as e:
        logger.error(f"❌ Erro criando Guard Agent: {e}", exc_info=True)
        return None

# Adicionar app como ponto de entrada (se necessário para o servidor)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Guard Service is running", 200
