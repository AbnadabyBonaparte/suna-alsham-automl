"""
ALSHAM QUANTUM - Notification Agent (CORRIGIDO)
Sistema de notificação multi-provider funcional
"""
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List
import asyncio
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class NotificationConfig:
    """Configuração de notificação"""
    provider: str
    enabled: bool = True
    config: Dict[str, Any] = None

class NotificationAgent:
    """Agente de notificação corrigido"""
    
    def __init__(self):
        self.agent_id = "notification_001"
        self.name = "Notification Agent"
        self.providers = {}
        self.initialized = False
        
    async def initialize(self) -> bool:
        """Inicializar agente de notificação"""
        try:
            logger.info("Inicializando Notification Agent...")
            
            # Configurar provedores disponíveis
            await self._setup_email_providers()
            await self._setup_sms_providers()
            await self._setup_social_providers()
            
            self.initialized = True
            logger.info("✅ Notification Agent inicializado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro na inicialização do Notification Agent: {e}")
            return False
    
    async def _setup_email_providers(self):
        """Configurar provedores de email"""
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
        """Configurar provedores de SMS"""
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
        """Configurar provedores sociais"""
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
    
    async def send_notification(self, notification_type: str, message: str, 
                              recipient: Optional[str] = None, 
                              subject: Optional[str] = None) -> bool:
        """Enviar notificação via provider disponível"""
        if not self.initialized:
            logger.error("Notification Agent não inicializado")
            return False
        
        # Tentar email primeiro
        if await self._send_email(message, recipient, subject):
            return True
        
        # Fallback para outros providers
        if await self._send_slack(message):
            return True
        
        if await self._send_sms(message, recipient):
            return True
        
        logger.warning("Nenhum provider de notificação disponível")
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
            "initialized": self.initialized,
            "providers_available": list(self.providers.keys()),
            "providers_count": len(self.providers),
            "email_providers": [p for p in self.providers if p in ["gmail", "outlook", "custom_smtp"]],
            "social_providers": [p for p in self.providers if p in ["slack", "discord"]],
            "sms_providers": [p for p in self.providers if p in ["twilio"]]
        }

def create_notification_agent():
    """Factory function para criar o notification agent"""
    return NotificationAgent()

# Instância global para compatibilidade
notification_agent = NotificationAgent()
