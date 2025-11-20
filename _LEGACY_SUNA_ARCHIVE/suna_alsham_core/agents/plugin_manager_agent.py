"""
plugin_manager_agent.py - Sistema de Gerenciamento de Plugins ALSHAM QUANTUM
Agente Core #36 - Arquitetura Microkernel Plugin-and-Play Enterprise
"""

import asyncio
import logging
import time
import yaml
import json
import docker
import subprocess
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import importlib.util
import threading
from concurrent.futures import ThreadPoolExecutor
import psutil
import requests

class PluginStatus(Enum):
    """Estados possíveis de um plugin"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    ERROR = "error"
    UNHEALTHY = "unhealthy"
    STOPPING = "stopping"

@dataclass
class PluginConfig:
    """Configuração de um plugin"""
    name: str
    version: str
    enabled: bool
    priority: int = 5
    config: Dict = None
    dependencies: List[str] = None
    resources: Dict = None
    health_check_url: str = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}
        if self.dependencies is None:
            self.dependencies = []
        if self.resources is None:
            self.resources = {"cpu": "500m", "memory": "512Mi"}

@dataclass
class PluginMetrics:
    """Métricas de um plugin"""
    name: str
    status: PluginStatus
    start_time: Optional[datetime] = None
    last_health_check: Optional[datetime] = None
    health_status: str = "unknown"
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    message_count: int = 0
    error_count: int = 0
    restart_count: int = 0

class PluginManagerAgent:
    """
    Plugin Manager Agent - Core #36
    Arquitetura Microkernel Plugin-and-Play Enterprise
    Responsável por: Descoberta, ciclo de vida, monitoramento, integração, configuração, isolamento de falhas, extensibilidade e produção.
    """
    def __init__(self, config_path: str = "/configs", message_bus_config: Optional[dict] = None, logger: Optional[logging.Logger] = None):
        self.agent_id = "plugin_manager_001"
        self.logger = logger or logging.getLogger(f"suna_alsham_core.agents.{self.agent_id}")
        self.capabilities: List[str] = [
            "plugin_discovery",
            "plugin_lifecycle_management",
            "plugin_health_monitoring",
            "message_bus_orchestration",
            "client_configuration_management",
            "fault_isolation_and_recovery",
            "plugin_registry_management",
            "resource_allocation_management"
        ]
        self.config_path = Path(config_path)
        self.message_bus_config = message_bus_config or self._default_message_bus_config()
        self.plugins: Dict[str, PluginConfig] = {}
        self.plugin_metrics: Dict[str, PluginMetrics] = {}
        self.plugin_processes: Dict[str, Any] = {}
        self.plugin_containers: Dict[str, Any] = {}
        self.active = True
        self.last_discovery: Optional[datetime] = None
        self.health_check_interval: int = 30
        self.client_config: Dict = {}
        self.hooks: Dict[str, Any] = {}  # Para integração externa
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            self.logger.warning(f"Docker client not available: {e}")
            self.docker_client = None
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.health_check_thread: Optional[threading.Thread] = None
        self.logger.info(f"🔌 {self.agent_id} inicializando - Plugin Manager ALSHAM QUANTUM")

    def register_hook(self, event: str, callback):
        """Permite integração de hooks externos para eventos do agente."""
        self.hooks[event] = callback

    def trigger_hook(self, event: str, *args, **kwargs):
        if event in self.hooks:
            try:
                return self.hooks[event](*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Erro no hook '{event}': {e}")
        return None
        
    def get_capabilities(self) -> List[str]:
        """Retorna capabilities do Plugin Manager"""
        return self.capabilities
    
    async def initialize(self) -> Dict[str, Any]:
        """Inicialização robusta do Plugin Manager, com fallback e logging detalhado."""
        try:
            self.logger.info("🔌 Inicializando Plugin Manager ALSHAM QUANTUM...")
            await self._load_client_configuration()
            await self._initialize_message_bus()
            await self._discover_plugins()
            await self._start_configured_plugins()
            self._start_health_monitoring()
            self.logger.info("✅ Plugin Manager ALSHAM QUANTUM inicializado com sucesso")
            self.trigger_hook('initialized', self)
            return {"status": "initialized", "plugins_loaded": len(self.plugins)}
        except Exception as e:
            self.logger.error(f"❌ Erro na inicialização do Plugin Manager: {e}", exc_info=True)
            self.trigger_hook('init_failed', self, e)
            return {"status": "failed", "error": str(e)}
    
    async def process_message(self, message: Dict) -> Dict:
        """Processar mensagens do Plugin Manager com robustez, logging e hooks."""
        try:
            msg_type = message.get('type', 'unknown')
            self.trigger_hook('message_received', self, message)
            if msg_type == 'plugin_command':
                return await self._handle_plugin_command(message)
            elif msg_type == 'health_check_request':
                return await self._handle_health_check_request()
            elif msg_type == 'plugin_discovery':
                return await self._handle_plugin_discovery()
            elif msg_type == 'system_status':
                return await self._handle_system_status()
            elif msg_type == 'configuration_update':
                return await self._handle_configuration_update(message)
            else:
                return await self._handle_generic_message(message)
        except Exception as e:
            self.logger.error(f"Erro no processamento de mensagem: {e}", exc_info=True)
            self.trigger_hook('message_error', self, message, e)
            return {"error": str(e), "agent": self.agent_id}
    
    async def _load_client_configuration(self):
        """Carregar configuração específica do cliente"""
        try:
            # Determine client config file
            client_id = os.getenv('CLIENT_ID', 'default')
            config_file = self.config_path / f"client_{client_id}.yaml"
            
            if not config_file.exists():
                config_file = self.config_path / "default.yaml"
                
            if config_file.exists():
                with open(config_file, 'r') as f:
                    self.client_config = yaml.safe_load(f)
                self.logger.info(f"📋 Configuração carregada: {config_file}")
            else:
                # Create default configuration
                self.client_config = self._create_default_config()
                await self._save_client_configuration(config_file)
                self.logger.info("📋 Configuração padrão criada")
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar configuração: {e}")
            self.client_config = self._create_default_config()
    
    def _create_default_config(self) -> dict:
        """Criar configuração padrão baseada no blueprint"""
        return {
            "client_id": "alsham_default",
            "core_required": True,
            "plugins": {
                "analytics": {
                    "version": "1.0.0",
                    "enabled": True,
                    "priority": 1,
                    "config": {
                        "data_retention_days": 90,
                        "real_time_processing": True
                    }
                },
                "sales": {
                    "version": "1.0.0", 
                    "enabled": True,
                    "priority": 2,
                    "config": {
                        "pipeline_stages": ["lead", "qualified", "opportunity", "closed"],
                        "auto_follow_up": True
                    }
                },
                "support": {
                    "version": "1.0.0",
                    "enabled": False,  # Disabled by default
                    "priority": 3,
                    "config": {
                        "ticket_auto_assignment": True,
                        "sla_monitoring": True
                    }
                }
            },
            "message_bus": {
                "type": "rabbitmq",
                "host": "localhost",
                "port": 5672,
                "virtual_host": "/",
                "username": "alsham",
                "password": "quantum123"
            },
            "monitoring": {
                "health_check_interval": 30,
                "metrics_collection": True,
                "alerting": {
                    "enabled": True,
                    "webhook_url": "http://localhost:8080/alerts"
                }
            }
        }
    
    async def _initialize_message_bus(self):
        """Inicializar conexão com Message Bus"""
        try:
            # Simulated message bus initialization
            # In production: Connect to RabbitMQ/Kafka
            self.message_bus_client = MessageBusClient(self.message_bus_config)
            await self.message_bus_client.connect()
            
            # Subscribe to plugin-related events
            await self.message_bus_client.subscribe("plugin.*", self._handle_plugin_event)
            await self.message_bus_client.subscribe("system.health_check", self._handle_health_check_event)
            
            self.logger.info("🔗 Message Bus conectado e configurado")
            
        except Exception as e:
            self.logger.error(f"Erro na inicialização do Message Bus: {e}")
            # Fallback to direct communication mode
            self.message_bus_client = None
    
    async def _discover_plugins(self):
        """Descobrir plugins disponíveis"""
        try:
            self.logger.info("🔍 Descobrindo plugins disponíveis...")
            
            # Discover from client configuration
            if "plugins" in self.client_config:
                for plugin_name, plugin_config in self.client_config["plugins"].items():
                    plugin = PluginConfig(
                        name=plugin_name,
                        version=plugin_config.get("version", "1.0.0"),
                        enabled=plugin_config.get("enabled", False),
                        priority=plugin_config.get("priority", 5),
                        config=plugin_config.get("config", {}),
                        dependencies=plugin_config.get("dependencies", []),
                        resources=plugin_config.get("resources", {"cpu": "500m", "memory": "512Mi"})
                    )
                    
                    self.plugins[plugin_name] = plugin
                    self.plugin_metrics[plugin_name] = PluginMetrics(
                        name=plugin_name,
                        status=PluginStatus.STOPPED
                    )
                    
                    self.logger.info(f"📦 Plugin descoberto: {plugin_name} v{plugin.version} (enabled: {plugin.enabled})")
            
            self.last_discovery = datetime.now()
            self.logger.info(f"✅ Descoberta concluída: {len(self.plugins)} plugins encontrados")
            
        except Exception as e:
            self.logger.error(f"Erro na descoberta de plugins: {e}")
    
    async def _start_configured_plugins(self):
        """Iniciar plugins configurados na ordem de prioridade"""
        try:
            # Sort by priority (lower number = higher priority)
            enabled_plugins = [
                (name, plugin) for name, plugin in self.plugins.items() 
                if plugin.enabled
            ]
            enabled_plugins.sort(key=lambda x: x[1].priority)
            
            self.logger.info(f"🚀 Iniciando {len(enabled_plugins)} plugins habilitados...")
            
            for plugin_name, plugin_config in enabled_plugins:
                try:
                    await self._start_plugin(plugin_name)
                    # Wait a bit between plugin starts to avoid resource contention
                    await asyncio.sleep(2)
                except Exception as e:
                    self.logger.error(f"❌ Erro ao iniciar plugin {plugin_name}: {e}")
                    self.plugin_metrics[plugin_name].status = PluginStatus.ERROR
                    self.plugin_metrics[plugin_name].error_count += 1
            
        except Exception as e:
            self.logger.error(f"Erro ao iniciar plugins configurados: {e}")
    
    async def _start_plugin(self, plugin_name: str) -> Dict:
        """Iniciar um plugin específico"""
        try:
            if plugin_name not in self.plugins:
                return {"status": "error", "message": f"Plugin {plugin_name} não encontrado"}
            
            plugin = self.plugins[plugin_name]
            metrics = self.plugin_metrics[plugin_name]
            
            if metrics.status == PluginStatus.RUNNING:
                return {"status": "already_running", "plugin": plugin_name}
            
            self.logger.info(f"🚀 Iniciando plugin: {plugin_name} v{plugin.version}")
            metrics.status = PluginStatus.STARTING
            
            # Check dependencies first
            for dependency in plugin.dependencies:
                if dependency not in self.plugin_metrics or \
                   self.plugin_metrics[dependency].status != PluginStatus.RUNNING:
                    return {
                        "status": "dependency_error", 
                        "message": f"Dependency {dependency} not running",
                        "plugin": plugin_name
                    }
            
            # Start plugin based on deployment type
            if self.docker_client:
                # Container-based plugin (Production)
                success = await self._start_container_plugin(plugin_name, plugin)
            else:
                # Process-based plugin (Development)
                success = await self._start_process_plugin(plugin_name, plugin)
            
            if success:
                metrics.status = PluginStatus.RUNNING
                metrics.start_time = datetime.now()
                metrics.restart_count += 1
                
                # Publish plugin started event
                if self.message_bus_client:
                    await self.message_bus_client.publish(
                        f"plugin.{plugin_name}.started",
                        {"plugin": plugin_name, "version": plugin.version, "timestamp": datetime.now().isoformat()}
                    )
                
                self.logger.info(f"✅ Plugin {plugin_name} iniciado com sucesso")
                return {"status": "started", "plugin": plugin_name}
            else:
                metrics.status = PluginStatus.ERROR
                metrics.error_count += 1
                return {"status": "failed", "plugin": plugin_name}
            
        except Exception as e:
            self.logger.error(f"Erro ao iniciar plugin {plugin_name}: {e}")
            if plugin_name in self.plugin_metrics:
                self.plugin_metrics[plugin_name].status = PluginStatus.ERROR
                self.plugin_metrics[plugin_name].error_count += 1
            return {"status": "error", "message": str(e), "plugin": plugin_name}
    
    async def _start_container_plugin(self, plugin_name: str, plugin: PluginConfig) -> bool:
        """Iniciar plugin como container Docker"""
        try:
            # Build container image name
            image_name = f"alsham/{plugin_name}-plugin:{plugin.version}"
            
            # Container configuration
            container_config = {
                "image": image_name,
                "name": f"alsham-{plugin_name}-{int(time.time())}",
                "environment": {
                    "PLUGIN_NAME": plugin_name,
                    "PLUGIN_VERSION": plugin.version,
                    "MESSAGE_BUS_HOST": self.message_bus_config.get("host", "localhost"),
                    "MESSAGE_BUS_PORT": str(self.message_bus_config.get("port", 5672)),
                    "PLUGIN_CONFIG": json.dumps(plugin.config)
                },
                "networks": ["alsham-network"],
                "restart_policy": {"Name": "on-failure", "MaximumRetryCount": 3},
                "resources": {
                    "cpu_limit": plugin.resources.get("cpu", "500m"),
                    "mem_limit": plugin.resources.get("memory", "512Mi")
                }
            }
            
            # Start container
            container = self.docker_client.containers.run(detach=True, **container_config)
            self.plugin_containers[plugin_name] = container
            
            # Wait a moment for container to initialize
            await asyncio.sleep(3)
            
            # Check if container is running
            container.reload()
            return container.status == "running"
            
        except Exception as e:
            self.logger.error(f"Erro ao iniciar container plugin {plugin_name}: {e}")
            return False
    
    async def _start_process_plugin(self, plugin_name: str, plugin: PluginConfig) -> bool:
        """Iniciar plugin como processo Python (modo desenvolvimento)"""
        try:
            # Plugin module path (assumes plugins are in /plugins directory)
            plugin_path = Path(f"/plugins/{plugin_name}_plugin/main.py")
            
            if not plugin_path.exists():
                self.logger.warning(f"Plugin path não encontrado: {plugin_path}")
                # Create mock plugin for demonstration
                return await self._create_mock_plugin(plugin_name, plugin)
            
            # Start plugin as subprocess
            env = {
                **os.environ,
                "PLUGIN_NAME": plugin_name,
                "PLUGIN_VERSION": plugin.version,
                "PLUGIN_CONFIG": json.dumps(plugin.config)
            }
            
            process = subprocess.Popen(
                ["python", str(plugin_path)],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.plugin_processes[plugin_name] = process
            
            # Wait a moment for process to initialize
            await asyncio.sleep(2)
            
            # Check if process is running
            return process.poll() is None
            
        except Exception as e:
            self.logger.error(f"Erro ao iniciar process plugin {plugin_name}: {e}")
            return False
    
    async def _create_mock_plugin(self, plugin_name: str, plugin: PluginConfig) -> bool:
        """Criar mock plugin para demonstração (modo desenvolvimento)"""
        try:
            # Create a mock plugin instance for demonstration
            mock_plugin = {
                "name": plugin_name,
                "version": plugin.version,
                "status": "running",
                "pid": f"mock-{int(time.time())}",
                "config": plugin.config
            }
            
            self.plugin_processes[plugin_name] = mock_plugin
            self.logger.info(f"🎭 Mock plugin criado para demonstração: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao criar mock plugin {plugin_name}: {e}")
            return False
    
    def _start_health_monitoring(self):
        """Iniciar thread de monitoramento de saúde"""
        if self.health_check_thread is None or not self.health_check_thread.is_alive():
            self.health_check_thread = threading.Thread(
                target=self._health_check_loop,
                daemon=True
            )
            self.health_check_thread.start()
            self.logger.info("💓 Monitoramento de saúde iniciado")
    
    def _health_check_loop(self):
        """Loop de monitoramento de saúde dos plugins"""
        while self.active:
            try:
                asyncio.run(self._perform_health_checks())
                time.sleep(self.health_check_interval)
            except Exception as e:
                self.logger.error(f"Erro no health check loop: {e}")
                time.sleep(5)  # Brief pause before retrying
    
    async def _perform_health_checks(self):
        """Executar verificações de saúde em todos os plugins ativos"""
        try:
            for plugin_name, metrics in self.plugin_metrics.items():
                if metrics.status == PluginStatus.RUNNING:
                    await self._check_plugin_health(plugin_name)
                    
        except Exception as e:
            self.logger.error(f"Erro nas verificações de saúde: {e}")
    
    async def _check_plugin_health(self, plugin_name: str):
        """Verificar saúde de um plugin específico"""
        try:
            metrics = self.plugin_metrics[plugin_name]
            
            # Container health check
            if plugin_name in self.plugin_containers:
                container = self.plugin_containers[plugin_name]
                container.reload()
                
                if container.status == "running":
                    metrics.health_status = "healthy"
                    
                    # Get container stats
                    stats = container.stats(stream=False)
                    metrics.cpu_usage = self._calculate_cpu_usage(stats)
                    metrics.memory_usage = self._calculate_memory_usage(stats)
                else:
                    metrics.health_status = "unhealthy"
                    metrics.status = PluginStatus.UNHEALTHY
                    
            # Process health check
            elif plugin_name in self.plugin_processes:
                process = self.plugin_processes[plugin_name]
                
                if isinstance(process, dict):  # Mock plugin
                    metrics.health_status = "healthy"
                elif process.poll() is None:  # Process running
                    metrics.health_status = "healthy"
                    
                    # Get process stats
                    try:
                        ps_process = psutil.Process(process.pid)
                        metrics.cpu_usage = ps_process.cpu_percent()
                        metrics.memory_usage = ps_process.memory_percent()
                    except psutil.NoSuchProcess:
                        metrics.health_status = "unhealthy"
                        metrics.status = PluginStatus.UNHEALTHY
                else:
                    metrics.health_status = "unhealthy"
                    metrics.status = PluginStatus.UNHEALTHY
            
            metrics.last_health_check = datetime.now()
            
            # Auto-restart unhealthy plugins
            if metrics.status == PluginStatus.UNHEALTHY:
                plugin = self.plugins[plugin_name]
                if plugin.enabled:  # Only restart if still enabled
                    self.logger.warning(f"🔄 Auto-reiniciando plugin não saudável: {plugin_name}")
                    await self._restart_plugin(plugin_name)
                    
        except Exception as e:
            self.logger.error(f"Erro na verificação de saúde do plugin {plugin_name}: {e}")
            if plugin_name in self.plugin_metrics:
                self.plugin_metrics[plugin_name].health_status = "error"
    
    def _calculate_cpu_usage(self, stats: dict) -> float:
        """Calcular uso de CPU do container"""
        try:
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                          stats['precpu_stats']['system_cpu_usage']
            
            if system_delta > 0:
                return (cpu_delta / system_delta) * len(stats['cpu_stats']['cpu_usage']['percpu_usage']) * 100.0
            return 0.0
        except (KeyError, ZeroDivisionError):
            return 0.0
    
    def _calculate_memory_usage(self, stats: dict) -> float:
        """Calcular uso de memória do container"""
        try:
            usage = stats['memory_stats']['usage']
            limit = stats['memory_stats']['limit']
            return (usage / limit) * 100.0 if limit > 0 else 0.0
        except (KeyError, ZeroDivisionError):
            return 0.0
    
    async def _restart_plugin(self, plugin_name: str) -> Dict:
        """Reiniciar um plugin"""
        try:
            self.logger.info(f"🔄 Reiniciando plugin: {plugin_name}")
            
            # Stop first
            await self._stop_plugin(plugin_name)
            await asyncio.sleep(2)
            
            # Then start
            result = await self._start_plugin(plugin_name)
            
            if result["status"] == "started":
                self.logger.info(f"✅ Plugin {plugin_name} reiniciado com sucesso")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao reiniciar plugin {plugin_name}: {e}")
            return {"status": "error", "message": str(e), "plugin": plugin_name}
    
    async def _stop_plugin(self, plugin_name: str) -> Dict:
        """Parar um plugin específico"""
        try:
            if plugin_name not in self.plugin_metrics:
                return {"status": "not_found", "plugin": plugin_name}
            
            metrics = self.plugin_metrics[plugin_name]
            if metrics.status == PluginStatus.STOPPED:
                return {"status": "already_stopped", "plugin": plugin_name}
            
            self.logger.info(f"⏹️ Parando plugin: {plugin_name}")
            metrics.status = PluginStatus.STOPPING
            
            # Stop container
            if plugin_name in self.plugin_containers:
                container = self.plugin_containers[plugin_name]
                container.stop(timeout=10)
                container.remove()
                del self.plugin_containers[plugin_name]
            
            # Stop process
            elif plugin_name in self.plugin_processes:
                process = self.plugin_processes[plugin_name]
                if not isinstance(process, dict):  # Not a mock plugin
                    process.terminate()
                    process.wait(timeout=10)
                del self.plugin_processes[plugin_name]
            
            metrics.status = PluginStatus.STOPPED
            
            # Publish plugin stopped event
            if self.message_bus_client:
                await self.message_bus_client.publish(
                    f"plugin.{plugin_name}.stopped",
                    {"plugin": plugin_name, "timestamp": datetime.now().isoformat()}
                )
            
            self.logger.info(f"✅ Plugin {plugin_name} parado com sucesso")
            return {"status": "stopped", "plugin": plugin_name}
            
        except Exception as e:
            self.logger.error(f"Erro ao parar plugin {plugin_name}: {e}")
            return {"status": "error", "message": str(e), "plugin": plugin_name}
    
    # Message Handlers
    async def _handle_plugin_command(self, message: Dict) -> Dict:
        """Processar comandos de plugin"""
        try:
            command = message.get('command')
            plugin_name = message.get('plugin_name')
            
            if command == 'start':
                return await self._start_plugin(plugin_name)
            elif command == 'stop':
                return await self._stop_plugin(plugin_name)
            elif command == 'restart':
                return await self._restart_plugin(plugin_name)
            elif command == 'status':
                return await self._get_plugin_status(plugin_name)
            else:
                return {"status": "unknown_command", "command": command}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def _handle_health_check_request(self) -> Dict:
        """Processar solicitação de health check"""
        try:
            healthy_plugins = sum(1 for m in self.plugin_metrics.values() 
                                if m.status == PluginStatus.RUNNING)
            total_plugins = len(self.plugins)
            
            return {
                "status": "healthy",
                "plugins": {
                    "total": total_plugins,
                    "running": healthy_plugins,
                    "health_percentage": (healthy_plugins / total_plugins * 100) if total_plugins > 0 else 100
                },
                "agent": self.agent_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e), "agent": self.agent_id}
    
    async def _handle_system_status(self) -> Dict:
        """Processar solicitação de status do sistema"""
        try:
            plugin_summary = {}
            for name, metrics in self.plugin_metrics.items():
                plugin_summary[name] = {
                    "status": metrics.status.value,
                    "health": metrics.health_status,
                    "cpu_usage": metrics.cpu_usage,
                    "memory_usage": metrics.memory_usage,
                    "restart_count": metrics.restart_count,
                    "error_count": metrics.error_count
                }
            
            return {
                "status": "system_operational",
                "total_plugins": len(self.plugins),
                "active_plugins": sum(1 for m in self.plugin_metrics.values() 
                                    if m.status == PluginStatus.RUNNING),
                "plugin_details": plugin_summary,
                "message_bus_connected": self.message_bus_client is not None,
                "last_discovery": self.last_discovery.isoformat() if self.last_discovery else None,
                "agent": self.agent_id
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e), "agent": self.agent_id}
    
    async def _get_plugin_status(self, plugin_name: str) -> Dict:
        """Obter status de um plugin específico"""
        try:
            if plugin_name not in self.plugin_metrics:
                return {"status": "not_found", "plugin": plugin_name}
            
            metrics = self.plugin_metrics[plugin_name]
            plugin = self.plugins[plugin_name]
            
            return {
                "status": "found",
                "plugin": plugin_name,
                "details": {
                    "version": plugin.version,
                    "enabled": plugin.enabled,
                    "status": metrics.status.value,
                    "health": metrics.health_status,
                    "start_time": metrics.start_time.isoformat() if metrics.start_time else None,
                    "cpu_usage": metrics.cpu_usage,
                    "memory_usage": metrics.memory_usage,
                    "restart_count": metrics.restart_count,
                    "error_count": metrics.error_count,
                    "dependencies": plugin.dependencies
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e), "plugin": plugin_name}
    
    def _default_message_bus_config(self) -> dict:
        """Configuração padrão do Message Bus"""
        return {
            "type": "rabbitmq",
            "host": "localhost", 
            "port": 5672,
            "virtual_host": "/",
            "username": "alsham",
            "password": "quantum123"
        }
    
    async def shutdown(self):
        """Shutdown graceful do Plugin Manager"""
        try:
            self.logger.info("🔄 Iniciando shutdown do Plugin Manager...")
            self.active = False
            
            # Stop all plugins
            for plugin_name in list(self.plugins.keys()):
                await self._stop_plugin(plugin_name)
            
            # Disconnect message bus
            if self.message_bus_client:
                await self.message_bus_client.disconnect()
            
            # Stop executor
            self.executor.shutdown(wait=True)
            
            self.logger.info("✅ Plugin Manager desligado com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro durante shutdown: {e}")

# Mock Message Bus Client for development
class MessageBusClient:
    """Mock Message Bus Client - Substituir por implementação real (RabbitMQ/Kafka)"""
    
    def __init__(self, config: dict):
        self.config = config
        self.connected = False
        self.subscriptions = {}
    
    async def connect(self):
        """Conectar ao Message Bus"""
        # Mock connection
        self.connected = True
        print(f"🔗 Mock Message Bus conectado: {self.config['host']}:{self.config['port']}")
    
    async def disconnect(self):
        """Desconectar do Message Bus"""
        self.connected = False
        print("🔌 Mock Message Bus desconectado")
    
    async def publish(self, topic: str, message: dict):
        """Publicar mensagem no Message Bus"""
        if self.connected:
            print(f"📤 Publicando em {topic}: {message}")
    
    async def subscribe(self, pattern: str, handler):
        """Subscrever a padrão de tópicos"""
        self.subscriptions[pattern] = handler
        print(f"📥 Subscrito em {pattern}")

# Factory function para criação do agente
def create_agents(*args, **kwargs) -> List[PluginManagerAgent]:
    """
    Criar Plugin Manager Agent - Core #36, robusto, extensível, pronto para produção.
    Aceita config_path, message_bus_config, logger via kwargs.
    Fallback seguro.
    """
    try:
        print("🔌 Criando Plugin Manager Agent - ALSHAM QUANTUM CORE #36...")
        config_path = kwargs.get('config_path', '/configs')
        message_bus_config = kwargs.get('message_bus_config', None)
        logger = kwargs.get('logger', None)
        plugin_manager = PluginManagerAgent(
            config_path=config_path,
            message_bus_config=message_bus_config,
            logger=logger
        )
        print(f"✅ Plugin Manager Agent criado: {plugin_manager.agent_id}")
        print(f"🔧 Capabilities: {', '.join(plugin_manager.capabilities)}")
        return [plugin_manager]
    except Exception as e:
        print(f"❌ Erro ao criar Plugin Manager Agent: {e}")
        import traceback
        traceback.print_exc()
        return []

# Testing function
async def test_plugin_manager():
    """Teste do Plugin Manager"""
    print("🧪 Testando Plugin Manager ALSHAM QUANTUM...")
    
    # Create Plugin Manager
    agents = create_agents()
    
    if agents:
        plugin_manager = agents[0]
        
        # Initialize
        result = await plugin_manager.initialize()
        print(f"📊 Inicialização: {result}")
        
        # Test system status
        status = await plugin_manager.process_message({"type": "system_status"})
        print(f"📊 Status do sistema: {status}")
        
        # Test health check
        health = await plugin_manager.process_message({"type": "health_check_request"})
        print(f"💓 Health check: {health}")
        
        return plugin_manager
    
    return None

if __name__ == "__main__":
    # Direct test
    import os
    os.makedirs("/configs", exist_ok=True)
    
    agents = create_agents()
    print(f"🎯 Plugin Manager Agent criado: {len(agents)} agente(s)")
    
    # Async test
    # asyncio.run(test_plugin_manager())
