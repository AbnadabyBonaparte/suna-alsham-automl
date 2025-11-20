"""
📊 SUNA-ALSHAM Enhanced Monitoring System
Sistema de monitoramento avançado com métricas em tempo real

FUNCIONALIDADES:
✅ Métricas detalhadas de cada agente
✅ Alertas automáticos para falhas
✅ Relatórios de performance
✅ Visualização em tempo real
✅ Logs estruturados
✅ Dashboard de status
"""

import asyncio
import json
import time
import logging
import statistics
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import threading
import psutil
import os

logger = logging.getLogger(__name__)


@dataclass
class AgentMetrics:
    """Métricas detalhadas de um agente"""
    agent_id: str
    agent_type: str
    status: str
    uptime_seconds: float
    messages_processed: int
    messages_per_second: float
    response_time_avg_ms: float
    error_count: int
    error_rate: float
    cpu_usage_percent: float
    memory_usage_mb: float
    last_activity: datetime
    capabilities_count: int
    active_tasks: int


@dataclass
class SystemAlert:
    """Alerta do sistema"""
    alert_id: str
    alert_type: str
    severity: str  # low, medium, high, critical
    agent_id: Optional[str]
    message: str
    details: Dict[str, Any]
    triggered_at: datetime
    resolved_at: Optional[datetime] = None
    is_resolved: bool = False


class PerformanceAnalyzer:
    """Analisador de performance do sistema"""
    
    def __init__(self):
        self.performance_history: deque = deque(maxlen=1000)
        self.baseline_metrics: Dict[str, float] = {}
        self.performance_thresholds = {
            "response_time_ms": 1000,
            "error_rate": 0.05,
            "cpu_usage": 80.0,
            "memory_usage_mb": 512,
            "messages_per_second": 1.0
        }
    
    def analyze_agent_performance(self, metrics: AgentMetrics) -> Dict[str, Any]:
        """Analisa performance de um agente"""
        analysis = {
            "agent_id": metrics.agent_id,
            "overall_score": 0.0,
            "performance_issues": [],
            "recommendations": [],
            "trend": "stable"
        }
        
        issues = []
        score_factors = []
        
        # Analisar tempo de resposta
        if metrics.response_time_avg_ms > self.performance_thresholds["response_time_ms"]:
            issues.append({
                "type": "high_response_time",
                "severity": "medium",
                "value": metrics.response_time_avg_ms,
                "threshold": self.performance_thresholds["response_time_ms"]
            })
            score_factors.append(0.6)
        else:
            score_factors.append(0.9)
        
        # Analisar taxa de erro
        if metrics.error_rate > self.performance_thresholds["error_rate"]:
            issues.append({
                "type": "high_error_rate",
                "severity": "high",
                "value": metrics.error_rate,
                "threshold": self.performance_thresholds["error_rate"]
            })
            score_factors.append(0.4)
        else:
            score_factors.append(0.95)
        
        # Analisar uso de CPU
        if metrics.cpu_usage_percent > self.performance_thresholds["cpu_usage"]:
            issues.append({
                "type": "high_cpu_usage",
                "severity": "medium",
                "value": metrics.cpu_usage_percent,
                "threshold": self.performance_thresholds["cpu_usage"]
            })
            score_factors.append(0.7)
        else:
            score_factors.append(0.9)
        
        # Analisar throughput
        if metrics.messages_per_second < self.performance_thresholds["messages_per_second"]:
            issues.append({
                "type": "low_throughput",
                "severity": "low",
                "value": metrics.messages_per_second,
                "threshold": self.performance_thresholds["messages_per_second"]
            })
            score_factors.append(0.8)
        else:
            score_factors.append(0.95)
        
        # Calcular score geral
        analysis["overall_score"] = statistics.mean(score_factors) * 100
        analysis["performance_issues"] = issues
        
        # Gerar recomendações
        recommendations = []
        for issue in issues:
            if issue["type"] == "high_response_time":
                recommendations.append("Optimize message processing logic")
            elif issue["type"] == "high_error_rate":
                recommendations.append("Implement better error handling")
            elif issue["type"] == "high_cpu_usage":
                recommendations.append("Optimize CPU-intensive operations")
            elif issue["type"] == "low_throughput":
                recommendations.append("Increase message processing capacity")
        
        analysis["recommendations"] = recommendations
        
        return analysis


