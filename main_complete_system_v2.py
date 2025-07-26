# SUBSTITUA a função criar_todos_agentes() no main_complete_system_v2.py por esta:

async def criar_todos_agentes(self):
    """Cria todos os 24 agentes do sistema"""
    self.logger.info("🎯 Criando agentes...")
    todos_agentes = []
    
    # MAPEAMENTO CORRETO: módulo → função real
    modulos_e_funcoes = [
        (specialized_agents, 'create_specialized_agents', 5),
        (ai_powered_agents, 'create_ai_agents', 3),
        (core_agents_v3, 'create_core_agents_v3', 5),
        (system_agents, 'create_system_agents', 3),
        (service_agents, 'create_service_agents', 2),  # Verificar nome
        (meta_cognitive_agents, 'create_meta_cognitive_agents', 2),  # Verificar nome
        (code_analyzer_agent, 'create_code_analyzer_agent', 1),  # Singular
        (web_search_agent, 'create_web_search_agent', 1),  # Singular
        (code_corrector_agent, 'create_code_corrector_agent', 1),  # Singular
        (performance_monitor_agent, 'create_performance_monitor_agent', 1)  # Singular
    ]
    
    for modulo, nome_funcao, qtd_esperada in modulos_e_funcoes:
        if modulo and hasattr(modulo, nome_funcao):
            try:
                self.logger.info(f"🔧 Criando agentes via {nome_funcao}...")
                
                # Obter a função correta
                create_function = getattr(modulo, nome_funcao)
                
                # Chamar a função com os parâmetros corretos
                if asyncio.iscoroutinefunction(create_function):
                    agentes = await create_function(self.network)
                else:
                    # A maioria precisa de message_bus como parâmetro
                    agentes = create_function(self.network)
                
                if agentes:
                    # Garantir que é uma lista
                    if not isinstance(agentes, list):
                        agentes = [agentes]
                    
                    todos_agentes.extend(agentes)
                    self.logger.info(f"✅ {len(agentes)}/{qtd_esperada} agentes criados via {nome_funcao}")
                    
                    # Listar agentes criados
                    for agent in agentes:
                        agent_id = getattr(agent, 'agent_id', 'unknown')
                        self.logger.info(f"  └─ {agent_id} inicializado")
                else:
                    self.logger.warning(f"⚠️ {nome_funcao} retornou vazio")
                    
            except Exception as e:
                self.logger.error(f"❌ Erro ao chamar {nome_funcao}: {str(e)}")
                import traceback
                self.logger.error(traceback.format_exc())
        else:
            self.logger.warning(f"⚠️ Função {nome_funcao} não encontrada no módulo")
    
    self.logger.info(f"📊 Total de agentes criados: {len(todos_agentes)}")
    return todos_agentes
