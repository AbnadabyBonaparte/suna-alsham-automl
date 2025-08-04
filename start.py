"""
ALSHAM QUANTUM - Sistema de Inicialização Principal
Correção crítica da lógica de bootstrap validation
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

# Importações do sistema
from suna_alsham_core.quantum_bootstrap import run_quantum_bootstrap
from suna_alsham_core.meta_cognitive_agents import QuantumOrchestrator
from suna_alsham_core.real_evolution_engine import RealEvolutionEngine
from suna_alsham_core.notification_agent import NotificationAgent
from suna_alsham_core.ai_powered_agents import AIAnalyzer

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Instâncias globais do sistema
orchestrator = None
evolution_engine = None
notification_agent = None
ai_analyzer = None
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
    global orchestrator, evolution_engine, notification_agent, ai_analyzer, system_status
    
    logger.info("🚀 ALSHAM QUANTUM - Iniciando sistema...")
    
    try:
        # ===== EXECUÇÃO DO BOOTSTRAP QUANTUM =====
        logger.info("⚡ Executando Bootstrap Quantum...")
        bootstrap_success = await run_quantum_bootstrap()
        
        # ===== LÓGICA CORRIGIDA DE VALIDAÇÃO =====
        if bootstrap_success:
            logger.info("✅ Bootstrap Quantum executado com SUCESSO!")
            system_status["bootstrap_completed"] = True
            
            # Inicializar componentes principais
            try:
                logger.info("🤖 Inicializando componentes principais...")
                
                # Orchestrator
                logger.info("  🧠 Inicializando Quantum Orchestrator...")
                orchestrator = QuantumOrchestrator()
                await orchestrator.initialize()
                logger.info("    ✅ Quantum Orchestrator ativo")
                
                # Evolution Engine
                logger.info("  🧬 Inicializando Real Evolution Engine...")
                evolution_engine = RealEvolutionEngine()
                await evolution_engine.initialize()
                logger.info("    ✅ Real Evolution Engine ativo")
                
                # Notification Agent
                logger.info("  📧 Inicializando Notification Agent...")
                notification_agent = NotificationAgent()
                await notification_agent.initialize()
                logger.info("    ✅ Notification Agent ativo")
                
                # AI Analyzer
                logger.info("  🤖 Inicializando AI Analyzer...")
                ai_analyzer = AIAnalyzer()
                await ai_analyzer.initialize()
                logger.info("    ✅ AI Analyzer ativo")
                
                system_status["agents_active"] = 4
                system_status["system_healthy"] = True
                
                logger.info("🎊 ALSHAM QUANTUM - Sistema 100% OPERACIONAL!")
                logger.info("🚀 Todos os componentes ativos e funcionando")
                
                # Notificação de sucesso
                if notification_agent:
                    try:
                        await notification_agent.send_notification(
                            "system_startup",
                            "🎊 ALSHAM QUANTUM ONLINE!\n\n"
                            "✅ Bootstrap: Sucesso\n"
                            "✅ Agentes: 4/4 Ativos\n" 
                            "✅ Sistema: 100% Operacional\n\n"
                            "🚀 Pronto para receber tarefas!"
                        )
                    except Exception as e:
                        logger.warning(f"⚠️ Notificação de startup falhou: {e}")
                        system_status["warnings"] += 1
                
            except Exception as e:
                logger.error(f"❌ Erro na inicialização de componentes: {e}")
                system_status["errors"] += 1
                # MAS NÃO FAZEMOS SHUTDOWN! Sistema pode funcionar parcialmente
                logger.warning("⚠️ Sistema continuando com funcionalidade limitada")
                
        else:
            # Bootstrap falhou em validações CRÍTICAS
            logger.critical("❌ Bootstrap Quantum falhou em validações CRÍTICAS!")
            logger.critical("🔴 Sistema não pode iniciar sem componentes essenciais")
            logger.info("🔄 Iniciando shutdown gracioso...")
            
            # Só aqui que fazemos shutdown por falha crítica real
            sys.exit(1)
            
    except Exception as e:
        logger.critical(f"💥 Erro crítico na inicialização: {e}")
        logger.info("🔄 Iniciando shutdown gracioso...")
        sys.exit(1)
    
    # Sistema iniciado - yield para manter rodando
    yield
    
    # Shutdown gracioso
    logger.info("🔄 Iniciando shutdown gracioso do ALSHAM QUANTUM...")
    
    try:
        if orchestrator:
            await orchestrator.shutdown()
            logger.info("  ✅ Quantum Orchestrator desligado")
            
        if evolution_engine:
            await evolution_engine.shutdown()
            logger.info("  ✅ Real Evolution Engine desligado")
            
        if notification_agent:
            await notification_agent.shutdown()
            logger.info("  ✅ Notification Agent desligado")
            
        if ai_analyzer:
            await ai_analyzer.shutdown()
            logger.info("  ✅ AI Analyzer desligado")
            
        logger.info("✅ ALSHAM QUANTUM - Shutdown completo")
        
    except Exception as e:
        logger.error(f"❌ Erro durante shutdown: {e}")

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
        "components": {
            "orchestrator": orchestrator is not None,
            "evolution_engine": evolution_engine is not None, 
            "notification_agent": notification_agent is not None,
            "ai_analyzer": ai_analyzer is not None
        },
        "metrics": {
            "agents_active": system_status["agents_active"],
            "warnings": system_status["warnings"],
            "errors": system_status["errors"]
        }
    }

@app.get("/status")
async def system_status_endpoint():
    """Status completo do sistema"""
    if not system_status["bootstrap_completed"]:
        raise HTTPException(status_code=503, detail="Sistema ainda inicializando")
    
    return {
        "system_name": "ALSHAM QUANTUM",
        "version": "2.0.0",
        "operational": system_status["system_healthy"],
        "bootstrap": {
            "completed": system_status["bootstrap_completed"],
            "agents_loaded": 30,  # Do bootstrap
            "components_active": system_status["agents_active"]
        },
        "health": {
            "overall": "healthy" if system_status["system_healthy"] else "degraded",
            "warnings": system_status["warnings"],
            "errors": system_status["errors"]
        }
    }

@app.post("/execute")
async def execute_task(task: dict):
    """Executar tarefa no sistema"""
    if not system_status["system_healthy"]:
        raise HTTPException(status_code=503, detail="Sistema não está saudável")
    
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator não disponível")
    
    try:
        result = await orchestrator.execute_task(task)
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Erro na execução de tarefa: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
async def list_agents():
    """Listar agentes disponíveis"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    return await orchestrator.list_agents()

# ===== INICIALIZAÇÃO PRINCIPAL =====

if __name__ == "__main__":
    # Configurações para diferentes ambientes
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    # Detectar ambiente
    is_railway = os.getenv("RAILWAY_ENVIRONMENT_NAME") is not None
    is_production = os.getenv("ENVIRONMENT") == "production"
    
    logger.info(f"🚀 Iniciando ALSHAM QUANTUM na porta {port}")
    if is_railway:
        logger.info("🚂 Ambiente: Railway")
    elif is_production:
        logger.info("🏭 Ambiente: Production")
    else:
        logger.info("🔧 Ambiente: Development")
    
    # Configurações do uvicorn
    uvicorn_config = {
        "app": "start:app",
        "host": host,
        "port": port,
        "log_level": "info",
        "access_log": True
    }
    
    # Configurações específicas para Railway
    if is_railway:
        uvicorn_config.update({
            "workers": 1,  # Railway funciona melhor com 1 worker
            "loop": "asyncio",
            "http": "httptools"
        })
    
    # Rodar servidor
    uvicorn.run(**uvicorn_config)
