# Adicione estas funções ao main_complete_system_v2.py
# Substitua as funções existentes ou adicione se não existirem

import traceback  # Certifique-se que está importado no topo do arquivo

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
            active_agents = await network.get_active_agents() if network else []
            logger.info(f"📊 Status: {len(active_agents)} agentes ativos")
            
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
        return
    
    try:
        # Inicializar rede
        global network
        network = MultiAgentNetwork()
        logger.info("✅ Rede Multi-Agente inicializada")
        
        # CRIAR TODOS OS AGENTES
        agentes = await criar_todos_agentes()
        
        if len(agentes) < 24:
            logger.warning(f"⚠️ Sistema iniciando com capacidade reduzida: {len(agentes)}/24 agentes")
        
        logger.info("🚀 Sistema SUNA-ALSHAM v2.0 operacional!")
        
        # IMPORTANTE: Manter sistema rodando com múltiplos loops
        await asyncio.gather(
            network.heartbeat_loop(),
            network.process_messages(),
            coordinator_loop(),
            keep_alive()  # Essencial para Railway
        )
        
    except Exception as e:
        logger.error(f"❌ Erro fatal: {str(e)}")
        logger.error(traceback.format_exc())
        raise  # Re-lançar para debugging

# IMPORTANTE: Bloco principal no final do arquivo
if __name__ == "__main__":
    try:
        logger.info("🚀 Iniciando SUNA-ALSHAM v2.0...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Sistema interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro crítico na inicialização: {str(e)}")
        logger.error(traceback.format_exc())
        # Manter o processo vivo por 5 segundos para logs
        import time
        time.sleep(5)
