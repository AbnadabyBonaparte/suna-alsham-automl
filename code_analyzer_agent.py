import logging
from typing import Dict, List
from multi_agent_network import BaseNetworkAgent, AgentType
import ast

logger = logging.getLogger(__name__)

class CodeAnalyzerAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['code_analysis', 'error_detection', 'suggestion_generation']
        self.status = 'active'  # ✅ ADICIONADO
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
            return {"file": file_path, "issues": issues, "suggestions": ["Revisar linhas indicadas", "Considerar refatoração"]}
        except Exception as e:
            logger.error(f"❌ Erro analisando {file_path}: {e}")
            return {"file": file_path, "issues": [str(e)], "suggestions": []}

def create_code_analyzer_agent(message_bus, num_instances=1) -> List['CodeAnalyzerAgent']:  # ✅ CORRIGIDO
    """Cria agente de análise de código - retorna lista para compatibilidade"""
    agents = []
    try:
        logger.info("🔍 Criando CodeAnalyzerAgent...")
        
        agent_id = "code_analyzer_001"  # ✅ ID fixo
        agent = CodeAnalyzerAgent(agent_id, AgentType.SPECIALIZED, message_bus)
        
        # Registrar no MessageBus
        if hasattr(message_bus, 'register_agent'):
            message_bus.register_agent(agent_id, agent)
        
        agents.append(agent)  # ✅ ADICIONADO À LISTA
        logger.info(f"✅ {len(agents)} agente de análise de código criado")
        return agents  # ✅ RETORNA LISTA
        
    except Exception as e:
        logger.error(f"❌ Erro criando CodeAnalyzerAgent: {e}")
        return []  # ✅ RETORNA LISTA VAZIA
