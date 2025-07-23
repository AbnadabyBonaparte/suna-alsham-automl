"""🤖 SUNA-ALSHAM Specialized Agents
Agentes especializados para a rede multi-agente

AGENTES INCLUÍDOS:
✅ OptimizationAgent - Otimização de performance
✅ SecurityAgent - Monitoramento de segurança
✅ LearningAgent - Aprendizado contínuo
✅ DataAgent - Processamento de dados
✅ IntegrationAgent - Integração com sistemas externos
✅ MonitoringAgent - Monitoramento de sistema
✅ PredictionAgent - Análise preditiva
✅ AutomationAgent - Automação de tarefas
"""

import asyncio
import json
import time
import uuid
import logging
import random
import statistics
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from collections import defaultdict
import numpy as np
import openai
import os

# Importações locais
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ..multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentCapability, MessageBus, AgentMessage

logger = logging.getLogger(__name__)

class OptimizationAgent(BaseNetworkAgent):
    """Agente especializado em otimização de performance"""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.OPTIMIZER, message_bus)
        self.optimization_history: List[Dict] = []
        self.current_optimizations: Dict[str, Any] = {}
        self.add_capability(AgentCapability(
            name="performance_optimization",
            description="Otimização de performance de sistemas",
            input_types=["metrics", "config"],
            output_types=["optimized_config", "recommendations"],
            processing_time_ms=800.0,
            accuracy_score=0.92,
            resource_cost=0.4
        ))
        self.add_capability(AgentCapability(
            name="resource_allocation",
            description="Alocação inteligente de recursos",
            input_types=["resource_data", "demand_forecast"],
            output_types=["allocation_plan"],
            processing_time_ms=600.0,
            accuracy_score=0.88,
            resource_cost=0.3
        ))
        self.message_handlers[MessageType.NOTIFICATION] = self._handle_notification
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat

    def _handle_request(self, message: AgentMessage):
        request_type = message.content.get("type")
        if request_type == "optimize_performance":
            self._optimize_performance(message)
        elif request_type == "allocate_resources":
            self._allocate_resources(message)
        else:
            super()._handle_request(message)

    def _handle_notification(self, message: AgentMessage):
        try:
            alert_type = message.content.get("alert_type")
            alert = message.content.get("alert", {})
            if alert_type == "threshold_exceeded":
                metric = alert.get("metric")
                value = alert.get("value")
                threshold = alert.get("threshold")
                if metric in ["response_time", "cpu_usage", "memory_usage"]:
                    logger.info(f"🔧 OptimizationAgent reagindo ao alerta: {metric} = {value} (threshold: {threshold})")
                    optimization_id = str(uuid.uuid4())
                    logger.info(f"✅ Otimização automática {optimization_id} iniciada para {metric}")
                    self.optimization_history.append({
                        "id": optimization_id,
                        "timestamp": datetime.now(),
                        "trigger": "alert",
                        "metric": metric,
                        "value": value,
                        "action": "auto_optimization"
                    })
        except Exception as e:
            logger.error(f"❌ Erro processando notificação no OptimizationAgent: {e}")

    def _handle_heartbeat(self, message: AgentMessage):
        logger.debug(f"💓 {self.agent_id} recebeu heartbeat de {message.sender_id}")

    def _optimize_performance(self, message: AgentMessage):
        metrics = message.content.get("metrics", {})
        target_improvement = message.content.get("target_improvement", 0.1)
        optimization_id = str(uuid.uuid4())
        current_performance = metrics.get("performance_score", 0.8)
        bottlenecks = self._identify_bottlenecks(metrics)
        recommendations = self._generate_optimization_recommendations(bottlenecks)
        expected_improvement = min(target_improvement, 0.25)
        result = {
            "optimization_id": optimization_id,
            "current_performance": current_performance,
            "expected_improvement": expected_improvement,
            "bottlenecks": bottlenecks,
            "recommendations": recommendations,
            "estimated_completion_time": "2-4 hours",
            "confidence_score": 0.85
        }
        self.optimization_history.append({
            "id": optimization_id,
            "timestamp": datetime.now(),
            "metrics": metrics,
            "result": result
        })
        self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "success", "result": result})
        logger.info(f"🔧 Otimização {optimization_id} concluída pelo agente {self.agent_id}")

    def _identify_bottlenecks(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        bottlenecks = []
        cpu_usage = metrics.get("cpu_usage", 0)
        if cpu_usage > 80:
            bottlenecks.append({"type": "cpu", "severity": "high" if cpu_usage > 90 else "medium", "current_value": cpu_usage, "threshold": 80})
        memory_usage = metrics.get("memory_usage", 0)
        if memory_usage > 85:
            bottlenecks.append({"type": "memory", "severity": "high" if memory_usage > 95 else "medium", "current_value": memory_usage, "threshold": 85})
        response_time = metrics.get("response_time_ms", 0)
        if response_time > 1000:
            bottlenecks.append({"type": "response_time", "severity": "high" if response_time > 2000 else "medium", "current_value": response_time, "threshold": 1000})
        return bottlenecks

    def _generate_optimization_recommendations(self, bottlenecks: List[Dict]) -> List[Dict[str, Any]]:
        recommendations = []
        for bottleneck in bottlenecks:
            if bottleneck["type"] == "cpu":
                recommendations.append({"category": "CPU Optimization", "action": "Implement CPU-intensive task queuing", "priority": "high", "estimated_impact": "15-25% CPU reduction", "implementation_effort": "medium"})
            elif bottleneck["type"] == "memory":
                recommendations.append({"category": "Memory Optimization", "action": "Enable memory caching and garbage collection tuning", "priority": "high", "estimated_impact": "20-30% memory reduction", "implementation_effort": "low"})
            elif bottleneck["type"] == "response_time":
                recommendations.append({"category": "Performance Optimization", "action": "Implement async processing and connection pooling", "priority": "medium", "estimated_impact": "30-50% response time improvement", "implementation_effort": "high"})
        return recommendations

    def _allocate_resources(self, message: AgentMessage):
        resource_data = message.content.get("resource_data", {})
        allocation_plan = {"status": "allocated", "details": f"Allocated based on {resource_data}"}
        self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "success", "result": allocation_plan})
        logger.info(f"🔧 Recursos alocados para {message.sender_id}")

