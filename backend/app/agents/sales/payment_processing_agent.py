"""
ALSHAM QUANTUM - Payment Processing Agent (Sales Module)
Versão Nativa - Sem dependências SUNA-ALSHAM
Corrigido em: 07/08/2025

Agente especializado em:
- Processamento seguro de pagamentos
- Gerenciamento de assinaturas
- Integração com múltiplos gateways
- Análise de transações e fraudes
- Conciliação financeira
"""

import asyncio
import json
import logging
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from decimal import Decimal
import uuid
import re

# Imports opcionais para gateways
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False

try:
    import mercadopago
    MERCADOPAGO_AVAILABLE = True
except ImportError:
    MERCADOPAGO_AVAILABLE = False

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

class PaymentMethod(Enum):
    """Métodos de pagamento suportados"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    PIX = "pix"
    BOLETO = "boleto"
    PAYPAL = "paypal"
    DIGITAL_WALLET = "digital_wallet"

class PaymentStatus(Enum):
    """Status de pagamentos"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    DISPUTED = "disputed"

class PaymentGateway(Enum):
    """Gateways de pagamento suportados"""
    STRIPE = "stripe"
    MERCADOPAGO = "mercadopago"
    PAGSEGURO = "pagseguro"
    CIELO = "cielo"
    INTERNAL = "internal"  # Sistema interno para testes

