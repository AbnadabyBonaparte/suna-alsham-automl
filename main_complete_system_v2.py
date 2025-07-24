#!/usr/bin/env python3
"""
SUNA-ALSHAM Sistema Completo v2.0 - EXATAMENTE 20 Agentes
Configuração final: 5+3+5+3+2+2 = 20 agentes
"""

import asyncio
import logging
import os
import sys
from typing import Dict, List, Any, Optional
import time
from datetime import datetime
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from urllib.parse import urlparse, parse_qs

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('suna_alsham_v2.log')
    ]
)
logger = logging.getLogger(__name__)

# Importar rede multi-agente
try:
    from multi_agent_network import MultiAgentNetwork
    logger.info("✅ MultiAgentNetwork importado com sucesso")
except ImportError as e:
    logger.error(f"❌ Erro importando MultiAgentNetwork: {e}")
    MultiAgentNetwork = None

# Importar agentes especializados
try:
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

def verificar_arquivos():
    """Verifica se todos os módulos necessários estão disponíveis"""
    return all([create_specialized_agents, create_ai_agents, create_core_agents_v3,
                create_system_agents, create_service_agents, create_meta_cognitive_agents])

class SUNAAlshamSystemV2:
    """Sistema SUNA-ALSHAM Completo v2.0 com EXATAMENTE 20 Agentes"""
    
    def __init__(self):
        self.network = None
        self.all_agents = {}
        self.system_status = 'initializing'
        self.total_agents = 0
        self.agent_categories = {
            'specialized': 0,
            'ai_powered': 0,
            'core_v3': 0,
            'system': 0,
            'service': 0,
            'meta_cognitive': 0
        }
        self.orchestrator = None
        self.created_at = datetime.now()
        self.initialization_log = []
        
        # Configuração EXATA para 20 agentes
        self.target_config = {
            'specialized': 5,      # 5 agentes especializados
            'ai_powered': 3,       # 3 agentes com IA
            'core_v3': 5,          # 5 agentes core v3
            'system': 3,           # 3 agentes de sistema
            'service': 2,          # 2 agentes de serviço
            'meta_cognitive': 2    # 2 agentes meta-cognitivos
        }
        # Total: 5+3+5+3+2+2 = 20 agentes exatos

    def _register_agents(self, agents: List, category: str):
        """Registra agentes na rede e no sistema com prevenção de duplicatas"""
        try:
            seen_ids = set()
            registered_count = 0
            target_count = self.target_config[category]
            
            for agent_instance in agents:
                # Parar se já atingimos o limite da categoria
                if registered_count >= target_count:
                    logger.info(f"🔧 Limitando {category} a {target_count} agentes (ignorando excedentes)")
                    break
                    
                if not hasattr(agent_instance, 'agent_id') or not hasattr(agent_instance, 'status'):
                    logger.error(f"❌ Agente inválido em {category}: {agent_instance}")
                    continue
                    
                if agent_instance.agent_id not in seen_ids:
                    # Registrar na rede
                    if self.network:
                        self.network.add_agent(agent_instance)
                    
                    # Registrar no sistema
                    self.all_agents[agent_instance.agent_id] = {
                        'instance': agent_instance,
                        'category': category,
                        'status': agent_instance.status,
                        'capabilities': getattr(agent_instance, 'capabilities', [])
                    }
                    
                    # Atualizar contadores
                    self.agent_categories[category] += 1
                    registered_count += 1
                    
                    # Log de inicialização
                    self.initialization_log.append({
                        'agent_id': agent_instance.agent_id,
                        'category': category,
                        'initialized_at': datetime.now().isoformat()
                    })
                    
                    logger.info(f"✅ Agente {agent_instance.agent_id} registrado na categoria {category}")
                    seen_ids.add(agent_instance.agent_id)
                    
            logger.info(f"📊 {category}: {registered_count}/{target_count} agentes registrados")
            
        except Exception as e:
            logger.error(f"❌ Erro registrando agentes {category}: {e}", exc_info=True)

    def log_agent_creation(self, func, category, custom_count=None):
        """Helper para criar número exato de agentes por categoria"""
        try:
            if func is None:
                logger.error(f"❌ Função para {category} não disponível")
                return
            
            target_count = custom_count or self.target_config[category]
            logger.info(f"🎯 Criando exatamente {target_count} agentes {category}...")
            
            # Criar agentes com base na configuração
            if category == 'meta_cognitive':
                # Meta-cognitive sempre cria 2 agentes
                agents = func(self.network.message_bus)
            else:
                # Para outras categorias, usar num_instances baseado no target
                if target_count <= 3:
                    num_instances = 1
                else:
                    # Para 5 agentes, usar num_instances=1 e criar manualmente os extras
                    num_instances = 1
                
                agents = func(self.network.message_bus, num_instances=num_instances)
            
            if not agents:
                logger.error(f"❌ Nenhum agente criado para {category}")
                return
            
            # Registrar agentes com limitação rigorosa
            self._register_agents(agents, category)
            
            # Verificação final
            actual_count = self.agent_categories[category]
            if actual_count == target_count:
                logger.info(f"✅ {actual_count} agentes {category} inicializados (meta: {target_count}) ✓")
            else:
                logger.error(f"❌ {category}: {actual_count} agentes (esperado: {target_count})")
            
        except Exception as e:
            logger.error(f"❌ Erro criando agentes {category}: {e}")

    async def initialize_complete_system(self):
        """Inicializa todo o sistema SUNA-ALSHAM v2.0 com EXATAMENTE 20 agentes"""
        try:
            logger.info("🚀 Iniciando SUNA-ALSHAM Sistema Completo v2.0")
            logger.info(f"🎯 Configuração alvo: {self.target_config}")
            logger.info(f"🎯 Total esperado: {sum(self.target_config.values())} agentes")
            
            # Verificar arquivos necessários
            if not verificar_arquivos():
                logger.error("❌ Arquivos necessários não encontrados")
                self.system_status = 'error'
                return False
            
            # Inicializar rede multi-agente
            if MultiAgentNetwork:
                self.network = MultiAgentNetwork()
                await self.network.initialize()
                logger.info("✅ Rede Multi-Agente inicializada")
            else:
                logger.error("❌ MultiAgentNetwork não disponível")
                self.system_status = 'error'
                return False
            
            # Limpar agentes existentes para evitar duplicações
            self.all_agents.clear()
            self.agent_categories = {k: 0 for k in self.agent_categories}
            logger.info("🧹 Limpeza de agentes concluída")
            
            # Criar agentes com configuração EXATA para 20 agentes
            logger.info("📊 Iniciando criação de agentes com limitação rigorosa...")
            
            # 5 agentes especializados (em vez de 6)
            self.log_agent_creation(create_specialized_agents, 'specialized', 5)
            
            # 3 agentes com IA
            self.log_agent_creation(create_ai_agents, 'ai_powered', 3)
            
            # 5 agentes core v3 (em vez de 6)
            self.log_agent_creation(create_core_agents_v3, 'core_v3', 5)
            
            # 3 agentes de sistema
            self.log_agent_creation(create_system_agents, 'system', 3)
            
            # 2 agentes de serviço
            self.log_agent_creation(create_service_agents, 'service', 2)
            
            # 2 agentes meta-cognitivos
            self.log_agent_creation(create_meta_cognitive_agents, 'meta_cognitive', 2)
            
            # Validação final RIGOROSA
            await self._validate_final_count()
            
            # Configurar orquestração suprema
            await self._setup_supreme_orchestration()
            
            # Ativar sistema apenas se tiver exatamente 20 agentes
            if self.total_agents == 20:
                self.system_status = 'active'
                logger.info("🎉 SISTEMA ATIVADO COM SUCESSO - 20 AGENTES CONFIRMADOS!")
            else:
                logger.error(f"❌ SISTEMA NÃO ATIVADO - {self.total_agents} agentes (esperado: 20)")
                self.system_status = 'error'
                return False
            
            # Relatório final
            await self._generate_system_report()
            
            logger.info("🎉 SISTEMA SUNA-ALSHAM V2.0 COMPLETAMENTE INICIALIZADO!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro inicializando sistema completo: {e}", exc_info=True)
            self.system_status = 'error'
            return False

    async def _validate_final_count(self):
        """Validação rigorosa da contagem final de agentes"""
        try:
            logger.info("🔍 Validação final da contagem de agentes...")
            
            # Contar agentes reais
            self.total_agents = len(self.all_agents)
            
            # Verificar cada categoria
            all_correct = True
            for category, expected in self.target_config.items():
                actual = self.agent_categories[category]
                if actual != expected:
                    logger.error(f"❌ {category}: {actual} agentes (esperado: {expected})")
                    all_correct = False
                else:
                    logger.info(f"✅ {category}: {actual} agentes (correto)")
            
            # Verificar total
            if self.total_agents == 20 and all_correct:
                logger.info("🎯 VALIDAÇÃO APROVADA: Exatamente 20 agentes confirmados!")
            else:
                logger.error(f"❌ VALIDAÇÃO FALHOU: {self.total_agents} agentes (esperado: 20)")
                
        except Exception as e:
            logger.error(f"❌ Erro na validação final: {e}")

    async def _setup_supreme_orchestration(self):
        """Configura orquestração suprema do sistema"""
        try:
            logger.info(f"🔍 Verificando {len(self.all_agents)} agentes para encontrar orquestrador")
            
            # Procurar pelo orquestrador
            orchestrator = None
            for agent_id, agent_data in self.all_agents.items():
                logger.info(f"🔎 Agente encontrado: {agent_id} (categoria: {agent_data['category']})")
                if 'orchestrator' in agent_id.lower():
                    orchestrator = agent_data['instance']
                    self.orchestrator = orchestrator
                    logger.info(f"👑 Orquestrador encontrado: {agent_id}")
                    break
            
            if orchestrator:
                # Configurar orquestração com todos os agentes (exceto o próprio orquestrador)
                managed_agents = [
                    agent_data['instance'] for agent_id, agent_data in self.all_agents.items()
                    if 'orchestrator' not in agent_id.lower()
                ]
                
                if hasattr(orchestrator, 'set_managed_agents'):
                    orchestrator.set_managed_agents(managed_agents)
                
                logger.info(f"👑 Orquestração suprema configurada com {len(managed_agents)} agentes")
            else:
                logger.warning("⚠️ Agente orquestrador não encontrado")
                logger.warning("⚠️ Usando coordenação distribuída")
                
        except Exception as e:
            logger.error(f"❌ Erro configurando orquestração suprema: {e}", exc_info=True)

    async def execute_system_wide_task(self, task: Any):
        """Executa uma tarefa em todo o sistema, delegando ao OrchestratorAgent"""
        try:
            if self.orchestrator:
                logger.info(f"👑 Tarefa {task} delegada ao orquestrador")
                if hasattr(self.orchestrator, 'orchestrate_system_wide_task'):
                    await self.orchestrator.orchestrate_system_wide_task(task)
                else:
                    logger.warning("⚠️ Orquestrador não tem método orchestrate_system_wide_task")
                logger.info(f"✅ Tarefa {task} executada com sucesso")
            else:
                # Fallback distribuído
                logger.info(f"🔄 Executando tarefa {task} de forma distribuída")
                for agent_id, agent_data in self.all_agents.items():
                    try:
                        agent = agent_data['instance']
                        if hasattr(agent, 'handle_task'):
                            await agent.handle_task(task)
                    except Exception as e:
                        logger.error(f"❌ Erro executando tarefa em {agent_id}: {e}")
                logger.info(f"✅ Tarefa {task} executada de forma distribuída")
        except Exception as e:
            logger.error(f"❌ Erro executando tarefa em todo o sistema: {e}")

    async def _generate_system_report(self):
        """Gera relatório completo do sistema"""
        try:
            logger.info("📊 Gerando relatório final do sistema...")
            logger.info(f"📊 Total de agentes: {self.total_agents}")
            logger.info(f"📋 Categorias: {dict(self.agent_categories)}")
            logger.info(f"🎯 Configuração alvo: {self.target_config}")
            logger.info(f"🔧 Status do sistema: {self.system_status}")
            logger.info(f"👑 Orquestrador: {'Ativo' if self.orchestrator else 'Não encontrado'}")
            
            # Lista de todos os agentes
            logger.info("📝 Lista completa de agentes:")
            for category, count in self.agent_categories.items():
                agents_in_category = [
                    agent_id for agent_id, agent_data in self.all_agents.items()
                    if agent_data['category'] == category
                ]
                logger.info(f"  {category} ({count}): {agents_in_category}")
            
            # Verificação final
            if self.total_agents == 20:
                logger.info("🎯 ✅ META ALCANÇADA: Sistema com exatamente 20 agentes!")
                logger.info("🚀 ✅ SISTEMA SUNA-ALSHAM V2.0 OPERACIONAL!")
            else:
                logger.error(f"❌ FALHA: {self.total_agents} agentes (meta: 20)")
                
        except Exception as e:
            logger.error(f"❌ Erro gerando relatório: {e}")

    def get_system_status(self) -> Dict:
        """Retorna status detalhado do sistema"""
        try:
            agent_statuses = {}
            for agent_id, agent_data in self.all_agents.items():
                agent_statuses[agent_id] = {
                    'agent_id': agent_id,
                    'status': agent_data['instance'].status,
                    'category': agent_data['category'],
                    'capabilities_count': len(agent_data['capabilities'])
                }
            
            status = {
                'system_status': self.system_status,
                'total_agents': self.total_agents,
                'target_agents': 20,
                'agent_categories': self.agent_categories,
                'target_config': self.target_config,
                'agent_statuses': agent_statuses,
                'network_status': 'active' if self.network and self.network._running else 'inactive',
                'orchestrator_active': self.orchestrator is not None,
                'created_at': self.created_at.isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            
            logger.info(f"📊 Status detalhado:\n{json.dumps(status, indent=2)}")
            return status
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo status: {e}", exc_info=True)
            return {'status': 'error', 'error': str(e)}

    async def run_continuous_operation(self):
        """Executa operação contínua do sistema"""
        try:
            logger.info("🔄 Iniciando operação contínua...")
            
            while self.system_status == 'active':
                # Executar ciclo de operação
                await self.execute_system_wide_task("continuous_operation")
                
                # Aguardar próximo ciclo
                await asyncio.sleep(30)  # 30 segundos entre ciclos
                
        except KeyboardInterrupt:
            logger.info("⏹️ Operação interrompida pelo usuário")
        except Exception as e:
            logger.error(f"❌ Erro na operação contínua: {e}")

async def main():
    """Função principal do sistema"""
    try:
        # Criar e inicializar sistema
        system = SUNAAlshamSystemV2()
        
        # Inicializar sistema
        success = await system.initialize_complete_system()
        
        if success:
            logger.info("✅ Sistema inicializado com sucesso!")
            
            # Executar operação contínua
            await system.run_continuous_operation()
        else:
            logger.error("❌ Falha na inicialização do sistema")
            
    except Exception as e:
        logger.error(f"❌ Erro na função principal: {e}")

if __name__ == "__main__":
    # Verificar variáveis de ambiente
    if not os.getenv('OPENAI_API_KEY'):
        logger.warning("⚠️ OPENAI_API_KEY não configurada - IA simulada será usada")
    
    if not os.getenv('REDIS_URL'):
        logger.warning("⚠️ REDIS_URL não configurada - cache local será usado")
    
    # Executar sistema
    asyncio.run(main())

