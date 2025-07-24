from multi_agent_network import MultiAgentNetwork
from main_complete_system_v2 import SUNAAlshamSystemV2
import logging
import asyncio

logger = logging.getLogger(__name__)

async def startup():
    system = SUNAAlshamSystemV2()
    await system.initialize_complete_system()
    logger.info("Sistema inicializado, aguardando tarefas")

if __name__ == "__main__":
    asyncio.run(startup())
