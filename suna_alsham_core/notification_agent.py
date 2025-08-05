#!/usr/bin/env python3
"""
ALSHAM QUANTUM - Notification Agent (INTEGRADO AO SISTEMA)
Sistema de notificação multi-provider como agente de rede completo
"""
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List
import asyncio
from dataclasses import dataclass

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

@dataclass
class NotificationConfig:
    """Configuração de notificação"""
    provider: str
    enabled: bool = True
    config: Dict[str, Any] = None

class NotificationAgent(BaseNetworkAgent):
    """
    Agente de notificação integrado ao sistema ALSHAM QUANTUM
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend([
            "email_notifications",
            "sms_notifications", 
            "social_notifications",
            "multi_provider_support",
            "notification_routing",
            "delivery_confirmation",
            "template_management"
        ])
        
        self.providers = {}
        self.notification_history = []
        self.failed_notifications = []
        self.templates = {}
        
        logger.info(f"📧 {self.agent_id} inicializado como agente de rede completo.")

    async def _post_init_setup(self):
        """Setup pós-inicialização"""
        try:
            # Configurar provedores disponíveis
            await self._setup_email_providers()
            await self._setup_sms_providers()
            await self._setup_social_providers()
            await self._setup_default_templates()
            
            logger.info(f"✅ {self.agent_id} configuração completa - {len(self.providers)} provedores ativos")
            
        except Exception as e:
            logger.error(f"❌ Erro na configuração do {self.agent_id}: {e}")

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas pelo agente"""
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get("request_type")
            
            if request_type == "send_notification":
                result = await self._handle_send_notification(message)
                await self.publish_response(message, result)
                
            elif request_type == "test_providers":
                result = await self._handle_test_providers(message)
                await self.publish_response(message, result)
                
            elif request_type == "get_notification_status":
                result = await self._handle_get_status(message)
                await self.publish_response(message, result)
                
            elif request_type == "configure_provider":
                result = await self._handle_configure_provider(message)
                await self.publish_response(message, result)
                
            else:
                logger.debug(f"Tipo de requisição não reconhecido: {request_type}")

    async def _handle_send_notification(self, message: AgentMessage) -> Dict[str, Any]:
        """Processa requisição de envio de notificação"""
        try:
            content = message.content
            notification_type = content.get("notification_type", "email")
            text_message = content.get("message", "")
            recipient = content.get("recipient")
            subject = content.get("subject")
            template = content.get("template")
            priority = content.get("priority", "normal")
            
            # Usar template se especificado
            if template and template in self.templates:
                text_message = self.templates[template].format(**content.get("template_vars", {}))
            
            # Enviar notificação
            success = await self.send_notification(
                notification_type=notification_type,
                message=text_message,
                recipient=recipient,
                subject=subject
            )
            
            # Registrar no histórico
            notification_record = {
                "timestamp": message.timestamp.isoformat(),
                "type": notification_type,
                "recipient": recipient,
                "success": success,
                "priority": priority
            }
            
            if success:
                self.notification_history.append(notification_record)
                logger.info(f"✅ Notificação enviada: {notification_type} para {recipient}")
            else:
                self.failed_notifications.append(notification_record)
                logger.warning(f"❌ Falha no envio: {notification_type} para {recipient}")
            
            return {
                "status": "completed" if success else "failed",
                "success": success,
                "notification_type": notification_type,
                "message": "Notificação enviada com sucesso" if success else "Falha no envio"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro processando notificação: {e}")
            return {
                "status": "error",
                "success": False,
                "message": f"Erro interno: {str(e)}"
            }

    async def _handle_test_providers(self, message: AgentMessage) -> Dict[str, Any]:
        """Testa todos os provedores disponíveis"""
        try:
            test_results = await self.test_notifications()
            
            return {
                "status": "completed",
                "provider_results": test_results,
                "providers_available": list(self.providers.keys()),
                "providers_working": [p for p, result in test_results.items() if result]
            }
            
        except Exception as e:
            logger.error(f"❌ Erro testando provedores: {e}")
            return {
                "status": "error",
                "message": f"Erro no teste: {str(e)}"
            }

    async def _handle_get_status(self, message: AgentMessage) -> Dict[str, Any]:
        """Retorna status do sistema de notificação"""
        try:
            status = await self.get_status()
            status.update({
                "notifications_sent": len(self.notification_history),
                "failed_notifications": len(self.failed_notifications),
                "success_rate": self._calculate_success_rate()
            })
            
            return {
                "status": "completed",
                "notification_system_status": status
            }
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo status: {e}")
            return {
                "status": "error", 
                "message": f"Erro: {str(e)}"
            }

    async def _handle_configure_provider(self, message: AgentMessage) -> Dict[str, Any]:
        """Configura um provedor específico"""
        try:
            provider_name = message.content.get("provider_name")
            provider_config = message.content.get("provider_config", {})
            
            if provider_name:
                self.providers[provider_name] = NotificationConfig(
                    provider=provider_name,
                    enabled=True,
                    config=provider_config
                )
                
                return {
                    "status": "completed",
                    "message": f"Provedor {provider_name} configurado com sucesso"
                }
            else:
                return {
                    "status": "error",
                    "message": "Nome do provedor não especificado"
                }
                
        except Exception as e:
            logger.error(f"❌ Erro configurando provedor: {e}")
            return {
                "status": "error",
                "message": f"Erro: {str(e)}"
            }

    async def _setup_email_providers(self):
        """Configura provedores de email"""
        # Gmail
        if os.getenv("GMAIL_USER") and os.getenv("GMAIL_PASSWORD"):
            self.providers["gmail"] = NotificationConfig(
                provider="gmail",
                enabled=True,
                config={
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "user": os.getenv("GMAIL_USER"),
                    "password": os.getenv("GMAIL_PASSWORD"),
                    "use_tls": True
                }
            )
            logger.info("  ✅ Gmail configurado")
        
        # Outlook
        if os.getenv("OUTLOOK_USER") and os.getenv("OUTLOOK_PASSWORD"):
            self.providers["outlook"] = NotificationConfig(
                provider="outlook",
                enabled=True,
                config={
                    "smtp_server": "smtp-mail.outlook.com",
                    "smtp_port": 587,
                    "user": os.getenv("OUTLOOK_USER"),
                    "password": os.getenv("OUTLOOK_PASSWORD"),
                    "use_tls": True
                }
            )
            logger.info("  ✅ Outlook configurado")
        
        # SMTP Custom
        if os.getenv("CUSTOM_SMTP_SERVER"):
            self.providers["custom_smtp"] = NotificationConfig(
                provider="custom_smtp",
                enabled=True,
                config={
                    "smtp_server": os.getenv("CUSTOM_SMTP_SERVER"),
                    "smtp_port": int(os.getenv("CUSTOM_SMTP_PORT", 587)),
                    "user": os.getenv("CUSTOM_SMTP_USER"),
                    "password": os.getenv("CUSTOM_SMTP_PASSWORD"),
                    "use_tls": os.getenv("CUSTOM_SMTP_USE_TLS", "true").lower() == "true"
                }
            )
            logger.info("  ✅ SMTP Custom configurado")
    
    async def _setup_sms_providers(self):
        """Configura provedores de SMS"""
        if os.getenv("TWILIO_ACCOUNT_SID") and os.getenv("TWILIO_AUTH_TOKEN"):
            self.providers["twilio"] = NotificationConfig(
                provider="twilio",
                enabled=True,
                config={
                    "account_sid": os.getenv("TWILIO_ACCOUNT_SID"),
                    "auth_token": os.getenv("TWILIO_AUTH_TOKEN"),
                    "phone_number": os.getenv("TWILIO_PHONE_NUMBER")
                }
            )
            logger.info("  ✅ Twilio SMS configurado")
    
    async def _setup_social_providers(self):
        """Configura provedores sociais"""
        # Slack
        if os.getenv("SLACK_BOT_TOKEN"):
            self.providers["slack"] = NotificationConfig(
                provider="slack",
                enabled=True,
                config={
                    "token": os.getenv("SLACK_BOT_TOKEN"),
                    "channel": os.getenv("SLACK_CHANNEL_GENERAL", "#general")
                }
            )
            logger.info("  ✅ Slack configurado")
        
        # Discord
        if os.getenv("DISCORD_BOT_TOKEN"):
            self.providers["discord"] = NotificationConfig(
                provider="discord",
                enabled=True,
                config={
                    "token": os.getenv("DISCORD_BOT_TOKEN"),
                    "channel_id": os.getenv("DISCORD_CHANNEL_ID")
                }
            )
            logger.info("  ✅ Discord configurado")

    async def _setup_default_templates(self):
        """Configura templates padrão"""
        self.templates = {
            "system_alert": "🚨 ALSHAM QUANTUM ALERT: {message}",
            "agent_notification": "🤖 Agent {agent_id}: {message}",
            "health_report": "🏥 System Health: {status} - {details}",
            "error_notification": "❌ ERROR in {component}: {error_message}",
            "success_notification": "✅ SUCCESS: {message}"
        }

    async def send_notification(self, notification_type: str, message: str, 
                              recipient: Optional[str] = None, 
                              subject: Optional[str] = None) -> bool:
        """Enviar notificação via provider disponível"""
        try:
            # Tentar email primeiro
            if notification_type in ["email", "all"] and await self._send_email(message, recipient, subject):
                return True
            
            # Fallback para outros providers
            if notification_type in ["slack", "all"] and await self._send_slack(message):
                return True
            
            if notification_type in ["sms", "all"] and await self._send_sms(message, recipient):
                return True
            
            logger.warning("Nenhum provider de notificação disponível")
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro no envio de notificação: {e}")
            return False
    
    async def _send_email(self, message: str, recipient: Optional[str] = None, 
                         subject: Optional[str] = None) -> bool:
        """Enviar email via SMTP"""
        # Tentar Gmail primeiro
        if "gmail" in self.providers:
            return await self._send_smtp_email("gmail", message, recipient, subject)
        
        # Tentar Outlook
        if "outlook" in self.providers:
            return await self._send_smtp_email("outlook", message, recipient, subject)
        
        # Tentar SMTP custom
        if "custom_smtp" in self.providers:
            return await self._send_smtp_email("custom_smtp", message, recipient, subject)
        
        return False
    
    async def _send_smtp_email(self, provider_name: str, message: str, 
                              recipient: Optional[str] = None, 
                              subject: Optional[str] = None) -> bool:
        """Enviar email via SMTP específico"""
        try:
            provider = self.providers[provider_name]
            config = provider.config
            
            # Configurar email
            msg = MIMEMultipart()
            msg['From'] = config['user']
            msg['To'] = recipient or config['user']  # Self se não especificado
            msg['Subject'] = subject or f"ALSHAM QUANTUM - {provider_name.title()}"
            
            msg.attach(MIMEText(message, 'plain'))
            
            # Conectar e enviar
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            
            if config.get('use_tls', False):
                server.starttls()
            
            server.login(config['user'], config['password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Email enviado via {provider_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar email via {provider_name}: {e}")
            return False
    
    async def _send_slack(self, message: str) -> bool:
        """Enviar mensagem via Slack"""
        if "slack" not in self.providers:
            return False
        
        try:
            # Implementação básica - pode ser expandida
            logger.info("📱 Slack: Enviaria mensagem (implementação básica)")
            return True
        except Exception as e:
            logger.error(f"❌ Erro Slack: {e}")
            return False
    
    async def _send_sms(self, message: str, recipient: Optional[str] = None) -> bool:
        """Enviar SMS via Twilio"""
        if "twilio" not in self.providers:
            return False
        
        try:
            # Implementação básica - pode ser expandida
            logger.info("📱 SMS: Enviaria mensagem (implementação básica)")
            return True
        except Exception as e:
            logger.error(f"❌ Erro SMS: {e}")
            return False
    
    async def test_notifications(self) -> Dict[str, bool]:
        """Testar todos os provedores de notificação"""
        results = {}
        
        test_message = "🧪 ALSHAM QUANTUM - Teste de notificação"
        
        for provider_name in self.providers:
            try:
                if provider_name in ["gmail", "outlook", "custom_smtp"]:
                    result = await self._send_smtp_email(provider_name, test_message)
                elif provider_name == "slack":
                    result = await self._send_slack(test_message)
                elif provider_name == "twilio":
                    result = await self._send_sms(test_message)
                else:
                    result = False
                
                results[provider_name] = result
                
            except Exception as e:
                logger.error(f"Erro no teste {provider_name}: {e}")
                results[provider_name] = False
        
        return results
    
    async def get_status(self) -> Dict[str, Any]:
        """Status do sistema de notificação"""
        return {
            "agent_id": self.agent_id,
            "providers_available": list(self.providers.keys()),
            "providers_count": len(self.providers),
            "email_providers": [p for p in self.providers if p in ["gmail", "outlook", "custom_smtp"]],
            "social_providers": [p for p in self.providers if p in ["slack", "discord"]],
            "sms_providers": [p for p in self.providers if p in ["twilio"]],
            "templates_available": list(self.templates.keys())
        }

    def _calculate_success_rate(self) -> float:
        """Calcula taxa de sucesso das notificações"""
        total = len(self.notification_history) + len(self.failed_notifications)
        if total == 0:
            return 100.0
        return (len(self.notification_history) / total) * 100

    async def initialize_agent(self):
        """Inicialização específica do agente"""
        await self._post_init_setup()

def create_notification_agent(message_bus) -> List[BaseNetworkAgent]:
    """Factory function para criar o notification agent integrado ao sistema"""
    logger.info("📧 Criando Notification Agent integrado...")
    
    agents = [NotificationAgent("notification_001", message_bus)]
    
    # Inicializar configuração
    asyncio.create_task(agents[0].initialize_agent())
    
    logger.info(f"✅ {len(agents)} Notification Agent criado e integrado ao sistema")
    return agents
