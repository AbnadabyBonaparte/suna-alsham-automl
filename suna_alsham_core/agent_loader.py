async def initialize_all_agents(network: Any) -> Dict[str, Any]:
    agents_loaded = 0
    failed_modules = []
    
    # Lista explícita de todas as fábricas em ordem de prioridade
    core_factories = [
        create_performance_monitor_agent,  # Primeiro os agentes de sistema críticos
        create_core_agents_v3,
        create_computer_control_agent,
        create_specialized_agents,
        create_web_search_agent,
        create_ai_agents,
        create_system_agents,
        create_service_agents,
        create_meta_cognitive_agents,
        create_code_corrector_agent,
        
        # Agentes que podem estar faltando - garantir que sejam chamados
        create_security_guardian_agent,     # <-- Garantir que este seja chamado
        create_security_enhancements_agent, # <-- Garantir que este seja chamado
        create_testing_agent,               # <-- Garantir que este seja chamado
        create_visualization_agent,         # <-- Garantir que este seja chamado
        create_disaster_recovery_agent,     # <-- Garantir que este seja chamado
        create_debug_master_agent,          # <-- Garantir que este seja chamado
        
        # Outros agentes
        create_code_analyzer_agent,
        create_validation_sentinel_agent,
        create_backup_agent,
        create_database_agent,
        create_logging_agent,
        create_api_gateway_agent,
        create_notification_agent,
        create_deployment_agent,
        create_evolution_engine_agents,
    ]
    
    domain_factories = [
        create_analytics_agents,
        create_sales_agents,
        create_social_media_agents,
    ]

    logger.info("--- INICIANDO AUDITORIA DE CARREGAMENTO DE AGENTES ---")
    
    # Carrega Agentes do Núcleo
    for factory in core_factories:
        factory_name = factory.__name__
        logger.info(f"--> Chamando fábrica de núcleo: {factory_name}...")
        try:
            agents = factory(network.message_bus)
            num_created = len(agents)
            logger.info(f"<-- SUCESSO: Fábrica '{factory_name}' retornou {num_created} agente(s).")
            for agent in agents:
                network.register_agent(agent)
                agents_loaded += 1
        except ModuleNotFoundError as e:
            logger.error(f"<-- FALHA: Fábrica '{factory_name}' falhou por módulo ausente: {e.name}", exc_info=True)
            failed_modules.append(f"{factory_name} (módulo ausente: {e.name})")
        except ImportError as e:
            logger.error(f"<-- FALHA: Fábrica '{factory_name}' falhou na importação: {str(e)}", exc_info=True)
            failed_modules.append(f"{factory_name} (erro de importação)")
        except Exception as e:
            logger.error(f"<-- FALHA: Fábrica '{factory_name}' falhou: {e}", exc_info=True)
            failed_modules.append(factory_name)

    # Carrega Agentes de Domínio
    for factory in domain_factories:
        factory_name = factory.__name__
        logger.info(f"--> Chamando fábrica de domínio: {factory_name}...")
        try:
            agents = factory(network.message_bus)
            num_created = len(agents)
            logger.info(f"<-- SUCESSO: Fábrica '{factory_name}' retornou {num_created} agente(s).")
            for agent in agents:
                network.register_agent(agent)
                agents_loaded += 1
        except Exception as e:
            logger.error(f"<-- FALHA: Fábrica '{factory_name}' falhou: {e}", exc_info=True)
            failed_modules.append(factory_name)
            
    logger.info(f"--- FIM DA AUDITORIA. Total: {agents_loaded} agentes carregados. ---")
    return {
        "summary": {"agents_loaded": agents_loaded, "failed_modules_count": len(failed_modules)},
        "failed_modules": failed_modules,
    }
