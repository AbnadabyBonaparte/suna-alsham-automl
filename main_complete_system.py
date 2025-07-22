"""
🌟 SUNA-ALSHAM Multi-Agent System v2.0
Sistema multi-agente com capacidades de IA avançada

CORREÇÕES IMPLEMENTADAS:
✅ Removido AnalyticsAgent inexistente
✅ Corrigidas todas as importações
✅ Logs detalhados para debug
✅ Funciona com/sem Redis
✅ Tratamento robusto de erros
✅ Inicialização dos 7 agentes especializados
"""

import asyncio
import logging
import os
import sys
import time
import signal
from typing import Dict, Any, Optional
from datetime import datetime

# Configurar logging avançado
handlers = [logging.StreamHandler(sys.stdout)]
if os.getenv("RAILWAY_ENVIRONMENT") is None:
    handlers.append(logging.FileHandler('suna_alsham.log', mode='a'))
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=handlers
)
logger = logging.getLogger(__name__)

# Verificar estrutura de arquivos
logger.info(f"🚀 Executando de: {os.path.abspath(__file__)}")
logger.info(f"📁 Diretório atual: {os.getcwd()}")
logger.info(f"📋 Arquivos no diretório: {os.listdir()}")

# Verificar variáveis de ambiente críticas
logger.info(f"🔑 OPENAI_API_KEY configurada: {'✅' if os.getenv('OPENAI_API_KEY') else '❌'}")
logger.info(f"🔗 REDIS_URL configurada: {'✅' if os.getenv('REDIS_URL') else '❌'}")

try:
    from suna_alsham.core.multi_agent_network import MultiAgentNetwork
    from suna_alsham.core.specialized_agents import (
    OptimizationAgent, SecurityAgent, LearningAgent, 
    DataAgent, MonitoringAgent
    )
    from suna_alsham.core.ai_powered_agents import SelfEvolvingAgent, AIOptimizationAgent
    logger.info("✅ Todos os módulos importados com sucesso")
except ImportError as e:
    logger.error(f"❌ Erro na importação: {e}")
    logger.error("🔍 Verifique se todos os arquivos estão presentes:")
    logger.error("   - multi_agent_network.py")
    logger.error("   - specialized_agents.py") 
    logger.error("   - ai_powered_agents.py")
    sys.exit(1)