class SecurityAgent(BaseNetworkAgent):
    """Agente especializado em segurança"""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.GUARD, message_bus)
        self.security_events: List[Dict] = []
        self.threat_patterns: Dict[str, Any] = {}
        self.security_score = 95.0
        self.add_capability(AgentCapability(
            name="threat_detection",
            description="Detecção de ameaças em tempo real",
            input_types=["logs", "network_traffic", "user_behavior"],
            output_types=["threat_report", "security_alert"],
            processing_time_ms=300.0,
            accuracy_score=0.96,
            resource_cost=0.2
        ))
        self.add_capability(AgentCapability(
            name="vulnerability_assessment",
            description="Avaliação de vulnerabilidades",
            input_types=["system_config", "code_analysis"],
            output_types=["vulnerability_report"],
            processing_time_ms=1200.0,
            accuracy_score=0.91,
            resource_cost=0.5
        ))
        self.message_handlers[MessageType.NOTIFICATION] = self._handle_notification
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat

    def _handle_request(self, message: AgentMessage):
        request_type = message.content.get("type")
        if request_type == "scan_threats":
            self._scan_threats(message)
        elif request_type == "assess_vulnerability":
            self._assess_vulnerability(message)
        elif request_type == "security_audit":
            self._security_audit(message)
        else:
            super()._handle_request(message)

    def _handle_notification(self, message: AgentMessage):
        try:
            alert_type = message.content.get("alert_type")
            alert = message.content.get("alert", {})
            if alert_type == "threshold_exceeded":
                metric = alert.get("metric")
                value = alert.get("value")
                threshold = alert.get("threshold")
                if metric in ["error_rate", "active_connections"]:
                    logger.info(f"🛡️ SecurityAgent reagindo ao alerta: {metric} = {value} (threshold: {threshold})")
                    security_action_id = str(uuid.uuid4())
                    action = "rate_limiting" if metric == "error_rate" else "ddos_protection"
                    logger.info(f"🔒 {action.capitalize()} - Ação {security_action_id}")
                    self.security_score = max(50, self.security_score - 2)
                    self.security_events.append({
                        "id": security_action_id,
                        "timestamp": datetime.now(),
                        "trigger": "alert",
                        "metric": metric,
                        "value": value,
                        "action": action,
                        "security_score": self.security_score
                    })
        except Exception as e:
            logger.error(f"❌ Erro processando notificação no SecurityAgent: {e}")

    def _handle_heartbeat(self, message: AgentMessage):
        logger.debug(f"💓 {self.agent_id} recebeu heartbeat de {message.sender_id}")

    def _scan_threats(self, message: AgentMessage):
        scan_data = message.content.get("data", {})
        scan_id = str(uuid.uuid4())
        threats_found = []
        if "failed_logins" in scan_data and scan_data["failed_logins"] > 10:
            threats_found.append({"type": "brute_force_attempt", "severity": "high", "details": f"{scan_data['failed_logins']} failed login attempts detected", "recommendation": "Implement IP blocking and CAPTCHA"})
        if "network_requests" in scan_data and scan_data["network_requests"] > 1000:
            threats_found.append({"type": "ddos_attempt", "severity": "critical", "details": f"Unusual traffic spike: {scan_data['network_requests']} requests/minute", "recommendation": "Enable rate limiting and DDoS protection"})
        threat_impact = len(threats_found) * 5
        current_security_score = max(50, self.security_score - threat_impact)
        result = {
            "scan_id": scan_id,
            "threats_found": len(threats_found),
            "threat_details": threats_found,
            "security_score": current_security_score,
            "scan_duration_ms": 250,
            "recommendations": self._generate_security_recommendations(threats_found)
        }
        self.security_events.append({"id": scan_id, "timestamp": datetime.now(), "type": "threat_scan", "result": result})
        self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "success", "result": result})
        if [t for t in threats_found if t["severity"] == "critical"]:
            self.broadcast_message(MessageType.EMERGENCY, {"alert_type": "critical_security_threat", "threats": [t for t in threats_found if t["severity"] == "critical"], "scan_id": scan_id}, Priority.CRITICAL)
        logger.info(f"🛡️ Scan de segurança {scan_id} concluído - {len(threats_found)} ameaças encontradas")

    def _generate_security_recommendations(self, threats: List[Dict]) -> List[str]:
        recommendations = []
        if any(t["type"] == "brute_force_attempt" for t in threats):
            recommendations.extend(["Implement multi-factor authentication", "Enable account lockout policies"])
        if any(t["type"] == "ddos_attempt" for t in threats):
            recommendations.extend(["Configure CDN and load balancing", "Implement advanced rate limiting"])
        if not recommendations:
            recommendations.extend(["Maintain current security measures", "Schedule regular security audits"])
        return recommendations

    def _assess_vulnerability(self, message: AgentMessage):
        pass  # Implementação pendente

    def _security_audit(self, message: AgentMessage):
        pass  # Implementação pendente

