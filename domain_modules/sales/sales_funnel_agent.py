"""
ALSHAM QUANTUM - Sales Funnel Agent (Sales Module)
Versão Nativa - Sem dependências SUNA-ALSHAM
Corrigido em: 07/08/2025

Agente especializado em:
- Análise completa do funil de vendas
- Identificação de estágios de leads
- Otimização de conversão por estágio
- Análise de jornada do cliente
- Automação de next best actions
"""

import asyncio
import json
import logging
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from decimal import Decimal
import uuid
import math
import numpy as np
from collections import defaultdict, Counter

class BaseNetworkAgent:
    """Classe base nativa para agentes da rede ALSHAM QUANTUM"""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.active = True
        self.logger = logging.getLogger(f"alsham_quantum.{agent_id}")
        
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Método base para processamento - deve ser sobrescrito"""
        raise NotImplementedError
        
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "active": self.active,
            "timestamp": datetime.now().isoformat()
        }

class FunnelStage(Enum):
    """Estágios do funil de vendas"""
    AWARENESS = "awareness"          # Topo do funil - consciência
    INTEREST = "interest"            # Interesse demonstrado
    CONSIDERATION = "consideration"   # Meio do funil - consideração
    INTENT = "intent"                # Intenção de compra
    EVALUATION = "evaluation"        # Avaliação/comparação
    PURCHASE = "purchase"            # Fundo do funil - compra
    RETENTION = "retention"          # Pós-venda - retenção
    ADVOCACY = "advocacy"            # Cliente promotor

class LeadScore(Enum):
    """Classificação de score do lead"""
    COLD = "cold"          # 0-25
    WARM = "warm"          # 26-50
    HOT = "hot"            # 51-75
    QUALIFIED = "qualified" # 76-100

class ActionType(Enum):
    """Tipos de ação recomendada"""
    NURTURE = "nurture"
    EDUCATE = "educate"
    ENGAGE = "engage"
    QUALIFY = "qualify"
    DEMO = "demo"
    PROPOSAL = "proposal"
    NEGOTIATE = "negotiate"
    CLOSE = "close"
    ONBOARD = "onboard"
    UPSELL = "upsell"

class ChannelPreference(Enum):
    """Preferências de canal"""
    EMAIL = "email"
    PHONE = "phone"
    SOCIAL = "social"
    WEBSITE = "website"
    WEBINAR = "webinar"
    IN_PERSON = "in_person"
    CHAT = "chat"

@dataclass
class LeadProfile:
    """Perfil completo do lead"""
    lead_id: str
    name: str
    email: str
    company: str
    role: str
    industry: str
    company_size: str
    current_stage: FunnelStage
    lead_score: int
    engagement_score: float
    intent_signals: List[str]
    interaction_history: List[Dict[str, Any]]
    channel_preferences: List[ChannelPreference]
    pain_points: List[str]
    budget_range: str
    decision_timeline: str
    decision_makers: List[str]

@dataclass
class FunnelAnalysis:
    """Análise completa do funil"""
    analysis_id: str
    lead_id: str
    current_stage: FunnelStage
    stage_confidence: float
    progression_probability: Dict[FunnelStage, float]
    bottlenecks: List[str]
    acceleration_opportunities: List[str]
    estimated_time_to_close: str
    conversion_likelihood: float

@dataclass
class NextBestAction:
    """Próxima melhor ação recomendada"""
    action_type: ActionType
    priority: int
    title: str
    description: str
    channel: ChannelPreference
    timing: str
    expected_outcome: str
    success_metrics: List[str]
    resources_needed: List[str]
    automation_possible: bool

@dataclass
class FunnelMetrics:
    """Métricas do funil de vendas"""
    stage_conversion_rates: Dict[str, float]
    average_time_in_stage: Dict[str, int]  # dias
    total_leads: int
    qualified_leads: int
    closed_won: int
    overall_conversion_rate: float
    revenue_generated: Decimal
    pipeline_velocity: float

@dataclass
class StageOptimization:
    """Otimização por estágio"""
    stage: FunnelStage
    current_conversion_rate: float
    benchmark_conversion_rate: float
    improvement_potential: float
    optimization_tactics: List[str]
    estimated_impact: str

class SalesFunnelAgent(BaseNetworkAgent):
    """Agente de Funil de Vendas nativo do ALSHAM QUANTUM"""
    
    def __init__(self):
        super().__init__("sales_funnel_agent", "Sales Funnel Agent")
        
        # Configurações de análise do funil
        self.funnel_config = {
            "stages_order": [
                FunnelStage.AWARENESS,
                FunnelStage.INTEREST, 
                FunnelStage.CONSIDERATION,
                FunnelStage.INTENT,
                FunnelStage.EVALUATION,
                FunnelStage.PURCHASE,
                FunnelStage.RETENTION,
                FunnelStage.ADVOCACY
            ],
            "benchmark_conversion_rates": {
                "awareness_to_interest": 0.15,
                "interest_to_consideration": 0.25,
                "consideration_to_intent": 0.30,
                "intent_to_evaluation": 0.40,
                "evaluation_to_purchase": 0.20,
                "purchase_to_retention": 0.80,
                "retention_to_advocacy": 0.15
            },
            "average_stage_duration": {  # em dias
                FunnelStage.AWARENESS: 7,
                FunnelStage.INTEREST: 14,
                FunnelStage.CONSIDERATION: 21,
                FunnelStage.INTENT: 14,
                FunnelStage.EVALUATION: 30,
                FunnelStage.PURCHASE: 7,
                FunnelStage.RETENTION: 90,
                FunnelStage.ADVOCACY: 365
            }
        }
        
        # Scoring de leads
        self.scoring_weights = {
            "demographic": 0.20,    # empresa, cargo, indústria
            "behavioral": 0.30,     # interações, downloads, tempo no site
            "engagement": 0.25,     # email opens, clicks, responses
            "intent": 0.25         # demo requests, pricing inquiries
        }
        
        # Cache de análises
        self.funnel_cache = {}
        
        # Base de conhecimento de sinais de intenção
        self.intent_signals = {
            "high_intent": [
                "demo_request", "pricing_inquiry", "trial_signup",
                "contact_sales", "rfi_submission", "competitor_comparison"
            ],
            "medium_intent": [
                "whitepaper_download", "case_study_view", "webinar_attendance",
                "multiple_page_views", "email_engagement", "social_engagement"
            ],
            "low_intent": [
                "blog_visit", "newsletter_signup", "single_page_view",
                "social_follow", "organic_search"
            ]
        }
        
        self.logger.info("Sales Funnel Agent inicializado com engine nativo")

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisições de análise de funil"""
        try:
            action = data.get("action", "analyze_lead_stage")
            
            if action == "analyze_lead_stage":
                return await self._analyze_lead_stage(data)
            elif action == "funnel_analysis":
                return await self._comprehensive_funnel_analysis(data)
            elif action == "stage_optimization":
                return await self._analyze_stage_optimization(data)
            elif action == "next_best_action":
                return await self._recommend_next_best_action(data)
            elif action == "lead_scoring":
                return await self._calculate_lead_score(data)
            elif action == "conversion_prediction":
                return await self._predict_conversion_probability(data)
            elif action == "pipeline_velocity":
                return await self._analyze_pipeline_velocity(data)
            elif action == "funnel_metrics":
                return await self._calculate_funnel_metrics(data)
            elif action == "journey_mapping":
                return await self._map_customer_journey(data)
            else:
                return {"error": f"Ação não reconhecida: {action}"}
                
        except Exception as e:
            self.logger.error(f"Erro na análise de funil: {str(e)}")
            return {"error": str(e)}

    async def _analyze_lead_stage(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise principal de estágio do lead"""
        
        # Construir perfil do lead
        lead_profile = self._build_lead_profile(data)
        
        # Análise de estágio atual
        stage_analysis = await self._determine_current_stage(lead_profile)
        
        # Calcular score do lead
        lead_score = self._calculate_comprehensive_lead_score(lead_profile)
        
        # Próxima melhor ação
        next_action = await self._determine_next_best_action(lead_profile, stage_analysis)
        
        # Predição de progressão
        progression_prediction = self._predict_stage_progression(lead_profile, stage_analysis)
        
        # Salvar no cache
        analysis_id = str(uuid.uuid4())
        self.funnel_cache[analysis_id] = {
            "lead_profile": asdict(lead_profile),
            "stage_analysis": asdict(stage_analysis),
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "analysis_id": analysis_id,
            "lead_id": lead_profile.lead_id,
            "lead_profile": {
                "name": lead_profile.name,
                "company": lead_profile.company,
                "role": lead_profile.role,
                "industry": lead_profile.industry,
                "company_size": lead_profile.company_size
            },
            "current_stage": {
                "stage": stage_analysis.current_stage.value,
                "confidence": stage_analysis.stage_confidence,
                "time_in_stage": self._estimate_time_in_stage(lead_profile),
                "typical_duration": self.funnel_config["average_stage_duration"][stage_analysis.current_stage]
            },
            "lead_scoring": {
                "total_score": lead_score,
                "classification": self._classify_lead_score(lead_score).value,
                "score_breakdown": self._get_score_breakdown(lead_profile)
            },
            "progression_analysis": {
                "next_likely_stage": max(progression_prediction, key=progression_prediction.get).value if progression_prediction else None,
                "progression_probabilities": {stage.value: prob for stage, prob in progression_prediction.items()},
                "estimated_time_to_close": stage_analysis.estimated_time_to_close,
                "conversion_likelihood": stage_analysis.conversion_likelihood
            },
            "next_best_action": {
                "action_type": next_action.action_type.value,
                "priority": next_action.priority,
                "title": next_action.title,
                "description": next_action.description,
                "recommended_channel": next_action.channel.value,
                "timing": next_action.timing,
                "expected_outcome": next_action.expected_outcome,
                "automation_possible": next_action.automation_possible
            },
            "insights": {
                "key_signals": lead_profile.intent_signals,
                "pain_points": lead_profile.pain_points,
                "bottlenecks": stage_analysis.bottlenecks,
                "opportunities": stage_analysis.acceleration_opportunities
            },
            "recommendations": self._generate_strategic_recommendations(lead_profile, stage_analysis),
            "timestamp": datetime.now().isoformat()
        }

    async def _determine_current_stage(self, lead_profile: LeadProfile) -> FunnelAnalysis:
        """Determina estágio atual do lead com IA nativa"""
        
        # Analisar sinais de intenção
        intent_score = self._calculate_intent_score(lead_profile.intent_signals)
        
        # Analisar histórico de interações
        engagement_depth = self._analyze_engagement_depth(lead_profile.interaction_history)
        
        # Determinar estágio baseado em regras e ML simulado
        stage_scores = {}
        
        # AWARENESS - sinais iniciais
        awareness_score = 0.0
        if any(signal in ["blog_visit", "newsletter_signup", "social_follow"] for signal in lead_profile.intent_signals):
            awareness_score += 0.6
        if engagement_depth["total_interactions"] <= 3:
            awareness_score += 0.4
        stage_scores[FunnelStage.AWARENESS] = awareness_score
        
        # INTEREST - demonstração de interesse
        interest_score = 0.0
        if any(signal in ["whitepaper_download", "webinar_attendance"] for signal in lead_profile.intent_signals):
            interest_score += 0.7
        if engagement_depth["email_engagement"] > 0.3:
            interest_score += 0.3
        stage_scores[FunnelStage.INTEREST] = interest_score
        
        # CONSIDERATION - avaliação ativa
        consideration_score = 0.0
        if any(signal in ["case_study_view", "multiple_page_views"] for signal in lead_profile.intent_signals):
            consideration_score += 0.6
        if engagement_depth["content_depth"] > 0.5:
            consideration_score += 0.4
        stage_scores[FunnelStage.CONSIDERATION] = consideration_score
        
        # INTENT - intenção clara
        intent_score_stage = 0.0
        if any(signal in ["demo_request", "trial_signup"] for signal in lead_profile.intent_signals):
            intent_score_stage += 0.8
        if lead_profile.budget_range != "unknown":
            intent_score_stage += 0.2
        stage_scores[FunnelStage.INTENT] = intent_score_stage
        
        # EVALUATION - comparação ativa
        evaluation_score = 0.0
        if any(signal in ["pricing_inquiry", "competitor_comparison"] for signal in lead_profile.intent_signals):
            evaluation_score += 0.7
        if len(lead_profile.decision_makers) > 1:
            evaluation_score += 0.3
        stage_scores[FunnelStage.EVALUATION] = evaluation_score
        
        # PURCHASE - pronto para comprar
        purchase_score = 0.0
        if any(signal in ["contact_sales", "rfi_submission"] for signal in lead_profile.intent_signals):
            purchase_score += 0.9
        if lead_profile.decision_timeline in ["immediate", "this_month"]:
            purchase_score += 0.1
        stage_scores[FunnelStage.PURCHASE] = purchase_score
        
        # Determinar estágio com maior score
        current_stage = max(stage_scores, key=stage_scores.get)
        stage_confidence = stage_scores[current_stage]
        
        # Calcular progressão para próximos estágios
        current_index = self.funnel_config["stages_order"].index(current_stage)
        progression_probabilities = {}
        
        for i, stage in enumerate(self.funnel_config["stages_order"][current_index:current_index+3]):
            if i == 0:
                progression_probabilities[stage] = stage_confidence
            else:
                base_conversion = list(self.funnel_config["benchmark_conversion_rates"].values())[min(current_index + i - 1, len(self.funnel_config["benchmark_conversion_rates"]) - 1)]
                progression_probabilities[stage] = stage_confidence * (base_conversion ** i)
        
        # Identificar bottlenecks e oportunidades
        bottlenecks = self._identify_bottlenecks(lead_profile, current_stage)
        opportunities = self._identify_acceleration_opportunities(lead_profile, current_stage)
        
        # Estimar tempo para fechamento
        stages_remaining = len(self.funnel_config["stages_order"]) - current_index - 1
        avg_time_remaining = sum(
            self.funnel_config["average_stage_duration"][stage] 
            for stage in self.funnel_config["stages_order"][current_index+1:current_index+4]  # Próximos 3 estágios
        )
        estimated_time_to_close = f"{avg_time_remaining} dias"
        
        # Calcular likelihood de conversão
        conversion_likelihood = stage_confidence * 0.7 + (intent_score / 100) * 0.3
        
        return FunnelAnalysis(
            analysis_id=str(uuid.uuid4()),
            lead_id=lead_profile.lead_id,
            current_stage=current_stage,
            stage_confidence=stage_confidence,
            progression_probability=progression_probabilities,
            bottlenecks=bottlenecks,
            acceleration_opportunities=opportunities,
            estimated_time_to_close=estimated_time_to_close,
            conversion_likelihood=conversion_likelihood
        )

    def _calculate_intent_score(self, intent_signals: List[str]) -> float:
        """Calcula score de intenção baseado nos sinais"""
        score = 0.0
        
        for signal in intent_signals:
            if signal in self.intent_signals["high_intent"]:
                score += 30
            elif signal in self.intent_signals["medium_intent"]:
                score += 15
            elif signal in self.intent_signals["low_intent"]:
                score += 5
                
        return min(100.0, score)

    def _analyze_engagement_depth(self, interaction_history: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analisa profundidade do engajamento"""
        if not interaction_history:
            return {
                "total_interactions": 0,
                "email_engagement": 0,
                "content_depth": 0,
                "recency_score": 0
            }
        
        total_interactions = len(interaction_history)
        
        # Calcular engajamento por email
        email_interactions = [i for i in interaction_history if i.get("type") == "email"]
        email_engagement = len(email_interactions) / max(1, total_interactions)
        
        # Calcular profundidade de conteúdo
        content_interactions = [i for i in interaction_history if i.get("type") in ["download", "view", "read"]]
        content_depth = len(content_interactions) / max(1, total_interactions)
        
        # Calcular score de recência
        if interaction_history:
            latest_interaction = max(interaction_history, key=lambda x: x.get("timestamp", "1900-01-01"))
            latest_date = datetime.fromisoformat(latest_interaction.get("timestamp", "1900-01-01"))
            days_since = (datetime.now() - latest_date).days
            recency_score = max(0, 1.0 - (days_since / 30))  # Decay over 30 days
        else:
            recency_score = 0
        
        return {
            "total_interactions": total_interactions,
            "email_engagement": email_engagement,
            "content_depth": content_depth,
            "recency_score": recency_score
        }

    def _calculate_comprehensive_lead_score(self, lead_profile: LeadProfile) -> int:
        """Calcula score abrangente do lead (0-100)"""
        score_components = {}
        
        # Score demográfico
        demographic_score = 0
        if lead_profile.company_size in ["enterprise", "large"]:
            demographic_score += 40
        elif lead_profile.company_size in ["medium"]:
            demographic_score += 25
        else:
            demographic_score += 10
            
        if lead_profile.role in ["ceo", "cto", "vp", "director"]:
            demographic_score += 35
        elif lead_profile.role in ["manager", "lead"]:
            demographic_score += 20
        else:
            demographic_score += 5
            
        if lead_profile.industry in ["technology", "finance", "healthcare"]:
            demographic_score += 25
        else:
            demographic_score += 15
            
        score_components["demographic"] = min(100, demographic_score)
        
        # Score comportamental
        behavioral_score = len(lead_profile.interaction_history) * 5
        behavioral_score += len(lead_profile.intent_signals) * 10
        score_components["behavioral"] = min(100, behavioral_score)
        
        # Score de engajamento
        engagement_score = lead_profile.engagement_score * 100
        score_components["engagement"] = min(100, engagement_score)
        
        # Score de intenção
        intent_score = self._calculate_intent_score(lead_profile.intent_signals)
        score_components["intent"] = intent_score
        
        # Score final ponderado
        final_score = sum(
            score_components[component] * self.scoring_weights[component]
            for component in score_components
        )
        
        return int(final_score)

    def _classify_lead_score(self, score: int) -> LeadScore:
        """Classifica o score do lead"""
        if score >= 76:
            return LeadScore.QUALIFIED
        elif score >= 51:
            return LeadScore.HOT
        elif score >= 26:
            return LeadScore.WARM
        else:
            return LeadScore.COLD

    def _get_score_breakdown(self, lead_profile: LeadProfile) -> Dict[str, int]:
        """Retorna breakdown detalhado do score"""
        return {
            "demographic": int(self._calculate_demographic_score(lead_profile)),
            "behavioral": int(len(lead_profile.interaction_history) * 5),
            "engagement": int(lead_profile.engagement_score * 100),
            "intent": int(self._calculate_intent_score(lead_profile.intent_signals))
        }

    def _calculate_demographic_score(self, lead_profile: LeadProfile) -> float:
        """Calcula score demográfico"""
        score = 0
        
        # Company size
        size_scores = {"enterprise": 40, "large": 35, "medium": 25, "small": 15, "startup": 10}
        score += size_scores.get(lead_profile.company_size, 10)
        
        # Role
        role_scores = {"ceo": 35, "cto": 35, "vp": 30, "director": 25, "manager": 20, "lead": 15}
        score += role_scores.get(lead_profile.role.lower(), 5)
        
        # Industry
        industry_scores = {"technology": 25, "finance": 25, "healthcare": 20, "manufacturing": 15}
        score += industry_scores.get(lead_profile.industry.lower(), 10)
        
        return min(100, score)

    async def _determine_next_best_action(self, lead_profile: LeadProfile, stage_analysis: FunnelAnalysis) -> NextBestAction:
        """Determina próxima melhor ação"""
        
        current_stage = stage_analysis.current_stage
        lead_score = self._calculate_comprehensive_lead_score(lead_profile)
        
        # Ações por estágio
        stage_actions = {
            FunnelStage.AWARENESS: {
                "action_type": ActionType.NURTURE,
                "title": "Nutrição com Conteúdo Educacional",
                "description": "Enviar série de emails com conteúdo educacional relevante",
                "channel": ChannelPreference.EMAIL,
                "timing": "Próximas 48h"
            },
            FunnelStage.INTEREST: {
                "action_type": ActionType.EDUCATE,
                "title": "Demonstração de Valor",
                "description": "Apresentar case studies e whitepapers específicos do setor",
                "channel": ChannelPreference.EMAIL,
                "timing": "Esta semana"
            },
            FunnelStage.CONSIDERATION: {
                "action_type": ActionType.ENGAGE,
                "title": "Engajamento Direto",
                "description": "Agendar call de discovery para entender necessidades",
                "channel": ChannelPreference.PHONE,
                "timing": "Próximos 3 dias"
            },
            FunnelStage.INTENT: {
                "action_type": ActionType.DEMO,
                "title": "Demonstração Personalizada",
                "description": "Agendar demo focado nas necessidades específicas",
                "channel": ChannelPreference.WEBINAR,
                "timing": "Esta semana"
            },
            FunnelStage.EVALUATION: {
                "action_type": ActionType.PROPOSAL,
                "title": "Proposta Comercial",
                "description": "Enviar proposta detalhada com pricing e implementação",
                "channel": ChannelPreference.EMAIL,
                "timing": "Próximos 2 dias"
            },
            FunnelStage.PURCHASE: {
                "action_type": ActionType.CLOSE,
                "title": "Fechamento da Venda",
                "description": "Call de fechamento com tomadores de decisão",
                "channel": ChannelPreference.PHONE,
                "timing": "Imediato"
            }
        }
        
        base_action = stage_actions.get(current_stage, stage_actions[FunnelStage.AWARENESS])
        
        # Ajustar baseado no score do lead
        if lead_score >= 75:  # Qualified lead
            priority = 1
            timing = "Imediato"
        elif lead_score >= 50:  # Hot lead
            priority = 2
            timing = base_action["timing"]
        else:  # Warm/Cold lead
            priority = 3
            timing = "Próxima semana"
            
        # Personalizar canal baseado em preferências
        preferred_channel = lead_profile.channel_preferences[0] if lead_profile.channel_preferences else base_action["channel"]
        
        return NextBestAction(
            action_type=base_action["action_type"],
            priority=priority,
            title=base_action["title"],
            description=base_action["description"],
            channel=preferred_channel,
            timing=timing,
            expected_outcome=self._predict_action_outcome(base_action["action_type"], current_stage),
            success_metrics=self._define_action_metrics(base_action["action_type"]),
            resources_needed=self._identify_required_resources(base_action["action_type"]),
            automation_possible=self._assess_automation_potential(base_action["action_type"], current_stage)
        )

    def _predict_action_outcome(self, action_type: ActionType, current_stage: FunnelStage) -> str:
        """Prediz resultado esperado da ação"""
        outcomes = {
            ActionType.NURTURE: "Aumentar engajamento e mover para estágio Interest",
            ActionType.EDUCATE: "Demonstrar valor e gerar interest qualified",
            ActionType.ENGAGE: "Qualificar necessidades e agendar próximos passos",
            ActionType.DEMO: "Demonstrar fit e avançar para evaluation",
            ActionType.PROPOSAL: "Formalizar proposta e acelerar decisão",
            ActionType.CLOSE: "Finalizar venda e iniciar onboarding"
        }
        return outcomes.get(action_type, "Progredir no funil de vendas")

    def _define_action_metrics(self, action_type: ActionType) -> List[str]:
        """Define métricas de sucesso da ação"""
        metrics_map = {
            ActionType.NURTURE: ["email_open_rate", "click_through_rate", "content_engagement"],
            ActionType.EDUCATE: ["content_downloads", "time_on_page", "follow_up_requests"],
            ActionType.ENGAGE: ["call_conversion", "discovery_completion", "qualification_score"],
            ActionType.DEMO: ["demo_attendance", "feature_interest", "next_step_commitment"],
            ActionType.PROPOSAL: ["proposal_review", "stakeholder_engagement", "objection_handling"],
            ActionType.CLOSE: ["decision_timeline", "contract_negotiation", "close_rate"]
        }
        return metrics_map.get(action_type, ["engagement_rate"])

    def _identify_required_resources(self, action_type: ActionType) -> List[str]:
        """Identifica recursos necessários"""
        resources_map = {
            ActionType.NURTURE: ["marketing_automation", "content_library", "email_templates"],
            ActionType.EDUCATE: ["case_studies", "whitepapers", "industry_research"],
            ActionType.ENGAGE: ["sales_rep_time", "discovery_framework", "CRM_tracking"],
            ActionType.DEMO: ["demo_environment", "technical_specialist", "presentation_slides"],
            ActionType.PROPOSAL: ["pricing_calculator", "legal_templates", "implementation_plan"],
            ActionType.CLOSE: ["senior_sales_rep", "negotiation_authority", "contract_templates"]
        }
        return resources_map.get(action_type, ["basic_resources"])

    def _assess_automation_potential(self, action_type: ActionType, current_stage: FunnelStage) -> bool:
        """Avalia potencial de automação"""
        high_automation_actions = [ActionType.NURTURE, ActionType.EDUCATE]
        return action_type in high_automation_actions and current_stage in [FunnelStage.AWARENESS, FunnelStage.INTEREST]

    def _predict_stage_progression(self, lead_profile: LeadProfile, stage_analysis: FunnelAnalysis) -> Dict[FunnelStage, float]:
        """Prediz probabilidade de progressão"""
        return stage_analysis.progression_probability

    def _identify_bottlenecks(self, lead_profile: LeadProfile, current_stage: FunnelStage) -> List[str]:
        """Identifica bottlenecks específicos"""
        bottlenecks = []
        
        if lead_profile.engagement_score < 0.3:
            bottlenecks.append("Baixo engajamento com conteúdo")
            
        if not lead_profile.budget_range or lead_profile.budget_range == "unknown":
            bottlenecks.append("Budget não qualificado")
            
        if not lead_profile.decision_makers:
            bottlenecks.append("Decision makers não identificados")
            
        if lead_profile.decision_timeline == "unknown":
            bottlenecks.append("Timeline de decisão indefinido")
            
        if current_stage in [FunnelStage.EVALUATION, FunnelStage.PURCHASE] and len(lead_profile.pain_points) < 2:
            bottlenecks.append("Pain points insuficientemente qualificados")
            
        return bottlenecks

    def _identify_acceleration_opportunities(self, lead_profile: LeadProfile, current_stage: FunnelStage) -> List[str]:
        """Identifica oportunidades de aceleração"""
        opportunities = []
        
        if len(lead_profile.intent_signals) >= 3:
            opportunities.append("Múltiplos sinais de interesse - acelerar follow-up")
            
        if lead_profile.engagement_score > 0.7:
            opportunities.append("Alto engajamento - oportunidade de upsell")
            
        if lead_profile.company_size in ["enterprise", "large"]:
            opportunities.append("Cliente enterprise - priorizar recursos sênior")
            
        if any(signal in ["demo_request", "pricing_inquiry"] for signal in lead_profile.intent_signals):
            opportunities.append("Sinais de compra - acelerar processo comercial")
            
        return opportunities

    def _estimate_time_in_stage(self, lead_profile: LeadProfile) -> int:
        """Estima tempo que o lead está no estágio atual"""
        if lead_profile.interaction_history:
            first_interaction = min(lead_profile.interaction_history, key=lambda x: x.get("timestamp", "2099-01-01"))
            first_date = datetime.fromisoformat(first_interaction.get("timestamp", "1900-01-01"))
            return (datetime.now() - first_date).days
        return 0

    def _generate_strategic_recommendations(self, lead_profile: LeadProfile, stage_analysis: FunnelAnalysis) -> List[str]:
        """Gera recomendações estratégicas"""
        recommendations = []
        
        if stage_analysis.conversion_likelihood > 0.7:
            recommendations.append("Lead de alta probabilidade - acelerar processo de vendas")
            
        if len(stage_analysis.bottlenecks) > 2:
            recommendations.append("Múltiplos bottlenecks identificados - implementar nurturing intensivo")
            
        if lead_profile.lead_score > 75:
            recommendations.append("Lead qualificado - alocar recursos sênior")
            
        return recommendations

    def _build_lead_profile(self, data: Dict[str, Any]) -> LeadProfile:
        """Constrói perfil completo do lead"""
        lead_data = data.get("lead_data", {})
        
        return LeadProfile(
            lead_id=lead_data.get("id", str(uuid.uuid4())),
            name=lead_data.get("name", "Unknown"),
            email=lead_data.get("email", "unknown@email.com"),
            company=lead_data.get("company", "Unknown Company"),
            role=lead_data.get("role", "unknown"),
            industry=lead_data.get("industry", "unknown"),
            company_size=lead_data.get("company_size", "unknown"),
            current_stage=FunnelStage(lead_data.get("current_stage", "awareness")),
            lead_score=lead_data.get("lead_score", 0),
            engagement_score=float(lead_data.get("engagement_score", 0.5)),
            intent_signals=lead_data.get("intent_signals", []),
            interaction_history=lead_data.get("interaction_history", []),
            channel_preferences=[ChannelPreference(ch) for ch in lead_data.get("channel_preferences", ["email"])],
            pain_points=lead_data.get("pain_points", []),
            budget_range=lead_data.get("budget_range", "unknown"),
            decision_timeline=lead_data.get("decision_timeline", "unknown"),
            decision_makers=lead_data.get("decision_makers", [])
        )

    async def _comprehensive_funnel_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise abrangente do funel para múltiplos leads"""
        leads_data = data.get("leads_data", [])
        
        if not leads_data:
            return {"error": "Nenhum dado de lead fornecido"}
            
        funnel_metrics = await self._calculate_comprehensive_funnel_metrics(leads_data)
        stage_optimization = await self._analyze_comprehensive_stage_optimization(leads_data)
        
        return {
            "analysis_id": str(uuid.uuid4()),
            "total_leads_analyzed": len(leads_data),
            "funnel_metrics": asdict(funnel_metrics),
            "stage_optimizations": [asdict(opt) for opt in stage_optimization],
            "strategic_insights": self._generate_funnel_insights(funnel_metrics, stage_optimization),
            "action_plan": self._create_funnel_action_plan(stage_optimization),
            "timestamp": datetime.now().isoformat()
        }

    async def _calculate_comprehensive_funnel_metrics(self, leads_data: List[Dict]) -> FunnelMetrics:
        """Calcula métricas abrangentes do funil"""
        
        # Contar leads por estágio
        stage_counts = defaultdict(int)
        qualified_leads = 0
        closed_won = 0
        total_revenue = Decimal("0")
        
        for lead in leads_data:
            stage = lead.get("current_stage", "awareness")
            stage_counts[stage] += 1
            
            if lead.get("lead_score", 0) >= 75:
                qualified_leads += 1
                
            if stage == "purchase":
                closed_won += 1
                revenue = lead.get("deal_value", 0)
                total_revenue += Decimal(str(revenue))
                
        # Calcular conversion rates
        total_leads = len(leads_data)
        stage_conversion_rates = {}
        
        funnel_stages = ["awareness", "interest", "consideration", "intent", "evaluation", "purchase"]
        for i in range(len(funnel_stages) - 1):
            current_stage = funnel_stages[i]
            next_stage = funnel_stages[i + 1]
            
            current_count = stage_counts[current_stage]
            next_count = sum(stage_counts[stage] for stage in funnel_stages[i+1:])
            
            if current_count > 0:
                conversion_rate = next_count / current_count
            else:
                conversion_rate = 0.0
                
            stage_conversion_rates[f"{current_stage}_to_{next_stage}"] = conversion_rate
        
        # Calcular métricas gerais
        overall_conversion_rate = closed_won / total_leads if total_leads > 0 else 0.0
        
        # Calcular pipeline velocity (simplificado)
        pipeline_velocity = closed_won / max(1, total_leads / 30)  # Assumindo 30 dias de ciclo
        
        # Average time in stage (simulado)
        average_time_in_stage = {
            stage.value: self.funnel_config["average_stage_duration"][stage] 
            for stage in FunnelStage
        }
        
        return FunnelMetrics(
            stage_conversion_rates=stage_conversion_rates,
            average_time_in_stage=average_time_in_stage,
            total_leads=total_leads,
            qualified_leads=qualified_leads,
            closed_won=closed_won,
            overall_conversion_rate=overall_conversion_rate,
            revenue_generated=total_revenue,
            pipeline_velocity=pipeline_velocity
        )

    async def _analyze_comprehensive_stage_optimization(self, leads_data: List[Dict]) -> List[StageOptimization]:
        """Analisa otimizações por estágio"""
        optimizations = []
        
        for stage in FunnelStage:
            # Leads neste estágio
            stage_leads = [lead for lead in leads_data if lead.get("current_stage") == stage.value]
            
            if not stage_leads:
                continue
                
            # Calcular conversion rate atual
            total_in_stage = len(stage_leads)
            converted = len([lead for lead in stage_leads if lead.get("converted", False)])
            current_conversion_rate = converted / total_in_stage if total_in_stage > 0 else 0.0
            
            # Benchmark rate
            benchmark_key = f"{stage.value}_conversion"
            benchmark_rate = list(self.funnel_config["benchmark_conversion_rates"].values())[
                min(list(FunnelStage).index(stage), len(self.funnel_config["benchmark_conversion_rates"]) - 1)
            ]
            
            # Improvement potential
            improvement_potential = max(0, benchmark_rate - current_conversion_rate)
            
            # Tactics baseados na análise dos leads
            optimization_tactics = self._generate_stage_tactics(stage, stage_leads)
            
            # Estimated impact
            estimated_impact = f"{improvement_potential * 100:.1f}% improvement potential"
            
            optimization = StageOptimization(
                stage=stage,
                current_conversion_rate=current_conversion_rate,
                benchmark_conversion_rate=benchmark_rate,
                improvement_potential=improvement_potential,
                optimization_tactics=optimization_tactics,
                estimated_impact=estimated_impact
            )
            
            optimizations.append(optimization)
            
        return optimizations

    def _generate_stage_tactics(self, stage: FunnelStage, stage_leads: List[Dict]) -> List[str]:
        """Gera táticas de otimização específicas por estágio"""
        tactics = []
        
        # Análise dos leads no estágio
        low_engagement_count = len([lead for lead in stage_leads if lead.get("engagement_score", 0.5) < 0.3])
        high_intent_count = len([lead for lead in stage_leads if len(lead.get("intent_signals", [])) >= 3])
        
        if stage == FunnelStage.AWARENESS:
            if low_engagement_count > len(stage_leads) * 0.5:
                tactics.append("Melhorar conteúdo inicial e onboarding")
            tactics.append("Implementar lead magnets mais atrativos")
            tactics.append("Otimizar canais de aquisição")
            
        elif stage == FunnelStage.INTEREST:
            tactics.append("Criar nurturing sequences personalizadas")
            tactics.append("Desenvolver conteúdo educacional segmentado")
            if high_intent_count > 0:
                tactics.append("Fast-track leads de alto intent")
                
        elif stage == FunnelStage.CONSIDERATION:
            tactics.append("Implementar social proof e case studies")
            tactics.append("Criar ferramentas de comparação")
            tactics.append("Oferecer trials ou demos gratuitas")
            
        elif stage == FunnelStage.EVALUATION:
            tactics.append("Acelerar processo de proposta")
            tactics.append("Melhorar materials de vendas")
            tactics.append("Implementar competitive battlecards")
            
        return tactics

    def _generate_funnel_insights(self, metrics: FunnelMetrics, optimizations: List[StageOptimization]) -> List[str]:
        """Gera insights estratégicos do funil"""
        insights = []
        
        # Insights de conversão
        if metrics.overall_conversion_rate < 0.1:
            insights.append("Conversion rate geral baixa - revisar qualificação de leads")
        elif metrics.overall_conversion_rate > 0.2:
            insights.append("Excelente performance de conversão - escalar aquisição")
            
        # Insights de estágios
        worst_performing_stage = min(optimizations, key=lambda x: x.current_conversion_rate)
        insights.append(f"Estágio com pior performance: {worst_performing_stage.stage.value}")
        
        # Insights de oportunidade
        total_improvement_potential = sum(opt.improvement_potential for opt in optimizations)
        if total_improvement_potential > 0.5:
            insights.append("Alto potencial de melhoria identificado - priorizar otimizações")
            
        return insights

    def _create_funnel_action_plan(self, optimizations: List[StageOptimization]) -> List[Dict[str, Any]]:
        """Cria plano de ação para otimização do funil"""
        action_plan = []
        
        # Priorizar por potencial de melhoria
        sorted_optimizations = sorted(optimizations, key=lambda x: x.improvement_potential, reverse=True)
        
        for i, optimization in enumerate(sorted_optimizations[:3]):  # Top 3
            action = {
                "priority": i + 1,
                "stage": optimization.stage.value,
                "focus_area": f"Improve {optimization.stage.value} conversion",
                "tactics": optimization.optimization_tactics[:2],  # Top 2 tactics
                "expected_impact": optimization.estimated_impact,
                "timeline": "4-6 semanas",
                "resources_needed": ["marketing_team", "sales_ops", "analytics"]
            }
            action_plan.append(action)
            
        return action_plan

def create_agents() -> List[SalesFunnelAgent]:
    """
    Função obrigatória para criação de agentes.
    Retorna lista de agentes Sales Funnel para o módulo Sales.
    """
    return [SalesFunnelAgent()]

# Função de inicialização para compatibilidade
def initialize_sales_funnel_agent():
    """Inicializa o agente Sales Funnel"""
    return SalesFunnelAgent()

# Ponto de entrada para testes
if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        agent = SalesFunnelAgent()
        
        # Dados de teste
        test_data = {
            "action": "analyze_lead_stage",
            "lead_data": {
                "id": "LEAD_001",
                "name": "João Silva",
                "email": "joao@empresa.com",
                "company": "TechCorp Ltda",
                "role": "CTO",
                "industry": "technology",
                "company_size": "medium",
                "current_stage": "consideration",
                "lead_score": 65,
                "engagement_score": 0.7,
                "intent_signals": ["whitepaper_download", "demo_request", "pricing_inquiry"],
                "interaction_history": [
                    {"type": "email", "timestamp": "2024-07-01", "action": "open"},
                    {"type": "download", "timestamp": "2024-07-15", "action": "whitepaper"},
                    {"type": "view", "timestamp": "2024-07-20", "action": "pricing_page"}
                ],
                "channel_preferences": ["email", "phone"],
                "pain_points": ["scalability", "integration"],
                "budget_range": "50k-100k",
                "decision_timeline": "this_quarter",
                "decision_makers": ["João Silva", "CEO"]
            }
        }
        
        result = await agent.process(test_data)
        print("Teste Sales Funnel Agent:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    # Executar teste
    asyncio.run(test_agent())
