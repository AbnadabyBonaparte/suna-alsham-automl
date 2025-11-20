"""
ALSHAM QUANTUM - Customer Success Agent (Sales Module)
Versão Nativa - Sem dependências SUNA-ALSHAM
Corrigido em: 07/08/2025

Agente especializado em:
- Análise de risco de churn de clientes
- Health scoring de contas
- Estratégias de retenção proativas
- Análise de engajamento e satisfação
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import statistics
import numpy as np
from collections import defaultdict

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

class ChurnRiskLevel(Enum):
    """Níveis de risco de churn"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class HealthScore(Enum):
    """Scores de saúde da conta"""
    EXCELLENT = "excellent"  # 90-100
    GOOD = "good"           # 75-89
    FAIR = "fair"           # 50-74
    POOR = "poor"           # 25-49
    CRITICAL = "critical"   # 0-24

@dataclass
class CustomerMetrics:
    """Métricas do cliente para análise"""
    customer_id: str
    last_login_days: int
    support_tickets_30d: int
    feature_usage_score: float
    payment_delays: int
    contract_value: float
    tenure_months: int
    nps_score: Optional[int] = None
    engagement_score: float = 0.0
    support_satisfaction: Optional[float] = None

@dataclass
class ChurnAnalysis:
    """Resultado da análise de churn"""
    customer_id: str
    risk_level: ChurnRiskLevel
    probability: float
    key_factors: List[str]
    recommended_actions: List[str]
    urgency_score: int  # 1-10

@dataclass
class HealthAnalysis:
    """Resultado da análise de saúde da conta"""
    customer_id: str
    health_score: HealthScore
    numeric_score: float
    strengths: List[str]
    concerns: List[str]
    improvement_areas: List[str]