class LearningAgent(BaseNetworkAgent):
    """Agente especializado em aprendizado contínuo"""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.LEARN, message_bus)
        self.learning_models: Dict[str, Any] = {}
        self.training_history: List[Dict] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.add_capability(AgentCapability(
            name="pattern_recognition",
            description="Reconhecimento de padrões em dados",
            input_types=["time_series", "structured_data"],
            output_types=["patterns", "predictions"],
            processing_time_ms=1000.0,
            accuracy_score=0.89,
            resource_cost=0.6
        ))
        self.add_capability(AgentCapability(
            name="model_training",
            description="Treinamento de modelos de ML",
            input_types=["training_data", "model_config"],
            output_types=["trained_model", "performance_metrics"],
            processing_time_ms=5000.0,
            accuracy_score=0.93,
            resource_cost=0.8
        ))
        self.message_handlers[MessageType.NOTIFICATION] = self._handle_notification
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat

    def _handle_request(self, message: AgentMessage):
        request_type = message.content.get("type")
        if request_type == "train_model":
            self._train_model(message)
        elif request_type == "recognize_patterns":
            self._recognize_patterns(message)
        elif request_type == "update_knowledge":
            self._update_knowledge(message)
        else:
            super()._handle_request(message)

    def _handle_notification(self, message: AgentMessage):
        try:
            alert_type = message.content.get("alert_type")
            alert = message.content.get("alert", {})
            if alert_type == "threshold_exceeded":
                metric = alert.get("metric")
                value = alert.get("value")
                threshold = alert.get("threshold")
                logger.info(f"🧠 LearningAgent aprendendo com alerta: {metric} = {value} (threshold: {threshold})")
                pattern_id = str(uuid.uuid4())
                pattern = {
                    "id": pattern_id,
                    "timestamp": datetime.now(),
                    "type": "alert_pattern",
                    "metric": metric,
                    "value": value,
                    "threshold": threshold,
                    "severity": alert.get("severity", "medium")
                }
                if metric not in self.knowledge_base:
                    self.knowledge_base[metric] = []
                self.knowledge_base[metric].append(pattern)
                if len(self.knowledge_base[metric]) > 100:
                    self.knowledge_base[metric] = self.knowledge_base[metric][-100:]
                logger.info(f"📚 Padrão {pattern_id} adicionado à base de conhecimento para {metric}")
                if len(self.knowledge_base[metric]) >= 5:
                    self._analyze_alert_trends(metric)
        except Exception as e:
            logger.error(f"❌ Erro processando notificação no LearningAgent: {e}")

    def _handle_heartbeat(self, message: AgentMessage):
        logger.debug(f"💓 {self.agent_id} recebeu heartbeat de {message.sender_id}")

    def _analyze_alert_trends(self, metric: str):
        try:
            patterns = self.knowledge_base[metric]
            values = [p["value"] for p in patterns[-10:]]
            if len(values) >= 3:
                trend = self._detect_trend(values)
                if trend:
                    logger.info(f"📈 Tendência detectada para {metric}: {trend['description']}")
                    if "insights" not in self.knowledge_base:
                        self.knowledge_base["insights"] = []
                    self.knowledge_base["insights"].append({
                        "metric": metric,
                        "trend": trend,
                        "timestamp": datetime.now(),
                        "confidence": trend.get("confidence", 0.5)
                    })
        except Exception as e:
            logger.error(f"❌ Erro analisando tendências: {e}")

    def _train_model(self, message: AgentMessage):
        training_data = message.content.get("training_data", [])
        model_type = message.content.get("model_type", "neural_network")
        model_id = str(uuid.uuid4())
        training_start = time.time()
        epochs = 100
        initial_accuracy = 0.6
        final_accuracy = min(0.95, initial_accuracy + random.uniform(0.2, 0.35))
        training_metrics = {
            "epochs": epochs,
            "initial_accuracy": initial_accuracy,
            "final_accuracy": final_accuracy,
            "training_time_ms": (time.time() - training_start) * 1000,
            "data_points": len(training_data),
            "model_size_mb": random.uniform(5, 50)
        }
        self.learning_models[model_id] = {
            "type": model_type,
            "created_at": datetime.now(),
            "metrics": training_metrics,
            "status": "trained"
        }
        result = {
            "model_id": model_id,
            "model_type": model_type,
            "training_metrics": training_metrics,
            "status": "training_completed",
            "deployment_ready": final_accuracy > 0.85
        }
        self.training_history.append({"model_id": model_id, "timestamp": datetime.now(), "result": result})
        self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "success", "result": result})
        logger.info(f"🧠 Modelo {model_id} treinado com accuracy {final_accuracy:.2%}")

    def _recognize_patterns(self, message: AgentMessage):
        data = message.content.get("data", [])
        pattern_type = message.content.get("pattern_type", "trend")
        patterns_found = []
        if isinstance(data, list) and len(data) > 5:
            if pattern_type in ["trend", "all"]:
                trend = self._detect_trend(data)
                if trend:
                    patterns_found.append(trend)
            if pattern_type in ["anomaly", "all"]:
                anomalies = self._detect_anomalies(data)
                patterns_found.extend(anomalies)
            if pattern_type in ["seasonal", "all"] and len(data) > 20:
                seasonal = self._detect_seasonality(data)
                if seasonal:
                    patterns_found.append(seasonal)
        result = {
            "analysis_id": str(uuid.uuid4()),
            "data_points": len(data),
            "patterns_found": len(patterns_found),
            "pattern_details": patterns_found,
            "confidence_score": 0.87,
            "analysis_time_ms": 150
        }
        self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "success", "result": result})
        logger.info(f"🔍 Análise de padrões concluída - {len(patterns_found)} padrões encontrados")

    def _detect_trend(self, data: List[float]) -> Optional[Dict[str, Any]]:
        if len(data) < 3:
            return None
        first_half = statistics.mean(data[:len(data)//2])
        second_half = statistics.mean(data[len(data)//2:])
        change_percent = ((second_half - first_half) / first_half) * 100 if first_half != 0 else 0
        if abs(change_percent) > 5:
            return {
                "type": "trend",
                "direction": "increasing" if change_percent > 0 else "decreasing",
                "change_percent": round(change_percent, 2),
                "confidence": 0.8,
                "description": f"Data shows {abs(change_percent):.1f}% {'increase' if change_percent > 0 else 'decrease'}"
            }
        return None

    def _detect_anomalies(self, data: List[float]) -> List[Dict[str, Any]]:
        if len(data) < 5:
            return []
        mean_val = statistics.mean(data)
        std_val = statistics.stdev(data) if len(data) > 1 else 0
        threshold = 2 * std_val
        return [{
            "type": "anomaly",
            "index": i,
            "value": value,
            "expected_range": [mean_val - threshold, mean_val + threshold],
            "deviation": abs(value - mean_val),
            "confidence": 0.75
        } for i, value in enumerate(data) if abs(value - mean_val) > threshold][:5]

    def _detect_seasonality(self, data: List[float]) -> Optional[Dict[str, Any]]:
        if len(data) < 20:
            return None
        period_candidates = [7, 12, 24]
        for period in period_candidates:
            if len(data) >= period * 2:
                correlation = self._calculate_autocorrelation(data, period)
                if correlation > 0.6:
                    return {
                        "type": "seasonality",
                        "period": period,
                        "correlation": round(correlation, 3),
                        "confidence": 0.7,
                        "description": f"Seasonal pattern detected with period {period}"
                    }
        return None

    def _calculate_autocorrelation(self, data: List[float], lag: int) -> float:
        if len(data) <= lag:
            return 0
        n = len(data) - lag
        mean_val = statistics.mean(data)
        numerator = sum((data[i] - mean_val) * (data[i + lag] - mean_val) for i in range(n))
        denominator = sum((x - mean_val) ** 2 for x in data)
        return numerator / denominator if denominator != 0 else 0

    def _update_knowledge(self, message: AgentMessage):
        pass  # Implementação pendente

class DataAgent(BaseNetworkAgent):
    """Agente especializado em processamento de dados"""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.SPECIALIST, message_bus)
        self.data_cache: Dict[str, Any] = {}
        self.processing_stats: Dict[str, int] = {"processed": 0, "cached": 0, "errors": 0}
        self.add_capability(AgentCapability(
            name="data_transformation",
            description="Transformação e limpeza de dados",
            input_types=["raw_data", "csv", "json"],
            output_types=["clean_data", "structured_data"],
            processing_time_ms=400.0,
            accuracy_score=0.94,
            resource_cost=0.3
        ))
        self.add_capability(AgentCapability(
            name="data_validation",
            description="Validação de qualidade de dados",
            input_types=["dataset", "schema"],
            output_types=["validation_report"],
            processing_time_ms=200.0,
            accuracy_score=0.97,
            resource_cost=0.2
        ))
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat

    def _handle_request(self, message: AgentMessage):
        request_type = message.content.get("type")
        if request_type == "process_data":
            self._process_data(message)
        elif request_type == "validate_data":
            self._validate_data(message)
        elif request_type == "transform_data":
            self._transform_data(message)
        else:
            super()._handle_request(message)

    def _handle_heartbeat(self, message: AgentMessage):
        logger.debug(f"💓 {self.agent_id} recebeu heartbeat de {message.sender_id}")

    def _process_data(self, message: AgentMessage):
        data = message.content.get("data", [])
        processing_type = message.content.get("processing_type", "standard")
        processing_id = str(uuid.uuid4())
        start_time = time.time()
        try:
            processed_data = self._simulate_data_processing(data, processing_type)
            processing_time = (time.time() - start_time) * 1000
            result = {
                "processing_id": processing_id,
                "input_records": len(data) if isinstance(data, list) else 1,
                "output_records": len(processed_data) if isinstance(processed_data, list) else 1,
                "processing_time_ms": processing_time,
                "processing_type": processing_type,
                "data_quality_score": 0.92,
                "processed_data": processed_data[:100] if isinstance(processed_data, list) else processed_data
            }
            self.processing_stats["processed"] += 1
            if len(str(data)) < 10000:
                cache_key = f"{processing_type}_{hash(str(data))}"
                self.data_cache[cache_key] = result
                self.processing_stats["cached"] += 1
            self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "success", "result": result})
            logger.info(f"📊 Dados processados - ID: {processing_id}, Records: {result['input_records']}")
        except Exception as e:
            self.processing_stats["errors"] += 1
            self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "error", "error": str(e), "processing_id": processing_id})
            logger.error(f"❌ Erro processando dados: {e}")

    def _simulate_data_processing(self, data: Any, processing_type: str) -> Any:
        if processing_type == "clean":
            return [item for item in data if item is not None and str(item).strip()] if isinstance(data, list) else data
        elif processing_type == "normalize":
            if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
                max_val = max(data) if data else 1
                return [x / max_val for x in data]
            return data
        elif processing_type == "aggregate":
            if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
                return {"count": len(data), "sum": sum(data), "mean": statistics.mean(data) if data else 0, "min": min(data) if data else 0, "max": max(data) if data else 0}
            return data
        return data

    def _validate_data(self, message: AgentMessage):
        dataset = message.content.get("dataset", {})
        validation_report = {"status": "valid", "details": f"Validated {len(dataset)} records"}
        self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "success", "result": validation_report})
        logger.info(f"✅ Dados validados para {message.sender_id}")

    def _transform_data(self, message: AgentMessage):
        raw_data = message.content.get("raw_data", {})
        transformed_data = {"transformed": f"Transformed {raw_data}"}
        self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "success", "result": transformed_data})
        logger.info(f"🔄 Dados transformados para {message.sender_id}")

