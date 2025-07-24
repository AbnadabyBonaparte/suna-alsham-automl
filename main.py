import logging
from multi_agent_network import MultiAgentNetwork
from main_complete_system_v2 import SUNAAlshamSystemV2
import asyncio
import uvicorn
from typing import Optional

logger = logging.getLogger(__name__)

class SystemApp:
    def __init__(self):
        self.system = None

    async def startup(self):
        logger.info("Iniciando sistema...")
        self.system = SUNAAlshamSystemV2()
        await self.system.initialize_complete_system()
        logger.info("Sistema inicializado com sucesso")

    async def shutdown(self):
        logger.info("Encerrando sistema...")
        if self.system:
            # Adicione lógica de desligamento, se necessário
            pass

    async def __call__(self, scope):
        if scope["type"] == "lifespan":
            while True:
                message = await scope["receive"]()
                if message["type"] == "lifespan.startup":
                    await self.startup()
                    await scope["send"]({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await self.shutdown()
                    await scope["send"]({"type": "lifespan.shutdown.complete"})
                    break
        else:
            raise NotImplementedError("Apenas suporte a lifespan")

app = SystemApp()

if __name__ == "__main__":
    config = uvicorn.Config(app, host="0.0.0.0", port=8080)
    server = uvicorn.Server(config)
    asyncio.run(server.serve())
