#!/usr/bin/env python3
"""
Arquivo principal do SUNA-ALSHAM System
Sistema Multi-Agente com FastAPI
"""

import logging
from multi_agent_network import MultiAgentNetwork
from agent_loader import initialize_all_agents
import asyncio
import uvicorn
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# Criar app FastAPI
app = FastAPI(title="SUNA-ALSHAM System")

# Sistema global - usando MultiAgentNetwork diretamente
system: Optional[MultiAgentNetwork] = None

@app.on_event("startup")
async def startup_event():
    """Inicializa o sistema no startup"""
    global system
    logger.info("Iniciando sistema SUNA-ALSHAM...")
    
    # Inicializar com MultiAgentNetwork
    system = MultiAgentNetwork()
    await system.initialize()
    
    # Carregar todos os 24+ agentes
    logger.info("🚀 Carregando agentes do sistema...")
    agent_result = await initialize_all_agents(system)
    logger.info(f"✅ Resultado do carregamento: {agent_result.get('agents_loaded_successfully', 0)} agentes carregados")
    
    logger.info("Sistema inicializado com sucesso")

@app.on_event("shutdown")
async def shutdown_event():
    """Desliga o sistema"""
    logger.info("Encerrando sistema...")
    if system:
        await system.shutdown()

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "name": "SUNA-ALSHAM System v2.0",
        "status": "active",
        "agents": len(system.agents) if system and hasattr(system, 'agents') else 0
    }

@app.get("/health")
async def health():
    """Endpoint de health check"""
    if system:
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "initialized": True,
                "agents_count": len(system.agents) if hasattr(system, 'agents') else 0,
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
        return {
            "status": "running",
            "agents": len(system.agents) if hasattr(system, 'agents') else 0,
            "system_type": "MultiAgentNetwork"
        }
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
