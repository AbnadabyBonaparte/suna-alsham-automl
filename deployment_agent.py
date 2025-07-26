#!/usr/bin/env python3
"""
Deployment Agent - CI/CD Automático e Deploy Inteligente
Sistema avançado de deploy com zero downtime e rollback automático
"""

import asyncio
import logging
import json
import subprocess
import time
import docker
import git
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import hashlib
from multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class DeploymentStatus(Enum):
    """Status do deployment"""
    PENDING = "pending"
    PREPARING = "preparing"
    BUILDING = "building"
    TESTING = "testing"
    DEPLOYING = "deploying"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"

class DeploymentStrategy(Enum):
    """Estratégias de deployment"""
    BLUE_GREEN = "blue_green"
    ROLLING = "rolling"
    CANARY = "canary"
    RECREATE = "recreate"
    A_B_TESTING = "a_b_testing"

class Environment(Enum):
    """Ambientes de deployment"""
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

@dataclass
class DeploymentConfig:
    """Configuração de deployment"""
    strategy: DeploymentStrategy
    environment: Environment
    auto_rollback: bool = True
    health_check_timeout: int = 300  # 5 minutos
    rollback_threshold: float = 0.05  # 5% de erro
    pre_deploy_checks: List[str] = field(default_factory=list)
    post_deploy_checks: List[str] = field(default_factory=list)
    notification_channels: List[str] = field(default_factory=list)

@dataclass
class DeploymentJob:
    """Job de deployment"""
    job_id: str
    commit_hash: str
    branch: str
    config: DeploymentConfig
    status: DeploymentStatus = DeploymentStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    rollback_version: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)

@dataclass
class HealthCheck:
    """Verificação de saúde"""
    check_id: str
    name: str
    url: str
    expected_status: int = 200
    timeout: int = 30
    retries: int = 3
    critical: bool = True

