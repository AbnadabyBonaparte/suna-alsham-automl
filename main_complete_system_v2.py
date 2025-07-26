# Adicione esta função no main_complete_system_v2.py, logo após a função verificar_arquivos():

def verificar_estrutura_completa():
    """Verifica e mostra toda a estrutura de arquivos do projeto"""
    logger.info("\n🔍 VERIFICANDO ESTRUTURA COMPLETA DO PROJETO")
    logger.info("=" * 60)
    
    # Arquivos de agentes esperados
    agentes_esperados = {
        'multi_agent_network.py': 'Rede de comunicação',
        'specialized_agents.py': '5 agentes especializados',
        'ai_powered_agents.py': '3 agentes com IA',
        'core_agents_v3.py': '5 agentes core',
        'system_agents.py': '3 agentes de sistema',
        'service_agents.py': '2 agentes de serviço',
        'meta_cognitive_agents.py': '2 agentes metacognitivos',
        'code_analyzer_agent.py': 'Analisador de código',
        'web_search_agent.py': 'Busca web',
        'code_corrector_agent.py': 'Corretor de código',
        'performance_monitor_agent.py': 'Monitor de performance',
        'guard_service.py': 'Serviço de segurança'
    }
    
    # Verificar na raiz
    logger.info("\n✅ ARQUIVOS NA RAIZ:")
    encontrados_raiz = []
    for arquivo, descricao in agentes_esperados.items():
        if os.path.exists(arquivo):
            encontrados_raiz.append(arquivo)
            logger.info(f"  ✓ {arquivo} - {descricao}")
    
    # Verificar em subdiretórios conhecidos
    subdirs_conhecidos = [
        'backend/agent/alsham',
        'suna_alsham/core',
        'suna_alsham/coordination',
        'suna_alsham/monitoring',
        'backend',
        'suna_alsham'
    ]
    
    logger.info("\n📁 VERIFICANDO SUBDIRETÓRIOS:")
    arquivos_em_subdirs = {}
    
    for subdir in subdirs_conhecidos:
        if os.path.exists(subdir):
            logger.info(f"\n  📂 {subdir}/")
            for arquivo in os.listdir(subdir):
                if arquivo.endswith('.py'):
                    caminho_completo = os.path.join(subdir, arquivo)
                    arquivos_em_subdirs[arquivo] = subdir
                    logger.info(f"    - {arquivo}")
    
    # Arquivos importantes em subdirs
    logger.info("\n⚠️ AGENTES IMPORTANTES EM SUBDIRETÓRIOS:")
    agentes_fora_raiz = []
    for arquivo in agentes_esperados:
        if arquivo not in encontrados_raiz:
            # Procurar em subdirs
            for nome_arquivo, local in arquivos_em_subdirs.items():
                if nome_arquivo == arquivo or nome_arquivo.replace('_', '') in arquivo:
                    agentes_fora_raiz.append(f"{arquivo} → {local}/")
                    logger.warning(f"  ⚠️ {arquivo} está em {local}/")
                    break
    
    # Resumo
    logger.info("\n" + "=" * 60)
    logger.info("📊 RESUMO DA ESTRUTURA:")
    logger.info(f"  ✅ Agentes na raiz: {len(encontrados_raiz)}/12")
    logger.info(f"  ⚠️ Agentes em subdirs: {len(agentes_fora_raiz)}")
    logger.info(f"  ❌ Agentes faltando: {12 - len(encontrados_raiz) - len(agentes_fora_raiz)}")
    
    # Adicionar paths necessários
    paths_adicionais = []
    for subdir in subdirs_conhecidos:
        if os.path.exists(subdir) and subdir not in sys.path:
            sys.path.append(subdir)
            paths_adicionais.append(subdir)
            logger.info(f"  📍 Adicionado ao path: {subdir}")
    
    return encontrados_raiz, agentes_fora_raiz, paths_adicionais

# E modifique a função main() para chamar esta verificação:

async def main():
    """Sistema principal SUNA-ALSHAM v2.0"""
    print_header()
    
    # NOVA: Verificar estrutura completa primeiro
    verificar_estrutura_completa()
    
    # Verificar arquivos
    arquivos_ok = verificar_arquivos()
    if not arquivos_ok:
        logger.error("❌ Verificação de arquivos falhou!")
        logger.info("⚠️ Continuando com módulos disponíveis...")
    
    # ... resto do código continua igual ...
