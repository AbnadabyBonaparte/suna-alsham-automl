"""
ALSHAM QUANTUM - Módulo Support
Sistema Multi-Agente Nativo v2.0
Módulo: Support (Suporte ao Cliente)
Agentes: 2/2 ativos
"""

from typing import List, Dict, Any
import logging
import asyncio
from datetime import datetime

# Importação dos agentes nativos do módulo Support
from .knowledge_base_agent import KnowledgeBaseAgent
from .satisfaction_analyzer_agent import SatisfactionAnalyzerAgent

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Metadata do módulo
MODULE_INFO = {
    "name": "Support",
    "version": "2.0.0",
    "description": "Módulo de Suporte ao Cliente com Base de Conhecimento e Análise de Satisfação",
    "agents_count": 2,
    "status": "active",
    "last_update": "2025-01-08",
    "dependencies": ["native_only"],
    "capabilities": [
        "knowledge_management",
        "intelligent_search",
        "satisfaction_analysis",
        "sentiment_analysis",
        "customer_feedback",
        "support_automation"
    ]
}

# Lista de agentes disponíveis no módulo
AVAILABLE_AGENTS = [
    {
        "name": "KnowledgeBaseAgent",
        "class": KnowledgeBaseAgent,
        "description": "Agente de Base de Conhecimento Inteligente",
        "capabilities": ["knowledge_search", "content_management", "smart_retrieval"]
    },
    {
        "name": "SatisfactionAnalyzerAgent",
        "class": SatisfactionAnalyzerAgent,
        "description": "Agente de Análise de Satisfação e Sentimentos",
        "capabilities": ["sentiment_analysis", "satisfaction_scoring", "feedback_processing"]
    }
]

# Função obrigatória para criação dos agentes
def create_agents(config: Dict[str, Any] = None) -> List[Any]:
    """
    Cria e inicializa todos os agentes do módulo Support.
    
    Args:
        config: Configurações opcionais para os agentes
        
    Returns:
        Lista com instâncias dos agentes criados
    """
    agents = []
    
    try:
        # Configuração padrão se não fornecida
        if config is None:
            config = {
                "openai_api_key": "sk-placeholder",
                "debug_mode": False,
                "auto_start": True
            }
        
        logger.info("🚀 Iniciando criação dos agentes do módulo Support...")
        
        # 1. Knowledge Base Agent
        logger.info("📚 Criando Knowledge Base Agent...")
        knowledge_agent = KnowledgeBaseAgent(
            agent_id="knowledge_base_001",
            config=config
        )
        agents.append(knowledge_agent)
        logger.info("✅ Knowledge Base Agent criado com sucesso")
        
        # 2. Satisfaction Analyzer Agent
        logger.info("📊 Criando Satisfaction Analyzer Agent...")
        satisfaction_agent = SatisfactionAnalyzerAgent(
            agent_id="satisfaction_analyzer_001",
            config=config
        )
        agents.append(satisfaction_agent)
        logger.info("✅ Satisfaction Analyzer Agent criado com sucesso")
        
        logger.info(f"🎉 Módulo Support inicializado com {len(agents)} agentes")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar agentes do módulo Support: {str(e)}")
        raise

# Função para verificar status dos agentes
async def check_agents_status() -> Dict[str, Any]:
    """
    Verifica o status de todos os agentes do módulo.
    
    Returns:
        Dicionário com status de cada agente
    """
    try:
        agents = create_agents()
        status_report = {
            "module": "Support",
            "timestamp": datetime.now().isoformat(),
            "total_agents": len(agents),
            "agents_status": []
        }
        
        for agent in agents:
            agent_status = {
                "name": agent.__class__.__name__,
                "id": getattr(agent, 'agent_id', 'unknown'),
                "status": "active" if hasattr(agent, 'is_running') else "initialized",
                "capabilities": getattr(agent, 'capabilities', [])
            }
            status_report["agents_status"].append(agent_status)
        
        return status_report
        
    except Exception as e:
        logger.error(f"Erro ao verificar status dos agentes: {str(e)}")
        return {"error": str(e)}

# Função para obter informações do módulo
def get_module_info() -> Dict[str, Any]:
    """
    Retorna informações completas do módulo Support.
    
    Returns:
        Dicionário com informações do módulo
    """
    return {
        "module_info": MODULE_INFO,
        "available_agents": AVAILABLE_AGENTS,
        "creation_function": "create_agents",
        "status_function": "check_agents_status"
    }

# Exports principais do módulo
__all__ = [
    # Classes dos agentes
    'KnowledgeBaseAgent',
    'SatisfactionAnalyzerAgent',
    
    # Funções principais
    'create_agents',
    'check_agents_status',
    'get_module_info',
    
    # Metadados
    'MODULE_INFO',
    'AVAILABLE_AGENTS'
]

# Inicialização automática se executado diretamente
if __name__ == "__main__":
    print("🔧 ALSHAM QUANTUM - Módulo Support")
    print("=" * 50)
    
    # Mostra informações do módulo
    info = get_module_info()
    print(f"📋 Módulo: {info['module_info']['name']}")
    print(f"🔢 Versão: {info['module_info']['version']}")
    print(f"📝 Descrição: {info['module_info']['description']}")
    print(f"🤖 Agentes: {info['module_info']['agents_count']}")
    
    # Lista os agentes disponíveis
    print("\n📚 Agentes Disponíveis:")
    for agent_info in info['available_agents']:
        print(f"  • {agent_info['name']}: {agent_info['description']}")
    
    # Testa criação dos agentes
    print("\n🚀 Testando criação dos agentes...")
    try:
        test_agents = create_agents()
        print(f"✅ {len(test_agents)} agentes criados com sucesso!")
        
        # Mostra status
        print("\n📊 Status dos Agentes:")
        for agent in test_agents:
            print(f"  • {agent.__class__.__name__}: Inicializado")
            
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
    
    print("\n🎉 Módulo Support pronto para uso!")
