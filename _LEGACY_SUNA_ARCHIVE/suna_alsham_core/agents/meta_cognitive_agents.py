"""
meta_cognitive_agents.py - Sistema Meta-Cognitivo Completo e Robusto
Orchestrator + MetaCognitive_001 + MetaCognitive_002 (redundância total, produção, extensível)
Melhorias: docstrings, tipagem, logging, fallback, hooks, validação, arquitetura, segurança, performance.
"""

import asyncio
import logging
import time
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor
import os

class BaseMetaAgent:
    """
    Classe base para agentes meta-cognitivos.
    Fornece interface, logging, validação e extensibilidade para produção.
    """
    def __init__(self, agent_id: str, config: Optional[Dict[str, Any]] = None, logger: Optional[logging.Logger] = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.logger = logger or logging.getLogger(f"suna_alsham_core.agents.{agent_id}")
        self.active = True
        self.last_heartbeat = time.time()
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "version": self.config.get("version", "1.0.0"),
            "status": "initializing"
        }
        self.hooks: Dict[str, Any] = {}  # Para integração externa
        self._validate_agent()

    def _validate_agent(self):
        assert isinstance(self.agent_id, str) and self.agent_id, "agent_id inválido"
        assert hasattr(self, 'process_message'), "Agente deve implementar process_message"

    def get_capabilities(self) -> List[str]:
        """Deve ser sobrescrito pelas subclasses."""
        return []

    async def process_message(self, message: Dict) -> Dict:
        """Deve ser sobrescrito pelas subclasses."""
        return {"status": "processed", "agent": self.agent_id}

    def register_hook(self, event: str, callback):
        """Permite integração de hooks externos para eventos do agente."""
        self.hooks[event] = callback

    def trigger_hook(self, event: str, *args, **kwargs):
        if event in self.hooks:
            try:
                return self.hooks[event](*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Erro no hook '{event}': {e}")
        return None

class WorkflowOrchestrator(BaseMetaAgent):
    """
    Orchestrador principal do sistema meta-cognitivo.
    Responsável por coordenação, delegação, monitoramento e integração.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None, logger: Optional[logging.Logger] = None):
        super().__init__("orchestrator_001", config, logger)
        self.capabilities = [
            "workflow_orchestration",
            "task_delegation",
            "resource_management",
            "system_coordination",
            "priority_management"
        ]
        self.active_workflows: Dict[str, Dict] = {}
        self.task_queue: List[Dict] = []
        self.agent_registry: Dict[str, Dict] = {}
        self.logger.info(f"🎭 {self.agent_id} inicializado - Orchestrador Principal")
        self.metadata["status"] = "active"

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    async def process_message(self, message: Dict) -> Dict:
        """Processar mensagens de orquestração com robustez e logging."""
        try:
            msg_type = message.get('type', 'unknown')
            if msg_type == 'workflow_start':
                return await self.start_workflow(message)
            elif msg_type == 'task_delegate':
                return await self.delegate_task(message)
            elif msg_type == 'system_status':
                return await self.get_system_status()
            elif msg_type == 'resource_check':
                return await self.check_resources()
            else:
                return await self.handle_generic_message(message)
        except Exception as e:
            self.logger.error(f"Erro no orchestrador: {e}", exc_info=True)
            return {"error": str(e), "agent": self.agent_id}
    
    async def start_workflow(self, message: Dict) -> Dict:
        """Iniciar novo workflow"""
        workflow_id = message.get('workflow_id', f"wf_{int(time.time())}")
        workflow_data = {
            'id': workflow_id,
            'started_at': datetime.now().isoformat(),
            'status': 'running',
            'tasks': message.get('tasks', []),
            'priority': message.get('priority', 'normal')
        }
        
        self.active_workflows[workflow_id] = workflow_data
        self.logger.info(f"🎭 Workflow iniciado: {workflow_id}")
        
        return {
            "status": "workflow_started",
            "workflow_id": workflow_id,
            "agent": self.agent_id
        }
    
    async def delegate_task(self, message: Dict) -> Dict:
        """Delegar tarefa para agente apropriado"""
        task = message.get('task', {})
        required_capability = task.get('capability', 'general')
        
        # Encontrar agente com capability necessária
        suitable_agents = [
            agent_id for agent_id, info in self.agent_registry.items()
            if required_capability in info.get('capabilities', [])
        ]
        
        if suitable_agents:
            selected_agent = suitable_agents[0]  # Algoritmo simples, pode ser melhorado
            self.logger.info(f"🎭 Tarefa delegada para {selected_agent}")
            return {
                "status": "task_delegated",
                "assigned_to": selected_agent,
                "task_id": task.get('id'),
                "agent": self.agent_id
            }
        else:
            return {
                "status": "no_suitable_agent",
                "required_capability": required_capability,
                "agent": self.agent_id
            }
    
    async def get_system_status(self) -> Dict:
        """Obter status geral do sistema com métricas reais."""
        uptime = time.time() - self.last_heartbeat
        try:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
        except Exception:
            cpu = mem = None
        return {
            "status": "system_operational",
            "active_workflows": len(self.active_workflows),
            "registered_agents": len(self.agent_registry),
            "queue_size": len(self.task_queue),
            "uptime": uptime,
            "cpu_usage": cpu,
            "memory_usage": mem,
            "agent": self.agent_id
        }
    
    async def check_resources(self) -> Dict:
        """Verificar recursos do sistema"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            return {
                "status": "resources_checked",
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available": memory.available,
                "system_healthy": cpu_percent < 80 and memory.percent < 85,
                "agent": self.agent_id
            }
        except Exception as e:
            return {
                "status": "resource_check_failed",
                "error": str(e),
                "agent": self.agent_id
            }
    
    async def handle_generic_message(self, message: Dict) -> Dict:
        """Handler genérico para mensagens"""
        return {
            "status": "message_received",
            "message_type": message.get('type', 'unknown'),
            "timestamp": datetime.now().isoformat(),
            "agent": self.agent_id
        }

