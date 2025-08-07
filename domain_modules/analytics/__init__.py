"""
Módulo Analytics - ALSHAM QUANTUM
Agentes para coleta, análise e visualização de dados
"""

from .data_collector_agent import create_agents as create_data_collector_agents
from .analytics_orchestrator_agent import create_agents as create_orchestrator_agents
from .predictive_analysis_agent import create_agents as create_predictive_agents
from .reporting_visualization_agent import create_agents as create_visualization_agents

def create_agents(config=None):
    """Cria todos os agentes do módulo Analytics"""
    config = config or {}
    
    all_agents = {}
    all_agents.update(create_data_collector_agents(config.get('data_collector', {})))
    all_agents.update(create_orchestrator_agents(config.get('orchestrator', {})))
    all_agents.update(create_predictive_agents(config.get('predictive', {})))
    all_agents.update(create_visualization_agents(config.get('visualization', {})))
    
    return all_agents

__all__ = ['create_agents']
