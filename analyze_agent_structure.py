#!/usr/bin/env python3
"""
Agent Structure Analyzer - Agente Especializado em Análise de Arquitetura
Transforma análise estática em um agente dinâmico e poderoso
"""

import inspect
import logging
import sys
import ast
import os
import importlib
import asyncio
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority, AgentMessage

logger = logging.getLogger(__name__)

class AnalysisType(Enum):
    """Tipos de análise estrutural"""
    AGENT_DISCOVERY = "agent_discovery"
    ARCHITECTURE_ANALYSIS = "architecture_analysis"
    DEPENDENCY_MAPPING = "dependency_mapping"
    CAPABILITY_ASSESSMENT = "capability_assessment"
    EVOLUTION_TRACKING = "evolution_tracking"
    HEALTH_CHECK = "health_check"
    OPTIMIZATION_OPPORTUNITIES = "optimization_opportunities"

class StructureStatus(Enum):
    """Status da estrutura analisada"""
    HEALTHY = "healthy"
    NEEDS_OPTIMIZATION = "needs_optimization"
    CRITICAL_ISSUES = "critical_issues"
    EVOLVING = "evolving"
    DEPRECATED = "deprecated"

@dataclass
class AgentInfo:
    """Informações detalhadas de um agente"""
    agent_id: str
    class_name: str
    module_name: str
    file_path: str
    agent_type: str
    capabilities: List[str]
    inheritance_chain: List[str]
    methods: List[str]
    complexity_score: float
    last_modified: datetime
    dependencies: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class ArchitectureReport:
    """Relatório completo da arquitetura"""
    report_id: str
    total_agents: int
    agents_by_type: Dict[str, int]
    dependency_graph: Dict[str, List[str]]
    capability_matrix: Dict[str, List[str]]
    health_score: float
    critical_issues: List[str]
    optimization_opportunities: List[str]
    evolution_suggestions: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