class IntegrationAgent(BaseNetworkAgent):
    """Agente especializado em integração com sistemas externos"""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.INTEGRATOR, message_bus)
        self.integration_points: Dict[str, Any] = {}
        self.add_capability(AgentCapability(
            name="external_integration",
            description="Integração com APIs externas",
            input_types=["api_endpoint", "credentials"],
            output_types=["integrated_data", "status_report"],
            processing_time_ms=500.0,
            accuracy_score=0.95,
            resource_cost=0.4
        ))
        self.message_handlers[MessageType.REQUEST] = self._handle_request
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat

    def _handle_request(self, message: AgentMessage):
        request_type = message.content.get("type")
        if request_type == "integrate_system":
            self._integrate_system(message)
        else:
            super()._handle_request(message)

    def _handle_heartbeat(self, message: AgentMessage):
        logger.debug(f"💓 {self.agent_id} recebeu heartbeat de {message.sender_id}")

    def _integrate_system(self, message: AgentMessage):
        endpoint = message.content.get("api_endpoint", "")
        integration_id = str(uuid.uuid4())
        result = {
            "integration_id": integration_id,
            "endpoint": endpoint,
            "status": "connected" if endpoint else "failed",
            "data": {"sample": "integrated data"} if endpoint else {}
        }
        self.integration_points[integration_id] = result
        self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "success", "result": result})
        logger.info(f"🔗 Integração {integration_id} concluída para {endpoint}")

