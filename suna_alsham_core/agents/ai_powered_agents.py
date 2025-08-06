#!/usr/bin/env python3
"""
Quantum AI-Powered Agents – ALSHAM QUANTUM
[Quantum Version 2.0 - Multi-Provider Intelligence]
"""

import asyncio
import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

# Multi-Provider AI Support
try:
    from openai import AsyncOpenAI, RateLimitError, APIError, APITimeoutError
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI, RateLimitError, APIError, APITimeoutError = None, None, None, None

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    genai = None

from suna_alsham_core.multi_agent_network import AgentMessage, AgentType, BaseNetworkAgent, MessageType, Priority

logger = logging.getLogger(__name__)

class AIProvider(Enum):
    """Provedores de IA suportados."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"

class TaskComplexity(Enum):
    """Níveis de complexidade de tarefa."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"

@dataclass
class AIProviderConfig:
    """Configuração de provedor de IA."""
    provider: AIProvider
    api_key: str
    model: str
    max_tokens: int = 4000
    temperature: float = 0.2
    available: bool = True
    last_error: Optional[str] = None
    response_times: List[float] = field(default_factory=list)

@dataclass
class PlanningRequest:
    """Requisição de planejamento estruturada."""
    request_id: str
    user_prompt: str
    complexity: TaskComplexity = TaskComplexity.MODERATE
    preferred_provider: Optional[AIProvider] = None
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class PlanningResponse:
    """Resposta de planejamento com métricas."""
    request_id: str
    plan: List[Dict[str, Any]]
    provider_used: AIProvider
    model_used: str
    response_time_ms: float
    confidence_score: float
    validation_passed: bool
    created_at: datetime = field(default_factory=datetime.now)

# Sistema de Prompt Quântico Avançado
QUANTUM_SYSTEM_PROMPT = """
Você é o "Quantum Chief Planning Officer" (QCPO) do ALSHAM QUANTUM, um sistema de múltiplos agentes de IA com capacidades quânticas.

MISSÃO PRINCIPAL:
Converter objetivos de alto nível em planos de execução JSON estruturados que garantam sucesso absoluto através de análise multidimensional.

CAPACIDADES QUÂNTICAS:
- Processamento paralelo de múltiplas estratégias
- Análise de probabilidade de sucesso para cada passo
- Consideração de cenários de falha e planos de contingência
- Otimização automática baseada em capacidades dos agentes

REGRAS CRÍTICAS DE FORMATAÇÃO:
1. Sua saída DEVE ser um objeto JSON válido com a chave "plan"
2. A chave "plan" DEVE conter uma lista de objetos representando passos sequenciais
3. Cada passo DEVE ter: "step" (int), "description" (str), "agent" (str), "task" (dict), "expected_outcome" (str), "fallback_strategy" (str)
4. Use APENAS agentes da lista disponível abaixo
5. Para referenciar outputs de passos anteriores: {{output_step_N.path.to.value}}

AGENTES DISPONÍVEIS E CAPACIDADES:
- "web_search_001": Pesquisa web avançada. task: {"query": "termo de busca"}. Retorna: {"result": {"details": [...]}}
- "content_creator_001": Criação de conteúdo inteligente. task: {"prompt_template": "template", "context_data": {...}}. Retorna: {"result": {"generated_text": "..."}}
- "notification_001": Sistema de notificação quantum. task: {"recipient_email": "email", "subject": "assunto", "body": "conteúdo"}. Retorna: {"status": "sent/queued"}
- "image_generator_001": Geração de imagens. task: {"prompt": "descrição", "style": "estilo"}. Retorna: {"result": {"image_url": "..."}}
- "data_analyzer_001": Análise de dados. task: {"data": [...], "analysis_type": "tipo"}. Retorna: {"result": {"insights": [...]}}
- "visualization_001": Criação de gráficos. task: {"data_source_agent": "agente", "query": "sql", "chart_type": "tipo"}. Retorna: {"chart_json": "..."}

ESTRATÉGIA QUANTUM DE PLANEJAMENTO:
1. ANÁLISE DIMENSIONAL: Considere múltiplas abordagens para cada objetivo
2. VALIDAÇÃO DE COMPLETUDE: Garanta que TODOS os requisitos sejam atendidos
3. REDUNDÂNCIA INTELIGENTE: Inclua verificações e validações em pontos críticos
4. CONTINGÊNCIA AUTOMÁTICA: Defina estratégias de fallback para cada passo crítico
5. OTIMIZAÇÃO DE FLUXO: Organize passos para eficiência máxima

EXEMPLO DE RESPOSTA QUANTUM:
{
  "plan": [
    {
      "step": 1,
      "description": "Pesquisar informações detalhadas sobre o tópico solicitado",
      "agent": "web_search_001",
      "task": {"query": "informações específicas sobre X"},
      "expected_outcome": "Dados completos coletados com sucesso",
      "fallback_strategy": "Se falhar, usar fonte alternativa ou conhecimento base"
    },
    {
      "step": 2,
      "description": "Criar conteúdo estruturado baseado nas informações coletadas",
      "agent": "content_creator_001",
      "task": {
        "prompt_template": "Criar conteúdo sobre {{output_step_1.result.details}}",
        "context_data": {"format": "estruturado", "tone": "profissional"}
      },
      "expected_outcome": "Conteúdo de alta qualidade gerado",
      "fallback_strategy": "Regenerar com parâmetros ajustados se qualidade insuficiente"
    },
    {
      "step": 3,
      "description": "Entregar resultado final ao usuário via notificação",
      "agent": "notification_001", 
      "task": {
        "recipient_email": "destinatario@email.com",
        "subject": "Resultado da sua solicitação",
        "body": "{{output_step_2.result.generated_text}}"
      },
      "expected_outcome": "Notificação entregue com sucesso",
      "fallback_strategy": "Tentar provedores alternativos de email se falhar"
    }
  ]
}

IMPORTANTES:
- SEMPRE inclua todos os passos necessários para completar 100% da tarefa
- SEMPRE valide se o plano atende completamente ao objetivo original
- SEMPRE considere pontos de falha e inclua estratégias de recuperação
- NUNCA omita passos críticos como validação ou entrega final
- Se a tarefa envolver email, SEMPRE inclua o passo de notificação
- Se a tarefa envolver busca de imagem, inclua passos específicos para isso
"""

