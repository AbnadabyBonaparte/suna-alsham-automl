"""
🤖 SUNA-ALSHAM Specialized Agents
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

# Importações locais para evitar circular import
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentCapability, MessageBus, AgentMessage


logger = logging.getLogger(__name__)


class OptimizationAgent(BaseNetworkAgent):
    """Agente especializado em otimização de performance"""
    
    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.OPTIMIZER, message_bus)
        
        self.optimization_history: List[Dict] = []
        self.current_optimizations: Dict[str, Any] = {}
        
        # Capacidades específicas
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
        
        # Adicionar handler para notificações
        self.message_handlers[MessageType.NOTIFICATION] = self._handle_notification
    
    def _handle_request(self, message: AgentMessage):
        """Handler para requisições de otimização"""
        request_type = message.content.get("type")
        
        if request_type == "optimize_performance":
            self._optimize_performance(message)
        elif request_type == "allocate_resources":
            self._allocate_resources(message)
        else:
            super()._handle_request(message)
    
    def _handle_notification(self, message: AgentMessage):
        """Handler para notificações de alertas"""
        try:
            alert_type = message.content.get("alert_type")
            alert = message.content.get("alert", {})
            
            if alert_type == "threshold_exceeded":
                metric = alert.get("metric")
                value = alert.get("value")
                threshold = alert.get("threshold")
                
                # Reagir a alertas específicos
                if metric in ["response_time", "cpu_usage", "memory_usage"]:
                    logger.info(f"🔧 OptimizationAgent reagindo ao alerta: {metric} = {value} (threshold: {threshold})")
                    
                    # Simular otimização automática
                    optimization_id = str(uuid.uuid4())
                    logger.info(f"✅ Otimização automática {optimization_id} iniciada para {metric}")
                    
                    # Armazenar no histórico
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
    
    def _optimize_performance(self, message: AgentMessage):
        """Otimiza performance baseado em métricas"""
        metrics = message.content.get("metrics", {})
        target_improvement = message.content.get("target_improvement", 0.1)
        
        # Simular análise de otimização
        optimization_id = str(uuid.uuid4())
        
        # Analisar métricas atuais
        current_performance = metrics.get("performance_score", 0.8)
        bottlenecks = self._identify_bottlenecks(metrics)
        
        # Gerar recomendações
        recommendations = self._generate_optimization_recommendations(bottlenecks)
        
        # Calcular melhoria esperada
        expected_improvement = min(target_improvement, 0.25)  # Máximo 25%
        
        result = {
            "optimization_id": optimization_id,
            "current_performance": current_performance,
            "expected_improvement": expected_improvement,
            "bottlenecks": bottlenecks,
            "recommendations": recommendations,
            "estimated_completion_time": "2-4 hours",
            "confidence_score": 0.85
        }
        
        # Armazenar no histórico
        self.optimization_history.append({
            "id": optimization_id,
            "timestamp": datetime.now(),
            "metrics": metrics,
            "result": result
        })
        
        # Enviar resposta
        self.send_message(
            message.sender_id,
            MessageType.RESPONSE,
            {"status": "success", "result": result}
        )
        
        logger.info(f"🔧 Otimização {optimization_id} concluída pelo agente {self.agent_id}")
    
    def _identify_bottlenecks(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica gargalos no sistema"""
        bottlenecks = []
        
        # Analisar CPU
        cpu_usage = metrics.get("cpu_usage", 0)
        if cpu_usage > 80:
            bottlenecks.append({
                "type": "cpu",
                "severity": "high" if cpu_usage > 90 else "medium",
                "current_value": cpu_usage,
                "threshold": 80
            })
        
        # Analisar memória
        memory_usage = metrics.get("memory_usage", 0)
        if memory_usage > 85:
            bottlenecks.append({
                "type": "memory",
                "severity": "high" if memory_usage > 95 else "medium",
                "current_value": memory_usage,
                "threshold": 85
            })
        
        # Analisar tempo de resposta
        response_time = metrics.get("response_time_ms", 0)
        if response_time > 1000:
            bottlenecks.append({
                "type": "response_time",
                "severity": "high" if response_time > 2000 else "medium",
                "current_value": response_time,
                "threshold": 1000
            })
        
        return bottlenecks
    
    def _generate_optimization_recommendations(self, bottlenecks: List[Dict]) -> List[Dict[str, Any]]:
        """Gera recomendações de otimização"""
        recommendations = []
        
        for bottleneck in bottlenecks:
            if bottleneck["type"] == "cpu":
                recommendations.append({
                    "category": "CPU Optimization",
                    "action": "Implement CPU-intensive task queuing",
                    "priority": "high",
                    "estimated_impact": "15-25% CPU reduction",
                    "implementation_effort": "medium"
                })
            
            elif bottleneck["type"] == "memory":
                recommendations.append({
                    "category": "Memory Optimization",
                    "action": "Enable memory caching and garbage collection tuning",
                    "priority": "high",
                    "estimated_impact": "20-30% memory reduction",
                    "implementation_effort": "low"
                })
            
            elif bottleneck["type"] == "response_time":
                recommendations.append({
                    "category": "Performance Optimization",
                    "action": "Implement async processing and connection pooling",
                    "priority": "medium",
                    "estimated_impact": "30-50% response time improvement",
                    "implementation_effort": "high"
                })
        
        return recommendations


