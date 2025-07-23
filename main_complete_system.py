"""
SUNA-ALSHAM Sistema Completo
Sistema principal com correção de importações
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Função principal com tratamento de erros melhorado"""
    try:
        logger.info(f"🚀 Executando de: {__file__}")
        logger.info(f"📁 Diretório atual: {os.getcwd()}")
        logger.info(f"📋 Arquivos no diretório: {os.listdir('.')}")
        
        # Verificar variáveis de ambiente
        openai_key = os.getenv('OPENAI_API_KEY')
        redis_url = os.getenv('REDIS_URL')
        
        logger.info(f"🔑 OPENAI_API_KEY configurada: {'✅' if openai_key else '❌'}")
        logger.info(f"🔗 REDIS_URL configurada: {'✅' if redis_url else '❌'}")
        
        # Verificar se pasta suna_alsham existe
        suna_path = Path('suna_alsham')
        if not suna_path.exists():
            logger.error("❌ Pasta 'suna_alsham' não encontrada!")
            return False
        
        # Listar arquivos na pasta suna_alsham
        suna_files = list(suna_path.glob('*.py'))
        logger.info(f"📁 Arquivos em suna_alsham/: {[f.name for f in suna_files]}")
        
        # Tentar importações com tratamento de erro individual
        try:
            from suna_alsham.multi_agent_network import network
            logger.info("✅ multi_agent_network importado com sucesso")
        except ImportError as e:
            logger.error(f"❌ Erro importando multi_agent_network: {e}")
            return False
        
        try:
            from suna_alsham.specialized_agents import create_specialized_agents
            logger.info("✅ specialized_agents importado com sucesso")
        except ImportError as e:
            logger.error(f"❌ Erro importando specialized_agents: {e}")
            return False
        
        try:
            from suna_alsham.ai_powered_agents import create_ai_agents
            logger.info("✅ ai_powered_agents importado com sucesso")
        except ImportError as e:
            logger.error(f"❌ Erro importando ai_powered_agents: {e}")
            return False
        
        # Se chegou até aqui, todas as importações funcionaram
        logger.info("🎉 Todas as importações funcionaram!")
        
        # Inicializar sistema
        asyncio.run(initialize_system(network, create_specialized_agents, create_ai_agents))
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro geral no sistema: {e}")
        import traceback
        logger.error(f"📋 Traceback: {traceback.format_exc()}")
        return False

async def initialize_system(network, create_specialized_agents, create_ai_agents):
    """Inicializa o sistema completo"""
    try:
        logger.info("🚀 Inicializando sistema SUNA-ALSHAM...")
        
        # Inicializar rede
        await network.initialize()
        
        # Criar agentes especializados
        specialized_agents = await create_specialized_agents()
        
        # Criar agentes com IA
        ai_agents = await create_ai_agents()
        
        # Registrar agentes na rede
        all_agents = {**specialized_agents, **ai_agents}
        for agent_name, agent in all_agents.items():
            await network.register_agent(agent_name, agent)
        
        # Status final
        status = await network.get_network_status()
        logger.info(f"✅ Sistema inicializado com {status['stats']['total_agents']} agentes")
        
        # Manter sistema rodando
        logger.info("🔄 Sistema em execução...")
        while True:
            await asyncio.sleep(60)  # Aguardar 1 minuto
            status = await network.get_network_status()
            logger.info(f"📊 Status: {status['stats']['active_agents']} agentes ativos")
            
    except Exception as e:
        logger.error(f"❌ Erro inicializando sistema: {e}")
        raise

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