class QuantumAIAnalyzerAgent(BaseNetworkAgent):
    """
    Agente Analisador de IA Quântico com capacidades avançadas:
    - Múltiplos provedores de IA (OpenAI, Anthropic, Google)
    - Inteligência adaptativa baseada na complexidade da tarefa
    - Sistema de fallback automático entre provedores
    - Cache inteligente para otimização de performance
    - Validação quantum de planos gerados
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.AI_POWERED, message_bus)
        self.capabilities.extend([
            "quantum_planning",
            "multi_provider_intelligence", 
            "adaptive_reasoning",
            "plan_validation",
            "contextual_optimization"
        ])
        
        self.providers: Dict[AIProvider, AIProviderConfig] = {}
        self.request_cache: Dict[str, PlanningResponse] = {}
        self.active_requests: Dict[str, PlanningRequest] = {}
        self.performance_metrics = {
            "total_requests": 0,
            "successful_plans": 0,
            "failed_requests": 0,
            "avg_response_time": 0.0,
            "provider_usage": {},
            "uptime_start": datetime.now()
        }
        
        # Inicialização quantum
        self._initialize_quantum_providers()
        self._quantum_init_task = asyncio.create_task(self._quantum_initialization())
        
        logger.info(f"🧠 {self.agent_id} (Quantum AI Analyzer) inicializado com {len(self.providers)} provedores de IA.")

    def _initialize_quantum_providers(self):
        """Inicializa múltiplos provedores de IA para redundância quantum."""
        
        # OpenAI Provider
        openai_key = os.environ.get("OPENAI_API_KEY")
        if OPENAI_AVAILABLE and openai_key:
            self.providers[AIProvider.OPENAI] = AIProviderConfig(
                provider=AIProvider.OPENAI,
                api_key=openai_key,
                model="gpt-4o-mini",
                max_tokens=4000,
                temperature=0.2
            )
            logger.info("✅ Provedor OpenAI configurado.")
        
        # Anthropic Provider  
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        if ANTHROPIC_AVAILABLE and anthropic_key:
            self.providers[AIProvider.ANTHROPIC] = AIProviderConfig(
                provider=AIProvider.ANTHROPIC,
                api_key=anthropic_key,
                model="claude-3-haiku-20240307",
                max_tokens=4000,
                temperature=0.2
            )
            logger.info("✅ Provedor Anthropic configurado.")
        
        # Google Provider
        google_key = os.environ.get("GOOGLE_API_KEY")
        if GOOGLE_AVAILABLE and google_key:
            self.providers[AIProvider.GOOGLE] = AIProviderConfig(
                provider=AIProvider.GOOGLE,
                api_key=google_key,
                model="gemini-pro",
                max_tokens=4000,
                temperature=0.2
            )
            logger.info("✅ Provedor Google configurado.")
        
        if not self.providers:
            self.status = "degraded"
            logger.critical("❌ NENHUM provedor de IA configurado! Configure ao menos um:")
            logger.critical("   OpenAI: OPENAI_API_KEY")
            logger.critical("   Anthropic: ANTHROPIC_API_KEY") 
            logger.critical("   Google: GOOGLE_API_KEY")

    async def _quantum_initialization(self):
        """Inicialização e teste de conexão quantum."""
        if not self.providers:
            self.status = "degraded"
            return
            
        logger.info("🔍 Testando conexões com provedores de IA...")
        active_providers = []
        
        for provider_type, config in self.providers.items():
            try:
                if await self._test_provider_connection(provider_type, config):
                    active_providers.append(provider_type)
                    logger.info(f"✅ Provedor {provider_type.value} validado com sucesso.")
                else:
                    config.available = False
                    logger.warning(f"⚠️ Provedor {provider_type.value} indisponível.")
            except Exception as e:
                config.available = False
                config.last_error = str(e)
                logger.error(f"❌ Erro testando provedor {provider_type.value}: {e}")
        
        if active_providers:
            self.status = "active"
            logger.info(f"🚀 {len(active_providers)} provedores ativos. Sistema quantum operacional.")
        else:
            self.status = "degraded"
            logger.critical("❌ NENHUM provedor de IA disponível! Sistema em modo degradado.")

    async def _test_provider_connection(self, provider_type: AIProvider, config: AIProviderConfig) -> bool:
        """Testa conexão com um provedor específico."""
        try:
            if provider_type == AIProvider.OPENAI and OPENAI_AVAILABLE:
                client = AsyncOpenAI(api_key=config.api_key, timeout=15.0)
                await client.models.list()
                return True
                
            elif provider_type == AIProvider.ANTHROPIC and ANTHROPIC_AVAILABLE:
                client = anthropic.AsyncAnthropic(api_key=config.api_key)
                # Teste simples com o Claude
                response = await client.messages.create(
                    model=config.model,
                    max_tokens=10,
                    messages=[{"role": "user", "content": "Test"}]
                )
                return bool(response)
                
            elif provider_type == AIProvider.GOOGLE and GOOGLE_AVAILABLE:
                genai.configure(api_key=config.api_key)
                model = genai.GenerativeModel(config.model)
                # Teste simples com Gemini
                response = await model.generate_content_async("Test")
                return bool(response)
                
        except Exception as e:
            logger.debug(f"Teste de conexão falhou para {provider_type.value}: {e}")
            
        return False

    def _determine_task_complexity(self, user_prompt: str) -> TaskComplexity:
        """Determina a complexidade da tarefa baseada no prompt."""
        prompt_lower = user_prompt.lower()
        
        # Indicadores de alta complexidade
        complex_indicators = [
            "análise avançada", "múltiplos passos", "integração", "otimização",
            "estratégia", "planejamento detalhado", "considerando", "levando em conta"
        ]
        
        # Indicadores de complexidade moderada
        moderate_indicators = [
            "criar", "gerar", "desenvolver", "pesquisar", "analisar", "comparar"
        ]
        
        if any(indicator in prompt_lower for indicator in complex_indicators):
            return TaskComplexity.COMPLEX
        elif any(indicator in prompt_lower for indicator in moderate_indicators):
            return TaskComplexity.MODERATE
        else:
            return TaskComplexity.SIMPLE

    def _select_optimal_provider(self, complexity: TaskComplexity, preferred: Optional[AIProvider] = None) -> Optional[AIProvider]:
        """Seleciona o provedor optimal baseado na complexidade e performance."""
        available_providers = [p for p, config in self.providers.items() if config.available]
        
        if not available_providers:
            return None
        
        # Usa provedor preferido se disponível
        if preferred and preferred in available_providers:
            return preferred
        
        # Seleção baseada na complexidade e performance
        if complexity in [TaskComplexity.COMPLEX, TaskComplexity.EXPERT]:
            # Para tarefas complexas, prioriza OpenAI GPT-4
            if AIProvider.OPENAI in available_providers:
                return AIProvider.OPENAI
            elif AIProvider.ANTHROPIC in available_providers:
                return AIProvider.ANTHROPIC
        
        # Para outras tarefas, seleciona baseado em performance (tempo de resposta)
        best_provider = min(
            available_providers,
            key=lambda p: (
                sum(self.providers[p].response_times[-10:]) / len(self.providers[p].response_times[-10:])
                if self.providers[p].response_times else 1.0
            )
        )
        
        return best_provider

    def _generate_cache_key(self, user_prompt: str, context: Dict[str, Any]) -> str:
        """Gera chave de cache para a requisição."""
        content = f"{user_prompt}_{json.dumps(context, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()

    async def _create_quantum_plan(self, request: PlanningRequest) -> PlanningResponse:
        """Cria um plano quantum usando o provedor optimal."""
        start_time = time.time()
        
        # Verifica cache primeiro
        cache_key = self._generate_cache_key(request.user_prompt, request.context)
        if cache_key in self.request_cache:
            cached_response = self.request_cache[cache_key]
            logger.info(f"🚀 Usando resposta em cache para requisição similar.")
            return cached_response
        
        # Seleciona provedor optimal
        provider_type = self._select_optimal_provider(request.complexity, request.preferred_provider)
        if not provider_type:
            raise Exception("Nenhum provedor de IA disponível")
        
        provider_config = self.providers[provider_type]
        
        try:
            # Executa planejamento com o provedor selecionado
            plan_data = await self._execute_planning_with_provider(
                provider_type, provider_config, request.user_prompt
            )
            
            response_time = (time.time() - start_time) * 1000
            
            # Valida o plano gerado
            validation_passed, confidence = self._validate_quantum_plan(plan_data, request.user_prompt)
            
            response = PlanningResponse(
                request_id=request.request_id,
                plan=plan_data,
                provider_used=provider_type,
                model_used=provider_config.model,
                response_time_ms=response_time,
                confidence_score=confidence,
                validation_passed=validation_passed
            )
            
            # Atualiza métricas
            provider_config.response_times.append(response_time)
            if len(provider_config.response_times) > 50:
                provider_config.response_times = provider_config.response_times[-50:]
            
            # Cache se validação passou
            if validation_passed:
                self.request_cache[cache_key] = response
                if len(self.request_cache) > 100:  # Limite do cache
                    oldest_key = min(self.request_cache.keys())
                    del self.request_cache[oldest_key]
            
            return response
            
        except Exception as e:
            provider_config.available = False
            provider_config.last_error = str(e)
            logger.error(f"❌ Provedor {provider_type.value} falhou: {e}")
            
            # Tenta com próximo provedor disponível
            remaining_providers = [p for p, c in self.providers.items() if c.available and p != provider_type]
            if remaining_providers:
                request.preferred_provider = remaining_providers[0]
                return await self._create_quantum_plan(request)
            else:
                raise Exception(f"Todos os provedores falharam. Último erro: {e}")

    async def _execute_planning_with_provider(self, provider_type: AIProvider, config: AIProviderConfig, user_prompt: str) -> List[Dict]:
        """Executa planejamento com um provedor específico."""
        
        if provider_type == AIProvider.OPENAI:
            client = AsyncOpenAI(api_key=config.api_key, timeout=30.0)
            response = await client.chat.completions.create(
                model=config.model,
                messages=[
                    {"role": "system", "content": QUANTUM_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
            content = response.choices[0].message.content
            
        elif provider_type == AIProvider.ANTHROPIC:
            client = anthropic.AsyncAnthropic(api_key=config.api_key)
            response = await client.messages.create(
                model=config.model,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                messages=[
                    {"role": "user", "content": f"{QUANTUM_SYSTEM_PROMPT}\n\nTarefa: {user_prompt}"}
                ]
            )
            content = response.content[0].text
            
        elif provider_type == AIProvider.GOOGLE:
            genai.configure(api_key=config.api_key)
            model = genai.GenerativeModel(config.model)
            prompt = f"{QUANTUM_SYSTEM_PROMPT}\n\nTarefa: {user_prompt}"
            response = await model.generate_content_async(prompt)
            content = response.text
            
        else:
            raise Exception(f"Provedor {provider_type.value} não suportado")
        
        # Parse da resposta JSON
        try:
            parsed_response = json.loads(content)
            if "plan" not in parsed_response:
                raise ValueError("Resposta não contém chave 'plan'")
            return parsed_response["plan"]
        except json.JSONDecodeError as e:
            # Tenta extrair JSON se estiver embutido em texto
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                parsed_response = json.loads(json_match.group())
                return parsed_response.get("plan", [])
            raise Exception(f"Falha ao parsear resposta JSON: {e}")

    def _validate_quantum_plan(self, plan: List[Dict], original_prompt: str) -> Tuple[bool, float]:
        """Valida se o plano gerado atende aos critérios quantum."""
        if not plan or not isinstance(plan, list):
            return False, 0.0
        
        validation_score = 0.0
        max_score = 6.0
        
        # 1. Verifica se tem passos sequenciais
        if len(plan) > 0:
            validation_score += 1.0
        
        # 2. Verifica se cada passo tem campos obrigatórios
        required_fields = ["step", "description", "agent", "task"]
        valid_steps = 0
        for step in plan:
            if all(field in step for field in required_fields):
                valid_steps += 1
        
        if valid_steps == len(plan):
            validation_score += 1.0
        
        # 3. Verifica se usa agentes válidos
        valid_agents = [
            "web_search_001", "content_creator_001", "notification_001",
            "image_generator_001", "data_analyzer_001", "visualization_001"
        ]
        uses_valid_agents = all(
            step.get("agent") in valid_agents for step in plan
        )
        if uses_valid_agents:
            validation_score += 1.0
        
        # 4. Verifica se o plano parece completo (tem início, meio, fim)
        if len(plan) >= 2:  # Pelo menos 2 passos
            validation_score += 1.0
        
        # 5. Verifica se inclui passo de notificação para entregas
        has_notification = any(
            step.get("agent") == "notification_001" for step in plan
        )
        if "email" in original_prompt.lower() or "enviar" in original_prompt.lower():
            if has_notification:
                validation_score += 1.0
        else:
            validation_score += 0.5  # Bonus parcial se não é obrigatório
        
        # 6. Verifica se tem estratégias de fallback (campo opcional mas desejável)
        has_fallback_strategies = any(
            "fallback_strategy" in step for step in plan
        )
        if has_fallback_strategies:
            validation_score += 1.0
        
        confidence = validation_score / max_score
        validation_passed = confidence >= 0.7  # 70% de confiança mínima
        
        return validation_passed, confidence

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de planejamento quantum."""
        if message.message_type != MessageType.REQUEST:
            return
        
        if self.status != "active":
            await self.publish_error_response(
                message, 
                f"Analisador de IA Quantum não está operacional. Status: {self.status.upper()}"
            )
            return
        
        user_request = message.content.get("content")
        if not user_request:
            await self.publish_error_response(message, "Conteúdo da requisição está vazio.")
            return
        
        request_id = message.message_id
        logger.info(f"🧠 [Quantum AI] Processando requisição '{request_id}': '{user_request[:100]}...'")
        
        try:
            # Cria estrutura de requisição
            planning_request = PlanningRequest(
                request_id=request_id,
                user_prompt=user_request,
                complexity=self._determine_task_complexity(user_request),
                context=message.content.get("context", {})
            )
            
            self.active_requests[request_id] = planning_request
            
            # Gera plano quantum
            planning_response = await self._create_quantum_plan(planning_request)
            
            # Atualiza métricas
            self.performance_metrics["total_requests"] += 1
            if planning_response.validation_passed:
                self.performance_metrics["successful_plans"] += 1
            
            provider_used = planning_response.provider_used.value
            self.performance_metrics["provider_usage"][provider_used] = (
                self.performance_metrics["provider_usage"].get(provider_used, 0) + 1
            )
            
            # Resposta de sucesso
            response_content = {
                "status": "success",
                "plan": planning_response.plan,
                "provider_used": provider_used,
                "response_time_ms": planning_response.response_time_ms,
                "confidence_score": planning_response.confidence_score,
                "validation_passed": planning_response.validation_passed
            }
            
            await self.publish_response(message, response_content)
            logger.info(f"🧠 [Quantum AI] Plano gerado com sucesso usando {provider_used} (confiança: {planning_response.confidence_score:.2f})")
            
        except Exception as e:
            self.performance_metrics["failed_requests"] += 1
            logger.error(f"❌ [Quantum AI] Erro ao processar requisição: {e}", exc_info=True)
            await self.publish_error_response(message, f"Erro no Analisador Quantum: {e}")
        
        finally:
            # Cleanup
            if request_id in self.active_requests:
                del self.active_requests[request_id]

    def get_quantum_metrics(self) -> Dict[str, Any]:
        """Retorna métricas quantum do sistema."""
        total_requests = self.performance_metrics["total_requests"]
        uptime = datetime.now() - self.performance_metrics["uptime_start"]
        
        # Calcula tempo médio de resposta
        all_response_times = []
        for config in self.providers.values():
            all_response_times.extend(config.response_times)
        
        avg_response_time = (
            sum(all_response_times) / len(all_response_times)
            if all_response_times else 0.0
        )
        
        return {
            **self.performance_metrics,
            "uptime_seconds": uptime.total_seconds(),
            "avg_response_time_ms": avg_response_time,
            "success_rate": (
                self.performance_metrics["successful_plans"] / total_requests
                if total_requests > 0 else 1.0
            ),
            "active_providers": len([p for p, c in self.providers.items() if c.available]),
            "total_providers": len(self.providers),
            "cache_size": len(self.request_cache),
            "active_requests": len(self.active_requests)
        }

def create_ai_agents(message_bus) -> List[BaseNetworkAgent]:
    """Cria os agentes de IA Quantum."""
    agents = []
    logger.info("🧠 Criando QuantumAIAnalyzerAgent...")
    try:
        agent = QuantumAIAnalyzerAgent("ai_analyzer_001", message_bus)
        agents.append(agent)
        logger.info("✅ QuantumAIAnalyzerAgent criado com sucesso.")
    except Exception as e:
        logger.error(f"❌ Erro crítico criando QuantumAIAnalyzerAgent: {e}", exc_info=True)
    return agents

def create_agents():
    """Função esperada pelo sistema de bootstrap para carregamento automático."""
    agents = []
    logger.info("🧠 Criando QuantumAIAnalyzerAgent...")
    try:
        agent = QuantumAIAnalyzerAgent("ai_analyzer_001", message_bus=None)
        agents.append(agent)
        logger.info("✅ QuantumAIAnalyzerAgent criado com sucesso.")
    except Exception as e:
        logger.error(f"❌ Erro crítico criando QuantumAIAnalyzerAgent: {e}", exc_info=True)
    return agents
