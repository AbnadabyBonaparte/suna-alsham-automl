#!/usr/bin/env python3
"""
Quantum Notification Agent - ALSHAM QUANTUM

[Quantum Version 2.0] - Sistema de notificação quântico com múltiplos 
provedores, auto-cura e confiabilidade absoluta.
"""

import asyncio
import logging
import os
import smtplib
import time
from dataclasses import dataclass, field
from datetime import datetime
from email.message import EmailMessage
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from suna_alsham_core.multi_agent_network import (
    AgentMessage,
    AgentType,
    BaseNetworkAgent,
    MessageType,
    Priority,
)

logger = logging.getLogger(__name__)

class NotificationProvider(Enum):
    """Provedores de notificação suportados."""
    GMAIL = "gmail"
    OUTLOOK = "outlook"
    SMTP_CUSTOM = "smtp_custom"

class NotificationStatus(Enum):
    """Status de entrega de notificação."""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class NotificationConfig:
    """Configuração de provedor de notificação."""
    provider: NotificationProvider
    smtp_host: str
    smtp_port: int
    use_tls: bool = True
    username: Optional[str] = None
    password: Optional[str] = None
    from_email: Optional[str] = None

@dataclass
class NotificationJob:
    """Job de notificação com retry automático."""
    job_id: str
    recipient_email: str
    subject: str
    body: str
    status: NotificationStatus = NotificationStatus.PENDING
    attempts: int = 0
    max_attempts: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None