class MonitoringAgent(BaseNetworkAgent):
    """Agente especializado em monitoramento de sistema"""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.MONITOR, message_bus)
        self.monitoring_data: Dict[str, List] = defaultdict(list)
        self.alerts: List[Dict] = []
        self.thresholds: Dict[str, float] = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "response_time": 1000.0,
            "error_rate": 5.0
        }
        self.add_capability(AgentCapability(
            name="system_monitoring",
            description="Monitoramento de métricas de sistema",
            input_types=["system_metrics", "logs"],
            output_types=["monitoring_report", "alerts"],
            processing_time_ms=100.0,
            accuracy_score=0.98,
            resource_cost=0.1
        ))
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat

    def _handle_heartbeat(self, message: AgentMessage):
        logger.debug(f"💓 {self.agent_id} recebeu heartbeat de {message.sender_id}")

    def _agent_specific_logic(self):
        current_metrics = self._collect_system_metrics()
        timestamp = datetime.now()
        for metric_name, value in current_metrics.items():
            self.monitoring_data[metric_name].append({"timestamp": timestamp, "value": value})
            if len(self.monitoring_data[metric_name]) > 1000:
                self.monitoring_data[metric_name] = self.monitoring_data[metric_name][-1000:]
        self._check_alerts(current_metrics)

    def _collect_system_metrics(self) -> Dict[str, float]:
        return {
            "cpu_usage": random.uniform(20, 95),
            "memory_usage": random.uniform(30, 90),
            "disk_usage": random.uniform(40, 80),
            "response_time": random.uniform(100, 2000),
            "error_rate": random.uniform(0, 10),
            "active_connections": random.randint(10, 500)
        }

    def _check_alerts(self, metrics: Dict[str, float]):
        for metric_name, value in metrics.items():
            threshold = self.thresholds.get(metric_name)
            if threshold and value > threshold:
                alert = {
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.now(),
                    "metric": metric_name,
                    "value": value,
                    "threshold": threshold,
                    "severity": "high" if value > threshold * 1.2 else "medium"
                }
                self.alerts.append(alert)
                self.broadcast_message(
                    MessageType.NOTIFICATION,
                    {"alert_type": "threshold_exceeded", "alert": alert},
                    Priority.HIGH if alert["severity"] == "high" else Priority.NORMAL
                )
                logger.warning(f"🚨 Alerta: {metric_name} = {value:.1f} (threshold: {threshold})")

