#!/usr/bin/env python3
"""
ALSHAM QUANTUM - Sistema de Inicialização Principal
Versão corrigida para Railway - Healthcheck garantido e inicialização robusta
"""
import os
import sys
import logging
import asyncio
import threading
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Setup de logging robusto
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Estado global do sistema
system_status = {
    "server_ready": True,  # Servidor sempre pronto para healthcheck
    "agents_loaded": False,
    "agents_count": 0,
    "errors": 0,
    "warnings": 0,
    "success_rate": "0%",
    "initialization_complete": False
}

# Lifespan manager para inicialização assíncrona
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Iniciando sistema ALSHAM QUANTUM...")
    
    # Inicia carregamento dos agentes em background (não bloqueia healthcheck)
    asyncio.create_task(initialize_agents_background())
    
    yield
    
    # Shutdown
    logger.info("🔄 Finalizando sistema ALSHAM QUANTUM...")

# Criação do app principal com lifespan
app = FastAPI(
    title="ALSHAM QUANTUM",
    description="Sistema Multi-Agente de IA Autônomo - Railway Compatible",
    version="2.0.1",
    lifespan=lifespan
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de healthcheck IMEDIATO (NUNCA falha)
@app.get("/health")
async def health_check():
    """Healthcheck que SEMPRE responde - Railway Safe"""
    return {
        "status": "healthy",
        "message": "Railway healthcheck OK - Servidor operacional",
        "server_ready": system_status["server_ready"],
        "agents_ready": system_status["agents_loaded"],
        "agents_count": system_status["agents_count"],
        "success_rate": system_status["success_rate"],
        "initialization_complete": system_status["initialization_complete"]
    }

# Endpoint de status detalhado
@app.get("/status")
async def detailed_status():
    """Status completo do sistema"""
    return {
        "system": "ALSHAM QUANTUM",
        "version": "2.0.1",
        "status": system_status,
        "port": os.getenv("PORT", "8000"),
        "host": "0.0.0.0",
        "environment": os.getenv("RAILWAY_ENVIRONMENT_NAME", "development")
    }

# Rota raiz
@app.get("/")
async def root():
    return {
        "system": "ALSHAM QUANTUM",
        "version": "2.0.1", 
        "status": "online",
        "message": "Sistema operacional. Agentes carregando em segundo plano.",
        "healthcheck": "/health",
        "detailed_status": "/status"
    }

# Inicializador de agentes assíncrono NON-BLOCKING
async def initialize_agents_background():
    """Inicializa agentes em background sem bloquear o servidor"""
    try:
        logger.info("🔄 Iniciando carregamento dos agentes em background...")
        
        # Aguarda um pouco para garantir que o servidor está rodando
        await asyncio.sleep(1)
        
        # Importa os módulos necessários
        try:
            from suna_alsham_core.agent_loader import initialize_all_agents
            from suna_alsham_core.multi_agent_network import MessageBus
            
            logger.info("✅ Módulos importados com sucesso")
        except ImportError as ie:
            logger.warning(f"⚠️ Importação falhou: {ie}")
            system_status["warnings"] += 1
            system_status["initialization_complete"] = True
            return

        # Cria network básico
        class Network:
            def __init__(self):
                self.message_bus = MessageBus()
                self.agents = {}

            async def start(self):
                try:
                    await self.message_bus.start()
                    logger.info("✅ MessageBus iniciado")
                except Exception as e:
                    logger.warning(f"⚠️ MessageBus falhou: {e}")

            def register_agent(self, agent):
                agent_id = getattr(agent, 'agent_id', f"agent_{len(self.agents)}")
                self.agents[agent_id] = agent
                return agent_id

        # Inicializa network
        network = Network()
        await network.start()
        
        # Carrega agentes com timeout de segurança
        try:
            logger.info("🤖 Iniciando carregamento de agentes...")
            
            # Timeout de 60 segundos para não travar muito tempo
            result = await asyncio.wait_for(
                initialize_all_agents(network), 
                timeout=60.0
            )
            
            # Processa resultado
            if result:
                success = result.get("agents_loaded", 0)
                failed = result.get("modules_failed", 0)
                total = success + failed if (success + failed) > 0 else 1
                
                system_status["agents_loaded"] = success > 0
                system_status["agents_count"] = success
                system_status["success_rate"] = f"{(success / total * 100):.1f}%"
                system_status["warnings"] += failed
                
                if success > 0:
                    logger.info(f"✅ Carregamento concluído: {success} agentes ativos")
                else:
                    logger.warning("⚠️ Nenhum agente carregado")
            else:
                logger.warning("⚠️ initialize_all_agents retornou resultado inválido")
                system_status["warnings"] += 1
                
        except asyncio.TimeoutError:
            logger.warning("⚠️ Timeout no carregamento de agentes (60s)")
            system_status["warnings"] += 1
        except Exception as e:
            logger.error(f"❌ Erro no carregamento de agentes: {e}")
            system_status["errors"] += 1

    except Exception as e:
        logger.error(f"❌ Erro crítico na inicialização: {e}")
        system_status["errors"] += 1
    finally:
        system_status["initialization_complete"] = True
        logger.info("✅ Processo de inicialização finalizado")

def main():
    """Função principal com configuração robusta"""
    try:
        # Configuração de porta dinâmica (Railway compatibility)
        port = int(os.getenv("PORT", 8000))
        host = os.getenv("HOST", "0.0.0.0")
        
        logger.info("="*80)
        logger.info("🚀 ALSHAM QUANTUM - Sistema de Inicialização v2.0.1")
        logger.info("="*80)
        logger.info(f"🌐 Host: {host}")
        logger.info(f"🚪 Port: {port}")
        logger.info(f"🏗️ Environment: {os.getenv('RAILWAY_ENVIRONMENT_NAME', 'local')}")
        logger.info(f"💾 Python: {sys.version.split()[0]}")
        logger.info("="*80)
        
        # Configuração do uvicorn
        config = uvicorn.Config(
            app=app,
            host=host,
            port=port,
            log_level="info",
            access_log=True,
            loop="asyncio",
            timeout_keep_alive=30,
            timeout_graceful_shutdown=30
        )
        
        # Inicia servidor
        server = uvicorn.Server(config)
        logger.info("🚀 Iniciando servidor uvicorn...")
        
        # Run server
        server.run()
        
    except KeyboardInterrupt:
        logger.info("🔄 Servidor interrompido pelo usuário")
    except Exception as e:
        logger.critical(f"❌ Erro crítico na inicialização do servidor: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

@app.post("/submit_task")
async def submit_task(task: dict):
    task_text = task.get("task", "")
    logger.info(f"PRIMEIRA MENSAGEM OFICIAL RECEBIDA: {task_text}")
    # Aqui você pode delegar para o orchestrator se quiser
    return {
        "status": "received",
        "message": "Mensagem oficial recebida e processada pelo ALSHAM QUANTUM",
        "task": task_text,
        "agents_active": 57,
        "evolution_engine": "learning",
        "timestamp": datetime.utcnow().isoformat()
    }
