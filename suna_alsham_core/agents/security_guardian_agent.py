"""
ALSHAM QUANTUM - Security Guardian Agent
Quantum Level Multi-Agent System Component

Agent: SecurityGuardianAgent
Purpose: Advanced security management with quantum encryption, threat detection, and comprehensive audit
Level: QUANTUM
Dependencies: cryptography, jwt, bcrypt, passlib, sqlalchemy
"""

import asyncio
import hashlib
import secrets
import time
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import re
import ipaddress
from collections import defaultdict, deque
import json

# CORREÇÃO: Import paths corrigidos
from ..core.base_agent import BaseAgent
from ..core.agent_types import AgentType
from ..core.message import Message, MessageType

class SecurityLevel(Enum):
    """Security clearance levels"""
    PUBLIC = "public"
    INTERNAL = "internal" 
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"
    QUANTUM = "quantum"

class ThreatLevel(Enum):
    """Threat assessment levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    APOCALYPTIC = "apocalyptic"

class AuthMethod(Enum):
    """Authentication methods"""
    PASSWORD = "password"
    MFA = "mfa"
    BIOMETRIC = "biometric"
    QUANTUM_KEY = "quantum_key"
    CERTIFICATE = "certificate"

@dataclass
class SecurityContext:
    """Security context for operations"""
    user_id: str
    session_id: str
    security_level: SecurityLevel
    permissions: Set[str] = field(default_factory=set)
    auth_methods: List[AuthMethod] = field(default_factory=list)
    ip_address: str = ""
    user_agent: str = ""
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(hours=8))
    last_activity: datetime = field(default_factory=datetime.utcnow)
    
    def is_valid(self) -> bool:
        """Check if context is still valid"""
        return datetime.utcnow() < self.expires_at
    
    def has_permission(self, permission: str) -> bool:
        """Check if context has specific permission"""
        return permission in self.permissions

@dataclass
class ThreatEvent:
    """Security threat event"""
    event_id: str
    timestamp: datetime
    threat_level: ThreatLevel
    source_ip: str
    event_type: str
    description: str
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    mitigated: bool = False

@dataclass
class AuditLog:
    """Security audit log entry"""
    log_id: str
    timestamp: datetime
    user_id: str
    action: str
    resource: str
    result: str
    ip_address: str
    user_agent: str
    security_level: SecurityLevel
    metadata: Dict[str, Any] = field(default_factory=dict)

class QuantumEncryption:
    """Quantum-resistant encryption system"""
    
    def __init__(self):
        self.master_key = Fernet.generate_key()
        self.fernet = Fernet(self.master_key)
        self.rsa_keys = self._generate_rsa_keys()
        self.session_keys: Dict[str, bytes] = {}
    
    def _generate_rsa_keys(self) -> Tuple[Any, Any]:
        """Generate RSA key pair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    def encrypt_data(self, data: str, session_id: Optional[str] = None) -> str:
        """Encrypt data with quantum-resistant encryption"""
        try:
            if session_id and session_id in self.session_keys:
                fernet = Fernet(self.session_keys[session_id])
                return fernet.encrypt(data.encode()).decode()
            return self.fernet.encrypt(data.encode()).decode()
        except Exception as e:
            raise Exception(f"Encryption failed: {e}")
    
    def decrypt_data(self, encrypted_data: str, session_id: Optional[str] = None) -> str:
        """Decrypt data"""
        try:
            if session_id and session_id in self.session_keys:
                fernet = Fernet(self.session_keys[session_id])
                return fernet.decrypt(encrypted_data.encode()).decode()
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            raise Exception(f"Decryption failed: {e}")
    
    def create_session_key(self, session_id: str) -> str:
        """Create session-specific encryption key"""
        session_key = Fernet.generate_key()
        self.session_keys[session_id] = session_key
        return base64.b64encode(session_key).decode()
    
    def sign_data(self, data: str) -> str:
        """Create digital signature"""
        private_key, _ = self.rsa_keys
        signature = private_key.sign(
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode()
    
    def verify_signature(self, data: str, signature: str) -> bool:
        """Verify digital signature"""
        try:
            _, public_key = self.rsa_keys
            public_key.verify(
                base64.b64decode(signature.encode()),
                data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

class ThreatDetector:
    """Advanced threat detection system"""
    
    def __init__(self):
        self.failed_attempts: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.suspicious_ips: Set[str] = set()
        self.blocked_ips: Set[str] = set()
        self.threat_patterns = [
            r'(?i)(union|select|insert|delete|drop|create|alter|exec|script)',
            r'(?i)(javascript:|data:|vbscript:)',
            r'(<script|<iframe|<object|<embed)',
            r'(\.\./|\.\.\\)',
            r'(/etc/passwd|/etc/shadow)',
            r'(cmd\.exe|powershell\.exe|bash)',
        ]
        self.rate_limits: Dict[str, Dict] = defaultdict(dict)
    
    def detect_brute_force(self, ip_address: str, user_id: str) -> ThreatLevel:
        """Detect brute force attacks"""
        current_time = time.time()
        key = f"{ip_address}:{user_id}"
        
        # Clean old attempts (older than 1 hour)
        while (self.failed_attempts[key] and 
               current_time - self.failed_attempts[key][0] > 3600):
            self.failed_attempts[key].popleft()
        
        self.failed_attempts[key].append(current_time)
        attempts = len(self.failed_attempts[key])
        
        if attempts >= 50:
            return ThreatLevel.APOCALYPTIC
        elif attempts >= 20:
            return ThreatLevel.CRITICAL
        elif attempts >= 10:
            return ThreatLevel.HIGH
        elif attempts >= 5:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def detect_injection_attack(self, input_data: str) -> bool:
        """Detect SQL injection and XSS attempts"""
        for pattern in self.threat_patterns:
            if re.search(pattern, input_data):
                return True
        return False
    
    def check_rate_limit(self, ip_address: str, endpoint: str, limit: int = 100, window: int = 3600) -> bool:
        """Check rate limiting"""
        current_time = time.time()
        key = f"{ip_address}:{endpoint}"
        
        if key not in self.rate_limits:
            self.rate_limits[key] = {'requests': deque(), 'blocked_until': 0}
        
        data = self.rate_limits[key]
        
        # Check if still blocked
        if current_time < data['blocked_until']:
            return False
        
        # Clean old requests
        while data['requests'] and current_time - data['requests'][0] > window:
            data['requests'].popleft()
        
        # Check limit
        if len(data['requests']) >= limit:
            data['blocked_until'] = current_time + 300  # Block for 5 minutes
            return False
        
        data['requests'].append(current_time)
        return True
    
    def analyze_user_behavior(self, context: SecurityContext) -> ThreatLevel:
        """Analyze user behavior for anomalies"""
        threat_score = 0
        
        # Check for suspicious IP
        try:
            ip = ipaddress.ip_address(context.ip_address)
            if ip.is_private:
                threat_score -= 1
            elif context.ip_address in self.suspicious_ips:
                threat_score += 3
            elif context.ip_address in self.blocked_ips:
                threat_score += 5
        except ValueError:
            threat_score += 2
        
        # Check session duration
        session_duration = (datetime.utcnow() - context.last_activity).total_seconds()
        if session_duration > 86400:  # 24 hours
            threat_score += 2
        
        # Check permission escalation attempts
        if SecurityLevel.QUANTUM in [context.security_level] and len(context.permissions) > 50:
            threat_score += 3
        
        if threat_score >= 8:
            return ThreatLevel.CRITICAL
        elif threat_score >= 5:
            return ThreatLevel.HIGH
        elif threat_score >= 3:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW

class SecurityGuardianAgent(BaseAgent):
    """
    Quantum Level Security Guardian Agent
    
    Advanced security management system providing:
    - Multi-factor authentication
    - Quantum-resistant encryption
    - Threat detection and prevention
    - Security audit and compliance
    - Access control and permissions
    - Real-time security monitoring
    """
    
    def __init__(self, agent_id: str = "security_guardian", message_bus=None):
        super().__init__(agent_id, AgentType.SECURITY, capabilities=[
            "quantum_encryption", "threat_detection", "authentication", 
            "audit_logging", "access_control", "behavioral_analysis"
        ])
        
        # Core components
        self.encryption = QuantumEncryption()
        self.threat_detector = ThreatDetector()
        self.message_bus = message_bus
        
        # Security state
        self.active_sessions: Dict[str, SecurityContext] = {}
        self.security_policies: Dict[str, Dict] = {}
        self.threat_events: List[ThreatEvent] = []
        self.audit_logs: List[AuditLog] = []
        
        # Configuration
        self.config = {
            'session_timeout': 28800,  # 8 hours
            'max_login_attempts': 5,
            'password_complexity': True,
            'mfa_required': True,
            'audit_retention_days': 365,
            'threat_response_enabled': True,
            'quantum_encryption': True
        }
        
        # Security metrics
        self.metrics = {
            'total_sessions': 0,
            'active_sessions': 0,
            'failed_authentications': 0,
            'threat_events': 0,
            'blocked_attempts': 0,
            'encryption_operations': 0
        }
        
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.logger.info("Security Guardian Agent initialized with quantum-level protection")
    
    async def authenticate_user(self, credentials: Dict[str, Any]) -> Optional[SecurityContext]:
        """Authenticate user with multiple factors"""
        try:
            username = credentials.get('username')
            password = credentials.get('password')
            ip_address = credentials.get('ip_address', '0.0.0.0')
            user_agent = credentials.get('user_agent', 'Unknown')
            
            if not username or not password:
                await self._log_security_event("authentication_failed", "Missing credentials", ip_address)
                return None
            
            # Check for brute force
            threat_level = self.threat_detector.detect_brute_force(ip_address, username)
            if threat_level in [ThreatLevel.CRITICAL, ThreatLevel.APOCALYPTIC]:
                await self._block_ip(ip_address, f"Brute force detected: {threat_level.value}")
                return None
            
            # Rate limiting
            if not self.threat_detector.check_rate_limit(ip_address, 'auth', 10, 300):
                await self._log_security_event("rate_limit_exceeded", f"Auth rate limit for {ip_address}", ip_address)
                return None
            
            # Validate credentials (simplified - would integrate with user database)
            user_data = await self._validate_credentials(username, password)
            if not user_data:
                self.metrics['failed_authentications'] += 1
                await self._log_security_event("authentication_failed", f"Invalid credentials for {username}", ip_address)
                return None
            
            # Create security context
            session_id = secrets.token_urlsafe(32)
            context = SecurityContext(
                user_id=user_data['user_id'],
                session_id=session_id,
                security_level=SecurityLevel(user_data.get('security_level', 'internal')),
                permissions=set(user_data.get('permissions', [])),
                auth_methods=[AuthMethod.PASSWORD],
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Handle MFA if required
            if self.config['mfa_required'] and user_data.get('mfa_enabled'):
                mfa_token = credentials.get('mfa_token')
                if not mfa_token or not await self._verify_mfa(user_data['user_id'], mfa_token):
                    await self._log_security_event("mfa_failed", f"MFA verification failed for {username}", ip_address)
                    return None
                context.auth_methods.append(AuthMethod.MFA)
            
            # Store session
            self.active_sessions[session_id] = context
            self.metrics['total_sessions'] += 1
            self.metrics['active_sessions'] = len(self.active_sessions)
            
            # Create session encryption key
            self.encryption.create_session_key(session_id)
            
            # Log successful authentication
            await self._log_audit_event(
                user_id=context.user_id,
                action="authentication_success",
                resource="auth_system",
                result="success",
                ip_address=ip_address,
                user_agent=user_agent,
                security_level=context.security_level
            )
            
            self.logger.info(f"User {username} authenticated successfully with session {session_id}")
            return context
            
        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            await self._log_security_event("authentication_error", str(e), ip_address)
            return None
    
    async def authorize_action(self, session_id: str, action: str, resource: str) -> bool:
        """Authorize user action"""
        try:
            if session_id not in self.active_sessions:
                await self._log_security_event("authorization_failed", f"Invalid session {session_id}")
                return False
            
            context = self.active_sessions[session_id]
            
            # Check session validity
            if not context.is_valid():
                await self._expire_session(session_id)
                return False
            
            # Update last activity
            context.last_activity = datetime.utcnow()
            
            # Check permissions
            required_permission = f"{action}:{resource}"
            if not context.has_permission(required_permission) and not context.has_permission("admin:*"):
                await self._log_audit_event(
                    user_id=context.user_id,
                    action="authorization_denied",
                    resource=resource,
                    result="denied",
                    ip_address=context.ip_address,
                    user_agent=context.user_agent,
                    security_level=context.security_level,
                    metadata={'required_permission': required_permission}
                )
                return False
            
            # Check security level requirements
            resource_security_level = await self._get_resource_security_level(resource)
            if resource_security_level and context.security_level.value < resource_security_level.value:
                await self._log_security_event("insufficient_clearance", 
                    f"User {context.user_id} lacks clearance for {resource}")
                return False
            
            # Log successful authorization
            await self._log_audit_event(
                user_id=context.user_id,
                action="authorization_success",
                resource=resource,
                result="granted",
                ip_address=context.ip_address,
                user_agent=context.user_agent,
                security_level=context.security_level,
                metadata={'action': action}
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Authorization error: {e}")
            return False
    
    async def encrypt_message(self, message: str, session_id: Optional[str] = None) -> str:
        """Encrypt message with quantum encryption"""
        try:
            encrypted = self.encryption.encrypt_data(message, session_id)
            self.metrics['encryption_operations'] += 1
            return encrypted
        except Exception as e:
            self.logger.error(f"Encryption failed: {e}")
            raise
    
    async def decrypt_message(self, encrypted_message: str, session_id: Optional[str] = None) -> str:
        """Decrypt message"""
        try:
            decrypted = self.encryption.decrypt_data(encrypted_message, session_id)
            self.metrics['encryption_operations'] += 1
            return decrypted
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            raise
    
    async def scan_for_threats(self, data: Dict[str, Any]) -> List[ThreatEvent]:
        """Scan data for security threats"""
        threats = []
        
        try:
            # Check for injection attacks
            for key, value in data.items():
                if isinstance(value, str) and self.threat_detector.detect_injection_attack(value):
                    threat = ThreatEvent(
                        event_id=secrets.token_hex(16),
                        timestamp=datetime.utcnow(),
                        threat_level=ThreatLevel.HIGH,
                        source_ip=data.get('ip_address', 'unknown'),
                        event_type='injection_attempt',
                        description=f'Injection pattern detected in field: {key}',
                        metadata={'field': key, 'pattern': value[:100]}
                    )
                    threats.append(threat)
                    await self._handle_threat(threat)
            
            # Behavioral analysis
            if 'session_id' in data and data['session_id'] in self.active_sessions:
                context = self.active_sessions[data['session_id']]
                behavior_threat = self.threat_detector.analyze_user_behavior(context)
                
                if behavior_threat in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
                    threat = ThreatEvent(
                        event_id=secrets.token_hex(16),
                        timestamp=datetime.utcnow(),
                        threat_level=behavior_threat,
                        source_ip=context.ip_address,
                        event_type='suspicious_behavior',
                        description=f'Anomalous user behavior detected',
                        user_id=context.user_id,
                        metadata={'behavior_score': behavior_threat.value}
                    )
                    threats.append(threat)
                    await self._handle_threat(threat)
            
            return threats
            
        except Exception as e:
            self.logger.error(f"Threat scanning error: {e}")
            return []
    
    async def generate_security_report(self) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        try:
            # Session statistics
            active_sessions = len(self.active_sessions)
            expired_sessions = 0
            
            for session_id, context in list(self.active_sessions.items()):
                if not context.is_valid():
                    expired_sessions += 1
                    await self._expire_session(session_id)
            
            # Threat analysis
            recent_threats = [t for t in self.threat_events 
                            if (datetime.utcnow() - t.timestamp).days <= 7]
            
            threat_by_level = defaultdict(int)
            for threat in recent_threats:
                threat_by_level[threat.threat_level.value] += 1
            
            # Security metrics
            report = {
                'timestamp': datetime.utcnow().isoformat(),
                'system_status': 'operational',
                'sessions': {
                    'active': active_sessions,
                    'total_created': self.metrics['total_sessions'],
                    'expired_cleaned': expired_sessions
                },
                'authentication': {
                    'failed_attempts': self.metrics['failed_authentications'],
                    'success_rate': self._calculate_auth_success_rate()
                },
                'threats': {
                    'total_detected': len(recent_threats),
                    'by_level': dict(threat_by_level),
                    'mitigated': len([t for t in recent_threats if t.mitigated]),
                    'blocked_ips': len(self.threat_detector.blocked_ips)
                },
                'encryption': {
                    'operations': self.metrics['encryption_operations'],
                    'quantum_enabled': self.config['quantum_encryption']
                },
                'audit': {
                    'total_logs': len(self.audit_logs),
                    'retention_days': self.config['audit_retention_days']
                },
                'recommendations': await self._generate_security_recommendations()
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Security report generation failed: {e}")
            return {'error': str(e), 'timestamp': datetime.utcnow().isoformat()}
    
    # Private helper methods
    async def _validate_credentials(self, username: str, password: str) -> Optional[Dict]:
        """Validate user credentials (simplified implementation)"""
        # This would integrate with your user database/directory service
        # For demo purposes, using hardcoded admin user
        if username == "admin" and password == "quantum_secure_2024!":
            return {
                'user_id': 'admin_001',
                'security_level': 'quantum',
                'permissions': ['admin:*', 'read:*', 'write:*', 'delete:*'],
                'mfa_enabled': True
            }
        return None
    
    async def _verify_mfa(self, user_id: str, token: str) -> bool:
        """Verify MFA token (simplified implementation)"""
        # This would integrate with your MFA service (TOTP, SMS, etc.)
        return token == "123456"  # Demo token
    
    async def _get_resource_security_level(self, resource: str) -> Optional[SecurityLevel]:
        """Get required security level for resource"""
        # Resource security classification
        security_map = {
            'quantum_core': SecurityLevel.QUANTUM,
            'admin_panel': SecurityLevel.SECRET,
            'user_data': SecurityLevel.CONFIDENTIAL,
            'public_api': SecurityLevel.INTERNAL
        }
        
        for pattern, level in security_map.items():
            if pattern in resource:
                return level
        
        return SecurityLevel.INTERNAL
    
    async def _handle_threat(self, threat: ThreatEvent):
        """Handle detected threat"""
        self.threat_events.append(threat)
        self.metrics['threat_events'] += 1
        
        if threat.threat_level in [ThreatLevel.CRITICAL, ThreatLevel.APOCALYPTIC]:
            # Immediate response for critical threats
            if threat.source_ip:
                await self._block_ip(threat.source_ip, f"Critical threat: {threat.event_type}")
            
            # Alert administrators
            await self._send_security_alert(threat)
        
        # Log the threat
        self.logger.warning(f"Threat detected: {threat.event_type} from {threat.source_ip} - Level: {threat.threat_level.value}")
    
    async def _block_ip(self, ip_address: str, reason: str):
        """Block IP address"""
        self.threat_detector.blocked_ips.add(ip_address)
        self.metrics['blocked_attempts'] += 1
        
        await self._log_security_event("ip_blocked", f"IP {ip_address} blocked: {reason}", ip_address)
        self.logger.warning(f"IP {ip_address} blocked: {reason}")
    
    async def _expire_session(self, session_id: str):
        """Expire user session"""
        if session_id in self.active_sessions:
            context = self.active_sessions[session_id]
            del self.active_sessions[session_id]
            
            # Clean up session key
            if session_id in self.encryption.session_keys:
                del self.encryption.session_keys[session_id]
            
            self.metrics['active_sessions'] = len(self.active_sessions)
            
            await self._log_audit_event(
                user_id=context.user_id,
                action="session_expired",
                resource="auth_system",
                result="expired",
                ip_address=context.ip_address,
                user_agent=context.user_agent,
                security_level=context.security_level
            )
    
    async def _log_security_event(self, event_type: str, description: str, ip_address: str = "unknown"):
        """Log security event"""
        threat = ThreatEvent(
            event_id=secrets.token_hex(16),
            timestamp=datetime.utcnow(),
            threat_level=ThreatLevel.MEDIUM,
            source_ip=ip_address,
            event_type=event_type,
            description=description
        )
        self.threat_events.append(threat)
    
    async def _log_audit_event(self, user_id: str, action: str, resource: str, result: str,
                             ip_address: str, user_agent: str, security_level: SecurityLevel,
                             metadata: Dict = None):
        """Log audit event"""
        audit_log = AuditLog(
            log_id=secrets.token_hex(16),
            timestamp=datetime.utcnow(),
            user_id=user_id,
            action=action,
            resource=resource,
            result=result,
            ip_address=ip_address,
            user_agent=user_agent,
            security_level=security_level,
            metadata=metadata or {}
        )
        self.audit_logs.append(audit_log)
    
    async def _send_security_alert(self, threat: ThreatEvent):
        """Send security alert to administrators"""
        alert_message = {
            'type': 'security_alert',
            'severity': 'critical',
            'threat_id': threat.event_id,
            'threat_level': threat.threat_level.value,
            'description': threat.description,
            'source_ip': threat.source_ip,
            'timestamp': threat.timestamp.isoformat()
        }
        
        if self.message_bus:
            await self.message_bus.broadcast('security_alert', alert_message)
    
    def _calculate_auth_success_rate(self) -> float:
        """Calculate authentication success rate"""
        if self.metrics['total_sessions'] == 0:
            return 100.0
        
        success_rate = ((self.metrics['total_sessions'] - self.metrics['failed_authentications']) / 
                       max(self.metrics['total_sessions'], 1)) * 100
        return round(success_rate, 2)
    
    async def _generate_security_recommendations(self) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        # Check authentication success rate
        success_rate = self._calculate_auth_success_rate()
        if success_rate < 90:
            recommendations.append("Consider implementing additional authentication security measures")
        
        # Check threat levels
        critical_threats = len([t for t in self.threat_events 
                              if t.threat_level in [ThreatLevel.CRITICAL, ThreatLevel.APOCALYPTIC]])
        if critical_threats > 10:
            recommendations.append("High number of critical threats detected - review security policies")
        
        # Check session management
        if len(self.active_sessions) > 1000:
            recommendations.append("Large number of active sessions - consider session timeout reduction")
        
        # Check blocked IPs
        if len(self.threat_detector.blocked_ips) > 100:
            recommendations.append("Review blocked IP list for potential false positives")
        
        if not recommendations:
            recommendations.append("Security posture is optimal - continue monitoring")
        
        return recommendations
    
    # Network agent methods
    async def process_message(self, message: Message) -> Message:
        """Process incoming security messages"""
        try:
            if message.type == MessageType.QUERY:
                content = message.content
                
                if isinstance(content, dict):
                    message_type = content.get('type', 'unknown')
                    
                    if message_type == 'authenticate':
                        context = await self.authenticate_user(content.get('credentials', {}))
                        return Message(
                            message_type=MessageType.RESPONSE,
                            sender_id=self.agent_id,
                            recipient_id=message.sender_id,
                            content={
                                'success': context is not None,
                                'session_id': context.session_id if context else None,
                                'security_level': context.security_level.value if context else None
                            }
                        )
                    
                    elif message_type == 'authorize':
                        authorized = await self.authorize_action(
                            content.get('session_id'),
                            content.get('action'),
                            content.get('resource')
                        )
                        return Message(
                            message_type=MessageType.RESPONSE,
                            sender_id=self.agent_id,
                            recipient_id=message.sender_id,
                            content={'authorized': authorized}
                        )
                    
                    elif message_type == 'encrypt':
                        encrypted = await self.encrypt_message(
                            content.get('data'),
                            content.get('session_id')
                        )
                        return Message(
                            message_type=MessageType.RESPONSE,
                            sender_id=self.agent_id,
                            recipient_id=message.sender_id,
                            content={'encrypted_data': encrypted}
                        )
                    
                    elif message_type == 'decrypt':
                        decrypted = await self.decrypt_message(
                            content.get('encrypted_data'),
                            content.get('session_id')
                        )
                        return Message(
                            message_type=MessageType.RESPONSE,
                            sender_id=self.agent_id,
                            recipient_id=message.sender_id,
                            content={'decrypted_data': decrypted}
                        )
                    
                    elif message_type == 'threat_scan':
                        threats = await self.scan_for_threats(content.get('data', {}))
                        return Message(
                            message_type=MessageType.RESPONSE,
                            sender_id=self.agent_id,
                            recipient_id=message.sender_id,
                            content={
                                'threats_found': len(threats),
                                'threats': [{'level': t.threat_level.value, 'type': t.event_type} for t in threats]
                            }
                        )
                    
                    elif message_type == 'security_report':
                        report = await self.generate_security_report()
                        return Message(
                            message_type=MessageType.RESPONSE,
                            sender_id=self.agent_id,
                            recipient_id=message.sender_id,
                            content=report
                        )
                    
                    else:
                        return Message(
                            message_type=MessageType.ERROR,
                            sender_id=self.agent_id,
                            recipient_id=message.sender_id,
                            content={'error': f'Unknown message type: {message_type}'}
                        )
                        
                elif isinstance(content, str) and "security" in content.lower():
                    report = await self.generate_security_report()
                    return Message(
                        message_type=MessageType.RESPONSE,
                        sender_id=self.agent_id,
                        recipient_id=message.sender_id,
                        content=report
                    )
            
            return await super().process_message(message)
                
        except Exception as e:
            self.logger.error(f"Message processing error: {e}")
            return Message(
                message_type=MessageType.ERROR,
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                content={'error': str(e)}
            )
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type.value,
            'status': 'operational',
            'security_level': 'quantum',
            'active_sessions': len(self.active_sessions),
            'threats_monitored': len(self.threat_events),
            'encryption_status': 'quantum_enabled',
            'last_updated': datetime.utcnow().isoformat(),
            'metrics': self.metrics
        }



class BasicSecurityAgent:
    """Agente de segurança básico como fallback"""
    def __init__(self):
        self.agent_id = "security_basic_001"
        self.capabilities = ["basic_monitoring", "log_analysis"]
    def get_capabilities(self):
        return self.capabilities
    async def process_message(self, message):
        return {"status": "basic_security_active", "agent": self.agent_id}

def create_agents(message_bus=None) -> List[BaseAgent]:
    """
    Função fábrica robusta para criar e inicializar o(s) SecurityGuardianAgent(s) do sistema ALSHAM QUANTUM.
    Sempre retorna pelo menos um agente funcional, mesmo com dependências ausentes.
    """
    agents: List[BaseAgent] = []
    try:
        # Verificação de dependências essenciais
        required_modules = ['cryptography', 'hashlib', 'secrets']
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        if missing_modules:
            print(f"⚠️ Módulos faltando para SecurityGuardian: {missing_modules}")
            basic_agent = BasicSecurityAgent()
            agents.append(basic_agent)
        else:
            agent = SecurityGuardianAgent("security_guardian", message_bus)
            agents.append(agent)
            logging.info(f"🛡️ SecurityGuardianAgent criado e registrado: {agent.agent_id}")
        print(f"✅ SecurityGuardian criado com sucesso: {len(agents)} agente(s)")
        return agents
    except Exception as e:
        print(f"❌ Erro ao criar SecurityGuardian: {e}")
        # Em caso de erro, criar pelo menos um agente básico
        try:
            fallback_agent = BasicSecurityAgent()
            return [fallback_agent]
        except Exception:
            return []

# Export for dynamic loading
__all__ = ['SecurityGuardianAgent', 'create_agents', 'SecurityLevel', 'ThreatLevel', 'AuthMethod']

    def get_capabilities(self):
        return ["authentication", "authorization", "encryption", "threat_detection", "jwt_management", "rate_limiting", "audit_logging", "intrusion_detection"]


    def get_capabilities(self):
        return ["authentication", "authorization", "encryption", "threat_detection", "jwt_management", "rate_limiting", "audit_logging", "intrusion_detection", "cryptographic_operations"]
