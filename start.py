"""
ALSHAM QUANTUM - Sistema de Inicialização Minimalista
Apenas para responder no /health
"""
import os
import logging
import uvicorn
from fastapi import FastAPI

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI mínima
app = FastAPI(
    title="ALSHAM QUANTUM",
    description="Sistema Multi-Agente de IA Autônomo",
    version="2.0.0"
)

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "system": "ALSHAM QUANTUM",
        "version": "2.0.0",
        "status": "online",
        "message": "Sistema funcionando"
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde"""
    return {
        "status": "healthy",
        "system": "ALSHAM QUANTUM",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"🚀 Iniciando ALSHAM QUANTUM na porta {port}")
    
    uvicorn.run(
        "start:app",
        host=host,
        port=port,
        log_level="info"
    )
