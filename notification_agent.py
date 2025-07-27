#!/usr/bin/env python3
"""
NotificationAgent - Sistema de Notificações Inteligentes Multi-Canal
Alertas avançados, priorização dinâmica e entrega garantida
"""

import logging
import asyncio
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
import hashlib
import os
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class NotificationChannel(Enum):
    """Canais de notificação disponíveis"""
    EMAIL = "email"
    SLACK = "slack"
    DISCORD = "discord"
    WEBHOOK = "webhook"
    SMS = "sms"
    PUSH = "push_notification"
    CONSOLE = "console"
    FILE = "file_log"
    DATABASE = "database"
    TELEGRAM = "telegram"

class NotificationPriority(Enum):
    """Prioridades de notificação"""
    CRITICAL = 1    # Emergência - entrega imediata
    HIGH = 2        # Urgente - entrega em 1 minuto
    MEDIUM = 3      # Normal - entrega em 5 minutos
    LOW = 4         # Informativo - entrega em 15 minutos
    BACKGROUND = 5  # Background - batch diário

class NotificationStatus(Enum):
    """Status da notificação"""
    PENDING = "pending"
    SENDING = "sending"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRY = "retry"
    EXPIRED = "expired"

class AlertType(Enum):
    """Tipos de alerta"""
    SYSTEM_ERROR = "system_error"
    PERFORMANCE_ISSUE = "performance_issue"
    SECURITY_ALERT = "security_alert"
    OPTIMIZATION_COMPLETE = "optimization_complete"
    AGENT_STATUS = "agent_status"
    RESOURCE_WARNING = "resource_warning"
    USER_ACTION = "user_action"
    MILESTONE = "milestone"
    HEALTH_CHECK = "health_check"
    CUSTOM = "custom"

@dataclass
class NotificationRule:
    """Regra de notificação"""
    rule_id: str
    name: str
    alert_types: List[AlertType]
    channels: List[NotificationChannel]
    priority: NotificationPriority
    conditions: Dict[str, Any]
    recipients: List[str]
    active: bool = True
    cooldown_minutes: int = 0
    max_per_hour: int = 0
    template: Optional[str] = None

@dataclass
class NotificationTemplate:
    """Template de notificação"""
    template_id: str
    name: str
    subject_template: str
    body_template: str
    channel: NotificationChannel
    variables: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Notification:
    """Notificação individual"""
    notification_id: str
    alert_type: AlertType
    priority: NotificationPriority
    title: str
    message: str
    channels: List[NotificationChannel]
    recipients: List[str]
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    scheduled_for: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    status: NotificationStatus = NotificationStatus.PENDING
    attempts: int = 0
    max_attempts: int = 3
    last_attempt: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    error_message: Optional[str] = None

@dataclass
class DeliveryReport:
    """Relatório de entrega"""
    notification_id: str
    channel: NotificationChannel
    recipient: str
    status: NotificationStatus
    delivered_at: Optional[datetime]
    error_message: Optional[str] = None
    response_data: Optional[Dict[str, Any]] = None