class FraudRiskLevel(Enum):
    """Níveis de risco de fraude"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass
class PaymentRequest:
    """Estrutura de requisição de pagamento"""
    amount: Decimal
    currency: str
    payment_method: PaymentMethod
    customer_id: str
    description: str
    gateway: PaymentGateway = PaymentGateway.INTERNAL
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class PaymentResult:
    """Resultado do processamento de pagamento"""
    transaction_id: str
    status: PaymentStatus
    gateway_response: Dict[str, Any]
    amount_processed: Decimal
    fees: Decimal
    net_amount: Decimal
    processing_time: float
    fraud_score: float
    gateway_transaction_id: Optional[str] = None
    receipt_url: Optional[str] = None
    error_message: Optional[str] = None

@dataclass
class SubscriptionRequest:
    """Estrutura de requisição de assinatura"""
    customer_id: str
    plan_id: str
    payment_method: PaymentMethod
    billing_cycle: str  # monthly, yearly, weekly
    trial_period_days: int = 0
    discount_percent: float = 0.0
    metadata: Dict[str, Any] = None

@dataclass
class FraudAnalysis:
    """Análise de fraude"""
    risk_level: FraudRiskLevel
    risk_score: float
    risk_factors: List[str]
    recommendations: List[str]
    requires_manual_review: bool

class PaymentProcessingAgent(BaseNetworkAgent):
    """Agente de Processamento de Pagamentos nativo do ALSHAM QUANTUM"""
    
    def __init__(self):
        super().__init__("payment_processing_agent", "Payment Processing Agent")
        
        # Configurações de gateway
        self.gateway_configs = {
            PaymentGateway.STRIPE: {
                "enabled": STRIPE_AVAILABLE,
                "fees": {
                    "credit_card": 0.029,  # 2.9% + $0.30
                    "debit_card": 0.029,
                    "default": 0.029
                },
                "supported_methods": [PaymentMethod.CREDIT_CARD, PaymentMethod.DEBIT_CARD]
            },
            PaymentGateway.MERCADOPAGO: {
                "enabled": MERCADOPAGO_AVAILABLE,
                "fees": {
                    "credit_card": 0.0399,  # 3.99%
                    "pix": 0.0099,  # 0.99%
                    "boleto": 3.49,  # R$ 3.49 flat fee
                    "default": 0.0399
                },
                "supported_methods": [
                    PaymentMethod.CREDIT_CARD, 
                    PaymentMethod.PIX, 
                    PaymentMethod.BOLETO
                ]
            },
            PaymentGateway.INTERNAL: {
                "enabled": True,
                "fees": {"default": 0.0},
                "supported_methods": list(PaymentMethod)
            }
        }
        
        # Cache de transações
        self.transaction_cache = {}
        
        # Configurações de fraude
        self.fraud_rules = {
            "max_amount_single": Decimal("10000.00"),
            "max_amount_daily": Decimal("50000.00"),
            "max_attempts_per_hour": 5,
            "suspicious_countries": ["XX", "YY"],  # Códigos de países suspeitos
            "velocity_threshold": 3  # Máximo de transações por minuto
        }
        
        # Blacklist de cartões/emails
        self.blacklist = {
            "cards": set(),
            "emails": set(),
            "ips": set()
        }
        
        self.logger.info("Payment Processing Agent inicializado com engine nativo")

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisições de pagamento"""
        try:
            action = data.get("action", "process_payment")
            
            if action == "process_payment":
                return await self._process_payment(data)
            elif action == "create_subscription":
                return await self._create_subscription(data)
            elif action == "refund_payment":
                return await self._refund_payment(data)
            elif action == "verify_payment":
                return await self._verify_payment(data)
            elif action == "analyze_fraud":
                return await self._analyze_fraud(data)
            elif action == "get_transaction_history":
                return await self._get_transaction_history(data)
            elif action == "reconcile_payments":
                return await self._reconcile_payments(data)
            elif action == "gateway_health":
                return await self._check_gateway_health(data)
            else:
                return {"error": f"Ação não reconhecida: {action}"}
                
        except Exception as e:
            self.logger.error(f"Erro no processamento de pagamento: {str(e)}")
            return {"error": str(e)}

    async def _process_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um pagamento"""
        start_time = datetime.now()
        
        # Validar dados de entrada
        validation_result = self._validate_payment_data(data)
        if validation_result.get("error"):
            return validation_result
            
        # Criar requisição de pagamento
        payment_request = self._create_payment_request(data)
        
        # Análise de fraude
        fraud_analysis = await self._perform_fraud_analysis(payment_request, data)
        
        if fraud_analysis.requires_manual_review:
            return {
                "status": "pending_review",
                "message": "Transação requer revisão manual",
                "fraud_analysis": asdict(fraud_analysis),
                "review_token": self._generate_review_token()
            }
            
        if fraud_analysis.risk_level == FraudRiskLevel.VERY_HIGH:
            return {
                "status": "blocked",
                "message": "Transação bloqueada por alto risco de fraude",
                "fraud_analysis": asdict(fraud_analysis)
            }
            
        # Selecionar gateway
        gateway = self._select_best_gateway(payment_request)
        
        # Processar pagamento
        try:
            result = await self._execute_payment(payment_request, gateway, fraud_analysis)
            
            # Calcular tempo de processamento
            processing_time = (datetime.now() - start_time).total_seconds()
            result.processing_time = processing_time
            
            # Salvar no cache
            self.transaction_cache[result.transaction_id] = {
                "request": asdict(payment_request),
                "result": asdict(result),
                "timestamp": datetime.now().isoformat(),
                "fraud_analysis": asdict(fraud_analysis)
            }
            
            return {
                "transaction_id": result.transaction_id,
                "status": result.status.value,
                "amount_processed": float(result.amount_processed),
                "net_amount": float(result.net_amount),
                "fees": float(result.fees),
                "gateway": gateway.value,
                "gateway_transaction_id": result.gateway_transaction_id,
                "receipt_url": result.receipt_url,
                "processing_time": result.processing_time,
                "fraud_score": result.fraud_score,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erro na execução do pagamento: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "transaction_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat()
            }

    async def _execute_payment(self, payment_request: PaymentRequest, gateway: PaymentGateway, fraud_analysis: FraudAnalysis) -> PaymentResult:
        """Executa o pagamento no gateway selecionado"""
        
        if gateway == PaymentGateway.STRIPE and STRIPE_AVAILABLE:
            return await self._process_stripe_payment(payment_request)
        elif gateway == PaymentGateway.MERCADOPAGO and MERCADOPAGO_AVAILABLE:
            return await self._process_mercadopago_payment(payment_request)
        else:
            return await self._process_internal_payment(payment_request, fraud_analysis)

    async def _process_stripe_payment(self, payment_request: PaymentRequest) -> PaymentResult:
        """Processa pagamento via Stripe"""
        try:
            # Simular processamento Stripe (implementar com API real)
            transaction_id = str(uuid.uuid4())
            gateway_transaction_id = f"pi_{secrets.token_hex(12)}"
            
            # Calcular taxas
            fees = self._calculate_fees(payment_request.amount, PaymentGateway.STRIPE, payment_request.payment_method)
            net_amount = payment_request.amount - fees
            
            # Simular resposta do Stripe
            gateway_response = {
                "id": gateway_transaction_id,
                "status": "succeeded",
                "amount": int(payment_request.amount * 100),  # Stripe usa centavos
                "currency": payment_request.currency.lower(),
                "description": payment_request.description
            }
            
            return PaymentResult(
                transaction_id=transaction_id,
                status=PaymentStatus.COMPLETED,
                gateway_response=gateway_response,
                amount_processed=payment_request.amount,
                fees=fees,
                net_amount=net_amount,
                processing_time=0.0,
                fraud_score=0.2,
                gateway_transaction_id=gateway_transaction_id,
                receipt_url=f"https://stripe.com/receipt/{gateway_transaction_id}"
            )
            
        except Exception as e:
            raise Exception(f"Erro no processamento Stripe: {str(e)}")

    async def _process_mercadopago_payment(self, payment_request: PaymentRequest) -> PaymentResult:
        """Processa pagamento via MercadoPago"""
        try:
            transaction_id = str(uuid.uuid4())
            gateway_transaction_id = f"mp_{secrets.token_hex(10)}"
            
            # Calcular taxas
            fees = self._calculate_fees(payment_request.amount, PaymentGateway.MERCADOPAGO, payment_request.payment_method)
            net_amount = payment_request.amount - fees
            
            # Simular resposta do MercadoPago
            gateway_response = {
                "id": int(secrets.token_hex(4), 16),
                "status": "approved",
                "amount": float(payment_request.amount),
                "currency": payment_request.currency,
                "payment_method": payment_request.payment_method.value
            }
            
            return PaymentResult(
                transaction_id=transaction_id,
                status=PaymentStatus.COMPLETED,
                gateway_response=gateway_response,
                amount_processed=payment_request.amount,
                fees=fees,
                net_amount=net_amount,
                processing_time=0.0,
                fraud_score=0.15,
                gateway_transaction_id=gateway_transaction_id
            )
            
        except Exception as e:
            raise Exception(f"Erro no processamento MercadoPago: {str(e)}")

    async def _process_internal_payment(self, payment_request: PaymentRequest, fraud_analysis: FraudAnalysis) -> PaymentResult:
        """Processa pagamento via sistema interno"""
        transaction_id = str(uuid.uuid4())
        
        # Sistema interno - sem taxas
        fees = Decimal("0.00")
        net_amount = payment_request.amount
        
        # Status baseado na análise de fraude
        if fraud_analysis.risk_level == FraudRiskLevel.HIGH:
            status = PaymentStatus.PENDING
        else:
            status = PaymentStatus.COMPLETED
            
        gateway_response = {
            "transaction_id": transaction_id,
            "status": "processed",
            "processor": "alsham_internal",
            "fraud_score": fraud_analysis.risk_score
        }
        
        return PaymentResult(
            transaction_id=transaction_id,
            status=status,
            gateway_response=gateway_response,
            amount_processed=payment_request.amount,
            fees=fees,
            net_amount=net_amount,
            processing_time=0.0,
            fraud_score=fraud_analysis.risk_score
        )

    async def _perform_fraud_analysis(self, payment_request: PaymentRequest, raw_data: Dict[str, Any]) -> FraudAnalysis:
        """Realiza análise de fraude"""
        risk_factors = []
        risk_score = 0.0
        
        # Verificar valor da transação
        if payment_request.amount > self.fraud_rules["max_amount_single"]:
            risk_factors.append(f"Valor alto: R$ {payment_request.amount}")
            risk_score += 0.3
            
        # Verificar blacklist
        customer_email = raw_data.get("customer_email", "")
        customer_ip = raw_data.get("customer_ip", "")
        card_hash = raw_data.get("card_hash", "")
        
        if customer_email in self.blacklist["emails"]:
            risk_factors.append("Email em blacklist")
            risk_score += 0.5
            
        if customer_ip in self.blacklist["ips"]:
            risk_factors.append("IP em blacklist")
            risk_score += 0.4
            
        if card_hash in self.blacklist["cards"]:
            risk_factors.append("Cartão em blacklist")
            risk_score += 0.6
            
        # Verificar país
        customer_country = raw_data.get("customer_country", "BR")
        if customer_country in self.fraud_rules["suspicious_countries"]:
            risk_factors.append(f"País suspeito: {customer_country}")
            risk_score += 0.25
            
        # Verificar velocidade de transações
        recent_transactions = self._count_recent_transactions(payment_request.customer_id)
        if recent_transactions > self.fraud_rules["velocity_threshold"]:
            risk_factors.append(f"Muitas transações recentes: {recent_transactions}")
            risk_score += 0.2
            
        # Determinar nível de risco
        if risk_score >= 0.8:
            risk_level = FraudRiskLevel.VERY_HIGH
        elif risk_score >= 0.6:
            risk_level = FraudRiskLevel.HIGH
        elif risk_score >= 0.4:
            risk_level = FraudRiskLevel.MEDIUM
        else:
            risk_level = FraudRiskLevel.LOW
            
        # Gerar recomendações
        recommendations = self._generate_fraud_recommendations(risk_level, risk_factors)
        
        return FraudAnalysis(
            risk_level=risk_level,
            risk_score=risk_score,
            risk_factors=risk_factors,
            recommendations=recommendations,
            requires_manual_review=(risk_score >= 0.7)
        )

    def _generate_fraud_recommendations(self, risk_level: FraudRiskLevel, risk_factors: List[str]) -> List[str]:
        """Gera recomendações baseadas na análise de fraude"""
        recommendations = []
        
        if risk_level == FraudRiskLevel.VERY_HIGH:
            recommendations.extend([
                "Bloquear transação imediatamente",
                "Investigar padrões de fraude",
                "Adicionar cliente à watch list"
            ])
        elif risk_level == FraudRiskLevel.HIGH:
            recommendations.extend([
                "Revisar manualmente antes de processar",
                "Solicitar verificação adicional do cliente",
                "Monitorar transações futuras"
            ])
        elif risk_level == FraudRiskLevel.MEDIUM:
            recommendations.extend([
                "Processar com monitoramento adicional",
                "Verificar dados do cliente",
                "Aplicar limites de transação"
            ])
            
        # Recomendações específicas por fator
        for factor in risk_factors:
            if "blacklist" in factor.lower():
                recommendations.append("Verificar motivo da inclusão em blacklist")
            if "valor alto" in factor.lower():
                recommendations.append("Confirmar capacidade de pagamento")
            if "país suspeito" in factor.lower():
                recommendations.append("Verificar documentação internacional")
                
        return list(set(recommendations))  # Remove duplicatas

    def _select_best_gateway(self, payment_request: PaymentRequest) -> PaymentGateway:
        """Seleciona o melhor gateway para a transação"""
        
        # Verificar método de pagamento suportado
        for gateway, config in self.gateway_configs.items():
            if (config["enabled"] and 
                payment_request.payment_method in config["supported_methods"]):
                
                # Lógica de seleção baseada em custos e disponibilidade
                if payment_request.payment_method == PaymentMethod.PIX:
                    return PaymentGateway.MERCADOPAGO  # Melhores taxas para PIX
                elif payment_request.payment_method in [PaymentMethod.CREDIT_CARD, PaymentMethod.DEBIT_CARD]:
                    if STRIPE_AVAILABLE:
                        return PaymentGateway.STRIPE  # Melhor para cartões internacionais
                    elif MERCADOPAGO_AVAILABLE:
                        return PaymentGateway.MERCADOPAGO
                        
        return PaymentGateway.INTERNAL  # Fallback

    def _calculate_fees(self, amount: Decimal, gateway: PaymentGateway, payment_method: PaymentMethod) -> Decimal:
        """Calcula as taxas de transação"""
        config = self.gateway_configs.get(gateway, {})
        fees_config = config.get("fees", {})
        
        fee_rate = fees_config.get(payment_method.value, fees_config.get("default", 0.0))
        
        if isinstance(fee_rate, float) and fee_rate < 1.0:  # Percentual
            return amount * Decimal(str(fee_rate))
        else:  # Valor fixo
            return Decimal(str(fee_rate))

    def _validate_payment_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida dados de pagamento"""
        required_fields = ["amount", "currency", "customer_id", "payment_method"]
        
        for field in required_fields:
            if not data.get(field):
                return {"error": f"Campo obrigatório ausente: {field}"}
                
        # Validar valor
        try:
            amount = Decimal(str(data["amount"]))
            if amount <= 0:
                return {"error": "Valor deve ser maior que zero"}
        except (ValueError, TypeError):
            return {"error": "Valor inválido"}
            
        # Validar método de pagamento
        try:
            PaymentMethod(data["payment_method"])
        except ValueError:
            return {"error": "Método de pagamento inválido"}
            
        return {"valid": True}

    def _create_payment_request(self, data: Dict[str, Any]) -> PaymentRequest:
        """Cria objeto PaymentRequest dos dados"""
        return PaymentRequest(
            amount=Decimal(str(data["amount"])),
            currency=data["currency"],
            payment_method=PaymentMethod(data["payment_method"]),
            customer_id=data["customer_id"],
            description=data.get("description", "Pagamento ALSHAM QUANTUM"),
            gateway=PaymentGateway(data.get("gateway", "internal")),
            metadata=data.get("metadata", {})
        )

    def _count_recent_transactions(self, customer_id: str) -> int:
        """Conta transações recentes do cliente"""
        count = 0
        cutoff_time = datetime.now() - timedelta(minutes=60)
        
        for transaction in self.transaction_cache.values():
            if (transaction["request"]["customer_id"] == customer_id and
                datetime.fromisoformat(transaction["timestamp"]) > cutoff_time):
                count += 1
                
        return count

    def _generate_review_token(self) -> str:
        """Gera token para revisão manual"""
        return f"review_{secrets.token_hex(16)}"

    async def _create_subscription(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria assinatura recorrente"""
        # Implementação de criação de assinatura
        subscription_id = str(uuid.uuid4())
        
        return {
            "subscription_id": subscription_id,
            "status": "active",
            "next_billing_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "created_at": datetime.now().isoformat()
        }

    async def _refund_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa reembolso"""
        transaction_id = data.get("transaction_id")
        refund_amount = data.get("amount")
        reason = data.get("reason", "Customer request")
        
        if transaction_id not in self.transaction_cache:
            return {"error": "Transação não encontrada"}
            
        refund_id = str(uuid.uuid4())
        
        return {
            "refund_id": refund_id,
            "transaction_id": transaction_id,
            "amount_refunded": refund_amount,
            "status": "completed",
            "reason": reason,
            "processed_at": datetime.now().isoformat()
        }

    async def _verify_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica status de pagamento"""
        transaction_id = data.get("transaction_id")
        
        if transaction_id in self.transaction_cache:
            transaction = self.transaction_cache[transaction_id]
            return {
                "transaction_id": transaction_id,
                "status": transaction["result"]["status"],
                "amount": transaction["result"]["amount_processed"],
                "verified": True,
                "timestamp": transaction["timestamp"]
            }
        else:
            return {
                "transaction_id": transaction_id,
                "verified": False,
                "error": "Transação não encontrada"
            }

    async def _analyze_fraud(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise de fraude standalone"""
        payment_request = self._create_payment_request(data)
        fraud_analysis = await self._perform_fraud_analysis(payment_request, data)
        
        return {
            "analysis_id": str(uuid.uuid4()),
            "fraud_analysis": asdict(fraud_analysis),
            "timestamp": datetime.now().isoformat()
        }

    async def _get_transaction_history(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Obtém histórico de transações"""
        customer_id = data.get("customer_id")
        limit = data.get("limit", 50)
        
        transactions = []
        count = 0
        
        for transaction in self.transaction_cache.values():
            if (transaction["request"]["customer_id"] == customer_id and 
                count < limit):
                transactions.append({
                    "transaction_id": transaction["result"]["transaction_id"],
                    "amount": transaction["result"]["amount_processed"],
                    "status": transaction["result"]["status"],
                    "timestamp": transaction["timestamp"],
                    "payment_method": transaction["request"]["payment_method"]
                })
                count += 1
                
        return {
            "customer_id": customer_id,
            "total_transactions": count,
            "transactions": transactions
        }

    async def _reconcile_payments(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Conciliação de pagamentos"""
        date_range = data.get("date_range", {})
        gateway = data.get("gateway")
        
        # Simular conciliação
        reconciliation_id = str(uuid.uuid4())
        
        return {
            "reconciliation_id": reconciliation_id,
            "gateway": gateway,
            "period": date_range,
            "total_transactions": len(self.transaction_cache),
            "total_amount": sum(float(t["result"]["amount_processed"]) for t in self.transaction_cache.values()),
            "discrepancies": [],
            "status": "completed",
            "processed_at": datetime.now().isoformat()
        }

    async def _check_gateway_health(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica saúde dos gateways"""
        health_status = {}
        
        for gateway, config in self.gateway_configs.items():
            health_status[gateway.value] = {
                "enabled": config["enabled"],
                "status": "online" if config["enabled"] else "offline",
                "supported_methods": [method.value for method in config["supported_methods"]],
                "last_check": datetime.now().isoformat()
            }
            
        return {
            "overall_status": "healthy",
            "gateways": health_status,
            "active_gateways": len([g for g in health_status.values() if g["enabled"]]),
            "check_timestamp": datetime.now().isoformat()
        }

def create_agents() -> List[PaymentProcessingAgent]:
    """
    Função obrigatória para criação de agentes.
    Retorna lista de agentes Payment Processing para o módulo Sales.
    """
    return [PaymentProcessingAgent()]

# Função de inicialização para compatibilidade
def initialize_payment_processing_agent():
    """Inicializa o agente Payment Processing"""
    return PaymentProcessingAgent()

# Ponto de entrada para testes
if __name__ == "__main__":
    import asyncio
    
    async def test_agent():
        agent = PaymentProcessingAgent()
        
        # Teste de pagamento
        test_payment = {
            "action": "process_payment",
            "amount": "150.00",
            "currency": "BRL",
            "customer_id": "CUST_001",
            "payment_method": "credit_card",
            "description": "Teste de pagamento ALSHAM QUANTUM",
            "customer_email": "test@example.com",
            "customer_ip": "192.168.1.1",
            "customer_country": "BR"
        }
        
        result = await agent.process(test_payment)
        print("Teste Payment Processing Agent:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Teste de análise de fraude
        fraud_test = {
            "action": "analyze_fraud",
            "amount": "50000.00",  # Valor alto para teste
            "currency": "BRL",
            "customer_id": "CUST_002",
            "payment_method": "credit_card",
            "customer_email": "suspicious@example.com"
        }
        
        fraud_result = await agent.process(fraud_test)
        print("\nTeste Análise de Fraude:")
        print(json.dumps(fraud_result, indent=2, ensure_ascii=False))
        
    # Executar teste
    asyncio.run(test_agent())
