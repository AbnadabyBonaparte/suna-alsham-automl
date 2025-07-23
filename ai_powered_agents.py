"""🧠 SUNA-ALSHAM AI-Powered Agents
Agentes com IA real integrada para auto-evolução genuína

FUNCIONALIDADES:
✅ Integração com OpenAI GPT-4 e Claude
✅ Auto-reflexão e meta-cognição
✅ Análise do próprio código-fonte
✅ Geração de melhorias automáticas
✅ Validação científica rigorosa
✅ Cache inteligente para otimização de custos
✅ Logging científico para publicação
✅ Segurança enterprise integrada
"""

import asyncio
import json
import time
import uuid
import logging
import hashlib
import os
import ast
import inspect
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
import openai
import redis
from contextlib import contextmanager
import threading
import queue
import statistics
import numpy as np

from multi_agent_network import (
    BaseNetworkAgent,
    AgentType,
    MessageType,
    Priority,
    AgentCapability,
    MessageBus
)

logger = logging.getLogger(__name__)

# Configurar OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

@dataclass
class AIReflectionResult:
    """Resultado de auto-reflexão da IA"""
    analysis_id: str
    code_analysis: Dict[str, Any]
    improvement_suggestions: List[Dict[str, Any]]
    performance_predictions: Dict[str, float]
    confidence_score: float
    reasoning: str
    timestamp: datetime
    tokens_used: int
    cost_usd: float

@dataclass
class ScientificMetrics:
    """Métricas científicas para validação rigorosa"""
    metric_id: str
    agent_id: str
    measurement_type: str
    baseline_value: float
    current_value: float
    improvement_percentage: float
    statistical_significance: float
    p_value: float
    confidence_interval: Tuple[float, float]
    sample_size: int
    measurement_timestamp: datetime
    validation_method: str

class AICache:
    """Sistema de cache inteligente para otimização de custos"""

    def __init__(self, redis_url: Optional[str] = None):
        self.redis_client = None
        self.local_cache: Dict[str, Any] = {}
        self.cache_stats = {"hits": 0, "misses": 0, "cost_saved": 0.0}
        
        if redis_url:
            try:
                self.redis_client = redis.from_url(redis_url)
                self.redis_client.ping()
                logger.info("✅ Cache Redis conectado")
            except Exception as e:
                logger.warning(f"⚠️ Redis não disponível, usando cache local: {e}")

    def _generate_cache_key(self, prompt: str, model: str, temperature: float) -> str:
        content = f"{prompt}|{model}|{temperature}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, prompt: str, model: str, temperature: float) -> Optional[Dict[str, Any]]:
        cache_key = self._generate_cache_key(prompt, model, temperature)
        if self.redis_client:
            try:
                cached = self.redis_client.get(cache_key)
                if cached:
                    self.cache_stats["hits"] += 1
                    result = json.loads(cached)
                    self.cache_stats["cost_saved"] += result.get("estimated_cost", 0.0)
                    return result
            except Exception as e:
                logger.warning(f"⚠️ Erro acessando Redis cache: {e}")
        if cache_key in self.local_cache:
            self.cache_stats["hits"] += 1
            result = self.local_cache[cache_key]
            self.cache_stats["cost_saved"] += result.get("estimated_cost", 0.0)
            return result
        self.cache_stats["misses"] += 1
        return None

    def set(self, prompt: str, model: str, temperature: float, response: Dict[str, Any], ttl: int = 3600):
        cache_key = self._generate_cache_key(prompt, model, temperature)
        cached_response = {
            **response,
            "cached_at": datetime.now().isoformat(),
            "ttl": ttl
        }
        if self.redis_client:
            try:
                self.redis_client.setex(cache_key, ttl, json.dumps(cached_response, default=str))
                return
            except Exception as e:
                logger.warning(f"⚠️ Erro salvando no Redis cache: {e}")
        self.local_cache[cache_key] = cached_response
        if len(self.local_cache) > 1000:
            items_to_remove = list(self.local_cache.keys())[:200]
            for key in items_to_remove:
                del self.local_cache[key]

    def get_stats(self) -> Dict[str, Any]:
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        return {
            "hit_rate_percentage": round(hit_rate, 2),
            "total_hits": self.cache_stats["hits"],
            "total_misses": self.cache_stats["misses"],
            "cost_saved_usd": round(self.cache_stats["cost_saved"], 4),
            "cache_size": len(self.local_cache)
        }

class AISecurityValidator:
    """Validador de segurança para operações de IA"""

    def __init__(self):
        self.security_patterns = [
            r"import\s+os",
            r"exec\s*\(",
            r"eval\s*\(",
            r"__import__",
            r"subprocess",
            r"system\s*\(",
            r"open\s*\(",
            r"file\s*\(",
            r"input\s*\(",
            r"raw_input\s*\("
        ]
        self.max_code_length = 10000
        self.max_tokens = 4000

    def validate_prompt(self, prompt: str) -> Tuple[bool, List[str]]:
        issues = []
        if len(prompt) > self.max_tokens * 4:
            issues.append(f"Prompt muito longo: {len(prompt)} caracteres")
        import re
        for pattern in self.security_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                issues.append(f"Padrão suspeito encontrado: {pattern}")
        return len(issues) == 0, issues

    def validate_generated_code(self, code: str) -> Tuple[bool, List[str]]:
        issues = []
        if len(code) > self.max_code_length:
            issues.append(f"Código muito longo: {len(code)} caracteres")
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(f"Erro de sintaxe: {e}")
        import re
        for pattern in self.security_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append(f"Código potencialmente perigoso: {pattern}")
        return len(issues) == 0, issues

