"""
SUNA-ALSHAM Sistema Completo v2.0
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
                logger.error("❌ Arquivos necessários não encontrados")
                return False
            
            # Inicializar rede multi-agente
            if MultiAgentNetwork:
                self.network = MultiAgentNetwork()
                await self.network.initialize()
                logger.info("✅ Rede Multi-Agente inicializada")
            else:
                logger.error("❌ MultiAgentNetwork não disponível")
                return False
            
            # Inicializar agentes especializados (3 agentes)
            if create_specialized_agents:
                specialized_agents = await create_specialized_agents()
                await self._register_agents(specialized_agents, 'specialized')
                logger.info(f"✅ {len(specialized_agents)} agentes especializados inicializados")
            else:
                logger.warning("⚠️ Agentes especializados não disponíveis")
            
            # Inicializar agentes com IA (3 agentes)
            if create_ai_agents:
                ai_agents = await create_ai_agents()
                await self._register_agents(ai_agents, 'ai_powered')
                logger.info(f"✅ {len(ai_agents)} agentes com IA inicializados")
            else:
                logger.warning("⚠️ Agentes com IA não disponíveis")
            
            # Inicializar agentes core v3 (3 agentes)
            if create_core_agents_v3:
                core_agents = await create_core_agents_v3()
                await self._register_agents(core_agents, 'core_v3')
                logger.info(f"✅ {len(core_agents)} agentes core v3.0 inicializados")
            else:
                logger.warning("⚠️ Agentes core v3 não disponíveis")
            
            # Inicializar agentes de sistema (3 agentes)
            if create_system_agents:
                system_agents = await create_system_agents()
                await self._register_agents(system_agents, 'system')
                logger.info(f"✅ {len(system_agents)} agentes de sistema inicializados")
            else:
                logger.warning("⚠️ Agentes de sistema não disponíveis")
            
            # Inicializar agentes de serviço (3 agentes)
            if create_service_agents:
                service_agents = await create_service_agents()
                await self._register_agents(service_agents, 'service')
                logger.info(f"✅ {len(service_agents)} agentes de serviço inicializados")
            else:
                logger.warning("⚠️ Agentes de serviço não disponíveis")
            
            # Inicializar agentes meta-cognitivos (2 agentes)
            if create_meta_cognitive_agents:
                meta_agents = await create_meta_cognitive_agents()
                await self._register_agents(meta_agents, 'meta_cognitive')
                logger.info(f"✅ {len(meta_agents)} agentes meta-cognitivos inicializados")
            else:
                logger.warning("⚠️ Agentes meta-cognitivos não disponíveis")
            
            # Configurar orquestração suprema
            await self._setup_supreme_orchestration()
            
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
    
    async def _register_agents(self, agents: Dict[str, Any], category: str):
        """Registra agentes na rede e no sistema"""
        try:
            for agent_name, agent_instance in agents.items():
                # Registrar na rede multi-agente
                if self.network:
                    await self.network.register_agent(
                        agent_instance.agent_id,
                        agent_instance,
                        agent_instance.capabilities
                    )
                
                # Adicionar ao sistema
                self.all_agents[agent_instance.agent_id] = {
                    'instance': agent_instance,
                    'category': category,
                    'name': agent_name,
                    'status': agent_instance.status,
                    'capabilities': agent_instance.capabilities
                }
                
                # Atualizar contadores
                self.agent_categories[category] += 1
                
                self.initialization_log.append({
                    'agent_id': agent_instance.agent_id,
                    'category': category,
                    'name': agent_name,
                    'initialized_at': datetime.now().isoformat()
                })
                
        except Exception as e:
            logger.error(f"❌ Erro registrando agentes {category}: {e}")
    
    async def _setup_supreme_orchestration(self):
        """Configura orquestração suprema"""
        try:
            # Encontrar agente orquestrador
            orchestrator = None
            for agent_id, agent_data in self.all_agents.items():
                if 'orchestrator' in agent_id.lower():
                    orchestrator = agent_data['instance']
                    break
            
            if orchestrator:
                # Registrar todos os agentes no orquestrador
                for agent_id, agent_data in self.all_agents.items():
                    if agent_id != orchestrator.agent_id:
                        await orchestrator.register_agent(
                            agent_id,
                            agent_data['instance'],
                            agent_data['capabilities']
                        )
                
                logger.info(f"👑 Orquestração suprema configurada com {len(self.all_agents)-1} agentes")
            else:
                logger.warning("⚠️ Agente orquestrador não encontrado")
                
        except Exception as e:
            logger.error(f"❌ Erro configurando orquestração: {e}")
    
    async def execute_system_wide_task(self, task: Dict) -> Dict:
        """Executa tarefa em todo o sistema"""
        try:
            # Encontrar orquestrador
            orchestrator = None
            for agent_id, agent_data in self.all_agents.items():
                if 'orchestrator' in agent_id.lower():
                    orchestrator = agent_data['instance']
                    break
            
            if orchestrator:
                result = await orchestrator.orchestrate_system_wide_task(task)
                logger.info(f"🎯 Tarefa executada via orquestração suprema")
                return result
            else:
                # Fallback: executar via rede
                if self.network:
                    result = await self.network.execute_collaborative_task(task)
                    logger.info(f"🔄 Tarefa executada via rede multi-agente")
                    return result
                else:
                    logger.error("❌ Nenhum mecanismo de execução disponível")
                    return {'status': 'error', 'error': 'No execution mechanism available'}
                    
        except Exception as e:
            logger.error(f"❌ Erro executando tarefa: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def perform_meta_cognitive_analysis(self) -> Dict:
        """Realiza análise meta-cognitiva do sistema"""
        try:
            # Encontrar agente meta-cognitivo
            metacognitive = None
            for agent_id, agent_data in self.all_agents.items():
                if 'metacognitive' in agent_id.lower():
                    metacognitive = agent_data['instance']
                    break
            
            if metacognitive:
                system_state = await self.get_system_state()
                result = await metacognitive.perform_self_reflection(system_state)
                logger.info(f"🧠 Análise meta-cognitiva realizada")
                return result
            else:
                logger.warning("⚠️ Agente meta-cognitivo não encontrado")
                return {'status': 'warning', 'message': 'Meta-cognitive agent not available'}
                
        except Exception as e:
            logger.error(f"❌ Erro na análise meta-cognitiva: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def optimize_system_performance(self) -> Dict:
        """Otimiza performance do sistema"""
        try:
            # Encontrar orquestrador
            orchestrator = None
            for agent_id, agent_data in self.all_agents.items():
                if 'orchestrator' in agent_id.lower():
                    orchestrator = agent_data['instance']
                    break
            
            if orchestrator:
                result = await orchestrator.optimize_system_performance()
                logger.info(f"⚡ Sistema otimizado via orquestração")
                return result
            else:
                logger.warning("⚠️ Orquestrador não disponível para otimização")
                return {'status': 'warning', 'message': 'Orchestrator not available'}
                
        except Exception as e:
            logger.error(f"❌ Erro otimizando sistema: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def detect_emergent_behaviors(self) -> Dict:
        """Detecta comportamentos emergentes"""
        try:
            # Encontrar orquestrador
            orchestrator = None
            for agent_id, agent_data in self.all_agents.items():
                if 'orchestrator' in agent_id.lower():
                    orchestrator = agent_data['instance']
                    break
            
            if orchestrator:
                result = await orchestrator.detect_emergent_behaviors()
                logger.info(f"🌟 Comportamentos emergentes analisados")
                return result
            else:
                logger.warning("⚠️ Orquestrador não disponível para detecção")
                return {'status': 'warning', 'message': 'Orchestrator not available'}
                
        except Exception as e:
            logger.error(f"❌ Erro detectando emergência: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def get_system_state(self) -> Dict:
        """Retorna estado completo do sistema"""
        try:
            agent_statuses = {}
            for agent_id, agent_data in self.all_agents.items():
                try:
                    if hasattr(agent_data['instance'], 'get_status'):
                        status = await agent_data['instance'].get_status()
                    else:
                        status = {
                            'agent_id': agent_id,
                            'status': agent_data['status'],
                            'category': agent_data['category']
                        }
                    agent_statuses[agent_id] = status
                except Exception as e:
                    logger.warning(f"⚠️ Erro obtendo status de {agent_id}: {e}")
                    agent_statuses[agent_id] = {'status': 'error', 'error': str(e)}
            
            return {
                'system_status': self.system_status,
                'total_agents': self.total_agents,
                'agent_categories': self.agent_categories,
                'agent_statuses': agent_statuses,
                'network_status': self.network.status if self.network else 'unavailable',
                'created_at': self.created_at.isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo estado do sistema: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def get_comprehensive_report(self) -> Dict:
        """Gera relatório abrangente do sistema"""
        try:
            system_state = await self.get_system_state()
            
            # Análise meta-cognitiva
            meta_analysis = await self.perform_meta_cognitive_analysis()
            
            # Detecção de emergência
            emergence_analysis = await self.detect_emergent_behaviors()
            
            # Estatísticas de performance
            performance_stats = {
                'agents_active': sum(1 for agent in self.all_agents.values() if agent['status'] == 'active'),
                'agents_total': self.total_agents,
                'categories_distribution': self.agent_categories,
                'system_uptime': str(datetime.now() - self.created_at),
                'initialization_success_rate': len(self.all_agents) / 20 if self.total_agents > 0 else 0
            }
            
            return {
                'report_id': f"comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'system_state': system_state,
                'meta_cognitive_analysis': meta_analysis,
                'emergence_analysis': emergence_analysis,
                'performance_statistics': performance_stats,
                'initialization_log': self.initialization_log,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro gerando relatório: {e}")
            return {'status': 'error', 'error': str(e)}

# Função principal para demonstração
async def main():
    """Função principal para demonstração do sistema"""
    try:
        logger.info("🚀 Iniciando demonstração SUNA-ALSHAM v2.0")
        
        # Criar e inicializar sistema
        system = SUNAAlshamSystemV2()
        success = await system.initialize_complete_system()
        
        if not success:
            logger.error("❌ Falha na inicialização do sistema")
            return
        
        # Demonstrar capacidades
        logger.info("🎯 Executando tarefa de demonstração")
        demo_task = {
            'id': 'demo_task_001',
            'type': 'data_analysis',
            'complexity': 'medium',
            'priority': 'high',
            'description': 'Análise demonstrativa do sistema multi-agente'
        }
        
        task_result = await system.execute_system_wide_task(demo_task)
        logger.info(f"✅ Tarefa executada: {task_result.get('orchestration_result', {}).get('execution_status', 'unknown')}")
        
        # Análise meta-cognitiva
        logger.info("🧠 Realizando análise meta-cognitiva")
        meta_result = await system.perform_meta_cognitive_analysis()
        logger.info(f"🔮 Auto-consciência: {meta_result.get('self_awareness_level', 'unknown')}")
        
        # Otimização do sistema
        logger.info("⚡ Otimizando performance do sistema")
        optimization_result = await system.optimize_system_performance()
        logger.info(f"📈 Eficiência: {optimization_result.get('new_system_efficiency', 'unknown')}")
        
        # Detecção de emergência
        logger.info("🌟 Detectando comportamentos emergentes")
        emergence_result = await system.detect_emergent_behaviors()
        logger.info(f"🔍 Emergência detectada: {emergence_result.get('system_evolution_indicator', False)}")
        
        # Relatório final
        logger.info("📊 Gerando relatório abrangente")
        final_report = await system.get_comprehensive_report()
        
        # Estatísticas finais
        stats = final_report.get('performance_statistics', {})
        logger.info("🎉 DEMONSTRAÇÃO COMPLETA!")
        logger.info(f"📊 Agentes ativos: {stats.get('agents_active', 0)}/{stats.get('agents_total', 0)}")
        logger.info(f"⏱️ Tempo de execução: {stats.get('system_uptime', 'unknown')}")
        logger.info(f"✅ Taxa de sucesso: {stats.get('initialization_success_rate', 0):.1%}")
        
        # Manter sistema rodando
        logger.info("🔄 Sistema em execução... (Ctrl+C para parar)")
        while True:
            await asyncio.sleep(60)  # Verificar a cada minuto
            
            # Status periódico
            current_time = datetime.now().strftime('%H:%M:%S')
            logger.info(f"📊 Status {current_time}: {system.total_agents} agentes ativos")
            
    except KeyboardInterrupt:
        logger.info("⏹️ Sistema interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro na demonstração: {e}")

if __name__ == "__main__":
    # Configurar variáveis de ambiente se necessário
    if not os.getenv('OPENAI_API_KEY'):
        logger.warning("⚠️ OPENAI_API_KEY não configurada - IA simulada será usada")
    
    if not os.getenv('REDIS_URL'):
        logger.warning("⚠️ REDIS_URL não configurada - cache local será usado")
    
    # Executar sistema
    asyncio.run(main())