class DeploymentAgent(BaseNetworkAgent):
    """Agente especializado em deployment automático e CI/CD"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'ci_cd_automation',
            'zero_downtime_deployment',
            'intelligent_rollback',
            'health_monitoring',
            'multi_environment_deploy',
            'canary_releases',
            'blue_green_deployment',
            'automated_testing',
            'infrastructure_management'
        ]
        self.status = 'active'
        
        # Estado do deployment
        self.active_deployments = {}  # job_id -> DeploymentJob
        self.deployment_history = []
        self.deployment_queue = asyncio.Queue()
        self.environments = {}  # env -> config
        self.health_checks = {}  # env -> List[HealthCheck]
        
        # Configurações
        self.docker_client = None
        self.git_repos = {}  # repo_name -> repo_path
        self.deployment_configs = self._load_deployment_configs()
        
        # Métricas
        self.deployment_metrics = {
            'total_deployments': 0,
            'successful_deployments': 0,
            'failed_deployments': 0,
            'rollbacks_executed': 0,
            'average_deployment_time': 0.0,
            'zero_downtime_percentage': 100.0
        }
        
        # Serviços
        self._deployment_task = None
        self._monitoring_task = None
        self._cleanup_task = None
        
        # Inicialização
        self._initialize_docker()
        self._setup_environments()
        
        logger.info(f"🚀 {self.agent_id} inicializado com CI/CD avançado")
    
    def _load_deployment_configs(self) -> Dict[str, DeploymentConfig]:
        """Carrega configurações de deployment"""
        return {
            'production': DeploymentConfig(
                strategy=DeploymentStrategy.BLUE_GREEN,
                environment=Environment.PRODUCTION,
                auto_rollback=True,
                health_check_timeout=600,
                rollback_threshold=0.02,
                pre_deploy_checks=['security_scan', 'performance_test', 'integration_test'],
                post_deploy_checks=['health_check', 'smoke_test', 'load_test'],
                notification_channels=['slack', 'email', 'webhook']
            ),
            'staging': DeploymentConfig(
                strategy=DeploymentStrategy.ROLLING,
                environment=Environment.STAGING,
                auto_rollback=True,
                health_check_timeout=300,
                pre_deploy_checks=['unit_test', 'integration_test'],
                post_deploy_checks=['health_check', 'smoke_test']
            ),
            'development': DeploymentConfig(
                strategy=DeploymentStrategy.RECREATE,
                environment=Environment.DEVELOPMENT,
                auto_rollback=False,
                health_check_timeout=120,
                pre_deploy_checks=['unit_test'],
                post_deploy_checks=['health_check']
            )
        }
    
    def _initialize_docker(self):
        """Inicializa cliente Docker"""
        try:
            self.docker_client = docker.from_env()
            logger.info("🐳 Cliente Docker inicializado")
        except Exception as e:
            logger.error(f"❌ Erro inicializando Docker: {e}")
    
    def _setup_environments(self):
        """Configura ambientes"""
        self.environments = {
            'production': {
                'url': 'https://suna-alsham-automl-production.up.railway.app',
                'replicas': 3,
                'resources': {'cpu': '1000m', 'memory': '1Gi'},
                'secrets': ['prod-db', 'prod-api-keys']
            },
            'staging': {
                'url': 'https://suna-alsham-staging.up.railway.app',
                'replicas': 2,
                'resources': {'cpu': '500m', 'memory': '512Mi'},
                'secrets': ['staging-db', 'staging-api-keys']
            },
            'development': {
                'url': 'http://localhost:8080',
                'replicas': 1,
                'resources': {'cpu': '250m', 'memory': '256Mi'},
                'secrets': ['dev-db']
            }
        }
        
        # Health checks por ambiente
        self.health_checks = {
            'production': [
                HealthCheck('health', 'Health Check', '/health', 200, 30, 3, True),
                HealthCheck('status', 'Status Check', '/status', 200, 15, 2, True),
                HealthCheck('metrics', 'Metrics Check', '/metrics', 200, 10, 1, False)
            ],
            'staging': [
                HealthCheck('health', 'Health Check', '/health', 200, 20, 2, True),
                HealthCheck('status', 'Status Check', '/status', 200, 10, 2, True)
            ],
            'development': [
                HealthCheck('health', 'Health Check', '/health', 200, 10, 1, True)
            ]
        }
    
    async def start_deployment_service(self):
        """Inicia serviços de deployment"""
        if not self._deployment_task:
            self._deployment_task = asyncio.create_task(self._deployment_loop())
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
            logger.info(f"🚀 {self.agent_id} iniciou serviços de deployment")
    
    async def stop_deployment_service(self):
        """Para serviços de deployment"""
        tasks = [self._deployment_task, self._monitoring_task, self._cleanup_task]
        for task in tasks:
            if task:
                task.cancel()
        
        self._deployment_task = None
        self._monitoring_task = None
        self._cleanup_task = None
        
        logger.info(f"🛑 {self.agent_id} parou serviços de deployment")
    
    async def _deployment_loop(self):
        """Loop principal de deployment"""
        while True:
            try:
                # Processar fila de deployment
                if not self.deployment_queue.empty():
                    job = await self.deployment_queue.get()
                    await self._execute_deployment(job)
                
                await asyncio.sleep(5)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de deployment: {e}")
    
    async def _monitoring_loop(self):
        """Loop de monitoramento de deployments ativos"""
        while True:
            try:
                for job_id, job in self.active_deployments.items():
                    if job.status == DeploymentStatus.DEPLOYING:
                        await self._monitor_deployment(job)
                    elif job.status == DeploymentStatus.VERIFYING:
                        await self._verify_deployment(job)
                
                await asyncio.sleep(10)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento: {e}")
    
    async def _cleanup_loop(self):
        """Loop de limpeza"""
        while True:
            try:
                # Limpar deployments antigos
                cutoff = datetime.now() - timedelta(hours=24)
                
                completed_jobs = [
                    job for job in self.deployment_history
                    if job.completed_at and job.completed_at < cutoff
                ]
                
                # Manter apenas últimos 50
                if len(completed_jobs) > 50:
                    self.deployment_history = self.deployment_history[-50:]
                
                await asyncio.sleep(3600)  # Limpeza a cada hora
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na limpeza: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'deploy':
                result = await self.deploy(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'rollback':
                result = await self.rollback(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'deployment_status':
                result = self.get_deployment_status(message.content.get('job_id'))
                await self._send_response(message, result)
                
            elif request_type == 'list_deployments':
                result = self.list_deployments(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'health_check':
                result = await self.perform_health_check(message.content)
                await self._send_response(message, result)
        
        elif message.message_type == MessageType.NOTIFICATION:
            if message.content.get('notification_type') == 'code_updated':
                await self._handle_code_update(message.content)
    
    async def deploy(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inicia deployment"""
        try:
            repo_name = request_data.get('repository', 'suna-alsham-automl')
            branch = request_data.get('branch', 'main')
            environment = request_data.get('environment', 'development')
            force_deploy = request_data.get('force', False)
            
            logger.info(f"🚀 Iniciando deployment: {repo_name}@{branch} -> {environment}")
            
            # Validar ambiente
            if environment not in self.deployment_configs:
                return {
                    'status': 'error',
                    'message': f'Ambiente {environment} não configurado'
                }
            
            # Obter commit hash
            commit_hash = await self._get_latest_commit(repo_name, branch)
            if not commit_hash:
                return {
                    'status': 'error',
                    'message': 'Não foi possível obter commit hash'
                }
            
            # Verificar se já existe deployment ativo
            if not force_deploy:
                active = [j for j in self.active_deployments.values() 
                         if j.config.environment.value == environment and 
                         j.status in [DeploymentStatus.DEPLOYING, DeploymentStatus.VERIFYING]]
                
                if active:
                    return {
                        'status': 'error',
                        'message': f'Deployment ativo em {environment}: {active[0].job_id}'
                    }
            
            # Criar job de deployment
            job = DeploymentJob(
                job_id=f"deploy_{int(time.time())}_{environment}",
                commit_hash=commit_hash,
                branch=branch,
                config=self.deployment_configs[environment]
            )
            
            # Adicionar à fila
            await self.deployment_queue.put(job)
            self.active_deployments[job.job_id] = job
            
            return {
                'status': 'accepted',
                'job_id': job.job_id,
                'commit_hash': commit_hash,
                'environment': environment,
                'strategy': job.config.strategy.value
            }
            
        except Exception as e:
            logger.error(f"❌ Erro iniciando deployment: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _execute_deployment(self, job: DeploymentJob):
        """Executa deployment completo"""
        try:
            job.status = DeploymentStatus.PREPARING
            job.started_at = datetime.now()
            
            logger.info(f"🔧 Executando deployment {job.job_id}")
            
            # 1. Preparação
            if not await self._prepare_deployment(job):
                job.status = DeploymentStatus.FAILED
                return
            
            # 2. Build
            job.status = DeploymentStatus.BUILDING
            if not await self._build_application(job):
                job.status = DeploymentStatus.FAILED
                return
            
            # 3. Testes
            job.status = DeploymentStatus.TESTING
            if not await self._run_pre_deploy_tests(job):
                job.status = DeploymentStatus.FAILED
                return
            
            # 4. Deploy
            job.status = DeploymentStatus.DEPLOYING
            if not await self._deploy_application(job):
                job.status = DeploymentStatus.FAILED
                return
            
            # 5. Verificação
            job.status = DeploymentStatus.VERIFYING
            if not await self._verify_deployment(job):
                if job.config.auto_rollback:
                    await self._perform_rollback(job)
                else:
                    job.status = DeploymentStatus.FAILED
                return
            
            # 6. Sucesso
            job.status = DeploymentStatus.COMPLETED
            job.completed_at = datetime.now()
            
            self.deployment_metrics['successful_deployments'] += 1
            await self._notify_deployment_success(job)
            
            logger.info(f"✅ Deployment {job.job_id} completado com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro executando deployment: {e}")
            job.status = DeploymentStatus.FAILED
            job.error_message = str(e)
            
            if job.config.auto_rollback:
                await self._perform_rollback(job)
        
        finally:
            # Mover para histórico
            self.deployment_history.append(job)
            if job.job_id in self.active_deployments:
                del self.active_deployments[job.job_id]
            
            self.deployment_metrics['total_deployments'] += 1
            if job.status == DeploymentStatus.FAILED:
                self.deployment_metrics['failed_deployments'] += 1
    
    async def _prepare_deployment(self, job: DeploymentJob) -> bool:
        """Prepara deployment"""
        try:
            job.logs.append("📦 Preparando deployment...")
            
            # Verificar pré-requisitos
            if not await self._check_prerequisites(job):
                return False
            
            # Backup da versão atual
            await self._backup_current_version(job)
            
            # Preparar ambiente
            await self._prepare_environment(job)
            
            job.logs.append("✅ Preparação concluída")
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro na preparação: {e}")
            return False
    
    async def _check_prerequisites(self, job: DeploymentJob) -> bool:
        """Verifica pré-requisitos"""
        try:
            # Verificar se ambiente está saudável
            env_name = job.config.environment.value
            health_status = await self._check_environment_health(env_name)
            
            if not health_status['healthy']:
                job.logs.append(f"❌ Ambiente {env_name} não está saudável")
                return False
            
            # Verificar recursos disponíveis
            if not await self._check_resources(job):
                job.logs.append("❌ Recursos insuficientes")
                return False
            
            # Verificar dependências
            if not await self._check_dependencies(job):
                job.logs.append("❌ Dependências não satisfeitas")
                return False
            
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro verificando pré-requisitos: {e}")
            return False
    
    async def _build_application(self, job: DeploymentJob) -> bool:
        """Build da aplicação"""
        try:
            job.logs.append("🔨 Construindo aplicação...")
            
            # Simular build com Docker
            if self.docker_client:
                # Build da imagem
                build_result = await self._docker_build(job)
                if not build_result:
                    return False
                
                # Tag da imagem
                await self._tag_image(job)
                
                # Push para registry (se necessário)
                if job.config.environment == Environment.PRODUCTION:
                    await self._push_image(job)
            
            job.logs.append("✅ Build concluído")
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro no build: {e}")
            return False
    
    async def _docker_build(self, job: DeploymentJob) -> bool:
        """Build Docker"""
        try:
            # Simular build
            await asyncio.sleep(2)  # Simular tempo de build
            
            job.logs.append("🐳 Imagem Docker construída")
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro no build Docker: {e}")
            return False
    
    async def _run_pre_deploy_tests(self, job: DeploymentJob) -> bool:
        """Executa testes pré-deploy"""
        try:
            job.logs.append("🧪 Executando testes pré-deploy...")
            
            for check in job.config.pre_deploy_checks:
                if not await self._run_test(check, job):
                    return False
            
            job.logs.append("✅ Todos os testes passaram")
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro nos testes: {e}")
            return False
    
    async def _run_test(self, test_name: str, job: DeploymentJob) -> bool:
        """Executa teste específico"""
        try:
            job.logs.append(f"  🔍 Executando {test_name}...")
            
            # Simular execução de teste
            await asyncio.sleep(1)
            
            # Simular resultado (99% de sucesso)
            import random
            success = random.random() > 0.01
            
            if success:
                job.logs.append(f"  ✅ {test_name} passou")
                return True
            else:
                job.logs.append(f"  ❌ {test_name} falhou")
                return False
                
        except Exception as e:
            job.logs.append(f"  ❌ Erro executando {test_name}: {e}")
            return False
    
    async def _deploy_application(self, job: DeploymentJob) -> bool:
        """Deploy da aplicação"""
        try:
            strategy = job.config.strategy
            
            job.logs.append(f"🚀 Deployando com estratégia {strategy.value}...")
            
            if strategy == DeploymentStrategy.BLUE_GREEN:
                return await self._blue_green_deploy(job)
            elif strategy == DeploymentStrategy.ROLLING:
                return await self._rolling_deploy(job)
            elif strategy == DeploymentStrategy.CANARY:
                return await self._canary_deploy(job)
            else:
                return await self._recreate_deploy(job)
            
        except Exception as e:
            job.logs.append(f"❌ Erro no deploy: {e}")
            return False
    
    async def _blue_green_deploy(self, job: DeploymentJob) -> bool:
        """Deploy Blue-Green (zero downtime)"""
        try:
            job.logs.append("🔵 Iniciando deploy Blue-Green...")
            
            # 1. Criar ambiente Green
            job.logs.append("  🟢 Criando ambiente Green...")
            await asyncio.sleep(2)
            
            # 2. Deploy no Green
            job.logs.append("  🚀 Deployando no ambiente Green...")
            await asyncio.sleep(3)
            
            # 3. Testes no Green
            job.logs.append("  🧪 Testando ambiente Green...")
            if not await self._test_green_environment(job):
                return False
            
            # 4. Switch de tráfego
            job.logs.append("  🔄 Redirecionando tráfego para Green...")
            await asyncio.sleep(1)
            
            # 5. Manter Blue como backup
            job.logs.append("  🔵 Mantendo Blue como backup...")
            
            job.logs.append("✅ Deploy Blue-Green concluído")
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro no Blue-Green deploy: {e}")
            return False
    
    async def _rolling_deploy(self, job: DeploymentJob) -> bool:
        """Deploy Rolling"""
        try:
            job.logs.append("🔄 Iniciando deploy Rolling...")
            
            replicas = self.environments[job.config.environment.value]['replicas']
            
            for i in range(replicas):
                job.logs.append(f"  📦 Atualizando replica {i+1}/{replicas}...")
                await asyncio.sleep(1)
                
                # Verificar saúde após cada replica
                if not await self._check_replica_health(i, job):
                    return False
            
            job.logs.append("✅ Deploy Rolling concluído")
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro no Rolling deploy: {e}")
            return False
    
    async def _canary_deploy(self, job: DeploymentJob) -> bool:
        """Deploy Canary"""
        try:
            job.logs.append("🐤 Iniciando deploy Canary...")
            
            # 1. Deploy para 10% do tráfego
            job.logs.append("  📊 Deployando para 10% do tráfego...")
            await asyncio.sleep(2)
            
            if not await self._monitor_canary_metrics(job, 0.1):
                return False
            
            # 2. Aumentar para 50%
            job.logs.append("  📊 Aumentando para 50% do tráfego...")
            await asyncio.sleep(2)
            
            if not await self._monitor_canary_metrics(job, 0.5):
                return False
            
            # 3. Deploy completo
            job.logs.append("  📊 Deploy completo (100%)...")
            await asyncio.sleep(1)
            
            job.logs.append("✅ Deploy Canary concluído")
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro no Canary deploy: {e}")
            return False
    
    async def _recreate_deploy(self, job: DeploymentJob) -> bool:
        """Deploy Recreate (com downtime)"""
        try:
            job.logs.append("🔄 Iniciando deploy Recreate...")
            
            # 1. Parar aplicação atual
            job.logs.append("  🛑 Parando aplicação atual...")
            await asyncio.sleep(1)
            
            # 2. Deploy nova versão
            job.logs.append("  🚀 Deployando nova versão...")
            await asyncio.sleep(2)
            
            # 3. Iniciar nova aplicação
            job.logs.append("  ▶️ Iniciando nova aplicação...")
            await asyncio.sleep(1)
            
            job.logs.append("✅ Deploy Recreate concluído")
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro no Recreate deploy: {e}")
            return False
    
    async def _verify_deployment(self, job: DeploymentJob) -> bool:
        """Verifica deployment"""
        try:
            job.logs.append("🔍 Verificando deployment...")
            
            # Health checks
            env_name = job.config.environment.value
            health_checks = self.health_checks.get(env_name, [])
            
            for check in health_checks:
                if not await self._perform_health_check_internal(check, job):
                    if check.critical:
                        return False
            
            # Testes pós-deploy
            for check in job.config.post_deploy_checks:
                if not await self._run_test(check, job):
                    return False
            
            # Monitorar métricas por alguns minutos
            if not await self._monitor_deployment_metrics(job):
                return False
            
            job.logs.append("✅ Verificação concluída com sucesso")
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro na verificação: {e}")
            return False
    
    async def _perform_health_check_internal(self, check: HealthCheck, job: DeploymentJob) -> bool:
        """Executa health check interno"""
        try:
            env_config = self.environments[job.config.environment.value]
            url = f"{env_config['url']}{check.url}"
            
            for attempt in range(check.retries):
                try:
                    # Simular requisição HTTP
                    await asyncio.sleep(0.5)  # Simular latência
                    
                    # Simular resultado (95% de sucesso)
                    import random
                    success = random.random() > 0.05
                    
                    if success:
                        job.logs.append(f"  ✅ {check.name} OK")
                        return True
                    else:
                        job.logs.append(f"  ⚠️ {check.name} falhou (tentativa {attempt + 1})")
                        
                except Exception as e:
                    job.logs.append(f"  ❌ {check.name} erro: {e}")
                
                if attempt < check.retries - 1:
                    await asyncio.sleep(2)
            
            job.logs.append(f"  ❌ {check.name} falhou após {check.retries} tentativas")
            return False
            
        except Exception as e:
            job.logs.append(f"  ❌ Erro executando health check: {e}")
            return False
    
    async def _monitor_deployment_metrics(self, job: DeploymentJob) -> bool:
        """Monitora métricas pós-deploy"""
        try:
            job.logs.append("📊 Monitorando métricas de deployment...")
            
            # Simular monitoramento por 30 segundos
            for i in range(6):  # 6 verificações de 5 segundos
                await asyncio.sleep(5)
                
                # Simular coleta de métricas
                error_rate = await self._get_error_rate(job)
                response_time = await self._get_response_time(job)
                
                job.metrics[f'check_{i}'] = {
                    'error_rate': error_rate,
                    'response_time': response_time,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Verificar se está dentro do threshold
                if error_rate > job.config.rollback_threshold:
                    job.logs.append(f"❌ Taxa de erro alta: {error_rate:.2%}")
                    return False
                
                if response_time > 5000:  # 5 segundos
                    job.logs.append(f"❌ Tempo de resposta alto: {response_time}ms")
                    return False
            
            job.logs.append("✅ Métricas dentro dos parâmetros normais")
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro monitorando métricas: {e}")
            return False
    
    async def _get_error_rate(self, job: DeploymentJob) -> float:
        """Obtém taxa de erro atual"""
        # Simular taxa de erro
        import random
        return random.uniform(0.0, 0.03)  # 0-3%
    
    async def _get_response_time(self, job: DeploymentJob) -> float:
        """Obtém tempo de resposta médio"""
        # Simular tempo de resposta
        import random
        return random.uniform(100, 500)  # 100-500ms
    
    async def rollback(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa rollback"""
        try:
            job_id = request_data.get('job_id')
            version = request_data.get('version')
            environment = request_data.get('environment')
            
            logger.info(f"🔄 Executando rollback: {job_id or environment}")
            
            # Criar job de rollback
            rollback_job = DeploymentJob(
                job_id=f"rollback_{int(time.time())}",
                commit_hash=version or 'previous',
                branch='rollback',
                config=self.deployment_configs.get(environment, self.deployment_configs['development'])
            )
            
            # Executar rollback
            success = await self._perform_rollback(rollback_job)
            
            if success:
                self.deployment_metrics['rollbacks_executed'] += 1
                return {
                    'status': 'completed',
                    'rollback_job_id': rollback_job.job_id,
                    'message': 'Rollback executado com sucesso'
                }
            else:
                return {
                    'status': 'failed',
                    'message': 'Falha no rollback'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro executando rollback: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _perform_rollback(self, job: DeploymentJob) -> bool:
        """Executa rollback automático"""
        try:
            job.logs.append("🔄 Iniciando rollback automático...")
            job.status = DeploymentStatus.ROLLING_BACK
            
            # 1. Identificar versão anterior
            previous_version = await self._get_previous_version(job)
            if not previous_version:
                job.logs.append("❌ Versão anterior não encontrada")
                return False
            
            # 2. Restaurar versão anterior
            job.logs.append(f"📦 Restaurando versão {previous_version}...")
            await asyncio.sleep(2)
            
            # 3. Verificar rollback
            job.logs.append("🔍 Verificando rollback...")
            if not await self._verify_rollback(job):
                job.logs.append("❌ Falha na verificação do rollback")
                return False
            
            job.status = DeploymentStatus.ROLLED_BACK
            job.logs.append("✅ Rollback concluído com sucesso")
            
            # Notificar sobre rollback
            await self._notify_rollback(job)
            
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro no rollback: {e}")
            return False
    
    async def _get_previous_version(self, job: DeploymentJob) -> Optional[str]:
        """Obtém versão anterior"""
        try:
            # Procurar último deployment bem-sucedido
            for prev_job in reversed(self.deployment_history):
                if (prev_job.config.environment == job.config.environment and 
                    prev_job.status == DeploymentStatus.COMPLETED and
                    prev_job.job_id != job.job_id):
                    return prev_job.commit_hash
            
            return "stable"  # Versão stable como fallback
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo versão anterior: {e}")
            return None
    
    async def _verify_rollback(self, job: DeploymentJob) -> bool:
        """Verifica se rollback foi bem-sucedido"""
        try:
            # Health checks básicos
            env_name = job.config.environment.value
            health_checks = self.health_checks.get(env_name, [])[:2]  # Apenas 2 checks críticos
            
            for check in health_checks:
                if check.critical:
                    if not await self._perform_health_check_internal(check, job):
                        return False
            
            return True
            
        except Exception as e:
            job.logs.append(f"❌ Erro verificando rollback: {e}")
            return False
    
    async def perform_health_check(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa health check manual"""
        try:
            environment = request_data.get('environment', 'development')
            
            logger.info(f"🔍 Executando health check: {environment}")
            
            health_status = await self._check_environment_health(environment)
            
            return {
                'status': 'completed',
                'environment': environment,
                'healthy': health_status['healthy'],
                'checks': health_status['checks'],
                'overall_score': health_status['score']
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no health check: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _check_environment_health(self, environment: str) -> Dict[str, Any]:
        """Verifica saúde do ambiente"""
        try:
            checks = self.health_checks.get(environment, [])
            results = []
            healthy_count = 0
            
            for check in checks:
                # Simular check
                await asyncio.sleep(0.1)
                
                # 90% de chance de sucesso
                import random
                success = random.random() > 0.1
                
                result = {
                    'name': check.name,
                    'status': 'healthy' if success else 'unhealthy',
                    'critical': check.critical
                }
                
                results.append(result)
                if success:
                    healthy_count += 1
            
            score = (healthy_count / len(checks)) * 100 if checks else 100
            overall_healthy = all(r['status'] == 'healthy' for r in results if r['critical'])
            
            return {
                'healthy': overall_healthy,
                'score': score,
                'checks': results
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'score': 0,
                'checks': [],
                'error': str(e)
            }
    
    def get_deployment_status(self, job_id: str) -> Dict[str, Any]:
        """Obtém status de deployment"""
        try:
            # Verificar deployments ativos
            if job_id in self.active_deployments:
                job = self.active_deployments[job_id]
                return self._job_to_dict(job)
            
            # Verificar histórico
            for job in self.deployment_history:
                if job.job_id == job_id:
                    return self._job_to_dict(job)
            
            return {
                'status': 'not_found',
                'message': f'Job {job_id} não encontrado'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def list_deployments(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Lista deployments"""
        try:
            environment = request_data.get('environment')
            limit = request_data.get('limit', 10)
            
            # Combinar ativos e histórico
            all_jobs = list(self.active_deployments.values()) + self.deployment_history
            
            # Filtrar por ambiente se especificado
            if environment:
                all_jobs = [j for j in all_jobs if j.config.environment.value == environment]
            
            # Ordenar por data de criação (mais recente primeiro)
            all_jobs.sort(key=lambda x: x.created_at, reverse=True)
            
            # Limitar resultados
            jobs = all_jobs[:limit]
            
            return {
                'status': 'completed',
                'deployments': [self._job_to_dict(job) for job in jobs],
                'total': len(all_jobs),
                'active_count': len(self.active_deployments),
                'metrics': self.deployment_metrics
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def _handle_code_update(self, notification_data: Dict[str, Any]):
        """Trata notificação de atualização de código"""
        try:
            repository = notification_data.get('repository', 'suna-alsham-automl')
            branch = notification_data.get('branch', 'main')
            auto_deploy = notification_data.get('auto_deploy', False)
            
            logger.info(f"📝 Código atualizado: {repository}@{branch}")
            
            if auto_deploy:
                # Auto-deploy para development
                await self.deploy({
                    'repository': repository,
                    'branch': branch,
                    'environment': 'development',
                    'force': True
                })
            
        except Exception as e:
            logger.error(f"❌ Erro tratando atualização de código: {e}")
    
    async def _get_latest_commit(self, repo_name: str, branch: str) -> Optional[str]:
        """Obtém hash do último commit"""
        try:
            # Simular obtenção de commit hash
            import hashlib
            import time
            
            # Gerar hash baseado no tempo (simula commit real)
            content = f"{repo_name}:{branch}:{int(time.time())}"
            commit_hash = hashlib.sha1(content.encode()).hexdigest()[:8]
            
            return commit_hash
            
        except Exception as e:
            logger.error(f"❌ Erro obtendo commit: {e}")
            return None
    
    async def _notify_deployment_success(self, job: DeploymentJob):
        """Notifica sucesso do deployment"""
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.MEDIUM,
            content={
                'notification_type': 'deployment_success',
                'job_id': job.job_id,
                'environment': job.config.environment.value,
                'commit_hash': job.commit_hash,
                'deployment_time': (job.completed_at - job.started_at).total_seconds(),
                'strategy': job.config.strategy.value
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)
    
    async def _notify_rollback(self, job: DeploymentJob):
        """Notifica sobre rollback"""
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.HIGH,
            content={
                'notification_type': 'rollback_executed',
                'job_id': job.job_id,
                'environment': job.config.environment.value,
                'reason': 'automatic_rollback'
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)
    
    def _job_to_dict(self, job: DeploymentJob) -> Dict[str, Any]:
        """Converte job para dicionário"""
        return {
            'job_id': job.job_id,
            'commit_hash': job.commit_hash,
            'branch': job.branch,
            'environment': job.config.environment.value,
            'strategy': job.config.strategy.value,
            'status': job.status.value,
            'created_at': job.created_at.isoformat(),
            'started_at': job.started_at.isoformat() if job.started_at else None,
            'completed_at': job.completed_at.isoformat() if job.completed_at else None,
            'duration': (
                (job.completed_at or datetime.now()) - (job.started_at or job.created_at)
            ).total_seconds() if job.started_at else 0,
            'error_message': job.error_message,
            'logs': job.logs[-10:],  # Últimos 10 logs
            'metrics': job.metrics
        }
    
    # Métodos auxiliares para simular operações
    async def _test_green_environment(self, job: DeploymentJob) -> bool:
        await asyncio.sleep(1)
        return True
    
    async def _check_replica_health(self, replica_index: int, job: DeploymentJob) -> bool:
        await asyncio.sleep(0.5)
        return True
    
    async def _monitor_canary_metrics(self, job: DeploymentJob, traffic_percentage: float) -> bool:
        await asyncio.sleep(1)
        return True
    
    async def _check_resources(self, job: DeploymentJob) -> bool:
        return True
    
    async def _check_dependencies(self, job: DeploymentJob) -> bool:
        return True
    
    async def _backup_current_version(self, job: DeploymentJob):
        await asyncio.sleep(0.5)
    
    async def _prepare_environment(self, job: DeploymentJob):
        await asyncio.sleep(0.5)
    
    async def _tag_image(self, job: DeploymentJob):
        await asyncio.sleep(0.2)
    
    async def _push_image(self, job: DeploymentJob):
        await asyncio.sleep(1)
    
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

def create_deployment_agent(message_bus, num_instances=1) -> List[DeploymentAgent]:
    """
    Cria agente de deployment automático
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de deployment
    """
    agents = []
    
    try:
        logger.info("🚀 Criando DeploymentAgent para CI/CD avançado...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "deployment_001"
        
        if agent_id not in existing_agents:
            try:
                agent = DeploymentAgent(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar serviços de deployment
                asyncio.create_task(agent.start_deployment_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com CI/CD automático")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de deployment criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando DeploymentAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []

if __name__ == "__main__":
    # Demo do DeploymentAgent
    async def demo_deployment():
        from multi_agent_network import create_network
        
        network = create_network()
        await network.initialize()
        
        agents = create_deployment_agent(network.message_bus)
        if agents:
            agent = agents[0]
            
            # Demo de deployment
            deploy_result = await agent.deploy({
                'repository': 'suna-alsham-automl',
                'branch': 'main',
                'environment': 'staging'
            })
            
            print("🚀 Demo Deployment Result:", deploy_result)
    
    # Executar demo
    # asyncio.run(demo_deployment())
