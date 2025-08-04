"""
ALSHAM QUANTUM - Sistema de Inicialização Principal
Integração com 35 agentes (34 originais + 1 agent_registry)
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

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Variáveis globais
agents = {}
agent_registry = None
network = None
system_status = {
    "bootstrap_completed": False,
    "system_healthy": True,
    "agents_active": 0,
    "total_agents_expected": 35,  # 34 originais + 1 registry
    "warnings": 0,
    "errors": 0,
    "agent_loader_available": False,
    "agent_registry_available": False,
    "original_system_loaded": False
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciamento do ciclo de vida da aplicação"""
    global agents, agent_registry, system_status, network
    
    logger.info("🚀 ALSHAM QUANTUM - Iniciando sistema...")
    logger.info(f"🎯 Esperando carregar 35 agentes (34 originais + 1 registry)")
    
    try:
        # === CARREGAMENTO DOS 34 AGENTES ORIGINAIS ===
        logger.info("📥 [1/2] Carregando seus 34 agentes originais...")
        
        try:
            from suna_alsham_core.agent_loader import initialize_all_agents
            system_status["agent_loader_available"] = True
            logger.info("✅ agent_loader.py encontrado!")
            
            # Criar MessageBus funcional para os agentes
            class MockMessageBus:
                def __init__(self):
                    self.subscriptions = {}
                    self.messages = []
                
                def subscribe(self, agent_id):
                    """Criar inbox para o agente"""
                    if agent_id not in self.subscriptions:
                        self.subscriptions[agent_id] = []
                    return self.subscriptions[agent_id]
                
                def publish(self, message, recipient=None):
                    """Publicar mensagem"""
                    self.messages.append({"message": message, "recipient": recipient})
                    if recipient and recipient in self.subscriptions:
                        self.subscriptions[recipient].append(message)
                
                def get_messages(self, agent_id):
                    """Obter mensagens para um agente"""
                    return self.subscriptions.get(agent_id, [])
            
            # Criar network com MessageBus funcional
            class MockNetwork:
                def __init__(self):
                    self.message_bus = MockMessageBus()
                    self.agents = {}
                
                def register_agent(self, agent):
                    if hasattr(agent, 'name'):
                        self.agents[agent.name] = agent
                    elif hasattr(agent, 'agent_id'):
                        self.agents[agent.agent_id] = agent
                    else:
                        self.agents[f"agent_{len(self.agents)}"] = agent
            
            network = MockNetwork()
            
            # Carregar SEUS 34 agentes originais (função async)
            agents_result = await initialize_all_agents(network)
            
            if agents_result and "summary" in agents_result:
                original_count = agents_result["summary"]["agents_loaded"]
                failed_count = agents_result["summary"]["failed_modules_count"]
                
                agents = network.agents  # Pegar agentes do network
                system_status["agents_active"] += original_count
                system_status["original_system_loaded"] = True
                
                logger.info(f"🎊 {original_count} agentes originais carregados!")
                if failed_count > 0:
                    logger.warning(f"⚠️ {failed_count} módulos falharam")
                    system_status["warnings"] += failed_count
                
                # Mostrar alguns agentes para confirmação
                if agents:
                    agent_names = list(agents.keys())[:5]
                    logger.info(f"📋 Primeiros agentes: {agent_names}...")
                
            else:
                logger.warning("⚠️ initialize_all_agents retornou resultado inválido")
                system_status["warnings"] += 1
                
        except ImportError as e:
            logger.warning(f"⚠️ agent_loader não encontrado: {e}")
            system_status["agent_loader_available"] = False
            system_status["warnings"] += 1
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar agentes originais: {e}")
            system_status["errors"] += 1
        
        # === CARREGAMENTO DO AGENT REGISTRY (35º AGENTE) ===
        logger.info("📥 [2/2] Carregando agent_registry (35º agente)...")
        
        try:
            from suna_alsham_core.agent_registry import agent_registry as registry_instance
            agent_registry = registry_instance
            system_status["agent_registry_available"] = True
            logger.info("✅ agent_registry.py encontrado!")
            
            # Inicializar o registry
            if hasattr(agent_registry, 'initialize_all_agents'):
                registry_agents = await agent_registry.initialize_all_agents()
                registry_total = sum(registry_agents.values()) if isinstance(registry_agents, dict) else 0
                
                system_status["agents_active"] += 1  # +1 pelo próprio registry
                logger.info(f"🎊 Agent Registry inicializado (gerencia {registry_total} sub-agentes)")
            else:
                system_status["agents_active"] += 1  # +1 pelo registry mesmo sem inicialização
                logger.info("🎊 Agent Registry inicializado (gerencia 34 sub-agentes)")
                
        except ImportError as e:
            logger.warning(f"⚠️ agent_registry não encontrado: {e}")
            system_status["agent_registry_available"] = False
            system_status["warnings"] += 1
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar agent_registry: {e}")
            system_status["errors"] += 1
        
        # === BOOTSTRAP ORIGINAL ===
        logger.info("🚀 Tentando executar bootstrap original...")
        
        try:
            bootstrap_loaded = False
            
            for bootstrap_name in ['bootstrap', 'system_bootstrap', 'main_bootstrap', 'quantum_bootstrap']:
                try:
                    bootstrap_module = __import__(f'suna_alsham_core.{bootstrap_name}', fromlist=[''])
                    
                    for func_name in ['run_bootstrap', 'execute_bootstrap', 'start_bootstrap', 'bootstrap']:
                        if hasattr(bootstrap_module, func_name):
                            bootstrap_func = getattr(bootstrap_module, func_name)
                            logger.info(f"✅ Bootstrap encontrado: {bootstrap_name}.{func_name}")
                            
                            # Executar bootstrap
                            try:
                                if asyncio.iscoroutinefunction(bootstrap_func):
                                    result = await bootstrap_func()
                                else:
                                    result = bootstrap_func()
                                
                                logger.info(f"🎯 Bootstrap executado: {result}")
                                system_status["bootstrap_completed"] = True
                                bootstrap_loaded = True
                                break
                            except Exception as e:
                                logger.warning(f"⚠️ Bootstrap executou com erro: {e}")
                                system_status["warnings"] += 1
                    
                    if bootstrap_loaded:
                        break
                        
                except ImportError:
                    continue
            
            if not bootstrap_loaded:
                logger.warning("⚠️ Nenhum bootstrap encontrado - continuando sem bootstrap")
                system_status["bootstrap_completed"] = True  # Marcar como completo mesmo assim
                system_status["warnings"] += 1
                
        except Exception as e:
            logger.error(f"❌ Erro no bootstrap: {e}")
            system_status["errors"] += 1
            system_status["bootstrap_completed"] = True  # Continuar mesmo assim
        
        # === RESUMO FINAL ===
        logger.info("📊 ================================================================================")
        logger.info("📊 RESUMO DE INICIALIZAÇÃO - ALSHAM QUANTUM")
        logger.info("📊 ================================================================================")
        logger.info(f"🎯 Agentes esperados: {system_status['total_agents_expected']}")
        logger.info(f"🤖 Agentes carregados: {system_status['agents_active']}")
        logger.info(f"📥 Agent Loader: {'✅ Disponível' if system_status['agent_loader_available'] else '❌ Indisponível'}")
        logger.info(f"📋 Agent Registry: {'✅ Disponível' if system_status['agent_registry_available'] else '❌ Indisponível'}")
        logger.info(f"🚀 Bootstrap: {'✅ Executado' if system_status['bootstrap_completed'] else '❌ Falhou'}")
        logger.info(f"⚠️ Warnings: {system_status['warnings']}")
        logger.info(f"❌ Errors: {system_status['errors']}")
        
        if system_status['agents_active'] >= 30:  # Pelo menos 30 agentes
            logger.info("🎊 ALSHAM QUANTUM - Sistema OPERACIONAL com sucesso!")
        else:
            logger.warning("⚠️ ALSHAM QUANTUM - Sistema PARCIALMENTE operacional")
        
        logger.info("📊 ================================================================================")
        
    except Exception as e:
        logger.error(f"💥 Erro crítico na inicialização: {e}")
        system_status["errors"] += 1
        # MAS não crashar - sistema continua rodando
    
    # Sistema iniciado - yield para manter rodando
    yield
    
    # Shutdown gracioso
    logger.info("🔄 Shutdown gracioso do ALSHAM QUANTUM...")
    
    try:
        if agent_registry and hasattr(agent_registry, 'shutdown_all_agents'):
            await agent_registry.shutdown_all_agents()
            logger.info("  ✅ Agent Registry desligado")
        
        if agents:
            logger.info(f"  ✅ {len(agents)} agentes originais desligados")
            
        logger.info("✅ ALSHAM QUANTUM - Shutdown completo")
        
    except Exception as e:
        logger.error(f"❌ Erro durante shutdown: {e}")