class QuantumNotificationAgent(BaseNetworkAgent):
    """
    Agente de Notificação Quântico - Confiabilidade absoluta através de:
    - Múltiplos provedores de email (Gmail, Outlook, SMTP customizado)
    - Sistema de retry inteligente
    - Auto-cura em caso de falhas
    - Logs detalhados para auditoria completa
    - Validação prévia de credenciais
    """
    
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.SERVICE, message_bus)
        self.capabilities.extend([
            "quantum_email_delivery",
            "multi_provider_support",
            "auto_healing",
            "intelligent_retry",
            "delivery_confirmation"
        ])
        
        self.notification_queue = asyncio.Queue()
        self.providers: List[NotificationConfig] = []
        self.active_provider_index = 0
        self.delivery_stats = {
            "total_sent": 0,
            "total_failed": 0,
            "total_retries": 0,
            "uptime_start": datetime.now()
        }
        
        # Inicialização quântica
        self._initialize_quantum_providers()
        self._quantum_validation_task = asyncio.create_task(self._validate_providers())
        self._quantum_delivery_task = asyncio.create_task(self._quantum_delivery_loop())
        
        logger.info(f"📧 {self.agent_id} (Quantum Notification) inicializado com {len(self.providers)} provedores.")

    def _initialize_quantum_providers(self):
        """Inicializa múltiplos provedores para redundância quântica."""
        
        # Provider 1: Gmail
        gmail_user = os.environ.get('GMAIL_USER')
        gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
        if gmail_user and gmail_password:
            self.providers.append(NotificationConfig(
                provider=NotificationProvider.GMAIL,
                smtp_host="smtp.gmail.com",
                smtp_port=587,
                use_tls=True,
                username=gmail_user,
                password=gmail_password,
                from_email=gmail_user
            ))
            logger.info("✅ Provedor Gmail configurado.")
        
        # Provider 2: Outlook
        outlook_user = os.environ.get('OUTLOOK_USER')
        outlook_password = os.environ.get('OUTLOOK_PASSWORD')
        if outlook_user and outlook_password:
            self.providers.append(NotificationConfig(
                provider=NotificationProvider.OUTLOOK,
                smtp_host="smtp-mail.outlook.com",
                smtp_port=587,
                use_tls=True,
                username=outlook_user,
                password=outlook_password,
                from_email=outlook_user
            ))
            logger.info("✅ Provedor Outlook configurado.")
        
        # Provider 3: SMTP Customizado
        smtp_host = os.environ.get('SMTP_HOST')
        smtp_port = os.environ.get('SMTP_PORT', '587')
        smtp_user = os.environ.get('SMTP_USER')
        smtp_password = os.environ.get('SMTP_PASSWORD')
        smtp_from = os.environ.get('SMTP_FROM_EMAIL')
        
        if smtp_host and smtp_user and smtp_password:
            self.providers.append(NotificationConfig(
                provider=NotificationProvider.SMTP_CUSTOM,
                smtp_host=smtp_host,
                smtp_port=int(smtp_port),
                use_tls=os.environ.get('SMTP_TLS', 'true').lower() == 'true',
                username=smtp_user,
                password=smtp_password,
                from_email=smtp_from or smtp_user
            ))
            logger.info("✅ Provedor SMTP customizado configurado.")
        
        # Status final
        if not self.providers:
            self.status = "degraded"
            logger.critical("❌ NENHUM provedor de email configurado! Configure ao menos um:")
            logger.critical("   Gmail: GMAIL_USER, GMAIL_APP_PASSWORD")
            logger.critical("   Outlook: OUTLOOK_USER, OUTLOOK_PASSWORD")
            logger.critical("   Custom: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD")
        else:
            logger.info(f"🚀 {len(self.providers)} provedores de email configurados para redundância quântica.")

    async def _validate_providers(self):
        """Valida todos os provedores assincronamente."""
        if not self.providers:
            return
            
        logger.info("🔍 Validando provedores de email...")
        valid_providers = []
        
        for i, provider in enumerate(self.providers):
            try:
                # Teste de conexão rápida
                if await self._test_provider_connection(provider):
                    valid_providers.append(provider)
                    logger.info(f"✅ Provedor {provider.provider.value} validado com sucesso.")
                else:
                    logger.warning(f"⚠️ Provedor {provider.provider.value} falhou na validação.")
            except Exception as e:
                logger.error(f"❌ Erro validando provedor {provider.provider.value}: {e}")
        
        if valid_providers:
            self.providers = valid_providers
            self.status = "active"
            logger.info(f"✅ {len(valid_providers)} provedores válidos. Sistema ativo.")
        else:
            self.status = "degraded"
            logger.critical("❌ NENHUM provedor válido! Sistema em modo degradado.")

    async def _test_provider_connection(self, provider: NotificationConfig) -> bool:
        """Testa conexão com um provedor específico."""
        try:
            loop = asyncio.get_running_loop()
            
            def _sync_test():
                server = smtplib.SMTP(provider.smtp_host, provider.smtp_port, timeout=10)
                if provider.use_tls:
                    server.starttls()
                server.login(provider.username, provider.password)
                server.quit()
                return True
            
            return await loop.run_in_executor(None, _sync_test)
        except Exception as e:
            logger.debug(f"Teste de conexão falhou para {provider.provider.value}: {e}")
            return False

    async def _quantum_delivery_loop(self):
        """Loop principal de entrega quântica com auto-cura."""
        while True:
            try:
                job: NotificationJob = await self.notification_queue.get()
                logger.info(f"📧 Processando job de notificação: {job.job_id}")
                
                success = await self._attempt_delivery(job)
                
                if success:
                    job.status = NotificationStatus.SENT
                    job.sent_at = datetime.now()
                    self.delivery_stats["total_sent"] += 1
                    logger.info(f"✅ Email enviado com sucesso para {job.recipient_email}")
                else:
                    job.attempts += 1
                    self.delivery_stats["total_retries"] += 1
                    
                    if job.attempts < job.max_attempts:
                        job.status = NotificationStatus.RETRYING
                        logger.warning(f"🔄 Tentativa {job.attempts}/{job.max_attempts} falhou. Reagendando...")
                        await asyncio.sleep(5 * job.attempts)  # Backoff exponencial
                        await self.notification_queue.put(job)
                    else:
                        job.status = NotificationStatus.FAILED
                        self.delivery_stats["total_failed"] += 1
                        logger.error(f"❌ Falha permanente no envio para {job.recipient_email} após {job.max_attempts} tentativas.")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro crítico no loop de entrega: {e}", exc_info=True)

    async def _attempt_delivery(self, job: NotificationJob) -> bool:
        """Tenta entregar uma notificação usando o provedor ativo."""
        if not self.providers or self.status == "degraded":
            logger.error("❌ Nenhum provedor disponível para entrega.")
            return False
        
        # Rotaciona entre provedores em caso de falha
        for attempt in range(len(self.providers)):
            provider = self.providers[self.active_provider_index]
            
            try:
                success = await self._send_email_with_provider(job, provider)
                if success:
                    return True
                else:
                    # Tenta próximo provedor
                    self.active_provider_index = (self.active_provider_index + 1) % len(self.providers)
                    logger.warning(f"🔄 Tentando próximo provedor: {self.providers[self.active_provider_index].provider.value}")
                    
            except Exception as e:
                logger.error(f"❌ Provedor {provider.provider.value} falhou: {e}")
                self.active_provider_index = (self.active_provider_index + 1) % len(self.providers)
        
        return False

    async def _send_email_with_provider(self, job: NotificationJob, provider: NotificationConfig) -> bool:
        """Envia email usando um provedor específico."""
        try:
            loop = asyncio.get_running_loop()
            
            def _sync_send():
                msg = EmailMessage()
                msg['Subject'] = job.subject
                msg['From'] = provider.from_email
                msg['To'] = job.recipient_email
                msg.set_content(job.body)
                
                server = smtplib.SMTP(provider.smtp_host, provider.smtp_port, timeout=30)
                if provider.use_tls:
                    server.starttls()
                server.login(provider.username, provider.password)
                server.send_message(msg)
                server.quit()
                return True
            
            return await loop.run_in_executor(None, _sync_send)
            
        except Exception as e:
            job.error_message = str(e)
            logger.error(f"❌ Falha no envio via {provider.provider.value}: {e}")
            return False

    async def _internal_handle_message(self, message: AgentMessage):
        """Processa requisições de notificação."""
        if message.message_type != MessageType.REQUEST:
            return
        
        if self.status == "degraded":
            await self.publish_error_response(message, "Serviço de notificação não está operacional. Configure as credenciais de email.")
            return
        
        recipient = message.content.get("recipient_email")
        subject = message.content.get("subject")
        body = message.content.get("body")
        
        if not all([recipient, subject, body]):
            await self.publish_error_response(message, "Campos obrigatórios: recipient_email, subject, body")
            return
        
        # Criar job de notificação
        job = NotificationJob(
            job_id=f"email_{int(time.time())}_{recipient.split('@')[0]}",
            recipient_email=recipient,
            subject=subject,
            body=body
        )
        
        # Adicionar à fila
        await self.notification_queue.put(job)
        
        logger.info(f"📧 Job de notificação criado: {job.job_id}")
        await self.publish_response(message, {
            "status": "queued",
            "job_id": job.job_id,
            "message": f"Email para {recipient} foi enfileirado para entrega."
        })

    def get_delivery_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de entrega."""
        uptime = datetime.now() - self.delivery_stats["uptime_start"]
        return {
            **self.delivery_stats,
            "uptime_seconds": uptime.total_seconds(),
            "active_providers": len(self.providers),
            "current_provider": self.providers[self.active_provider_index].provider.value if self.providers else None,
            "success_rate": (
                self.delivery_stats["total_sent"] / 
                (self.delivery_stats["total_sent"] + self.delivery_stats["total_failed"])
                if self.delivery_stats["total_sent"] + self.delivery_stats["total_failed"] > 0 else 1.0
            )
        }

def create_notification_agent(message_bus) -> List[BaseNetworkAgent]:
    """Cria o agente de Notificação Quântico."""
    agents = []
    logger.info("📧 Criando QuantumNotificationAgent...")
    try:
        agent = QuantumNotificationAgent("notification_001", message_bus)
        agents.append(agent)
        logger.info("✅ QuantumNotificationAgent criado com sucesso.")
    except Exception as e:
        logger.error(f"❌ Erro crítico criando QuantumNotificationAgent: {e}", exc_info=True)
    return agents
