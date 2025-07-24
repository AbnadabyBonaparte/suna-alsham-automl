import logging
from typing import List, Dict, Any
from datetime import datetime
import json
import uuid
from multi_agent_network import MultiAgentNetwork, AgentType, AgentMessage, MessageType, Priority

try:
    from specialized_agents import create_specialized_agents
except ImportError:
    create_specialized_agents = None
try:
    from ai_powered_agents import create_ai_agents
except ImportError:
    create_ai_agents = None
try:
    from core_agents_v3 import create_core_agents_v3
except ImportError:
    create_core_agents_v3 = None
try:
    from system_agents import create_system_agents
except ImportError:
    create_system_agents = None
try:
    from service_agents import create_service_agents
except ImportError:
    create_service_agents = None
try:
    from meta_cognitive_agents import create_meta_cognitive_agents
except ImportError:
    create_meta_cognitive_agents = None

logger = logging.getLogger(__name__)

def verificar_arquivos():
    return all([create_specialized_agents, create_ai_agents, create_core_agents_v3,
                create_system_agents, create_service_agents, create_meta_cognitive_agents])

class SUNAAlshamSystemV2:
    def __init__(self):
        self.network = None
        self.all_agents = {}
        self.agent_categories = {
            'specialized': 0,
            'ai_powered': 0,
            'core_v3': 0,
            'system': 0,
            'service': 0,
            'meta_cognitive': 0
        }
        self.system_status = 'initializing'
        self.created_at = datetime.now()
        self.initialization_log = []

    def _register_agents(self, agents: List, category: str):
        try:
            for agent_instance in agents:
                if not hasattr(agent_instance, 'agent_id') or not hasattr(agent_instance, 'status'):
                    logger.error(f"❌ Agente inválido em {category}: {agent_instance}")
                    continue
                if self.network:
                    self.network.add_agent(agent_instance)
                self.all_agents[agent_instance.agent_id] = {
                    'instance': agent_instance,
                    'category': category,
                    'status': agent_instance.status,
                    'capabilities': getattr(agent_instance, 'capabilities', [])
                }
                self.agent_categories[category] += 1
                self.initialization_log.append({
                    'agent_id': agent_instance.agent_id,
                    'category': category,
                    'initialized_at': datetime.now().isoformat()
                })
                logger.info(f"✅ Agente {agent_instance.agent_id} registrado na categoria {category}")
        except Exception as e:
            logger.error(f"❌ Erro registrando agentes {category}: {e}", exc_info=True)

    def _setup_supreme_orchestration(self):
        try:
            logger.info(f"🔍 Verificando {len(self.all_agents)} agentes para encontrar orquestrador")
            orchestrator = None
            for agent_id, agent_data in self.all_agents.items():
                logger.info(f"🔎 Agente encontrado: {agent_id} (categoria: {agent_data['category']})")
                if 'orchestrator' in agent_id.lower():
                    orchestrator = agent_data['instance']
                    logger.info(f"👑 Orquestrador encontrado: {agent_id}")
                    break
            if orchestrator:
                logger.info(f"👑 Orquestração suprema configurada com {len(self.all_agents)-1} agentes")
            else:
                logger.error("❌ Agente orquestrador não encontrado")
                logger.warning("⚠️ Usando coordenação distribuída")
        except Exception as e:
            logger.error(f"❌ Erro configurando orquestração: {e}", exc_info=True)

    async def initialize_complete_system(self):
        try:
            logger.info("🚀 Iniciando SUNA-ALSHAM Sistema Completo v2.0")
            if not verificar_arquivos():
                logger.error("❌ Arquivos necessários não encontrados")
                self.system_status = 'error'
                return False
            
            if MultiAgentNetwork:
                self.network = MultiAgentNetwork()
                await self.network.initialize()
                logger.info("✅ Rede Multi-Agente inicializada")
            else:
                logger.error("❌ MultiAgentNetwork não disponível")
                self.system_status = 'error'
                return False
            
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
                        agents = agents[:2]  # Limitar a 2 agentes de serviço
                    self._register_agents(agents, category)
                    logger.info(f"✅ {len(agents)} agentes {category} inicializados")
                except Exception as e:
                    logger.error(f"❌ Erro criando agentes {category}: {e}", exc_info=True)
            
            # Limpar agentes existentes para evitar duplicações
            self.all_agents.clear()
            self.agent_categories = {k: 0 for k in self.agent_categories}
            
            log_agent_creation(create_specialized_agents, 'specialized', num_instances=2)  # 6 agentes
            log_agent_creation(create_ai_agents, 'ai_powered', num_instances=1)  # 3 agentes
            log_agent_creation(create_core_agents_v3, 'core_v3', num_instances=2)  # 6 agentes
            log_agent_creation(create_system_agents, 'system', num_instances=1)  # 3 agentes
            log_agent_creation(create_service_agents, 'service', num_instances=1)  # 2 agentes
            log_agent_creation(create_meta_cognitive_agents, 'meta_cognitive')  # 2 agentes
            
            total_agents = sum(self.agent_categories.values())
            if total_agents != 20:
                logger.error(f"❌ Total de agentes inválido: {total_agents} (esperado: 20)")
                self.system_status = 'error'
                return False
            
            self._setup_supreme_orchestration()
            self.system_status = 'active'
            self.total_agents = len(self.all_agents)
            
            logger.info("🎉 SISTEMA SUNA-ALSHAM V2.0 COMPLETAMENTE INICIALIZADO!")
            logger.info(f"📊 Total de agentes: {self.total_agents}")
            logger.info(f"📋 Categorias: {self.agent_categories}")
            return True
        except Exception as e:
            logger.error(f"❌ Erro inicializando sistema completo: {e}", exc_info=True)
            self.system_status = 'error'
            return False

    async def execute_system_wide_task(self, task: Any):
        try:
            orchestrator = None
            for agent_id, agent_data in self.all_agents.items():
                if 'orchestrator' in agent_id.lower():
                    orchestrator = agent_data['instance']
                    logger.info(f"👑 Tarefa {task} delegada ao orquestrador {agent_id}")
                    break
            
            if orchestrator:
                await orchestrator.orchestrate_system_wide_task(task)
                logger.info(f"✅ Tarefa {task} executada com sucesso")
            else:
                logger.warning("⚠️ Orquestrador não encontrado - distribuindo tarefa para todos os agentes")
                for agent_id, agent_data in self.all_agents.items():
                    if hasattr(agent_data['instance'], 'handle_message'):
                        message = AgentMessage(
                            id=str(uuid.uuid4()),
                            sender_id='system',
                            recipient_id=agent_id,
                            message_type=MessageType.TASK_ASSIGNMENT,
                            priority=Priority.MEDIUM,
                            content=task,
                            timestamp=datetime.now()
                        )
                        await agent_data['instance'].handle_message(message)
                logger.info(f"✅ Tarefa {task} distribuída para agentes disponíveis")
        except Exception as e:
            logger.error(f"❌ Erro executando tarefa em todo o sistema: {e}", exc_info=True)

    def get_system_status(self) -> Dict:
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
                'agent_categories': self.agent_categories,
                'agent_statuses': agent_statuses,
                'network_status': 'active' if self.network and self.network._running else 'inactive',
                'created_at': self.created_at.isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            logger.info(f"📊 Status detalhado:\n{json.dumps(status, indent=2)}")
            return status
        except Exception as e:
            logger.error(f"❌ Erro obtendo status: {e}", exc_info=True)
            return {'status': 'error', 'error': str(e)}
