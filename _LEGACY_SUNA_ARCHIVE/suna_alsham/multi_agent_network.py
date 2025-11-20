"""
SUNA-ALSHAM Multi-Agent Network
Sistema de rede multi-agente com coordenação inteligente
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class MultiAgentNetwork:
    """Rede principal de agentes multi-agente"""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.message_queue = asyncio.Queue()
        self.is_running = False
        self.network_stats = {
            'total_agents': 0,
            'active_agents': 0,
            'messages_processed': 0,
            'start_time': None
        }
        
    async def initialize(self):
        """Inicializa a rede de agentes"""
        try:
            logger.info("🚀 Inicializando Multi-Agent Network...")
            self.network_stats['start_time'] = datetime.now()
            self.is_running = True
            logger.info("✅ Multi-Agent Network inicializada com sucesso")
            return True
        except Exception as e:
            logger.error(f"❌ Erro inicializando network: {e}")
            return False
    
    async def register_agent(self, agent_id: str, agent_instance: Any):
        """Registra um agente na rede"""
        try:
            self.agents[agent_id] = {
                'instance': agent_instance,
                'status': 'active',
                'registered_at': datetime.now(),
                'message_count': 0
            }
            self.network_stats['total_agents'] = len(self.agents)
            self.network_stats['active_agents'] = len([a for a in self.agents.values() if a['status'] == 'active'])
            
            logger.info(f"✅ Agente {agent_id} registrado na rede")
            return True
        except Exception as e:
            logger.error(f"❌ Erro registrando agente {agent_id}: {e}")
            return False
    
    async def send_message(self, from_agent: str, to_agent: str, message: Dict):
        """Envia mensagem entre agentes"""
        try:
            if to_agent not in self.agents:
                logger.warning(f"⚠️ Agente {to_agent} não encontrado")
                return False
                
            message_data = {
                'from': from_agent,
                'to': to_agent,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            
            await self.message_queue.put(message_data)
            self.network_stats['messages_processed'] += 1
            
            logger.debug(f"📨 Mensagem enviada: {from_agent} -> {to_agent}")
            return True
        except Exception as e:
            logger.error(f"❌ Erro enviando mensagem: {e}")
            return False
    
    async def get_network_status(self):
        """Retorna status da rede"""
        return {
            'status': 'running' if self.is_running else 'stopped',
            'stats': self.network_stats,
            'agents': {
                agent_id: {
                    'status': agent_data['status'],
                    'message_count': agent_data['message_count']
                }
                for agent_id, agent_data in self.agents.items()
            }
        }
    
    async def shutdown(self):
        """Desliga a rede de agentes"""
        try:
            logger.info("🔄 Desligando Multi-Agent Network...")
            self.is_running = False
            
            # Notificar todos os agentes
            for agent_id, agent_data in self.agents.items():
                try:
                    if hasattr(agent_data['instance'], 'shutdown'):
                        await agent_data['instance'].shutdown()
                except Exception as e:
                    logger.warning(f"⚠️ Erro desligando agente {agent_id}: {e}")
            
            logger.info("✅ Multi-Agent Network desligada")
        except Exception as e:
            logger.error(f"❌ Erro desligando network: {e}")

# Instância global
network = MultiAgentNetwork()
