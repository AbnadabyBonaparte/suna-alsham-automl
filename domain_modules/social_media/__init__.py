"""
Módulo Social Media - ALSHAM QUANTUM
Agentes para automação de mídias sociais
"""

from .content_creator_agent import create_agents as create_content_agents
from .engagement_maximizer_agent import create_agents as create_engagement_agents
from .influencer_network_agent import create_agents as create_influencer_agents
from .social_media_orchestrator_agent import create_agents as create_orchestrator_agents
from .video_automation_agent import create_agents as create_video_agents

def create_agents(config=None):
    """Cria todos os agentes do módulo Social Media"""
    config = config or {}
    
    all_agents = {}
    all_agents.update(create_content_agents(config.get('content', {})))
    all_agents.update(create_engagement_agents(config.get('engagement', {})))
    all_agents.update(create_influencer_agents(config.get('influencer', {})))
    all_agents.update(create_orchestrator_agents(config.get('orchestrator', {})))
    all_agents.update(create_video_agents(config.get('video', {})))
    
    return all_agents

__all__ = ['create_agents']