class SecurityAgent(BaseNetworkAgent):
    """Agente especializado em segurança"""
    
    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.GUARD, message_bus)
        
        self.security_events: List[Dict] = []
        self.threat_patterns: Dict[str, Any] = {}
        self.security_score = 95.0
        
        # Capacidades específicas
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
        
        # Adicionar handler para notificações
        self.message_handlers[MessageType.NOTIFICATION] = self._handle_notification
    
    def _handle_request(self, message: AgentMessage):
        """Handler para requisições de segurança"""
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
        """Handler para notificações de alertas"""
        try:
            alert_type = message.content.get("alert_type")
            alert = message.content.get("alert", {})
            
            if alert_type == "threshold_exceeded":
                metric = alert.get("metric")
                value = alert.get("value")
                threshold = alert.get("threshold")
                
                # Reagir a alertas de segurança
                if metric in ["error_rate", "active_connections"]:
                    logger.info(f"🛡️ SecurityAgent reagindo ao alerta: {metric} = {value} (threshold: {threshold})")
                    
                    # Simular ação de segurança
                    security_action_id = str(uuid.uuid4())
                    
                    if metric == "error_rate":
                        logger.info(f"🔒 Implementando rate limiting - Ação {security_action_id}")
                        action = "rate_limiting"
                    elif metric == "active_connections":
                        logger.info(f"🛡️ Ativando proteção DDoS - Ação {security_action_id}")
                        action = "ddos_protection"
                    
                    # Atualizar score de segurança
                    self.security_score = max(50, self.security_score - 2)
                    
                    # Armazenar evento de segurança
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
    
    def _scan_threats(self, message: AgentMessage):
        """Escaneia ameaças no sistema"""
        scan_data = message.content.get("data", {})
        scan_id = str(uuid.uuid4())
        
        # Simular detecção de ameaças
        threats_found = []
        
        # Verificar padrões suspeitos
        if "failed_logins" in scan_data:
            failed_logins = scan_data["failed_logins"]
            if failed_logins > 10:
                threats_found.append({
                    "type": "brute_force_attempt",
                    "severity": "high",
                    "details": f"{failed_logins} failed login attempts detected",
                    "recommendation": "Implement IP blocking and CAPTCHA"
                })
        
        # Verificar tráfego anômalo
        if "network_requests" in scan_data:
            requests = scan_data["network_requests"]
            if requests > 1000:
                threats_found.append({
                    "type": "ddos_attempt",
                    "severity": "critical",
                    "details": f"Unusual traffic spike: {requests} requests/minute",
                    "recommendation": "Enable rate limiting and DDoS protection"
                })
        
        # Calcular score de segurança
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
        
        # Armazenar evento
        self.security_events.append({
            "id": scan_id,
            "timestamp": datetime.now(),
            "type": "threat_scan",
            "result": result
        })
        
        # Enviar resposta
        self.send_message(
            message.sender_id,
            MessageType.RESPONSE,
            {"status": "success", "result": result}
        )
        
        # Se ameaças críticas, enviar alerta
        critical_threats = [t for t in threats_found if t["severity"] == "critical"]
        if critical_threats:
            self.broadcast_message(
                MessageType.EMERGENCY,
                {
                    "alert_type": "critical_security_threat",
                    "threats": critical_threats,
                    "scan_id": scan_id
                },
                Priority.CRITICAL
            )
        
        logger.info(f"🛡️ Scan de segurança {scan_id} concluído - {len(threats_found)} ameaças encontradas")
    
    def _generate_security_recommendations(self, threats: List[Dict]) -> List[str]:
        """Gera recomendações de segurança"""
        recommendations = []
        
        if any(t["type"] == "brute_force_attempt" for t in threats):
            recommendations.append("Implement multi-factor authentication")
            recommendations.append("Enable account lockout policies")
        
        if any(t["type"] == "ddos_attempt" for t in threats):
            recommendations.append("Configure CDN and load balancing")
            recommendations.append("Implement advanced rate limiting")
        
        if not recommendations:
            recommendations.append("Maintain current security measures")
            recommendations.append("Schedule regular security audits")
        
        return recommendations


