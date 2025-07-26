import logging
from multi_agent_network import MultiAgentNetwork
from main_complete_system_v2 import SUNAAlshamSystemV2
import asyncio
import uvicorn
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# Criar app FastAPI
app = FastAPI(title="SUNA-ALSHAM System")

# Sistema global
system: Optional[SUNAAlshamSystemV2] = None

@app.on_event("startup")
async def startup_event():
    """Inicializa o sistema no startup"""
    global system
    logger.info("Iniciando sistema SUNA-ALSHAM...")
    system = SUNAAlshamSystemV2()
    await system.initialize_complete_system()
    logger.info("Sistema inicializado com sucesso")

@app.on_event("shutdown")
async def shutdown_event():
    """Desliga o sistema"""
    logger.info("Encerrando sistema...")
    # Adicione lógica de shutdown se necessário

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "name": "SUNA-ALSHAM System v2.0",
        "status": "active",
        "agents": len(system.agents) if system else 0
    }

@app.get("/health")
async def health():
    """Endpoint de health check"""
    if system and system.initialized:
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "initialized": True,
                "agents_count": len(system.agents),
                "message": "System is running"
            }
        )
    else:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "initialized": False,
                "message": "System not initialized"
            }
        )

@app.get("/status")
async def status():
    """Status detalhado do sistema"""
    if system:
        return system.get_status()
    return {"status": "not_initialized"}

if __name__ == "__main__":
    # Configurar uvicorn
    config = uvicorn.Config(
        app, 
        host="0.0.0.0", 
        port=8080,
        log_level="info"
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())
