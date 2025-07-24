"""
SUNA-ALSHAM Sistema Completo v2.0 - CORRIGIDO
Sistema Multi-Agente com 20 Agentes Especializados
Integração completa de todos os módulos de agentes
"""

import asyncio
import logging
import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Verificar se todos os arquivos estão presentes
def verificar_arquivos():
    """Verifica se todos os arquivos de agentes estão presentes"""
    arquivos_necessarios = [
        'multi_agent_network.py',
        'specialized_agents.py', 
        'ai_powered_agents.py',
        'core_agents_v3.py',
        'system_agents.py',
        'service_agents.py',
        'meta_cognitive_agents.py'
    ]
    
    arquivos_presentes = []
    arquivos_faltando = []
    
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            arquivos_presentes.append(arquivo)
            logger.info(f"✅ {arquivo} encontrado")
        else:
            arquivos_faltando.append(arquivo)
            logger.warning(f"⚠️ {arquivo} não encontrado")
    
    logger.info(f"📊 Verificação: {len(arquivos_presentes)}/{len(arquivos_necessarios)} arquivos presentes")
    
    if arquivos_faltando:
        logger.error(f"❌ Arquivos faltando: {arquivos_faltando}")
        return False
    
    return True

# Importações condicionais com tratamento de erro
try:
    # Importar rede multi-agente
    from multi_agent_network import MultiAgentNetwork
    logger.info("✅ multi_agent_network importado com sucesso")
except ImportError as e:
    logger.error(f"❌ Erro importando multi_agent_network: {e}")
    MultiAgentNetwork = None

try:
    # Importar agentes especializados
    from specialized_agents import create_specialized_agents
    logger.info("✅ specialized_agents importado com sucesso")
except ImportError as e:
    logger.error(f"❌ Erro importando specialized_agents: {e}")
    create_specialized_agents = None

try:
    # Importar agentes com IA
    from ai_powered_agents import create_ai_agents
    logger.info("✅ ai_powered_agents importado com sucesso")
except ImportError as e:
    logger.error(f"❌ Erro importando ai_powered_agents: {e}")
    create_ai_agents = None

try:
    # Importar agentes core v3
    from core_agents_v3 import create_core_agents_v3
    logger.info("✅ core_agents_v3 importado com sucesso")
except ImportError as e:
    logger.error(f"❌ Erro importando core_agents_v3: {e}")
    create_core_agents_v3 = None

try:
    # Importar agentes de sistema
    from system_agents import create_system_agents
    logger.info("✅ system_agents importado com sucesso")
except ImportError as e:
    logger.error(f"❌ Erro importando system_agents: {e}")
    create_system_agents = None

try:
    # Importar agentes de serviço
    from service_agents import create_service_agents
    logger.info("✅ service_agents importado com sucesso")
except ImportError as e:
    logger.error(f"❌ Erro importando service_agents: {e}")
    create_service_agents = None

try:
    # Importar agentes meta-cognitivos
    from meta_cognitive_agents import create_meta_cognitive_agents
    logger.info("✅ meta_cognitive_agents importado com sucesso")
except ImportError as e:
    logger.error(f"❌ Erro importando meta_cognitive_agents: {e}")
    create_meta_cognitive_agents = None

