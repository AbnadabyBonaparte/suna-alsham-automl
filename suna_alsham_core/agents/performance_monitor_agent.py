import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import psutil
import time
from dataclasses import dataclass
from enum import Enum

# Assuming these imports exist in your system
from ..core.base_agent import BaseAgent
from ..core.agent_types import AgentType
from ..core.message import Message, MessageType

@dataclass
class PerformanceMetrics:
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, int]
    active_agents: int
    response_times: List[float]

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class PerformanceMonitorAgent(BaseAgent):
    def __init__(self, agent_id: str = "performance_monitor"):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.MONITOR,
            capabilities=["system_monitoring", "performance_analysis", "alerting"]
        )
        self.metrics_history: List[PerformanceMetrics] = []
        # Permite configuração dos thresholds via env ou parâmetros
        import os
        self.alert_thresholds = {
            'cpu_critical': float(os.environ.get('PERF_CPU_CRITICAL', 90.0)),
            'cpu_warning': float(os.environ.get('PERF_CPU_WARNING', 75.0)),
            'memory_critical': float(os.environ.get('PERF_MEM_CRITICAL', 85.0)),
            'memory_warning': float(os.environ.get('PERF_MEM_WARNING', 70.0)),
            'response_time_critical': float(os.environ.get('PERF_RESP_CRITICAL', 5000)),
            'response_time_warning': float(os.environ.get('PERF_RESP_WARNING', 2000))
        }
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.active_alerts: List[Dict[str, Any]] = []  # Armazena alertas ativos
        self.alert_callback = None  # Callback customizável para integração externa

    def get_capabilities(self) -> List[str]:
        """Implementação obrigatória do método abstrato get_capabilities"""
        return [
            "system_monitoring",
            "performance_analysis",
            "resource_tracking",
            "bottleneck_detection",
            "optimization_recommendations"
        ]

    async def initialize(self) -> bool:
        """Initialize the performance monitoring system"""
        try:
            self.logger.info("Initializing Performance Monitor Agent")
            # Start background monitoring task
            asyncio.create_task(self._continuous_monitoring())
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize: {e}")
            return False

    async def process_message(self, message: Message) -> Message:
        """Process incoming messages for performance queries"""
        try:
            if message.type == MessageType.QUERY:
                if "performance" in message.content.lower():
                    metrics = await self._collect_current_metrics()
                    return Message(
                        message_type=MessageType.RESPONSE,
                        sender_id=self.agent_id,
                        recipient_id=message.sender_id,
                        content=self._format_metrics_report(metrics)
                    )
                elif "alerts" in message.content.lower():
                    alerts = await self._get_active_alerts()
                    return Message(
                        message_type=MessageType.RESPONSE,
                        sender_id=self.agent_id,
                        recipient_id=message.sender_id,
                        content={"active_alerts": alerts}
                    )
            
            return await super().process_message(message)
        
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return Message(
                message_type=MessageType.ERROR,
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                content=f"Processing error: {str(e)}"
            )

    async def _continuous_monitoring(self):
        """Background task for continuous system monitoring"""
        while True:
            try:
                metrics = await self._collect_current_metrics()
                self.metrics_history.append(metrics)
                
                # Keep only last 1000 metrics
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]
                
                # Check for alerts
                await self._check_alerts(metrics)
                
                # Wait 30 seconds before next collection
                await asyncio.sleep(30)
                
            except Exception as e:
                self.logger.error(f"Error in continuous monitoring: {e}")
                await asyncio.sleep(60)  # Wait longer on error

    async def _collect_current_metrics(self) -> PerformanceMetrics:
        """Collect current system performance metrics"""
        try:
            # System metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # Agent-specific metrics (placeholder - integrate with your agent system)
            active_agents = await self._count_active_agents()
            response_times = await self._get_recent_response_times()
            
            return PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=(disk.used / disk.total) * 100,
                network_io={
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv
                },
                active_agents=active_agents,
                response_times=response_times
            )
        except Exception as e:
            self.logger.error(f"Error collecting metrics: {e}")
            return PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                network_io={},
                active_agents=0,
                response_times=[]
            )

    async def _count_active_agents(self) -> int:
        """Count currently active agents in the system"""
        # This should integrate with your agent registry/orchestrator
        # Placeholder implementation
        return len(self.metrics_history)  # Temporary

    async def _get_recent_response_times(self) -> List[float]:
        """Get recent response times from agents"""
        # This should integrate with your message routing system
        # Placeholder implementation
        return [100.0, 150.0, 200.0]  # Temporary

    async def _check_alerts(self, metrics: PerformanceMetrics):
        """Check metrics against thresholds and generate alerts. Mantém lista de alertas ativos."""
        alerts = []
        # CPU alerts
        if metrics.cpu_usage >= self.alert_thresholds['cpu_critical']:
            alerts.append(self._create_alert(AlertLevel.CRITICAL, f"CPU usage critical: {metrics.cpu_usage}%"))
        elif metrics.cpu_usage >= self.alert_thresholds['cpu_warning']:
            alerts.append(self._create_alert(AlertLevel.WARNING, f"CPU usage high: {metrics.cpu_usage}%"))
        # Memory alerts
        if metrics.memory_usage >= self.alert_thresholds['memory_critical']:
            alerts.append(self._create_alert(AlertLevel.CRITICAL, f"Memory usage critical: {metrics.memory_usage}%"))
        elif metrics.memory_usage >= self.alert_thresholds['memory_warning']:
            alerts.append(self._create_alert(AlertLevel.WARNING, f"Memory usage high: {metrics.memory_usage}%"))
        # Response time alerts
        if metrics.response_times:
            avg_response = sum(metrics.response_times) / len(metrics.response_times)
            if avg_response >= self.alert_thresholds['response_time_critical']:
                alerts.append(self._create_alert(AlertLevel.CRITICAL, f"Response time critical: {avg_response}ms"))
            elif avg_response >= self.alert_thresholds['response_time_warning']:
                alerts.append(self._create_alert(AlertLevel.WARNING, f"Response time high: {avg_response}ms"))
        # Atualiza lista de alertas ativos (mantém só os últimos 100)
        if alerts:
            self.active_alerts.extend(alerts)
            self.active_alerts = self.active_alerts[-100:]
        # Envia alertas (callback externo se definido)
        for alert in alerts:
            await self._send_alert(alert)

    def _create_alert(self, level: AlertLevel, message: str) -> Dict[str, Any]:
        """Create an alert dictionary"""
        return {
            'level': level.value,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'source': self.agent_id
        }

    async def _send_alert(self, alert: Dict[str, Any]):
        """Send alert to appropriate handlers. Suporta callback externo."""
        self.logger.warning(f"ALERT [{alert['level'].upper()}]: {alert['message']}")
        if self.alert_callback:
            try:
                await self.alert_callback(alert)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {e}")

    async def _get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get currently active alerts (últimos 100)."""
        return list(self.active_alerts)

    def _format_metrics_report(self, metrics: PerformanceMetrics) -> Dict[str, Any]:
        """Format metrics into a readable report"""
        return {
            'timestamp': metrics.timestamp.isoformat(),
            'system_performance': {
                'cpu_usage_percent': metrics.cpu_usage,
                'memory_usage_percent': metrics.memory_usage,
                'disk_usage_percent': metrics.disk_usage
            },
            'network': metrics.network_io,
            'agents': {
                'active_count': metrics.active_agents,
                'avg_response_time_ms': sum(metrics.response_times) / len(metrics.response_times) if metrics.response_times else 0
            }
        }

def create_agents(alert_callback=None) -> List[BaseAgent]:
    """
    Factory function to create performance monitoring agents.
    Permite passar callback para integração de alertas externos.
    """
    agents = [
        PerformanceMonitorAgent("performance_monitor_main"),
        PerformanceMonitorAgent("performance_monitor_backup")
    ]
    if alert_callback:
        for agent in agents:
            agent.alert_callback = alert_callback
    return agents
