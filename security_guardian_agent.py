#!/usr/bin/env python3
"""
Security Guardian Agent - Proteção Suprema do Sistema SUNA-ALSHAM
Agente de segurança avançado com capacidades de proteção em tempo real
"""

import logging
import hashlib
import secrets
import jwt
import time
import re
import subprocess
import socket
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import json
from pathlib import Path
from collections import defaultdict, deque
import ipaddress
from multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class ThreatLevel(Enum):
    """Níveis de ameaça"""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    CATASTROPHIC = "catastrophic"

class SecurityEventType(Enum):
    """Tipos de eventos de segurança"""
    AUTHENTICATION_FAILURE = "auth_failure"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    INTRUSION_ATTEMPT = "intrusion_attempt"
    DATA_BREACH = "data_breach"
    MALWARE_DETECTED = "malware_detected"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    SQL_INJECTION = "sql_injection"
    XSS_ATTEMPT = "xss_attempt"
    BRUTE_FORCE = "brute_force"
    DDoS_ATTACK = "ddos_attack"
    INSIDER_THREAT = "insider_threat"

class AccessLevel(Enum):
    """Níveis de acesso"""
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    SYSTEM = "system"
    ROOT = "root"

@dataclass
class SecurityEvent:
    """Evento de segurança"""
    event_id: str
    event_type: SecurityEventType
    threat_level: ThreatLevel
    source_ip: str
    user_agent: Optional[str]
    description: str
    affected_resource: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False

@dataclass
class SecurityRule:
    """Regra de segurança"""
    rule_id: str
    name: str
    description: str
    pattern: str
    action: str  # block, alert, quarantine, log
    enabled: bool = True
    severity: ThreatLevel = ThreatLevel.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class AccessToken:
    """Token de acesso"""
    token_id: str
    user_id: str
    access_level: AccessLevel
    permissions: List[str]
    expires_at: datetime
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None

