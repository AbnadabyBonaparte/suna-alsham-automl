"""
SUNA-ALSHAM Sistema Completo v2.0 - CORRIGIDO PARA 20 AGENTES
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
            
            # CORREÇÃO 2: Função helper para criação de agentes com múltiplas instâncias
            def log_agent_creation(func, category, num_instances=1):
                try:
                    if func is None:
                        logger.error(f"❌ Função para {category} não disponível")
                        return
                    agents = func(self.network.message_bus, num_instances=num_instances) if category != 'meta_cognitive' else func(self.network.message_bus)
                    if not agents:
                        logger.error(f"❌ Nenhum agente criado para {category}")
                        return
                    if category == 'service' and num_instances == 1:
                        agents = agents[:2]  # Limitar a 2 agentes de serviço para total de 20
                    self._register_agents(agents, category)
                    logger.info(f"✅ {len(agents)} agentes {category} inicializados")
                except Exception as e:
                    logger.error(f"❌ Erro criando agentes {category}: {e}")
            
            # Inicializar agentes com configuração para 20 agentes total
            log_agent_creation(create_specialized_agents, 'specialized', num_instances=2)  # 6 agentes
            log_agent_creation(create_ai_agents, 'ai_powered', num_instances=1)  # 3 agentes
            log_agent_creation(create_core_agents_v3, 'core_v3', num_instances=2)  # 6 agentes
            log_agent_creation(create_system_agents, 'system', num_instances=1)  # 3 agentes
            log_agent_creation(create_service_agents, 'service', num_instances=1)  # 2 agentes (limitado)
            log_agent_creation(create_meta_cognitive_agents, 'meta_cognitive')  # 2 agentes
            
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
    
    # CORREÇÃO 1: Adicionar método execute_system_wide_task
    async def execute_system_wide_task(self, task: Any):
        """Executa uma tarefa em todo o sistema, delegando ao OrchestratorAgent"""
        try:
            orchestrator = None
            for agent_id, agent_data in self.all_agents.items():
                if 'orchestrator' in agent_id.lower():
                    orchestrator = agent_data['instance']
                    logger.info(f"👑 Tarefa {task} delegada ao orquestrador {agent_id}")
                    break
            
            if orchestrator:
                if hasattr(orchestrator, 'orchestrate_system_wide_task'):
                    await orchestrator.orchestrate_system_wide_task(task)
                    logger.info(f"✅ Tarefa {task} executada com sucesso")
                else:
                    logger.warning(f"⚠️ Orquestrador {orchestrator.agent_id} não tem método orchestrate_system_wide_task")
                    # Fallback: distribuir tarefa para todos os agentes
                    for agent_id, agent_data in self.all_agents.items():
                        if agent_id != orchestrator.agent_id and hasattr(agent_data['instance'], 'handle_system_task'):
                            await agent_data['instance'].handle_system_task(task)
                    logger.info(f"✅ Tarefa {task} distribuída para todos os agentes")
            else:
                logger.warning("⚠️ Orquestrador não encontrado - distribuindo tarefa para todos os agentes")
                for agent_id, agent_data in self.all_agents.items():
                    if hasattr(agent_data['instance'], 'handle_system_task'):
                        await agent_data['instance'].handle_system_task(task)
                logger.info(f"✅ Tarefa {task} distribuída para agentes disponíveis")
                
        except Exception as e:
            logger.error(f"❌ Erro executando tarefa em todo o sistema: {e}")
    
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

