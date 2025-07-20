"""
SUNA-ALSHAM Bootstrap Script
Sistema Auto-Evolutivo de IA com AutoML Real
Versão: 2.1.0 - Enterprise Edition
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('suna_alsham.log', mode='a')
    ]
)

logger = logging.getLogger("SUNA-ALSHAM-BOOTSTRAP")

def setup_environment():
    """Configura o ambiente do sistema."""
    logger.info("🔧 Configurando ambiente SUNA-ALSHAM...")
    
    # Adicionar diretório raiz ao PYTHONPATH
    project_root = Path(__file__).parent.absolute()
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Verificar variáveis de ambiente essenciais
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"⚠️ Variáveis de ambiente não configuradas: {missing_vars}")
        logger.info("💡 Sistema funcionará em modo de desenvolvimento")
    else:
        logger.info("✅ Variáveis de ambiente configuradas")
    
    return True

def import_system_components():
    """Importa os componentes do sistema."""
    logger.info("📦 Importando componentes do sistema...")
    
    try:
        # Tentar importar componentes principais
        from backend.agent.alsham.core_agent import CoreAgent
        from backend.agent.alsham.config import CoreAgentConfig
        
        logger.info("✅ Componentes principais importados com sucesso")
        return CoreAgent, CoreAgentConfig
        
    except ImportError as e:
        logger.error(f"❌ Erro ao importar componentes: {e}")
        logger.info("🔄 Criando componentes mock para desenvolvimento...")
        
        # Componentes mock para desenvolvimento
        class MockCoreAgent:
            def __init__(self, config=None):
                self.agent_id = "mock-core-agent"
                self.name = "CORE_AUTOML_MOCK"
                self.enabled = True
                logger.info("🤖 Mock Core Agent inicializado")
            
            def run_evolution_cycle(self):
                logger.info("🔄 Executando ciclo de evolução mock...")
                time.sleep(2)  # Simular processamento
                return {
                    "success": True,
                    "message": "Mock evolution cycle completed",
                    "improvement_percentage": 12.5,
                    "method": "mock_automl"
                }
        
        class MockConfig:
            def __init__(self):
                self.enabled = True
                self.min_improvement_percentage = 5.0
        
        return MockCoreAgent, MockConfig

def initialize_core_agent():
    """Inicializa o Core Agent AutoML."""
    logger.info("🤖 Inicializando Core Agent AutoML...")
    
    try:
        CoreAgent, CoreAgentConfig = import_system_components()
        
        # Configurar Core Agent
        config = CoreAgentConfig()
        core_agent = CoreAgent(config)
        
        logger.info(f"✅ Core Agent inicializado - ID: {core_agent.agent_id}")
        return core_agent
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar Core Agent: {e}")
        return None

def run_evolution_cycle(core_agent):
    """Executa um ciclo de evolução."""
    if not core_agent:
        logger.error("❌ Core Agent não disponível")
        return False
    
    try:
        logger.info("🔄 Iniciando ciclo de evolução AutoML...")
        result = core_agent.run_evolution_cycle()
        
        if result.get('success'):
            improvement = result.get('improvement_percentage', 0)
            method = result.get('method', 'unknown')
            
            logger.info(f"✅ Ciclo concluído com sucesso!")
            logger.info(f"📈 Melhoria: {improvement:.2f}%")
            logger.info(f"🔬 Método: {method}")
            return True
        else:
            logger.error(f"❌ Ciclo falhou: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro durante ciclo de evolução: {e}")
        return False

def main():
    """Função principal do sistema."""
    logger.info("🚀 SUNA-ALSHAM Sistema Auto-Evolutivo Iniciando...")
    logger.info("=" * 60)
    
    # Configurar ambiente
    if not setup_environment():
        logger.error("❌ Falha na configuração do ambiente")
        sys.exit(1)
    
    # Inicializar Core Agent
    core_agent = initialize_core_agent()
    if not core_agent:
        logger.error("❌ Falha na inicialização do Core Agent")
        sys.exit(1)
    
    # Configurações do sistema
    auto_start = os.getenv('SUNA_ALSHAM_AUTO_START', 'true').lower() == 'true'
    evolution_interval = int(os.getenv('SUNA_ALSHAM_EVOLUTION_INTERVAL', '60'))
    
    logger.info(f"⚙️ Auto-start: {auto_start}")
    logger.info(f"⏱️ Intervalo de evolução: {evolution_interval} minutos")
    
    if auto_start:
        logger.info("🔄 Modo automático ativado - Executando ciclos de evolução...")
        
        cycle_count = 0
        while True:
            try:
                cycle_count += 1
                logger.info(f"🔄 Ciclo #{cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Executar ciclo de evolução
                success = run_evolution_cycle(core_agent)
                
                if success:
                    logger.info(f"✅ Ciclo #{cycle_count} concluído com sucesso")
                else:
                    logger.warning(f"⚠️ Ciclo #{cycle_count} teve problemas")
                
                # Aguardar próximo ciclo
                logger.info(f"⏳ Aguardando {evolution_interval} minutos para próximo ciclo...")
                time.sleep(evolution_interval * 60)
                
            except KeyboardInterrupt:
                logger.info("🛑 Sistema interrompido pelo usuário")
                break
            except Exception as e:
                logger.error(f"❌ Erro inesperado: {e}")
                logger.info("🔄 Tentando novamente em 5 minutos...")
                time.sleep(300)  # 5 minutos
    
    else:
        logger.info("🔄 Modo manual - Executando um ciclo único...")
        success = run_evolution_cycle(core_agent)
        
        if success:
            logger.info("✅ Ciclo único concluído com sucesso")
        else:
            logger.error("❌ Ciclo único falhou")
    
    logger.info("🏁 SUNA-ALSHAM Sistema finalizado")

if __name__ == "__main__":
    main()