class SecurityGuardianAgent(BaseNetworkAgent):
    """Agente Guardian de Segurança Supremo do Sistema"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'authentication',
            'authorization', 
            'intrusion_detection',
            'encryption_management',
            'access_control',
            'threat_prevention',
            'security_audit',
            'vulnerability_scanning',
            'malware_detection',
            'network_security',
            'real_time_monitoring',
            'incident_response',
            'forensic_analysis',
            'compliance_checking'
        ]
        self.status = 'active'
        
        # Estado de segurança
        self.security_events = deque(maxlen=10000)
        self.active_threats = {}
        self.security_rules = {}
        self.access_tokens = {}
        self.blocked_ips = set()
        self.suspicious_ips = defaultdict(int)
        self.failed_attempts = defaultdict(list)
        
        # Configurações de segurança
        self.max_login_attempts = 5
        self.lockout_duration = 300  # 5 minutos
        self.token_expiry = 3600  # 1 hora
        self.encryption_key = self._generate_encryption_key()
        self.jwt_secret = secrets.token_urlsafe(64)
        
        # Padrões de ameaças
        self.threat_patterns = self._load_threat_patterns()
        self.malware_signatures = self._load_malware_signatures()
        self.vulnerability_db = self._load_vulnerability_database()
        
        # Monitoramento
        self.monitoring_active = True
        self.scan_interval = 30  # segundos
        self.alert_thresholds = {
            'failed_logins_per_minute': 10,
            'suspicious_requests_per_minute': 50,
            'data_transfer_mb_per_minute': 100
        }
        
        # Estatísticas
        self.security_metrics = {
            'threats_blocked': 0,
            'intrusions_detected': 0,
            'vulnerabilities_found': 0,
            'malware_detected': 0,
            'unauthorized_access_prevented': 0,
            'security_scans_performed': 0
        }
        
        # Tasks de background
        self._monitoring_task = None
        self._scanning_task = None
        self._cleanup_task = None
        
        # Inicializar regras padrão
        self._setup_default_rules()
        
        logger.info(f"🛡️ {self.agent_id} inicializado como Guardian Supremo da Segurança")
    
    def _generate_encryption_key(self) -> bytes:
        """Gera chave de criptografia segura"""
        return secrets.token_bytes(32)
    
    def _load_threat_patterns(self) -> Dict[str, Any]:
        """Carrega padrões de ameaças conhecidas"""
        return {
            'sql_injection': [
                re.compile(r"(\%27)|(\')|(\-\-)|(\%23)|(#)", re.IGNORECASE),
                re.compile(r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))", re.IGNORECASE),
                re.compile(r"union[\s]+select", re.IGNORECASE),
                re.compile(r"select[\s]+.*[\s]+from", re.IGNORECASE)
            ],
            'xss': [
                re.compile(r"<script[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL),
                re.compile(r"javascript:", re.IGNORECASE),
                re.compile(r"on\w+\s*=", re.IGNORECASE),
                re.compile(r"<iframe", re.IGNORECASE)
            ],
            'path_traversal': [
                re.compile(r"\.\.[\\/]", re.IGNORECASE),
                re.compile(r"[\\/]etc[\\/]passwd", re.IGNORECASE),
                re.compile(r"[\\/]proc[\\/]", re.IGNORECASE)
            ],
            'command_injection': [
                re.compile(r"[;&|`]", re.IGNORECASE),
                re.compile(r"\$\(.*\)", re.IGNORECASE),
                re.compile(r"&&|\|\|", re.IGNORECASE)
            ]
        }
    
    def _load_malware_signatures(self) -> List[Dict[str, Any]]:
        """Carrega assinaturas de malware"""
        return [
            {
                'name': 'Suspicious PowerShell',
                'pattern': re.compile(r'powershell.*-enc.*', re.IGNORECASE),
                'severity': ThreatLevel.HIGH
            },
            {
                'name': 'Base64 Encoded Payload',
                'pattern': re.compile(r'[A-Za-z0-9+/]{50,}={0,2}'),
                'severity': ThreatLevel.MEDIUM
            },
            {
                'name': 'Reverse Shell',
                'pattern': re.compile(r'(nc|netcat).*-e.*sh', re.IGNORECASE),
                'severity': ThreatLevel.CRITICAL
            },
            {
                'name': 'Crypto Mining',
                'pattern': re.compile(r'(stratum|mining|cryptonight)', re.IGNORECASE),
                'severity': ThreatLevel.HIGH
            }
        ]
    
    def _load_vulnerability_database(self) -> Dict[str, Any]:
        """Carrega base de vulnerabilidades conhecidas"""
        return {
            'CVE-2021-44228': {  # Log4j
                'severity': ThreatLevel.CRITICAL,
                'description': 'Log4j Remote Code Execution',
                'indicators': ['${jndi:', '${ldap:', '${rmi:']
            },
            'CVE-2021-34527': {  # PrintNightmare
                'severity': ThreatLevel.HIGH,
                'description': 'Windows Print Spooler RCE',
                'indicators': ['spoolsv.exe', 'localspl.dll']
            },
            'CVE-2022-0778': {  # OpenSSL
                'severity': ThreatLevel.HIGH,
                'description': 'OpenSSL Infinite Loop DoS',
                'indicators': ['openssl', 'BN_mod_sqrt']
            }
        }
    
    def _setup_default_rules(self):
        """Configura regras de segurança padrão"""
        default_rules = [
            SecurityRule(
                rule_id="RULE_001",
                name="Block SQL Injection",
                description="Detecta e bloqueia tentativas de SQL injection",
                pattern="sql_injection",
                action="block",
                severity=ThreatLevel.HIGH
            ),
            SecurityRule(
                rule_id="RULE_002",
                name="Block XSS Attempts",
                description="Detecta e bloqueia tentativas de Cross-Site Scripting",
                pattern="xss",
                action="block",
                severity=ThreatLevel.MEDIUM
            ),
            SecurityRule(
                rule_id="RULE_003",
                name="Detect Brute Force",
                description="Detecta ataques de força bruta",
                pattern="brute_force",
                action="alert",
                severity=ThreatLevel.HIGH
            ),
            SecurityRule(
                rule_id="RULE_004",
                name="Block Malware Signatures",
                description="Detecta assinaturas de malware conhecidas",
                pattern="malware",
                action="quarantine",
                severity=ThreatLevel.CRITICAL
            )
        ]
        
        for rule in default_rules:
            self.security_rules[rule.rule_id] = rule
    
    async def start_security_services(self):
        """Inicia serviços de segurança"""
        if not self._monitoring_task:
            self._monitoring_task = asyncio.create_task(self._security_monitoring_loop())
            self._scanning_task = asyncio.create_task(self._vulnerability_scanning_loop())
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
            logger.info(f"🛡️ {self.agent_id} iniciou serviços de segurança")
    
    async def stop_security_services(self):
        """Para serviços de segurança"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
        if self._scanning_task:
            self._scanning_task.cancel()
            self._scanning_task = None
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None
        logger.info(f"🛑 {self.agent_id} parou serviços de segurança")
    
    async def _security_monitoring_loop(self):
        """Loop principal de monitoramento de segurança"""
        while True:
            try:
                # Monitorar conexões ativas
                await self._monitor_network_connections()
                
                # Verificar IPs suspeitos
                await self._analyze_suspicious_activity()
                
                # Detectar anomalias
                anomalies = await self._detect_security_anomalies()
                if anomalies:
                    await self._handle_security_anomalies(anomalies)
                
                # Verificar integridade do sistema
                await self._verify_system_integrity()
                
                await asyncio.sleep(self.scan_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento de segurança: {e}")
    
    async def _vulnerability_scanning_loop(self):
        """Loop de varredura de vulnerabilidades"""
        while True:
            try:
                # Scan de vulnerabilidades
                vulnerabilities = await self._scan_vulnerabilities()
                
                if vulnerabilities:
                    await self._process_vulnerabilities(vulnerabilities)
                
                # Scan de malware
                malware_detected = await self._scan_malware()
                
                if malware_detected:
                    await self._handle_malware_detection(malware_detected)
                
                await asyncio.sleep(300)  # Scan a cada 5 minutos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no scan de vulnerabilidades: {e}")
    
    async def _cleanup_loop(self):
        """Loop de limpeza de dados antigos"""
        while True:
            try:
                # Limpar eventos antigos
                cutoff_time = datetime.now() - timedelta(hours=24)
                
                # Remover eventos antigos
                while self.security_events and self.security_events[0].timestamp < cutoff_time:
                    self.security_events.popleft()
                
                # Limpar IPs bloqueados temporariamente
                await self._cleanup_temporary_blocks()
                
                # Limpar tokens expirados
                await self._cleanup_expired_tokens()
                
                await asyncio.sleep(3600)  # Limpeza a cada hora
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na limpeza: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens de segurança"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'authenticate':
                result = await self.authenticate_user(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'authorize':
                result = await self.authorize_access(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'security_scan':
                result = await self.perform_security_scan(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'threat_analysis':
                result = await self.analyze_threat(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'encrypt_data':
                result = await self.encrypt_data(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'decrypt_data':
                result = await self.decrypt_data(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'security_report':
                result = await self.generate_security_report(message.content)
                await self._send_response(message, result)
        
        elif message.message_type == MessageType.NOTIFICATION:
            # Processar notificações de segurança
            notification_type = message.content.get('notification_type')
            
            if notification_type == 'suspicious_activity':
                await self._handle_suspicious_activity_notification(message.content)
            elif notification_type == 'security_alert':
                await self._handle_security_alert(message.content)
    
    async def authenticate_user(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Autentica usuário no sistema"""
        try:
            username = request_data.get('username')
            password = request_data.get('password')
            source_ip = request_data.get('source_ip', 'unknown')
            
            logger.info(f"🔐 Tentativa de autenticação: {username} de {source_ip}")
            
            # Verificar se IP está bloqueado
            if source_ip in self.blocked_ips:
                await self._log_security_event(
                    SecurityEventType.AUTHENTICATION_FAILURE,
                    ThreatLevel.HIGH,
                    source_ip,
                    f"Tentativa de login de IP bloqueado: {username}"
                )
                return {
                    'status': 'blocked',
                    'message': 'IP bloqueado por atividade suspeita'
                }
            
            # Verificar tentativas anteriores
            if self._check_brute_force(username, source_ip):
                return {
                    'status': 'blocked',
                    'message': 'Muitas tentativas de login falharam'
                }
            
            # Simular autenticação (em produção, verificaria hash da senha)
            if self._verify_credentials(username, password):
                # Gerar token de acesso
                token = await self._generate_access_token(username, source_ip)
                
                await self._log_security_event(
                    SecurityEventType.AUTHENTICATION_FAILURE,  # Sucesso seria outro tipo
                    ThreatLevel.MINIMAL,
                    source_ip,
                    f"Login bem-sucedido: {username}"
                )
                
                return {
                    'status': 'success',
                    'token': token,
                    'expires_in': self.token_expiry
                }
            else:
                # Registrar falha
                self._record_failed_attempt(username, source_ip)
                
                await self._log_security_event(
                    SecurityEventType.AUTHENTICATION_FAILURE,
                    ThreatLevel.MEDIUM,
                    source_ip,
                    f"Falha na autenticação: {username}"
                )
                
                return {
                    'status': 'failed',
                    'message': 'Credenciais inválidas'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro na autenticação: {e}")
            return {'status': 'error', 'message': 'Erro interno de autenticação'}
    
    def _verify_credentials(self, username: str, password: str) -> bool:
        """Verifica credenciais do usuário"""
        # Em produção, verificaria hash armazenado
        # Simulação simples para demonstração
        test_users = {
            'admin': 'admin123',
            'user': 'user123',
            'test': 'test123'
        }
        
        return test_users.get(username) == password
    
    def _check_brute_force(self, username: str, source_ip: str) -> bool:
        """Verifica se há tentativa de força bruta"""
        key = f"{username}:{source_ip}"
        now = datetime.now()
        
        # Limpar tentativas antigas
        if key in self.failed_attempts:
            self.failed_attempts[key] = [
                attempt for attempt in self.failed_attempts[key]
                if (now - attempt).seconds < self.lockout_duration
            ]
        
        # Verificar se excedeu limite
        if len(self.failed_attempts.get(key, [])) >= self.max_login_attempts:
            # Bloquear IP temporariamente
            self.blocked_ips.add(source_ip)
            logger.warning(f"🚨 IP {source_ip} bloqueado por força bruta")
            return True
        
        return False
    
    def _record_failed_attempt(self, username: str, source_ip: str):
        """Registra tentativa de login falhada"""
        key = f"{username}:{source_ip}"
        if key not in self.failed_attempts:
            self.failed_attempts[key] = []
        
        self.failed_attempts[key].append(datetime.now())
    
    async def _generate_access_token(self, username: str, source_ip: str) -> str:
        """Gera token de acesso JWT"""
        payload = {
            'username': username,
            'source_ip': source_ip,
            'issued_at': time.time(),
            'expires_at': time.time() + self.token_expiry,
            'permissions': self._get_user_permissions(username)
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        
        # Armazenar token
        token_id = hashlib.sha256(token.encode()).hexdigest()[:16]
        access_token = AccessToken(
            token_id=token_id,
            user_id=username,
            access_level=self._get_user_access_level(username),
            permissions=payload['permissions'],
            expires_at=datetime.fromtimestamp(payload['expires_at'])
        )
        
        self.access_tokens[token_id] = access_token
        
        return token
    
    def _get_user_permissions(self, username: str) -> List[str]:
        """Obtém permissões do usuário"""
        # Simulação de permissões
        permissions_map = {
            'admin': ['read', 'write', 'delete', 'admin'],
            'user': ['read', 'write'],
            'test': ['read']
        }
        
        return permissions_map.get(username, ['read'])
    
    def _get_user_access_level(self, username: str) -> AccessLevel:
        """Obtém nível de acesso do usuário"""
        if username == 'admin':
            return AccessLevel.ADMIN
        elif username == 'user':
            return AccessLevel.USER
        else:
            return AccessLevel.GUEST
    
    async def authorize_access(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Autoriza acesso a recurso"""
        try:
            token = request_data.get('token')
            resource = request_data.get('resource')
            action = request_data.get('action', 'read')
            
            # Verificar token
            token_data = self._verify_token(token)
            if not token_data:
                return {
                    'status': 'denied',
                    'message': 'Token inválido ou expirado'
                }
            
            # Verificar permissões
            if self._check_permissions(token_data, resource, action):
                await self._log_security_event(
                    SecurityEventType.UNAUTHORIZED_ACCESS,  # Seria ACCESS_GRANTED
                    ThreatLevel.MINIMAL,
                    token_data.get('source_ip', 'unknown'),
                    f"Acesso autorizado: {resource} - {action}"
                )
                
                return {
                    'status': 'granted',
                    'user': token_data['username'],
                    'permissions': token_data['permissions']
                }
            else:
                await self._log_security_event(
                    SecurityEventType.UNAUTHORIZED_ACCESS,
                    ThreatLevel.HIGH,
                    token_data.get('source_ip', 'unknown'),
                    f"Acesso negado: {resource} - {action}"
                )
                
                return {
                    'status': 'denied',
                    'message': 'Permissões insuficientes'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro na autorização: {e}")
            return {'status': 'error', 'message': 'Erro interno de autorização'}
    
    def _verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verifica validade do token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            
            # Verificar expiração
            if time.time() > payload['expires_at']:
                return None
            
            return payload
            
        except jwt.InvalidTokenError:
            return None
    
    def _check_permissions(self, token_data: Dict[str, Any], resource: str, action: str) -> bool:
        """Verifica se usuário tem permissão para ação"""
        permissions = token_data.get('permissions', [])
        
        # Verificar permissão específica
        if action in permissions:
            return True
        
        # Admin tem acesso total
        if 'admin' in permissions:
            return True
        
        # Verificar permissões baseadas em recurso
        if resource.startswith('public/') and 'read' in permissions:
            return True
        
        return False
    
    async def perform_security_scan(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza varredura de segurança"""
        try:
            scan_type = request_data.get('scan_type', 'comprehensive')
            target = request_data.get('target', 'system')
            
            logger.info(f"🔍 Iniciando scan de segurança: {scan_type} em {target}")
            
            scan_results = {
                'scan_id': f"scan_{int(time.time())}",
                'scan_type': scan_type,
                'target': target,
                'started_at': datetime.now().isoformat(),
                'vulnerabilities': [],
                'threats': [],
                'recommendations': []
            }
            
            if scan_type in ['comprehensive', 'vulnerability']:
                vulnerabilities = await self._scan_vulnerabilities()
                scan_results['vulnerabilities'] = vulnerabilities
            
            if scan_type in ['comprehensive', 'malware']:
                malware = await self._scan_malware()
                scan_results['threats'].extend(malware)
            
            if scan_type in ['comprehensive', 'network']:
                network_threats = await self._scan_network_security()
                scan_results['threats'].extend(network_threats)
            
            # Gerar recomendações
            scan_results['recommendations'] = self._generate_security_recommendations(scan_results)
            
            scan_results['completed_at'] = datetime.now().isoformat()
            scan_results['status'] = 'completed'
            
            self.security_metrics['security_scans_performed'] += 1
            
            return scan_results
            
        except Exception as e:
            logger.error(f"❌ Erro no scan de segurança: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _scan_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Escaneia vulnerabilidades conhecidas"""
        vulnerabilities = []
        
        for vuln_id, vuln_data in self.vulnerability_db.items():
            # Simular detecção de vulnerabilidade
            if self._check_vulnerability_indicators(vuln_data['indicators']):
                vulnerabilities.append({
                    'cve_id': vuln_id,
                    'severity': vuln_data['severity'].value,
                    'description': vuln_data['description'],
                    'detected_at': datetime.now().isoformat(),
                    'status': 'detected'
                })
                
                self.security_metrics['vulnerabilities_found'] += 1
        
        return vulnerabilities
    
    def _check_vulnerability_indicators(self, indicators: List[str]) -> bool:
        """Verifica indicadores de vulnerabilidade"""
        # Simulação - em produção faria verificação real
        import random
        return random.random() < 0.1  # 10% chance de detecção
    
    async def _scan_malware(self) -> List[Dict[str, Any]]:
        """Escaneia por malware"""
        detected_malware = []
        
        # Simular scan de arquivos
        for signature in self.malware_signatures:
            if self._check_malware_signature(signature):
                detected_malware.append({
                    'name': signature['name'],
                    'severity': signature['severity'].value,
                    'detected_at': datetime.now().isoformat(),
                    'action_taken': 'quarantined'
                })
                
                self.security_metrics['malware_detected'] += 1
        
        return detected_malware
    
    def _check_malware_signature(self, signature: Dict[str, Any]) -> bool:
        """Verifica assinatura de malware"""
        # Simulação
        import random
        return random.random() < 0.05  # 5% chance de detecção
    
    async def _scan_network_security(self) -> List[Dict[str, Any]]:
        """Escaneia segurança da rede"""
        network_threats = []
        
        # Verificar conexões suspeitas
        suspicious_connections = await self._detect_suspicious_connections()
        
        for connection in suspicious_connections:
            network_threats.append({
                'type': 'suspicious_connection',
                'source': connection['source'],
                'destination': connection['destination'],
                'threat_level': connection['threat_level'],
                'detected_at': datetime.now().isoformat()
            })
        
        return network_threats
    
    async def _detect_suspicious_connections(self) -> List[Dict[str, Any]]:
        """Detecta conexões suspeitas"""
        # Simulação de detecção de conexões
        suspicious = []
        
        # Em produção, analisaria netstat, logs de firewall, etc.
        known_bad_ips = ['192.168.1.100', '10.0.0.50']
        
        for bad_ip in known_bad_ips:
            if self._is_ip_active(bad_ip):
                suspicious.append({
                    'source': bad_ip,
                    'destination': 'localhost',
                    'threat_level': ThreatLevel.HIGH.value
                })
        
        return suspicious
    
    def _is_ip_active(self, ip: str) -> bool:
        """Verifica se IP está ativo"""
        # Simulação
        import random
        return random.random() < 0.2
    
    async def analyze_threat(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa ameaça específica"""
        try:
            threat_data = request_data.get('threat_data')
            context = request_data.get('context', {})
            
            analysis = {
                'threat_id': f"threat_{int(time.time())}",
                'analyzed_at': datetime.now().isoformat(),
                'threat_level': ThreatLevel.MEDIUM.value,
                'indicators': [],
                'attack_vectors': [],
                'recommendations': []
            }
            
            # Analisar contra padrões conhecidos
            for pattern_type, patterns in self.threat_patterns.items():
                if self._matches_threat_pattern(threat_data, patterns):
                    analysis['indicators'].append({
                        'type': pattern_type,
                        'confidence': 0.8,
                        'description': f'Corresponde ao padrão {pattern_type}'
                    })
                    
                    if pattern_type in ['sql_injection', 'command_injection']:
                        analysis['threat_level'] = ThreatLevel.HIGH.value
            
            # Determinar vetores de ataque
            analysis['attack_vectors'] = self._identify_attack_vectors(threat_data, analysis['indicators'])
            
            # Gerar recomendações
            analysis['recommendations'] = self._generate_threat_recommendations(analysis)
            
            return {
                'status': 'completed',
                'analysis': analysis
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise de ameaça: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _matches_threat_pattern(self, data: str, patterns: List) -> bool:
        """Verifica se dados correspondem a padrão de ameaça"""
        if isinstance(data, dict):
            data = json.dumps(data)
        elif not isinstance(data, str):
            data = str(data)
        
        for pattern in patterns:
            if pattern.search(data):
                return True
        
        return False
    
    def _identify_attack_vectors(self, threat_data: Any, indicators: List[Dict]) -> List[str]:
        """Identifica possíveis vetores de ataque"""
        vectors = []
        
        for indicator in indicators:
            indicator_type = indicator['type']
            
            if indicator_type == 'sql_injection':
                vectors.extend(['database', 'web_application', 'api'])
            elif indicator_type == 'xss':
                vectors.extend(['web_browser', 'client_side', 'frontend'])
            elif indicator_type == 'command_injection':
                vectors.extend(['system_shell', 'server_side', 'backend'])
            elif indicator_type == 'path_traversal':
                vectors.extend(['file_system', 'directory_access'])
        
        return list(set(vectors))
    
    def _generate_threat_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Gera recomendações baseadas na análise"""
        recommendations = []
        
        threat_level = analysis['threat_level']
        indicators = analysis['indicators']
        
        if threat_level == ThreatLevel.CRITICAL.value:
            recommendations.append("AÇÃO IMEDIATA: Isolar sistema afetado")
            recommendations.append("Ativar protocolo de resposta a incidentes")
        
        for indicator in indicators:
            indicator_type = indicator['type']
            
            if indicator_type == 'sql_injection':
                recommendations.append("Implementar prepared statements")
                recommendations.append("Validar todas as entradas do usuário")
            elif indicator_type == 'xss':
                recommendations.append("Sanitizar saídas HTML")
                recommendations.append("Implementar Content Security Policy")
        
        if not recommendations:
            recommendations.append("Continuar monitoramento")
        
        return recommendations
    
    async def encrypt_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criptografa dados sensíveis"""
        try:
            data = request_data.get('data')
            encryption_type = request_data.get('type', 'AES')
            
            if isinstance(data, dict):
                data = json.dumps(data)
            elif not isinstance(data, str):
                data = str(data)
            
            # Simulação de criptografia (em produção usaria cryptography library)
            encrypted_data = self._simulate_encryption(data)
            
            return {
                'status': 'success',
                'encrypted_data': encrypted_data,
                'encryption_type': encryption_type,
                'key_id': 'key_001'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na criptografia: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _simulate_encryption(self, data: str) -> str:
        """Simula criptografia de dados"""
        # Em produção, usaria AES/Fernet real
        import base64
        encoded = base64.b64encode(data.encode()).decode()
        return f"ENC:{encoded}"
    
    async def decrypt_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Descriptografa dados"""
        try:
            encrypted_data = request_data.get('encrypted_data')
            key_id = request_data.get('key_id')
            
            # Verificar se é dados criptografados válidos
            if not encrypted_data.startswith('ENC:'):
                return {'status': 'error', 'message': 'Dados não criptografados'}
            
            decrypted_data = self._simulate_decryption(encrypted_data)
            
            return {
                'status': 'success',
                'decrypted_data': decrypted_data
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na descriptografia: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _simulate_decryption(self, encrypted_data: str) -> str:
        """Simula descriptografia de dados"""
        import base64
        encoded = encrypted_data[4:]  # Remove 'ENC:'
        return base64.b64decode(encoded).decode()
    
    async def generate_security_report(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera relatório de segurança"""
        try:
            period = request_data.get('period', 'last_24h')
            
            # Determinar período
            now = datetime.now()
            if period == 'last_24h':
                start_time = now - timedelta(hours=24)
            elif period == 'last_week':
                start_time = now - timedelta(days=7)
            else:
                start_time = now - timedelta(hours=1)
            
            # Filtrar eventos do período
            period_events = [
                event for event in self.security_events
                if event.timestamp >= start_time
            ]
            
            # Analisar eventos
            event_summary = defaultdict(int)
            threat_levels = defaultdict(int)
            
            for event in period_events:
                event_summary[event.event_type.value] += 1
                threat_levels[event.threat_level.value] += 1
            
            report = {
                'report_id': f"security_report_{int(time.time())}",
                'period': period,
                'generated_at': now.isoformat(),
                'summary': {
                    'total_events': len(period_events),
                    'events_by_type': dict(event_summary),
                    'threats_by_level': dict(threat_levels),
                    'blocked_ips': len(self.blocked_ips),
                    'active_tokens': len(self.access_tokens)
                },
                'metrics': self.security_metrics.copy(),
                'top_threats': self._get_top_threats(period_events),
                'recommendations': self._generate_security_recommendations({'events': period_events}),
                'system_status': self._get_security_status()
            }
            
            return {
                'status': 'completed',
                'report': report
            }
            
        except Exception as e:
            logger.error(f"❌ Erro gerando relatório: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _get_top_threats(self, events: List[SecurityEvent]) -> List[Dict[str, Any]]:
        """Obtém principais ameaças do período"""
        threat_counts = defaultdict(int)
        
        for event in events:
            if event.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
                threat_counts[event.event_type.value] += 1
        
        # Ordenar por frequência
        sorted_threats = sorted(threat_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {'threat_type': threat, 'count': count}
            for threat, count in sorted_threats[:5]
        ]
    
    def _generate_security_recommendations(self, scan_data: Dict[str, Any]) -> List[str]:
        """Gera recomendações de segurança"""
        recommendations = []
        
        # Baseado em vulnerabilidades
        if 'vulnerabilities' in scan_data:
            vuln_count = len(scan_data['vulnerabilities'])
            if vuln_count > 5:
                recommendations.append("Priorize correção de vulnerabilidades críticas")
            elif vuln_count > 0:
                recommendations.append("Agende correção de vulnerabilidades detectadas")
        
        # Baseado em eventos
        if 'events' in scan_data:
            events = scan_data['events']
            auth_failures = sum(1 for e in events if e.event_type == SecurityEventType.AUTHENTICATION_FAILURE)
            
            if auth_failures > 10:
                recommendations.append("Implementar bloqueio automático por múltiplas falhas de autenticação")
            
            intrusion_attempts = sum(1 for e in events if e.event_type == SecurityEventType.INTRUSION_ATTEMPT)
            if intrusion_attempts > 5:
                recommendations.append("Revisar e fortalecer sistemas de detecção de intrusão")
        
        # Baseado em métricas
        if self.security_metrics['malware_detected'] > 0:
            recommendations.append("Realizar scan completo de malware em todo o sistema")
        
        if len(self.blocked_ips) > 50:
            recommendations.append("Revisar lista de IPs bloqueados e implementar whitelist")
        
        # Recomendações gerais
        recommendations.extend([
            "Manter sistemas atualizados com patches de segurança",
            "Realizar backup regular de dados críticos",
            "Treinar usuários sobre segurança cibernética"
        ])
        
        return recommendations[:10]  # Limitar a 10 recomendações
    
    def _get_security_status(self) -> str:
        """Obtém status geral de segurança"""
        critical_events = sum(
            1 for event in self.security_events
            if event.threat_level == ThreatLevel.CRITICAL and not event.resolved
        )
        
        high_events = sum(
            1 for event in self.security_events
            if event.threat_level == ThreatLevel.HIGH and not event.resolved
        )
        
        if critical_events > 0:
            return "CRÍTICO"
        elif high_events > 5:
            return "ALTO RISCO"
        elif high_events > 0:
            return "ATENÇÃO"
        else:
            return "SEGURO"
    
    async def _log_security_event(self, event_type: SecurityEventType, threat_level: ThreatLevel, 
                                source_ip: str, description: str, metadata: Dict[str, Any] = None):
        """Registra evento de segurança"""
        event = SecurityEvent(
            event_id=f"sec_{int(time.time())}_{len(self.security_events)}",
            event_type=event_type,
            threat_level=threat_level,
            source_ip=source_ip,
            user_agent=metadata.get('user_agent') if metadata else None,
            description=description,
            affected_resource=metadata.get('resource', 'system') if metadata else 'system',
            metadata=metadata or {}
        )
        
        self.security_events.append(event)
        
        # Log crítico
        if threat_level in [ThreatLevel.CRITICAL, ThreatLevel.HIGH]:
            logger.warning(f"🚨 ALERTA DE SEGURANÇA: {description} - Nível: {threat_level.value}")
            
            # Notificar outros agentes
            await self._send_security_alert(event)
    
    async def _send_security_alert(self, event: SecurityEvent):
        """Envia alerta de segurança para outros agentes"""
        alert = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.CRITICAL if event.threat_level == ThreatLevel.CRITICAL else Priority.HIGH,
            content={
                'notification_type': 'security_alert',
                'event': {
                    'id': event.event_id,
                    'type': event.event_type.value,
                    'threat_level': event.threat_level.value,
                    'description': event.description,
                    'source_ip': event.source_ip,
                    'timestamp': event.timestamp.isoformat()
                }
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(alert)
    
    async def _monitor_network_connections(self):
        """Monitora conexões de rede"""
        # Simulação de monitoramento
        pass
    
    async def _analyze_suspicious_activity(self):
        """Analisa atividade suspeita"""
        # Verificar IPs com muitas tentativas
        for ip, count in list(self.suspicious_ips.items()):
            if count > 20:  # Limite de atividade suspeita
                self.blocked_ips.add(ip)
                await self._log_security_event(
                    SecurityEventType.SUSPICIOUS_ACTIVITY,
                    ThreatLevel.HIGH,
                    ip,
                    f"IP bloqueado por atividade suspeita: {count} eventos"
                )
                del self.suspicious_ips[ip]
    
    async def _detect_security_anomalies(self) -> List[Dict[str, Any]]:
        """Detecta anomalias de segurança"""
        anomalies = []
        
        # Verificar picos de atividade
        recent_events = [
            e for e in self.security_events
            if (datetime.now() - e.timestamp).seconds < 300  # Últimos 5 minutos
        ]
        
        if len(recent_events) > 50:  # Muitos eventos em pouco tempo
            anomalies.append({
                'type': 'high_activity',
                'description': f'{len(recent_events)} eventos nos últimos 5 minutos',
                'severity': ThreatLevel.MEDIUM.value
            })
        
        return anomalies
    
    async def _handle_security_anomalies(self, anomalies: List[Dict[str, Any]]):
        """Trata anomalias de segurança"""
        for anomaly in anomalies:
            await self._log_security_event(
                SecurityEventType.SUSPICIOUS_ACTIVITY,
                ThreatLevel(anomaly['severity']),
                'system',
                f"Anomalia detectada: {anomaly['description']}"
            )
    
    async def _verify_system_integrity(self):
        """Verifica integridade do sistema"""
        # Simulação de verificação de integridade
        pass
    
    async def _process_vulnerabilities(self, vulnerabilities: List[Dict[str, Any]]):
        """Processa vulnerabilidades encontradas"""
        for vuln in vulnerabilities:
            if vuln['severity'] == ThreatLevel.CRITICAL.value:
                await self._log_security_event(
                    SecurityEventType.DATA_BREACH,  # Seria VULNERABILITY_DETECTED
                    ThreatLevel.CRITICAL,
                    'system',
                    f"Vulnerabilidade crítica: {vuln['cve_id']}"
                )
    
    async def _handle_malware_detection(self, malware_list: List[Dict[str, Any]]):
        """Trata detecção de malware"""
        for malware in malware_list:
            await self._log_security_event(
                SecurityEventType.MALWARE_DETECTED,
                ThreatLevel(malware['severity']),
                'system',
                f"Malware detectado: {malware['name']}"
            )
    
    async def _cleanup_temporary_blocks(self):
        """Remove bloqueios temporários expirados"""
        # Em produção, manteria timestamp dos bloqueios
        pass
    
    async def _cleanup_expired_tokens(self):
        """Remove tokens expirados"""
        now = datetime.now()
        expired_tokens = [
            token_id for token_id, token in self.access_tokens.items()
            if token.expires_at < now
        ]
        
        for token_id in expired_tokens:
            del self.access_tokens[token_id]
    
    async def _handle_suspicious_activity_notification(self, notification_data: Dict[str, Any]):
        """Trata notificação de atividade suspeita"""
        source_ip = notification_data.get('source_ip', 'unknown')
        activity_type = notification_data.get('activity_type', 'unknown')
        
        self.suspicious_ips[source_ip] += 1
        
        await self._log_security_event(
            SecurityEventType.SUSPICIOUS_ACTIVITY,
            ThreatLevel.MEDIUM,
            source_ip,
            f"Atividade suspeita reportada: {activity_type}"
        )
    
    async def _handle_security_alert(self, alert_data: Dict[str, Any]):
        """Trata alerta de segurança"""
        alert_type = alert_data.get('alert_type')
        severity = alert_data.get('severity', 'medium')
        
        if severity == 'critical':
            # Ativar protocolo de resposta a incidentes
            await self._activate_incident_response(alert_data)
    
    async def _activate_incident_response(self, incident_data: Dict[str, Any]):
        """Ativa resposta a incidentes"""
        logger.critical(f"🚨 PROTOCOLO DE INCIDENTE ATIVADO: {incident_data}")
        
        # Notificar todos os agentes críticos
        incident_alert = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="broadcast",
            message_type=MessageType.EMERGENCY,
            priority=Priority.CRITICAL,
            content={
                'emergency_type': 'security_incident',
                'incident_data': incident_data,
                'response_required': True,
                'escalation_level': 'critical'
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(incident_alert)
    
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

def create_security_guardian_agent(message_bus, num_instances=1) -> List[SecurityGuardianAgent]:
    """
    Cria agente Guardian de Segurança Supremo
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente guardian de segurança
    """
    agents = []
    
    try:
        logger.info("🛡️ Criando SecurityGuardianAgent - Proteção Suprema...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "security_guardian_001"
        
        if agent_id not in existing_agents:
            try:
                agent = SecurityGuardianAgent(agent_id, AgentType.GUARD, message_bus)
                
                # Iniciar serviços de segurança
                asyncio.create_task(agent.start_security_services())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado como Guardian Supremo da Segurança")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente Guardian de Segurança criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando SecurityGuardianAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