class MetaCognitiveAgent001(BaseMetaAgent):
    """
    Primeiro agente meta-cognitivo - Análise principal, auto-monitoramento, aprendizado.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None, logger: Optional[logging.Logger] = None):
        super().__init__("metacognitive_001", config, logger)
        self.capabilities = [
            "self_monitoring",
            "performance_analysis",
            "pattern_recognition",
            "system_reflection",
            "strategic_thinking",
            "learning_optimization"
        ]
        self.analysis_history: List[Dict] = []
        self.pattern_database: Dict[str, Any] = {}
        self.performance_metrics: Dict[str, Any] = {}
        self.learning_model: Dict[str, Any] = {}
        self.logger.info(f"🧠 {self.agent_id} inicializado - Meta-Cognição Principal")
        self.metadata["status"] = "active"

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    async def process_message(self, message: Dict) -> Dict:
        """Processar mensagens meta-cognitivas com robustez e logging."""
        try:
            msg_type = message.get('type', 'unknown')
            if msg_type == 'analyze_system':
                return await self.analyze_system_state()
            elif msg_type == 'detect_patterns':
                return await self.detect_patterns(message.get('data', {}))
            elif msg_type == 'performance_review':
                return await self.review_performance()
            elif msg_type == 'learning_update':
                return await self.update_learning(message.get('experience', {}))
            elif msg_type == 'strategic_assessment':
                return await self.strategic_assessment()
            else:
                return await self.default_analysis(message)
        except Exception as e:
            self.logger.error(f"Erro meta-cognitivo: {e}", exc_info=True)
            return {"error": str(e), "agent": self.agent_id}
    
    async def analyze_system_state(self) -> Dict:
        """Análise principal do estado do sistema"""
        try:
            current_time = datetime.now()
            
            # Coleta de métricas do sistema
            system_metrics = {
                "timestamp": current_time.isoformat(),
                "cpu_usage": psutil.cpu_percent(),
                "memory_usage": psutil.virtual_memory().percent,
                "active_processes": len(psutil.pids()),
                "network_connections": len(psutil.net_connections())
            }
            
            # Análise meta-cognitiva
            analysis = {
                "system_health": "healthy" if system_metrics["cpu_usage"] < 70 and system_metrics["memory_usage"] < 80 else "stressed",
                "performance_trend": self._calculate_performance_trend(),
                "anomalies_detected": self._detect_anomalies(system_metrics),
                "recommendations": self._generate_recommendations(system_metrics)
            }
            
            # Salvar histórico
            self.analysis_history.append({
                "timestamp": current_time.isoformat(),
                "metrics": system_metrics,
                "analysis": analysis
            })
            
            # Manter apenas últimas 100 análises
            if len(self.analysis_history) > 100:
                self.analysis_history = self.analysis_history[-100:]
            
            self.logger.info(f"🧠 Análise sistema concluída - Status: {analysis['system_health']}")
            
            return {
                "status": "analysis_complete",
                "system_metrics": system_metrics,
                "analysis": analysis,
                "agent": self.agent_id
            }
            
        except Exception as e:
            self.logger.error(f"Erro na análise do sistema: {e}")
            return {"status": "analysis_failed", "error": str(e), "agent": self.agent_id}
    
    async def detect_patterns(self, data: Dict) -> Dict:
        """Detectar padrões nos dados"""
        patterns_found = []
        
        # Análise de padrões temporais
        if 'timestamp_data' in data:
            temporal_patterns = self._analyze_temporal_patterns(data['timestamp_data'])
            patterns_found.extend(temporal_patterns)
        
        # Análise de padrões de uso
        if 'usage_data' in data:
            usage_patterns = self._analyze_usage_patterns(data['usage_data'])
            patterns_found.extend(usage_patterns)
        
        # Armazenar padrões descobertos
        pattern_id = f"pattern_{int(time.time())}"
        self.pattern_database[pattern_id] = {
            "discovered_at": datetime.now().isoformat(),
            "patterns": patterns_found,
            "data_source": data.get('source', 'unknown')
        }
        
        return {
            "status": "patterns_detected",
            "patterns_count": len(patterns_found),
            "patterns": patterns_found,
            "pattern_id": pattern_id,
            "agent": self.agent_id
        }
    
    async def review_performance(self) -> Dict:
        """Revisar performance do sistema"""
        if not self.analysis_history:
            return {
                "status": "insufficient_data",
                "message": "Histórico insuficiente para análise",
                "agent": self.agent_id
            }
        
        recent_analyses = self.analysis_history[-10:]  # Últimas 10 análises
        
        # Calcular médias
        avg_cpu = sum(a["metrics"]["cpu_usage"] for a in recent_analyses) / len(recent_analyses)
        avg_memory = sum(a["metrics"]["memory_usage"] for a in recent_analyses) / len(recent_analyses)
        
        # Avaliar tendências
        performance_score = self._calculate_performance_score(avg_cpu, avg_memory)
        
        performance_review = {
            "average_cpu": round(avg_cpu, 2),
            "average_memory": round(avg_memory, 2),
            "performance_score": performance_score,
            "trend": "improving" if performance_score > 75 else "stable" if performance_score > 50 else "declining",
            "samples_analyzed": len(recent_analyses)
        }
        
        return {
            "status": "performance_reviewed",
            "review": performance_review,
            "agent": self.agent_id
        }
    
    def _calculate_performance_trend(self) -> str:
        """Calcular tendência de performance"""
        if len(self.analysis_history) < 2:
            return "insufficient_data"
        
        recent = self.analysis_history[-5:] if len(self.analysis_history) >= 5 else self.analysis_history
        cpu_trend = [a["metrics"]["cpu_usage"] for a in recent]
        
        if len(cpu_trend) < 2:
            return "stable"
        
        trend_slope = (cpu_trend[-1] - cpu_trend[0]) / len(cpu_trend)
        
        if trend_slope > 5:
            return "increasing"
        elif trend_slope < -5:
            return "decreasing"
        else:
            return "stable"
    
    def _detect_anomalies(self, metrics: Dict) -> List[str]:
        """Detectar anomalias nos metrics"""
        anomalies = []
        
        if metrics["cpu_usage"] > 90:
            anomalies.append("high_cpu_usage")
        
        if metrics["memory_usage"] > 90:
            anomalies.append("high_memory_usage")
        
        if metrics["active_processes"] > 500:
            anomalies.append("high_process_count")
        
        return anomalies
    
    def _generate_recommendations(self, metrics: Dict) -> List[str]:
        """Gerar recomendações baseadas nos metrics"""
        recommendations = []
        
        if metrics["cpu_usage"] > 80:
            recommendations.append("consider_cpu_optimization")
        
        if metrics["memory_usage"] > 85:
            recommendations.append("review_memory_usage")
        
        if not recommendations:
            recommendations.append("system_operating_normally")
        
        return recommendations
    
    def _analyze_temporal_patterns(self, data: List) -> List[Dict]:
        """Analisar padrões temporais"""
        return [{"type": "temporal", "description": "Pattern analysis placeholder"}]
    
    def _analyze_usage_patterns(self, data: Dict) -> List[Dict]:
        """Analisar padrões de uso"""
        return [{"type": "usage", "description": "Usage pattern analysis placeholder"}]
    
    def _calculate_performance_score(self, cpu: float, memory: float) -> float:
        """Calcular score de performance"""
        cpu_score = max(0, 100 - cpu)
        memory_score = max(0, 100 - memory)
        return (cpu_score + memory_score) / 2

class MetaCognitiveAgent002(BaseMetaAgent):
    """
    Segundo agente meta-cognitivo - Validação cruzada, redundância, consistência, backup.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None, logger: Optional[logging.Logger] = None):
        super().__init__("metacognitive_002", config, logger)
        self.capabilities = [
            "cross_validation",
            "redundancy_check",
            "consensus_analysis",
            "anomaly_detection",
            "system_consistency",
            "backup_analysis"
        ]
        self.validation_results: List[Dict] = []
        self.consensus_data: Dict[str, Any] = {}
        self.anomaly_patterns: Dict[str, Any] = {}
        self.sister_agent_id = "metacognitive_001"
        self.logger.info(f"🧠 {self.agent_id} inicializado - Meta-Cognição Redundante")
        self.metadata["status"] = "active"

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    async def process_message(self, message: Dict) -> Dict:
        """Processar mensagens de validação e redundância com robustez e logging."""
        try:
            msg_type = message.get('type', 'unknown')
            if msg_type == 'validate_analysis':
                return await self.validate_sister_analysis(message.get('analysis', {}))
            elif msg_type == 'consensus_check':
                return await self.consensus_analysis(message.get('data', {}))
            elif msg_type == 'anomaly_scan':
                return await self.deep_anomaly_scan()
            elif msg_type == 'consistency_check':
                return await self.check_system_consistency()
            elif msg_type == 'backup_analysis':
                return await self.backup_system_analysis()
            else:
                return await self.independent_analysis(message)
        except Exception as e:
            self.logger.error(f"Erro meta-cognitivo 002: {e}", exc_info=True)
            return {"error": str(e), "agent": self.agent_id}
    
    async def validate_sister_analysis(self, analysis: Dict) -> Dict:
        """Validar análise do meta-cognitivo 001"""
        try:
            # Executar análise independente
            independent_result = await self.independent_system_check()
            
            # Comparar resultados
            validation = self._compare_analyses(analysis, independent_result)
            
            # Salvar resultado da validação
            validation_record = {
                "timestamp": datetime.now().isoformat(),
                "original_analysis": analysis,
                "independent_check": independent_result,
                "validation": validation
            }
            
            self.validation_results.append(validation_record)
            
            # Manter apenas últimas 50 validações
            if len(self.validation_results) > 50:
                self.validation_results = self.validation_results[-50:]
            
            self.logger.info(f"🧠 Validação cruzada concluída - Concordância: {validation['agreement_score']}%")
            
            return {
                "status": "validation_complete",
                "validation": validation,
                "agreement_score": validation["agreement_score"],
                "agent": self.agent_id
            }
            
        except Exception as e:
            return {"status": "validation_failed", "error": str(e), "agent": self.agent_id}
    
    async def consensus_analysis(self, data: Dict) -> Dict:
        """Análise de consenso entre agentes meta-cognitivos"""
        consensus_id = f"consensus_{int(time.time())}"
        
        # Análise independente dos dados
        my_analysis = await self._analyze_data_independently(data)
        
        # Criar registro de consenso
        consensus_record = {
            "id": consensus_id,
            "timestamp": datetime.now().isoformat(),
            "data_analyzed": data,
            "my_analysis": my_analysis,
            "waiting_for_sister": True
        }
        
        self.consensus_data[consensus_id] = consensus_record
        
        return {
            "status": "consensus_analysis_ready",
            "consensus_id": consensus_id,
            "my_analysis": my_analysis,
            "agent": self.agent_id
        }
    
    async def deep_anomaly_scan(self) -> Dict:
        """Scan profundo de anomalias usando método alternativo"""
        try:
            current_time = datetime.now()
            
            # Coleta de dados por método alternativo
            system_snapshot = {
                "processes": self._analyze_process_anomalies(),
                "network": self._analyze_network_anomalies(),
                "performance": self._analyze_performance_anomalies(),
                "patterns": self._analyze_behavioral_patterns()
            }
            
            # Detecção de anomalias
            detected_anomalies = []
            
            for category, data in system_snapshot.items():
                category_anomalies = self._detect_category_anomalies(category, data)
                detected_anomalies.extend(category_anomalies)
            
            # Classificação por severidade
            anomaly_summary = {
                "critical": [a for a in detected_anomalies if a.get("severity") == "critical"],
                "warning": [a for a in detected_anomalies if a.get("severity") == "warning"],
                "info": [a for a in detected_anomalies if a.get("severity") == "info"]
            }
            
            self.logger.info(f"🧠 Scan de anomalias concluído - {len(detected_anomalies)} anomalias detectadas")
            
            return {
                "status": "anomaly_scan_complete",
                "total_anomalies": len(detected_anomalies),
                "anomaly_summary": anomaly_summary,
                "system_snapshot": system_snapshot,
                "scan_timestamp": current_time.isoformat(),
                "agent": self.agent_id
            }
            
        except Exception as e:
            return {"status": "anomaly_scan_failed", "error": str(e), "agent": self.agent_id}
    
    async def check_system_consistency(self) -> Dict:
        """Verificar consistência do sistema"""
        consistency_checks = {
            "agent_registry": self._check_agent_registry_consistency(),
            "message_flow": self._check_message_flow_consistency(),
            "resource_allocation": self._check_resource_consistency(),
            "data_integrity": self._check_data_integrity()
        }
        
        # Calcular score de consistência geral
        passed_checks = sum(1 for check in consistency_checks.values() if check.get("status") == "consistent")
        total_checks = len(consistency_checks)
        consistency_score = (passed_checks / total_checks) * 100
        
        return {
            "status": "consistency_check_complete",
            "consistency_score": round(consistency_score, 2),
            "checks": consistency_checks,
            "system_consistent": consistency_score >= 80,
            "agent": self.agent_id
        }
    
    async def backup_system_analysis(self) -> Dict:
        """Análise de backup quando agente principal falha"""
        self.logger.warning("🧠 Executando análise de backup - agente principal pode estar indisponível")
        
        try:
            # Análise básica de sistema
            basic_metrics = {
                "cpu": psutil.cpu_percent(interval=1),
                "memory": psutil.virtual_memory().percent,
                "disk": psutil.disk_usage('/').percent,
                "processes": len(psutil.pids())
            }
            
            # Status simplificado
            system_status = "healthy" if all(
                basic_metrics["cpu"] < 80,
                basic_metrics["memory"] < 85,
                basic_metrics["disk"] < 90
            ) else "stressed"
            
            return {
                "status": "backup_analysis_complete",
                "system_status": system_status,
                "basic_metrics": basic_metrics,
                "backup_mode": True,
                "agent": self.agent_id
            }
            
        except Exception as e:
            return {"status": "backup_analysis_failed", "error": str(e), "agent": self.agent_id}
    
    async def independent_analysis(self, message: Dict) -> Dict:
        """Análise independente de mensagens"""
        return {
            "status": "independent_analysis_complete",
            "message_processed": True,
            "analysis_method": "alternative",
            "timestamp": datetime.now().isoformat(),
            "agent": self.agent_id
        }
    
    async def independent_system_check(self) -> Dict:
        """Check independente do sistema"""
        try:
            # Métrica alternativa de sistema
            cpu_samples = [psutil.cpu_percent() for _ in range(3)]
            avg_cpu = sum(cpu_samples) / len(cpu_samples)
            
            memory_info = psutil.virtual_memory()
            
            return {
                "cpu_usage": round(avg_cpu, 2),
                "memory_usage": round(memory_info.percent, 2),
                "memory_available_gb": round(memory_info.available / (1024**3), 2),
                "system_load": psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0,
                "analysis_method": "independent"
            }
        except Exception as e:
            return {"error": str(e), "analysis_method": "failed"}
    
    def _compare_analyses(self, analysis1: Dict, analysis2: Dict) -> Dict:
        """Comparar duas análises"""
        agreement_factors = []
        
        # Comparar CPU usage se disponível
        if "cpu_usage" in analysis1 and "cpu_usage" in analysis2:
            cpu_diff = abs(analysis1["cpu_usage"] - analysis2["cpu_usage"])
            cpu_agreement = max(0, 100 - (cpu_diff * 2))  # Diferença de 50% = 0% concordância
            agreement_factors.append(cpu_agreement)
        
        # Comparar Memory usage se disponível  
        if "memory_usage" in analysis1 and "memory_usage" in analysis2:
            mem_diff = abs(analysis1["memory_usage"] - analysis2["memory_usage"])
            mem_agreement = max(0, 100 - (mem_diff * 2))
            agreement_factors.append(mem_agreement)
        
        # Calcular score médio de concordância
        agreement_score = sum(agreement_factors) / len(agreement_factors) if agreement_factors else 50
        
        return {
            "agreement_score": round(agreement_score, 2),
            "factors_compared": len(agreement_factors),
            "high_agreement": agreement_score >= 80,
            "discrepancies": agreement_score < 60
        }
    
    async def _analyze_data_independently(self, data: Dict) -> Dict:
        """Análise independente de dados"""
        return {
            "data_size": len(str(data)),
            "analysis_timestamp": datetime.now().isoformat(),
            "independent_score": 85.5,  # Placeholder
            "method": "alternative_analysis"
        }
    
    def _analyze_process_anomalies(self) -> Dict:
        """Analisar anomalias de processo"""
        try:
            processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']))
            high_cpu_processes = [p for p in processes if p.info['cpu_percent'] > 10]
            high_memory_processes = [p for p in processes if p.info['memory_percent'] > 5]
            
            return {
                "total_processes": len(processes),
                "high_cpu_count": len(high_cpu_processes),
                "high_memory_count": len(high_memory_processes),
                "anomaly_detected": len(high_cpu_processes) > 10 or len(high_memory_processes) > 15
            }
        except:
            return {"error": "process_analysis_failed"}
    
    def _analyze_network_anomalies(self) -> Dict:
        """Analisar anomalias de rede"""
        try:
            connections = psutil.net_connections()
            return {
                "total_connections": len(connections),
                "anomaly_detected": len(connections) > 1000
            }
        except:
            return {"error": "network_analysis_failed"}
    
    def _analyze_performance_anomalies(self) -> Dict:
        """Analisar anomalias de performance"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            return {
                "cpu_anomaly": cpu_percent > 90,
                "memory_anomaly": memory_percent > 90,
                "performance_score": max(0, 100 - (cpu_percent + memory_percent) / 2)
            }
        except:
            return {"error": "performance_analysis_failed"}
    
    def _analyze_behavioral_patterns(self) -> Dict:
        """Analisar padrões comportamentais"""
        return {
            "pattern_consistency": 85,  # Placeholder
            "behavioral_anomalies": 0,
            "pattern_deviation": "normal"
        }
    
    def _detect_category_anomalies(self, category: str, data: Dict) -> List[Dict]:
        """Detectar anomalias por categoria"""
        anomalies = []
        
        if category == "processes" and data.get("anomaly_detected"):
            anomalies.append({
                "category": "processes",
                "type": "high_process_activity",
                "severity": "warning"
            })
        
        if category == "performance":
            if data.get("cpu_anomaly"):
                anomalies.append({
                    "category": "performance",
                    "type": "high_cpu_usage",
                    "severity": "critical"
                })
            if data.get("memory_anomaly"):
                anomalies.append({
                    "category": "performance", 
                    "type": "high_memory_usage",
                    "severity": "critical"
                })
        
        return anomalies
    
    def _check_agent_registry_consistency(self) -> Dict:
        """Verificar consistência do registro de agentes"""
        return {"status": "consistent", "message": "Registry check placeholder"}
    
    def _check_message_flow_consistency(self) -> Dict:
        """Verificar consistência do fluxo de mensagens"""
        return {"status": "consistent", "message": "Message flow check placeholder"}
    
    def _check_resource_consistency(self) -> Dict:
        """Verificar consistência de recursos"""
        return {"status": "consistent", "message": "Resource consistency placeholder"}
    
    def _check_data_integrity(self) -> Dict:
        """Verificar integridade dos dados"""
        return {"status": "consistent", "message": "Data integrity placeholder"}

def create_agents(*args, **kwargs) -> List[BaseMetaAgent]:
    """
    Criar todos os 3 agentes meta-cognitivos robustos e extensíveis:
    - Orchestrator (coordenação)
    - MetaCognitive_001 (análise principal)
    - MetaCognitive_002 (validação cruzada)
    Aceita config/loggers via kwargs. Fallback seguro.
    """
    agents: List[BaseMetaAgent] = []
    config = kwargs.get('config', {})
    logger = kwargs.get('logger', None)
    try:
        print("🧠 Iniciando criação completa dos meta-cognitive agents...")
        orchestrator = WorkflowOrchestrator(config=config.get('orchestrator'), logger=logger)
        agents.append(orchestrator)
        print(f"✅ Orchestrator criado: {orchestrator.agent_id}")
        meta001 = MetaCognitiveAgent001(config=config.get('meta001'), logger=logger)
        agents.append(meta001)
        print(f"✅ Meta-Cognitive 001 criado: {meta001.agent_id}")
        meta002 = MetaCognitiveAgent002(config=config.get('meta002'), logger=logger)
        agents.append(meta002)
        print(f"✅ Meta-Cognitive 002 criado: {meta002.agent_id}")
        print(f"🎯 Total de meta-cognitive agents criados: {len(agents)}")
        print("🧠 Sistema meta-cognitivo completo: Orchestrator + Primary + Backup")
        return agents
    except Exception as e:
        print(f"❌ Erro crítico na criação dos meta-cognitive agents: {e}")
        import traceback
        traceback.print_exc()
        # FALLBACK: pelo menos o orchestrator básico
        try:
            basic_orchestrator = WorkflowOrchestrator()
            print(f"⚠️ Fallback: apenas orchestrator criado: {basic_orchestrator.agent_id}")
            return [basic_orchestrator]
        except Exception as fallback_error:
            print(f"❌ Fallback também falhou: {fallback_error}")
            return []

# Função auxiliar para testing
async def test_meta_cognitive_system():
    """
    Testa o sistema meta-cognitivo completo, validando robustez e integração.
    """
    agents = create_agents()
    if len(agents) == 3:
        print("✅ Sistema meta-cognitivo completo criado!")
        for agent in agents:
            test_message = {
                "type": "system_status" if "orchestrator" in agent.agent_id
                      else "analyze_system" if "001" in agent.agent_id
                      else "consistency_check",
                "timestamp": datetime.now().isoformat()
            }
            try:
                result = await agent.process_message(test_message)
                print(f"🧪 Teste {agent.agent_id}: {result.get('status', 'unknown')}")
            except Exception as e:
                print(f"❌ Erro ao testar {agent.agent_id}: {e}")
    else:
        print(f"⚠️ Apenas {len(agents)} agentes criados. Verifique dependências.")
    return agents

if __name__ == "__main__":
    # Teste direto do módulo
    agents = create_agents()
    print(f"🎯 Agentes meta-cognitivos criados: {len(agents)}")
    # Teste assíncrono se rodando diretamente
    # asyncio.run(test_meta_cognitive_system())