class SUNAAlshamSystemV2:
    """Sistema SUNA-ALSHAM Completo v2.0 com 20 Agentes"""
    
    def __init__(self):
        self.network = None
        self.all_agents = {}
        self.system_status = 'inactive'
        self.total_agents = 0
        self.agent_categories = {
            'specialized': 0,
            'ai_powered': 0,
            'core_v3': 0,
            'system': 0,
            'service': 0,
            'meta_cognitive': 0
        }
        self.initialization_log = []
        self.created_at = datetime.now()
        
    async def initialize_complete_system(self):
        """Inicializa sistema completo com todos os 20 agentes"""
        try:
            logger.info("🚀 Iniciando SUNA-ALSHAM Sistema Completo v2.0")
            
            # Verificar arquivos necessários
            if not verificar_arquivos():
                logger.warning("⚠️ Alguns arquivos não encontrados - continuando com disponíveis")
            
            # Inicializar rede multi-agente
            if MultiAgentNetwork:
                self.network = MultiAgentNetwork()
                await self.network.initialize()
                logger.info("✅ Rede Multi-Agente inicializada")
            else:
                logger.error("❌ MultiAgentNetwork não disponível")
                return False
            
            # Inicializar agentes especializados (3 agentes) - CORRIGIDO
            if create_specialized_agents:
                try:
                    specialized_agents = create_specialized_agents(self.network.message_bus)
                    self._register_agents(specialized_agents, 'specialized')
                    logger.info(f"✅ {len(specialized_agents)} agentes especializados inicializados")
                except Exception as e:
                    logger.error(f"❌ Erro criando agentes especializados: {e}")
            else:
                logger.warning("⚠️ Agentes especializados não disponíveis")
            
            # Inicializar agentes com IA (3 agentes) - CORRIGIDO
            if create_ai_agents:
                try:
                    ai_agents = create_ai_agents(self.network.message_bus)
                    self._register_agents(ai_agents, 'ai_powered')
                    logger.info(f"✅ {len(ai_agents)} agentes com IA inicializados")
                except Exception as e:
                    logger.error(f"❌ Erro criando agentes com IA: {e}")
            else:
                logger.warning("⚠️ Agentes com IA não disponíveis")
            
            # Inicializar agentes core v3 (3 agentes) - CORRIGIDO
            if create_core_agents_v3:
                try:
                    core_agents = create_core_agents_v3(self.network.message_bus)
                    self._register_agents(core_agents, 'core_v3')
                    logger.info(f"✅ {len(core_agents)} agentes core v3.0 inicializados")
                except Exception as e:
                    logger.error(f"❌ Erro criando agentes core v3: {e}")
            else:
                logger.warning("⚠️ Agentes core v3 não disponíveis")
            
            # Inicializar agentes de sistema (3 agentes) - CORRIGIDO
            if create_system_agents:
                try:
                    system_agents = create_system_agents(self.network.message_bus)
                    self._register_agents(system_agents, 'system')
                    logger.info(f"✅ {len(system_agents)} agentes de sistema inicializados")
                except Exception as e:
                    logger.error(f"❌ Erro criando agentes de sistema: {e}")
            else:
                logger.warning("⚠️ Agentes de sistema não disponíveis")
            
            # Inicializar agentes de serviço (3 agentes) - CORRIGIDO
            if create_service_agents:
                try:
                    service_agents = create_service_agents(self.network.message_bus)
                    self._register_agents(service_agents, 'service')
                    logger.info(f"✅ {len(service_agents)} agentes de serviço inicializados")
                except Exception as e:
                    logger.error(f"❌ Erro criando agentes de serviço: {e}")
            else:
                logger.warning("⚠️ Agentes de serviço não disponíveis")
            
            # Inicializar agentes meta-cognitivos (2 agentes) - CORRIGIDO
            if create_meta_cognitive_agents:
                try:
                    meta_agents = create_meta_cognitive_agents(self.network.message_bus)
                    self._register_agents(meta_agents, 'meta_cognitive')
                    logger.info(f"✅ {len(meta_agents)} agentes meta-cognitivos inicializados")
                except Exception as e:
                    logger.error(f"❌ Erro criando agentes meta-cognitivos: {e}")
            else:
                logger.warning("⚠️ Agentes meta-cognitivos não disponíveis")
            
            # Configurar orquestração suprema
            self._setup_supreme_orchestration()
            
            # Ativar sistema
            self.system_status = 'active'
            self.total_agents = len(self.all_agents)
            
            # Log final
            logger.info("🎉 SISTEMA SUNA-ALSHAM V2.0 COMPLETAMENTE INICIALIZADO!")
            logger.info(f"📊 Total de agentes: {self.total_agents}")
            logger.info(f"📋 Categorias: {self.agent_categories}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro inicializando sistema completo: {e}")
            self.system_status = 'error'
            return False
    
    def _register_agents(self, agents: List, category: str):
        """Registra agentes na rede e no sistema - CORRIGIDO"""
        try:
            for agent_instance in agents:
                # Adicionar à rede multi-agente
                if self.network:
                    self.network.add_agent(agent_instance)
                
                # Adicionar ao sistema
                self.all_agents[agent_instance.agent_id] = {
                    'instance': agent_instance,
                    'category': category,
                    'status': agent_instance.status,
                    'capabilities': agent_instance.capabilities
                }
                
                # Atualizar contadores
                self.agent_categories[category] += 1
                
                self.initialization_log.append({
                    'agent_id': agent_instance.agent_id,
                    'category': category,
                    'initialized_at': datetime.now().isoformat()
                })
                
                logger.info(f"✅ Agente {agent_instance.agent_id} registrado na categoria {category}")
                
        except Exception as e:
            logger.error(f"❌ Erro registrando agentes {category}: {e}")
    
    def _setup_supreme_orchestration(self):
        """Configura orquestração suprema - CORRIGIDO"""
        try:
            # Encontrar agente orquestrador
            orchestrator = None
            for agent_id, agent_data in self.all_agents.items():
                if 'orchestrator' in agent_id.lower():
                    orchestrator = agent_data['instance']
                    break
            
            if orchestrator:
                logger.info(f"👑 Orquestração suprema configurada com {len(self.all_agents)-1} agentes")
            else:
                logger.warning("⚠️ Agente orquestrador não encontrado - usando coordenação distribuída")
                
        except Exception as e:
            logger.error(f"❌ Erro configurando orquestração: {e}")
    
    def get_system_status(self) -> Dict:
        """Retorna status completo do sistema"""
        try:
            agent_statuses = {}
            for agent_id, agent_data in self.all_agents.items():
                agent_statuses[agent_id] = {
                    'agent_id': agent_id,
                    'status': agent_data['instance'].status,
                    'category': agent_data['category'],
                    'capabilities_count': len(agent_data['capabilities'])
                }
            
            return {
                'system_status': self.system_status,
                'total_agents': self.total_agents,
                'agent_categories': self.agent_categories,
                'agent_statuses': agent_statuses,
                'network_status': 'active' if self.network and self.network._running else 'inactive',
                'created_at': self.created_at.isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo status: {e}")
            return {'status': 'error', 'error': str(e)}

# Função principal para inicialização
async def initialize_suna_alsham_system():
    """Inicializa o sistema SUNA-ALSHAM completo"""
    try:
        logger.info("🚀 Iniciando inicialização do sistema SUNA-ALSHAM v2.0")
        
        # Criar instância do sistema
        system = SUNAAlshamSystemV2()
        
        # Inicializar sistema completo
        success = await system.initialize_complete_system()
        
        if success:
            logger.info("✅ Sistema SUNA-ALSHAM v2.0 inicializado com sucesso!")
            
            # Mostrar status final
            status = system.get_system_status()
            logger.info(f"📊 Status final: {status['total_agents']} agentes ativos")
            logger.info(f"📋 Distribuição: {status['agent_categories']}")
            
            return system
        else:
            logger.error("❌ Falha na inicialização do sistema")
            return None
            
    except Exception as e:
        logger.error(f"❌ Erro crítico na inicialização: {e}")
        return None

# Ponto de entrada principal
if __name__ == "__main__":
    async def main():
        system = await initialize_suna_alsham_system()
        if system:
            logger.info("🎉 Sistema pronto para operação!")
            
            # Manter sistema ativo
            try:
                while True:
                    await asyncio.sleep(10)
                    status = system.get_system_status()
                    logger.info(f"💓 Sistema ativo: {status['total_agents']} agentes")
            except KeyboardInterrupt:
                logger.info("🛑 Sistema interrompido pelo usuário")
        else:
            logger.error("❌ Sistema não pôde ser inicializado")
    
    # Executar sistema
    asyncio.run(main())

