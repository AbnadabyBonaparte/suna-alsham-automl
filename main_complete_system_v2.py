import logging
from typing import List, Dict, Any
from datetime import datetime
import json
import uuid
import asyncio
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
try:
    from code_analyzer_agent import create_code_analyzer_agent
except ImportError:
    create_code_analyzer_agent = None
try:
    from web_search_agent import create_web_search_agent
except ImportError:
    create_web_search_agent = None
try:
    from code_corrector_agent import create_code_corrector_agent
except ImportError:
    create_code_corrector_agent = None
try:
    from performance_monitor_agent import create_performance_monitor_agent
except ImportError:
    create_performance_monitor_agent = None

logger = logging.getLogger(__name__)

def verificar_arquivos():
    """Verifica se todos os módulos de agentes estão disponíveis"""
    modules = [
        create_specialized_agents, create_ai_agents, create_core_agents_v3,
        create_system_agents, create_service_agents, create_meta_cognitive_agents,
        create_code_analyzer_agent, create_web_search_agent, 
        create_code_corrector_agent, create_performance_monitor_agent
    ]
    return all(modules)

class SUNAAlshamSystemV2:
    """
    Sistema Multi-Agente SUNA-ALSHAM v2.0 - AUTOEVOLUÇÃO COMPLETA
    
    Coordena 24 agentes distribuídos em 6 categorias:
    - specialized: 9 agentes (incluindo agentes de autoevolução)
    - ai_powered: 3 agentes  
    - core_v3: 5 agentes
    - system: 3 agentes
    - service: 2 agentes
    - meta_cognitive: 2 agentes
    
    AGENTES DE AUTOEVOLUÇÃO:
    - CodeAnalyzerAgent: Análise automática de código
    - WebSearchAgent: Busca melhorias na internet
    - CodeCorrectorAgent: Aplicação automática de correções
    - PerformanceMonitorAgent: Monitoramento de performance
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
        self.autoevolution_enabled = False

    def _register_agents(self, agents: List, category: str):
        """Registra agentes no sistema evitando duplicações"""
        try:
            seen_ids = set()
            registered_count = 0
            
            for agent_instance in agents:
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
                        'capabilities': getattr(agent_instance, 'capabilities', []),
                        'registered_at': datetime.now()
                    }
                    
                    self.agent_categories[category] += 1
                    registered_count += 1
                    
                    self.initialization_log.append({
                        'agent_id': agent_instance.agent_id,
                        'category': category,
                        'initialized_at': datetime.now().isoformat()
                    })
                    
                    logger.info(f"✅ Agente {agent_instance.agent_id} registrado na categoria {category}")
                    seen_ids.add(agent_instance.agent_id)
                else:
                    logger.warning(f"⚠️ Agente {agent_instance.agent_id} já registrado - ignorando duplicação")
            
            logger.info(f"📊 {registered_count} agentes registrados na categoria {category}")
            
        except Exception as e:
            logger.error(f"❌ Erro registrando agentes {category}: {e}", exc_info=True)

    def _setup_supreme_orchestration(self):
        """Configura o sistema de orquestração suprema"""
        try:
            logger.info(f"🔍 Verificando {len(self.all_agents)} agentes para encontrar orquestrador")
            orchestrator = None
            
            for agent_id, agent_data in self.all_agents.items():
                logger.info(f"🔎 Agente encontrado: {agent_id} (categoria: {agent_data['category']})")
                if 'orchestrator' in agent_id.lower() and agent_data['category'] == 'meta_cognitive':
                    orchestrator = agent_data['instance']
                    logger.info(f"👑 Orquestrador encontrado: {agent_id}")
                    break
            
            if not orchestrator:
                logger.error("❌ Agente orquestrador não encontrado")
                raise ValueError("Orquestrador não disponível")
            
            logger.info(f"👑 Orquestração suprema configurada com {len(self.all_agents)-1} agentes subordinados")
            return orchestrator
            
        except Exception as e:
            logger.error(f"❌ Erro configurando orquestração: {e}", exc_info=True)
            raise

    def _setup_autoevolution_system(self):
        """Configura sistema de autoevolução"""
        try:
            # Identificar agentes de autoevolução
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
                logger.info("🚀 Sistema de autoevolução configurado e ATIVO!")
                logger.info(f"   ├── Analyzer: {autoevolution_agents['analyzer'].agent_id}")
                logger.info(f"   ├── Searcher: {autoevolution_agents['searcher'].agent_id}")
                logger.info(f"   ├── Corrector: {autoevolution_agents['corrector'].agent_id}")
                logger.info(f"   └── Monitor: {autoevolution_agents['monitor'].agent_id}")
            else:
                logger.warning(f"⚠️ Sistema de autoevolução incompleto: {len(autoevolution_agents)}/4 agentes")
                
        except Exception as e:
            logger.error(f"❌ Erro configurando autoevolução: {e}")

    async def start_metrics_display(self):
        """Exibe métricas automaticamente a cada 30 segundos"""
        logger.info("📊 Sistema de métricas automáticas iniciado")
        
        while self.system_status == 'active':
            try:
                await asyncio.sleep(30)  # A cada 30 segundos
                
                # Obter status completo
                status = self.get_system_status()
                
                # Exibir métricas formatadas
                logger.info("=" * 60)
                logger.info("📊 MÉTRICAS DO SISTEMA SUNA-ALSHAM v2.0")
                logger.info("=" * 60)
                logger.info(f"🚀 Status: {self.system_status}")
                logger.info(f"🤖 Total de Agentes: {self.total_agents}")
                logger.info(f"🔄 Autoevolução: {'ATIVA' if self.autoevolution_enabled else 'INATIVA'}")
                logger.info(f"🌐 Rede: {status.get('network', {}).get('status', 'unknown')}")
                logger.info(f"⏰ Uptime: {self._get_uptime()}")
                
                # Métricas por categoria
                logger.info("📋 AGENTES POR CATEGORIA:")
                for category, count in self.agent_categories.items():
                    logger.info(f"   ├── {category}: {count} agentes")
                
                # Métricas de autoevolução
                if self.autoevolution_enabled:
                    logger.info("🔄 SISTEMA DE AUTOEVOLUÇÃO:")
                    logger.info("   ├── CodeAnalyzer: Monitorando qualidade")
                    logger.info("   ├── WebSearcher: Buscando melhorias")
                    logger.info("   ├── CodeCorrector: Aplicando otimizações")
                    logger.info("   └── PerformanceMonitor: Medindo resultados")
                
                # Métricas da rede se disponível
                if self.network:
                    try:
                        net_metrics = self.network.get_network_status()
                        logger.info(f"📈 MÉTRICAS DA REDE:")
                        logger.info(f"   ├── Agentes Ativos: {net_metrics.get('active_agents', 0)}")
                        
                        # Métricas do MessageBus
                        msg_metrics = net_metrics.get('message_bus_metrics', {})
                        if msg_metrics:
                            logger.info(f"📤 MÉTRICAS DE MENSAGENS:")
                            logger.info(f"   ├── Enviadas: {msg_metrics.get('messages_sent', 0)}")
                            logger.info(f"   ├── Entregues: {msg_metrics.get('messages_delivered', 0)}")
                            logger.info(f"   ├── Falhadas: {msg_metrics.get('messages_failed', 0)}")
                            logger.info(f"   ├── Taxa Sucesso: {msg_metrics.get('success_rate', 0):.1f}%")
                            logger.info(f"   └── Latência Média: {msg_metrics.get('average_latency_ms', 0):.2f}ms")
                    except Exception as e:
                        logger.warning(f"⚠️ Erro obtendo métricas da rede: {e}")
                
                logger.info("=" * 60)
                
            except Exception as e:
                logger.error(f"❌ Erro exibindo métricas: {e}")
                
        logger.info("📊 Sistema de métricas automáticas finalizado")

    def _get_uptime(self) -> str:
        """Calcula o tempo de atividade do sistema"""
        uptime = datetime.now() - self.created_at
        hours, remainder = divmod(uptime.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

    async def initialize_complete_system(self):
        """Inicializa o sistema completo com todos os agentes"""
        try:
            logger.info("🚀 Iniciando SUNA-ALSHAM Sistema Completo v2.0 - AUTOEVOLUÇÃO")
            logger.info(f"⏰ Inicialização em: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Verificar módulos necessários
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
            
            def log_agent_creation(func, category, num_instances=1):
                """Helper para criar e logar agentes"""
                try:
                    if func is None:
                        logger.error(f"❌ Função para {category} não disponível")
                        return
                    
                    logger.info(f"🔧 Criando agentes {category}...")
                    
                    # Criar agentes
                    if category != 'meta_cognitive':
                        agents = func(self.network.message_bus, num_instances=num_instances)
                    else:
                        agents = func(self.network.message_bus)
                    
                    if not agents:
                        logger.error(f"❌ Nenhum agente criado para {category}")
                        return
                    
                    # Limitar agentes de serviço
                    if category == 'service' and num_instances == 1:
                        agents = agents[:2]  # Limitar a 2 agentes de serviço
                    
                    # Registrar agentes
                    self._register_agents(agents, category)
                    logger.info(f"✅ {len(agents)} agentes {category} inicializados com sucesso")
                    
                except Exception as e:
                    logger.error(f"❌ Erro criando agentes {category}: {e}", exc_info=True)
            
            # Limpar agentes existentes para evitar duplicações
            logger.info("🧹 Limpando registros anteriores...")
            self.all_agents.clear()
            self.agent_categories = {k: 0 for k in self.agent_categories}
            
            # Criar todos os agentes por categoria
            logger.info("🎯 Iniciando criação de agentes por categoria...")
            
            # Agentes originais
            log_agent_creation(create_specialized_agents, 'specialized', num_instances=2)
            log_agent_creation(create_ai_agents, 'ai_powered', num_instances=1)
            log_agent_creation(create_core_agents_v3, 'core_v3', num_instances=2)
            log_agent_creation(create_system_agents, 'system', num_instances=1)
            log_agent_creation(create_service_agents, 'service', num_instances=1)
            log_agent_creation(create_meta_cognitive_agents, 'meta_cognitive')
            
            # AGENTES DE AUTOEVOLUÇÃO (NOVOS)
            logger.info("🔄 Criando sistema de autoevolução...")
            log_agent_creation(create_code_analyzer_agent, 'specialized')        # +1 agente
            log_agent_creation(create_web_search_agent, 'specialized')           # +1 agente  
            log_agent_creation(create_code_corrector_agent, 'specialized')       # +1 agente
            log_agent_creation(create_performance_monitor_agent, 'specialized')  # +1 agente
            
            # Validar contagem total de agentes
            total_agents = sum(self.agent_categories.values())
            logger.info(f"🧮 Contagem total de agentes: {total_agents}")
            
            if total_agents != 24:
                logger.error(f"❌ Total de agentes inválido: {total_agents} (esperado: 24)")
                logger.error(f"📊 Distribuição atual: {self.agent_categories}")
                self.system_status = 'error'
                return False
            
            # Configurar orquestração
            logger.info("👑 Configurando sistema de orquestração...")
            self._setup_supreme_orchestration()
            
            # Configurar autoevolução
            logger.info("🔄 Configurando sistema de autoevolução...")
            self._setup_autoevolution_system()
            
            # Finalizar inicialização
            self.system_status = 'active'
            self.total_agents = len(self.all_agents)
            
            # Logs de sucesso
            logger.info("🎉 SISTEMA SUNA-ALSHAM V2.0 - AUTOEVOLUÇÃO COMPLETAMENTE INICIALIZADO!")
            logger.info(f"📊 Total de agentes: {self.total_agents}")
            logger.info(f"📋 Categorias: {self.agent_categories}")
            logger.info(f"🔄 Autoevolução: {'ATIVA' if self.autoevolution_enabled else 'INATIVA'}")
            logger.info(f"🌐 Rede ativa: {self.network._running}")
            logger.info(f"⏰ Tempo de inicialização: {self._get_uptime()}")
            
            # Iniciar sistema de métricas automáticas
            self.metrics_task = asyncio.create_task(self.start_metrics_display())
            
            # Exibir métricas iniciais
            logger.info("📊 EXIBINDO STATUS INICIAL:")
            initial_status = self.get_system_status()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro crítico inicializando sistema completo: {e}", exc_info=True)
            self.system_status = 'error'
            return False

    async def execute_autoevolution_cycle(self):
        """Executa um ciclo completo de autoevolução"""
        try:
            if not self.autoevolution_enabled:
                logger.warning("⚠️ Sistema de autoevolução não está ativo")
                return False
            
            logger.info("🔄 Iniciando ciclo de autoevolução...")
            
            # 1. Análise de código
            analyzer = None
            for agent_id, agent_data in self.all_agents.items():
                if 'code_analyzer' in agent_id.lower():
                    analyzer = agent_data['instance']
                    break
            
            if analyzer:
                # Analisar arquivo principal
                analysis_result = analyzer.analyze_code_quality(__file__)
                logger.info(f"📊 Análise concluída: {len(analysis_result.get('issues', []))} problemas encontrados")
            
            # 2. Busca por melhorias
            searcher = None
            for agent_id, agent_data in self.all_agents.items():
                if 'web_search' in agent_id.lower():
                    searcher = agent_data['instance']
                    break
            
            if searcher:
                with open(__file__, 'r') as f:
                    current_code = f.read()
                search_result = searcher.search_better_code_patterns(current_code)
                logger.info(f"🔍 Busca concluída: {len(search_result.get('improvement_suggestions', []))} sugestões encontradas")
            
            # 3. Aplicar correções (se houver)
            corrector = None
            for agent_id, agent_data in self.all_agents.items():
                if 'code_corrector' in agent_id.lower():
                    corrector = agent_data['instance']
                    break
            
            # 4. Monitorar performance
            monitor = None
            for agent_id, agent_data in self.all_agents.items():
                if 'performance_monitor' in agent_id.lower():
                    monitor = agent_data['instance']
                    break
            
            if monitor:
                system_status = monitor.monitor_system_resources()
                logger.info(f"📈 Monitoramento concluído: Sistema {system_status.get('system_health', 'unknown')}")
            
            logger.info("✅ Ciclo de autoevolução completado")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro no ciclo de autoevolução: {e}")
            return False

    async def execute_system_wide_task(self, task: Any):
        """Executa uma tarefa em todo o sistema via orquestrador"""
        try:
            if self.system_status != 'active':
                raise ValueError(f"Sistema não está ativo (status: {self.system_status})")
            
            orchestrator = None
            for agent_id, agent_data in self.all_agents.items():
                if 'orchestrator' in agent_id.lower() and agent_data['category'] == 'meta_cognitive':
                    orchestrator = agent_data['instance']
                    logger.info(f"👑 Tarefa {task} delegada ao orquestrador {agent_id}")
                    break
            
            if orchestrator:
                await orchestrator.orchestrate_system_wide_task(task)
                logger.info(f"✅ Tarefa {task} executada com sucesso")
                return True
            else:
                logger.error("❌ Orquestrador não encontrado - falha na execução")
                raise ValueError("Orquestrador não disponível")
                
        except Exception as e:
            logger.error(f"❌ Erro executando tarefa em todo o sistema: {e}", exc_info=True)
            return False

    def get_system_status(self) -> Dict:
        """Retorna status detalhado do sistema com métricas"""
        try:
            # Status dos agentes individuais
            agent_statuses = {}
            for agent_id, agent_data in self.all_agents.items():
                try:
                    agent_statuses[agent_id] = {
                        'agent_id': agent_id,
                        'status': agent_data['instance'].status,
                        'category': agent_data['category'],
                        'capabilities_count': len(agent_data['capabilities']),
                        'capabilities': agent_data['capabilities'],
                        'registered_at': agent_data.get('registered_at', self.created_at).isoformat()
                    }
                except Exception as e:
                    logger.warning(f"⚠️ Erro obtendo status do agente {agent_id}: {e}")
                    agent_statuses[agent_id] = {
                        'agent_id': agent_id,
                        'status': 'error',
                        'category': agent_data.get('category', 'unknown'),
                        'capabilities_count': 0,
                        'error': str(e)
                    }
            
            # Status da rede
            network_status = 'inactive'
            network_metrics = {}
            if self.network:
                network_status = 'active' if self.network._running else 'inactive'
                try:
                    network_metrics = self.network.get_network_status()
                except Exception as e:
                    logger.warning(f"⚠️ Erro obtendo métricas da rede: {e}")
            
            # Compilar status completo
            status = {
                'system_info': {
                    'name': 'SUNA-ALSHAM Multi-Agent System - AUTOEVOLUTION',
                    'version': '2.0',
                    'status': self.system_status,
                    'autoevolution_enabled': self.autoevolution_enabled,
                    'created_at': self.created_at.isoformat(),
                    'uptime': self._get_uptime(),
                    'last_updated': datetime.now().isoformat()
                },
                'agents': {
                    'total_agents': self.total_agents,
                    'agent_categories': self.agent_categories,
                    'agent_statuses': agent_statuses
                },
                'network': {
                    'status': network_status,
                    'metrics': network_metrics
                },
                'autoevolution': {
                    'enabled': self.autoevolution_enabled,
                    'agents_count': 4 if self.autoevolution_enabled else 0
                },
                'initialization_log': self.initialization_log[-10:]  # Últimos 10 logs
            }
            
            # Log detalhado apenas em debug
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"📊 Status detalhado:\n{json.dumps(status, indent=2, default=str)}")
            
            return status
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo status do sistema: {e}", exc_info=True)
            return {
                'system_info': {
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
            }

    async def shutdown_system(self):
        """Desliga o sistema de forma organizada"""
        try:
            logger.info("🛑 Iniciando desligamento do sistema...")
            
            # Parar métricas automáticas
            if self.metrics_task:
                self.metrics_task.cancel()
                logger.info("📊 Sistema de métricas parado")
            
            # Alterar status
            self.system_status = 'shutting_down'
            
            # Desativar autoevolução
            self.autoevolution_enabled = False
            logger.info("🔄 Sistema de autoevolução desativado")
            
            # Parar rede
            if self.network:
                self.network.stop()
                logger.info("🌐 Rede multi-agente parada")
            
            # Finalizar
            self.system_status = 'stopped'
            logger.info("✅ Sistema desligado com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro durante desligamento: {e}", exc_info=True)
            self.system_status = 'error'

    def __repr__(self):
        return f"SUNAAlshamSystemV2(agents={self.total_agents}, autoevolution={self.autoevolution_enabled}, status='{self.system_status}')"

    def __str__(self):
        return f"SUNA-ALSHAM Multi-Agent System v2.0 - {self.total_agents} agents - Autoevolution: {'ON' if self.autoevolution_enabled else 'OFF'} - Status: {self.system_status}"


# Função utilitária para criar instância do sistema
def create_suna_system() -> SUNAAlshamSystemV2:
    """Factory function para criar instância do sistema"""
    return SUNAAlshamSystemV2()


# Script de teste se executado diretamente
if __name__ == "__main__":
    async def test_system():
        """Teste básico do sistema"""
        system = SUNAAlshamSystemV2()
        
        logger.info("🧪 Iniciando teste do sistema...")
        success = await system.initialize_complete_system()
        
        if success:
            logger.info("✅ Sistema inicializado com sucesso no teste")
            
            # Testar autoevolução
            if system.autoevolution_enabled:
                logger.info("🔄 Testando ciclo de autoevolução...")
                await system.execute_autoevolution_cycle()
            
            # Aguardar alguns segundos para ver métricas
            await asyncio.sleep(60)
            
            # Desligar sistema
            await system.shutdown_system()
        else:
            logger.error("❌ Falha no teste de inicialização")
    
    # Executar teste
    asyncio.run(test_system())