class CustomerSuccessAgent(BaseNetworkAgent):
    """Agente Customer Success nativo do ALSHAM QUANTUM"""
    
    def __init__(self):
        super().__init__("customer_success_agent", "Customer Success Agent")
        
        # Configurações de análise
        self.churn_thresholds = {
            "high_risk_login_days": 14,
            "medium_risk_login_days": 7,
            "high_support_tickets": 5,
            "low_feature_usage": 0.3,
            "payment_delay_threshold": 2
        }
        
        # Pesos para cálculo de health score
        self.health_weights = {
            "engagement": 0.3,
            "feature_usage": 0.25,
            "support_satisfaction": 0.2,
            "payment_history": 0.15,
            "tenure": 0.1
        }
        
        # Cache para análises
        self.analysis_cache = {}
        
        self.logger.info("Customer Success Agent inicializado com engine nativo")

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisições de customer success"""
        try:
            action = data.get("action", "analyze_customer")
            
            if action == "analyze_customer":
                return await self._analyze_customer(data)
            elif action == "batch_churn_analysis":
                return await self._batch_churn_analysis(data)
            elif action == "health_check":
                return await self._health_check(data)
            elif action == "retention_strategy":
                return await self._generate_retention_strategy(data)
            elif action == "proactive_outreach":
                return await self._identify_proactive_outreach(data)
            else:
                return {"error": f"Ação não reconhecida: {action}"}
                
        except Exception as e:
            self.logger.error(f"Erro no processamento: {str(e)}")
            return {"error": str(e)}

    async def _analyze_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise completa de um cliente"""
        customer_data = data.get("customer_data", {})
        
        # Converter dados para métricas
        metrics = self._extract_metrics(customer_data)
        
        # Análise de churn
        churn_analysis = await self._analyze_churn_risk(metrics)
        
        # Análise de saúde
        health_analysis = await self._analyze_account_health(metrics)
        
        # Estratégias recomendadas
        strategies = await self._recommend_strategies(churn_analysis, health_analysis)
        
        return {
            "customer_id": metrics.customer_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "churn_analysis": {
                "risk_level": churn_analysis.risk_level.value,
                "probability": churn_analysis.probability,
                "key_factors": churn_analysis.key_factors,
                "urgency_score": churn_analysis.urgency_score
            },
            "health_analysis": {
                "health_score": health_analysis.health_score.value,
                "numeric_score": health_analysis.numeric_score,
                "strengths": health_analysis.strengths,
                "concerns": health_analysis.concerns,
                "improvement_areas": health_analysis.improvement_areas
            },
            "recommended_strategies": strategies,
            "next_review_date": (datetime.now() + timedelta(days=30)).isoformat()
        }

    async def _analyze_churn_risk(self, metrics: CustomerMetrics) -> ChurnAnalysis:
        """Analisa risco de churn do cliente"""
        risk_factors = []
        probability = 0.0
        
        # Análise de login recente
        if metrics.last_login_days > self.churn_thresholds["high_risk_login_days"]:
            risk_factors.append(f"Último login há {metrics.last_login_days} dias")
            probability += 0.25
        elif metrics.last_login_days > self.churn_thresholds["medium_risk_login_days"]:
            risk_factors.append(f"Login pouco frequente ({metrics.last_login_days} dias)")
            probability += 0.15
            
        # Análise de tickets de suporte
        if metrics.support_tickets_30d > self.churn_thresholds["high_support_tickets"]:
            risk_factors.append(f"Muitos tickets de suporte ({metrics.support_tickets_30d})")
            probability += 0.2
            
        # Análise de uso de features
        if metrics.feature_usage_score < self.churn_thresholds["low_feature_usage"]:
            risk_factors.append(f"Baixo uso de recursos ({metrics.feature_usage_score:.2f})")
            probability += 0.3
            
        # Análise de pagamentos
        if metrics.payment_delays > self.churn_thresholds["payment_delay_threshold"]:
            risk_factors.append(f"Atrasos em pagamentos ({metrics.payment_delays})")
            probability += 0.2
            
        # Análise de NPS
        if metrics.nps_score is not None and metrics.nps_score < 7:
            risk_factors.append(f"NPS baixo ({metrics.nps_score})")
            probability += 0.15
            
        # Determinar nível de risco
        if probability >= 0.7:
            risk_level = ChurnRiskLevel.CRITICAL
        elif probability >= 0.5:
            risk_level = ChurnRiskLevel.HIGH
        elif probability >= 0.3:
            risk_level = ChurnRiskLevel.MEDIUM
        else:
            risk_level = ChurnRiskLevel.LOW
            
        # Gerar ações recomendadas
        recommended_actions = self._generate_churn_actions(risk_factors, risk_level)
        
        # Calcular urgência (1-10)
        urgency_score = min(10, int(probability * 10) + 1)
        
        return ChurnAnalysis(
            customer_id=metrics.customer_id,
            risk_level=risk_level,
            probability=min(1.0, probability),
            key_factors=risk_factors,
            recommended_actions=recommended_actions,
            urgency_score=urgency_score
        )

    async def _analyze_account_health(self, metrics: CustomerMetrics) -> HealthAnalysis:
        """Analisa saúde geral da conta"""
        scores = {}
        strengths = []
        concerns = []
        improvement_areas = []
        
        # Score de engajamento
        engagement_score = max(0, 100 - (metrics.last_login_days * 5))
        scores["engagement"] = engagement_score / 100
        
        if engagement_score > 80:
            strengths.append("Alto engajamento com a plataforma")
        elif engagement_score < 40:
            concerns.append("Baixo engajamento")
            improvement_areas.append("Aumentar frequência de uso")
            
        # Score de uso de features
        scores["feature_usage"] = metrics.feature_usage_score
        if metrics.feature_usage_score > 0.7:
            strengths.append("Excelente adoção de recursos")
        elif metrics.feature_usage_score < 0.4:
            concerns.append("Subutilização de recursos")
            improvement_areas.append("Treinamento em recursos avançados")
            
        # Score de satisfação com suporte
        if metrics.support_satisfaction is not None:
            scores["support_satisfaction"] = metrics.support_satisfaction / 100
            if metrics.support_satisfaction > 80:
                strengths.append("Alta satisfação com suporte")
            elif metrics.support_satisfaction < 60:
                concerns.append("Insatisfação com suporte")
                improvement_areas.append("Melhorar qualidade do atendimento")
        else:
            scores["support_satisfaction"] = 0.5  # Neutro se não há dados
            
        # Score de histórico de pagamento
        payment_score = max(0, 100 - (metrics.payment_delays * 20)) / 100
        scores["payment_history"] = payment_score
        
        if payment_score > 0.9:
            strengths.append("Excelente histórico de pagamentos")
        elif payment_score < 0.6:
            concerns.append("Problemas com pagamentos")
            improvement_areas.append("Revisar condições de pagamento")
            
        # Score de tenure (estabilidade)
        tenure_score = min(1.0, metrics.tenure_months / 24)  # Normaliza para 24 meses
        scores["tenure"] = tenure_score
        
        if metrics.tenure_months > 12:
            strengths.append("Cliente estabelecido e leal")
        elif metrics.tenure_months < 3:
            concerns.append("Cliente novo - período crítico")
            improvement_areas.append("Acompanhamento intensivo de onboarding")
            
        # Calcular score final
        final_score = sum(
            scores[key] * self.health_weights[key] 
            for key in scores
        ) * 100
        
        # Determinar categoria de saúde
        if final_score >= 90:
            health_score = HealthScore.EXCELLENT
        elif final_score >= 75:
            health_score = HealthScore.GOOD
        elif final_score >= 50:
            health_score = HealthScore.FAIR
        elif final_score >= 25:
            health_score = HealthScore.POOR
        else:
            health_score = HealthScore.CRITICAL
            
        return HealthAnalysis(
            customer_id=metrics.customer_id,
            health_score=health_score,
            numeric_score=final_score,
            strengths=strengths,
            concerns=concerns,
            improvement_areas=improvement_areas
        )

    def _generate_churn_actions(self, risk_factors: List[str], risk_level: ChurnRiskLevel) -> List[str]:
        """Gera ações específicas baseadas nos fatores de risco"""
        actions = []
        
        for factor in risk_factors:
            if "login" in factor.lower():
                actions.append("Contato proativo para verificar necessidades")
                actions.append("Oferecer sessão de re-onboarding")
                
            if "suporte" in factor.lower():
                actions.append("Revisar tickets em aberto")
                actions.append("Escalação para Customer Success Manager")
                
            if "recursos" in factor.lower() or "uso" in factor.lower():
                actions.append("Agendar treinamento personalizado")
                actions.append("Demonstração de recursos subutilizados")
                
            if "pagamento" in factor.lower():
                actions.append("Negociar condições de pagamento")
                actions.append("Revisar plano e necessidades")
                
            if "nps" in factor.lower():
                actions.append("Pesquisa detalhada de satisfação")
                actions.append("Reunião com stakeholders")
                
        # Ações gerais por nível de risco
        if risk_level == ChurnRiskLevel.CRITICAL:
            actions.extend([
                "Intervenção imediata do CS Manager",
                "Oferecer desconto ou benefício especial",
                "Reunião de emergência com tomador de decisão"
            ])
        elif risk_level == ChurnRiskLevel.HIGH:
            actions.extend([
                "Contato dentro de 24h",
                "Análise de ROI do cliente",
                "Proposta de value-add"
            ])
            
        return list(set(actions))  # Remove duplicatas

    async def _recommend_strategies(self, churn_analysis: ChurnAnalysis, health_analysis: HealthAnalysis) -> List[Dict[str, Any]]:
        """Recomenda estratégias baseadas nas análises"""
        strategies = []
        
        # Estratégias baseadas em churn risk
        if churn_analysis.risk_level in [ChurnRiskLevel.HIGH, ChurnRiskLevel.CRITICAL]:
            strategies.append({
                "type": "retention_campaign",
                "priority": "high",
                "title": "Campanha de Retenção Urgente",
                "description": "Intervenção proativa com oferta personalizada",
                "timeline": "1-3 dias",
                "owner": "Customer Success Manager"
            })
            
        # Estratégias baseadas em health score
        if health_analysis.health_score == HealthScore.EXCELLENT:
            strategies.append({
                "type": "expansion",
                "priority": "medium",
                "title": "Oportunidade de Upsell",
                "description": "Cliente saudável - explorar expansão de conta",
                "timeline": "2-4 semanas",
                "owner": "Account Manager"
            })
        elif health_analysis.health_score in [HealthScore.POOR, HealthScore.CRITICAL]:
            strategies.append({
                "type": "health_recovery",
                "priority": "high",
                "title": "Plano de Recuperação de Saúde",
                "description": "Programa intensivo de melhoria da experiência",
                "timeline": "1-2 semanas",
                "owner": "Customer Success Team"
            })
            
        # Estratégias específicas por improvement areas
        for area in health_analysis.improvement_areas:
            if "treinamento" in area.lower():
                strategies.append({
                    "type": "education",
                    "priority": "medium",
                    "title": "Programa de Educação",
                    "description": f"Foco em: {area}",
                    "timeline": "1-2 semanas",
                    "owner": "Customer Education Team"
                })
                
        return strategies

    async def _batch_churn_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise de churn em lote para múltiplos clientes"""
        customers_data = data.get("customers", [])
        results = []
        
        for customer_data in customers_data:
            metrics = self._extract_metrics(customer_data)
            churn_analysis = await self._analyze_churn_risk(metrics)
            
            results.append({
                "customer_id": metrics.customer_id,
                "risk_level": churn_analysis.risk_level.value,
                "probability": churn_analysis.probability,
                "urgency_score": churn_analysis.urgency_score
            })
            
        # Agregar estatísticas
        risk_distribution = defaultdict(int)
        total_customers = len(results)
        
        for result in results:
            risk_distribution[result["risk_level"]] += 1
            
        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "total_customers_analyzed": total_customers,
            "risk_distribution": dict(risk_distribution),
            "high_risk_customers": [
                r["customer_id"] for r in results 
                if r["risk_level"] in ["high", "critical"]
            ],
            "detailed_results": results
        }

    async def _identify_proactive_outreach(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Identifica clientes que precisam de contato proativo"""
        customers_data = data.get("customers", [])
        outreach_candidates = []
        
        for customer_data in customers_data:
            metrics = self._extract_metrics(customer_data)
            churn_analysis = await self._analyze_churn_risk(metrics)
            health_analysis = await self._analyze_account_health(metrics)
            
            # Critérios para outreach proativo
            needs_outreach = (
                churn_analysis.risk_level in [ChurnRiskLevel.MEDIUM, ChurnRiskLevel.HIGH, ChurnRiskLevel.CRITICAL] or
                health_analysis.health_score in [HealthScore.POOR, HealthScore.CRITICAL] or
                metrics.last_login_days > 7 or
                (metrics.nps_score is not None and metrics.nps_score < 7)
            )
            
            if needs_outreach:
                outreach_candidates.append({
                    "customer_id": metrics.customer_id,
                    "priority": churn_analysis.urgency_score,
                    "reason": churn_analysis.key_factors[:2],  # Top 2 reasons
                    "suggested_approach": "phone_call" if churn_analysis.risk_level == ChurnRiskLevel.CRITICAL else "email",
                    "timeline": "24h" if churn_analysis.urgency_score > 7 else "72h"
                })
                
        # Ordenar por prioridade
        outreach_candidates.sort(key=lambda x: x["priority"], reverse=True)
        
        return {
            "outreach_timestamp": datetime.now().isoformat(),
            "total_candidates": len(outreach_candidates),
            "urgent_candidates": len([c for c in outreach_candidates if c["priority"] > 7]),
            "outreach_list": outreach_candidates
        }

    def _extract_metrics(self, customer_data: Dict[str, Any]) -> CustomerMetrics:
        """Extrai métricas do cliente dos dados fornecidos"""
        return CustomerMetrics(
            customer_id=customer_data.get("customer_id", "unknown"),
            last_login_days=customer_data.get("last_login_days", 0),
            support_tickets_30d=customer_data.get("support_tickets_30d", 0),
            feature_usage_score=customer_data.get("feature_usage_score", 0.5),
            payment_delays=customer_data.get("payment_delays", 0),
            contract_value=customer_data.get("contract_value", 0.0),
            tenure_months=customer_data.get("tenure_months", 0),
            nps_score=customer_data.get("nps_score"),
            engagement_score=customer_data.get("engagement_score", 0.5),
            support_satisfaction=customer_data.get("support_satisfaction")
        )

    async def _health_check(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Health check do próprio agente"""
        return {
            "agent_status": "healthy",
            "cache_size": len(self.analysis_cache),
            "last_analysis": datetime.now().isoformat(),
            "thresholds_configured": len(self.churn_thresholds),
            "health_weights_sum": sum(self.health_weights.values())
        }

    async def _generate_retention_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera estratégia de retenção personalizada"""
        customer_data = data.get("customer_data", {})
        metrics = self._extract_metrics(customer_data)
        
        churn_analysis = await self._analyze_churn_risk(metrics)
        health_analysis = await self._analyze_account_health(metrics)
        
        # Estratégia baseada no perfil do cliente
        strategy = {
            "customer_id": metrics.customer_id,
            "strategy_type": self._determine_strategy_type(metrics, churn_analysis),
            "immediate_actions": churn_analysis.recommended_actions,
            "long_term_plan": self._create_longterm_plan(health_analysis),
            "success_metrics": self._define_success_metrics(metrics),
            "review_schedule": self._create_review_schedule(churn_analysis.risk_level),
            "budget_recommendation": self._estimate_retention_budget(metrics.contract_value, churn_analysis.risk_level),
            "expected_outcomes": self._predict_outcomes(churn_analysis, health_analysis)
        }
        
        return strategy

    def _determine_strategy_type(self, metrics: CustomerMetrics, churn_analysis: ChurnAnalysis) -> str:
        """Determina o tipo de estratégia de retenção"""
        if churn_analysis.risk_level == ChurnRiskLevel.CRITICAL:
            return "emergency_intervention"
        elif churn_analysis.risk_level == ChurnRiskLevel.HIGH:
            return "intensive_care"
        elif metrics.feature_usage_score < 0.4:
            return "adoption_focused"
        elif metrics.contract_value > 10000:
            return "white_glove_service"
        else:
            return "standard_care"

    def _create_longterm_plan(self, health_analysis: HealthAnalysis) -> List[Dict[str, str]]:
        """Cria plano de longo prazo baseado na saúde da conta"""
        plan = []
        
        for area in health_analysis.improvement_areas:
            if "treinamento" in area.lower():
                plan.append({
                    "phase": "Education",
                    "duration": "4 weeks",
                    "objective": "Increase feature adoption",
                    "activities": ["Weekly training sessions", "Resource library access", "Certification program"]
                })
            elif "engajamento" in area.lower():
                plan.append({
                    "phase": "Engagement",
                    "duration": "6 weeks",
                    "objective": "Increase platform usage",
                    "activities": ["Gamification program", "Regular check-ins", "Success milestones"]
                })
                
        return plan

    def _define_success_metrics(self, metrics: CustomerMetrics) -> Dict[str, Any]:
        """Define métricas de sucesso para a estratégia"""
        return {
            "login_frequency_target": max(1, metrics.last_login_days - 3),
            "feature_usage_target": min(1.0, metrics.feature_usage_score + 0.2),
            "support_tickets_target": max(0, metrics.support_tickets_30d - 2),
            "nps_target": 8 if metrics.nps_score else 7,
            "timeline": "90 days"
        }

    def _create_review_schedule(self, risk_level: ChurnRiskLevel) -> List[str]:
        """Cria cronograma de revisões"""
        if risk_level == ChurnRiskLevel.CRITICAL:
            return ["3 days", "1 week", "2 weeks", "1 month"]
        elif risk_level == ChurnRiskLevel.HIGH:
            return ["1 week", "2 weeks", "1 month", "2 months"]
        else:
            return ["2 weeks", "1 month", "3 months"]

    def _estimate_retention_budget(self, contract_value: float, risk_level: ChurnRiskLevel) -> Dict[str, float]:
        """Estima orçamento recomendado para retenção"""
        base_percentage = {
            ChurnRiskLevel.CRITICAL: 0.15,  # 15% do valor do contrato
            ChurnRiskLevel.HIGH: 0.10,      # 10%
            ChurnRiskLevel.MEDIUM: 0.05,    # 5%
            ChurnRiskLevel.LOW: 0.02        # 2%
        }
        
        budget = contract_value * base_percentage.get(risk_level, 0.05)
        
        return {
            "recommended_budget": budget,
            "max_budget": budget * 1.5,
            "roi_breakeven": budget / (contract_value * 0.8),  # Assumindo 80% de margem
            "currency": "BRL"
        }

    def _predict_outcomes(self, churn_analysis: ChurnAnalysis, health_analysis: HealthAnalysis) -> Dict[str, Any]:
        """Prediz resultados esperados da estratégia"""
        base_success_rate = {
            ChurnRiskLevel.CRITICAL: 0.3,
            ChurnRiskLevel.HIGH: 0.6,
            ChurnRiskLevel.MEDIUM: 0.8,
            ChurnRiskLevel.LOW: 0.95
        }
        
        # Ajuste baseado na saúde da conta
        health_modifier = {
            HealthScore.EXCELLENT: 1.2,
            HealthScore.GOOD: 1.1,
            HealthScore.FAIR: 1.0,
            HealthScore.POOR: 0.9,
            HealthScore.CRITICAL: 0.7
        }
        
        success_probability = min(0.95, 
            base_success_rate[churn_analysis.risk_level] * 
            health_modifier[health_analysis.health_score]
        )
        
        return {
            "retention_probability": success_probability,
            "timeline_to_stability": f"{30 + (10 - success_probability * 10):.0f} days",
            "expected_health_improvement": min(20, (1 - success_probability) * 30),
            "confidence_level": "high" if success_probability > 0.7 else "medium"
        }

def create_agents() -> List[CustomerSuccessAgent]:
    """
    Função obrigatória para criação de agentes.
    Retorna lista de agentes Customer Success para o módulo Sales.
    """
    return [CustomerSuccessAgent()]

# Função de inicialização para compatibilidade
def initialize_customer_success_agent():
    """Inicializa o agente Customer Success"""
    return CustomerSuccessAgent()

# Ponto de entrada para testes
if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        agent = CustomerSuccessAgent()
        
        # Dados de teste
        test_data = {
            "action": "analyze_customer",
            "customer_data": {
                "customer_id": "CUST_001",
                "last_login_days": 12,
                "support_tickets_30d": 3,
                "feature_usage_score": 0.45,
                "payment_delays": 1,
                "contract_value": 15000.0,
                "tenure_months": 8,
                "nps_score": 6,
                "engagement_score": 0.6,
                "support_satisfaction": 75
            }
        }
        
        result = await agent.process(test_data)
        print("Teste Customer Success Agent:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    # Executar teste
    asyncio.run(test_agent())
