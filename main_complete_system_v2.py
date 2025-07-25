import logging
from typing import List, Dict, Any
from datetime import datetime
import json
import uuid
import asyncio
import os
import traceback
from multi_agent_network import MultiAgentNetwork, AgentType, AgentMessage, MessageType, Priority

# Configuração de logging mais detalhada
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ✅ CONFIGURAÇÃO REDIS
REDIS_URL = os.getenv(
    'REDIS_URL', 
    'redis://default:fXKBQfXNMrkmxyvLrOtGyhImjmTxaedq@turntable.proxy.rlwy.net:52678'
)

# Importações com tratamento de erro detalhado
def safe_import(module_name: str, create_function_name: str):
    """Importa módulo com logging detalhado de erros"""
    try:
        module = __import__(module_name)
        create_function = getattr(module, create_function_name)
        logger.info(f"✅ Módulo {module_name} importado com sucesso")
        return create_function
    except ImportError as e:
        logger.error(f"❌ Erro importando {module_name}: {e}")
        logger.error(f"   Detalhes: {traceback.format_exc()}")
        return None
    except AttributeError as e:
        logger.error(f"❌ Função {create_function_name} não encontrada em {module_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Erro inesperado importando {module_name}: {e}")
        logger.error(f"   Detalhes: {traceback.format_exc()}")
        return None

# Importar todos os módulos com tratamento de erro
create_specialized_agents = safe_import('specialized_agents', 'create_specialized_agents')
create_ai_agents = safe_import('ai_powered_agents', 'create_ai_agents')
create_core_agents_v3 = safe_import('core_agents_v3', 'create_core_agents_v3')
create_system_agents = safe_import('system_agents', 'create_system_agents')
create_service_agents = safe_import('service_agents', 'create_service_agents')
create_meta_cognitive_agents = safe_import('meta_cognitive_agents', 'create_meta_cognitive_agents')
create_code_analyzer_agent = safe_import('code_analyzer_agent', 'create_code_analyzer_agent')
create_web_search_agent = safe_import('web_search_agent', 'create_web_search_agent')
create_code_corrector_agent = safe_import('code_corrector_agent', 'create_code_corrector_agent')
create_performance_monitor_agent = safe_import('performance_monitor_agent', 'create_performance_monitor_agent')

def verificar_arquivos():
    """Verifica se todos os módulos de agentes estão disponíveis com logging detalhado"""
    modules = {
        'specialized_agents': create_specialized_agents,
        'ai_powered_agents': create_ai_agents,
        'core_agents_v3': create_core_agents_v3,
        'system_agents': create_system_agents,
        'service_agents': create_service_agents,
        'meta_cognitive_agents': create_meta_cognitive_agents,
        'code_analyzer_agent': create_code_analyzer_agent,
        'web_search_agent': create_web_search_agent,
        'code_corrector_agent': create_code_corrector_agent,
        'performance_monitor_agent': create_performance_monitor_agent
    }
    
    missing_modules = []
    available_modules = []
    
    for module_name, module_func in modules.items():
        if module_func is None:
            missing_modules.append(module_name)
        else:
            available_modules.append(module_name)
    
    logger.info(f"📊 VERIFICAÇÃO DE MÓDULOS:")
    logger.info(f"   ✅ Disponíveis: {len(available_modules)}/10")
    logger.info(f"   ❌ Faltando: {len(missing_modules)}/10")
    
    if missing_modules:
        logger.error(f"❌ Módulos ausentes: {missing_modules}")
        for module in missing_modules:
            logger.error(f"   - {module}.py não encontrado ou com erro")
    
    if available_modules:
        logger.info(f"✅ Módulos disponíveis: {available_modules}")
    
    # Retorna True apenas se todos os módulos essenciais estão disponíveis
    essential_modules = ['specialized_agents', 'ai_powered_agents', 'core_agents_v3']
    essential_available = all(modules[m] is not None for m in essential_modules)
    
    if not essential_available:
        logger.error("❌ Módulos essenciais faltando! Sistema não pode inicializar.")
        return False
    
    return True  # Permite inicialização parcial se módulos essenciais estão OK

