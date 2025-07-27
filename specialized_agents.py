import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class SpecialtyType(Enum):
    """Tipos de especialização dos agentes"""
    ANALYSIS = "analysis"
    OPTIMIZATION = "optimization"
    DATA_ANALYSIS = "data_analysis"
    REPORTING = "reporting"
    PREDICTION = "prediction"
    FORECASTING = "forecasting"

@dataclass
class AgentConfig:
    """Configuração para criação de agentes"""
    agent_class: type
    agent_id: str
    capabilities: List[str]
    specialty: SpecialtyType

class SpecialistAgent(BaseNetworkAgent):
    """Agente especialista em análise e otimização"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['analysis', 'optimization']
        self.specialty = SpecialtyType.ANALYSIS
        self._setup_capability_handlers()
        logger.info(f"✅ {self.agent_id} inicializado com especialização em {self.specialty.value}")
    
    def _setup_capability_handlers(self):
        """Configura handlers para cada capability"""
        self.capability_handlers = {
            'analysis': self._perform_analysis,
            'optimization': self._perform_optimization
        }
    
    async def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa análise especializada nos dados"""
        try:
            logger.info(f"🔍 {self.agent_id} executando análise...")
            # Simulação de análise
            result = {
                'status': 'completed',
                'analysis_type': 'general',
                'data_points': len(data.get('items', [])),
                'timestamp': str(datetime.now()),
                'findings': []
            }
            
            # Análise básica
            if 'items' in data:
                result['findings'].append(f"Processados {len(data['items'])} itens")
            
            return result
        except Exception as e:
            logger.error(f"❌ Erro na análise: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _perform_optimization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa otimização nos dados"""
        try:
            logger.info(f"⚡ {self.agent_id} executando otimização...")
            # Simulação de otimização
            result = {
                'status': 'completed',
                'optimization_type': 'performance',
                'improvements': [],
                'metrics': {
                    'before': data.get('current_performance', 0),
                    'after': data.get('current_performance', 0) * 1.15  # 15% melhoria simulada
                }
            }
            return result
        except Exception as e:
            logger.error(f"❌ Erro na otimização: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens com base nas capabilities"""
        await super().handle_message(message)
        
        # Processar requisições de capability
        if message.message_type == MessageType.REQUEST:
            requested_capability = message.content.get('capability')
            if requested_capability in self.capability_handlers:
                result = await self.capability_handlers[requested_capability](message.content.get('data', {}))
                
                # Enviar resposta
                response = AgentMessage(
                    id=str(uuid.uuid4()),
                    sender_id=self.agent_id,
                    recipient_id=message.sender_id,
                    message_type=MessageType.RESPONSE,
                    priority=message.priority,
                    content={
                        'capability': requested_capability,
                        'result': result
                    },
                    timestamp=datetime.now(),
                    correlation_id=message.id
                )
                await self.message_bus.publish(response)

class AnalyticsAgent(BaseNetworkAgent):
    """Agente especializado em análise de dados e relatórios"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['data_analysis', 'reporting']
        self.specialty = SpecialtyType.DATA_ANALYSIS
        self._setup_capability_handlers()
        self.analysis_cache = {}  # Cache para análises frequentes
        logger.info(f"✅ {self.agent_id} inicializado com especialização em {self.specialty.value}")
    
    def _setup_capability_handlers(self):
        """Configura handlers para cada capability"""
        self.capability_handlers = {
            'data_analysis': self._analyze_data,
            'reporting': self._generate_report
        }
    
    async def _analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza análise detalhada de dados"""
        try:
            logger.info(f"📊 {self.agent_id} analisando dados...")
            
            # Verificar cache
            cache_key = str(hash(str(data)))
            if cache_key in self.analysis_cache:
                logger.info(f"📋 Retornando análise do cache")
                return self.analysis_cache[cache_key]
            
            analysis = {
                'status': 'completed',
                'statistics': {
                    'total_records': len(data.get('records', [])),
                    'data_types': list(set(type(v).__name__ for v in data.values())),
                    'completeness': self._calculate_completeness(data)
                },
                'insights': []
            }
            
            # Adicionar ao cache
            self.analysis_cache[cache_key] = analysis
            
            return analysis
        except Exception as e:
            logger.error(f"❌ Erro na análise de dados: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _calculate_completeness(self, data: Dict[str, Any]) -> float:
        """Calcula a completude dos dados"""
        if not data:
            return 0.0
        
        total_fields = len(data)
        filled_fields = sum(1 for v in data.values() if v is not None and v != "")
        return (filled_fields / total_fields) * 100 if total_fields > 0 else 0.0
    
    async def _generate_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera relatório baseado nos dados"""
        try:
            logger.info(f"📄 {self.agent_id} gerando relatório...")
            
            report = {
                'status': 'completed',
                'report_type': data.get('type', 'general'),
                'sections': [],
                'summary': {
                    'generated_at': str(datetime.now()),
                    'total_sections': 0
                }
            }
            
            # Adicionar seções baseadas nos dados
            if 'analysis_results' in data:
                report['sections'].append({
                    'title': 'Resultados da Análise',
                    'content': data['analysis_results']
                })
            
            report['summary']['total_sections'] = len(report['sections'])
            
            return report
        except Exception as e:
            logger.error(f"❌ Erro gerando relatório: {e}")
            return {'status': 'error', 'message': str(e)}

class PredictorAgent(BaseNetworkAgent):
    """Agente especializado em predições e previsões"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['prediction', 'forecasting']
        self.specialty = SpecialtyType.PREDICTION
        self._setup_capability_handlers()
        self.prediction_models = {}  # Armazena modelos de predição
        logger.info(f"✅ {self.agent_id} inicializado com especialização em {self.specialty.value}")
    
    def _setup_capability_handlers(self):
        """Configura handlers para cada capability"""
        self.capability_handlers = {
            'prediction': self._make_prediction,
            'forecasting': self._make_forecast
        }
    
    async def _make_prediction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza predição baseada nos dados"""
        try:
            logger.info(f"🔮 {self.agent_id} fazendo predição...")
            
            prediction = {
                'status': 'completed',
                'prediction_type': data.get('type', 'general'),
                'confidence': 0.85,  # Confiança simulada
                'result': {
                    'value': None,
                    'range': {'min': 0, 'max': 100},
                    'factors': []
                }
            }
            
            # Simulação de predição
            if 'historical_data' in data:
                avg = sum(data['historical_data']) / len(data['historical_data'])
                prediction['result']['value'] = avg * 1.1  # Previsão 10% acima da média
                prediction['result']['factors'].append('Tendência histórica')
            
            return prediction
        except Exception as e:
            logger.error(f"❌ Erro na predição: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _make_forecast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza previsão de longo prazo"""
        try:
            logger.info(f"📈 {self.agent_id} fazendo forecast...")
            
            forecast = {
                'status': 'completed',
                'forecast_period': data.get('period', '30_days'),
                'scenarios': {
                    'optimistic': {'probability': 0.25, 'values': []},
                    'realistic': {'probability': 0.50, 'values': []},
                    'pessimistic': {'probability': 0.25, 'values': []}
                },
                'methodology': 'time_series_analysis'
            }
            
            # Gerar valores simulados para cada cenário
            base_value = data.get('current_value', 100)
            periods = data.get('periods', 10)
            
            for i in range(periods):
                forecast['scenarios']['optimistic']['values'].append(base_value * (1.02 ** i))
                forecast['scenarios']['realistic']['values'].append(base_value * (1.01 ** i))
                forecast['scenarios']['pessimistic']['values'].append(base_value * (0.99 ** i))
            
            return forecast
        except Exception as e:
            logger.error(f"❌ Erro no forecast: {e}")
            return {'status': 'error', 'message': str(e)}

# Configuração dos agentes
AGENT_CONFIGURATIONS = [
    AgentConfig(SpecialistAgent, "specialist_001", ['analysis', 'optimization'], SpecialtyType.ANALYSIS),
    AgentConfig(AnalyticsAgent, "analytics_001", ['data_analysis', 'reporting'], SpecialtyType.DATA_ANALYSIS),
    AgentConfig(PredictorAgent, "predictor_001", ['prediction', 'forecasting'], SpecialtyType.PREDICTION),
    AgentConfig(SpecialistAgent, "specialist_002", ['analysis', 'optimization'], SpecialtyType.OPTIMIZATION),
    AgentConfig(AnalyticsAgent, "analytics_002", ['data_analysis', 'reporting'], SpecialtyType.REPORTING)
]

def create_specialized_agents(message_bus, num_instances=1) -> List:
    """
    Cria agentes especializados com base na configuração
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com exatamente 5 agentes especializados
    """
    agents = []
    
    try:
        logger.info("🎯 Criando agentes especializados com configuração aprimorada...")
        
        # Verificar agentes existentes no message_bus
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
            if existing_agents:
                logger.info(f"📋 {len(existing_agents)} agentes já existentes no sistema")
        
        # Criar agentes baseados na configuração
        for config in AGENT_CONFIGURATIONS:
            if config.agent_id not in existing_agents:
                try:
                    # Criar instância do agente
                    agent = config.agent_class(
                        config.agent_id, 
                        AgentType.SPECIALIZED, 
                        message_bus
                    )
                    
                    # Adicionar capabilities configuradas
                    for capability in config.capabilities:
                        if capability not in agent.capabilities:
                            agent.capabilities.append(capability)
                    
                    agents.append(agent)
                    logger.info(f"✅ Agente {config.agent_id} criado com sucesso")
                    logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                    
                except Exception as e:
                    logger.error(f"❌ Erro criando agente {config.agent_id}: {e}")
            else:
                logger.warning(f"⚠️ Agente {config.agent_id} já existe - pulando criação")
        
        # Validar quantidade de agentes
        if len(agents) != 5:
            logger.warning(f"⚠️ Criados {len(agents)} agentes, esperado 5")
            
        logger.info(f"✅ {len(agents)} agentes especializados criados com sucesso")
        logger.info(f"📋 IDs dos agentes: {[agent.agent_id for agent in agents]}")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando agentes especializados: {e}")
        return []

# Importações necessárias que estavam faltando
import uuid
from datetime import datetime
