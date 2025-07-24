# main_orchestrator.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app FastAPI
app = FastAPI(
    title="SUNA-ALSHAM Sistema Multi-Agente",
    description="API do Sistema Multi-Agente SUNA-ALSHAM",
    version="2.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sistema global
system = None

@app.on_event("startup")
async def startup():
    """Inicializar sistema na startup"""
    global system
    try:
        logger.info("🚀 Iniciando SUNA-ALSHAM Sistema Multi-Agente...")
        from main_complete_system_v2 import SUNAAlshamSystemV2
        system = SUNAAlshamSystemV2()
        success = await system.initialize_complete_system()
        if success:
            logger.info("✅ Sistema inicializado com sucesso!")
        else:
            logger.error("❌ Falha na inicialização do sistema")
    except Exception as e:
        logger.error(f"❌ Erro na startup: {e}")

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "SUNA-ALSHAM Sistema Multi-Agente Online",
        "version": "2.0",
        "status": "active" if system and system.system_status == 'active' else "initializing",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/metrics")
async def get_metrics():
    """Obter métricas do sistema"""
    try:
        if system and system.system_status == 'active':
            return system.get_system_status()
        else:
            return {
                "error": "Sistema não inicializado",
                "status": "initializing",
                "message": "Aguarde a inicialização completa"
            }
    except Exception as e:
        logger.error(f"Erro obtendo métricas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics_alt():
    """Endpoint alternativo para métricas"""
    return await get_metrics()

@app.get("/api/health")
async def health_check():
    """Health check do sistema"""
    try:
        if system and system.system_status == 'active':
            return {
                "status": "healthy",
                "agents": len(system.all_agents),
                "uptime": system._get_uptime(),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "initializing",
                "message": "Sistema sendo inicializado",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/status")
async def status():
    """Status geral do sistema"""
    return await health_check()

@app.get("/api/system-status")
async def system_status():
    """Status detalhado do sistema"""
    return await get_metrics()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
