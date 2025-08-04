#!/usr/bin/env python3
"""
ALSHAM QUANTUM - Sistema de Inicialização Principal
[Quantum Version 2.0] - Startup with Quantum Bootstrap
"""

import asyncio
import logging
import os
import signal
import sys
from contextlib import asynccontextmanager
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configuração de logging antes de qualquer import
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Imports do sistema
from suna_alsham_core.quantum_bootstrap import execute_quantum_bootstrap
from suna_alsham_core.system import SUNAAlshamSystemV2

# Estado global do sistema
quantum_system: SUNAAlshamSystemV2 = None
system_ready = False
bootstrap_report = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação com bootstrap quantum."""
    global quantum_system, system_ready, bootstrap_report
    
    logger.info("🚀 ALSHAM QUANTUM - Iniciando sistema...")
    
    try:
        # Fase 1: Bootstrap Quantum
        logger.info("🔧 Executando Bootstrap Quantum...")
        bootstrap_success = await execute_quantum_bootstrap()
        
        if not bootstrap_success:
            logger.critical("❌ Bootstrap Quantum falhou! Sistema não pode iniciar.")
            sys.exit(1)
        
        # Fase 2: Inicialização do Sistema
        logger.info("🤖 Inicializando Sistema Multi-Agente...")
        quantum_system = SUNAAlshamSystemV2()
        
        initialization_success = await quantum_system.initialize_complete_system()
        
        if not initialization_success:
            logger.critical("❌ Inicialização do sistema falhou!")
            sys.exit(1)
        
        system_ready = True
        logger.info("✅ ALSHAM QUANTUM operacional!")
        
        yield  # Aplicação rodando
        
    except Exception as e:
        logger.critical(f"❌ Erro crítico na inicialização: {e}", exc_info=True)
        sys.exit(1)
    
    finally:
        # Shutdown gracioso
        logger.info("🔄 Iniciando shutdown gracioso...")
        system_ready = False
        
        if quantum_system:
            try:
                await quantum_system.network.message_bus.stop()
                logger.info("✅ Sistema encerrado graciosamente")
            except Exception as e:
                logger.error(f"⚠️ Erro no shutdown: {e}")

# Criação da aplicação FastAPI
app = FastAPI(
    title="ALSHAM QUANTUM",
    description="Sistema Multi-Agente de IA com Capacidades Quantum",
    version="2.0.0",
    lifespan=lifespan
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("API_CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ROTAS DA API =====

@app.get("/")
async def root():
    """Rota raiz com informações do sistema."""
    if not system_ready:
        raise HTTPException(status_code=503, detail="Sistema ainda inicializando")
    
    return {
        "system": "ALSHAM QUANTUM",
        "version": "2.0.0",
        "status": "operational",
        "capabilities": [
            "quantum_orchestration",
            "multi_ai_providers", 
            "intelligent_recovery",
            "self_evolution",
            "quantum_coherence"
        ],
        "message": "Sistema Multi-Agente de IA Quantum operacional"
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde detalhada."""
    if not system_ready or not quantum_system:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "message": "Sistema não inicializado",
                "ready": False
            }
        )
    
    try:
        system_status = quantum_system.get_system_status()
        
        health_status = {
            "status": "healthy" if system_status["system_status"] == "active" else "degraded",
            "ready": True,
            "timestamp": system_status.get("uptime_seconds", 0),
            "agents": {
                "total": system_status.get("total_agents", 0),
                "active": system_status.get("active_agents", 0),
                "categories": system_status.get("agent_categories", {})
            },
            "system": {
                "status": system_status.get("system_status", "unknown"),
                "uptime_seconds": system_status.get("uptime_seconds", 0),
                "failed_modules": system_status.get("failed_modules", [])
            }
        }
        
        return health_status
        
    except Exception as e:
        logger.error(f"Erro na verificação de saúde: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Erro interno: {str(e)}",
                "ready": False
            }
        )

@app.get("/status")
async def system_status():
    """Status completo do sistema."""
    if not system_ready or not quantum_system:
        raise HTTPException(status_code=503, detail="Sistema não disponível")
    
    try:
        return quantum_system.get_system_status()
    except Exception as e:
        logger.error(f"Erro obtendo status: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/metrics")
async def system_metrics():
    """Métricas detalhadas do sistema."""
    if not system_ready or not quantum_system:
        raise HTTPException(status_code=503, detail="Sistema não disponível")
    
    try:
        base_status = quantum_system.get_system_status()
        
        # Adiciona métricas específicas
        metrics = {
            **base_status,
            "quantum_metrics": {
                "coherence": 0.95,  # Placeholder
                "evolution_cycles": 0,  # Placeholder
                "learning_rate": 0.1   # Placeholder
            }
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Erro obtendo métricas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/submit_task")
async def submit_task(task_data: Dict[str, Any]):
    """Submete uma tarefa para execução pelo sistema."""
    if not system_ready or not quantum_system:
        raise HTTPException(status_code=503, detail="Sistema não disponível")
    
    try:
        content = task_data.get("content") or task_data.get("task") or task_data.get("request")
        
        if not content:
            raise HTTPException(status_code=400, detail="Conteúdo da tarefa não especificado")
        
        # Envia tarefa para o API Gateway
        api_gateway = quantum_system.all_agents.get("api_gateway_001")
        
        if not api_gateway:
            raise HTTPException(status_code=500, detail="API Gateway não disponível")
        
        # Simula processamento (implementação real seria mais complexa)
        await api_gateway.handle_incoming({
            "content": content,
            "context": task_data.get("context", {}),
            "priority": task_data.get("priority", "normal")
        })
        
        return {
            "status": "accepted",
            "message": "Tarefa aceita para processamento",
            "task_preview": content[:100] + "..." if len(content) > 100 else content
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro processando tarefa: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/agents")
async def list_agents():
    """Lista todos os agentes ativos no sistema."""
    if not system_ready or not quantum_system:
        raise HTTPException(status_code=503, detail="Sistema não disponível")
    
    try:
        agents_info = {}
        
        for agent_id, agent in quantum_system.all_agents.items():
            agents_info[agent_id] = {
                "type": agent.agent_type.value if hasattr(agent, 'agent_type') else "unknown",
                "status": agent.status if hasattr(agent, 'status') else "unknown",
                "capabilities": agent.capabilities if hasattr(agent, 'capabilities') else []
            }
        
        return {
            "total_agents": len(agents_info),
            "agents": agents_info,
            "categories": quantum_system.agent_categories
        }
        
    except Exception as e:
        logger.error(f"Erro listando agentes: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# ===== SIGNAL HANDLERS =====

def signal_handler(signum, frame):
    """Handler para sinais do sistema."""
    logger.info(f"Sinal {signum} recebido. Iniciando shutdown gracioso...")
    # O lifespan context manager cuidará do shutdown

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# ===== FUNÇÃO PRINCIPAL =====

def main():
    """Função principal de inicialização."""
    # Configurações do servidor
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    workers = int(os.environ.get("MAX_WORKERS", 1))
    
    # Log de inicialização
    logger.info(f"🚀 Iniciando ALSHAM QUANTUM na porta {port}")
    logger.info(f"🌍 Ambiente: {os.environ.get('ENVIRONMENT', 'production')}")
    logger.info(f"👥 Workers: {workers}")
    
    # Inicia o servidor
    uvicorn.run(
        "start:app",
        host=host,
        port=port,
        workers=workers,
        log_level=os.environ.get("LOG_LEVEL", "info").lower(),
        access_log=True,
        use_colors=True,
        loop="asyncio"
    )

if __name__ == "__main__":
    main()