class EnhancedSystemManager:
    """Gerenciador avançado do sistema multi-agente"""
    
    def __init__(self):
        self.network = None
        self.agents: Dict[str, Any] = {}
        self.is_running = False
        self.start_time = datetime.now()
        self.shutdown_requested = False
        
        # Configurar handlers de sinal para shutdown graceful
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handler para sinais de shutdown"""
        logger.info(f"🛑 Sinal {signum} recebido, iniciando shutdown graceful...")
        self.shutdown_requested = True
        self.is_running = False
    
    def initialize_system(self) -> bool:
        """Inicializa o sistema multi-agente"""
        logger.info("🌟 Inicializando sistema SUNA-ALSHAM...")
        
        try:
            # Verificar API key do OpenAI
            if not os.getenv("OPENAI_API_KEY"):
                logger.error("❌ OPENAI_API_KEY não configurada")
                logger.error("🔧 Configure a variável de ambiente OPENAI_API_KEY")
                return False
            logger.info("✅ OPENAI_API_KEY configurada")
            
            # Verificar Redis
            redis_url = os.getenv("REDIS_URL")
            if redis_url:
                try:
                    import redis
                    redis_client = redis.from_url(redis_url)
                    redis_client.ping()
                    logger.info("✅ Redis conectado com sucesso")
                except Exception as e:
                    logger.warning(f"⚠️ Falha na conexão com Redis: {e}")
                    logger.info("🔄 Usando cache em memória como fallback")
            else:
                logger.warning("⚠️ REDIS_URL não configurada - usando cache em memória")
            
            # Criar rede multi-agente
            logger.info("🌐 Criando rede multi-agente...")
            self.network = MultiAgentNetwork()
            logger.info("✅ Rede multi-agente criada")
            
            # Criar todos os agentes especializados
            self._create_all_agents()
            
            # Iniciar a rede
            logger.info("🚀 Iniciando rede multi-agente...")
            self.network.start()
            self.is_running = True
            
            logger.info(f"🎉 Sistema inicializado com sucesso!")
            logger.info(f"📊 Total de agentes criados: {len(self.agents)}")
            logger.info(f"⏰ Tempo de inicialização: {(datetime.now() - self.start_time).total_seconds():.2f}s")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro crítico na inicialização do sistema: {e}", exc_info=True)
            return False
    
    def _create_all_agents(self):
        """Cria todos os agentes especializados"""
        logger.info("🤖 Iniciando criação dos agentes especializados...")
        
        agents_config = [
            ("optimizer_001", OptimizationAgent, "Otimização de performance"),
            ("security_001", SecurityAgent, "Monitoramento de segurança"),
            ("learner_001", LearningAgent, "Aprendizado contínuo"),
            ("data_001", DataAgent, "Processamento de dados"),
            ("monitor_001", MonitoringAgent, "Monitoramento de sistema"),
            ("evolving_001", SelfEvolvingAgent, "Auto-evolução com IA"),
            ("ai_optimizer_001", AIOptimizationAgent, "Otimização com IA"),
        ]
        
        successful_agents = 0
        failed_agents = 0
        
        for agent_id, agent_class, description in agents_config:
            logger.info(f"🔄 Tentando criar agente: {agent_id} ({agent_class.__name__}) - {description}")
            try:
                if agent_class in [SelfEvolvingAgent, AIOptimizationAgent]:
                    redis_url = os.getenv("REDIS_URL", None)
                    logger.info(f"🧠 Criando {agent_class.__name__} com REDIS_URL: {'configurada' if redis_url else 'não configurada'}")
                    agent = agent_class(agent_id, self.network.message_bus, redis_url=redis_url)
                else:
                    agent = agent_class(agent_id, self.network.message_bus)
                self.network.add_agent(agent)
                self.agents[agent_id] = agent
                successful_agents += 1
                logger.info(f"✅ Agente {agent_id} ({agent_class.__name__}) criado e adicionado com sucesso")
                if hasattr(agent, 'capabilities') and agent.capabilities:
                    capabilities = [cap.name for cap in agent.capabilities]
                    logger.info(f"   🎯 Capacidades: {', '.join(capabilities)}")
            except Exception as e:
                failed_agents += 1
                logger.error(f"❌ Erro criando agente {agent_id} ({agent_class.__name__}): {str(e)}", exc_info=True)
                continue
        
        logger.info("=" * 60)
        logger.info("📊 RESUMO DA CRIAÇÃO DE AGENTES")
        logger.info("=" * 60)
        logger.info(f"✅ Agentes criados com sucesso: {successful_agents}")
        logger.info(f"❌ Agentes que falharam: {failed_agents}")
        logger.info(f"📈 Taxa de sucesso: {(successful_agents/(successful_agents+failed_agents)*100):.1f}%")
        
        if successful_agents == 0:
            logger.error("❌ CRÍTICO: Nenhum agente foi criado com sucesso!")
            raise Exception("Falha na criação de todos os agentes")
        
        logger.info(f"🎯 Total de {successful_agents} agentes especializados criados e prontos")
    
    async def run_system_demo(self, duration: int):
        """Executa uma demonstração do sistema por um período"""
        logger.info(f"🚀 Iniciando demonstração do sistema por {duration} segundos")
        
        start_time = time.time()
        last_status_log = 0
        
        while self.is_running and not self.shutdown_requested and (time.time() - start_time) < duration:
            try:
                current_time = time.time()
                elapsed = current_time - start_time
                
                if current_time - last_status_log >= 30:
                    logger.info(f"⏱️ Demonstração em andamento: {elapsed:.0f}s/{duration}s")
                    try:
                        network_status = self.network.get_network_status()
                        logger.info(f"📊 Status da rede: {network_status}")
                    except Exception as e:
                        logger.warning(f"⚠️ Erro coletando status da rede: {e}")
                    
                    active_agents = 0
                    for agent_id, agent in self.agents.items():
                        try:
                            if hasattr(agent, 'status') and agent.status == 'running':
                                active_agents += 1
                            logger.debug(f"🤖 Agente {agent_id}: {getattr(agent, 'status', 'unknown')}")
                        except Exception as e:
                            logger.debug(f"⚠️ Erro verificando status do agente {agent_id}: {e}")
                    
                    logger.info(f"🤖 Agentes ativos: {active_agents}/{len(self.agents)}")
                    last_status_log = current_time
                
                if int(elapsed) % 60 == 0 and int(elapsed) > 0:
                    logger.info(f"🔄 Sistema operando normalmente - {int(elapsed/60)} minuto(s) de uptime")
                
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"❌ Erro durante demonstração: {e}", exc_info=True)
                break
        
        if self.shutdown_requested:
            logger.info("🛑 Demonstração interrompida por solicitação de shutdown")
        else:
            logger.info("🏁 Demonstração concluída com sucesso")
    
    def shutdown_system(self):
        """Desliga o sistema de forma segura"""
        logger.info("🛑 Iniciando shutdown graceful do sistema...")
        self.is_running = False
        try:
            for agent_id, agent in self.agents.items():
                try:
                    logger.info(f"⏹️ Parando agente {agent_id}")
                    if hasattr(agent, 'stop'):
                        agent.stop()
                    logger.debug(f"✅ Agente {agent_id} parado")
                except Exception as e:
                    logger.warning(f"⚠️ Erro parando agente {agent_id}: {e}")
            
            if self.network:
                logger.info("⏹️ Parando rede multi-agente...")
                self.network.stop()
                logger.info("✅ Rede multi-agente parada")
            
            uptime = (datetime.now() - self.start_time).total_seconds()
            logger.info(f"⏰ Tempo total de operação: {uptime:.2f} segundos")
            logger.info("✅ Sistema SUNA-ALSHAM encerrado com sucesso")
        except Exception as e:
            logger.error(f"❌ Erro durante shutdown: {e}", exc_info=True)

def main():
    """Função principal do sistema"""
    logger.info("🌟 INICIANDO SUNA-ALSHAM MULTI-AGENT SYSTEM v2.0")
    logger.info("🔧 Versão corrigida com melhorias dos colaboradores")
    logger.info("📅 Iniciado em: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    system_manager = None
    try:
        system_manager = EnhancedSystemManager()
        if not system_manager.initialize_system():
            logger.error("❌ Falha crítica na inicialização do sistema")
            sys.exit(1)
        
        demo_duration = int(os.getenv("DEMO_DURATION", "120"))
        logger.info(f"⏱️ Duração da demonstração: {demo_duration} segundos")
        asyncio.run(system_manager.run_system_demo(demo_duration))
        
    except KeyboardInterrupt:
        logger.info("🛑 Interrupção pelo usuário (Ctrl+C)")
    except Exception as e:
        logger.error(f"❌ Erro crítico no sistema: {str(e)}", exc_info=True)
        raise
    finally:
        if system_manager:
            system_manager.shutdown_system()
        logger.info("👋 SUNA-ALSHAM Multi-Agent System finalizado")

if __name__ == "__main__":
    main()
