import logging
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import json
from collections import defaultdict
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class CommunicationProtocol(Enum):
    """Protocolos de comunicação suportados"""
    DIRECT = "direct"
    BROADCAST = "broadcast"
    MULTICAST = "multicast"
    REQUEST_RESPONSE = "request_response"
    PUBLISH_SUBSCRIBE = "publish_subscribe"
    ASYNC_CALLBACK = "async_callback"

class DecisionStrategy(Enum):
    """Estratégias de tomada de decisão"""
    CONSENSUS = "consensus"
    VOTING = "voting"
    WEIGHTED = "weighted"
    HIERARCHICAL = "hierarchical"
    AUTONOMOUS = "autonomous"
    COLLABORATIVE = "collaborative"

@dataclass
class CommunicationChannel:
    """Canal de comunicação entre agentes"""
    channel_id: str
    protocol: CommunicationProtocol
    participants: Set[str]
    created_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    message_count: int = 0
    last_activity: Optional[datetime] = None

@dataclass
class Decision:
    """Decisão tomada pelo sistema"""
    decision_id: str
    strategy: DecisionStrategy
    options: List[Dict[str, Any]]
    selected_option: Optional[Dict[str, Any]]
    confidence: float
    participants: List[str]
    rationale: str
    timestamp: datetime
    execution_status: str = "pending"

