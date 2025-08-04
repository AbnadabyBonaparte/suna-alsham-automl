"""
ALSHAM QUANTUM - Sistema de Inicialização Principal
Usando arquitetura original existente
"""
import os
import sys
import logging
import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Importações do SEU sistema ORIGINAL
try:
    from suna_alsham_core.agent_loader import load_all_agents
    from suna_alsham_core.bootstrap import run_bootstrap  # Seu bootstrap original
    ORIGINAL_SYSTEM_AVAILABLE = True
except ImportError as e:
    logger.error(f"Erro ao importar sistema original: {e}")
    ORIGINAL_SYSTEM_AVAILABLE = False

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Variáveis globais
agents = {}
system_status = {
    "bootstrap_completed": False,
    "system_healthy": False,
    "agents_active": 0,
    "warnings": 0,
    "errors": 0
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciamento do ciclo de vida da aplicação"""
    global agents, system_status
    
    logger.info("🚀 ALSHAM QUANTUM - Iniciando sistema...")
    
    try:
        if ORIGINAL_SYSTEM_AVAILABLE:
            # Usar SEU sistema original
            logger.info("⚡ Executando bootstrap original...")
            
            # Executar SEU bootstrap
            bootstrap_success = await run_bootstrap() if asyncio.iscoroutinefunction(run_bootstrap) else run_bootstrap()
            
            if bootstrap_success:
                logger.info("✅ Bootstrap original executado com sucesso!")
                
                # Carregar SEUS agentes
                logger.info("🤖 Carregando agentes via agent_loader...")
                agents = load_all_agents()
                
                if agents:
                    system_status["agents_active"] = len(agents)
                    system_status["bootstrap_completed"] = True
                    system_status["system_healthy"] = True
                    
                    logger.info(f"🎊 Sistema carregado com {len(agents)} agentes!")
                    logger.info("🚀 ALSHAM QUANTUM - Sistema 100% OPERACIONAL!")
                else:
                    logger.warning("⚠️ Nenhum agente carregado")
                    system_status["warnings"] += 1
                    system_status["system_healthy"] = True  # Continuar mesmo assim
            else:
                logger.error("❌ Bootstrap original falhou")
                system_status["errors"] += 1
                # MAS não fazer shutdown - continuar degradado
                system_status["system_healthy"] = False
        else:
            # Sistema mínimo se não conseguir carregar o original
            logger.warning("⚠️ Sistema original não disponível - modo degradado")
            system_status["bootstrap_completed"] = True
            system_status["system_healthy"] = False
            system_status["warnings"] += 1
            
    except Exception as e:
        logger.error(f"💥 Erro na inicialização: {e}")
        system_status["errors"] += 1
        system_status["system_healthy"] = False
        # NÃO fazer shutdown - deixar o sistema responder
    
    # Sistema iniciado - yield para manter rodando
    yield
    
    # Shutdown gracioso
    logger.info("🔄 Shutdown gracioso do ALSHAM QUANTUM...")
    if agents:
        logger.info(f"  ✅ {len(agents)} agentes desligados")

# Criar aplicação FastAPI
app = FastAPI(
    title="ALSHAM QUANTUM",
    description="Sistema Multi-Agente de IA Autônomo",
    version="2.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ROTAS DA API =====

@app.get("/")
async def root():
    """Endpoint raiz com status do sistema"""
    return {
        "system": "ALSHAM QUANTUM",
        "version": "2.0.0",
        "status": "online" if system_status["system_healthy"] else "degraded",
        "message": "🚀 Sistema Multi-Agente de IA Autônomo",
        "bootstrap_completed": system_status["bootstrap_completed"],
        "agents_active": system_status["agents_active"],
        "warnings": system_status["warnings"],
        "errors": system_status["errors"]
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde detalhada"""
    return {
        "status": "healthy" if system_status["system_healthy"] else "unhealthy",
        "bootstrap_completed": system_status["bootstrap_completed"],
        "agents_loaded": len(agents) if agents else 0,
        "original_system": ORIGINAL_SYSTEM_AVAILABLE,
        "metrics": {
            "agents_active": system_status["agents_active"],
            "warnings": system_status["warnings"],
            "errors": system_status["errors"]
        }
    }

@app.get("/status")
async def system_status_endpoint():
    """Status completo do sistema"""
    return {
        "system_name": "ALSHAM QUANTUM",
        "version": "2.0.0",
        "operational": system_status["system_healthy"],
        "bootstrap": {
            "completed": system_status["bootstrap_completed"],
            "agents_loaded": len(agents) if agents else 0,
            "original_system": ORIGINAL_SYSTEM_AVAILABLE
        },
        "health": {
            "overall": "healthy" if system_status["system_healthy"] else "degraded",
            "warnings": system_status["warnings"],
            "errors": system_status["errors"]
        }
    }

@app.get("/agents")
async def list_agents():
    """Listar agentes disponíveis"""
    if not agents:
        return {"agents": [], "count": 0, "message": "Nenhum agente carregado"}
    
    return {
        "agents": list(agents.keys()) if isinstance(agents, dict) else ["agents_loaded"],
        "count": len(agents) if agents else 0,
        "status": "active"
    }

# ===== INICIALIZAÇÃO PRINCIPAL =====

if __name__ == "__main__":
    # Configurações para diferentes ambientes
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"🚀 Iniciando ALSHAM QUANTUM na porta {port}")
    
    # Configurações do uvicorn
    uvicorn_config = {
        "app": "start:app",
        "host": host,
        "port": port,
        "log_level": "info",
        "access_log": True,
        "workers": 1
    }
    
    # Rodar servidor
    uvicorn.run(**uvicorn_config)