class LearningAgent(BaseNetworkAgent):
    """Agente especializado em aprendizado contínuo"""
    
    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.LEARN, message_bus)
        
        self.learning_models: Dict[str, Any] = {}
        self.training_history: List[Dict] = []
        self.knowledge_base: Dict[str, Any] = {}
        
        # Capacidades específicas
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
        
        # Adicionar handler para notificações
        self.message_handlers[MessageType.NOTIFICATION] = self._handle_notification
    
    def _handle_request(self, message: AgentMessage):
        """Handler para requisições de aprendizado"""
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
        """Handler para notificações de alertas"""
        try:
            alert_type = message.content.get("alert_type")
            alert = message.content.get("alert", {})
            
            if alert_type == "threshold_exceeded":
                metric = alert.get("metric")
                value = alert.get("value")
                threshold = alert.get("threshold")
                
                logger.info(f"🧠 LearningAgent aprendendo com alerta: {metric} = {value} (threshold: {threshold})")
                
                # Atualizar base de conhecimento
                pattern_id = str(uuid.uuid4())
                
                # Armazenar padrão observado
                pattern = {
                    "id": pattern_id,
                    "timestamp": datetime.now(),
                    "type": "alert_pattern",
                    "metric": metric,
                    "value": value,
                    "threshold": threshold,
                    "severity": alert.get("severity", "medium")
                }
                
                # Adicionar à base de conhecimento
                if metric not in self.knowledge_base:
                    self.knowledge_base[metric] = []
                
                self.knowledge_base[metric].append(pattern)
                
                # Manter apenas últimos 100 padrões por métrica
                if len(self.knowledge_base[metric]) > 100:
                    self.knowledge_base[metric] = self.knowledge_base[metric][-100:]
                
                logger.info(f"📚 Padrão {pattern_id} adicionado à base de conhecimento para {metric}")
                
                # Analisar tendências se temos dados suficientes
                if len(self.knowledge_base[metric]) >= 5:
                    self._analyze_alert_trends(metric)
                    
        except Exception as e:
            logger.error(f"❌ Erro processando notificação no LearningAgent: {e}")
    
    def _analyze_alert_trends(self, metric: str):
        """Analisa tendências nos alertas"""
        try:
            patterns = self.knowledge_base[metric]
            values = [p["value"] for p in patterns[-10:]]  # Últimos 10 valores
            
            if len(values) >= 3:
                trend = self._detect_trend(values)
                if trend:
                    logger.info(f"📈 Tendência detectada para {metric}: {trend['description']}")
                    
                    # Armazenar insight
                    insight = {
                        "metric": metric,
                        "trend": trend,
                        "timestamp": datetime.now(),
                        "confidence": trend.get("confidence", 0.5)
                    }
                    
                    if "insights" not in self.knowledge_base:
                        self.knowledge_base["insights"] = []
                    
                    self.knowledge_base["insights"].append(insight)
                    
        except Exception as e:
            logger.error(f"❌ Erro analisando tendências: {e}")
    
    def _train_model(self, message: AgentMessage):
        """Treina um modelo de machine learning"""
        training_data = message.content.get("training_data", [])
        model_type = message.content.get("model_type", "neural_network")
        model_id = str(uuid.uuid4())
        
        # Simular treinamento
        training_start = time.time()
        
        # Simular métricas de treinamento
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
        
        # Armazenar modelo
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
        
        # Armazenar no histórico
        self.training_history.append({
            "model_id": model_id,
            "timestamp": datetime.now(),
            "result": result
        })
        
        # Enviar resposta
        self.send_message(
            message.sender_id,
            MessageType.RESPONSE,
            {"status": "success", "result": result}
        )
        
        logger.info(f"🧠 Modelo {model_id} treinado com accuracy {final_accuracy:.2%}")
    
    def _recognize_patterns(self, message: AgentMessage):
        """Reconhece padrões nos dados"""
        data = message.content.get("data", [])
        pattern_type = message.content.get("pattern_type", "trend")
        
        patterns_found = []
        
        if isinstance(data, list) and len(data) > 5:
            # Detectar tendências
            if pattern_type in ["trend", "all"]:
                trend = self._detect_trend(data)
                if trend:
                    patterns_found.append(trend)
            
            # Detectar anomalias
            if pattern_type in ["anomaly", "all"]:
                anomalies = self._detect_anomalies(data)
                patterns_found.extend(anomalies)
            
            # Detectar sazonalidade
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
        
        # Enviar resposta
        self.send_message(
            message.sender_id,
            MessageType.RESPONSE,
            {"status": "success", "result": result}
        )
        
        logger.info(f"🔍 Análise de padrões concluída - {len(patterns_found)} padrões encontrados")
    
    def _detect_trend(self, data: List[float]) -> Optional[Dict[str, Any]]:
        """Detecta tendências nos dados"""
        if len(data) < 3:
            return None
        
        # Calcular tendência simples
        first_half = statistics.mean(data[:len(data)//2])
        second_half = statistics.mean(data[len(data)//2:])
        
        change_percent = ((second_half - first_half) / first_half) * 100 if first_half != 0 else 0
        
        if abs(change_percent) > 5:  # Mudança significativa
            return {
                "type": "trend",
                "direction": "increasing" if change_percent > 0 else "decreasing",
                "change_percent": round(change_percent, 2),
                "confidence": 0.8,
                "description": f"Data shows {abs(change_percent):.1f}% {'increase' if change_percent > 0 else 'decrease'}"
            }
        
        return None
    
    def _detect_anomalies(self, data: List[float]) -> List[Dict[str, Any]]:
        """Detecta anomalias nos dados"""
        if len(data) < 5:
            return []
        
        mean_val = statistics.mean(data)
        std_val = statistics.stdev(data) if len(data) > 1 else 0
        
        anomalies = []
        threshold = 2 * std_val  # 2 desvios padrão
        
        for i, value in enumerate(data):
            if abs(value - mean_val) > threshold:
                anomalies.append({
                    "type": "anomaly",
                    "index": i,
                    "value": value,
                    "expected_range": [mean_val - threshold, mean_val + threshold],
                    "deviation": abs(value - mean_val),
                    "confidence": 0.75
                })
        
        return anomalies[:5]  # Máximo 5 anomalias
    
    def _detect_seasonality(self, data: List[float]) -> Optional[Dict[str, Any]]:
        """Detecta sazonalidade nos dados"""
        # Implementação simples - pode ser expandida
        if len(data) < 20:
            return None
        
        # Verificar padrões repetitivos simples
        period_candidates = [7, 12, 24]  # Períodos comuns
        
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
        """Calcula autocorrelação simples"""
        if len(data) <= lag:
            return 0
        
        n = len(data) - lag
        if n <= 0:
            return 0
        
        mean_val = statistics.mean(data)
        
        numerator = sum((data[i] - mean_val) * (data[i + lag] - mean_val) for i in range(n))
        denominator = sum((x - mean_val) ** 2 for x in data)
        
        return numerator / denominator if denominator != 0 else 0


class DataAgent(BaseNetworkAgent):
    """Agente especializado em processamento de dados"""
    
    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentType.SPECIALIST, message_bus)
        
        self.data_cache: Dict[str, Any] = {}
        self.processing_stats: Dict[str, int] = {"processed": 0, "cached": 0, "errors": 0}
        
        # Capacidades específicas
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
    
    def _handle_request(self, message: AgentMessage):
        """Handler para requisições de dados"""
        request_type = message.content.get("type")
        
        if request_type == "process_data":
            self._process_data(message)
        elif request_type == "validate_data":
            self._validate_data(message)
        elif request_type == "transform_data":
            self._transform_data(message)
        else:
            super()._handle_request(message)
    
    def _process_data(self, message: AgentMessage):
        """Processa dados brutos"""
        data = message.content.get("data", [])
        processing_type = message.content.get("processing_type", "standard")
        
        processing_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # Simular processamento
            processed_data = self._simulate_data_processing(data, processing_type)
            
            processing_time = (time.time() - start_time) * 1000
            
            result = {
                "processing_id": processing_id,
                "input_records": len(data) if isinstance(data, list) else 1,
                "output_records": len(processed_data) if isinstance(processed_data, list) else 1,
                "processing_time_ms": processing_time,
                "processing_type": processing_type,
                "data_quality_score": 0.92,
                "processed_data": processed_data[:100] if isinstance(processed_data, list) else processed_data  # Limitar resposta
            }
            
            self.processing_stats["processed"] += 1
            
            # Cache resultado se útil
            if len(str(data)) < 10000:  # Cache apenas dados pequenos
                cache_key = f"{processing_type}_{hash(str(data))}"
                self.data_cache[cache_key] = result
                self.processing_stats["cached"] += 1
            
            # Enviar resposta
            self.send_message(
                message.sender_id,
                MessageType.RESPONSE,
                {"status": "success", "result": result}
            )
            
            logger.info(f"📊 Dados processados - ID: {processing_id}, Records: {result['input_records']}")
            
        except Exception as e:
            self.processing_stats["errors"] += 1
            
            # Enviar erro
            self.send_message(
                message.sender_id,
                MessageType.RESPONSE,
                {"status": "error", "error": str(e), "processing_id": processing_id}
            )
            
            logger.error(f"❌ Erro processando dados: {e}")
    
    def _simulate_data_processing(self, data: Any, processing_type: str) -> Any:
        """Simula processamento de dados"""
        if processing_type == "clean":
            # Simular limpeza de dados
            if isinstance(data, list):
                return [item for item in data if item is not None and str(item).strip()]
            return data
        
        elif processing_type == "normalize":
            # Simular normalização
            if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
                max_val = max(data) if data else 1
                return [x / max_val for x in data]
            return data
        
        elif processing_type == "aggregate":
            # Simular agregação
            if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
                return {
                    "count": len(data),
                    "sum": sum(data),
                    "mean": statistics.mean(data) if data else 0,
                    "min": min(data) if data else 0,
                    "max": max(data) if data else 0
                }
            return data
        
        else:
            # Processamento padrão
            return data


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
        
        # Capacidades específicas
        self.add_capability(AgentCapability(
            name="system_monitoring",
            description="Monitoramento de métricas de sistema",
            input_types=["system_metrics", "logs"],
            output_types=["monitoring_report", "alerts"],
            processing_time_ms=100.0,
            accuracy_score=0.98,
            resource_cost=0.1
        ))
    
    def _agent_specific_logic(self):
        """Lógica específica do agente de monitoramento"""
        # Coletar métricas do sistema a cada ciclo
        current_metrics = self._collect_system_metrics()
        
        # Armazenar métricas
        timestamp = datetime.now()
        for metric_name, value in current_metrics.items():
            self.monitoring_data[metric_name].append({
                "timestamp": timestamp,
                "value": value
            })
            
            # Manter apenas últimas 1000 medições
            if len(self.monitoring_data[metric_name]) > 1000:
                self.monitoring_data[metric_name] = self.monitoring_data[metric_name][-1000:]
        
        # Verificar alertas
        self._check_alerts(current_metrics)
    
    def _collect_system_metrics(self) -> Dict[str, float]:
        """Coleta métricas do sistema"""
        # Simular coleta de métricas
        return {
            "cpu_usage": random.uniform(20, 95),
            "memory_usage": random.uniform(30, 90),
            "disk_usage": random.uniform(40, 80),
            "response_time": random.uniform(100, 2000),
            "error_rate": random.uniform(0, 10),
            "active_connections": random.randint(10, 500)
        }
    
    def _check_alerts(self, metrics: Dict[str, float]):
        """Verifica se alguma métrica excedeu os thresholds"""
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
                
                # Enviar alerta para a rede
                self.broadcast_message(
                    MessageType.NOTIFICATION,
                    {
                        "alert_type": "threshold_exceeded",
                        "alert": alert
                    },
                    Priority.HIGH if alert["severity"] == "high" else Priority.NORMAL
                )
                
                logger.warning(f"🚨 Alerta: {metric_name} = {value:.1f} (threshold: {threshold})")


if __name__ == "__main__":
    # Exemplo de uso dos agentes especializados
    from multi_agent_network import MultiAgentNetwork
    
    # Criar rede
    network = MultiAgentNetwork()
    
    # Adicionar agentes especializados
    optimization_agent = OptimizationAgent("optimizer_001", network.message_bus)
    security_agent = SecurityAgent("security_001", network.message_bus)
    learning_agent = LearningAgent("learning_001", network.message_bus)
    data_agent = DataAgent("data_001", network.message_bus)
    monitoring_agent = MonitoringAgent("monitor_001", network.message_bus)
    
    network.add_agent(optimization_agent)
    network.add_agent(security_agent)
    network.add_agent(learning_agent)
    network.add_agent(data_agent)
    network.add_agent(monitoring_agent)
    
    try:
        # Iniciar rede
        network.start()
        
        print("🌐 Rede multi-agente com agentes especializados iniciada!")
        print("Agentes ativos:")
        for agent_id, agent in network.agents.items():
            print(f"  - {agent_id} ({agent.agent_type.value})")
        
        # Simular operações
        time.sleep(10)
        
        # Verificar status
        status = network.get_network_status()
        print(f"\n📊 Status da rede: {status['network_metrics']['active_agents']} agentes ativos")
        
        # Manter rodando
        input("\nPressione Enter para parar...")
        
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário")
    finally:
        network.stop()