class CommunicationAgent(BaseNetworkAgent):
    """Agente responsável pela comunicação e roteamento de mensagens"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'communication',
            'message_routing',
            'protocol_translation',
            'channel_management'
        ]
        self.channels = {}  # channel_id -> CommunicationChannel
        self.routing_table = defaultdict(list)  # agent_id -> [channel_ids]
        self.message_queues = defaultdict(asyncio.Queue)  # agent_id -> Queue
        self.protocol_handlers = self._setup_protocol_handlers()
        self.statistics = {
            'messages_routed': 0,
            'channels_created': 0,
            'routing_failures': 0,
            'active_channels': 0
        }
        self._routing_task = None
        logger.info(f"✅ {self.agent_id} inicializado com roteamento avançado")
    
    def _setup_protocol_handlers(self) -> Dict[CommunicationProtocol, callable]:
        """Configura handlers para cada protocolo"""
        return {
            CommunicationProtocol.DIRECT: self._handle_direct_message,
            CommunicationProtocol.BROADCAST: self._handle_broadcast_message,
            CommunicationProtocol.MULTICAST: self._handle_multicast_message,
            CommunicationProtocol.REQUEST_RESPONSE: self._handle_request_response,
            CommunicationProtocol.PUBLISH_SUBSCRIBE: self._handle_publish_subscribe,
            CommunicationProtocol.ASYNC_CALLBACK: self._handle_async_callback
        }
    
    async def start_routing_service(self):
        """Inicia serviço de roteamento"""
        if not self._routing_task:
            self._routing_task = asyncio.create_task(self._message_routing_loop())
            logger.info(f"📡 {self.agent_id} iniciou serviço de roteamento")
    
    async def stop_routing_service(self):
        """Para serviço de roteamento"""
        if self._routing_task:
            self._routing_task.cancel()
            self._routing_task = None
            logger.info(f"🛑 {self.agent_id} parou serviço de roteamento")
    
    async def _message_routing_loop(self):
        """Loop principal de roteamento de mensagens"""
        while True:
            try:
                # Processar filas de mensagens
                for agent_id, queue in self.message_queues.items():
                    if not queue.empty():
                        message = await queue.get()
                        await self._route_message(message)
                
                await asyncio.sleep(0.1)  # Pequeno delay para não sobrecarregar
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de roteamento: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'create_channel':
                result = await self._create_communication_channel(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'send_message':
                result = await self._process_communication_request(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'get_channels':
                result = await self._get_agent_channels(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'channel_stats':
                result = self._get_channel_statistics()
                await self._send_response(message, result)
    
    async def _create_communication_channel(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria novo canal de comunicação"""
        try:
            protocol = CommunicationProtocol(data.get('protocol', 'direct'))
            participants = set(data.get('participants', []))
            metadata = data.get('metadata', {})
            
            channel_id = f"channel_{len(self.channels) + 1:03d}"
            
            channel = CommunicationChannel(
                channel_id=channel_id,
                protocol=protocol,
                participants=participants,
                created_at=datetime.now(),
                metadata=metadata
            )
            
            self.channels[channel_id] = channel
            
            # Atualizar tabela de roteamento
            for participant in participants:
                self.routing_table[participant].append(channel_id)
            
            self.statistics['channels_created'] += 1
            self.statistics['active_channels'] = len([
                c for c in self.channels.values() 
                if c.last_activity and (datetime.now() - c.last_activity).seconds < 3600
            ])
            
            logger.info(f"📢 Canal {channel_id} criado com protocolo {protocol.value}")
            
            return {
                'status': 'completed',
                'channel_id': channel_id,
                'protocol': protocol.value,
                'participants': list(participants)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando canal: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _process_communication_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisição de comunicação"""
        try:
            channel_id = data.get('channel_id')
            protocol = data.get('protocol', 'direct')
            message_content = data.get('message')
            sender = data.get('sender')
            recipients = data.get('recipients', [])
            
            # Se não há canal específico, criar um temporário
            if not channel_id and protocol == 'direct' and recipients:
                temp_channel = await self._create_communication_channel({
                    'protocol': protocol,
                    'participants': [sender] + recipients,
                    'metadata': {'temporary': True}
                })
                channel_id = temp_channel['channel_id']
            
            if channel_id not in self.channels:
                return {
                    'status': 'error',
                    'message': f'Canal {channel_id} não encontrado'
                }
            
            channel = self.channels[channel_id]
            channel.message_count += 1
            channel.last_activity = datetime.now()
            
            # Processar mensagem baseado no protocolo
            protocol_enum = CommunicationProtocol(protocol)
            handler = self.protocol_handlers.get(protocol_enum)
            
            if handler:
                result = await handler({
                    'channel': channel,
                    'message': message_content,
                    'sender': sender,
                    'recipients': recipients
                })
                
                self.statistics['messages_routed'] += 1
                
                return {
                    'status': 'completed',
                    'channel_id': channel_id,
                    'messages_sent': result.get('sent_count', 0),
                    'protocol_used': protocol
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Protocolo {protocol} não suportado'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro processando comunicação: {e}")
            self.statistics['routing_failures'] += 1
            return {'status': 'error', 'message': str(e)}
    
    async def _handle_direct_message(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Envia mensagem direta para um destinatário"""
        try:
            message = AgentMessage(
                id=str(uuid4()),
                sender_id=context['sender'],
                recipient_id=context['recipients'][0],
                message_type=MessageType.REQUEST,
                priority=Priority.MEDIUM,
                content=context['message'],
                timestamp=datetime.now()
            )
            
            await self.message_bus.publish(message)
            
            return {'sent_count': 1}
            
        except Exception as e:
            logger.error(f"❌ Erro em mensagem direta: {e}")
            return {'sent_count': 0}
    
    async def _handle_broadcast_message(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Envia mensagem para todos os participantes do canal"""
        try:
            channel = context['channel']
            sent_count = 0
            
            for participant in channel.participants:
                if participant != context['sender']:
                    message = AgentMessage(
                        id=str(uuid4()),
                        sender_id=context['sender'],
                        recipient_id=participant,
                        message_type=MessageType.BROADCAST,
                        priority=Priority.LOW,
                        content=context['message'],
                        timestamp=datetime.now()
                    )
                    
                    await self.message_bus.publish(message)
                    sent_count += 1
            
            return {'sent_count': sent_count}
            
        except Exception as e:
            logger.error(f"❌ Erro em broadcast: {e}")
            return {'sent_count': 0}
    
    async def _handle_multicast_message(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Envia mensagem para grupo específico"""
        try:
            recipients = context['recipients']
            sent_count = 0
            
            for recipient in recipients:
                message = AgentMessage(
                    id=str(uuid4()),
                    sender_id=context['sender'],
                    recipient_id=recipient,
                    message_type=MessageType.REQUEST,
                    priority=Priority.MEDIUM,
                    content=context['message'],
                    timestamp=datetime.now()
                )
                
                await self.message_bus.publish(message)
                sent_count += 1
            
            return {'sent_count': sent_count}
            
        except Exception as e:
            logger.error(f"❌ Erro em multicast: {e}")
            return {'sent_count': 0}
    
    async def _handle_request_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Envia requisição e aguarda resposta"""
        try:
            # Criar ID de correlação para rastrear resposta
            correlation_id = str(uuid4())
            
            message = AgentMessage(
                id=correlation_id,
                sender_id=context['sender'],
                recipient_id=context['recipients'][0],
                message_type=MessageType.REQUEST,
                priority=Priority.HIGH,
                content=context['message'],
                timestamp=datetime.now(),
                correlation_id=correlation_id
            )
            
            await self.message_bus.publish(message)
            
            # TODO: Implementar espera por resposta com timeout
            
            return {'sent_count': 1, 'correlation_id': correlation_id}
            
        except Exception as e:
            logger.error(f"❌ Erro em request-response: {e}")
            return {'sent_count': 0}
    
    async def _handle_publish_subscribe(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Publica mensagem para subscribers de um tópico"""
        try:
            topic = context['message'].get('topic', 'general')
            channel = context['channel']
            
            # Filtrar subscribers do tópico
            subscribers = [
                p for p in channel.participants
                if channel.metadata.get(f'{p}_subscriptions', {}).get(topic, False)
            ]
            
            sent_count = 0
            for subscriber in subscribers:
                message = AgentMessage(
                    id=str(uuid4()),
                    sender_id=context['sender'],
                    recipient_id=subscriber,
                    message_type=MessageType.NOTIFICATION,
                    priority=Priority.LOW,
                    content={
                        'topic': topic,
                        'data': context['message']
                    },
                    timestamp=datetime.now()
                )
                
                await self.message_bus.publish(message)
                sent_count += 1
            
            return {'sent_count': sent_count}
            
        except Exception as e:
            logger.error(f"❌ Erro em publish-subscribe: {e}")
            return {'sent_count': 0}
    
    async def _handle_async_callback(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Envia mensagem com callback assíncrono"""
        try:
            callback_id = str(uuid4())
            
            # Armazenar callback para execução futura
            self.message_queues[context['sender']].put_nowait({
                'callback_id': callback_id,
                'callback_function': context['message'].get('callback'),
                'timeout': context['message'].get('timeout', 30)
            })
            
            # Enviar mensagem principal
            message = AgentMessage(
                id=str(uuid4()),
                sender_id=context['sender'],
                recipient_id=context['recipients'][0],
                message_type=MessageType.REQUEST,
                priority=Priority.HIGH,
                content={
                    'data': context['message'].get('data'),
                    'callback_id': callback_id
                },
                timestamp=datetime.now()
            )
            
            await self.message_bus.publish(message)
            
            return {'sent_count': 1, 'callback_id': callback_id}
            
        except Exception as e:
            logger.error(f"❌ Erro em async callback: {e}")
            return {'sent_count': 0}
    
    async def _route_message(self, message: Dict[str, Any]):
        """Roteia mensagem através do sistema"""
        # Implementação do roteamento real seria aqui
        pass
    
    async def _get_agent_channels(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna canais de um agente"""
        try:
            agent_id = data.get('agent_id')
            channel_ids = self.routing_table.get(agent_id, [])
            
            channels_info = []
            for channel_id in channel_ids:
                if channel_id in self.channels:
                    channel = self.channels[channel_id]
                    channels_info.append({
                        'channel_id': channel_id,
                        'protocol': channel.protocol.value,
                        'participants': list(channel.participants),
                        'message_count': channel.message_count,
                        'last_activity': channel.last_activity.isoformat() if channel.last_activity else None
                    })
            
            return {
                'status': 'completed',
                'agent_id': agent_id,
                'channels': channels_info
            }
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo canais: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _get_channel_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas dos canais"""
        return {
            'status': 'completed',
            'statistics': {
                'total_channels': len(self.channels),
                'active_channels': self.statistics['active_channels'],
                'messages_routed': self.statistics['messages_routed'],
                'routing_failures': self.statistics['routing_failures'],
                'channels_by_protocol': self._count_channels_by_protocol()
            }
        }
    
    def _count_channels_by_protocol(self) -> Dict[str, int]:
        """Conta canais por protocolo"""
        counts = defaultdict(int)
        for channel in self.channels.values():
            counts[channel.protocol.value] += 1
        return dict(counts)
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
        response = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            priority=original_message.priority,
            content=response_data,
            timestamp=datetime.now(),
            correlation_id=original_message.id
        )
        await self.message_bus.publish(response)

class DecisionAgent(BaseNetworkAgent):
    """Agente responsável por tomada de decisões complexas"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'decision_making',
            'consensus_building',
            'risk_assessment',
            'strategy_evaluation'
        ]
        self.decision_history = []
        self.active_decisions = {}  # decision_id -> Decision
        self.decision_strategies = self._setup_decision_strategies()
        self.voting_sessions = {}  # session_id -> voting data
        self.risk_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
        logger.info(f"✅ {self.agent_id} inicializado com estratégias de decisão")
    
    def _setup_decision_strategies(self) -> Dict[DecisionStrategy, callable]:
        """Configura estratégias de decisão"""
        return {
            DecisionStrategy.CONSENSUS: self._consensus_decision,
            DecisionStrategy.VOTING: self._voting_decision,
            DecisionStrategy.WEIGHTED: self._weighted_decision,
            DecisionStrategy.HIERARCHICAL: self._hierarchical_decision,
            DecisionStrategy.AUTONOMOUS: self._autonomous_decision,
            DecisionStrategy.COLLABORATIVE: self._collaborative_decision
        }
    
    async def handle_message(self, message: AgentMessage):
        """Processa requisições de decisão"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'make_decision':
                result = await self._process_decision_request(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'evaluate_options':
                result = await self._evaluate_options(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'risk_assessment':
                result = await self._assess_risk(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'decision_status':
                result = self._get_decision_status(message.content)
                await self._send_response(message, result)
    
    async def _process_decision_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisição de tomada de decisão"""
        try:
            strategy = DecisionStrategy(data.get('strategy', 'autonomous'))
            options = data.get('options', [])
            context = data.get('context', {})
            participants = data.get('participants', [])
            
            if not options:
                return {
                    'status': 'error',
                    'message': 'Nenhuma opção fornecida para decisão'
                }
            
            decision_id = f"decision_{len(self.decision_history) + 1:03d}"
            
            # Criar objeto de decisão
            decision = Decision(
                decision_id=decision_id,
                strategy=strategy,
                options=options,
                selected_option=None,
                confidence=0.0,
                participants=participants or [self.agent_id],
                rationale="",
                timestamp=datetime.now()
            )
            
            self.active_decisions[decision_id] = decision
            
            # Executar estratégia de decisão
            strategy_handler = self.decision_strategies.get(strategy)
            if strategy_handler:
                result = await strategy_handler(decision, context)
                
                # Atualizar decisão com resultado
                decision.selected_option = result['selected_option']
                decision.confidence = result['confidence']
                decision.rationale = result['rationale']
                decision.execution_status = 'completed'
                
                # Mover para histórico
                self.decision_history.append(decision)
                del self.active_decisions[decision_id]
                
                logger.info(f"🎯 Decisão {decision_id} tomada com {strategy.value}")
                
                return {
                    'status': 'completed',
                    'decision_id': decision_id,
                    'selected_option': decision.selected_option,
                    'confidence': decision.confidence,
                    'rationale': decision.rationale
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Estratégia {strategy.value} não implementada'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro processando decisão: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _consensus_decision(self, decision: Decision, context: Dict[str, Any]) -> Dict[str, Any]:
        """Toma decisão por consenso entre participantes"""
        try:
            # Simular processo de consenso
            votes = {}
            for option in decision.options:
                votes[option['id']] = 0
            
            # Coletar "votos" simulados dos participantes
            for participant in decision.participants:
                # Simular análise do participante
                best_option = self._simulate_participant_preference(
                    participant, decision.options, context
                )
                votes[best_option['id']] += 1
            
            # Verificar se há consenso (maioria absoluta)
            total_votes = len(decision.participants)
            for option_id, vote_count in votes.items():
                if vote_count > total_votes / 2:
                    selected = next(o for o in decision.options if o['id'] == option_id)
                    return {
                        'selected_option': selected,
                        'confidence': vote_count / total_votes,
                        'rationale': f"Consenso alcançado com {vote_count}/{total_votes} votos"
                    }
            
            # Se não há consenso, escolher mais votada
            best_option_id = max(votes, key=votes.get)
            selected = next(o for o in decision.options if o['id'] == best_option_id)
            
            return {
                'selected_option': selected,
                'confidence': votes[best_option_id] / total_votes,
                'rationale': f"Maioria simples com {votes[best_option_id]}/{total_votes} votos"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro em decisão por consenso: {e}")
            return {
                'selected_option': decision.options[0],
                'confidence': 0.5,
                'rationale': f"Erro no consenso: {str(e)}"
            }
    
    async def _voting_decision(self, decision: Decision, context: Dict[str, Any]) -> Dict[str, Any]:
        """Toma decisão por votação formal"""
        try:
            # Criar sessão de votação
            session_id = f"voting_{decision.decision_id}"
            self.voting_sessions[session_id] = {
                'options': decision.options,
                'votes': defaultdict(int),
                'voters': set(),
                'deadline': datetime.now() + timedelta(minutes=5)
            }
            
            # Simular processo de votação
            for participant in decision.participants:
                vote = self._simulate_participant_preference(
                    participant, decision.options, context
                )
                self.voting_sessions[session_id]['votes'][vote['id']] += 1
                self.voting_sessions[session_id]['voters'].add(participant)
            
            # Contabilizar votos
            votes = self.voting_sessions[session_id]['votes']
            total_votes = sum(votes.values())
            
            if total_votes == 0:
                return {
                    'selected_option': decision.options[0],
                    'confidence': 0.0,
                    'rationale': "Nenhum voto recebido"
                }
            
            # Encontrar vencedor
            winner_id = max(votes, key=votes.get)
            winner = next(o for o in decision.options if o['id'] == winner_id)
            
            # Limpar sessão
            del self.voting_sessions[session_id]
            
            return {
                'selected_option': winner,
                'confidence': votes[winner_id] / total_votes,
                'rationale': f"Votação: {votes[winner_id]}/{total_votes} votos"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro em votação: {e}")
            return {
                'selected_option': decision.options[0],
                'confidence': 0.5,
                'rationale': f"Erro na votação: {str(e)}"
            }
    
    async def _weighted_decision(self, decision: Decision, context: Dict[str, Any]) -> Dict[str, Any]:
        """Toma decisão com pesos diferenciados"""
        try:
            # Definir pesos dos critérios
            criteria_weights = context.get('criteria_weights', {
                'cost': 0.3,
                'benefit': 0.4,
                'risk': 0.2,
                'time': 0.1
            })
            
            # Calcular score ponderado para cada opção
            scores = {}
            for option in decision.options:
                score = 0.0
                for criterion, weight in criteria_weights.items():
                    criterion_value = option.get(criterion, 0.5)
                    score += criterion_value * weight
                scores[option['id']] = score
            
            # Selecionar melhor opção
            best_option_id = max(scores, key=scores.get)
            selected = next(o for o in decision.options if o['id'] == best_option_id)
            
            # Calcular confiança baseada na diferença de scores
            sorted_scores = sorted(scores.values(), reverse=True)
            if len(sorted_scores) > 1:
                confidence = min(0.95, (sorted_scores[0] - sorted_scores[1]) * 2)
            else:
                confidence = 0.8
            
            return {
                'selected_option': selected,
                'confidence': confidence,
                'rationale': f"Score ponderado: {scores[best_option_id]:.2f}"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro em decisão ponderada: {e}")
            return {
                'selected_option': decision.options[0],
                'confidence': 0.5,
                'rationale': f"Erro na ponderação: {str(e)}"
            }
    
    async def _hierarchical_decision(self, decision: Decision, context: Dict[str, Any]) -> Dict[str, Any]:
        """Toma decisão baseada em hierarquia"""
        try:
            # Definir hierarquia (simulada)
            hierarchy = context.get('hierarchy', {
                'level_1': ['orchestrator_001'],
                'level_2': ['core_v3_001', 'core_v3_002'],
                'level_3': decision.participants
            })
            
            # Decisão top-down
            for level, agents in sorted(hierarchy.items()):
                if any(agent in decision.participants for agent in agents):
                    # Simular decisão do nível
                    selected = self._simulate_hierarchical_choice(
                        level, decision.options, context
                    )
                    
                    return {
                        'selected_option': selected,
                        'confidence': 0.85,
                        'rationale': f"Decisão hierárquica nível {level}"
                    }
            
            # Fallback para primeira opção
            return {
                'selected_option': decision.options[0],
                'confidence': 0.6,
                'rationale': "Decisão hierárquica padrão"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro em decisão hierárquica: {e}")
            return {
                'selected_option': decision.options[0],
                'confidence': 0.5,
                'rationale': f"Erro na hierarquia: {str(e)}"
            }
    
    async def _autonomous_decision(self, decision: Decision, context: Dict[str, Any]) -> Dict[str, Any]:
        """Toma decisão autônoma baseada em análise"""
        try:
            # Analisar cada opção
            option_scores = {}
            
            for option in decision.options:
                # Calcular score baseado em múltiplos fatores
                score = 0.0
                
                # Fator de benefício
                benefit = option.get('benefit', 0.5)
                score += benefit * 0.4
                
                # Fator de custo (invertido)
                cost = option.get('cost', 0.5)
                score += (1 - cost) * 0.3
                
                # Fator de risco (invertido)
                risk = option.get('risk', 0.5)
                score += (1 - risk) * 0.2
                
                # Fator de tempo
                time_factor = option.get('time_factor', 0.5)
                score += time_factor * 0.1
                
                option_scores[option['id']] = score
            
            # Selecionar melhor opção
            best_option_id = max(option_scores, key=option_scores.get)
            selected = next(o for o in decision.options if o['id'] == best_option_id)
            
            # Confiança baseada no score
            confidence = min(0.95, option_scores[best_option_id])
            
            return {
                'selected_option': selected,
                'confidence': confidence,
                'rationale': f"Análise autônoma: score {option_scores[best_option_id]:.2f}"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro em decisão autônoma: {e}")
            return {
                'selected_option': decision.options[0],
                'confidence': 0.5,
                'rationale': f"Erro na análise: {str(e)}"
            }
    
    async def _collaborative_decision(self, decision: Decision, context: Dict[str, Any]) -> Dict[str, Any]:
        """Toma decisão colaborativa com múltiplas perspectivas"""
        try:
            # Coletar perspectivas de diferentes agentes
            perspectives = {}
            
            for participant in decision.participants:
                # Simular perspectiva do participante
                perspective = self._get_participant_perspective(
                    participant, decision.options, context
                )
                perspectives[participant] = perspective
            
            # Sintetizar perspectivas
            synthesis = self._synthesize_perspectives(perspectives, decision.options)
            
            # Selecionar opção baseada na síntese
            selected = synthesis['best_option']
            confidence = synthesis['confidence']
            
            return {
                'selected_option': selected,
                'confidence': confidence,
                'rationale': f"Síntese colaborativa de {len(perspectives)} perspectivas"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro em decisão colaborativa: {e}")
            return {
                'selected_option': decision.options[0],
                'confidence': 0.5,
                'rationale': f"Erro na colaboração: {str(e)}"
            }
    
    async def _evaluate_options(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Avalia opções disponíveis"""
        try:
            options = data.get('options', [])
            criteria = data.get('criteria', ['benefit', 'cost', 'risk', 'feasibility'])
            
            evaluations = []
            
            for option in options:
                evaluation = {
                    'option_id': option['id'],
                    'name': option.get('name', 'Unknown'),
                    'scores': {}
                }
                
                # Avaliar cada critério
                for criterion in criteria:
                    score = self._evaluate_criterion(option, criterion)
                    evaluation['scores'][criterion] = score
                
                # Calcular score geral
                evaluation['overall_score'] = sum(evaluation['scores'].values()) / len(criteria)
                evaluations.append(evaluation)
            
            # Ordenar por score geral
            evaluations.sort(key=lambda x: x['overall_score'], reverse=True)
            
            return {
                'status': 'completed',
                'evaluations': evaluations,
                'best_option': evaluations[0] if evaluations else None,
                'criteria_used': criteria
            }
            
        except Exception as e:
            logger.error(f"❌ Erro avaliando opções: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _assess_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Avalia riscos de uma decisão ou ação"""
        try:
            action = data.get('action', {})
            context = data.get('context', {})
            
            # Identificar fatores de risco
            risk_factors = []
            
            # Risco técnico
            if action.get('technical_complexity', 0) > 0.7:
                risk_factors.append({
                    'type': 'technical',
                    'level': 'high',
                    'description': 'Alta complexidade técnica',
                    'mitigation': 'Realizar prototipagem e testes extensivos'
                })
            
            # Risco de recursos
            if action.get('resource_requirement', 0) > 0.8:
                risk_factors.append({
                    'type': 'resource',
                    'level': 'medium',
                    'description': 'Alto requisito de recursos',
                    'mitigation': 'Garantir alocação adequada de recursos'
                })
            
            # Risco de tempo
            if action.get('time_constraint', 0) > 0.6:
                risk_factors.append({
                    'type': 'time',
                    'level': 'medium',
                    'description': 'Restrições de tempo apertadas',
                    'mitigation': 'Criar buffer de tempo e plano de contingência'
                })
            
            # Calcular risco geral
            if not risk_factors:
                overall_risk = 'low'
                risk_score = 0.2
            else:
                high_risks = sum(1 for r in risk_factors if r['level'] == 'high')
                medium_risks = sum(1 for r in risk_factors if r['level'] == 'medium')
                
                risk_score = (high_risks * 0.4 + medium_risks * 0.2) / max(1, len(risk_factors))
                
                if risk_score > self.risk_thresholds['high']:
                    overall_risk = 'high'
                elif risk_score > self.risk_thresholds['medium']:
                    overall_risk = 'medium'
                else:
                    overall_risk = 'low'
            
            return {
                'status': 'completed',
                'overall_risk': overall_risk,
                'risk_score': risk_score,
                'risk_factors': risk_factors,
                'recommendation': self._get_risk_recommendation(overall_risk)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro avaliando risco: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _get_decision_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna status de uma decisão"""
        try:
            decision_id = data.get('decision_id')
            
            # Verificar decisões ativas
            if decision_id in self.active_decisions:
                decision = self.active_decisions[decision_id]
                return {
                    'status': 'in_progress',
                    'decision_id': decision_id,
                    'strategy': decision.strategy.value,
                    'started_at': decision.timestamp.isoformat()
                }
            
            # Verificar histórico
            for decision in self.decision_history:
                if decision.decision_id == decision_id:
                    return {
                        'status': 'completed',
                        'decision_id': decision_id,
                        'selected_option': decision.selected_option,
                        'confidence': decision.confidence,
                        'rationale': decision.rationale,
                        'completed_at': decision.timestamp.isoformat()
                    }
            
            return {
                'status': 'not_found',
                'message': f'Decisão {decision_id} não encontrada'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo status: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _simulate_participant_preference(self, participant: str, options: List[Dict], context: Dict) -> Dict:
        """Simula preferência de um participante"""
        # Simulação simples - em produção seria mais complexo
        import random
        return random.choice(options)
    
    def _simulate_hierarchical_choice(self, level: str, options: List[Dict], context: Dict) -> Dict:
        """Simula escolha hierárquica"""
        # Níveis superiores tendem a escolher opções mais conservadoras
        if 'level_1' in level:
            # Escolher opção com menor risco
            return min(options, key=lambda x: x.get('risk', 0.5))
        else:
            # Escolher opção com melhor benefício
            return max(options, key=lambda x: x.get('benefit', 0.5))
    
    def _get_participant_perspective(self, participant: str, options: List[Dict], context: Dict) -> Dict:
        """Obtém perspectiva de um participante"""
        # Simulação de diferentes perspectivas
        perspectives = {
            'technical': lambda opts: max(opts, key=lambda x: x.get('technical_score', 0.5)),
            'business': lambda opts: max(opts, key=lambda x: x.get('benefit', 0.5) - x.get('cost', 0.5)),
            'risk': lambda opts: min(opts, key=lambda x: x.get('risk', 0.5))
        }
        
        # Determinar tipo de perspectiva baseado no agente
        if 'analyzer' in participant:
            perspective_type = 'technical'
        elif 'optimizer' in participant:
            perspective_type = 'business'
        else:
            perspective_type = 'risk'
        
        chosen_option = perspectives[perspective_type](options)
        
        return {
            'preferred_option': chosen_option,
            'perspective_type': perspective_type,
            'confidence': 0.7 + (0.3 * random.random())
        }
    
    def _synthesize_perspectives(self, perspectives: Dict[str, Dict], options: List[Dict]) -> Dict:
        """Sintetiza múltiplas perspectivas"""
        # Contar votos para cada opção
        option_votes = defaultdict(int)
        total_confidence = 0.0
        
        for participant, perspective in perspectives.items():
            preferred = perspective['preferred_option']
            option_id = preferred['id']
            option_votes[option_id] += perspective['confidence']
            total_confidence += perspective['confidence']
        
        # Encontrar opção mais votada
        if option_votes:
            best_option_id = max(option_votes, key=option_votes.get)
            best_option = next(o for o in options if o['id'] == best_option_id)
            confidence = option_votes[best_option_id] / max(1, total_confidence)
        else:
            best_option = options[0]
            confidence = 0.5
        
        return {
            'best_option': best_option,
            'confidence': min(0.95, confidence)
        }
    
    def _evaluate_criterion(self, option: Dict, criterion: str) -> float:
        """Avalia um critério específico de uma opção"""
        # Se o critério existe na opção, usar seu valor
        if criterion in option:
            return float(option[criterion])
        
        # Caso contrário, usar avaliação padrão
        default_scores = {
            'benefit': 0.5,
            'cost': 0.5,
            'risk': 0.5,
            'feasibility': 0.7,
            'impact': 0.6
        }
        
        return default_scores.get(criterion, 0.5)
    
    def _get_risk_recommendation(self, risk_level: str) -> str:
        """Retorna recomendação baseada no nível de risco"""
        recommendations = {
            'low': "Prosseguir com monitoramento padrão",
            'medium': "Implementar medidas de mitigação e monitoramento aumentado",
            'high': "Revisar plano, considerar alternativas ou implementar controles rigorosos"
        }
        
        return recommendations.get(risk_level, "Avaliar cuidadosamente antes de prosseguir")
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
        response = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            priority=original_message.priority,
            content=response_data,
            timestamp=datetime.now(),
            correlation_id=original_message.id
        )
        await self.message_bus.publish(response)

# Importações necessárias
from uuid import uuid4
import random

def create_service_agents(message_bus, num_instances=1) -> List:
    """
    Cria agentes de serviço
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com exatamente 2 agentes de serviço
    """
    agents = []
    
    try:
        logger.info("🔧 Criando agentes de Serviço...")
        
        # Verificar agentes existentes
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        # IDs fixos para os 2 agentes
        agent_configs = [
            ('communication_001', CommunicationAgent),
            ('decision_001', DecisionAgent)
        ]
        
        # Criar agentes
        for agent_id, agent_class in agent_configs:
            if agent_id not in existing_agents:
                try:
                    agent = agent_class(agent_id, AgentType.SERVICE, message_bus)
                    
                    # Iniciar serviço de roteamento para CommunicationAgent
                    if isinstance(agent, CommunicationAgent):
                        asyncio.create_task(agent.start_routing_service())
                    
                    agents.append(agent)
                    logger.info(f"✅ {agent_id} criado com sucesso")
                    logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                    
                except Exception as e:
                    logger.error(f"❌ Erro criando {agent_id}: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
            else:
                logger.warning(f"⚠️ Agente {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agentes de Serviço criados com sucesso")
        
        # Validar quantidade
        if len(agents) != 2:
            logger.warning(f"⚠️ Esperado 2 agentes, criados {len(agents)}")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando agentes de Serviço: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
