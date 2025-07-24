"""
SUNA-ALSHAM System Agents
Agentes de sistema para monitoramento, evolução e integração
"""

import asyncio
import logging
import os
import json
import psutil
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class MonitorAgent:
    """Agente de monitoramento avançado do sistema"""
    
    def __init__(self, agent_id: str = "monitor_001"):
        self.agent_id = agent_id
        self.agent_type = "MonitorAgent"
        self.status = 'inactive'
        self.capabilities = [
            'system_monitoring', 'performance_tracking', 'resource_monitoring',
            'health_checks', 'alert_management', 'predictive_monitoring'
        ]
        self.monitoring_interval = 30  # segundos
        self.metrics_history = []
        self.alerts_generated = 0
        self.created_at = datetime.now()
        
    async def initialize(self):
        """Inicializa o agente de monitoramento"""
        try:
            self.status = 'active'
            logger.info(f"📊 {self.agent_type} {self.agent_id} inicializado")
            logger.info(f"⏱️ Intervalo de monitoramento: {self.monitoring_interval}s")
            return True
        except Exception as e:
            logger.error(f"❌ Erro inicializando {self.agent_id}: {e}")
            return False
    
    async def collect_system_metrics(self) -> Dict:
        """Coleta métricas do sistema"""
        try:
            # Métricas básicas do sistema
            cpu_percent = random.uniform(10, 80)  # Simulação
            memory_percent = random.uniform(20, 70)
            disk_usage = random.uniform(30, 60)
            
            # Métricas de rede (simuladas)
            network_io = {
                'bytes_sent': random.randint(1000000, 10000000),
                'bytes_recv': random.randint(1000000, 10000000)
            }
            
            # Métricas de aplicação
            response_time = random.uniform(0.1, 2.0)
            throughput = random.randint(100, 1000)
            error_rate = random.uniform(0.0, 0.05)
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'system': {
                    'cpu_percent': round(cpu_percent, 2),
                    'memory_percent': round(memory_percent, 2),
                    'disk_usage': round(disk_usage, 2)
                },
                'network': network_io,
                'application': {
                    'response_time': round(response_time, 3),
                    'throughput': throughput,
                    'error_rate': round(error_rate, 4)
                },
                'health_score': self._calculate_health_score(cpu_percent, memory_percent, error_rate)
            }
            
            # Armazenar histórico (manter últimas 100 medições)
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 100:
                self.metrics_history.pop(0)
            
            # Verificar alertas
            await self._check_alerts(metrics)
            
            logger.debug(f"📊 Métricas coletadas - Health Score: {metrics['health_score']}")
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Erro coletando métricas: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def generate_performance_report(self) -> Dict:
        """Gera relatório de performance"""
        try:
            if not self.metrics_history:
                return {'error': 'Nenhuma métrica disponível'}
            
            # Análise das últimas métricas
            recent_metrics = self.metrics_history[-10:] if len(self.metrics_history) >= 10 else self.metrics_history
            
            # Cálculos estatísticos
            avg_cpu = sum(m['system']['cpu_percent'] for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m['system']['memory_percent'] for m in recent_metrics) / len(recent_metrics)
            avg_response_time = sum(m['application']['response_time'] for m in recent_metrics) / len(recent_metrics)
            avg_health = sum(m['health_score'] for m in recent_metrics) / len(recent_metrics)
            
            # Tendências
            if len(recent_metrics) >= 5:
                cpu_trend = self._calculate_trend([m['system']['cpu_percent'] for m in recent_metrics[-5:]])
                memory_trend = self._calculate_trend([m['system']['memory_percent'] for m in recent_metrics[-5:]])
            else:
                cpu_trend = memory_trend = 'stable'
            
            report = {
                'agent_id': self.agent_id,
                'report_period': f"Últimas {len(recent_metrics)} medições",
                'averages': {
                    'cpu_percent': round(avg_cpu, 2),
                    'memory_percent': round(avg_memory, 2),
                    'response_time': round(avg_response_time, 3),
                    'health_score': round(avg_health, 2)
                },
                'trends': {
                    'cpu': cpu_trend,
                    'memory': memory_trend
                },
                'alerts_generated': self.alerts_generated,
                'recommendations': self._generate_recommendations(avg_cpu, avg_memory, avg_response_time),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"📋 Relatório de performance gerado - Health: {avg_health:.2f}")
            return report
            
        except Exception as e:
            logger.error(f"❌ Erro gerando relatório: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _calculate_health_score(self, cpu: float, memory: float, error_rate: float) -> float:
        """Calcula score de saúde do sistema"""
        # Score baseado em CPU, memória e taxa de erro
        cpu_score = max(0, 100 - cpu) / 100
        memory_score = max(0, 100 - memory) / 100
        error_score = max(0, 1 - error_rate * 20)  # Penaliza erros
        
        health_score = (cpu_score * 0.4 + memory_score * 0.4 + error_score * 0.2) * 100
        return round(health_score, 2)
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calcula tendência dos valores"""
        if len(values) < 2:
            return 'stable'
        
        # Regressão linear simples
        n = len(values)
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * values[i] for i in range(n))
        x2_sum = sum(i * i for i in range(n))
        
        slope = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum * x_sum)
        
        if slope > 0.5:
            return 'increasing'
        elif slope < -0.5:
            return 'decreasing'
        else:
            return 'stable'
    
    def _generate_recommendations(self, cpu: float, memory: float, response_time: float) -> List[str]:
        """Gera recomendações baseadas nas métricas"""
        recommendations = []
        
        if cpu > 70:
            recommendations.append("CPU alta - considerar otimização de algoritmos")
        if memory > 80:
            recommendations.append("Memória alta - verificar vazamentos de memória")
        if response_time > 1.5:
            recommendations.append("Tempo de resposta alto - otimizar consultas")
        if cpu < 20 and memory < 30:
            recommendations.append("Recursos subutilizados - considerar redimensionamento")
        
        return recommendations
    
    async def _check_alerts(self, metrics: Dict):
        """Verifica se deve gerar alertas"""
        try:
            alerts = []
            
            # Alertas de CPU
            if metrics['system']['cpu_percent'] > 85:
                alerts.append({
                    'type': 'cpu_high',
                    'severity': 'high',
                    'message': f"CPU crítica: {metrics['system']['cpu_percent']}%"
                })
            
            # Alertas de memória
            if metrics['system']['memory_percent'] > 90:
                alerts.append({
                    'type': 'memory_high',
                    'severity': 'high',
                    'message': f"Memória crítica: {metrics['system']['memory_percent']}%"
                })
            
            # Alertas de erro
            if metrics['application']['error_rate'] > 0.1:
                alerts.append({
                    'type': 'error_rate_high',
                    'severity': 'medium',
                    'message': f"Taxa de erro alta: {metrics['application']['error_rate']:.2%}"
                })
            
            if alerts:
                self.alerts_generated += len(alerts)
                for alert in alerts:
                    logger.warning(f"🚨 ALERTA {alert['severity'].upper()}: {alert['message']}")
                    
        except Exception as e:
            logger.error(f"❌ Erro verificando alertas: {e}")
    
    async def get_status(self):
        """Retorna status do monitoramento"""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'status': self.status,
            'capabilities': self.capabilities,
            'monitoring_interval': self.monitoring_interval,
            'metrics_collected': len(self.metrics_history),
            'alerts_generated': self.alerts_generated,
            'created_at': self.created_at.isoformat()
        }

class EvolverAgent:
    """Agente de evolução e auto-melhoria do sistema"""
    
    def __init__(self, agent_id: str = "evolver_001"):
        self.agent_id = agent_id
        self.agent_type = "EvolverAgent"
        self.status = 'inactive'
        self.capabilities = [
            'system_evolution', 'auto_optimization', 'adaptive_learning',
            'performance_enhancement', 'code_generation', 'self_modification'
        ]
        self.evolution_cycles = 0
        self.improvements_made = 0
        self.evolution_history = []
        self.created_at = datetime.now()
        
    async def initialize(self):
        """Inicializa o agente de evolução"""
        try:
            self.status = 'active'
            logger.info(f"🧬 {self.agent_type} {self.agent_id} inicializado")
            logger.info(f"🔄 Capacidades evolutivas ativadas")
            return True
        except Exception as e:
            logger.error(f"❌ Erro inicializando {self.agent_id}: {e}")
            return False
    
    async def analyze_system_evolution(self, system_metrics: Dict) -> Dict:
        """Analisa oportunidades de evolução do sistema"""
        try:
            # Análise de performance atual
            current_performance = system_metrics.get('health_score', 80)
            target_performance = 95
            
            # Identificar áreas de melhoria
            improvement_areas = []
            
            if system_metrics.get('system', {}).get('cpu_percent', 0) > 60:
                improvement_areas.append({
                    'area': 'cpu_optimization',
                    'priority': 'high',
                    'description': 'Otimizar uso de CPU através de algoritmos mais eficientes'
                })
            
            if system_metrics.get('application', {}).get('response_time', 0) > 1.0:
                improvement_areas.append({
                    'area': 'response_optimization',
                    'priority': 'medium',
                    'description': 'Melhorar tempo de resposta com cache inteligente'
                })
            
            if system_metrics.get('application', {}).get('error_rate', 0) > 0.02:
                improvement_areas.append({
                    'area': 'error_reduction',
                    'priority': 'high',
                    'description': 'Implementar tratamento de erros mais robusto'
                })
            
            # Gerar plano de evolução
            evolution_plan = {
                'agent_id': self.agent_id,
                'current_performance': current_performance,
                'target_performance': target_performance,
                'performance_gap': target_performance - current_performance,
                'improvement_areas': improvement_areas,
                'evolution_strategy': self._generate_evolution_strategy(improvement_areas),
                'estimated_improvement': f"{min(len(improvement_areas) * 5, 15)}%",
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"🧬 Análise evolutiva completa - {len(improvement_areas)} áreas identificadas")
            return evolution_plan
            
        except Exception as e:
            logger.error(f"❌ Erro na análise evolutiva: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def execute_evolution_cycle(self, evolution_plan: Dict) -> Dict:
        """Executa um ciclo de evolução do sistema"""
        try:
            improvements = []
            
            # Simular implementação de melhorias
            for area in evolution_plan.get('improvement_areas', []):
                improvement = await self._implement_improvement(area)
                improvements.append(improvement)
                
                if improvement['success']:
                    self.improvements_made += 1
            
            # Registrar ciclo de evolução
            self.evolution_cycles += 1
            evolution_record = {
                'cycle': self.evolution_cycles,
                'timestamp': datetime.now().isoformat(),
                'improvements': improvements,
                'success_rate': sum(1 for i in improvements if i['success']) / len(improvements) if improvements else 0
            }
            
            self.evolution_history.append(evolution_record)
            
            # Manter apenas últimos 20 ciclos
            if len(self.evolution_history) > 20:
                self.evolution_history.pop(0)
            
            result = {
                'agent_id': self.agent_id,
                'evolution_cycle': self.evolution_cycles,
                'improvements_attempted': len(improvements),
                'improvements_successful': sum(1 for i in improvements if i['success']),
                'success_rate': evolution_record['success_rate'],
                'total_improvements': self.improvements_made,
                'next_evolution_eta': '24 hours',
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"🚀 Ciclo evolutivo {self.evolution_cycles} completo - {result['improvements_successful']}/{result['improvements_attempted']} sucessos")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro no ciclo evolutivo: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _generate_evolution_strategy(self, improvement_areas: List[Dict]) -> str:
        """Gera estratégia de evolução"""
        if not improvement_areas:
            return 'maintenance'
        
        high_priority = sum(1 for area in improvement_areas if area['priority'] == 'high')
        
        if high_priority >= 2:
            return 'aggressive_optimization'
        elif high_priority == 1:
            return 'targeted_improvement'
        else:
            return 'gradual_enhancement'
    
    async def _implement_improvement(self, improvement_area: Dict) -> Dict:
        """Simula implementação de uma melhoria"""
        try:
            # Simulação de tempo de implementação
            implementation_time = random.uniform(0.1, 0.5)
            await asyncio.sleep(implementation_time)
            
            # Simulação de sucesso (90% de chance)
            success = random.random() > 0.1
            
            improvement = {
                'area': improvement_area['area'],
                'description': improvement_area['description'],
                'priority': improvement_area['priority'],
                'success': success,
                'implementation_time': round(implementation_time, 3),
                'estimated_impact': f"{random.randint(5, 20)}%" if success else "0%"
            }
            
            if success:
                logger.info(f"✅ Melhoria implementada: {improvement_area['area']}")
            else:
                logger.warning(f"⚠️ Falha na implementação: {improvement_area['area']}")
            
            return improvement
            
        except Exception as e:
            logger.error(f"❌ Erro implementando melhoria: {e}")
            return {'success': False, 'error': str(e)}
    
    async def get_status(self):
        """Retorna status da evolução"""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'status': self.status,
            'capabilities': self.capabilities,
            'evolution_cycles': self.evolution_cycles,
            'improvements_made': self.improvements_made,
            'evolution_history_size': len(self.evolution_history),
            'created_at': self.created_at.isoformat()
        }

class IntegratorAgent:
    """Agente de integração com sistemas externos"""
    
    def __init__(self, agent_id: str = "integrator_001"):
        self.agent_id = agent_id
        self.agent_type = "IntegratorAgent"
        self.status = 'inactive'
        self.capabilities = [
            'api_integration', 'data_synchronization', 'protocol_translation',
            'service_orchestration', 'webhook_management', 'real_time_sync'
        ]
        self.integrations = {}
        self.sync_operations = 0
        self.failed_integrations = 0
        self.created_at = datetime.now()
        
    async def initialize(self):
        """Inicializa o agente de integração"""
        try:
            self.status = 'active'
            logger.info(f"🔗 {self.agent_type} {self.agent_id} inicializado")
            logger.info(f"🌐 Pronto para integrações externas")
            return True
        except Exception as e:
            logger.error(f"❌ Erro inicializando {self.agent_id}: {e}")
            return False
    
    async def register_integration(self, integration_config: Dict) -> Dict:
        """Registra nova integração externa"""
        try:
            integration_id = integration_config.get('id', f"integration_{len(self.integrations) + 1}")
            service_name = integration_config.get('service_name', 'unknown')
            endpoint = integration_config.get('endpoint', '')
            auth_type = integration_config.get('auth_type', 'none')
            
            # Validar configuração
            if not endpoint:
                raise ValueError("Endpoint é obrigatório")
            
            # Registrar integração
            self.integrations[integration_id] = {
                'id': integration_id,
                'service_name': service_name,
                'endpoint': endpoint,
                'auth_type': auth_type,
                'status': 'registered',
                'last_sync': None,
                'sync_count': 0,
                'error_count': 0,
                'registered_at': datetime.now().isoformat()
            }
            
            result = {
                'agent_id': self.agent_id,
                'integration_id': integration_id,
                'service_name': service_name,
                'status': 'registered',
                'total_integrations': len(self.integrations),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"🔗 Integração registrada: {service_name} ({integration_id})")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro registrando integração: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def sync_with_external_service(self, integration_id: str, data: Dict) -> Dict:
        """Sincroniza dados com serviço externo"""
        try:
            if integration_id not in self.integrations:
                raise ValueError(f"Integração {integration_id} não encontrada")
            
            integration = self.integrations[integration_id]
            
            # Simulação de sincronização
            sync_time = random.uniform(0.2, 1.0)
            await asyncio.sleep(sync_time)
            
            # Simulação de sucesso (85% de chance)
            success = random.random() > 0.15
            
            if success:
                # Atualizar estatísticas de sucesso
                integration['status'] = 'active'
                integration['last_sync'] = datetime.now().isoformat()
                integration['sync_count'] += 1
                self.sync_operations += 1
                
                result = {
                    'agent_id': self.agent_id,
                    'integration_id': integration_id,
                    'service_name': integration['service_name'],
                    'status': 'success',
                    'sync_time': round(sync_time, 3),
                    'data_points_synced': len(data.get('items', [])),
                    'total_syncs': integration['sync_count'],
                    'timestamp': datetime.now().isoformat()
                }
                
                logger.info(f"✅ Sincronização bem-sucedida: {integration['service_name']}")
                
            else:
                # Atualizar estatísticas de erro
                integration['error_count'] += 1
                self.failed_integrations += 1
                
                result = {
                    'agent_id': self.agent_id,
                    'integration_id': integration_id,
                    'service_name': integration['service_name'],
                    'status': 'failed',
                    'error': 'Falha na comunicação com serviço externo',
                    'retry_in': '5 minutes',
                    'timestamp': datetime.now().isoformat()
                }
                
                logger.warning(f"⚠️ Falha na sincronização: {integration['service_name']}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na sincronização: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def get_integration_status(self) -> Dict:
        """Retorna status de todas as integrações"""
        try:
            active_integrations = sum(1 for i in self.integrations.values() if i['status'] == 'active')
            total_syncs = sum(i['sync_count'] for i in self.integrations.values())
            total_errors = sum(i['error_count'] for i in self.integrations.values())
            
            status = {
                'agent_id': self.agent_id,
                'total_integrations': len(self.integrations),
                'active_integrations': active_integrations,
                'total_sync_operations': total_syncs,
                'total_errors': total_errors,
                'success_rate': round((total_syncs / max(total_syncs + total_errors, 1)) * 100, 2),
                'integrations': {
                    integration_id: {
                        'service_name': integration['service_name'],
                        'status': integration['status'],
                        'sync_count': integration['sync_count'],
                        'error_count': integration['error_count'],
                        'last_sync': integration['last_sync']
                    }
                    for integration_id, integration in self.integrations.items()
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return status
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo status das integrações: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def get_status(self):
        """Retorna status do integrador"""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'status': self.status,
            'capabilities': self.capabilities,
            'total_integrations': len(self.integrations),
            'sync_operations': self.sync_operations,
            'failed_integrations': self.failed_integrations,
            'created_at': self.created_at.isoformat()
        }

# Função para criar agentes de sistema - CORRIGIDO
def create_system_agents(message_bus) -> List:
    """Cria e inicializa agentes de sistema com MessageBus"""
    from multi_agent_network import BaseNetworkAgent, AgentType
    
    # Criar agentes compatíveis com a rede
    agents = [
        MonitorAgentNetworkAdapter("monitor_001", AgentType.MONITOR, message_bus),
        EvolverAgentNetworkAdapter("evolver_001", AgentType.EVOLVER, message_bus),
        IntegratorAgentNetworkAdapter("integrator_001", AgentType.INTEGRATOR, message_bus)
    ]
    
    logger.info(f"✅ {len(agents)} agentes de sistema criados com MessageBus")
    return agents


# Adaptadores para compatibilidade com rede multi-agente
class MonitorAgentNetworkAdapter:
    """Adaptador para MonitorAgent na rede multi-agente"""
    
    def __init__(self, agent_id: str, agent_type, message_bus):
        from multi_agent_network import BaseNetworkAgent, AgentCapability
        
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_bus = message_bus
        self.status = 'active'
        self.capabilities = [
            AgentCapability(
                name="system_monitoring",
                description="Monitoramento avançado do sistema",
                input_types=["system_metrics", "performance_data"],
                output_types=["monitoring_report", "alerts"],
                processing_time_ms=200.0,
                accuracy_score=0.96,
                resource_cost=0.1
            )
        ]
        
        self.monitor_agent = MonitorAgent(agent_id)
        
        if message_bus:
            message_bus.register_agent(self)

class EvolverAgentNetworkAdapter:
    """Adaptador para EvolverAgent na rede multi-agente"""
    
    def __init__(self, agent_id: str, agent_type, message_bus):
        from multi_agent_network import BaseNetworkAgent, AgentCapability
        
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_bus = message_bus
        self.status = 'active'
        self.capabilities = [
            AgentCapability(
                name="system_evolution",
                description="Evolução contínua do sistema",
                input_types=["evolution_data", "adaptation_signals"],
                output_types=["evolved_system", "improvements"],
                processing_time_ms=1500.0,
                accuracy_score=0.88,
                resource_cost=0.6
            )
        ]
        
        self.evolver_agent = EvolverAgent(agent_id)
        
        if message_bus:
            message_bus.register_agent(self)

class IntegratorAgentNetworkAdapter:
    """Adaptador para IntegratorAgent na rede multi-agente"""
    
    def __init__(self, agent_id: str, agent_type, message_bus):
        from multi_agent_network import BaseNetworkAgent, AgentCapability
        
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_bus = message_bus
        self.status = 'active'
        self.capabilities = [
            AgentCapability(
                name="system_integration",
                description="Integração de componentes do sistema",
                input_types=["integration_request", "component_data"],
                output_types=["integrated_system", "integration_report"],
                processing_time_ms=800.0,
                accuracy_score=0.92,
                resource_cost=0.4
            )
        ]
        
        self.integrator_agent = IntegratorAgent(agent_id)
        
        if message_bus:
            message_bus.register_agent(self)

