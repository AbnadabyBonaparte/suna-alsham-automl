# domain_modules/support/__init__.py
"""
ALSHAM QUANTUM - Support Module
Sistema Multi-Agente Nativo v2.0
Module: Support (Customer Support)
Agents: 5/5 active
"""

from typing import List, Dict, Any
import logging
import asyncio
from datetime import datetime

# Importação dos agentes nativos do módulo Support
from .support_orchestrator_agent import SupportOrchestratorAgent
from .chatbot_agent import ChatbotAgent
from .ticket_manager_agent import TicketManagerAgent
from .knowledge_base_agent import KnowledgeBaseAgent
from .satisfaction_analyzer_agent import SatisfactionAnalyzerAgent

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Metadata do módulo
MODULE_INFO = {
    "name": "Support",
    "version": "2.0.0",
    "description": "Customer Support Module with AI-powered agents",
    "agents_count": 5,
    "status": "active",
    "last_update": "2025-01-08",
    "dependencies": ["native_only"],
    "capabilities": [
        "support_orchestration",
        "intelligent_chatbot",
        "ticket_management",
        "knowledge_management",
        "satisfaction_analysis",
        "sentiment_analysis",
        "customer_feedback",
        "support_automation"
    ]
}

# Lista de agentes disponíveis no módulo
AVAILABLE_AGENTS = [
    {
        "name": "SupportOrchestratorAgent",
        "class": SupportOrchestratorAgent,
        "description": "Support System Orchestrator Agent",
        "capabilities": ["workflow_orchestration", "agent_coordination", "support_management"]
    },
    {
        "name": "ChatbotAgent", 
        "class": ChatbotAgent,
        "description": "AI-Powered Customer Chatbot Agent",
        "capabilities": ["natural_language_processing", "automated_responses", "customer_interaction"]
    },
    {
        "name": "TicketManagerAgent",
        "class": TicketManagerAgent, 
        "description": "Intelligent Ticket Management Agent",
        "capabilities": ["ticket_routing", "priority_assessment", "workflow_automation"]
    },
    {
        "name": "KnowledgeBaseAgent",
        "class": KnowledgeBaseAgent,
        "description": "Intelligent Knowledge Base Agent", 
        "capabilities": ["knowledge_search", "content_management", "smart_retrieval"]
    },
    {
        "name": "SatisfactionAnalyzerAgent",
        "class": SatisfactionAnalyzerAgent,
        "description": "Customer Satisfaction Analysis Agent",
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
        
        # 1. Support Orchestrator Agent
        logger.info("🎯 Criando Support Orchestrator Agent...")
        orchestrator_agent = SupportOrchestratorAgent(
            agent_id="support_orchestrator_001",
            config=config
        )
        agents.append(orchestrator_agent)
        logger.info("✅ Support Orchestrator Agent criado com sucesso")
        
        # 2. Chatbot Agent
        logger.info("🤖 Criando Chatbot Agent...")
        chatbot_agent = ChatbotAgent(
            agent_id="chatbot_001",
            config=config
        )
        agents.append(chatbot_agent)
        logger.info("✅ Chatbot Agent criado com sucesso")
        
        # 3. Ticket Manager Agent
        logger.info("🎫 Criando Ticket Manager Agent...")
        ticket_agent = TicketManagerAgent(
            agent_id="ticket_manager_001",
            config=config
        )
        agents.append(ticket_agent)
        logger.info("✅ Ticket Manager Agent criado com sucesso")
        
        # 4. Knowledge Base Agent
        logger.info("📚 Criando Knowledge Base Agent...")
        knowledge_agent = KnowledgeBaseAgent(
            agent_id="knowledge_base_001",
            config=config
        )
        agents.append(knowledge_agent)
        logger.info("✅ Knowledge Base Agent criado com sucesso")
        
        # 5. Satisfaction Analyzer Agent
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
    'SupportOrchestratorAgent',
    'ChatbotAgent', 
    'TicketManagerAgent',
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
    print("🔧 ALSHAM QUANTUM - Support Module")
    print("=" * 50)
    
    # Mostra informações do módulo
    info = get_module_info()
    print(f"📋 Module: {info['module_info']['name']}")
    print(f"🔢 Version: {info['module_info']['version']}")
    print(f"📝 Description: {info['module_info']['description']}")
    print(f"🤖 Agents: {info['module_info']['agents_count']}")
    
    # Lista os agentes disponíveis
    print("\n📚 Available Agents:")
    for agent_info in info['available_agents']:
        print(f"  • {agent_info['name']}: {agent_info['description']}")
    
    # Testa criação dos agentes
    print("\n🚀 Testing agent creation...")
    try:
        test_agents = create_agents()
        print(f"✅ {len(test_agents)} agents created successfully!")
        
        # Mostra status
        print("\n📊 Agents Status:")
        for agent in test_agents:
            print(f"  • {agent.__class__.__name__}: Initialized")
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
    
    print("\n🎉 Support Module ready for use!")
