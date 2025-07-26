#!/usr/bin/env python3
"""
SUNA-ALSHAM AutoML Enterprise System v2.0
Sistema Multi-Agente com Autoevolução
"""

import os
import sys
import asyncio
import logging
import traceback
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================
# CONFIGURAÇÃO DE LOGGING - PRIMEIRA COISA NO ARQUIVO
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('main_complete_system_v2')

# ============================================================
# CONFIGURAÇÃO DO SISTEMA
# ============================================================
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY:
    logger.info("✅ OPENAI_API_KEY configurada")
else:
    logger.warning("⚠️ OPENAI_API_KEY não encontrada")

# Adicionar paths para encontrar módulos em subdiretórios
sys.path.extend([
    'backend/agent/alsham',
    'suna_alsham/coordination',
    'suna_alsham/monitoring'
])

# ============================================================
# IMPORTS DOS MÓDULOS
# ============================================================
def safe_import(module_name):
    """Importa módulo com tratamento de erro"""
    try:
        module = __import__(module_name)
        logger.info(f"✅ Módulo {module_name} importado com sucesso")
        return module
    except Exception as e:
        logger.error(f"❌ Erro importando {module_name}: {str(e)}")
        return None

# Importar módulos do sistema
logger.info("📦 Importando módulos do sistema...")
multi_agent_network = safe_import('multi_agent_network')
specialized_agents = safe_import('specialized_agents')
ai_powered_agents = safe_import('ai_powered_agents')
core_agents_v3 = safe_import('core_agents_v3')
system_agents = safe_import('system_agents')
service_agents = safe_import('service_agents')
meta_cognitive_agents = safe_import('meta_cognitive_agents')
code_analyzer_agent = safe_import('code_analyzer_agent')
web_search_agent = safe_import('web_search_agent')
code_corrector_agent = safe_import('code_corrector_agent')
performance_monitor_agent = safe_import('performance_monitor_agent')

# Importar classes necessárias
if multi_agent_network:
    MultiAgentNetwork = multi_agent_network.MultiAgentNetwork
else:
    logger.error("❌ MultiAgentNetwork não disponível!")
    MultiAgentNetwork = None

# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================
network = None

# ============================================================
# CLASSE PRINCIPAL DO SISTEMA
# ============================================================
class SUNAAlshamSystemV2:
    """Classe wrapper para o sistema SUNA-ALSHAM v2.0"""
    
    def __init__(self):
        self.network = None
        self.agents = []
        self.logger = logging.getLogger('SUNAAlshamSystemV2')
        self.initialized = False
        
    async def initialize_complete_system(self):
        """Inicializa o sistema completo"""
        self.logger.info("🚀 Inicializando SUNA-ALSHAM v2.0...")
        
        try:
            # Verificar se MultiAgentNetwork está disponível
            if not MultiAgentNetwork:
                self.logger.error("❌ MultiAgentNetwork não disponível")
                return False
            
            # Inicializar rede
            self.network = MultiAgentNetwork()
            self.logger.info("✅ Rede Multi-Agente inicializada")
            
            # Criar agentes
            global network
            network = self.network
            self.agents = await self.criar_todos_agentes()
            
            self.logger.info(f"📊 {len(self.agents)} agentes criados")
            
            # Iniciar loops assíncronos
            asyncio.create_task(self.run_system_loops())
            
            self.initialized = True
            self.logger.info("✅ Sistema inicializado com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro na inicialização: {str(e)}")
            self.logger.error(traceback.format_exc())
            return False
    
    async def criar_todos_agentes(self):
        """Cria todos os 24 agentes do sistema"""
        self.logger.info("🎯 Criando agentes...")
        todos_agentes = []
        
        # Lista de módulos e quantidade esperada
        modulos_agentes = [
            (specialized_agents, 'specialized_agents', 5),
            (ai_powered_agents, 'ai_powered_agents', 3),
            (core_agents_v3, 'core_agents_v3', 5),
            (system_agents, 'system_agents', 3),
            (service_agents, 'service_agents', 2),
            (meta_cognitive_agents, 'meta_cognitive_agents', 2),
            (code_analyzer_agent, 'code_analyzer_agent', 1),
            (web_search_agent, 'web_search_agent', 1),
            (code_corrector_agent, 'code_corrector_agent', 1),
            (performance_monitor_agent, 'performance_monitor_agent', 1)
        ]
        
        for modulo, nome, qtd_esperada in modulos_agentes:
            if modulo and hasattr(modulo, 'create_agents'):
                try:
                    agentes = await modulo.create_agents(self.network)
                    if agentes:
                        todos_agentes.extend(agentes)
                        self.logger.info(f"✅ {len(agentes)}/{qtd_esperada} agentes de {nome}")
                except Exception as e:
                    self.logger.error(f"❌ Erro em {nome}: {str(e)}")
        
        return todos_agentes
    
    async def run_system_loops(self):
        """Executa os loops do sistema"""
        tasks = []
        
        if self.network:
            if hasattr(self.network, 'heartbeat_loop'):
                tasks.append(self.network.heartbeat_loop())
            if hasattr(self.network, 'process_messages'):
                tasks.append(self.network.process_messages())
        
        tasks.append(self.keep_alive())
        
        await asyncio.gather(*tasks)
    
    async def keep_alive(self):
        """Mantém o sistema ativo"""
        while True:
            await asyncio.sleep(60)
            self.logger.debug(f"💓 Sistema ativo - {len(self.agents)} agentes")
    
    def get_status(self):
        """Retorna status do sistema"""
        return {
            "initialized": self.initialized,
            "agents_count": len(self.agents),
            "network_active": self.network is not None
        }

# ============================================================
# FUNÇÕES DE SUPORTE
# ============================================================
def print_header():
    """Imprime cabeçalho do sistema"""
    header = """
    ============================================================
    🚀 INICIANDO SUNA-ALSHAM SISTEMA v2.0
    ⏰ Inicialização: {}
    ============================================================
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info(header)

# ============================================================
# EXECUÇÃO DIRETA (se não for importado)
# ============================================================
async def main():
    """Função principal para execução direta"""
    print_header()
    
    system = SUNAAlshamSystemV2()
    success = await system.initialize_complete_system()
    
    if success:
        logger.info("🚀 Sistema rodando...")
        # Manter rodando
        await system.keep_alive()
    else:
        logger.error("❌ Falha na inicialização")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