class ScientificLogger:
    """Logger científico para análise e publicação"""

    def __init__(self, log_file: str = "scientific_metrics.jsonl"):
        self.log_file = log_file
        self.metrics_buffer: List[ScientificMetrics] = []
        self.buffer_size = 100
        self._lock = threading.Lock()

    def log_metric(self, metric: ScientificMetrics):
        with self._lock:
            self.metrics_buffer.append(metric)
            if len(self.metrics_buffer) >= self.buffer_size:
                self._flush_buffer()

    def _flush_buffer(self):
        try:
            with open(self.log_file, "a") as f:
                for metric in self.metrics_buffer:
                    f.write(json.dumps(asdict(metric), default=str) + "\n")
            logger.info(f"📊 {len(self.metrics_buffer)} métricas científicas salvas")
            self.metrics_buffer.clear()
        except Exception as e:
            logger.error(f"❌ Erro salvando métricas científicas: {e}")

    def get_metrics_summary(self, agent_id: Optional[str] = None, hours: int = 24) -> Dict[str, Any]:
        try:
            metrics = []
            cutoff_time = datetime.now() - timedelta(hours=hours)
            with open(self.log_file, "r") as f:
                for line in f:
                    try:
                        metric_data = json.loads(line)
                        metric_time = datetime.fromisoformat(metric_data["measurement_timestamp"])
                        if metric_time > cutoff_time and (not agent_id or metric_data["agent_id"] == agent_id):
                            metrics.append(metric_data)
                    except:
                        continue
            if not metrics:
                return {"total_metrics": 0, "summary": "No metrics found"}
            improvements = [m["improvement_percentage"] for m in metrics]
            significances = [m["statistical_significance"] for m in metrics]
            return {
                "total_metrics": len(metrics),
                "average_improvement": statistics.mean(improvements),
                "median_improvement": statistics.median(improvements),
                "average_significance": statistics.mean(significances),
                "significant_improvements": len([i for i in improvements if i > 5.0]),
                "time_range_hours": hours
            }
        except Exception as e:
            logger.error(f"❌ Erro gerando resumo de métricas: {e}")
            return {"error": str(e)}

class AIReflectionEngine:
    """Motor de auto-reflexão com IA real"""

    def __init__(self, cache: AICache, security_validator: AISecurityValidator):
        self.cache = cache
        self.security_validator = security_validator
        self.reflection_history: List[AIReflectionResult] = []
        self.models = {
            "analysis": "gpt-4",
            "code_generation": "gpt-4",
            "validation": "gpt-3.5-turbo"
        }
        self.costs_per_token = {
            "gpt-4": {"input": 0.00003, "output": 0.00006},
            "gpt-3.5-turbo": {"input": 0.0000015, "output": 0.000002}
        }

    async def analyze_agent_code(self, agent_code: str, performance_data: Dict[str, Any]) -> AIReflectionResult:
        analysis_id = str(uuid.uuid4())
        analysis_prompt = self._create_analysis_prompt(agent_code, performance_data)
        is_safe, issues = self.security_validator.validate_prompt(analysis_prompt)
        if not is_safe:
            raise ValueError(f"Prompt inseguro: {issues}")
        cached_result = self.cache.get(analysis_prompt, self.models["analysis"], 0.3)
        if cached_result:
            logger.info(f"🎯 Análise {analysis_id} obtida do cache")
            return AIReflectionResult(**cached_result["result"])
        try:
            start_time = time.time()
            response = await openai.ChatCompletion.acreate(
                model=self.models["analysis"],
                messages=[
                    {"role": "system", "content": "You are an expert AI system analyst specializing in self-improving agent architectures. Analyze the provided code and performance data to suggest concrete improvements."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            analysis_time = time.time() - start_time
            ai_response = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            cost_usd = self._calculate_cost(tokens_used, self.models["analysis"])
            analysis_result = self._parse_ai_analysis(ai_response)
            result = AIReflectionResult(
                analysis_id=analysis_id,
                code_analysis=analysis_result["code_analysis"],
                improvement_suggestions=analysis_result["improvements"],
                performance_predictions=analysis_result["predictions"],
                confidence_score=analysis_result["confidence"],
                reasoning=analysis_result["reasoning"],
                timestamp=datetime.now(),
                tokens_used=tokens_used,
                cost_usd=cost_usd
            )
            self.cache.set(analysis_prompt, self.models["analysis"], 0.3, {"result": asdict(result), "estimated_cost": cost_usd}, ttl=3600)
            self.reflection_history.append(result)
            logger.info(f"🧠 Análise {analysis_id} concluída - {tokens_used} tokens, ${cost_usd:.4f}")
            return result
        except Exception as e:
            logger.error(f"❌ Erro na análise de IA: {e}")
            raise

    def _create_analysis_prompt(self, agent_code: str, performance_data: Dict[str, Any]) -> str:
        return f"""
Analyze this AI agent code and its performance data to suggest improvements:

AGENT CODE:

```python
{agent_code[:5000]}