class SUNAAlshamSystemV2:
    """
    Sistema Multi-Agente SUNA-ALSHAM v2.0 - AUTOEVOLUÇÃO COMPLETA
    
    Coordena 24 agentes distribuídos em 6 categorias com inicialização robusta
    """
    
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
        self.total_agents = 0
        self.metrics_task = None
        self.redis_client = None
        self.autoevolution_enabled = False
        self.failed_agents = []  # Track failed agent creations
        
        # Configuração Redis
        self.redis_config = {
            'url': REDIS_URL,
            'decode_responses': True,
            'health_check_interval': 30,
            'socket_keepalive': True,
            'retry_on_timeout': True
        }
        logger.info("✅ Sistema SUNA-ALSHAM v2.0 inicializado")

    async def initialize_redis(self):
        """Inicializa conexão Redis com fallback silencioso"""
        try:
            import redis.asyncio as redis
            
            self.redis_client = redis.from_url(
                self.redis_config['url'],
                decode_responses=self.redis_config['decode_responses'],
                health_check_interval=self.redis_config['health_check_interval'],
                socket_keepalive=self.redis_config['socket_keepalive'],
                retry_on_timeout=self.redis_config['retry_on_timeout']
            )
            
            await self.redis_client.ping()
            logger.info("✅ Redis conectado com sucesso")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Redis não disponível: {e}")
            logger.info("ℹ️ Continuando com cache em memória")
            self.redis_client = None
            return False

    def _register_agents(self, agents: List, category: str):
        """Registra agentes no sistema com tratamento de erro robusto"""
        if not agents:
            logger.warning(f"⚠️ Nenhum agente recebido para categoria {category}")
            return
            
        try:
            seen_ids = set()
            registered_count = 0
            
            for agent_instance in agents:
                try:
                    if not hasattr(agent_instance, 'agent_id'):
                        logger.error(f"❌ Agente sem agent_id em {category}")
                        continue
                        
                    agent_id = agent_instance.agent_id
                    
                    if agent_id in seen_ids or agent_id in self.all_agents:
                        logger.warning(f"⚠️ Agente {agent_id} duplicado - ignorando")
                        continue
                    
                    # Registrar no network
                    if self.network:
                        success = self.network.add_agent(agent_instance)
                        if not success:
                            logger.error(f"❌ Falha ao adicionar {agent_id} à rede")
                            continue
                    
                    # Registrar internamente
                    self.all_agents[agent_id] = {
                        'instance': agent_instance,
                        'category': category,
                        'status': getattr(agent_instance, 'status', 'unknown'),
                        'capabilities': getattr(agent_instance, 'capabilities', []),
                        'registered_at': datetime.now()
                    }
                    
                    self.agent_categories[category] += 1
                    registered_count += 1
                    seen_ids.add(agent_id)
                    
                    self.initialization_log.append({
                        'agent_id': agent_id,
                        'category': category,
                        'status': 'success',
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    logger.info(f"✅ Agente {agent_id} registrado ({category})")
                    
                except Exception as e:
                    logger.error(f"❌ Erro registrando agente individual: {e}")
                    self.failed_agents.append({
                        'category': category,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
            
            logger.info(f"📊 {registered_count} agentes registrados em {category}")
            
        except Exception as e:
            logger.error(f"❌ Erro crítico registrando agentes {category}: {e}")
            logger.error(f"   Detalhes: {traceback.format_exc()}")

    async def create_agents_safely(self, create_func, category: str, num_instances: int = 1):
        """Cria agentes com tratamento de erro e timeout"""
        if create_func is None:
            logger.error(f"❌ Função de criação para {category} não disponível")
            self.failed_agents.append({
                'category': category,
                'error': 'Módulo não disponível',
                'timestamp': datetime.now().isoformat()
            })
            return []
        
        try:
            logger.info(f"🔧 Criando agentes {category}...")
            
            # Timeout de 30 segundos para criação de agentes
            if category == 'meta_cognitive':
                agents = await asyncio.wait_for(
                    asyncio.to_thread(create_func, self.network.message_bus),
                    timeout=30.0
                )
            else:
                agents = await asyncio.wait_for(
                    asyncio.to_thread(create_func, self.network.message_bus, num_instances),
                    timeout=30.0
                )
            
            if not agents:
                logger.warning(f"⚠️ Nenhum agente criado para {category}")
                return []
            
            # Limitar agentes de serviço se necessário
            if category == 'service' and len(agents) > 2:
                agents = agents[:2]
            
            logger.info(f"✅ {len(agents)} agentes {category} criados")
            return agents
            
        except asyncio.TimeoutError:
            logger.error(f"❌ Timeout criando agentes {category} (>30s)")
            self.failed_agents.append({
                'category': category,
                'error': 'Timeout na criação',
                'timestamp': datetime.now().isoformat()
            })
            return []
        except Exception as e:
            logger.error(f"❌ Erro criando agentes {category}: {e}")
            logger.error(f"   Detalhes: {traceback.format_exc()}")
            self.failed_agents.append({
                'category': category,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return []

    async def initialize_complete_system(self):
        """Inicializa o sistema completo com tratamento robusto de erros"""
        try:
            logger.info("=" * 60)
            logger.info("🚀 INICIANDO SUNA-ALSHAM SISTEMA v2.0")
            logger.info(f"⏰ Inicialização: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("=" * 60)
            
            # Verificar arquivos
            if not verificar_arquivos():
                logger.warning("⚠️ Alguns módulos não estão disponíveis")
                logger.info("ℹ️ Tentando inicialização parcial...")
            
            # Inicializar Redis (não crítico)
            await self.initialize_redis()
            
            # Inicializar rede (crítico)
            if not MultiAgentNetwork:
                logger.error("❌ MultiAgentNetwork não disponível - ABORTANDO")
                self.system_status = 'error'
                return False
            
            self.network = MultiAgentNetwork()
            await self.network.initialize()
            logger.info("✅ Rede Multi-Agente inicializada")
            
            # Limpar estado anterior
            self.all_agents.clear()
            self.agent_categories = {k: 0 for k in self.agent_categories}
            self.failed_agents.clear()
            
            # CRIAR TODOS OS AGENTES COM TRATAMENTO DE ERRO
            logger.info("\n🎯 INICIANDO CRIAÇÃO DE 24 AGENTES...")
            
            # 1. Specialized (5 base + 4 autoevolução = 9 total)
            agents = await self.create_agents_safely(create_specialized_agents, 'specialized')
            self._register_agents(agents, 'specialized')
            
            # 2. AI-Powered (3 agentes)
            agents = await self.create_agents_safely(create_ai_agents, 'ai_powered')
            self._register_agents(agents, 'ai_powered')
            
            # 3. Core v3 (5 agentes)
            agents = await self.create_agents_safely(create_core_agents_v3, 'core_v3')
            self._register_agents(agents, 'core_v3')
            
            # 4. System (3 agentes)
            agents = await self.create_agents_safely(create_system_agents, 'system')
            self._register_agents(agents, 'system')
            
            # 5. Service (2 agentes)
            agents = await self.create_agents_safely(create_service_agents, 'service')
            self._register_agents(agents, 'service')
            
            # 6. Meta-Cognitive (2 agentes)
            agents = await self.create_agents_safely(create_meta_cognitive_agents, 'meta_cognitive')
            self._register_agents(agents, 'meta_cognitive')
            
            # 7. Agentes de Autoevolução (4 agentes adicionais)
            logger.info("\n🔄 CRIANDO SISTEMA DE AUTOEVOLUÇÃO...")
            
            agents = await self.create_agents_safely(create_code_analyzer_agent, 'specialized')
            self._register_agents(agents, 'specialized')
            
            agents = await self.create_agents_safely(create_web_search_agent, 'specialized')
            self._register_agents(agents, 'specialized')
            
            agents = await self.create_agents_safely(create_code_corrector_agent, 'specialized')
            self._register_agents(agents, 'specialized')
            
            agents = await self.create_agents_safely(create_performance_monitor_agent, 'specialized')
            self._register_agents(agents, 'specialized')
            
            # VALIDAÇÃO E RELATÓRIO
            self.total_agents = len(self.all_agents)
            
            logger.info("\n" + "=" * 60)
            logger.info("📊 RELATÓRIO DE INICIALIZAÇÃO")
            logger.info("=" * 60)
            logger.info(f"✅ Agentes criados: {self.total_agents}/24")
            logger.info(f"❌ Falhas: {len(self.failed_agents)}")
            
            logger.info("\n📋 DISTRIBUIÇÃO POR CATEGORIA:")
            for category, count in self.agent_categories.items():
                expected = {
                    'specialized': 9, 'ai_powered': 3, 'core_v3': 5,
                    'system': 3, 'service': 2, 'meta_cognitive': 2
                }[category]
                status = "✅" if count == expected else "❌"
                logger.info(f"   {status} {category}: {count}/{expected}")
            
            if self.failed_agents:
                logger.info("\n❌ AGENTES QUE FALHARAM:")
                for failure in self.failed_agents:
                    logger.info(f"   - {failure['category']}: {failure['error']}")
            
            # Configurar orquestração e autoevolução
            if self.total_agents >= 20:  # Aceitar inicialização com 80%+ dos agentes
                logger.info("\n👑 Configurando orquestração...")
                try:
                    self._setup_supreme_orchestration()
                except Exception as e:
                    logger.warning(f"⚠️ Orquestração não configurada: {e}")
                
                logger.info("🔄 Configurando autoevolução...")
                try:
                    self._setup_autoevolution_system()
                except Exception as e:
                    logger.warning(f"⚠️ Autoevolução não configurada: {e}")
                
                self.system_status = 'active'
                
                # Iniciar métricas
                self.metrics_task = asyncio.create_task(self.start_metrics_display())
                
                logger.info("\n" + "🎉" * 20)
                logger.info("✅ SISTEMA SUNA-ALSHAM v2.0 INICIALIZADO!")
                logger.info(f"📊 Total: {self.total_agents} agentes ativos")
                logger.info(f"🔄 Autoevolução: {'ATIVA' if self.autoevolution_enabled else 'INATIVA'}")
                logger.info("🎉" * 20 + "\n")
                
                return True
            else:
                logger.error(f"\n❌ INICIALIZAÇÃO FALHOU: Apenas {self.total_agents}/24 agentes")
                self.system_status = 'partial'
                return False
                
        except Exception as e:
            logger.error(f"❌ ERRO CRÍTICO NA INICIALIZAÇÃO: {e}")
            logger.error(f"   Detalhes: {traceback.format_exc()}")
            self.system_status = 'error'
            return False

    def _setup_supreme_orchestration(self):
        """Configura o sistema de orquestração suprema"""
        orchestrator = None
        for agent_id, agent_data in self.all_agents.items():
            if 'orchestrator' in agent_id.lower():
                orchestrator = agent_data['instance']
                logger.info(f"👑 Orquestrador encontrado: {agent_id}")
                break
        
        if not orchestrator:
            raise ValueError("Orquestrador não encontrado")
        
        logger.info(f"✅ Orquestração configurada com {len(self.all_agents)-1} agentes")

    def _setup_autoevolution_system(self):
        """Configura sistema de autoevolução"""
        autoevolution_agents = {}
        
        for agent_id, agent_data in self.all_agents.items():
            if 'code_analyzer' in agent_id.lower():
                autoevolution_agents['analyzer'] = agent_data['instance']
            elif 'web_search' in agent_id.lower():
                autoevolution_agents['searcher'] = agent_data['instance']
            elif 'code_corrector' in agent_id.lower():
                autoevolution_agents['corrector'] = agent_data['instance']
            elif 'performance_monitor' in agent_id.lower():
                autoevolution_agents['monitor'] = agent_data['instance']
        
        if len(autoevolution_agents) == 4:
            self.autoevolution_enabled = True
            logger.info("✅ Sistema de autoevolução ATIVO com 4 agentes")
        else:
            logger.warning(f"⚠️ Autoevolução parcial: {len(autoevolution_agents)}/4 agentes")

    async def start_metrics_display(self):
        """Exibe métricas periodicamente"""
        logger.info("📊 Sistema de métricas iniciado")
        
        while self.system_status in ['active', 'partial']:
            try:
                await asyncio.sleep(30)
                
                logger.info("\n" + "📊" * 20)
                logger.info(f"MÉTRICAS - {datetime.now().strftime('%H:%M:%S')}")
                logger.info("📊" * 20)
                logger.info(f"Status: {self.system_status}")
                logger.info(f"Agentes: {self.total_agents}/24")
                logger.info(f"Autoevolução: {'ON' if self.autoevolution_enabled else 'OFF'}")
                logger.info(f"Uptime: {self._get_uptime()}")
                
                if self.network:
                    metrics = self.network.get_network_status()
                    if metrics:
                        msg_metrics = metrics.get('message_bus_metrics', {})
                        if msg_metrics:
                            logger.info(f"Mensagens: {msg_metrics.get('messages_sent', 0)} enviadas")
                            logger.info(f"Taxa sucesso: {msg_metrics.get('success_rate', 0):.1f}%")
                
            except Exception as e:
                logger.error(f"Erro nas métricas: {e}")

    def _get_uptime(self) -> str:
        """Calcula uptime do sistema"""
        uptime = datetime.now() - self.created_at
        hours, remainder = divmod(uptime.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

    def get_system_status(self) -> Dict:
        """Retorna status detalhado do sistema"""
        try:
            return {
                'system_info': {
                    'name': 'SUNA-ALSHAM v2.0',
                    'status': self.system_status,
                    'total_agents': self.total_agents,
                    'expected_agents': 24,
                    'completion_rate': f"{(self.total_agents/24)*100:.1f}%",
                    'autoevolution': self.autoevolution_enabled,
                    'redis': self.redis_client is not None,
                    'uptime': self._get_uptime(),
                    'created_at': self.created_at.isoformat()
                },
                'agents': {
                    'total': self.total_agents,
                    'by_category': self.agent_categories,
                    'failed': len(self.failed_agents)
                },
                'failures': self.failed_agents
            }
        except Exception as e:
            logger.error(f"Erro obtendo status: {e}")
            return {'error': str(e)}

    async def shutdown_system(self):
        """Desliga o sistema gracefully"""
        try:
            logger.info("🛑 Iniciando shutdown...")
            
            self.system_status = 'shutting_down'
            
            if self.metrics_task:
                self.metrics_task.cancel()
            
            if self.redis_client:
                await self.redis_client.close()
            
            if self.network:
                self.network.stop()
            
            self.system_status = 'stopped'
            logger.info("✅ Sistema desligado")
            
        except Exception as e:
            logger.error(f"Erro no shutdown: {e}")

def create_suna_system() -> SUNAAlshamSystemV2:
    """Factory function para criar instância do sistema"""
    return SUNAAlshamSystemV2()

if __name__ == "__main__":
    async def test_system():
        """Teste do sistema com inicialização robusta"""
        system = SUNAAlshamSystemV2()
        
        try:
            logger.info("🧪 TESTE DE INICIALIZAÇÃO INICIADO")
            success = await system.initialize_complete_system()
            
            if success:
                logger.info("✅ TESTE PASSOU - Sistema inicializado")
                await asyncio.sleep(60)  # Rodar por 1 minuto
            else:
                logger.error("❌ TESTE FALHOU - Inicialização incompleta")
            
            await system.shutdown_system()
            
        except Exception as e:
            logger.error(f"❌ ERRO NO TESTE: {e}")
            logger.error(traceback.format_exc())
    
    asyncio.run(test_system())