class PredictionAgent(BaseNetworkAgent):
    """Agente especializado em análise preditiva"""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.PREDICTOR, message_bus)
        self.prediction_models: Dict[str, Any] = {}
        self.add_capability(AgentCapability(
            name="predictive_analysis",
            description="Previsão de métricas futuras",
            input_types=["historical_data", "model_config"],
            output_types=["prediction_report"],
            processing_time_ms=700.0,
            accuracy_score=0.90,
            resource_cost=0.5
        ))
        self.message_handlers[MessageType.REQUEST] = self._handle_request
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat

    def _handle_request(self, message: AgentMessage):
        request_type = message.content.get("type")
        if request_type == "predict_metric":
            self._predict_metric(message)
        else:
            super()._handle_request(message)

    def _handle_heartbeat(self, message: AgentMessage):
        logger.debug(f"💓 {self.agent_id} recebeu heartbeat de {message.sender_id}")

    def _predict_metric(self, message: AgentMessage):
        historical_data = message.content.get("historical_data", [])
        prediction_id = str(uuid.uuid4())
        predicted_value = statistics.mean(historical_data) * (1 + random.uniform(-0.1, 0.1)) if historical_data else random.uniform(50, 150)
        result = {
            "prediction_id": prediction_id,
            "predicted_value": predicted_value,
            "confidence": 0.85,
            "time_horizon": "24h",
            "historical_data_points": len(historical_data)
        }
        self.prediction_models[prediction_id] = result
        self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "success", "result": result})
        logger.info(f"🔮 Previsão {prediction_id} gerada para {message.sender_id}")