class NotificationAgent(BaseNetworkAgent):
    """Agente de notificações inteligentes multi-canal"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'intelligent_notifications',
            'multi_channel_delivery',
            'priority_management',
            'template_engine',
            'delivery_tracking',
            'rule_engine',
            'batch_processing',
            'retry_logic',
            'analytics'
        ]
        self.status = 'active'
        
        # Estado do sistema
        self.notification_queue = asyncio.PriorityQueue()
        self.notification_history = deque(maxlen=10000)
        self.delivery_reports = defaultdict(list)
        self.notification_rules = {}
        self.templates = {}
        self.channel_configs = {}
        
        # Controles de rate limiting
        self.rate_limits = defaultdict(lambda: defaultdict(int))  # channel -> recipient -> count
        self.cooldowns = defaultdict(lambda: defaultdict(datetime))  # rule_id -> recipient -> last_sent
        
        # Configurações
        self.batch_size = 50
        self.processing_interval = 1  # segundo
        self.cleanup_interval = 3600  # 1 hora
        self.max_queue_size = 1000
        
        # Estatísticas
        self.stats = {
            'notifications_sent': 0,
            'notifications_failed': 0,
            'delivery_rate': 0.0,
            'average_delivery_time': 0.0,
            'channels_active': 0,
            'rules_processed': 0
        }
        
        # Tasks de background
        self._processing_task = None
        self._cleanup_task = None
        self._analytics_task = None
        
        # Inicialização
        self._setup_default_templates()
        self._setup_default_rules()
        self._configure_channels()
        
        logger.info(f"🔔 {self.agent_id} inicializado com notificações inteligentes")
    
    def _setup_default_templates(self):
        """Configura templates padrão"""
        # Template para erro do sistema
        self.templates['system_error'] = NotificationTemplate(
            template_id='system_error',
            name='Erro do Sistema',
            subject_template='🚨 ERRO CRÍTICO: {error_type}',
            body_template='''
🚨 ALERTA CRÍTICO DO SISTEMA SUNA-ALSHAM

❌ Erro: {error_type}
📍 Localização: {location}
⏰ Timestamp: {timestamp}
🔍 Detalhes: {details}

🛠️ Ação Recomendada: {recommended_action}

---
Sistema: {system_name}
Agente: {agent_id}
            ''',
            channel=NotificationChannel.EMAIL,
            variables=['error_type', 'location', 'timestamp', 'details', 'recommended_action']
        )
        
        # Template para otimização completa
        self.templates['optimization_complete'] = NotificationTemplate(
            template_id='optimization_complete',
            name='Otimização Completa',
            subject_template='✅ Otimização Concluída: {improvement}% de melhoria',
            body_template='''
✅ OTIMIZAÇÃO SUNA-ALSHAM CONCLUÍDA

📈 Melhoria: {improvement}%
🎯 Arquivo: {file_path}
⚡ Tipo: {optimization_type}
⏱️ Tempo: {execution_time}s

📊 Métricas:
• Performance: {performance_gain}%
• Memória: {memory_improvement}%
• CPU: {cpu_improvement}%

🎉 O sistema está mais eficiente!
            ''',
            channel=NotificationChannel.SLACK,
            variables=['improvement', 'file_path', 'optimization_type', 'execution_time']
        )
        
        # Template para alerta de performance
        self.templates['performance_issue'] = NotificationTemplate(
            template_id='performance_issue',
            name='Problema de Performance',
            subject_template='⚠️ Alerta de Performance: {metric_name}',
            body_template='''
⚠️ ALERTA DE PERFORMANCE

📊 Métrica: {metric_name}
📈 Valor Atual: {current_value}
🎯 Limite: {threshold}
📍 Componente: {component}

🔍 Análise:
{analysis_details}

🛠️ Recomendação:
{recommendation}
            ''',
            channel=NotificationChannel.WEBHOOK,
            variables=['metric_name', 'current_value', 'threshold', 'component']
        )
    
    def _setup_default_rules(self):
        """Configura regras padrão de notificação"""
        # Regra para erros críticos
        self.notification_rules['critical_errors'] = NotificationRule(
            rule_id='critical_errors',
            name='Erros Críticos do Sistema',
            alert_types=[AlertType.SYSTEM_ERROR],
            channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK, NotificationChannel.CONSOLE],
            priority=NotificationPriority.CRITICAL,
            conditions={'severity': 'critical'},
            recipients=['admin@company.com', '#alerts-channel'],
            cooldown_minutes=0,  # Sem cooldown para críticos
            max_per_hour=0  # Sem limite para críticos
        )
        
        # Regra para otimizações
        self.notification_rules['optimizations'] = NotificationRule(
            rule_id='optimizations',
            name='Otimizações Concluídas',
            alert_types=[AlertType.OPTIMIZATION_COMPLETE],
            channels=[NotificationChannel.SLACK, NotificationChannel.CONSOLE],
            priority=NotificationPriority.MEDIUM,
            conditions={'improvement': {'min': 5}},  # Mínimo 5% de melhoria
            recipients=['#development-channel'],
            cooldown_minutes=15,
            max_per_hour=10
        )
        
        # Regra para performance
        self.notification_rules['performance_alerts'] = NotificationRule(
            rule_id='performance_alerts',
            name='Alertas de Performance',
            alert_types=[AlertType.PERFORMANCE_ISSUE],
            channels=[NotificationChannel.WEBHOOK, NotificationChannel.EMAIL],
            priority=NotificationPriority.HIGH,
            conditions={'threshold_exceeded': True},
            recipients=['performance-webhook-url', 'devops@company.com'],
            cooldown_minutes=30,
            max_per_hour=5
        )
        
        # Regra para status de agentes
        self.notification_rules['agent_status'] = NotificationRule(
            rule_id='agent_status',
            name='Status dos Agentes',
            alert_types=[AlertType.AGENT_STATUS],
            channels=[NotificationChannel.CONSOLE, NotificationChannel.FILE],
            priority=NotificationPriority.LOW,
            conditions={},
            recipients=['system.log'],
            cooldown_minutes=60,
            max_per_hour=20
        )
    
    def _configure_channels(self):
        """Configura canais de notificação"""
        self.channel_configs = {
            NotificationChannel.EMAIL: {
                'smtp_server': os.getenv('SMTP_SERVER', 'localhost'),
                'smtp_port': int(os.getenv('SMTP_PORT', '587')),
                'username': os.getenv('SMTP_USERNAME'),
                'password': os.getenv('SMTP_PASSWORD'),
                'from_address': os.getenv('SMTP_FROM', 'noreply@suna-alsham.ai'),
                'use_tls': True
            },
            NotificationChannel.SLACK: {
                'webhook_url': os.getenv('SLACK_WEBHOOK_URL'),
                'bot_token': os.getenv('SLACK_BOT_TOKEN'),
                'default_channel': os.getenv('SLACK_DEFAULT_CHANNEL', '#general')
            },
            NotificationChannel.DISCORD: {
                'webhook_url': os.getenv('DISCORD_WEBHOOK_URL'),
                'bot_token': os.getenv('DISCORD_BOT_TOKEN')
            },
            NotificationChannel.WEBHOOK: {
                'default_url': os.getenv('DEFAULT_WEBHOOK_URL'),
                'timeout': 30,
                'retry_count': 3
            },
            NotificationChannel.TELEGRAM: {
                'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
                'default_chat_id': os.getenv('TELEGRAM_CHAT_ID')
            }
        }
        
        # Contar canais ativos
        self.stats['channels_active'] = sum(
            1 for config in self.channel_configs.values() 
            if any(config.values())
        )
    
    async def start_notification_service(self):
        """Inicia serviço de notificações"""
        if not self._processing_task:
            self._processing_task = asyncio.create_task(self._processing_loop())
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
            self._analytics_task = asyncio.create_task(self._analytics_loop())
            logger.info(f"🔔 {self.agent_id} iniciou serviços de notificação")
    
    async def stop_notification_service(self):
        """Para serviço de notificações"""
        if self._processing_task:
            self._processing_task.cancel()
            self._processing_task = None
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None
        if self._analytics_task:
            self._analytics_task.cancel()
            self._analytics_task = None
        logger.info(f"🛑 {self.agent_id} parou serviços de notificação")
    
    async def _processing_loop(self):
        """Loop principal de processamento"""
        while True:
            try:
                batch = []
                
                # Coletar batch de notificações
                for _ in range(self.batch_size):
                    if not self.notification_queue.empty():
                        priority, notification = await self.notification_queue.get()
                        batch.append(notification)
                    else:
                        break
                
                # Processar batch
                if batch:
                    await self._process_notification_batch(batch)
                
                await asyncio.sleep(self.processing_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de processamento: {e}")
    
    async def _cleanup_loop(self):
        """Loop de limpeza"""
        while True:
            try:
                # Limpar notificações antigas
                cutoff = datetime.now() - timedelta(hours=24)
                
                cleaned = 0
                while (self.notification_history and 
                       self.notification_history[0].created_at < cutoff):
                    self.notification_history.popleft()
                    cleaned += 1
                
                if cleaned > 0:
                    logger.info(f"🧹 Limpeza: {cleaned} notificações antigas removidas")
                
                # Resetar rate limits por hora
                current_hour = datetime.now().hour
                if hasattr(self, '_last_rate_reset') and self._last_rate_reset != current_hour:
                    self.rate_limits.clear()
                self._last_rate_reset = current_hour
                
                await asyncio.sleep(self.cleanup_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no cleanup: {e}")
    
    async def _analytics_loop(self):
        """Loop de análise e métricas"""
        while True:
            try:
                # Calcular métricas
                self._calculate_analytics()
                
                # Gerar relatório se necessário
                if len(self.notification_history) > 100:
                    await self._generate_analytics_report()
                
                await asyncio.sleep(300)  # A cada 5 minutos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no analytics: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'send_notification':
                result = await self.send_notification(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'create_rule':
                result = await self.create_notification_rule(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'get_statistics':
                result = self.get_notification_statistics()
                await self._send_response(message, result)
                
            elif request_type == 'test_channel':
                result = await self.test_notification_channel(message.content)
                await self._send_response(message, result)
        
        elif message.message_type == MessageType.NOTIFICATION:
            # Auto-processar notificações de outros agentes
            await self._auto_process_notification(message.content)
    
    async def send_notification(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Envia notificação"""
        try:
            alert_type = AlertType(request_data.get('alert_type', 'custom'))
            priority = NotificationPriority(request_data.get('priority', 3))
            title = request_data.get('title', 'Notificação SUNA-ALSHAM')
            message = request_data.get('message', '')
            
            # Aplicar regras automáticas
            applicable_rules = self._find_applicable_rules(alert_type, request_data)
            
            if not applicable_rules:
                # Criar notificação manual
                notification = Notification(
                    notification_id=self._generate_notification_id(),
                    alert_type=alert_type,
                    priority=priority,
                    title=title,
                    message=message,
                    channels=request_data.get('channels', [NotificationChannel.CONSOLE]),
                    recipients=request_data.get('recipients', []),
                    data=request_data.get('data', {})
                )
                
                await self._queue_notification(notification)
                
                return {
                    'status': 'queued',
                    'notification_id': notification.notification_id,
                    'channels': len(notification.channels)
                }
            else:
                # Processar regras automaticamente
                notifications_created = []
                
                for rule in applicable_rules:
                    if self._check_rule_conditions(rule, request_data):
                        notification = self._create_notification_from_rule(
                            rule, alert_type, request_data
                        )
                        await self._queue_notification(notification)
                        notifications_created.append(notification.notification_id)
                
                return {
                    'status': 'rules_applied',
                    'notifications_created': notifications_created,
                    'rules_matched': len(applicable_rules)
                }
                
        except Exception as e:
            logger.error(f"❌ Erro enviando notificação: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_notification_id(self) -> str:
        """Gera ID único para notificação"""
        timestamp = datetime.now().isoformat()
        return hashlib.sha256(f"{self.agent_id}_{timestamp}".encode()).hexdigest()[:16]
    
    def _find_applicable_rules(self, alert_type: AlertType, data: Dict[str, Any]) -> List[NotificationRule]:
        """Encontra regras aplicáveis"""
        applicable = []
        
        for rule in self.notification_rules.values():
            if rule.active and alert_type in rule.alert_types:
                applicable.append(rule)
        
        return applicable
    
    def _check_rule_conditions(self, rule: NotificationRule, data: Dict[str, Any]) -> bool:
        """Verifica se as condições da regra são atendidas"""
        if not rule.conditions:
            return True
        
        for condition_key, condition_value in rule.conditions.items():
            data_value = data.get(condition_key)
            
            if isinstance(condition_value, dict):
                # Condições complexas (min, max, etc.)
                if 'min' in condition_value and data_value < condition_value['min']:
                    return False
                if 'max' in condition_value and data_value > condition_value['max']:
                    return False
                if 'equals' in condition_value and data_value != condition_value['equals']:
                    return False
            else:
                # Condição simples
                if data_value != condition_value:
                    return False
        
        return True
    
    def _create_notification_from_rule(self, rule: NotificationRule, 
                                     alert_type: AlertType, data: Dict[str, Any]) -> Notification:
        """Cria notificação baseada em regra"""
        # Aplicar template se existir
        template = self.templates.get(alert_type.value)
        
        if template:
            title = self._apply_template(template.subject_template, data)
            message = self._apply_template(template.body_template, data)
        else:
            title = data.get('title', f'Alerta {alert_type.value}')
            message = data.get('message', str(data))
        
        # Determinar expiração baseada na prioridade
        expires_at = None
        if rule.priority == NotificationPriority.CRITICAL:
            expires_at = datetime.now() + timedelta(hours=1)
        elif rule.priority == NotificationPriority.HIGH:
            expires_at = datetime.now() + timedelta(hours=6)
        else:
            expires_at = datetime.now() + timedelta(days=1)
        
        return Notification(
            notification_id=self._generate_notification_id(),
            alert_type=alert_type,
            priority=rule.priority,
            title=title,
            message=message,
            channels=rule.channels,
            recipients=rule.recipients,
            data=data,
            expires_at=expires_at
        )
    
    def _apply_template(self, template: str, data: Dict[str, Any]) -> str:
        """Aplica template com dados"""
        try:
            # Adicionar dados do sistema
            template_data = {
                'system_name': 'SUNA-ALSHAM',
                'agent_id': self.agent_id,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                **data
            }
            
            return template.format(**template_data)
        except Exception as e:
            logger.error(f"❌ Erro aplicando template: {e}")
            return template
    
    async def _queue_notification(self, notification: Notification):
        """Adiciona notificação à fila"""
        if self.notification_queue.qsize() >= self.max_queue_size:
            logger.warning("⚠️ Fila de notificações cheia, descartando mais antiga")
            await self.notification_queue.get()  # Remove mais antiga
        
        # Prioridade como negativo para PriorityQueue (menor número = maior prioridade)
        priority = notification.priority.value
        await self.notification_queue.put((priority, notification))
        
        logger.info(f"📥 Notificação {notification.notification_id} adicionada à fila (prioridade {priority})")
    
    async def _process_notification_batch(self, batch: List[Notification]):
        """Processa batch de notificações"""
        for notification in batch:
            await self._process_single_notification(notification)
    
    async def _process_single_notification(self, notification: Notification):
        """Processa uma notificação individual"""
        try:
            # Verificar rate limits e cooldowns
            if not self._check_rate_limits(notification):
                logger.info(f"⏸️ Notificação {notification.notification_id} pulada (rate limit)")
                return
            
            # Verificar se expirou
            if notification.expires_at and datetime.now() > notification.expires_at:
                notification.status = NotificationStatus.EXPIRED
                logger.info(f"⏰ Notificação {notification.notification_id} expirou")
                return
            
            notification.status = NotificationStatus.SENDING
            notification.last_attempt = datetime.now()
            notification.attempts += 1
            
            delivery_results = []
            
            # Enviar para cada canal
            for channel in notification.channels:
                for recipient in notification.recipients:
                    try:
                        result = await self._send_to_channel(notification, channel, recipient)
                        delivery_results.append(result)
                        
                        if result.status == NotificationStatus.DELIVERED:
                            self.stats['notifications_sent'] += 1
                        else:
                            self.stats['notifications_failed'] += 1
                            
                    except Exception as e:
                        logger.error(f"❌ Erro enviando para {channel.value}: {e}")
                        delivery_results.append(DeliveryReport(
                            notification_id=notification.notification_id,
                            channel=channel,
                            recipient=recipient,
                            status=NotificationStatus.FAILED,
                            delivered_at=None,
                            error_message=str(e)
                        ))
                        self.stats['notifications_failed'] += 1
            
            # Determinar status final
            successful_deliveries = [r for r in delivery_results if r.status == NotificationStatus.DELIVERED]
            
            if successful_deliveries:
                notification.status = NotificationStatus.DELIVERED
                notification.delivered_at = datetime.now()
                logger.info(f"✅ Notificação {notification.notification_id} entregue com sucesso")
            elif notification.attempts >= notification.max_attempts:
                notification.status = NotificationStatus.FAILED
                logger.error(f"❌ Notificação {notification.notification_id} falhou após {notification.attempts} tentativas")
            else:
                notification.status = NotificationStatus.RETRY
                # Reagendar com delay exponencial
                delay = min(300, 30 * (2 ** (notification.attempts - 1)))  # Máximo 5 minutos
                notification.scheduled_for = datetime.now() + timedelta(seconds=delay)
                await self._queue_notification(notification)
                logger.info(f"🔄 Notificação {notification.notification_id} reagendada em {delay}s")
            
            # Armazenar resultados
            self.delivery_reports[notification.notification_id] = delivery_results
            self.notification_history.append(notification)
            
        except Exception as e:
            logger.error(f"❌ Erro processando notificação: {e}")
            notification.status = NotificationStatus.FAILED
            notification.error_message = str(e)
    
    def _check_rate_limits(self, notification: Notification) -> bool:
        """Verifica rate limits"""
        # Encontrar regra aplicável
        rule = None
        for r in self.notification_rules.values():
            if notification.alert_type in r.alert_types:
                rule = r
                break
        
        if not rule:
            return True
        
        # Verificar cooldown
        if rule.cooldown_minutes > 0:
            for recipient in notification.recipients:
                last_sent = self.cooldowns[rule.rule_id].get(recipient)
                if last_sent:
                    cooldown_expires = last_sent + timedelta(minutes=rule.cooldown_minutes)
                    if datetime.now() < cooldown_expires:
                        return False
        
        # Verificar limite por hora
        if rule.max_per_hour > 0:
            current_hour = datetime.now().hour
            for channel in notification.channels:
                for recipient in notification.recipients:
                    key = f"{channel.value}_{recipient}_{current_hour}"
                    if self.rate_limits[rule.rule_id][key] >= rule.max_per_hour:
                        return False
        
        # Atualizar contadores
        for recipient in notification.recipients:
            self.cooldowns[rule.rule_id][recipient] = datetime.now()
            
            if rule.max_per_hour > 0:
                current_hour = datetime.now().hour
                for channel in notification.channels:
                    key = f"{channel.value}_{recipient}_{current_hour}"
                    self.rate_limits[rule.rule_id][key] += 1
        
        return True
    
    async def _send_to_channel(self, notification: Notification, 
                             channel: NotificationChannel, recipient: str) -> DeliveryReport:
        """Envia notificação para canal específico"""
        start_time = datetime.now()
        
        try:
            if channel == NotificationChannel.EMAIL:
                result = await self._send_email(notification, recipient)
            elif channel == NotificationChannel.SLACK:
                result = await self._send_slack(notification, recipient)
            elif channel == NotificationChannel.DISCORD:
                result = await self._send_discord(notification, recipient)
            elif channel == NotificationChannel.WEBHOOK:
                result = await self._send_webhook(notification, recipient)
            elif channel == NotificationChannel.CONSOLE:
                result = await self._send_console(notification, recipient)
            elif channel == NotificationChannel.FILE:
                result = await self._send_file(notification, recipient)
            elif channel == NotificationChannel.TELEGRAM:
                result = await self._send_telegram(notification, recipient)
            else:
                raise Exception(f"Canal {channel.value} não implementado")
            
            delivery_time = (datetime.now() - start_time).total_seconds()
            
            return DeliveryReport(
                notification_id=notification.notification_id,
                channel=channel,
                recipient=recipient,
                status=NotificationStatus.DELIVERED if result else NotificationStatus.FAILED,
                delivered_at=datetime.now() if result else None,
                response_data={'delivery_time_seconds': delivery_time}
            )
            
        except Exception as e:
            return DeliveryReport(
                notification_id=notification.notification_id,
                channel=channel,
                recipient=recipient,
                status=NotificationStatus.FAILED,
                delivered_at=None,
                error_message=str(e)
            )
    
    async def _send_email(self, notification: Notification, recipient: str) -> bool:
        """Envia email"""
        try:
            config = self.channel_configs[NotificationChannel.EMAIL]
            
            if not config.get('username') or not config.get('password'):
                # Simular envio se não configurado
                await asyncio.sleep(0.1)
                logger.info(f"📧 Email simulado para {recipient}: {notification.title}")
                return True
            
            # Implementação real de email
            msg = MIMEMultipart()
            msg['From'] = config['from_address']
            msg['To'] = recipient
            msg['Subject'] = notification.title
            
            msg.attach(MIMEText(notification.message, 'plain'))
            
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            if config['use_tls']:
                server.starttls()
            server.login(config['username'], config['password'])
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro enviando email: {e}")
            return False
    
    async def _send_slack(self, notification: Notification, recipient: str) -> bool:
        """Envia para Slack"""
        try:
            config = self.channel_configs[NotificationChannel.SLACK]
            webhook_url = config.get('webhook_url')
            
            if not webhook_url:
                # Simular envio
                await asyncio.sleep(0.1)
                logger.info(f"💬 Slack simulado para {recipient}: {notification.title}")
                return True
            
            # Formatar mensagem para Slack
            slack_data = {
                'channel': recipient if recipient.startswith('#') else config['default_channel'],
                'username': 'SUNA-ALSHAM',
                'icon_emoji': self._get_priority_emoji(notification.priority),
                'attachments': [{
                    'color': self._get_priority_color(notification.priority),
                    'title': notification.title,
                    'text': notification.message,
                    'footer': f"SUNA-ALSHAM • {notification.alert_type.value}",
                    'ts': int(notification.created_at.timestamp())
                }]
            }
            
            async with requests.Session() as session:
                response = requests.post(webhook_url, json=slack_data, timeout=10)
                return response.status_code == 200
                
        except Exception as e:
            logger.error(f"❌ Erro enviando Slack: {e}")
            return False
    
    async def _send_webhook(self, notification: Notification, recipient: str) -> bool:
        """Envia para webhook"""
        try:
            webhook_data = {
                'notification_id': notification.notification_id,
                'alert_type': notification.alert_type.value,
                'priority': notification.priority.value,
                'title': notification.title,
                'message': notification.message,
                'timestamp': notification.created_at.isoformat(),
                'data': notification.data
            }
            
            async with requests.Session() as session:
                response = requests.post(
                    recipient, 
                    json=webhook_data, 
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                return response.status_code < 400
                
        except Exception as e:
            logger.error(f"❌ Erro enviando webhook: {e}")
            return False
    
    async def _send_console(self, notification: Notification, recipient: str) -> bool:
        """Envia para console"""
        try:
            emoji = self._get_priority_emoji(notification.priority)
            priority_name = notification.priority.name
            
            console_message = f"""
{emoji} [{priority_name}] {notification.title}
📍 {notification.alert_type.value} • {notification.created_at.strftime('%H:%M:%S')}
💬 {notification.message}
{'─' * 60}
"""
            print(console_message)
            logger.info(f"🖥️ Console: {notification.title}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro enviando console: {e}")
            return False
    
    async def _send_file(self, notification: Notification, recipient: str) -> bool:
        """Envia para arquivo de log"""
        try:
            log_entry = {
                'timestamp': notification.created_at.isoformat(),
                'notification_id': notification.notification_id,
                'alert_type': notification.alert_type.value,
                'priority': notification.priority.value,
                'title': notification.title,
                'message': notification.message,
                'data': notification.data
            }
            
            with open(recipient, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro enviando para arquivo: {e}")
            return False
    
    async def _send_discord(self, notification: Notification, recipient: str) -> bool:
        """Envia para Discord (simulado)"""
        await asyncio.sleep(0.1)
        logger.info(f"🎮 Discord simulado para {recipient}: {notification.title}")
        return True
    
    async def _send_telegram(self, notification: Notification, recipient: str) -> bool:
        """Envia para Telegram (simulado)"""
        await asyncio.sleep(0.1)
        logger.info(f"📱 Telegram simulado para {recipient}: {notification.title}")
        return True
    
    def _get_priority_emoji(self, priority: NotificationPriority) -> str:
        """Retorna emoji baseado na prioridade"""
        emoji_map = {
            NotificationPriority.CRITICAL: '🚨',
            NotificationPriority.HIGH: '⚠️',
            NotificationPriority.MEDIUM: 'ℹ️',
            NotificationPriority.LOW: '📝',
            NotificationPriority.BACKGROUND: '🔍'
        }
        return emoji_map.get(priority, 'ℹ️')
    
    def _get_priority_color(self, priority: NotificationPriority) -> str:
        """Retorna cor baseada na prioridade"""
        color_map = {
            NotificationPriority.CRITICAL: 'danger',
            NotificationPriority.HIGH: 'warning',
            NotificationPriority.MEDIUM: 'good',
            NotificationPriority.LOW: '#36a64f',
            NotificationPriority.BACKGROUND: '#cccccc'
        }
        return color_map.get(priority, 'good')
    
    async def create_notification_rule(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria nova regra de notificação"""
        try:
            rule = NotificationRule(
                rule_id=request_data['rule_id'],
                name=request_data['name'],
                alert_types=[AlertType(t) for t in request_data['alert_types']],
                channels=[NotificationChannel(c) for c in request_data['channels']],
                priority=NotificationPriority(request_data['priority']),
                conditions=request_data.get('conditions', {}),
                recipients=request_data['recipients'],
                cooldown_minutes=request_data.get('cooldown_minutes', 0),
                max_per_hour=request_data.get('max_per_hour', 0)
            )
            
            self.notification_rules[rule.rule_id] = rule
            logger.info(f"📋 Regra {rule.rule_id} criada com sucesso")
            
            return {
                'status': 'created',
                'rule_id': rule.rule_id,
                'alert_types': len(rule.alert_types),
                'channels': len(rule.channels)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro criando regra: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_notification_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas das notificações"""
        # Calcular estatísticas atualizadas
        self._calculate_analytics()
        
        return {
            'status': 'active',
            'statistics': self.stats,
            'queue_size': self.notification_queue.qsize(),
            'history_size': len(self.notification_history),
            'active_rules': len([r for r in self.notification_rules.values() if r.active]),
            'total_rules': len(self.notification_rules),
            'available_channels': len(self.channel_configs),
            'recent_activity': self._get_recent_activity()
        }
    
    def _get_recent_activity(self) -> Dict[str, Any]:
        """Retorna atividade recente"""
        now = datetime.now()
        last_hour = now - timedelta(hours=1)
        
        recent = [n for n in self.notification_history if n.created_at >= last_hour]
        
        return {
            'last_hour': len(recent),
            'by_priority': {
                p.name: len([n for n in recent if n.priority == p]) 
                for p in NotificationPriority
            },
            'by_status': {
                s.name: len([n for n in recent if n.status == s])
                for s in NotificationStatus
            }
        }
    
    def _calculate_analytics(self):
        """Calcula analytics das notificações"""
        if not self.notification_history:
            return
        
        # Taxa de entrega
        delivered = len([n for n in self.notification_history if n.status == NotificationStatus.DELIVERED])
        total = len(self.notification_history)
        self.stats['delivery_rate'] = (delivered / total) * 100 if total > 0 else 0
        
        # Tempo médio de entrega
        delivery_times = []
        for notification in self.notification_history:
            if notification.delivered_at and notification.created_at:
                delivery_time = (notification.delivered_at - notification.created_at).total_seconds()
                delivery_times.append(delivery_time)
        
        self.stats['average_delivery_time'] = (
            sum(delivery_times) / len(delivery_times) if delivery_times else 0
        )
    
    async def _generate_analytics_report(self):
        """Gera relatório de analytics"""
        report = {
            'period': '24h',
            'total_notifications': len(self.notification_history),
            'delivery_rate': self.stats['delivery_rate'],
            'average_delivery_time': self.stats['average_delivery_time'],
            'top_alert_types': self._get_top_alert_types(),
            'channel_performance': self._get_channel_performance(),
            'failure_analysis': self._get_failure_analysis()
        }
        
        # Enviar relatório para administradores
        await self.send_notification({
            'alert_type': 'custom',
            'title': '📊 Relatório de Notificações - 24h',
            'message': f"Taxa de entrega: {report['delivery_rate']:.1f}%\nTempo médio: {report['average_delivery_time']:.1f}s",
            'channels': ['console'],
            'recipients': ['admin'],
            'data': report
        })
    
    def _get_top_alert_types(self) -> List[Dict[str, Any]]:
        """Retorna tipos de alerta mais frequentes"""
        type_counts = defaultdict(int)
        for notification in self.notification_history:
            type_counts[notification.alert_type.value] += 1
        
        return [
            {'type': alert_type, 'count': count}
            for alert_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
    
    def _get_channel_performance(self) -> Dict[str, Dict[str, Any]]:
        """Retorna performance por canal"""
        channel_stats = defaultdict(lambda: {'sent': 0, 'delivered': 0, 'failed': 0})
        
        for reports in self.delivery_reports.values():
            for report in reports:
                channel = report.channel.value
                channel_stats[channel]['sent'] += 1
                
                if report.status == NotificationStatus.DELIVERED:
                    channel_stats[channel]['delivered'] += 1
                else:
                    channel_stats[channel]['failed'] += 1
        
        # Calcular taxa de sucesso
        result = {}
        for channel, stats in channel_stats.items():
            total = stats['sent']
            success_rate = (stats['delivered'] / total * 100) if total > 0 else 0
            result[channel] = {
                **stats,
                'success_rate': success_rate
            }
        
        return result
    
    def _get_failure_analysis(self) -> Dict[str, Any]:
        """Analisa falhas de entrega"""
        total_failures = 0
        error_types = defaultdict(int)
        
        for reports in self.delivery_reports.values():
            for report in reports:
                if report.status == NotificationStatus.FAILED:
                    total_failures += 1
                    if report.error_message:
                        # Categorizar erros
                        if 'timeout' in report.error_message.lower():
                            error_types['timeout'] += 1
                        elif 'connection' in report.error_message.lower():
                            error_types['connection'] += 1
                        elif 'auth' in report.error_message.lower():
                            error_types['authentication'] += 1
                        else:
                            error_types['other'] += 1
        
        return {
            'total_failures': total_failures,
            'error_categories': dict(error_types),
            'most_common_error': max(error_types.items(), key=lambda x: x[1])[0] if error_types else None
        }
    
    async def test_notification_channel(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Testa canal de notificação"""
        try:
            channel = NotificationChannel(request_data['channel'])
            recipient = request_data['recipient']
            
            # Criar notificação de teste
            test_notification = Notification(
                notification_id=f"test_{self._generate_notification_id()}",
                alert_type=AlertType.CUSTOM,
                priority=NotificationPriority.LOW,
                title="🧪 Teste de Notificação SUNA-ALSHAM",
                message="Esta é uma notificação de teste para verificar a configuração do canal.",
                channels=[channel],
                recipients=[recipient],
                data={'test': True}
            )
            
            # Enviar teste
            result = await self._send_to_channel(test_notification, channel, recipient)
            
            return {
                'status': 'completed',
                'channel': channel.value,
                'recipient': recipient,
                'test_successful': result.status == NotificationStatus.DELIVERED,
                'delivery_time': result.response_data.get('delivery_time_seconds') if result.response_data else None,
                'error_message': result.error_message
            }
            
        except Exception as e:
            logger.error(f"❌ Erro testando canal: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _auto_process_notification(self, notification_content: Dict[str, Any]):
        """Processa automaticamente notificações de outros agentes"""
        try:
            notification_type = notification_content.get('notification_type')
            
            # Mapear tipos de notificação
            alert_type_map = {
                'critical_code_issues': AlertType.SYSTEM_ERROR,
                'performance_alert': AlertType.PERFORMANCE_ISSUE,
                'security_alert': AlertType.SECURITY_ALERT,
                'optimization_complete': AlertType.OPTIMIZATION_COMPLETE,
                'system_insight': AlertType.SYSTEM_ERROR,
                'recovery_completed': AlertType.SYSTEM_ERROR
            }
            
            alert_type = alert_type_map.get(notification_type, AlertType.CUSTOM)
            
            # Determinar prioridade
            priority = NotificationPriority.MEDIUM
            if 'critical' in str(notification_content).lower():
                priority = NotificationPriority.CRITICAL
            elif 'high' in str(notification_content).lower():
                priority = NotificationPriority.HIGH
            
            # Criar e enviar notificação
            await self.send_notification({
                'alert_type': alert_type.value,
                'priority': priority.value,
                'title': f"🤖 {notification_type.replace('_', ' ').title()}",
                'message': str(notification_content),
                'data': notification_content
            })
            
        except Exception as e:
            logger.error(f"❌ Erro processando auto-notificação: {e}")
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
        from uuid import uuid4
        
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

def create_notification_agent(message_bus, num_instances=1) -> List[NotificationAgent]:
    """
    Cria agente de notificações inteligentes
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de notificações
    """
    agents = []
    
    try:
        logger.info("🔔 Criando NotificationAgent para alertas inteligentes...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "notification_001"
        
        if agent_id not in existing_agents:
            try:
                agent = NotificationAgent(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar serviços de notificação
                asyncio.create_task(agent.start_notification_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com notificações multi-canal")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                logger.info(f"   📋 Regras ativas: {len(agent.notification_rules)}")
                logger.info(f"   📊 Canais configurados: {agent.stats['channels_active']}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de notificações criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando NotificationAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