class AlertManager:
    """Gerenciador de alertas do sistema"""
    
    def __init__(self):
        self.active_alerts: Dict[str, SystemAlert] = {}
        self.alert_history: deque = deque(maxlen=1000)
        self.alert_rules = {
            "agent_down": {"severity": "critical", "cooldown": 300},
            "high_error_rate": {"severity": "high", "cooldown": 180},
            "performance_degradation": {"severity": "medium", "cooldown": 120},
            "resource_exhaustion": {"severity": "high", "cooldown": 240}
        }
    
    def check_agent_alerts(self, metrics: AgentMetrics) -> List[SystemAlert]:
        """Verifica alertas para um agente"""
        alerts = []
        
        # Verificar se agente está down
        if metrics.status != "running":
            alert = self._create_alert(
                "agent_down",
                metrics.agent_id,
                f"Agent {metrics.agent_id} is not running (status: {metrics.status})",
                {"status": metrics.status, "last_activity": metrics.last_activity.isoformat()}
            )
            alerts.append(alert)
        
        # Verificar alta taxa de erro
        if metrics.error_rate > 0.1:  # 10%
            alert = self._create_alert(
                "high_error_rate",
                metrics.agent_id,
                f"High error rate detected: {metrics.error_rate:.2%}",
                {"error_rate": metrics.error_rate, "error_count": metrics.error_count}
            )
            alerts.append(alert)
        
        # Verificar degradação de performance
        if metrics.response_time_avg_ms > 2000:  # 2 segundos
            alert = self._create_alert(
                "performance_degradation",
                metrics.agent_id,
                f"Performance degradation: {metrics.response_time_avg_ms:.0f}ms avg response time",
                {"response_time_ms": metrics.response_time_avg_ms}
            )
            alerts.append(alert)
        
        # Verificar uso excessivo de recursos
        if metrics.memory_usage_mb > 1024:  # 1GB
            alert = self._create_alert(
                "resource_exhaustion",
                metrics.agent_id,
                f"High memory usage: {metrics.memory_usage_mb:.0f}MB",
                {"memory_usage_mb": metrics.memory_usage_mb}
            )
            alerts.append(alert)
        
        return alerts
    
    def _create_alert(self, alert_type: str, agent_id: str, message: str, details: Dict[str, Any]) -> SystemAlert:
        """Cria um novo alerta"""
        alert_id = f"{alert_type}_{agent_id}_{int(time.time())}"
        
        alert = SystemAlert(
            alert_id=alert_id,
            alert_type=alert_type,
            severity=self.alert_rules[alert_type]["severity"],
            agent_id=agent_id,
            message=message,
            details=details,
            triggered_at=datetime.now()
        )
        
        # Verificar cooldown
        cooldown = self.alert_rules[alert_type]["cooldown"]
        recent_alerts = [
            a for a in self.alert_history 
            if a.alert_type == alert_type and a.agent_id == agent_id
            and (datetime.now() - a.triggered_at).seconds < cooldown
        ]
        
        if not recent_alerts:
            self.active_alerts[alert_id] = alert
            self.alert_history.append(alert)
            logger.warning(f"🚨 ALERTA {alert.severity.upper()}: {alert.message}")
        
        return alert
    
    def resolve_alert(self, alert_id: str):
        """Resolve um alerta"""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.resolved_at = datetime.now()
            alert.is_resolved = True
            del self.active_alerts[alert_id]
            logger.info(f"✅ Alerta {alert_id} resolvido")
    
    def get_active_alerts(self) -> List[SystemAlert]:
        """Retorna alertas ativos"""
        return list(self.active_alerts.values())
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Retorna resumo dos alertas"""
        active_by_severity = defaultdict(int)
        for alert in self.active_alerts.values():
            active_by_severity[alert.severity] += 1
        
        return {
            "total_active": len(self.active_alerts),
            "by_severity": dict(active_by_severity),
            "total_history": len(self.alert_history),
            "last_24h": len([
                a for a in self.alert_history 
                if (datetime.now() - a.triggered_at).days < 1
            ])
        }


class SystemHealthMonitor:
    """Monitor de saúde do sistema"""
    
    def __init__(self):
        self.system_metrics = {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "disk_percent": 0.0,
            "network_io": {"bytes_sent": 0, "bytes_recv": 0},
            "process_count": 0,
            "uptime_seconds": 0
        }
        self.start_time = datetime.now()
    
    def collect_system_metrics(self) -> Dict[str, Any]:
        """Coleta métricas do sistema"""
        try:
            # CPU
            self.system_metrics["cpu_percent"] = psutil.cpu_percent(interval=1)
            
            # Memória
            memory = psutil.virtual_memory()
            self.system_metrics["memory_percent"] = memory.percent
            self.system_metrics["memory_available_mb"] = memory.available / (1024 * 1024)
            
            # Disco
            disk = psutil.disk_usage('/')
            self.system_metrics["disk_percent"] = disk.percent
            self.system_metrics["disk_free_gb"] = disk.free / (1024 * 1024 * 1024)
            
            # Rede
            net_io = psutil.net_io_counters()
            self.system_metrics["network_io"] = {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv
            }
            
            # Processos
            self.system_metrics["process_count"] = len(psutil.pids())
            
            # Uptime
            self.system_metrics["uptime_seconds"] = (datetime.now() - self.start_time).total_seconds()
            
        except Exception as e:
            logger.error(f"❌ Erro coletando métricas do sistema: {e}")
        
        return self.system_metrics.copy()
    
    def get_health_status(self) -> Dict[str, Any]:
        """Retorna status de saúde do sistema"""
        metrics = self.collect_system_metrics()
        
        # Determinar status geral
        health_issues = []
        
        if metrics["cpu_percent"] > 90:
            health_issues.append("High CPU usage")
        if metrics["memory_percent"] > 90:
            health_issues.append("High memory usage")
        if metrics["disk_percent"] > 95:
            health_issues.append("Low disk space")
        
        if not health_issues:
            overall_status = "healthy"
        elif len(health_issues) == 1:
            overall_status = "warning"
        else:
            overall_status = "critical"
        
        return {
            "overall_status": overall_status,
            "health_issues": health_issues,
            "system_metrics": metrics,
            "last_check": datetime.now().isoformat()
        }


class EnhancedMonitoringSystem:
    """Sistema de monitoramento avançado completo"""
    
    def __init__(self):
        self.performance_analyzer = PerformanceAnalyzer()
        self.alert_manager = AlertManager()
        self.health_monitor = SystemHealthMonitor()
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.monitoring_active = False
        self.monitoring_thread = None
    
    def start_monitoring(self):
        """Inicia monitoramento"""
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        logger.info("📊 Sistema de monitoramento avançado iniciado")
    
    def stop_monitoring(self):
        """Para monitoramento"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        logger.info("📊 Sistema de monitoramento parado")
    
    def _monitoring_loop(self):
        """Loop principal de monitoramento"""
        while self.monitoring_active:
            try:
                # Coletar métricas do sistema
                system_health = self.health_monitor.get_health_status()
                
                # Verificar alertas de sistema
                if system_health["overall_status"] != "healthy":
                    for issue in system_health["health_issues"]:
                        alert = self.alert_manager._create_alert(
                            "system_health",
                            "system",
                            f"System health issue: {issue}",
                            system_health["system_metrics"]
                        )
                
                # Analisar performance dos agentes
                for agent_id, metrics in self.agent_metrics.items():
                    analysis = self.performance_analyzer.analyze_agent_performance(metrics)
                    
                    # Verificar alertas do agente
                    alerts = self.alert_manager.check_agent_alerts(metrics)
                
                # Log resumo a cada 60 segundos
                if int(time.time()) % 60 == 0:
                    self._log_monitoring_summary()
                
            except Exception as e:
                logger.error(f"❌ Erro no loop de monitoramento: {e}")
            
            time.sleep(5)  # Verificar a cada 5 segundos
    
    def update_agent_metrics(self, agent_id: str, metrics_data: Dict[str, Any]):
        """Atualiza métricas de um agente"""
        try:
            metrics = AgentMetrics(
                agent_id=agent_id,
                agent_type=metrics_data.get("agent_type", "unknown"),
                status=metrics_data.get("status", "unknown"),
                uptime_seconds=metrics_data.get("uptime_seconds", 0),
                messages_processed=metrics_data.get("messages_processed", 0),
                messages_per_second=metrics_data.get("messages_per_second", 0.0),
                response_time_avg_ms=metrics_data.get("response_time_avg_ms", 0.0),
                error_count=metrics_data.get("error_count", 0),
                error_rate=metrics_data.get("error_rate", 0.0),
                cpu_usage_percent=metrics_data.get("cpu_usage_percent", 0.0),
                memory_usage_mb=metrics_data.get("memory_usage_mb", 0.0),
                last_activity=datetime.now(),
                capabilities_count=metrics_data.get("capabilities_count", 0),
                active_tasks=metrics_data.get("active_tasks", 0)
            )
            
            self.agent_metrics[agent_id] = metrics
            
        except Exception as e:
            logger.error(f"❌ Erro atualizando métricas do agente {agent_id}: {e}")
    
    def _log_monitoring_summary(self):
        """Log resumo do monitoramento"""
        system_health = self.health_monitor.get_health_status()
        alert_summary = self.alert_manager.get_alert_summary()
        
        logger.info("=" * 50)
        logger.info("📊 RESUMO DE MONITORAMENTO")
        logger.info("=" * 50)
        logger.info(f"🖥️ Sistema: {system_health['overall_status'].upper()}")
        logger.info(f"🤖 Agentes Monitorados: {len(self.agent_metrics)}")
        logger.info(f"🚨 Alertas Ativos: {alert_summary['total_active']}")
        
        if alert_summary['by_severity']:
            logger.info(f"   Por Severidade: {alert_summary['by_severity']}")
        
        # Top 3 agentes por performance
        if self.agent_metrics:
            performances = []
            for agent_id, metrics in self.agent_metrics.items():
                analysis = self.performance_analyzer.analyze_agent_performance(metrics)
                performances.append((agent_id, analysis["overall_score"]))
            
            performances.sort(key=lambda x: x[1], reverse=True)
            logger.info("🏆 Top 3 Agentes por Performance:")
            for i, (agent_id, score) in enumerate(performances[:3], 1):
                logger.info(f"   {i}. {agent_id}: {score:.1f}%")
        
        logger.info("=" * 50)
    
    def get_comprehensive_report(self) -> Dict[str, Any]:
        """Gera relatório abrangente do sistema"""
        system_health = self.health_monitor.get_health_status()
        alert_summary = self.alert_manager.get_alert_summary()
        
        # Análise de performance de todos os agentes
        agent_analyses = {}
        for agent_id, metrics in self.agent_metrics.items():
            agent_analyses[agent_id] = self.performance_analyzer.analyze_agent_performance(metrics)
        
        # Calcular métricas agregadas
        if self.agent_metrics:
            avg_response_time = statistics.mean([m.response_time_avg_ms for m in self.agent_metrics.values()])
            avg_error_rate = statistics.mean([m.error_rate for m in self.agent_metrics.values()])
            total_messages = sum([m.messages_processed for m in self.agent_metrics.values()])
        else:
            avg_response_time = 0
            avg_error_rate = 0
            total_messages = 0
        
        return {
            "report_timestamp": datetime.now().isoformat(),
            "system_health": system_health,
            "alert_summary": alert_summary,
            "agent_count": len(self.agent_metrics),
            "agent_analyses": agent_analyses,
            "aggregate_metrics": {
                "avg_response_time_ms": avg_response_time,
                "avg_error_rate": avg_error_rate,
                "total_messages_processed": total_messages
            },
            "active_alerts": [asdict(alert) for alert in self.alert_manager.get_active_alerts()]
        }


if __name__ == "__main__":
    # Teste do sistema de monitoramento
    monitoring = EnhancedMonitoringSystem()
    monitoring.start_monitoring()
    
    try:
        # Simular métricas de agentes
        for i in range(3):
            monitoring.update_agent_metrics(f"test_agent_{i}", {
                "agent_type": "test",
                "status": "running",
                "uptime_seconds": 300,
                "messages_processed": 100 + i * 50,
                "messages_per_second": 2.5,
                "response_time_avg_ms": 200 + i * 100,
                "error_count": i,
                "error_rate": i * 0.01,
                "cpu_usage_percent": 30 + i * 20,
                "memory_usage_mb": 128 + i * 64,
                "capabilities_count": 3,
                "active_tasks": i + 1
            })
        
        time.sleep(10)
        
        # Gerar relatório
        report = monitoring.get_comprehensive_report()
        print(json.dumps(report, indent=2, default=str))
        
    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
    finally:
        monitoring.stop_monitoring()