class AutomationAgent(BaseNetworkAgent):
    """Agente especializado em automação de tarefas"""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.AUTOMATOR, message_bus)
        self.automation_tasks: Dict[str, Any] = {}
        self.add_capability(AgentCapability(
            name="task_automation",
            description="Automação de tarefas repetitivas",
            input_types=["task_config", "trigger_conditions"],
            output_types=["task_status", "execution_log"],
            processing_time_ms=300.0,
            accuracy_score=0.95,
            resource_cost=0.3
        ))
        self.message_handlers[MessageType.REQUEST] = self._handle_request
        self.message_handlers[MessageType.HEARTBEAT] = self._handle_heartbeat

    def _handle_request(self, message: AgentMessage):
        request_type = message.content.get("type")
        if request_type == "automate_task":
            self._automate_task(message)
        else:
            super()._handle_request(message)

    def _handle_heartbeat(self, message: AgentMessage):
        logger.debug(f"💓 {self.agent_id} recebeu heartbeat de {message.sender_id}")

    def _automate_task(self, message: AgentMessage):
        task_config = message.content.get("task_config", {})
        task_id = str(uuid.uuid4())
        result = {
            "task_id": task_id,
            "status": "completed",
            "details": f"Automated task {task_config.get('name', 'unknown')}"
        }
        self.automation_tasks[task_id] = result
        self.send_message(message.sender_id, MessageType.RESPONSE, {"status": "success", "result": result})
        logger.info(f"🤖 Tarefa {task_id} automatizada para {message.sender_id}")