class AgentStructureAnalyzer(BaseNetworkAgent):
    """Agente especializado em análise e otimização da arquitetura do sistema"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'architecture_analysis',
            'agent_discovery',
            'dependency_mapping',
            'capability_assessment',
            'structure_optimization',
            'evolution_tracking',
            'health_monitoring',
            'pattern_detection',
            'refactoring_suggestions'
        ]
        self.status = 'active'
        
        # Estado do analisador
        self.discovered_agents = {}  # agent_id -> AgentInfo
        self.analysis_history = []
        self.dependency_graph = defaultdict(set)
        self.capability_matrix = defaultdict(set)
        
        # Cache e otimizações
        self.module_cache = {}
        self.last_scan_time = {}
        self.architecture_snapshots = []
        
        # Configurações
        self.scan_directories = ['.', './src', './lib', './app']
        self.supported_extensions = ['.py']
        self.analysis_interval = 300  # 5 minutos
        
        # Métricas
        self.analysis_metrics = {
            'total_scans': 0,
            'agents_discovered': 0,
            'issues_found': 0,
            'optimizations_suggested': 0,
            'architecture_changes_detected': 0
        }
        
        # Tasks de background
        self._monitoring_task = None
        self._evolution_task = None
        
        logger.info(f"🏗️ {self.agent_id} inicializado com análise arquitetural avançada")
    
    async def start_architecture_monitoring(self):
        """Inicia monitoramento contínuo da arquitetura"""
        if not self._monitoring_task:
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            self._evolution_task = asyncio.create_task(self._evolution_tracking_loop())
            
            # Executar scan inicial
            await self.discover_all_agents()
            
            logger.info(f"🏗️ {self.agent_id} iniciou monitoramento arquitetural")
    
    async def stop_architecture_monitoring(self):
        """Para monitoramento arquitetural"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
        if self._evolution_task:
            self._evolution_task.cancel()
            self._evolution_task = None
        logger.info(f"🛑 {self.agent_id} parou monitoramento arquitetural")
    
    async def _monitoring_loop(self):
        """Loop principal de monitoramento"""
        while True:
            try:
                # Verificar mudanças na arquitetura
                changes_detected = await self._detect_architecture_changes()
                
                if changes_detected:
                    logger.info(f"🔄 Mudanças arquiteturais detectadas")
                    await self._handle_architecture_changes(changes_detected)
                
                # Analisar saúde da arquitetura
                health_issues = await self._analyze_architecture_health()
                
                if health_issues:
                    await self._handle_health_issues(health_issues)
                
                await asyncio.sleep(self.analysis_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento arquitetural: {e}")
    
    async def _evolution_tracking_loop(self):
        """Loop de tracking de evolução"""
        while True:
            try:
                # Capturar snapshot da arquitetura
                snapshot = await self._capture_architecture_snapshot()
                self.architecture_snapshots.append(snapshot)
                
                # Manter apenas últimos 20 snapshots
                if len(self.architecture_snapshots) > 20:
                    self.architecture_snapshots = self.architecture_snapshots[-20:]
                
                # Analisar evolução
                if len(self.architecture_snapshots) > 3:
                    evolution_analysis = self._analyze_evolution_trends()
                    await self._report_evolution_insights(evolution_analysis)
                
                await asyncio.sleep(self.analysis_interval * 4)  # A cada 20 minutos
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no tracking de evolução: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'analyze_architecture':
                result = await self.analyze_complete_architecture()
                await self._send_response(message, result)
                
            elif request_type == 'discover_agents':
                result = await self.discover_all_agents()
                await self._send_response(message, result)
                
            elif request_type == 'map_dependencies':
                result = await self.map_agent_dependencies()
                await self._send_response(message, result)
                
            elif request_type == 'assess_capabilities':
                result = await self.assess_system_capabilities()
                await self._send_response(message, result)
                
            elif request_type == 'suggest_optimizations':
                result = await self.suggest_architecture_optimizations()
                await self._send_response(message, result)
                
            elif request_type == 'get_health_report':
                result = await self.generate_health_report()
                await self._send_response(message, result)
    
    async def discover_all_agents(self) -> Dict[str, Any]:
        """Descobre todos os agentes no sistema"""
        try:
            logger.info(f"🔍 Iniciando descoberta completa de agentes...")
            
            discovered = {}
            
            # Escanear diretórios
            for directory in self.scan_directories:
                if os.path.exists(directory):
                    agents_in_dir = await self._scan_directory_for_agents(directory)
                    discovered.update(agents_in_dir)
            
            # Analisar agentes ativos no sistema
            active_agents = await self._analyze_active_agents()
            
            # Merge descobertas
            for agent_id, info in active_agents.items():
                if agent_id in discovered:
                    discovered[agent_id].capabilities.extend(info.get('capabilities', []))
                else:
                    discovered[agent_id] = AgentInfo(
                        agent_id=agent_id,
                        class_name=info.get('class_name', 'Unknown'),
                        module_name='runtime',
                        file_path='active_system',
                        agent_type=info.get('type', 'unknown'),
                        capabilities=info.get('capabilities', []),
                        inheritance_chain=[],
                        methods=[],
                        complexity_score=0.0,
                        last_modified=datetime.now()
                    )
            
            # Atualizar cache
            self.discovered_agents = discovered
            self.analysis_metrics['agents_discovered'] = len(discovered)
            self.analysis_metrics['total_scans'] += 1
            
            logger.info(f"✅ Descoberta completa: {len(discovered)} agentes encontrados")
            
            return {
                'status': 'completed',
                'total_agents': len(discovered),
                'agents': {k: self._agent_info_to_dict(v) for k, v in discovered.items()},
                'discovery_summary': self._generate_discovery_summary(discovered)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na descoberta de agentes: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _scan_directory_for_agents(self, directory: str) -> Dict[str, AgentInfo]:
        """Escaneia diretório em busca de agentes"""
        agents = {}
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in self.supported_extensions):
                    file_path = os.path.join(root, file)
                    
                    # Verificar se arquivo foi modificado desde último scan
                    if self._should_scan_file(file_path):
                        file_agents = await self._analyze_file_for_agents(file_path)
                        agents.update(file_agents)
        
        return agents
    
    def _should_scan_file(self, file_path: str) -> bool:
        """Verifica se arquivo deve ser escaneado"""
        try:
            mtime = os.path.getmtime(file_path)
            last_scan = self.last_scan_time.get(file_path, 0)
            
            if mtime > last_scan:
                self.last_scan_time[file_path] = mtime
                return True
            return False
        except:
            return True
    
    async def _analyze_file_for_agents(self, file_path: str) -> Dict[str, AgentInfo]:
        """Analisa arquivo específico em busca de agentes"""
        agents = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content, filename=file_path)
            
            # Encontrar classes que herdam de agentes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if self._is_agent_class(node):
                        agent_info = await self._extract_agent_info(node, file_path, content)
                        if agent_info:
                            agents[agent_info.agent_id] = agent_info
            
            # Procurar funções create_*_agents
            create_functions = self._find_create_functions(tree)
            for func_info in create_functions:
                # Analisar função para descobrir que agentes ela cria
                created_agents = await self._analyze_create_function(func_info, file_path)
                agents.update(created_agents)
            
        except Exception as e:
            logger.error(f"❌ Erro analisando {file_path}: {e}")
        
        return agents
    
    def _is_agent_class(self, node: ast.ClassDef) -> bool:
        """Verifica se uma classe é um agente"""
        # Verificar herança
        for base in node.bases:
            if isinstance(base, ast.Name):
                if 'Agent' in base.id:
                    return True
            elif isinstance(base, ast.Attribute):
                if 'Agent' in base.attr:
                    return True
        
        # Verificar nome da classe
        if 'Agent' in node.name:
            return True
        
        return False
    
    async def _extract_agent_info(self, node: ast.ClassDef, file_path: str, content: str) -> Optional[AgentInfo]:
        """Extrai informações detalhadas do agente"""
        try:
            # Informações básicas
            class_name = node.name
            agent_id = f"{class_name.lower()}_{file_path.split('/')[-1].replace('.py', '')}"
            
            # Extrair herança
            inheritance_chain = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    inheritance_chain.append(base.id)
                elif isinstance(base, ast.Attribute):
                    inheritance_chain.append(base.attr)
            
            # Extrair métodos
            methods = []
            capabilities = []
            
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(item.name)
                    
                    # Procurar por capabilities no __init__
                    if item.name == '__init__':
                        capabilities.extend(self._extract_capabilities_from_init(item))
            
            # Calcular complexidade
            complexity = self._calculate_class_complexity(node)
            
            # Detectar tipo de agente
            agent_type = self._detect_agent_type(class_name, capabilities)
            
            return AgentInfo(
                agent_id=agent_id,
                class_name=class_name,
                module_name=os.path.basename(file_path).replace('.py', ''),
                file_path=file_path,
                agent_type=agent_type,
                capabilities=capabilities,
                inheritance_chain=inheritance_chain,
                methods=methods,
                complexity_score=complexity,
                last_modified=datetime.fromtimestamp(os.path.getmtime(file_path))
            )
            
        except Exception as e:
            logger.error(f"❌ Erro extraindo info do agente: {e}")
            return None
    
    def _extract_capabilities_from_init(self, init_node: ast.FunctionDef) -> List[str]:
        """Extrai capabilities do método __init__"""
        capabilities = []
        
        for node in ast.walk(init_node):
            if isinstance(node, ast.Assign):
                # Procurar por self.capabilities = [...]
                for target in node.targets:
                    if (isinstance(target, ast.Attribute) and 
                        isinstance(target.value, ast.Name) and 
                        target.value.id == 'self' and 
                        target.attr == 'capabilities'):
                        
                        if isinstance(node.value, ast.List):
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Str):
                                    capabilities.append(elt.s)
                                elif isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                    capabilities.append(elt.value)
        
        return capabilities
    
    def _calculate_class_complexity(self, node: ast.ClassDef) -> float:
        """Calcula complexidade da classe"""
        complexity = 0
        
        # Contar métodos
        methods = sum(1 for item in node.body if isinstance(item, ast.FunctionDef))
        complexity += methods * 2
        
        # Contar linhas de código
        lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 50
        complexity += lines / 10
        
        # Contar decisões (if, for, while)
        decisions = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                decisions += 1
        complexity += decisions
        
        return complexity
    
    def _detect_agent_type(self, class_name: str, capabilities: List[str]) -> str:
        """Detecta tipo do agente baseado no nome e capabilities"""
        name_lower = class_name.lower()
        
        # Mapeamento por nome
        if 'analyzer' in name_lower:
            return 'analytics'
        elif 'monitor' in name_lower:
            return 'monitoring'
        elif 'control' in name_lower:
            return 'control'
        elif 'orchestrator' in name_lower:
            return 'orchestration'
        elif 'cognitive' in name_lower:
            return 'meta_cognitive'
        elif 'specialized' in name_lower:
            return 'specialized'
        elif 'core' in name_lower:
            return 'core'
        elif 'system' in name_lower:
            return 'system'
        elif 'service' in name_lower:
            return 'service'
        
        # Mapeamento por capabilities
        cap_str = ' '.join(capabilities).lower()
        if 'analysis' in cap_str or 'analytics' in cap_str:
            return 'analytics'
        elif 'monitoring' in cap_str or 'performance' in cap_str:
            return 'monitoring'
        elif 'security' in cap_str or 'guard' in cap_str:
            return 'security'
        elif 'optimization' in cap_str:
            return 'optimizer'
        
        return 'general'
    
    def _find_create_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Encontra funções create_*_agents"""
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('create_') and 'agent' in node.name.lower():
                    functions.append({
                        'name': node.name,
                        'node': node,
                        'line': node.lineno
                    })
        
        return functions
    
    async def _analyze_create_function(self, func_info: Dict[str, Any], file_path: str) -> Dict[str, AgentInfo]:
        """Analisa função create_*_agents para descobrir agentes criados"""
        agents = {}
        
        try:
            # Analisar corpo da função para identificar agentes criados
            func_node = func_info['node']
            
            for node in ast.walk(func_node):
                if isinstance(node, ast.Call):
                    # Procurar por chamadas de construtor de agentes
                    if isinstance(node.func, ast.Name):
                        class_name = node.func.id
                        if 'Agent' in class_name:
                            # Extrair ID do agente dos argumentos
                            agent_id = self._extract_agent_id_from_call(node)
                            if agent_id:
                                agents[agent_id] = AgentInfo(
                                    agent_id=agent_id,
                                    class_name=class_name,
                                    module_name=os.path.basename(file_path).replace('.py', ''),
                                    file_path=file_path,
                                    agent_type=self._detect_agent_type(class_name, []),
                                    capabilities=[],
                                    inheritance_chain=[],
                                    methods=[],
                                    complexity_score=0.0,
                                    last_modified=datetime.fromtimestamp(os.path.getmtime(file_path))
                                )
        
        except Exception as e:
            logger.error(f"❌ Erro analisando função create: {e}")
        
        return agents
    
    def _extract_agent_id_from_call(self, node: ast.Call) -> Optional[str]:
        """Extrai ID do agente de uma chamada de construtor"""
        try:
            # Procurar primeiro argumento que é string (geralmente o agent_id)
            for arg in node.args:
                if isinstance(arg, ast.Str):
                    return arg.s
                elif isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    return arg.value
        except:
            pass
        return None
    
    async def _analyze_active_agents(self) -> Dict[str, Dict[str, Any]]:
        """Analisa agentes atualmente ativos no sistema"""
        active_agents = {}
        
        try:
            # Acessar agentes do message_bus
            if hasattr(self.message_bus, 'subscribers'):
                for agent_id, agent in self.message_bus.subscribers.items():
                    if agent_id != self.agent_id:  # Não incluir a si mesmo
                        agent_info = {
                            'class_name': agent.__class__.__name__,
                            'type': getattr(agent, 'agent_type', 'unknown'),
                            'capabilities': getattr(agent, 'capabilities', []),
                            'status': getattr(agent, 'status', 'unknown')
                        }
                        active_agents[agent_id] = agent_info
        
        except Exception as e:
            logger.error(f"❌ Erro analisando agentes ativos: {e}")
        
        return active_agents
    
    async def analyze_complete_architecture(self) -> Dict[str, Any]:
        """Analisa arquitetura completa do sistema"""
        try:
            logger.info(f"🏗️ Iniciando análise completa da arquitetura...")
            
            # Descobrir todos os agentes
            discovery_result = await self.discover_all_agents()
            
            # Mapear dependências
            dependency_result = await self.map_agent_dependencies()
            
            # Avaliar capabilities
            capability_result = await self.assess_system_capabilities()
            
            # Calcular métricas arquiteturais
            metrics = self._calculate_architecture_metrics()
            
            # Detectar problemas
            issues = self._detect_architecture_issues()
            
            # Sugerir otimizações
            optimizations = await self.suggest_architecture_optimizations()
            
            # Gerar score de saúde
            health_score = self._calculate_architecture_health_score(metrics, issues)
            
            # Criar relatório
            report = ArchitectureReport(
                report_id=f"arch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                total_agents=len(self.discovered_agents),
                agents_by_type=self._count_agents_by_type(),
                dependency_graph=dict(self.dependency_graph),
                capability_matrix=dict(self.capability_matrix),
                health_score=health_score,
                critical_issues=issues.get('critical', []),
                optimization_opportunities=optimizations.get('opportunities', []),
                evolution_suggestions=optimizations.get('evolution_suggestions', [])
            )
            
            self.analysis_history.append(report)
            
            return {
                'status': 'completed',
                'report': self._report_to_dict(report),
                'metrics': metrics,
                'recommendations': self._generate_architecture_recommendations(report)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise arquitetural: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def map_agent_dependencies(self) -> Dict[str, Any]:
        """Mapeia dependências entre agentes"""
        try:
            logger.info(f"🔗 Mapeando dependências entre agentes...")
            
            dependencies = defaultdict(set)
            
            # Analisar imports e comunicações
            for agent_id, agent_info in self.discovered_agents.items():
                # Analisar arquivo fonte para dependências
                file_deps = await self._analyze_file_dependencies(agent_info.file_path)
                dependencies[agent_id].update(file_deps)
                
                # Analisar dependências de capabilities
                cap_deps = self._analyze_capability_dependencies(agent_info.capabilities)
                dependencies[agent_id].update(cap_deps)
            
            # Atualizar grafo de dependências
            self.dependency_graph = dependencies
            
            return {
                'status': 'completed',
                'dependencies': {k: list(v) for k, v in dependencies.items()},
                'dependency_count': sum(len(deps) for deps in dependencies.values()),
                'circular_dependencies': self._detect_circular_dependencies(dependencies)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro mapeando dependências: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _analyze_file_dependencies(self, file_path: str) -> Set[str]:
        """Analisa dependências de um arquivo"""
        dependencies = set()
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                # Analisar imports
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if 'agent' in alias.name.lower():
                                dependencies.add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and 'agent' in node.module.lower():
                            dependencies.add(node.module)
        
        except Exception as e:
            logger.error(f"❌ Erro analisando dependências do arquivo: {e}")
        
        return dependencies
    
    def _analyze_capability_dependencies(self, capabilities: List[str]) -> Set[str]:
        """Analisa dependências baseadas em capabilities"""
        dependencies = set()
        
        # Mapeamento de capabilities que implicam dependências
        capability_deps = {
            'orchestration': ['coordination', 'task_distribution'],
            'meta_cognition': ['learning', 'analysis'],
            'performance_monitoring': ['metrics_collection', 'alerting'],
            'security': ['validation', 'threat_detection']
        }
        
        for capability in capabilities:
            for dep_capability, implied_deps in capability_deps.items():
                if dep_capability in capability:
                    dependencies.update(implied_deps)
        
        return dependencies
    
    def _detect_circular_dependencies(self, dependencies: Dict[str, Set[str]]) -> List[List[str]]:
        """Detecta dependências circulares"""
        circular = []
        
        def dfs(node, path, visited):
            if node in path:
                # Encontrou ciclo
                cycle_start = path.index(node)
                circular.append(path[cycle_start:] + [node])
                return
            
            if node in visited:
                return
            
            visited.add(node)
            path.append(node)
            
            for neighbor in dependencies.get(node, []):
                dfs(neighbor, path[:], visited)
        
        visited = set()
        for agent_id in dependencies:
            if agent_id not in visited:
                dfs(agent_id, [], visited)
        
        return circular
    
    async def assess_system_capabilities(self) -> Dict[str, Any]:
        """Avalia capabilities do sistema completo"""
        try:
            logger.info(f"⚡ Avaliando capabilities do sistema...")
            
            all_capabilities = set()
            capability_coverage = defaultdict(list)
            
            # Coletar todas as capabilities
            for agent_id, agent_info in self.discovered_agents.items():
                all_capabilities.update(agent_info.capabilities)
                for capability in agent_info.capabilities:
                    capability_coverage[capability].append(agent_id)
            
            # Atualizar matriz de capabilities
            self.capability_matrix = capability_coverage
            
            # Analisar cobertura
            redundant_capabilities = {
                cap: agents for cap, agents in capability_coverage.items() 
                if len(agents) > 3
            }
            
            missing_capabilities = self._identify_missing_capabilities(all_capabilities)
            
            return {
                'status': 'completed',
                'total_capabilities': len(all_capabilities),
                'capabilities': list(all_capabilities),
                'coverage_matrix': {k: v for k, v in capability_coverage.items()},
                'redundant_capabilities': redundant_capabilities,
                'missing_capabilities': missing_capabilities,
                'capability_distribution': self._analyze_capability_distribution(capability_coverage)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro avaliando capabilities: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _identify_missing_capabilities(self, current_capabilities: Set[str]) -> List[str]:
        """Identifica capabilities que deveriam existir mas não existem"""
        expected_capabilities = {
            'logging', 'error_handling', 'configuration_management',
            'health_checking', 'metrics_reporting', 'backup_recovery',
            'load_balancing', 'caching', 'authentication', 'authorization'
        }
        
        return list(expected_capabilities - current_capabilities)
    
    def _analyze_capability_distribution(self, coverage: Dict[str, List[str]]) -> Dict[str, Any]:
        """Analisa distribuição de capabilities"""
        distribution = {
            'single_agent': 0,
            'multiple_agents': 0,
            'highly_redundant': 0
        }
        
        for capability, agents in coverage.items():
            if len(agents) == 1:
                distribution['single_agent'] += 1
            elif len(agents) <= 3:
                distribution['multiple_agents'] += 1
            else:
                distribution['highly_redundant'] += 1
        
        return distribution
    
    async def suggest_architecture_optimizations(self) -> Dict[str, Any]:
        """Sugere otimizações para a arquitetura"""
        try:
            logger.info(f"💡 Gerando sugestões de otimização...")
            
            opportunities = []
            evolution_suggestions = []
            
            # Analisar redundâncias
            redundancies = self._identify_redundancies()
            if redundancies:
                opportunities.extend([
                    f"Consolidar agentes redundantes: {', '.join(redundancies[:3])}"
                ])
            
            # Analisar gaps
            gaps = self._identify_capability_gaps()
            if gaps:
                opportunities.extend([
                    f"Implementar capabilities faltantes: {', '.join(gaps[:3])}"
                ])
            
            # Analisar complexidade
            complex_agents = self._identify_overly_complex_agents()
            if complex_agents:
                opportunities.extend([
                    f"Refatorar agentes complexos: {', '.join(complex_agents[:3])}"
                ])
            
            # Sugestões de evolução
            evolution_suggestions.extend([
                "Implementar padrão de factory para criação de agentes",
                "Adicionar interface comum para todos os agentes",
                "Implementar sistema de plugins para capabilities",
                "Criar registry centralizado de agentes"
            ])
            
            self.analysis_metrics['optimizations_suggested'] += len(opportunities)
            
            return {
                'status': 'completed',
                'opportunities': opportunities,
                'evolution_suggestions': evolution_suggestions,
                'priority_recommendations': self._prioritize_recommendations(opportunities)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro gerando otimizações: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _identify_redundancies(self) -> List[str]:
        """Identifica agentes redundantes"""
        redundant = []
        
        # Agrupar agentes por tipo e capabilities similares
        type_groups = defaultdict(list)
        for agent_id, info in self.discovered_agents.items():
            type_groups[info.agent_type].append((agent_id, info))
        
        for agent_type, agents in type_groups.items():
            if len(agents) > 3:  # Muitos agentes do mesmo tipo
                redundant.append(agent_type)
        
        return redundant
    
    def _identify_capability_gaps(self) -> List[str]:
        """Identifica gaps de capabilities"""
        current_caps = set()
        for info in self.discovered_agents.values():
            current_caps.update(info.capabilities)
        
        expected_caps = {
            'error_recovery', 'performance_optimization', 'resource_management',
            'scalability_management', 'fault_tolerance'
        }
        
        return list(expected_caps - current_caps)
    
    def _identify_overly_complex_agents(self) -> List[str]:
        """Identifica agentes excessivamente complexos"""
        complex_agents = []
        
        for agent_id, info in self.discovered_agents.items():
            if info.complexity_score > 50:  # Threshold de complexidade
                complex_agents.append(agent_id)
        
        return complex_agents
    
    def _prioritize_recommendations(self, opportunities: List[str]) -> List[Dict[str, Any]]:
        """Prioriza recomendações por impacto"""
        prioritized = []
        
        for opportunity in opportunities:
            priority = 'medium'
            impact = 'medium'
            
            if 'redundant' in opportunity.lower():
                priority = 'high'
                impact = 'high'
            elif 'complex' in opportunity.lower():
                priority = 'medium'
                impact = 'high'
            elif 'faltantes' in opportunity.lower():
                priority = 'low'
                impact = 'medium'
            
            prioritized.append({
                'recommendation': opportunity,
                'priority': priority,
                'impact': impact
            })
        
        return sorted(prioritized, key=lambda x: (
            ['high', 'medium', 'low'].index(x['priority']),
            ['high', 'medium', 'low'].index(x['impact'])
        ))
    
    async def generate_health_report(self) -> Dict[str, Any]:
        """Gera relatório de saúde da arquitetura"""
        try:
            logger.info(f"🏥 Gerando relatório de saúde arquitetural...")
            
            # Calcular métricas de saúde
            health_metrics = {
                'total_agents': len(self.discovered_agents),
                'active_agents': len([a for a in self.discovered_agents.values() if 'active' in str(a)]),
                'average_complexity': sum(a.complexity_score for a in self.discovered_agents.values()) / max(1, len(self.discovered_agents)),
                'capability_coverage': len(self.capability_matrix),
                'dependency_complexity': len(self.dependency_graph)
            }
            
            # Detectar problemas de saúde
            health_issues = self._detect_architecture_issues()
            
            # Calcular score geral
            health_score = self._calculate_architecture_health_score(health_metrics, health_issues)
            
            # Determinar status
            if health_score >= 80:
                status = StructureStatus.HEALTHY
            elif health_score >= 60:
                status = StructureStatus.NEEDS_OPTIMIZATION
            else:
                status = StructureStatus.CRITICAL_ISSUES
            
            return {
                'status': 'completed',
                'health_score': health_score,
                'overall_status': status.value,
                'metrics': health_metrics,
                'issues': health_issues,
                'recommendations': self._generate_health_recommendations(health_issues)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro gerando relatório de saúde: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _calculate_architecture_metrics(self) -> Dict[str, Any]:
        """Calcula métricas arquiteturais"""
        return {
            'modularity_score': self._calculate_modularity_score(),
            'coupling_score': self._calculate_coupling_score(),
            'cohesion_score': self._calculate_cohesion_score(),
            'complexity_score': self._calculate_overall_complexity(),
            'maintainability_score': self._calculate_maintainability_score()
        }
    
    def _calculate_modularity_score(self) -> float:
        """Calcula score de modularidade"""
        # Baseado na separação de responsabilidades
        type_distribution = self._count_agents_by_type()
        total_types = len(type_distribution)
        
        if total_types >= 5:  # Boa separação
            return 90.0
        elif total_types >= 3:
            return 70.0
        else:
            return 40.0
    
    def _calculate_coupling_score(self) -> float:
        """Calcula score de acoplamento (menor é melhor)"""
        total_deps = sum(len(deps) for deps in self.dependency_graph.values())
        total_agents = len(self.discovered_agents)
        
        if total_agents == 0:
            return 100.0
        
        avg_deps = total_deps / total_agents
        
        if avg_deps <= 2:
            return 90.0
        elif avg_deps <= 4:
            return 70.0
        else:
            return 50.0
    
    def _calculate_cohesion_score(self) -> float:
        """Calcula score de coesão"""
        # Baseado na consistência de capabilities por tipo
        cohesion_scores = []
        
        type_groups = defaultdict(list)
        for info in self.discovered_agents.values():
            type_groups[info.agent_type].append(info.capabilities)
        
        for agent_type, caps_list in type_groups.items():
            if len(caps_list) > 1:
                # Calcular similaridade entre capabilities
                all_caps = set()
                for caps in caps_list:
                    all_caps.update(caps)
                
                common_caps = set(caps_list[0])
                for caps in caps_list[1:]:
                    common_caps &= set(caps)
                
                if all_caps:
                    cohesion = len(common_caps) / len(all_caps)
                    cohesion_scores.append(cohesion)
        
        return (sum(cohesion_scores) / len(cohesion_scores) * 100) if cohesion_scores else 50.0
    
    def _calculate_overall_complexity(self) -> float:
        """Calcula complexidade geral"""
        if not self.discovered_agents:
            return 0.0
        
        total_complexity = sum(info.complexity_score for info in self.discovered_agents.values())
        avg_complexity = total_complexity / len(self.discovered_agents)
        
        # Normalizar para 0-100 (invertido, menor complexidade = melhor score)
        return max(0, min(100, 100 - (avg_complexity / 10)))
    
    def _calculate_maintainability_score(self) -> float:
        """Calcula score de manutenibilidade"""
        factors = []
        
        # Fator de documentação (assumindo que agentes com mais métodos têm mais doc)
        avg_methods = sum(len(info.methods) for info in self.discovered_agents.values()) / max(1, len(self.discovered_agents))
        doc_score = min(100, avg_methods * 10)
        factors.append(doc_score)
        
        # Fator de modularidade
        factors.append(self._calculate_modularity_score())
        
        # Fator de simplicidade
        factors.append(self._calculate_overall_complexity())
        
        return sum(factors) / len(factors) if factors else 50.0
    
    def _detect_architecture_issues(self) -> Dict[str, List[str]]:
        """Detecta problemas na arquitetura"""
        issues = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        # Dependências circulares
        circular_deps = self._detect_circular_dependencies(self.dependency_graph)
        if circular_deps:
            issues['critical'].append(f"Dependências circulares detectadas: {len(circular_deps)}")
        
        # Agentes órfãos (sem dependências nem dependentes)
        orphan_agents = self._detect_orphan_agents()
        if orphan_agents:
            issues['medium'].extend([f"Agente órfão: {agent}" for agent in orphan_agents[:3]])
        
        # Capabilities não cobertas
        missing_caps = self._identify_capability_gaps()
        if missing_caps:
            issues['high'].extend([f"Capability faltante: {cap}" for cap in missing_caps[:3]])
        
        return issues
    
    def _detect_orphan_agents(self) -> List[str]:
        """Detecta agentes órfãos"""
        orphans = []
        
        all_referenced = set()
        for deps in self.dependency_graph.values():
            all_referenced.update(deps)
        
        for agent_id in self.discovered_agents:
            has_deps = bool(self.dependency_graph.get(agent_id))
            is_referenced = agent_id in all_referenced
            
            if not has_deps and not is_referenced:
                orphans.append(agent_id)
        
        return orphans
    
    def _calculate_architecture_health_score(self, metrics: Dict[str, Any], issues: Dict[str, List[str]]) -> float:
        """Calcula score geral de saúde da arquitetura"""
        base_score = 100.0
        
        # Penalizar por problemas
        base_score -= len(issues.get('critical', [])) * 20
        base_score -= len(issues.get('high', [])) * 10
        base_score -= len(issues.get('medium', [])) * 5
        base_score -= len(issues.get('low', [])) * 1
        
        # Considerar métricas arquiteturais
        if 'modularity_score' in metrics:
            base_score = (base_score + metrics['modularity_score']) / 2
        
        return max(0, min(100, base_score))
    
    def _count_agents_by_type(self) -> Dict[str, int]:
        """Conta agentes por tipo"""
        counts = defaultdict(int)
        for info in self.discovered_agents.values():
            counts[info.agent_type] += 1
        return dict(counts)
    
    def _generate_discovery_summary(self, discovered: Dict[str, AgentInfo]) -> Dict[str, Any]:
        """Gera resumo da descoberta"""
        return {
            'by_type': self._count_agents_by_type(),
            'by_module': defaultdict(int, {
                info.module_name: sum(1 for i in discovered.values() if i.module_name == info.module_name)
                for info in discovered.values()
            }),
            'total_capabilities': len(set().union(*(info.capabilities for info in discovered.values()))),
            'average_complexity': sum(info.complexity_score for info in discovered.values()) / max(1, len(discovered))
        }
    
    def _generate_architecture_recommendations(self, report: ArchitectureReport) -> List[str]:
        """Gera recomendações baseadas no relatório"""
        recommendations = []
        
        if report.health_score < 70:
            recommendations.append("Arquitetura necessita de refatoração significativa")
        
        if report.critical_issues:
            recommendations.append("Resolver issues críticos imediatamente")
        
        if len(report.optimization_opportunities) > 5:
            recommendations.append("Implementar otimizações gradualmente por prioridade")
        
        if report.total_agents > 50:
            recommendations.append("Considerar divisão em subsistemas menores")
        
        return recommendations
    
    def _generate_health_recommendations(self, issues: Dict[str, List[str]]) -> List[str]:
        """Gera recomendações de saúde"""
        recommendations = []
        
        if issues.get('critical'):
            recommendations.append("Ação imediata necessária para resolver problemas críticos")
        
        if issues.get('high'):
            recommendations.append("Planejar correções para problemas de alta prioridade")
        
        if len(issues.get('medium', [])) > 5:
            recommendations.append("Considerar refatoração para resolver problemas médios")
        
        return recommendations
    
    # Métodos de detecção de mudanças e evolução
    async def _detect_architecture_changes(self) -> List[Dict[str, Any]]:
        """Detecta mudanças na arquitetura"""
        # Implementação simplificada
        return []
    
    async def _handle_architecture_changes(self, changes: List[Dict[str, Any]]):
        """Trata mudanças arquiteturais"""
        self.analysis_metrics['architecture_changes_detected'] += len(changes)
    
    async def _analyze_architecture_health(self) -> List[Dict[str, Any]]:
        """Analisa saúde arquitetural"""
        # Implementação simplificada
        return []
    
    async def _handle_health_issues(self, issues: List[Dict[str, Any]]):
        """Trata problemas de saúde"""
        for issue in issues:
            self.analysis_metrics['issues_found'] += 1
    
    async def _capture_architecture_snapshot(self) -> Dict[str, Any]:
        """Captura snapshot da arquitetura"""
        return {
            'timestamp': datetime.now().isoformat(),
            'agent_count': len(self.discovered_agents),
            'dependency_count': sum(len(deps) for deps in self.dependency_graph.values()),
            'capability_count': len(self.capability_matrix)
        }
    
    def _analyze_evolution_trends(self) -> Dict[str, Any]:
        """Analisa tendências de evolução"""
        if len(self.architecture_snapshots) < 2:
            return {}
        
        first = self.architecture_snapshots[0]
        last = self.architecture_snapshots[-1]
        
        return {
            'agent_growth': last['agent_count'] - first['agent_count'],
            'dependency_growth': last['dependency_count'] - first['dependency_count'],
            'capability_growth': last['capability_count'] - first['capability_count']
        }
    
    async def _report_evolution_insights(self, analysis: Dict[str, Any]):
        """Reporta insights de evolução"""
        if analysis:
            logger.info(f"📈 Evolução detectada: {analysis}")
    
    # Métodos de conversão e resposta
    def _agent_info_to_dict(self, info: AgentInfo) -> Dict[str, Any]:
        """Converte AgentInfo para dicionário"""
        return {
            'agent_id': info.agent_id,
            'class_name': info.class_name,
            'module_name': info.module_name,
            'agent_type': info.agent_type,
            'capabilities': info.capabilities,
            'methods': info.methods,
            'complexity_score': info.complexity_score,
            'last_modified': info.last_modified.isoformat()
        }
    
    def _report_to_dict(self, report: ArchitectureReport) -> Dict[str, Any]:
        """Converte relatório para dicionário"""
        return {
            'report_id': report.report_id,
            'total_agents': report.total_agents,
            'agents_by_type': report.agents_by_type,
            'health_score': report.health_score,
            'critical_issues': report.critical_issues,
            'optimization_opportunities': report.optimization_opportunities,
            'timestamp': report.timestamp.isoformat()
        }
    
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

def create_structure_analyzer_agent(message_bus, num_instances=1) -> List[AgentStructureAnalyzer]:
    """
    Cria agente de análise de estrutura arquitetural
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de análise estrutural
    """
    agents = []
    
    try:
        logger.info("🏗️ Criando AgentStructureAnalyzer...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "structure_analyzer_001"
        
        if agent_id not in existing_agents:
            try:
                agent = AgentStructureAnalyzer(agent_id, AgentType.SPECIALIZED, message_bus)
                
                # Iniciar monitoramento arquitetural
                asyncio.create_task(agent.start_architecture_monitoring())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com análise arquitetural avançada")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de análise estrutural criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando AgentStructureAnalyzer: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []
