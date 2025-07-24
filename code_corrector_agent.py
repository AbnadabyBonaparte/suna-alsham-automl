import logging
from typing import List, Dict
from multi_agent_network import BaseNetworkAgent, AgentType
from uuid import uuid4

logger = logging.getLogger(__name__)

class CodeCorrectorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['code_correction', 'optimization']
        logger.info(f"✅ {self.agent_id} inicializado")

    def apply_correction(self, file_path: str, suggestions: List[str]) -> Dict:
        try:
            with open(file_path, 'r') as file:
                code = file.read()
            # Simulação de correção (substituir por lógica real)
            corrected_code = f"# Correção aplicada: {suggestions[0]}\n{code}"
            with open(file_path, 'w') as file:
                file.write(corrected_code)
            logger.info(f"🔧 Correção aplicada em {file_path}")
            return {"file": file_path, "status": "success", "changes": suggestions}
        except Exception as e:
            logger.error(f"❌ Erro aplicando correção em {file_path}: {e}")
            return {"file": file_path, "status": "failed", "error": str(e)}

def create_code_corrector_agent(message_bus) -> 'CodeCorrectorAgent':
    try:
        agent_id = f"code_corrector_{uuid4()}"
        agent = CodeCorrectorAgent(agent_id, AgentType.SPECIALIZED, message_bus)
        message_bus.register_agent(agent_id, agent)
        logger.info(f"✅ {agent_id} criado")
        return agent
    except Exception as e:
        logger.error(f"❌ Erro criando CodeCorrectorAgent: {e}")
        return None
