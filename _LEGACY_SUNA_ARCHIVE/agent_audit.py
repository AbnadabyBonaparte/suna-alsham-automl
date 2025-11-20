#!/usr/bin/env python3
"""
ALSHAM QUANTUM - Auditoria Completa de Agentes
Mapeia EXATAMENTE quais agentes estão funcionando vs faltando
"""
import os
import sys
import importlib
import inspect
from pathlib import Path

class AgentAuditor:
    def __init__(self):
        self.core_structure = {
            # Arquivos Agrupados (9 agentes)
            'system_agents.py': ['SystemMonitorAgent', 'ResourceOptimizerAgent', 'ConfigurationAgent'],
            'service_agents.py': ['ApiGatewayAgent', 'DatabaseAgent'], 
            'specialized_agents.py': ['SecurityAgent', 'PerformanceAgent'],
            'core_agents_v3.py': ['CoreOrchestratorAgent', 'MetaLearningAgent'],
            
            # Arquivos Individuais Críticos (27 agentes)
            'central_coordinator_agent.py': ['CentralCoordinatorAgent'],
            'performance_monitor_agent.py': ['PerformanceMonitorAgent'],
            'security_guardian_agent.py': ['SecurityGuardianAgent'],
            'meta_cognitive_agents.py': ['MetaCognitiveAgent'],
            'quantum_core_agent.py': ['QuantumCoreAgent'],
            'adaptive_learning_agent.py': ['AdaptiveLearningAgent'],
            'resource_manager_agent.py': ['ResourceManagerAgent'],
            'task_coordinator_agent.py': ['TaskCoordinatorAgent'],
            'communication_hub_agent.py': ['CommunicationHubAgent'],
            'data_integration_agent.py': ['DataIntegrationAgent'],
            'workflow_orchestrator_agent.py': ['WorkflowOrchestratorAgent'],
            'intelligence_coordinator_agent.py': ['IntelligenceCoordinatorAgent'],
            'system_health_agent.py': ['SystemHealthAgent'],
            'error_handler_agent.py': ['ErrorHandlerAgent'],
            'logging_agent.py': ['LoggingAgent'],
            'configuration_manager_agent.py': ['ConfigurationManagerAgent'],
            'deployment_agent.py': ['DeploymentAgent'],
            'monitoring_dashboard_agent.py': ['MonitoringDashboardAgent'],
            'alert_system_agent.py': ['AlertSystemAgent'],
            'backup_recovery_agent.py': ['BackupRecoveryAgent'],
            'load_balancer_agent.py': ['LoadBalancerAgent'],
            'cache_manager_agent.py': ['CacheManagerAgent'],
            'api_rate_limiter_agent.py': ['ApiRateLimiterAgent'],
            'data_validation_agent.py': ['DataValidationAgent'],
            'encryption_agent.py': ['EncryptionAgent'],
            'audit_logger_agent.py': ['AuditLoggerAgent'],
            'health_check_agent.py': ['HealthCheckAgent']
        }
        
        self.loaded_agents = []
        self.failed_agents = []
        self.missing_files = []
        
    def audit_core_agents(self):
        """Auditoria completa dos 36 agentes CORE"""
        print("🔍 AUDITORIA COMPLETA - ALSHAM QUANTUM CORE")
        print("="*60)
        
        total_expected = sum(len(agents) for agents in self.core_structure.values())
        print(f"📊 Agentes CORE Esperados: {total_expected}")
        
        for file_path, agent_classes in self.core_structure.items():
            print(f"\n📁 Verificando: {file_path}")
            
            if not os.path.exists(file_path):
                print(f"❌ ARQUIVO FALTANDO: {file_path}")
                self.missing_files.append(file_path)
                for agent_class in agent_classes:
                    self.failed_agents.append(f"{file_path}::{agent_class}")
                continue
                
            # Tentar importar cada agente
            module_name = file_path.replace('.py', '').replace('/', '.')
            
            try:
                # Adicionar diretório atual ao path se necessário
                if '.' not in sys.path:
                    sys.path.insert(0, '.')
                
                module = importlib.import_module(module_name)
                print(f"✅ Módulo carregado: {module_name}")
                
                # Verificar cada classe de agente
                for agent_class in agent_classes:
                    try:
                        if hasattr(module, agent_class):
                            agent_obj = getattr(module, agent_class)
                            if inspect.isclass(agent_obj):
                                self.loaded_agents.append(f"{file_path}::{agent_class}")
                                print(f"  ✅ {agent_class} - OK")
                            else:
                                self.failed_agents.append(f"{file_path}::{agent_class}")
                                print(f"  ❌ {agent_class} - Não é classe")
                        else:
                            self.failed_agents.append(f"{file_path}::{agent_class}")
                            print(f"  ❌ {agent_class} - Classe não encontrada")
                    except Exception as e:
                        self.failed_agents.append(f"{file_path}::{agent_class}")
                        print(f"  ❌ {agent_class} - Erro: {str(e)[:50]}")
                        
            except Exception as e:
                print(f"❌ ERRO no módulo {module_name}: {str(e)[:100]}")
                for agent_class in agent_classes:
                    self.failed_agents.append(f"{file_path}::{agent_class}")
    
    def generate_report(self):
        """Gera relatório completo da auditoria"""
        print("\n" + "="*60)
        print("📋 RELATÓRIO FINAL DA AUDITORIA")
        print("="*60)
        
        total_expected = sum(len(agents) for agents in self.core_structure.values())
        loaded_count = len(self.loaded_agents)
        failed_count = len(self.failed_agents)
        
        print(f"📊 RESUMO EXECUTIVO:")
        print(f"   Agentes Esperados: {total_expected}")
        print(f"   Agentes Carregados: {loaded_count}")
        print(f"   Agentes Falhando: {failed_count}")
        print(f"   Taxa de Sucesso: {(loaded_count/total_expected)*100:.1f}%")
        
        if self.missing_files:
            print(f"\n❌ ARQUIVOS FALTANDO ({len(self.missing_files)}):")
            for file in self.missing_files:
                print(f"   - {file}")
        
        if self.failed_agents:
            print(f"\n❌ AGENTES FALHANDO ({len(self.failed_agents)}):")
            for agent in self.failed_agents:
                print(f"   - {agent}")
        
        print(f"\n✅ AGENTES FUNCIONANDO ({len(self.loaded_agents)}):")
        for agent in self.loaded_agents:
            print(f"   - {agent}")
            
        return {
            'total_expected': total_expected,
            'loaded_count': loaded_count,
            'failed_count': failed_count,
            'success_rate': (loaded_count/total_expected)*100,
            'missing_files': self.missing_files,
            'failed_agents': self.failed_agents,
            'loaded_agents': self.loaded_agents
        }

if __name__ == "__main__":
    auditor = AgentAuditor()
    auditor.audit_core_agents()
    report = auditor.generate_report()
