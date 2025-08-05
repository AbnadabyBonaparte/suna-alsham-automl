# CONFIGURAÇÃO COMPLETA - TODOS OS 55 AGENTES
agent_factories_config = [
    # ===== NÚCLEO SUNA-ALSHAM (34 AGENTES) =====
    
    # Arquivo: core_agents_v3.py (5 Agentes)
    {"factory_path": "suna_alsham_core.core_agents_v3", "factory_name": "create_core_agents_v3", "params": [network.message_bus]},
    
    # Arquivo: specialized_agents.py (2 Agentes) ✅ CONFIRMADO
    {"factory_path": "suna_alsham_core.specialized_agents", "factory_name": "create_specialized_agents", "params": [network.message_bus]},
    
    # Arquivo: system_agents.py (3 Agentes) ✅ CONFIRMADO
    {"factory_path": "suna_alsham_core.system_agents", "factory_name": "create_system_agents", "params": [network.message_bus]},
    
    # Arquivo: service_agents.py (2 Agentes)
    {"factory_path": "suna_alsham_core.service_agents", "factory_name": "create_service_agents", "params": [network.message_bus]},
    
    # Arquivo: meta_cognitive_agents.py (2 Agentes)
    {"factory_path": "suna_alsham_core.meta_cognitive_agents", "factory_name": "create_meta_cognitive_agents", "params": [network.message_bus]},
    
    # Arquivo: ai_powered_agents.py (1 Agente)
    {"factory_path": "suna_alsham_core.ai_powered_agents", "factory_name": "create_ai_powered_agents", "params": [network.message_bus]},
    
    # Arquivo: api_gateway_agent.py (1 Agente) ✅ CONFIRMADO
    {"factory_path": "suna_alsham_core.api_gateway_agent", "factory_name": "create_api_gateway_agent", "params": [network.message_bus]},
    
    # Arquivo: backup_agent.py (1 Agente) ✅ CONFIRMADO
    {"factory_path": "suna_alsham_core.backup_agent", "factory_name": "create_backup_agent", "params": [network.message_bus]},
    
    # Arquivo: code_analyzer_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.code_analyzer_agent", "factory_name": "create_code_analyzer_agent", "params": [network.message_bus]},
    
    # Arquivo: code_corrector_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.code_corrector_agent", "factory_name": "create_code_corrector_agent", "params": [network.message_bus]},
    
    # Arquivo: computer_control_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.computer_control_agent", "factory_name": "create_computer_control_agent", "params": [network.message_bus]},
    
    # Arquivo: database_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.database_agent", "factory_name": "create_database_agent", "params": [network.message_bus]},
    
    # Arquivo: debug_agent_creation.py (1 Agente)
    {"factory_path": "suna_alsham_core.debug_agent_creation", "factory_name": "create_debug_master_agent", "params": [network.message_bus]},
    
    # Arquivo: deployment_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.deployment_agent", "factory_name": "create_deployment_agent", "params": [network.message_bus]},
    
    # Arquivo: disaster_recovery_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.disaster_recovery_agent", "factory_name": "create_disaster_recovery_agent", "params": [network.message_bus]},
    
    # Arquivo: logging_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.logging_agent", "factory_name": "create_logging_agent", "params": [network.message_bus]},
    
    # Arquivo: notification_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.notification_agent", "factory_name": "create_notification_agent", "params": [network.message_bus]},
    
    # Arquivo: performance_monitor_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.performance_monitor_agent", "factory_name": "create_performance_monitor_agent", "params": [network.message_bus]},
    
    # Arquivo: real_evolution_engine.py (1 Agente)
    {"factory_path": "suna_alsham_core.real_evolution_engine", "factory_name": "create_evolution_engine_agent", "params": [network.message_bus]},
    
    # Arquivo: security_enhancements_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.security_enhancements_agent", "factory_name": "create_security_enhancements_agent", "params": [network.message_bus]},
    
    # Arquivo: security_guardian_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.security_guardian_agent", "factory_name": "create_security_guardian_agent", "params": [network.message_bus]},
    
    # Arquivo: testing_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.testing_agent", "factory_name": "create_testing_agent", "params": [network.message_bus]},
    
    # Arquivo: validation_sentinel_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.validation_sentinel_agent", "factory_name": "create_validation_sentinel_agent", "params": [network.message_bus]},
    
    # Arquivo: visualization_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.visualization_agent", "factory_name": "create_visualization_agent", "params": [network.message_bus]},
    
    # Arquivo: web_search_agent.py (1 Agente)
    {"factory_path": "suna_alsham_core.web_search_agent", "factory_name": "create_web_search_agent", "params": [network.message_bus]},
    
    # ===== MÓDULOS DE DOMÍNIO ALSHAM GLOBAL (21 AGENTES) =====
    
    # Módulo: Analytics (5 Agentes) ✅ CONFIRMADO
    {"factory_path": "domain_modules.analytics.analytics_orchestrator_agent", "factory_name": "create_analytics_agents", "params": [network.message_bus]},
    
    # Módulo: Vendas (6 Agentes)
    {"factory_path": "domain_modules.sales.sales_orchestrator_agent", "factory_name": "create_sales_agents", "params": [network.message_bus]},
    
    # Módulo: Mídias Sociais (5 Agentes)
    {"factory_path": "domain_modules.social_media.social_media_orchestrator_agent", "factory_name": "create_social_media_agents", "params": [network.message_bus]},
    
    # Módulo: Suporte (5 Agentes) ✅ CONFIRMADO FUNCIONANDO
    {"factory_path": "domain_modules.suporte.support_orchestrator_agent", "factory_name": "create_suporte_agents", "params": [network.message_bus]},
]
