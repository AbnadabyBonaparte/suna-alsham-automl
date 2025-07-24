import logging
from typing import Dict, List
from multi_agent_network import BaseNetworkAgent, AgentType
import ast
from uuid import uuid4

logger = logging.getLogger(__name__)

class CodeAnalyzerAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['code_analysis', 'error_detection']
        logger.info(f"✅ {self.agent_id} inicializado")

    def analyze_code_quality(self, file_path: str) -> Dict:
        try:
            with open(file_path, 'r') as file:
                code = file.read()
            tree = ast.parse(code)
            issues = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Raise):
                    issues.append(f"Possível erro detectado em {file_path}: Linha {node.lineno}")
            logger.info(f"🔍 Análise de {file_path} concluída - {len(issues)} problemas encontrados")
            return {"file": file_path, "issues": issues, "suggestions": ["Revisar linhas indicadas"]}
        except Exception as e:
            logger.error(f"❌ Erro analisando {file_path}: {e}")
            return {"file": file_path, "issues": [str(e)], "suggestions": []}

def create_code_analyzer_agent(message_bus) -> 'CodeAnalyzerAgent':
    try:
        agent_id = f"code_analyzer_{uuid4()}"
        agent = CodeAnalyzerAgent(agent_id, AgentType.SPECIALIZED, message_bus)
        message_bus.register_agent(agent_id, agent)
        logger.info(f"✅ {agent_id} criado")
        return agent
    except Exception as e:
        logger.error(f"❌ Erro criando CodeAnalyzerAgent: {e}")
        return None