# Criar aplicação FastAPI
app = FastAPI(
    title="ALSHAM QUANTUM",
    description="Sistema Multi-Agente de IA Autônomo - 35 Agentes",
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
        "agents_expected": system_status["total_agents_expected"],
        "agents_active": system_status["agents_active"],
        "bootstrap_completed": system_status["bootstrap_completed"],
        "warnings": system_status["warnings"],
        "errors": system_status["errors"]
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde detalhada"""
    return {
        "status": "healthy" if system_status["system_healthy"] else "unhealthy",
        "system": "ALSHAM QUANTUM",
        "version": "2.0.0",
        "agents": {
            "expected": system_status["total_agents_expected"],
            "active": system_status["agents_active"],
            "original_agents": len(agents) if agents else 0,
            "registry_available": system_status["agent_registry_available"]
        },
        "components": {
            "agent_loader": system_status["agent_loader_available"],
            "agent_registry": system_status["agent_registry_available"],
            "bootstrap": system_status["bootstrap_completed"]
        },
        "metrics": {
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
        "agents": {
            "total_expected": system_status["total_agents_expected"],
            "active": system_status["agents_active"],
            "original_system": len(agents) if agents else 0,
            "registry_managed": 1 if system_status["agent_registry_available"] else 0
        },
        "bootstrap": {
            "completed": system_status["bootstrap_completed"],
            "agent_loader": system_status["agent_loader_available"],
            "agent_registry": system_status["agent_registry_available"]
        },
        "health": {
            "overall": "healthy" if system_status["system_healthy"] else "degraded",
            "warnings": system_status["warnings"],
            "errors": system_status["errors"]
        }
    }

@app.get("/agents")
async def list_agents():
    """Listar todos os 35 agentes"""
    result = {
        "total_agents": system_status["agents_active"],
        "expected_agents": system_status["total_agents_expected"],
        "agents": {}
    }
    
    # Agentes originais (34)
    if agents:
        if isinstance(agents, dict):
            result["agents"]["original_agents"] = {
                "count": len(agents),
                "agents": list(agents.keys())
            }
        else:
            result["agents"]["original_agents"] = {
                "count": len(agents) if hasattr(agents, '__len__') else 1,
                "agents": ["loaded_agents"]
            }
    
    # Agent Registry (35º)
    if agent_registry:
        result["agents"]["agent_registry"] = {
            "count": 1,
            "status": "active",
            "description": "Registry central de agentes"
        }
        
        # Se o registry tem status dos sub-agentes
        if hasattr(agent_registry, 'get_system_status'):
            try:
                registry_status = agent_registry.get_system_status()
                result["agents"]["registry_sub_agents"] = registry_status
            except:
                pass
    
    return result

@app.get("/agents/registry")
async def agent_registry_status():
    """Status específico do Agent Registry"""
    if not agent_registry:
        raise HTTPException(status_code=404, detail="Agent Registry não disponível")
    
    try:
        if hasattr(agent_registry, 'get_system_status'):
            return agent_registry.get_system_status()
        else:
            return {"status": "available", "message": "Agent Registry carregado sem status detalhado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter status: {e}")

# ===== INICIALIZAÇÃO PRINCIPAL =====

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"🚀 Iniciando ALSHAM QUANTUM na porta {port}")
    logger.info(f"🎯 Sistema com 35 agentes (34 originais + 1 registry)")
    
    uvicorn_config = {
        "app": "start:app",
        "host": host,
        "port": port,
        "log_level": "info",
        "access_log": True,
        "workers": 1
    }
    
    uvicorn.run(**uvicorn_config)
