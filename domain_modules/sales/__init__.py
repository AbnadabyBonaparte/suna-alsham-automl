"""
Módulo Sales - ALSHAM QUANTUM  
Agentes para automação de vendas e CRM
"""

from .sales_orchestrator_agent import create_agents as create_orchestrator_agents
from .customer_success_agent import create_agents as create_customer_agents
from .payment_processing_agent import create_agents as create_payment_agents
from .pricing_optimizer_agent import create_agents as create_pricing_agents
from .revenue_optimization_agent import create_agents as create_revenue_agents
from .sales_funnel_agent import create_agents as create_funnel_agents

def create_agents(config=None):
    """Cria todos os agentes do módulo Sales"""
    config = config or {}
    
    all_agents = {}
    all_agents.update(create_orchestrator_agents(config.get('orchestrator', {})))
    all_agents.update(create_customer_agents(config.get('customer', {})))
    all_agents.update(create_payment_agents(config.get('payment', {})))
    all_agents.update(create_pricing_agents(config.get('pricing', {})))
    all_agents.update(create_revenue_agents(config.get('revenue', {})))
    all_agents.update(create_funnel_agents(config.get('funnel', {})))
    
    return all_agents

__all__ = ['create_agents']
