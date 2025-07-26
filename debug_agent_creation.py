#!/usr/bin/env python3
"""
Debug Enterprise - Por que os agentes não estão sendo criados?
"""

import asyncio
import logging
import sys
import traceback
from datetime import datetime

# Configurar logging detalhado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)8s] %(name)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger('AgentDebug')

async def debug_agent_creation():
    """Debug detalhado da criação de agentes"""
    
    logger.info("="*60)
    logger.info("DEBUG: CRIAÇÃO DE AGENTES")
    logger.info("="*60)
    
    try:
        # 1. Importar sistema
        logger.info("\n1️⃣ Importando sistema principal...")
        from main_complete_system_v2 import SUNAAlshamSystemV2
        from multi_agent_network import MultiAgentNetwork
        
        # 2. Criar rede
        logger.info("\n2️⃣ Criando rede...")
        network = MultiAgentNetwork()
        logger.info(f"   Rede criada: {network}")
        
        # 3. Verificar módulos de agentes
        logger.info("\n3️⃣ Verificando módulos de agentes...")
        
        agent_modules = [
            'specialized_agents',
            'ai_powered_agents',
            'core_agents_v3',
            'system_agents',
            'service_agents',
            'meta_cognitive_agents',
            'code_analyzer_agent',
            'web_search_agent',
            'code_corrector_agent',
            'performance_monitor_agent'
        ]
        
        for module_name in agent_modules:
            try:
                module = __import__(module_name)
                logger.info(f"✅ {module_name} importado")
                
                # Verificar se tem create_agents
                if hasattr(module, 'create_agents'):
                    logger.info(f"   └─ create_agents() encontrada")
                    
                    # Tentar chamar create_agents
                    try:
                        logger.info(f"   └─ Chamando create_agents()...")
                        if asyncio.iscoroutinefunction(module.create_agents):
                            agents = await module.create_agents(network)
                        else:
                            agents = module.create_agents(network)
                        
                        if agents:
                            logger.info(f"   └─ ✅ {len(agents)} agentes criados!")
                            for agent in agents[:3]:  # Mostrar primeiros 3
                                logger.info(f"      └─ {agent.agent_id if hasattr(agent, 'agent_id') else agent}")
                        else:
                            logger.warning(f"   └─ ⚠️ create_agents() retornou vazio/None")
                            
                    except Exception as e:
                        logger.error(f"   └─ ❌ Erro ao chamar create_agents(): {e}")
                        logger.error(f"      Tipo do erro: {type(e).__name__}")
                        logger.error(f"      Traceback:\n{traceback.format_exc()}")
                else:
                    logger.warning(f"   └─ ⚠️ Módulo não tem create_agents()")
                    
                    # Verificar outras funções
                    funcs = [attr for attr in dir(module) if callable(getattr(module, attr)) and not attr.startswith('_')]
                    logger.info(f"   └─ Funções disponíveis: {funcs[:5]}")
                    
            except Exception as e:
                logger.error(f"❌ Erro com {module_name}: {e}")
        
        # 4. Testar criação via SUNAAlshamSystemV2
        logger.info("\n4️⃣ Testando via SUNAAlshamSystemV2...")
        system = SUNAAlshamSystemV2()
        
        # Verificar método criar_todos_agentes
        if hasattr(system, 'criar_todos_agentes'):
            logger.info("   └─ método criar_todos_agentes() existe")
            
            # Chamar com network global
            import main_complete_system_v2
            main_complete_system_v2.network = network
            
            agents = await system.criar_todos_agentes()
            logger.info(f"   └─ Resultado: {len(agents) if agents else 0} agentes")
            
            if not agents:
                logger.error("   └─ ❌ Nenhum agente foi criado!")
        else:
            logger.error("   └─ ❌ método criar_todos_agentes() não encontrado!")
            
        # 5. Verificar estrutura de SUNAAlshamSystemV2
        logger.info("\n5️⃣ Analisando estrutura de SUNAAlshamSystemV2...")
        logger.info(f"   Métodos disponíveis: {[m for m in dir(system) if not m.startswith('_')]}")
        
    except Exception as e:
        logger.error(f"\n❌ ERRO CRÍTICO: {e}")
        logger.error(traceback.format_exc())

async def main():
    """Executa debug completo"""
    start_time = datetime.now()
    
    await debug_agent_creation()
    
    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info(f"\n⏱️ Debug completado em {elapsed:.2f} segundos")

if __name__ == "__main__":
    asyncio.run(main())
