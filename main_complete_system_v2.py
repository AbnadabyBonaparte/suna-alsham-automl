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
        logger.error(f"  Detalhes: {traceback.format_exc()}")
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
# FUNÇÕES AUXILIARES
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

def verificar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    logger.info("🔍 Verificando arquivos do sistema...")
    
    arquivos_necessarios = [
        'multi_agent_network.py',
        'specialized_agents.py',
        'ai_powered_agents.py',
        'core_agents_v3.py',
        'system_agents.py',
        'service_agents.py',
        'meta_cognitive_agents.py'
    ]
    
    todos_presentes = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            logger.info(f"✅ {arquivo} encontrado")
        else:
            logger.error(f"❌ {arquivo} NÃO encontrado")
            todos_presentes = False
    
    return todos_presentes

# ============================================================
# FUNÇÕES PRINCIPAIS DO SISTEMA
# ============================================================
async def criar_todos_agentes():
    """Cria todos os 24 agentes do sistema com logging detalhado"""
    logger.info("🎯 INICIANDO CRIAÇÃO DE 24 AGENTES...")
    
    todos_agentes = []
    total_esperado = 24
    
    # Mapeamento de módulos e quantidade esperada
    modulos_agentes = [
        ('specialized_agents', 5),
        ('ai_powered_agents', 3),
        ('core_agents_v3', 5),
        ('system_agents', 3),
        ('service_agents', 2),
        ('meta_cognitive_agents', 2),
        ('code_analyzer_agent', 1),
        ('web_search_agent', 1),
        ('code_corrector_agent', 1),
        ('performance_monitor_agent', 1)
    ]
    
    # Criar agentes de cada módulo
    for modulo_nome, qtd_esperada in modulos_agentes:
        try:
            logger.info(f"\n🔧 Criando agentes {modulo_nome}...")
            
            # Verificar se módulo existe
            modulo = globals().get(modulo_nome)
            if not modulo:
                logger.error(f"❌ Módulo {modulo_nome} não encontrado!")
                continue
            
            # Criar agentes
            if hasattr(modulo, 'create_agents'):
                agentes = await modulo.create_agents(network)
                if agentes:
                    todos_agentes.extend(agentes)
                    logger.info(f"✅ {len(agentes)}/{qtd_esperada} agentes criados de {modulo_nome}")
                    
                    # Listar agentes criados
                    for agent in agentes:
                        logger.info(f"  └─ {agent.agent_id} inicializado")
                else:
                    logger.warning(f"⚠️ Nenhum agente criado de {modulo_nome}")
            else:
                logger.error(f"❌ {modulo_nome} não tem create_agents()")
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar agentes de {modulo_nome}: {str(e)}")
            logger.error(f"Detalhes: {traceback.format_exc()}")
    
    # Relatório final
    logger.info("\n" + "="*60)
    logger.info(f"📊 TOTAL DE AGENTES CRIADOS: {len(todos_agentes)}/{total_esperado}")
    
    if len(todos_agentes) < total_esperado:
        logger.warning(f"⚠️ ATENÇÃO: Faltam {total_esperado - len(todos_agentes)} agentes!")
        logger.info("Verifique os logs acima para identificar problemas")
    else:
        logger.info("🎉 TODOS OS AGENTES FORAM CRIADOS COM SUCESSO!")
    
    return todos_agentes

async def coordinator_loop():
    """Loop do coordenador do sistema"""
    logger.info("🎯 Coordinator loop iniciado")
    while True:
        try:
            # Verificar status dos agentes periodicamente
            if network and hasattr(network, 'get_active_agents'):
                active_agents = await network.get_active_agents()
                logger.info(f"📊 Status: {len(active_agents)} agentes ativos")
            else:
                logger.debug("📊 Verificação de status...")
            
            # Aguardar 30 segundos antes da próxima verificação
            await asyncio.sleep(30)
            
        except Exception as e:
            logger.error(f"Erro no coordinator: {str(e)}")
            await asyncio.sleep(5)

async def keep_alive():
    """Mantém o sistema ativo para evitar que o container pare"""
    logger.info("💓 Sistema keep-alive iniciado")
    while True:
        await asyncio.sleep(60)  # Heartbeat a cada 60 segundos
        logger.debug("💓 Sistema ativo e operacional...")

async def main():
    """Sistema principal SUNA-ALSHAM v2.0"""
    print_header()
    
    # Verificar arquivos primeiro
    arquivos_ok = verificar_arquivos()
    if not arquivos_ok:
        logger.error("❌ Verificação de arquivos falhou!")
        logger.info("⚠️ Continuando com módulos disponíveis...")
    
    try:
        # Inicializar rede se disponível
        global network
        if MultiAgentNetwork:
            network = MultiAgentNetwork()
            logger.info("✅ Rede Multi-Agente inicializada")
        else:
            logger.error("❌ MultiAgentNetwork não disponível - sistema limitado")
            return
        
        # CRIAR TODOS OS AGENTES
        agentes = await criar_todos_agentes()
        
        if len(agentes) < 24:
            logger.warning(f"⚠️ Sistema iniciando com capacidade reduzida: {len(agentes)}/24 agentes")
        
        logger.info("🚀 Sistema SUNA-ALSHAM v2.0 operacional!")
        
        # Preparar tarefas assíncronas
        tasks = [keep_alive()]  # Keep-alive é essencial
        
        if network and hasattr(network, 'heartbeat_loop'):
            tasks.append(network.heartbeat_loop())
        
        if network and hasattr(network, 'process_messages'):
            tasks.append(network.process_messages())
        
        tasks.append(coordinator_loop())
        
        # Executar todas as tarefas
        await asyncio.gather(*tasks)
        
    except Exception as e:
        logger.error(f"❌ Erro fatal: {str(e)}")
        logger.error(traceback.format_exc())
        raise

# ============================================================
# PONTO DE ENTRADA PRINCIPAL
# ============================================================
if __name__ == "__main__":
    try:
        logger.info("🚀 Iniciando SUNA-ALSHAM v2.0...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Sistema interrompido pelo usuário")
    except Exception as e:
        # Usar print se logger falhar
        print(f"❌ Erro crítico na inicialização: {str(e)}")
        print(traceback.format_exc())
        # Manter o processo vivo por 5 segundos para logs
        import time
        time.sleep(5)