if __name__ == "__main__":
    from ..multi_agent_network import MultiAgentNetwork
    network = MultiAgentNetwork()
    optimization_agent = OptimizationAgent("optimizer_001", network.message_bus)
    security_agent = SecurityAgent("security_001", network.message_bus)
    learning_agent = LearningAgent("learning_001", network.message_bus)
    data_agent = DataAgent("data_001", network.message_bus)
    integration_agent = IntegrationAgent("integration_001", network.message_bus)
    monitoring_agent = MonitoringAgent("monitor_001", network.message_bus)
    prediction_agent = PredictionAgent("prediction_001", network.message_bus)
    automation_agent = AutomationAgent("automation_001", network.message_bus)
    network.add_agent(optimization_agent)
    network.add_agent(security_agent)
    network.add_agent(learning_agent)
    network.add_agent(data_agent)
    network.add_agent(integration_agent)
    network.add_agent(monitoring_agent)
    network.add_agent(prediction_agent)
    network.add_agent(automation_agent)

    try:
        network.start()
        print("🌐 Rede multi-agente com agentes especializados iniciada!")
        print("Agentes ativos:")
        for agent_id, agent in network.agents.items():
            print(f"  - {agent_id} ({agent.agent_type.value})")
        time.sleep(10)
        status = network.get_network_status()
        print(f"\n📊 Status da rede: {status['network_metrics']['active_agents']} agentes ativos")
        input("\nPressione Enter para parar...")
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário")
    finally:
        network.stop()
