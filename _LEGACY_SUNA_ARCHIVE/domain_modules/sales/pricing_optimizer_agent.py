"""
ALSHAM QUANTUM - Pricing Optimizer Agent (Sales Module)
Versão Nativa - Sem dependências SUNA-ALSHAM
Corrigido em: 07/08/2025

Agente especializado em:
- Otimização dinâmica de preços
- Análise de elasticidade de demanda
- Precificação competitiva
- Estratégias de pricing psicológico
- Análise de margem e rentabilidade
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

class PricingStrategy(Enum):
    """Estratégias de precificação"""
    COST_PLUS = "cost_plus"
    VALUE_BASED = "value_based"
    COMPETITIVE = "competitive"
    PENETRATION = "penetration"
    SKIMMING = "skimming"
    DYNAMIC = "dynamic"
    PSYCHOLOGICAL = "psychological"
    BUNDLE = "bundle"

class MarketSegment(Enum):
    """Segmentos de mercado"""
    PREMIUM = "premium"
    MASS_MARKET = "mass_market"
    ECONOMY = "economy"
    LUXURY = "luxury"
    ENTERPRISE = "enterprise"
    SMB = "smb"

class PriceElasticity(Enum):
    """Elasticidade da demanda"""
    HIGHLY_ELASTIC = "highly_elastic"      # > 1.5
    ELASTIC = "elastic"                    # 1.0 - 1.5
    UNIT_ELASTIC = "unit_elastic"          # ~1.0
    INELASTIC = "inelastic"                # 0.5 - 1.0
    HIGHLY_INELASTIC = "highly_inelastic"  # < 0.5

@dataclass
class ProductData:
    """Dados do produto para análise de preço"""
    product_id: str
    name: str
    category: str
    cost_of_goods: Decimal
    current_price: Decimal
    target_margin: float
    features_score: float
    brand_strength: float
    market_position: str
    lifecycle_stage: str
    seasonality_factor: float = 1.0

@dataclass
class MarketData:
    """Dados de mercado para análise"""
    market_size: float
    growth_rate: float
    competitor_prices: List[Decimal]
    market_share: float
    price_sensitivity: float
    seasonal_trends: Dict[str, float]
    economic_indicators: Dict[str, float]

@dataclass
class CompetitorAnalysis:
    """Análise de concorrentes"""
    competitor_id: str
    price: Decimal
    market_share: float
    features_comparison: float  # 0-1 score vs our product
    brand_strength: float
    positioning: str

@dataclass
class PriceOptimization:
    """Resultado da otimização de preço"""
    product_id: str
    current_price: Decimal
    optimized_price: Decimal
    price_change_percent: float
    expected_demand_change: float
    expected_revenue_change: float
    expected_profit_change: float
    strategy_used: PricingStrategy
    confidence_score: float
    rationale: List[str]
    risk_factors: List[str]

@dataclass
class ElasticityAnalysis:
    """Análise de elasticidade de preço"""
    product_id: str
    elasticity_coefficient: float
    elasticity_category: PriceElasticity
    price_sensitivity_score: float
    demand_forecast: Dict[str, float]  # price -> demand
    optimal_price_point: Decimal

class PricingOptimizerAgent(BaseNetworkAgent):
    """Agente Otimizador de Preços nativo do ALSHAM QUANTUM"""
    
    def __init__(self):
        super().__init__("pricing_optimizer_agent", "Pricing Optimizer Agent")
        
        # Configurações de otimização
        self.optimization_params = {
            "max_price_increase": 0.20,  # 20% máximo de aumento
            "max_price_decrease": 0.15,  # 15% máximo de redução
            "target_profit_margin": 0.30,  # 30% margem alvo
            "confidence_threshold": 0.7,  # 70% confiança mínima
            "market_response_sensitivity": 0.8
        }
        
        # Fatores de ajuste por categoria
        self.category_factors = {
            "software": {"elasticity": -1.2, "innovation_premium": 0.15},
            "hardware": {"elasticity": -0.8, "innovation_premium": 0.10},
            "services": {"elasticity": -1.5, "innovation_premium": 0.20},
            "subscription": {"elasticity": -1.8, "innovation_premium": 0.25},
            "default": {"elasticity": -1.0, "innovation_premium": 0.12}
        }
        
        # Cache de otimizações
        self.optimization_cache = {}
        
        # Histórico de preços
        self.price_history = defaultdict(list)
        
        self.logger.info("Pricing Optimizer Agent inicializado com engine nativo")

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisições de otimização de preços"""
        try:
            action = data.get("action", "optimize_price")
            
            if action == "optimize_price":
                return await self._optimize_price(data)
            elif action == "analyze_elasticity":
                return await self._analyze_price_elasticity(data)
            elif action == "competitor_analysis":
                return await self._analyze_competitors(data)
            elif action == "market_positioning":
                return await self._analyze_market_positioning(data)
            elif action == "dynamic_pricing":
                return await self._dynamic_pricing_strategy(data)
            elif action == "bundle_optimization":
                return await self._optimize_bundle_pricing(data)
            elif action == "psychological_pricing":
                return await self._apply_psychological_pricing(data)
            elif action == "scenario_analysis":
                return await self._price_scenario_analysis(data)
            else:
                return {"error": f"Ação não reconhecida: {action}"}
                
        except Exception as e:
            self.logger.error(f"Erro na otimização de preços: {str(e)}")
            return {"error": str(e)}

    async def _optimize_price(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Otimização principal de preço"""
        
        # Extrair dados
        product_data = self._extract_product_data(data)
        market_data = self._extract_market_data(data)
        
        # Análises preliminares
        competitor_analysis = await self._perform_competitor_analysis(market_data)
        elasticity_analysis = await self._calculate_elasticity(product_data, market_data)
        
        # Aplicar estratégias de precificação
        strategies_results = await self._evaluate_pricing_strategies(
            product_data, market_data, competitor_analysis, elasticity_analysis
        )
        
        # Selecionar melhor estratégia
        best_strategy = self._select_best_strategy(strategies_results)
        
        # Aplicar ajustes finais
        final_optimization = await self._apply_final_adjustments(
            best_strategy, product_data, market_data
        )
        
        # Salvar no cache
        optimization_id = str(uuid.uuid4())
        self.optimization_cache[optimization_id] = {
            "product_data": asdict(product_data),
            "optimization": asdict(final_optimization),
            "timestamp": datetime.now().isoformat()
        }
        
        # Atualizar histórico
        self._update_price_history(product_data.product_id, final_optimization.optimized_price)
        
        return {
            "optimization_id": optimization_id,
            "product_id": product_data.product_id,
            "product_name": product_data.name,
            "current_price": float(final_optimization.current_price),
            "optimized_price": float(final_optimization.optimized_price),
            "price_change": {
                "absolute": float(final_optimization.optimized_price - final_optimization.current_price),
                "percentage": final_optimization.price_change_percent
            },
            "expected_impact": {
                "demand_change": final_optimization.expected_demand_change,
                "revenue_change": final_optimization.expected_revenue_change,
                "profit_change": final_optimization.expected_profit_change
            },
            "strategy": {
                "name": final_optimization.strategy_used.value,
                "confidence": final_optimization.confidence_score,
                "rationale": final_optimization.rationale
            },
            "risk_assessment": {
                "risk_factors": final_optimization.risk_factors,
                "recommendation": self._generate_implementation_plan(final_optimization)
            },
            "competitor_analysis": competitor_analysis,
            "elasticity_analysis": asdict(elasticity_analysis),
            "timestamp": datetime.now().isoformat()
        }

    async def _evaluate_pricing_strategies(self, product_data: ProductData, market_data: MarketData, 
                                         competitor_analysis: List[CompetitorAnalysis],
                                         elasticity_analysis: ElasticityAnalysis) -> Dict[str, PriceOptimization]:
        """Avalia diferentes estratégias de precificação"""
        
        strategies = {}
        
        # 1. Cost-Plus Pricing
        strategies["cost_plus"] = self._cost_plus_strategy(product_data)
        
        # 2. Value-Based Pricing  
        strategies["value_based"] = self._value_based_strategy(product_data, market_data)
        
        # 3. Competitive Pricing
        strategies["competitive"] = self._competitive_strategy(product_data, competitor_analysis)
        
        # 4. Dynamic Pricing
        strategies["dynamic"] = self._dynamic_strategy(product_data, market_data, elasticity_analysis)
        
        # 5. Psychological Pricing
        strategies["psychological"] = self._psychological_strategy(product_data)
        
        return strategies

    def _cost_plus_strategy(self, product_data: ProductData) -> PriceOptimization:
        """Estratégia Cost-Plus"""
        markup = 1 + product_data.target_margin
        optimized_price = product_data.cost_of_goods * Decimal(str(markup))
        
        price_change = float((optimized_price - product_data.current_price) / product_data.current_price * 100)
        
        return PriceOptimization(
            product_id=product_data.product_id,
            current_price=product_data.current_price,
            optimized_price=optimized_price,
            price_change_percent=price_change,
            expected_demand_change=-abs(price_change) * 0.5,  # Estimativa simples
            expected_revenue_change=price_change * 0.8,
            expected_profit_change=price_change * 1.2,
            strategy_used=PricingStrategy.COST_PLUS,
            confidence_score=0.8,
            rationale=[
                f"Baseado em custo de R$ {product_data.cost_of_goods} + margem de {product_data.target_margin*100}%",
                "Estratégia conservadora garantindo margem mínima"
            ],
            risk_factors=["Não considera valor percebido pelo cliente", "Ignora preços competitivos"]
        )

    def _value_based_strategy(self, product_data: ProductData, market_data: MarketData) -> PriceOptimization:
        """Estratégia Value-Based"""
        
        # Calcular value score baseado em features e posicionamento
        value_multiplier = (
            product_data.features_score * 0.4 +
            product_data.brand_strength * 0.3 +
            (1.0 if product_data.market_position == "leader" else 0.5) * 0.3
        )
        
        # Preço base da categoria + premium por valor
        category_avg = statistics.mean(market_data.competitor_prices) if market_data.competitor_prices else product_data.current_price
        optimized_price = category_avg * Decimal(str(1 + value_multiplier * 0.2))
        
        price_change = float((optimized_price - product_data.current_price) / product_data.current_price * 100)
        
        return PriceOptimization(
            product_id=product_data.product_id,
            current_price=product_data.current_price,
            optimized_price=optimized_price,
            price_change_percent=price_change,
            expected_demand_change=-abs(price_change) * 0.7,
            expected_revenue_change=price_change * 0.9,
            expected_profit_change=price_change * 1.3,
            strategy_used=PricingStrategy.VALUE_BASED,
            confidence_score=0.85,
            rationale=[
                f"Value score calculado: {value_multiplier:.2f}",
                f"Premium justificado pelas features superiores",
                f"Posicionamento de mercado: {product_data.market_position}"
            ],
            risk_factors=["Clientes podem não perceber o valor adicional", "Risco de perda de market share"]
        )

    def _competitive_strategy(self, product_data: ProductData, 
                            competitor_analysis: List[CompetitorAnalysis]) -> PriceOptimization:
        """Estratégia Competitive"""
        
        if not competitor_analysis:
            # Fallback para preço atual se não há dados competitivos
            return self._cost_plus_strategy(product_data)
            
        # Calcular posicionamento competitivo
        weighted_competitor_price = Decimal("0")
        total_weight = 0
        
        for comp in competitor_analysis:
            weight = comp.market_share * comp.features_comparison
            weighted_competitor_price += comp.price * Decimal(str(weight))
            total_weight += weight
            
        if total_weight > 0:
            avg_competitive_price = weighted_competitor_price / Decimal(str(total_weight))
        else:
            avg_competitive_price = statistics.mean(comp.price for comp in competitor_analysis)
            
        # Ajustar baseado em nossa posição
        if product_data.brand_strength > 0.8:
            optimized_price = avg_competitive_price * Decimal("1.05")  # 5% premium
        elif product_data.features_score > 0.8:
            optimized_price = avg_competitive_price * Decimal("1.03")  # 3% premium
        else:
            optimized_price = avg_competitive_price * Decimal("0.98")  # 2% desconto
            
        price_change = float((optimized_price - product_data.current_price) / product_data.current_price * 100)
        
        return PriceOptimization(
            product_id=product_data.product_id,
            current_price=product_data.current_price,
            optimized_price=optimized_price,
            price_change_percent=price_change,
            expected_demand_change=-abs(price_change) * 0.9,
            expected_revenue_change=price_change * 0.95,
            expected_profit_change=price_change * 1.1,
            strategy_used=PricingStrategy.COMPETITIVE,
            confidence_score=0.9,
            rationale=[
                f"Preço médio ponderado dos concorrentes: R$ {avg_competitive_price}",
                f"Ajuste baseado em brand strength ({product_data.brand_strength}) e features ({product_data.features_score})",
                "Estratégia para manter competitividade"
            ],
            risk_factors=["Guerra de preços com concorrentes", "Redução de margens"]
        )

    def _dynamic_strategy(self, product_data: ProductData, market_data: MarketData,
                         elasticity_analysis: ElasticityAnalysis) -> PriceOptimization:
        """Estratégia Dynamic baseada em elasticidade"""
        
        # Usar ponto ótimo da análise de elasticidade
        optimized_price = elasticity_analysis.optimal_price_point
        
        # Aplicar fatores sazonais e de mercado
        seasonal_factor = product_data.seasonality_factor
        market_factor = 1 + (market_data.growth_rate / 100) * 0.1
        
        optimized_price *= Decimal(str(seasonal_factor * market_factor))
        
        # Limitar mudanças drásticas
        max_increase = product_data.current_price * Decimal(str(1 + self.optimization_params["max_price_increase"]))
        max_decrease = product_data.current_price * Decimal(str(1 - self.optimization_params["max_price_decrease"]))
        
        optimized_price = max(min(optimized_price, max_increase), max_decrease)
        
        price_change = float((optimized_price - product_data.current_price) / product_data.current_price * 100)
        
        # Calcular impacto baseado em elasticidade
        demand_change = elasticity_analysis.elasticity_coefficient * price_change
        revenue_change = price_change + demand_change
        
        return PriceOptimization(
            product_id=product_data.product_id,
            current_price=product_data.current_price,
            optimized_price=optimized_price,
            price_change_percent=price_change,
            expected_demand_change=demand_change,
            expected_revenue_change=revenue_change,
            expected_profit_change=revenue_change * 1.2,  # Assumindo margem
            strategy_used=PricingStrategy.DYNAMIC,
            confidence_score=0.88,
            rationale=[
                f"Baseado em elasticidade de {elasticity_analysis.elasticity_coefficient:.2f}",
                f"Ajuste sazonal: {seasonal_factor:.2f}",
                f"Fator de crescimento de mercado: {market_factor:.2f}",
                "Otimização matemática para máximo revenue"
            ],
            risk_factors=["Sensibilidade a mudanças de mercado", "Requer monitoramento constante"]
        )

    def _psychological_strategy(self, product_data: ProductData) -> PriceOptimization:
        """Estratégia Psychological Pricing"""
        
        current_price = product_data.current_price
        
        # Aplicar preços psicológicos (.99, .95, etc.)
        if current_price >= Decimal("100"):
            # Para preços altos, usar terminação .99
            optimized_price = Decimal(str(int(current_price))) - Decimal("0.01")
        elif current_price >= Decimal("10"):
            # Para preços médios, usar terminação .95
            optimized_price = Decimal(str(int(current_price))) - Decimal("0.05")
        else:
            # Para preços baixos, arredondar para .99
            optimized_price = Decimal(f"{int(current_price)}.99")
            
        # Se a diferença for muito pequena, aplicar desconto de 5%
        if abs(optimized_price - current_price) < Decimal("0.10"):
            optimized_price = current_price * Decimal("0.95")
            optimized_price = self._apply_psychological_ending(optimized_price)
            
        price_change = float((optimized_price - product_data.current_price) / product_data.current_price * 100)
        
        return PriceOptimization(
            product_id=product_data.product_id,
            current_price=product_data.current_price,
            optimized_price=optimized_price,
            price_change_percent=price_change,
            expected_demand_change=-price_change * 0.3,  # Menor impacto devido a psychological pricing
            expected_revenue_change=price_change * 1.1,   # Melhor percepção de valor
            expected_profit_change=price_change * 1.15,
            strategy_used=PricingStrategy.PSYCHOLOGICAL,
            confidence_score=0.75,
            rationale=[
                f"Aplicação de terminação psicológica ao preço",
                "Melhora percepção de valor pelo consumidor",
                "Baseado em princípios de psicologia comportamental"
            ],
            risk_factors=["Pode parecer manipulativo para alguns segmentos", "Efetividade varia por mercado"]
        )

    def _apply_psychological_ending(self, price: Decimal) -> Decimal:
        """Aplica terminações psicológicas ao preço"""
        if price >= Decimal("100"):
            return Decimal(str(int(price))) - Decimal("0.01")
        elif price >= Decimal("10"):
            return Decimal(str(int(price))) - Decimal("0.05")
        else:
            return Decimal(f"{int(price)}.99")

    async def _calculate_elasticity(self, product_data: ProductData, market_data: MarketData) -> ElasticityAnalysis:
        """Calcula elasticidade de preço da demanda"""
        
        # Obter elasticidade base da categoria
        category_factor = self.category_factors.get(
            product_data.category.lower(), 
            self.category_factors["default"]
        )
        
        base_elasticity = category_factor["elasticity"]
        
        # Ajustar baseado em fatores do produto
        elasticity_adjustments = 0
        
        # Produtos com features únicas são menos elásticos
        if product_data.features_score > 0.8:
            elasticity_adjustments += 0.2
            
        # Marcas fortes são menos elásticas
        if product_data.brand_strength > 0.7:
            elasticity_adjustments += 0.3
            
        # Market leaders são menos elásticos
        if product_data.market_position == "leader":
            elasticity_adjustments += 0.25
            
        # Ajustar pela sensibilidade do mercado
        market_adjustment = market_data.price_sensitivity * 0.5
        
        final_elasticity = base_elasticity + elasticity_adjustments - market_adjustment
        
        # Classificar elasticidade
        if abs(final_elasticity) > 1.5:
            elasticity_category = PriceElasticity.HIGHLY_ELASTIC
        elif abs(final_elasticity) > 1.0:
            elasticity_category = PriceElasticity.ELASTIC
        elif abs(final_elasticity) > 0.9:
            elasticity_category = PriceElasticity.UNIT_ELASTIC
        elif abs(final_elasticity) > 0.5:
            elasticity_category = PriceElasticity.INELASTIC
        else:
            elasticity_category = PriceElasticity.HIGHLY_INELASTIC
            
        # Calcular ponto ótimo de preço (maximização de receita)
        current_price = product_data.current_price
        
        # Para maximizar receita: elasticidade = -1
        # Preço ótimo = preço atual * (elasticidade / (elasticidade + 1))
        if final_elasticity != -1:
            price_multiplier = final_elasticity / (final_elasticity + 1)
            optimal_price = current_price * Decimal(str(abs(price_multiplier)))
        else:
            optimal_price = current_price  # Já no ponto ótimo
            
        # Gerar forecast de demanda para diferentes preços
        demand_forecast = self._generate_demand_forecast(current_price, final_elasticity)
        
        return ElasticityAnalysis(
            product_id=product_data.product_id,
            elasticity_coefficient=final_elasticity,
            elasticity_category=elasticity_category,
            price_sensitivity_score=market_data.price_sensitivity,
            demand_forecast=demand_forecast,
            optimal_price_point=optimal_price
        )

    def _generate_demand_forecast(self, current_price: Decimal, elasticity: float) -> Dict[str, float]:
        """Gera forecast de demanda para diferentes níveis de preço"""
        forecast = {}
        base_demand = 100.0  # Demanda base normalizada
        
        # Testar diferentes variações de preço
        price_variations = [-0.20, -0.15, -0.10, -0.05, 0.0, 0.05, 0.10, 0.15, 0.20]
        
        for variation in price_variations:
            new_price = current_price * Decimal(str(1 + variation))
            # Demand_change = elasticity * price_change
            demand_change = elasticity * (variation * 100)
            new_demand = base_demand * (1 + demand_change / 100)
            
            forecast[str(new_price)] = max(0, new_demand)  # Demanda não pode ser negativa
            
        return forecast

    async def _perform_competitor_analysis(self, market_data: MarketData) -> List[CompetitorAnalysis]:
        """Realiza análise competitiva (simulada)"""
        competitors = []
        
        if not market_data.competitor_prices:
            return competitors
            
        # Simular dados de concorrentes baseado nos preços
        for i, price in enumerate(market_data.competitor_prices):
            competitor = CompetitorAnalysis(
                competitor_id=f"COMP_{i+1:03d}",
                price=price,
                market_share=max(0.05, (len(market_data.competitor_prices) - i) / len(market_data.competitor_prices) * 0.3),
                features_comparison=0.7 + (i * 0.1) % 0.3,  # Variação simulada
                brand_strength=0.5 + (i * 0.15) % 0.4,
                positioning="competitor"
            )
            competitors.append(competitor)
            
        return competitors

    def _select_best_strategy(self, strategies: Dict[str, PriceOptimization]) -> PriceOptimization:
        """Seleciona a melhor estratégia baseada em critérios múltiplos"""
        
        scored_strategies = []
        
        for name, strategy in strategies.items():
            # Calcular score baseado em múltiplos fatores
            score = 0
            
            # Confiança (peso 30%)
            score += strategy.confidence_score * 0.30
            
            # Impacto na receita (peso 25%)
            revenue_score = min(1.0, max(0.0, (strategy.expected_revenue_change + 20) / 40))
            score += revenue_score * 0.25
            
            # Impacto no lucro (peso 25%)
            profit_score = min(1.0, max(0.0, (strategy.expected_profit_change + 20) / 40))
            score += profit_score * 0.25
            
            # Menor risco (peso 20%)
            risk_score = max(0.0, 1.0 - len(strategy.risk_factors) * 0.2)
            score += risk_score * 0.20
            
            scored_strategies.append((score, strategy))
            
        # Retornar estratégia com maior score
        scored_strategies.sort(key=lambda x: x[0], reverse=True)
        return scored_strategies[0][1]

    async def _apply_final_adjustments(self, optimization: PriceOptimization, 
                                     product_data: ProductData, market_data: MarketData) -> PriceOptimization:
        """Aplica ajustes finais à otimização"""
        
        # Verificar limites de mudança de preço
        max_increase = product_data.current_price * Decimal(str(1 + self.optimization_params["max_price_increase"]))
        max_decrease = product_data.current_price * Decimal(str(1 - self.optimization_params["max_price_decrease"]))
        
        if optimization.optimized_price > max_increase:
            optimization.optimized_price = max_increase
            optimization.risk_factors.append(f"Preço limitado a {self.optimization_params['max_price_increase']*100}% de aumento")
            
        if optimization.optimized_price < max_decrease:
            optimization.optimized_price = max_decrease
            optimization.risk_factors.append(f"Preço limitado a {self.optimization_params['max_price_decrease']*100}% de redução")
            
        # Recalcular métricas após ajustes
        price_change = float((optimization.optimized_price - optimization.current_price) / optimization.current_price * 100)
        optimization.price_change_percent = price_change
        
        # Adicionar fatores sazonais
        if product_data.seasonality_factor != 1.0:
            seasonal_adjustment = (product_data.seasonality_factor - 1.0) * 0.1
            optimization.optimized_price *= Decimal(str(1 + seasonal_adjustment))
            optimization.rationale.append(f"Ajuste sazonal aplicado: {seasonal_adjustment*100:.1f}%")
            
        return optimization

    def _generate_implementation_plan(self, optimization: PriceOptimization) -> Dict[str, Any]:
        """Gera plano de implementação da nova precificação"""
        
        implementation_speed = "gradual"
        if abs(optimization.price_change_percent) > 15:
            implementation_speed = "phased"
        elif abs(optimization.price_change_percent) < 5:
            implementation_speed = "immediate"
            
        monitoring_frequency = "weekly"
        if optimization.strategy_used == PricingStrategy.DYNAMIC:
            monitoring_frequency = "daily"
        elif optimization.confidence_score < 0.7:
            monitoring_frequency = "daily"
            
        return {
            "implementation_speed": implementation_speed,
            "monitoring_frequency": monitoring_frequency,
            "rollback_threshold": abs(optimization.expected_demand_change) * 1.5,
            "success_metrics": [
                "Revenue growth",
                "Market share stability",
                "Customer satisfaction",
                "Competitor response"
            ],
            "timeline": f"{7 if implementation_speed == 'immediate' else 30} days"
        }

    def _extract_product_data(self, data: Dict[str, Any]) -> ProductData:
        """Extrai dados do produto da requisição"""
        product_info = data.get("product_data", {})
        
        return ProductData(
            product_id=product_info.get("product_id", str(uuid.uuid4())),
            name=product_info.get("name", "Unknown Product"),
            category=product_info.get("category", "default"),
            cost_of_goods=Decimal(str(product_info.get("cost_of_goods", "0.00"))),
            current_price=Decimal(str(product_info.get("current_price", "0.00"))),
            target_margin=float(product_info.get("target_margin", 0.30)),
            features_score=float(product_info.get("features_score", 0.5)),
            brand_strength=float(product_info.get("brand_strength", 0.5)),
            market_position=product_info.get("market_position", "follower"),
            lifecycle_stage=product_info.get("lifecycle_stage", "growth"),
            seasonality_factor=float(product_info.get("seasonality_factor", 1.0))
        )

    def _extract_market_data(self, data: Dict[str, Any]) -> MarketData:
        """Extrai dados de mercado da requisição"""
        market_info = data.get("market_data", {})
        
        competitor_prices = []
        if "competitor_prices" in market_info:
            competitor_prices = [Decimal(str(p)) for p in market_info["competitor_prices"]]
            
        return MarketData(
            market_size=float(market_info.get("market_size", 1000000)),
            growth_rate=float(market_info.get("growth_rate", 5.0)),
            competitor_prices=competitor_prices,
            market_share=float(market_info.get("market_share", 0.1)),
            price_sensitivity=float(market_info.get("price_sensitivity", 0.5)),
            seasonal_trends=market_info.get("seasonal_trends", {}),
            economic_indicators=market_info.get("economic_indicators", {})
        )

    def _update_price_history(self, product_id: str, new_price: Decimal):
        """Atualiza histórico de preços"""
        self.price_history[product_id].append({
            "price": float(new_price),
            "timestamp": datetime.now().isoformat()
        })
        
        # Manter apenas últimos 100 registros
        if len(self.price_history[product_id]) > 100:
            self.price_history[product_id] = self.price_history[product_id][-100:]

    async def _analyze_price_elasticity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise standalone de elasticidade de preço"""
        product_data = self._extract_product_data(data)
        market_data = self._extract_market_data(data)
        
        elasticity_analysis = await self._calculate_elasticity(product_data, market_data)
        
        return {
            "analysis_id": str(uuid.uuid4()),
            "product_id": product_data.product_id,
            "elasticity_analysis": asdict(elasticity_analysis),
            "insights": {
                "price_sensitivity": "high" if abs(elasticity_analysis.elasticity_coefficient) > 1.0 else "low",
                "optimal_strategy": "focus_on_volume" if abs(elasticity_analysis.elasticity_coefficient) > 1.0 else "focus_on_margin",
                "market_response": "sensitive" if elasticity_analysis.price_sensitivity_score > 0.7 else "stable"
            },
            "timestamp": datetime.now().isoformat()
        }

    async def _analyze_competitors(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise standalone de concorrentes"""
        market_data = self._extract_market_data(data)
        competitor_analysis = await self._perform_competitor_analysis(market_data)
        
        # Estatísticas competitivas
        if competitor_analysis:
            avg_price = statistics.mean(comp.price for comp in competitor_analysis)
            min_price = min(comp.price for comp in competitor_analysis)
            max_price = max(comp.price for comp in competitor_analysis)
            
            price_spread = float(max_price - min_price)
            market_concentration = sum(comp.market_share for comp in competitor_analysis[:3])  # Top 3
        else:
            avg_price = min_price = max_price = Decimal("0")
            price_spread = 0.0
            market_concentration = 0.0
        
        return {
            "analysis_id": str(uuid.uuid4()),
            "competitors": [asdict(comp) for comp in competitor_analysis],
            "market_statistics": {
                "average_price": float(avg_price),
                "min_price": float(min_price),
                "max_price": float(max_price),
                "price_spread": price_spread,
                "market_concentration": market_concentration
            },
            "competitive_insights": {
                "price_positioning": "premium" if len(market_data.competitor_prices) > 0 and avg_price > statistics.mean(market_data.competitor_prices) else "competitive",
                "market_structure": "concentrated" if market_concentration > 0.6 else "fragmented",
                "pricing_opportunity": "premium_positioning" if price_spread > float(avg_price) * 0.3 else "competitive_pricing"
            },
            "timestamp": datetime.now().isoformat()
        }

    async def _analyze_market_positioning(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise de posicionamento de mercado"""
        product_data = self._extract_product_data(data)
        market_data = self._extract_market_data(data)
        
        # Calcular posição no mercado
        if market_data.competitor_prices:
            avg_market_price = statistics.mean(market_data.competitor_prices)
            price_index = float(product_data.current_price / avg_market_price)
        else:
            price_index = 1.0
            avg_market_price = product_data.current_price
            
        # Determinar segmento
        if price_index > 1.3:
            market_segment = MarketSegment.PREMIUM
        elif price_index > 1.1:
            market_segment = MarketSegment.MASS_MARKET
        elif price_index > 0.9:
            market_segment = MarketSegment.MASS_MARKET
        else:
            market_segment = MarketSegment.ECONOMY
            
        return {
            "analysis_id": str(uuid.uuid4()),
            "product_id": product_data.product_id,
            "current_positioning": {
                "market_segment": market_segment.value,
                "price_index": price_index,
                "relative_position": "above_market" if price_index > 1.1 else "at_market" if price_index > 0.9 else "below_market"
            },
            "positioning_metrics": {
                "brand_strength": product_data.brand_strength,
                "features_score": product_data.features_score,
                "market_share": market_data.market_share,
                "value_perception": (product_data.features_score + product_data.brand_strength) / 2
            },
            "repositioning_opportunities": [
                "Move to premium segment" if price_index < 1.2 and product_data.features_score > 0.8 else None,
                "Value positioning" if product_data.features_score > 0.7 and price_index < 1.0 else None,
                "Cost leadership" if product_data.cost_of_goods < avg_market_price * Decimal("0.6") else None
            ],
            "timestamp": datetime.now().isoformat()
        }

    async def _dynamic_pricing_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Estratégia de pricing dinâmico em tempo real"""
        product_data = self._extract_product_data(data)
        market_data = self._extract_market_data(data)
        
        # Fatores dinâmicos
        time_factors = {
            "hour_of_day": datetime.now().hour,
            "day_of_week": datetime.now().weekday(),
            "day_of_month": datetime.now().day,
            "season": self._get_season()
        }
        
        # Calcular multiplicadores dinâmicos
        dynamic_multiplier = 1.0
        
        # Ajuste por hora (para produtos digitais)
        if product_data.category in ["software", "subscription"]:
            if 9 <= time_factors["hour_of_day"] <= 17:  # Horário comercial
                dynamic_multiplier *= 1.02
            elif 20 <= time_factors["hour_of_day"] <= 23:  # Noite
                dynamic_multiplier *= 0.98
                
        # Ajuste sazonal
        dynamic_multiplier *= product_data.seasonality_factor
        
        # Calcular preço dinâmico
        dynamic_price = product_data.current_price * Decimal(str(dynamic_multiplier))
        
        return {
            "strategy_id": str(uuid.uuid4()),
            "product_id": product_data.product_id,
            "dynamic_pricing": {
                "base_price": float(product_data.current_price),
                "dynamic_price": float(dynamic_price),
                "multiplier": dynamic_multiplier,
                "factors": time_factors
            },
            "validity_period": "1 hour",  # Preços dinâmicos têm validade curta
            "next_update": (datetime.now() + timedelta(hours=1)).isoformat(),
            "pricing_rules": {
                "min_price": float(product_data.current_price * Decimal("0.85")),
                "max_price": float(product_data.current_price * Decimal("1.15")),
                "update_frequency": "hourly"
            },
            "timestamp": datetime.now().isoformat()
        }

    def _get_season(self) -> str:
        """Determina a estação atual"""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return "summer"  # Verão no Brasil
        elif month in [3, 4, 5]:
            return "autumn"
        elif month in [6, 7, 8]:
            return "winter"
        else:
            return "spring"

    async def _optimize_bundle_pricing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Otimização de preços de bundle"""
        bundle_products = data.get("bundle_products", [])
        
        if len(bundle_products) < 2:
            return {"error": "Bundle deve conter pelo menos 2 produtos"}
            
        # Calcular preços individuais
        individual_total = Decimal("0")
        products_data = []
        
        for product_info in bundle_products:
            product_data = ProductData(
                product_id=product_info.get("product_id", str(uuid.uuid4())),
                name=product_info.get("name", "Unknown"),
                category=product_info.get("category", "default"),
                cost_of_goods=Decimal(str(product_info.get("cost_of_goods", "0"))),
                current_price=Decimal(str(product_info.get("current_price", "0"))),
                target_margin=float(product_info.get("target_margin", 0.30)),
                features_score=float(product_info.get("features_score", 0.5)),
                brand_strength=float(product_info.get("brand_strength", 0.5)),
                market_position=product_info.get("market_position", "follower"),
                lifecycle_stage=product_info.get("lifecycle_stage", "growth")
            )
            products_data.append(product_data)
            individual_total += product_data.current_price
            
        # Calcular desconto de bundle (tipicamente 10-20%)
        bundle_discount = 0.15  # 15% desconto padrão
        
        # Ajustar desconto baseado na complementaridade dos produtos
        category_diversity = len(set(p.category for p in products_data)) / len(products_data)
        if category_diversity > 0.5:  # Produtos de categorias diferentes
            bundle_discount += 0.05  # Desconto adicional de 5%
            
        bundle_price = individual_total * Decimal(str(1 - bundle_discount))
        
        # Calcular métricas
        savings = individual_total - bundle_price
        savings_percent = float(savings / individual_total * 100)
        
        return {
            "bundle_id": str(uuid.uuid4()),
            "products": [{"id": p.product_id, "name": p.name, "price": float(p.current_price)} for p in products_data],
            "pricing": {
                "individual_total": float(individual_total),
                "bundle_price": float(bundle_price),
                "savings": float(savings),
                "savings_percent": savings_percent,
                "discount_applied": bundle_discount * 100
            },
            "bundle_strategy": {
                "type": "complementary_discount",
                "rationale": f"Produtos complementares com {savings_percent:.1f}% de desconto",
                "expected_uptake": "25-35%" if savings_percent > 10 else "15-25%"
            },
            "timestamp": datetime.now().isoformat()
        }

    async def _apply_psychological_pricing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Aplicação de técnicas de pricing psicológico"""
        product_data = self._extract_product_data(data)
        
        original_price = product_data.current_price
        psychological_variations = {}
        
        # 1. Charm Pricing (.99, .95)
        charm_price = self._apply_psychological_ending(original_price)
        psychological_variations["charm_pricing"] = {
            "price": float(charm_price),
            "technique": "Charm pricing (.99/.95 ending)",
            "expected_impact": "5-8% increase in sales"
        }
        
        # 2. Prestige Pricing (arredondamento para cima)
        if original_price >= Decimal("100"):
            prestige_price = Decimal(str(int(original_price) + 1))
            psychological_variations["prestige_pricing"] = {
                "price": float(prestige_price),
                "technique": "Prestige pricing (round numbers)",
                "expected_impact": "Premium perception, 10-15% margin increase"
            }
            
        # 3. Anchoring (preço alto como referência)
        anchor_price = original_price * Decimal("1.25")
        psychological_variations["anchoring"] = {
            "price": float(anchor_price),
            "technique": "High anchor price",
            "expected_impact": "Makes original price seem reasonable"
        }
        
        # 4. Bundle Anchor (preço individual vs bundle)
        if data.get("has_bundle_option"):
            bundle_anchor = original_price * Decimal("1.4")
            psychological_variations["bundle_anchor"] = {
                "price": float(bundle_anchor),
                "technique": "Individual price to promote bundle",
                "expected_impact": "Increases bundle adoption by 20-30%"
            }
            
        # Recomendar melhor opção
        if product_data.market_position == "premium":
            recommended = "prestige_pricing"
        elif product_data.category in ["software", "subscription"]:
            recommended = "charm_pricing"
        else:
            recommended = "charm_pricing"
            
        return {
            "analysis_id": str(uuid.uuid4()),
            "product_id": product_data.product_id,
            "original_price": float(original_price),
            "psychological_variations": psychological_variations,
            "recommended_technique": recommended,
            "implementation_tips": [
                "Test different variations with A/B testing",
                "Monitor customer perception and satisfaction",
                "Consider cultural factors in pricing psychology",
                "Ensure pricing aligns with brand positioning"
            ],
            "timestamp": datetime.now().isoformat()
        }

    async def _price_scenario_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise de cenários de preço"""
        product_data = self._extract_product_data(data)
        market_data = self._extract_market_data(data)
        
        base_price = product_data.current_price
        scenarios = {}
        
        # Cenários de teste
        price_changes = [-0.20, -0.10, -0.05, 0.05, 0.10, 0.20]  # -20% a +20%
        
        for change in price_changes:
            scenario_price = base_price * Decimal(str(1 + change))
            
            # Estimar impactos (usando elasticidade simulada)
            elasticity_analysis = await self._calculate_elasticity(product_data, market_data)
            demand_change = elasticity_analysis.elasticity_coefficient * (change * 100)
            revenue_change = (change * 100) + demand_change
            
            # Calcular métricas do cenário
            scenario_revenue = float(scenario_price) * (100 + demand_change)
            current_revenue = float(base_price) * 100
            
            scenarios[f"{change*100:+.0f}%"] = {
                "price": float(scenario_price),
                "price_change_percent": change * 100,
                "expected_demand_change": demand_change,
                "expected_revenue_change": revenue_change,
                "absolute_revenue": scenario_revenue,
                "risk_level": "high" if abs(change) > 0.15 else "medium" if abs(change) > 0.10 else "low",
                "recommendation": self._get_scenario_recommendation(change, demand_change, revenue_change)
            }
            
        # Identificar melhor cenário
        best_scenario = max(scenarios.items(), 
                          key=lambda x: x[1]["absolute_revenue"])
        
        return {
            "analysis_id": str(uuid.uuid4()),
            "product_id": product_data.product_id,
            "base_price": float(base_price),
            "scenarios": scenarios,
            "best_scenario": {
                "name": best_scenario[0],
                "details": best_scenario[1]
            },
            "insights": {
                "optimal_direction": "increase" if best_scenario[1]["price_change_percent"] > 0 else "decrease",
                "sensitivity_analysis": "high" if abs(elasticity_analysis.elasticity_coefficient) > 1.0 else "low",
                "recommendation_confidence": "high" if best_scenario[1]["risk_level"] == "low" else "medium"
            },
            "timestamp": datetime.now().isoformat()
        }

    def _get_scenario_recommendation(self, price_change: float, demand_change: float, revenue_change: float) -> str:
        """Gera recomendação para cenário específico"""
        if revenue_change > 10:
            return "Highly recommended - significant revenue increase"
        elif revenue_change > 5:
            return "Recommended - positive revenue impact"
        elif revenue_change > 0:
            return "Consider - marginal revenue improvement"
        elif revenue_change > -5:
            return "Neutral - minimal impact"
        else:
            return "Not recommended - negative revenue impact"

def create_agents() -> List[PricingOptimizerAgent]:
    """
    Função obrigatória para criação de agentes.
    Retorna lista de agentes Pricing Optimizer para o módulo Sales.
    """
    return [PricingOptimizerAgent()]

# Função de inicialização para compatibilidade
def initialize_pricing_optimizer_agent():
    """Inicializa o agente Pricing Optimizer"""
    return PricingOptimizerAgent()

# Ponto de entrada para testes
if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        agent = PricingOptimizerAgent()
        
        # Teste de otimização de preço
        test_data = {
            "action": "optimize_price",
            "product_data": {
                "product_id": "PROD_001",
                "name": "ALSHAM QUANTUM Premium",
                "category": "software",
                "cost_of_goods": "50.00",
                "current_price": "299.00",
                "target_margin": 0.40,
                "features_score": 0.85,
                "brand_strength": 0.75,
                "market_position": "leader",
                "lifecycle_stage": "growth",
                "seasonality_factor": 1.1
            },
            "market_data": {
                "market_size": 50000000,
                "growth_rate": 15.0,
                "competitor_prices": ["199.00", "349.00", "279.00", "399.00"],
                "market_share": 0.25,
                "price_sensitivity": 0.6,
                "seasonal_trends": {"Q4": 1.2, "Q1": 0.9},
                "economic_indicators": {"inflation": 0.05, "gdp_growth": 0.03}
            }
        }
        
        result = await agent.process(test_data)
        print("Teste Pricing Optimizer Agent:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Teste de análise de elasticidade
        elasticity_test = {
            "action": "analyze_elasticity",
            "product_data": test_data["product_data"],
            "market_data": test_data["market_data"]
        }
        
        elasticity_result = await agent.process(elasticity_test)
        print("\nTeste Análise de Elasticidade:")
        print(json.dumps(elasticity_result, indent=2, ensure_ascii=False))
        
    # Executar teste
    asyncio.run(test_agent())
