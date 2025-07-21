"""
SUNA-ALSHAM Enterprise Startup Script
Script de inicialização para Railway com detecção automática de porta
"""

import os
import sys
import asyncio
import uvicorn
from pathlib import Path

# Adicionar diretório atual ao path
sys.path.append(str(Path(__file__).parent))

def get_port():
    """Detecta a porta do Railway ou usa padrão"""
    return int(os.environ.get("PORT", 8080))

def get_host():
    """Detecta o host apropriado"""
    return "0.0.0.0"

async def startup_sequence():
    """Sequência de inicialização dos serviços"""
    print("🚀 Iniciando SUNA-ALSHAM Enterprise...")
    
    # Verificar variáveis de ambiente essenciais
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key:
        print("⚠️ OPENAI_API_KEY não configurada - usando modo demo")
    else:
        print("✅ OPENAI_API_KEY configurada")
    
    # Verificar Redis
    redis_url = os.environ.get("REDIS_URL")
    if redis_url:
        print(f"✅ Redis configurado: {redis_url[:20]}...")
    else:
        print("⚠️ Redis não configurado - usando cache em memória")
    
    print("✅ Sequência de inicialização concluída")

def main():
    """Função principal de inicialização"""
    
    # Executar sequência de startup
    asyncio.run(startup_sequence())
    
    # Configurações do servidor
    port = get_port()
    host = get_host()
    
    print(f"🌐 Iniciando servidor em {host}:{port}")
    
    # Tentar importar o orquestrador principal
    try:
        from main_orchestrator import app
        print("✅ Orquestrador principal carregado")
        
        # Configurações de produção
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True,
            use_colors=True,
            loop="asyncio"
        )
        
    except ImportError as e:
        print(f"⚠️ Orquestrador não encontrado, usando guard_service: {e}")
        
        # Fallback para guard_service atual
        try:
            from guard_service import app
            print("✅ Guard Service carregado como fallback")
            
            uvicorn.run(
                app,
                host=host,
                port=port,
                log_level="info",
                access_log=True,
                use_colors=True,
                loop="asyncio"
            )
            
        except ImportError as e2:
            print(f"❌ Erro crítico: Nenhum serviço encontrado: {e2}")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

