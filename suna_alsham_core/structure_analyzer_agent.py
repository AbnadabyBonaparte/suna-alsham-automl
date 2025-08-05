# suna_alsham_core/structure_analyzer_agent.py - CORREÇÃO COMPLETA

import asyncio
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import importlib
import inspect
from collections import defaultdict, Counter

from .base_network_agent import BaseNetworkAgent, AgentType
from .message_bus import MessageBus
from .task_queue import TaskQueue

@dataclass
class StructuralMetrics:
    """Métricas estruturais do sistema"""
    agent_count: int = 0
    module_count: int = 0
    dependency_count: int = 0
    circular_dependencies: int = 0
    coverage_percentage: float = 0.0
    health_score: float = 0.0
    last_analysis: Optional[datetime] = None
    issues_found: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class DependencyNode:
    """Nó de dependência no grafo estrutural"""
    name: str
    node_type: str  # 'agent', 'module', 'class', 'function'
    dependencies: Set[str] = field(default_factory=set)
    dependents: Set[str] = field(default_factory=set)
    weight: int = 1
    is_critical: bool = False
    health_status: str = "unknown"

class StructureAnalyzerAgent(BaseNetworkAgent):
    """
    Agente Analisador de Estrutura do ALSHAM QUANTUM
    Analisa arquitetura, dependências e saúde estrutural do sistema
    """
    
    def __init__(self, agent_id: str = "structure_analyzer_001"):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.STRUCTURE_ANALYZER,
            capabilities=[
                "architectural_analysis",
                "dependency_mapping",
                "system_health_monitoring",
                "structure_optimization",
                "capability_assessment",
                "performance_analysis",
                "security_assessment",
                "scalability_analysis"
            ]
        )
        
        self.metrics = StructuralMetrics()
        self.dependency_graph: Dict[str, DependencyNode] = {}
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.module_registry: Dict[str, Dict[str, Any]] = {}
        self.analysis_history: List[Dict[str, Any]] = []
        self.monitoring_active = False
        
        # Configurações de análise
        self.analysis_depth = "deep"  # shallow, medium, deep
        self.scan_intervals = {
            "structure": timedelta(minutes=30),
            "health": timedelta(minutes=10),
            "dependencies": timedelta(hours=1)
        }
        
        logging.info(f"🔍 StructureAnalyzerAgent {agent_id} inicializado")

    async def initialize_agent(self) -> bool:
        """Inicializa o analisador de estrutura"""
        try:
            # Realizar análise inicial completa
            await self._perform_initial_analysis()
            
            # Configurar monitoramento contínuo
            await self._setup_continuous_monitoring()
            
            # Registrar callbacks de análise
            await self._register_analysis_callbacks()
            
            # Inicializar métricas baseline
            await self._initialize_baseline_metrics()
            
            logging.info(f"✅ Structure Analyzer {self.agent_id} inicializado com sucesso")
            return True
            
        except Exception as e:
            logging.error(f"❌ Erro na inicialização do Structure Analyzer: {e}")
            return False

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagens de análise estrutural"""
        try:
            message_type = message.get("type")
            
            if message_type == "analyze_structure":
                return await self._handle_structure_analysis(message)
            elif message_type == "dependency_check":
                return await self._handle_dependency_check(message)
            elif message_type == "health_assessment":
                return await self._handle_health_assessment(message)
            elif message_type == "optimization_request":
                return await self._handle_optimization_request(message)
            elif message_type == "capability_audit":
                return await self._handle_capability_audit(message)
            elif message_type == "performance_analysis":
                return await self._handle_performance_analysis(message)
            elif message_type == "security_scan":
                return await self._handle_security_scan(message)
            else:
                return {
                    "status": "error",
                    "message": f"Tipo de mensagem não reconhecido: {message_type}"
                }
                
        except Exception as e:
            logging.error(f"❌ Erro ao processar mensagem de análise: {e}")
            return {"status": "error", "message": str(e)}

    async def _perform_initial_analysis(self):
        """Realiza análise inicial completa do sistema"""
        logging.info("🔍 Iniciando análise estrutural completa...")
        
        # Análise de agentes
        await self._analyze_agent_structure()
        
        # Análise de módulos
        await self._analyze_module_structure()
        
        # Análise de dependências
        await self._analyze_dependencies()
        
        # Análise de saúde
        await self._analyze_system_health()
        
        # Calcular métricas
        await self._calculate_structural_metrics()
        
        logging.info("✅ Análise inicial completa")

    async def _analyze_agent_structure(self):
        """Analisa estrutura dos agentes"""
        try:
            # Escanear diretório core
            core_path = Path("suna_alsham_core")
            if core_path.exists():
                await self._scan_directory_for_agents(core_path, "core")
            
            # Escanear módulos de domínio
            domain_path = Path("domain_modules")
            if domain_path.exists():
                await self._scan_directory_for_agents(domain_path, "domain")
            
            self.metrics.agent_count = len(self.agent_registry)
            logging.info(f"📊 Agentes analisados: {self.metrics.agent_count}")
            
        except Exception as e:
            logging.error(f"❌ Erro na análise de agentes: {e}")

    async def _scan_directory_for_agents(self, directory: Path, category: str):
        """Escaneia diretório em busca de agentes"""
        for file_path in directory.rglob("*.py"):
            if file_path.name.startswith("__"):
                continue
                
            try:
                # Analisar arquivo Python
                agent_info = await self._analyze_python_file(file_path, category)
                if agent_info:
                    self.agent_registry[agent_info["name"]] = agent_info
                    
            except Exception as e:
                logging.warning(f"⚠️ Erro ao analisar {file_path}: {e}")

    async def _analyze_python_file(self, file_path: Path, category: str) -> Optional[Dict[str, Any]]:
        """Analisa arquivo Python em busca de agentes"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar se é um agente
            if "BaseNetworkAgent" in content or "AgentType" in content:
                return {
                    "name": file_path.stem,
                    "path": str(file_path),
                    "category": category,
                    "size": len(content),
                    "lines": len(content.splitlines()),
                    "classes": self._extract_classes(content),
                    "functions": self._extract_functions(content),
                    "imports": self._extract_imports(content),
                    "agent_types": self._extract_agent_types(content),
                    "capabilities": self._extract_capabilities(content),
                    "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime)
                }
                
        except Exception as e:
            logging.warning(f"⚠️ Erro ao ler arquivo {file_path}: {e}")
        
        return None

    def _extract_classes(self, content: str) -> List[str]:
        """Extrai classes do conteúdo"""
        classes = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("class ") and ":" in line:
                class_name = line.split("class ")[1].split("(")[0].split(":")[0].strip()
                classes.append(class_name)
        return classes

    def _extract_functions(self, content: str) -> List[str]:
        """Extrai funções do conteúdo"""
        functions = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("def ") and "(" in line:
                func_name = line.split("def ")[1].split("(")[0].strip()
                functions.append(func_name)
        return functions

    def _extract_imports(self, content: str) -> List[str]:
        """Extrai imports do conteúdo"""
        imports = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("from ") or line.startswith("import "):
                imports.append(line)
        return imports

    def _extract_agent_types(self, content: str) -> List[str]:
        """Extrai tipos de agente do conteúdo"""
        agent_types = []
        for line in content.splitlines():
            if "AgentType." in line:
                parts = line.split("AgentType.")
                for part in parts[1:]:
                    agent_type = part.split()[0].split(",")[0].split(")")[0]
                    if agent_type and agent_type not in agent_types:
                        agent_types.append(agent_type)
        return agent_types

    def _extract_capabilities(self, content: str) -> List[str]:
        """Extrai capacidades do conteúdo"""
        capabilities = []
        in_capabilities = False
        for line in content.splitlines():
            line = line.strip()
            if "capabilities=[" in line or "capabilities = [" in line:
                in_capabilities = True
                # Extrair capacidades da mesma linha
                if '"' in line:
                    caps = line.split('[')[1].split(']')[0]
                    capabilities.extend([c.strip().strip('"\'') for c in caps.split(',')])
                continue
            elif in_capabilities:
                if "]" in line:
                    in_capabilities = False
                elif '"' in line or "'" in line:
                    cap = line.strip().strip('",\'')
                    if cap:
                        capabilities.append(cap)
        return capabilities

    async def _analyze_module_structure(self):
        """Analisa estrutura dos módulos"""
        try:
            # Analisar módulos Python carregados
            for module_name, module in self._get_loaded_modules():
                module_info = {
                    "name": module_name,
                    "file": getattr(module, "__file__", "unknown"),
                    "doc": getattr(module, "__doc__", ""),
                    "classes": [],
                    "functions": [],
                    "attributes": []
                }
                
                # Analisar conteúdo do módulo
                for attr_name in dir(module):
                    if not attr_name.startswith("_"):
                        attr = getattr(module, attr_name)
                        if inspect.isclass(attr):
                            module_info["classes"].append(attr_name)
                        elif inspect.isfunction(attr):
                            module_info["functions"].append(attr_name)
                        else:
                            module_info["attributes"].append(attr_name)
                
                self.module_registry[module_name] = module_info
            
            self.metrics.module_count = len(self.module_registry)
            logging.info(f"📊 Módulos analisados: {self.metrics.module_count}")
            
        except Exception as e:
            logging.error(f"❌ Erro na análise de módulos: {e}")

    def _get_loaded_modules(self) -> List[Tuple[str, Any]]:
        """Obtém módulos carregados relacionados ao sistema"""
        import sys
        relevant_modules = []
        
        for module_name, module in sys.modules.items():
            if any(keyword in module_name.lower() for keyword in 
                   ["alsham", "suna", "agent", "quantum"]):
                relevant_modules.append((module_name, module))
        
        return relevant_modules

    async def _analyze_dependencies(self):
        """Analisa dependências do sistema"""
        try:
            # Construir grafo de dependências
            for agent_name, agent_info in self.agent_registry.items():
                node = DependencyNode(
                    name=agent_name,
                    node_type="agent"
                )
                
                # Analisar imports como dependências
                for import_line in agent_info.get("imports", []):
                    deps = self._parse_import_dependencies(import_line)
                    node.dependencies.update(deps)
                
                self.dependency_graph[agent_name] = node
            
            # Calcular dependentes (inverso)
            for node_name, node in self.dependency_graph.items():
                for dep in node.dependencies:
                    if dep in self.dependency_graph:
                        self.dependency_graph[dep].dependents.add(node_name)
            
            # Detectar dependências circulares
            await self._detect_circular_dependencies()
            
            self.metrics.dependency_count = sum(
                len(node.dependencies) for node in self.dependency_graph.values()
            )
            
            logging.info(f"📊 Dependências analisadas: {self.metrics.dependency_count}")
            
        except Exception as e:
            logging.error(f"❌ Erro na análise de dependências: {e}")

    def _parse_import_dependencies(self, import_line: str) -> Set[str]:
        """Parseia linha de import para extrair dependências"""
        deps = set()
        
        if import_line.startswith("from "):
            # from module import something
            module = import_line.split("from ")[1].split(" import")[0].strip()
            if module.startswith("."):
                module = module[1:]  # Remove relative import dot
            deps.add(module)
        elif import_line.startswith("import "):
            # import module
            modules = import_line.split("import ")[1].split(",")
            for module in modules:
                module = module.strip().split(" as ")[0].strip()
                deps.add(module)
        
        return deps

    async def _detect_circular_dependencies(self):
        """Detecta dependências circulares"""
        visited = set()
        rec_stack = set()
        circular_deps = []
        
        def dfs(node_name: str, path: List[str]) -> bool:
            if node_name in rec_stack:
                # Encontrada dependência circular
                cycle_start = path.index(node_name)
                cycle = path[cycle_start:] + [node_name]
                circular_deps.append(cycle)
                return True
            
            if node_name in visited:
                return False
            
            visited.add(node_name)
            rec_stack.add(node_name)
            
            node = self.dependency_graph.get(node_name)
            if node:
                for dep in node.dependencies:
                    if dep in self.dependency_graph:
                        if dfs(dep, path + [node_name]):
                            return True
            
            rec_stack.remove(node_name)
            return False
        
        # Executar DFS para cada nó
        for node_name in self.dependency_graph:
            if node_name not in visited:
                dfs(node_name, [])
        
        self.metrics.circular_dependencies = len(circular_deps)
        if circular_deps:
            logging.warning(f"⚠️ {len(circular_deps)} dependências circulares detectadas")
            for cycle in circular_deps:
                logging.warning(f"   Ciclo: {' → '.join(cycle)}")

    async def _analyze_system_health(self):
        """Analisa saúde geral do sistema"""
        try:
            health_factors = []
            
            # Fator 1: Cobertura de agentes (esperados vs encontrados)
            expected_agents = 56
            found_agents = len(self.agent_registry)
            coverage = (found_agents / expected_agents) * 100
            health_factors.append(min(coverage / 100, 1.0))
            
            # Fator 2: Dependências saudáveis (sem ciclos)
            if self.metrics.dependency_count > 0:
                circular_ratio = self.metrics.circular_dependencies / self.metrics.dependency_count
                health_factors.append(1.0 - circular_ratio)
            else:
                health_factors.append(0.5)  # Neutro se não há dependências
            
            # Fator 3: Distribuição de capacidades
            all_capabilities = []
            for agent_info in self.agent_registry.values():
                all_capabilities.extend(agent_info.get("capabilities", []))
            
            capability_distribution = len(set(all_capabilities)) / max(len(all_capabilities), 1)
            health_factors.append(capability_distribution)
            
            # Fator 4: Complexidade modular
            avg_complexity = sum(
                len(info.get("classes", [])) + len(info.get("functions", []))
                for info in self.agent_registry.values()
            ) / max(len(self.agent_registry), 1)
            
            # Normalizar complexidade (assumindo 10-50 como faixa saudável)
            complexity_health = 1.0 - abs(avg_complexity - 30) / 30
            health_factors.append(max(0.0, complexity_health))
            
            # Calcular score de saúde final
            self.metrics.health_score = sum(health_factors) / len(health_factors)
            self.metrics.coverage_percentage = coverage
            
            logging.info(f"🏥 Saúde do sistema: {self.metrics.health_score:.2%}")
            
        except Exception as e:
            logging.error(f"❌ Erro na análise de saúde: {e}")

    async def _calculate_structural_metrics(self):
        """Calcula métricas estruturais consolidadas"""
        self.metrics.last_analysis = datetime.now()
        
        # Identificar problemas
        self.metrics.issues_found = []
        self.metrics.recommendations = []
        
        if self.metrics.coverage_percentage < 100:
            missing = 56 - len(self.agent_registry)
            self.metrics.issues_found.append(f"Faltam {missing} agentes esperados")
            self.metrics.recommendations.append("Verificar implementação de agentes faltantes")
        
        if self.metrics.circular_dependencies > 0:
            self.metrics.issues_found.append(f"{self.metrics.circular_dependencies} dependências circulares")
            self.metrics.recommendations.append("Refatorar dependências circulares")
        
        if self.metrics.health_score < 0.8:
            self.metrics.issues_found.append("Score de saúde abaixo do ideal")
            self.metrics.recommendations.append("Melhorar arquitetura e distribuição de responsabilidades")

    async def _setup_continuous_monitoring(self):
        """Configura monitoramento contínuo"""
        if not self.monitoring_active:
            self.monitoring_active = True
            
            # Agendar análises periódicas
            asyncio.create_task(self._continuous_health_monitoring())
            asyncio.create_task(self._continuous_structure_monitoring())
            
            logging.info("🔄 Monitoramento contínuo ativado")

    async def _continuous_health_monitoring(self):
        """Monitoramento contínuo de saúde"""
        while self.monitoring_active:
            try:
                await asyncio.sleep(self.scan_intervals["health"].total_seconds())
                await self._analyze_system_health()
                
                # Notificar se saúde degradou
                if self.metrics.health_score < 0.7:
                    await self.message_bus.publish("system.health_alert", {
                        "health_score": self.metrics.health_score,
                        "issues": self.metrics.issues_found,
                        "agent_id": self.agent_id
                    })
                    
            except Exception as e:
                logging.error(f"❌ Erro no monitoramento de saúde: {e}")

    async def _continuous_structure_monitoring(self):
        """Monitoramento contínuo de estrutura"""
        while self.monitoring_active:
            try:
                await asyncio.sleep(self.scan_intervals["structure"].total_seconds())
                
                # Re-analisar estrutura
                old_count = self.metrics.agent_count
                await self._analyze_agent_structure()
                
                # Notificar mudanças
                if self.metrics.agent_count != old_count:
                    await self.message_bus.publish("system.structure_change", {
                        "old_count": old_count,
                        "new_count": self.metrics.agent_count,
                        "change": self.metrics.agent_count - old_count,
                        "agent_id": self.agent_id
                    })
                    
            except Exception as e:
                logging.error(f"❌ Erro no monitoramento estrutural: {e}")

    async def _register_analysis_callbacks(self):
        """Registra callbacks para eventos de análise"""
        callbacks = {
            "structure_analysis_request": self._on_structure_analysis_request,
            "health_check_request": self._on_health_check_request,
            "dependency_analysis_request": self._on_dependency_analysis_request
        }
        
        for event, callback in callbacks.items():
            await self.message_bus.register_callback(f"analysis.{event}", callback)

    async def _initialize_baseline_metrics(self):
        """Inicializa métricas baseline do sistema"""
        baseline = {
            "timestamp": datetime.now().isoformat(),
            "agent_count": self.metrics.agent_count,
            "module_count": self.metrics.module_count,
            "dependency_count": self.metrics.dependency_count,
            "health_score": self.metrics.health_score,
            "coverage_percentage": self.metrics.coverage_percentage
        }
        
        self.analysis_history.append(baseline)
        logging.info("📊 Métricas baseline estabelecidas")

    # Message Handlers
    async def _handle_structure_analysis(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa solicitação de análise estrutural"""
        try:
            analysis_type = message.get("analysis_type", "full")
            target = message.get("target", "all")
            
            if analysis_type == "full":
                await self._perform_initial_analysis()
            elif analysis_type == "agents":
                await self._analyze_agent_structure()
            elif analysis_type == "dependencies":
                await self._analyze_dependencies()
            elif analysis_type == "health":
                await self._analyze_system_health()
            
            return {
                "status": "success",
                "analysis_type": analysis_type,
                "metrics": {
                    "agent_count": self.metrics.agent_count,
                    "module_count": self.metrics.module_count,
                    "dependency_count": self.metrics.dependency_count,
                    "health_score": self.metrics.health_score,
                    "coverage_percentage": self.metrics.coverage_percentage,
                    "issues_found": self.metrics.issues_found,
                    "recommendations": self.metrics.recommendations
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _handle_dependency_check(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa verificação de dependências"""
        try:
            target_agent = message.get("agent_name")
            
            if target_agent and target_agent in self.dependency_graph:
                node = self.dependency_graph[target_agent]
                return {
                    "status": "success",
                    "agent": target_agent,
                    "dependencies": list(node.dependencies),
                    "dependents": list(node.dependents),
                    "is_critical": node.is_critical,
                    "health_status": node.health_status
                }
            else:
                # Retornar análise geral
                return {
                    "status": "success",
                    "total_dependencies": self.metrics.dependency_count,
                    "circular_dependencies": self.metrics.circular_dependencies,
                    "dependency_graph_size": len(self.dependency_graph)
                }
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _handle_health_assessment(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa avaliação de saúde"""
        try:
            await self._analyze_system_health()
            
            return {
                "status": "success",
                "health_score": self.metrics.health_score,
                "coverage_percentage": self.metrics.coverage_percentage,
                "issues_found": self.metrics.issues_found,
                "recommendations": self.metrics.recommendations,
                "last_analysis": self.metrics.last_analysis.isoformat() if self.metrics.last_analysis else None,
                "trend": self._calculate_health_trend()
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _calculate_health_trend(self) -> str:
        """Calcula tendência de saúde"""
        if len(self.analysis_history) < 2:
            return "insufficient_data"
        
        current_health = self.metrics.health_score
        previous_health = self.analysis_history[-2].get("health_score", 0)
        
        if current_health > previous_health * 1.05:
            return "improving"
        elif current_health < previous_health * 0.95:
            return "declining"
        else:
            return "stable"

    async def _handle_optimization_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa solicitação de otimização"""
        try:
            optimization_target = message.get("target", "general")
            
            suggestions = []
            
            if optimization_target == "dependencies":
                suggestions.extend(self._generate_dependency_optimizations())
            elif optimization_target == "performance":
                suggestions.extend(self._generate_performance_optimizations())
            elif optimization_target == "architecture":
                suggestions.extend(self._generate_architecture_optimizations())
            else:
                suggestions.extend(self._generate_general_optimizations())
            
            return {
                "status": "success",
                "optimization_target": optimization_target,
                "suggestions": suggestions,
                "priority_actions": [s for s in suggestions if s.get("priority") == "high"]
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _generate_dependency_optimizations(self) -> List[Dict[str, Any]]:
        """Gera otimizações de dependências"""
        suggestions = []
        
        if self.metrics.circular_dependencies > 0:
            suggestions.append({
                "type": "dependency_optimization",
                "priority": "high",
                "description": "Resolver dependências circulares detectadas",
                "impact": "high",
                "effort": "medium"
            })
        
        # Analisar nós com muitas dependências
        high_dependency_nodes = [
            name for name, node in self.dependency_graph.items()
            if len(node.dependencies) > 10
        ]
        
        if high_dependency_nodes:
            suggestions.append({
                "type": "dependency_reduction",
                "priority": "medium",
                "description": f"Reduzir dependências em: {', '.join(high_dependency_nodes[:3])}",
                "impact": "medium",
                "effort": "high"
            })
        
        return suggestions

    def _generate_performance_optimizations(self) -> List[Dict[str, Any]]:
        """Gera otimizações de performance"""
        suggestions = []
        
        # Analisar agentes com muitas funções (potencial refatoração)
        complex_agents = [
            name for name, info in self.agent_registry.items()
            if len(info.get("functions", [])) > 20
        ]
        
        if complex_agents:
            suggestions.append({
                "type": "complexity_reduction",
                "priority": "medium",
                "description": f"Refatorar agentes complexos: {', '.join(complex_agents[:3])}",
                "impact": "high",
                "effort": "high"
            })
        
        return suggestions

    def _generate_architecture_optimizations(self) -> List[Dict[str, Any]]:
        """Gera otimizações arquiteturais"""
        suggestions = []
        
        if self.metrics.coverage_percentage < 100:
            suggestions.append({
                "type": "completeness",
                "priority": "high", 
                "description": "Implementar agentes faltantes para atingir 100% de cobertura",
                "impact": "high",
                "effort": "medium"
            })
        
        return suggestions

    def _generate_general_optimizations(self) -> List[Dict[str, Any]]:
        """Gera otimizações gerais"""
        suggestions = []
        suggestions.extend(self._generate_dependency_optimizations())
        suggestions.extend(self._generate_performance_optimizations())
        suggestions.extend(self._generate_architecture_optimizations())
        return suggestions

    async def _handle_capability_audit(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa auditoria de capacidades"""
        try:
            # Coletar todas as capacidades
            all_capabilities = []
            capability_map = defaultdict(list)
            
            for agent_name, agent_info in self.agent_registry.items():
                capabilities = agent_info.get("capabilities", [])
                all_capabilities.extend(capabilities)
                for cap in capabilities:
                    capability_map[cap].append(agent_name)
            
            capability_stats = Counter(all_capabilities)
            
            return {
                "status": "success",
                "total_capabilities": len(set(all_capabilities)),
                "capability_distribution": dict(capability_stats),
                "capability_coverage": {
                    cap: agents for cap, agents in capability_map.items()
                },
                "redundant_capabilities": [
                    cap for cap, count in capability_stats.items() if count > 3
                ],
                "unique_capabilities": [
                    cap for cap, count in capability_stats.items() if count == 1
                ]
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _handle_performance_analysis(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa análise de performance"""
        try:
            metrics = message.get("performance_metrics", {})
            
            # Analisar métricas de performance
            analysis = {
                "response_time_analysis": self._analyze_response_times(metrics),
                "throughput_analysis": self._analyze_throughput(metrics),
                "resource_usage_analysis": self._analyze_resource_usage(metrics),
                "bottleneck_identification": self._identify_bottlenecks(metrics)
            }
            
            return {
                "status": "success",
                "performance_analysis": analysis,
                "recommendations": self._generate_performance_recommendations(analysis)
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _analyze_response_times(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa tempos de resposta"""
        response_times = metrics.get("response_times", {})
        
        if not response_times:
            return {"status": "no_data"}
        
        avg_time = sum(response_times.values()) / len(response_times)
        slow_agents = {k: v for k, v in response_times.items() if v > avg_time * 2}
        
        return {
            "average_time": avg_time,
            "slow_agents": slow_agents,
            "fastest_agent": min(response_times, key=response_times.get),
            "slowest_agent": max(response_times, key=response_times.get)
        }

    def _analyze_throughput(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa throughput do sistema"""
        throughput_data = metrics.get("throughput", {})
        
        if not throughput_data:
            return {"status": "no_data"}
        
        return {
            "total_throughput": sum(throughput_data.values()),
            "agent_throughput": throughput_data,
            "high_throughput_agents": {
                k: v for k, v in throughput_data.items() 
                if v > sum(throughput_data.values()) / len(throughput_data)
            }
        }

    def _analyze_resource_usage(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa uso de recursos"""
        resource_data = metrics.get("resource_usage", {})
        
        return {
            "memory_usage": resource_data.get("memory", {}),
            "cpu_usage": resource_data.get("cpu", {}),
            "high_resource_agents": self._identify_high_resource_agents(resource_data)
        }

    def _identify_high_resource_agents(self, resource_data: Dict[str, Any]) -> List[str]:
        """Identifica agentes com alto uso de recursos"""
        high_resource = []
        
        memory_data = resource_data.get("memory", {})
        cpu_data = resource_data.get("cpu", {})
        
        if memory_data:
            avg_memory = sum(memory_data.values()) / len(memory_data)
            high_resource.extend([
                agent for agent, usage in memory_data.items() 
                if usage > avg_memory * 2
            ])
        
        if cpu_data:
            avg_cpu = sum(cpu_data.values()) / len(cpu_data)
            high_resource.extend([
                agent for agent, usage in cpu_data.items() 
                if usage > avg_cpu * 2
            ])
        
        return list(set(high_resource))

    def _identify_bottlenecks(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica gargalos do sistema"""
        bottlenecks = []
        
        # Analisar dependências como possíveis gargalos
        for name, node in self.dependency_graph.items():
            if len(node.dependents) > 5:  # Muitos dependentes
                bottlenecks.append({
                    "type": "dependency_bottleneck",
                    "agent": name,
                    "dependents": len(node.dependents),
                    "severity": "high" if len(node.dependents) > 10 else "medium"
                })
        
        return bottlenecks

    def _generate_performance_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gera recomendações de performance"""
        recommendations = []
        
        # Recomendações baseadas em tempo de resposta
        response_analysis = analysis.get("response_time_analysis", {})
        if "slow_agents" in response_analysis and response_analysis["slow_agents"]:
            recommendations.append({
                "type": "optimize_slow_agents",
                "priority": "high",
                "description": f"Otimizar agentes lentos: {list(response_analysis['slow_agents'].keys())}",
                "impact": "high"
            })
        
        # Recomendações baseadas em gargalos
        bottlenecks = analysis.get("bottleneck_identification", [])
        if bottlenecks:
            recommendations.append({
                "type": "resolve_bottlenecks",
                "priority": "high",
                "description": f"Resolver gargalos identificados: {len(bottlenecks)} encontrados",
                "impact": "high"
            })
        
        return recommendations

    async def _handle_security_scan(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa scan de segurança"""
        try:
            scan_type = message.get("scan_type", "basic")
            
            security_issues = []
            
            # Verificar imports potencialmente perigosos
            dangerous_imports = ["os", "subprocess", "eval", "exec"]
            for agent_name, agent_info in self.agent_registry.items():
                imports = agent_info.get("imports", [])
                for imp in imports:
                    for dangerous in dangerous_imports:
                        if dangerous in imp:
                            security_issues.append({
                                "type": "dangerous_import",
                                "agent": agent_name,
                                "import": imp,
                                "severity": "medium"
                            })
            
            # Verificar exposição de credenciais (simulado)
            for agent_name, agent_info in self.agent_registry.items():
                if any("password" in func.lower() or "secret" in func.lower() 
                       for func in agent_info.get("functions", [])):
                    security_issues.append({
                        "type": "credential_exposure_risk",
                        "agent": agent_name,
                        "severity": "low",
                        "description": "Funções relacionadas a credenciais detectadas"
                    })
            
            return {
                "status": "success",
                "scan_type": scan_type,
                "security_issues": security_issues,
                "security_score": max(0, 1.0 - len(security_issues) * 0.1),
                "recommendations": self._generate_security_recommendations(security_issues)
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _generate_security_recommendations(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Gera recomendações de segurança"""
        recommendations = []
        
        if any(issue["type"] == "dangerous_import" for issue in issues):
            recommendations.append({
                "type": "review_imports",
                "priority": "medium",
                "description": "Revisar imports potencialmente perigosos",
                "impact": "security"
            })
        
        if any(issue["type"] == "credential_exposure_risk" for issue in issues):
            recommendations.append({
                "type": "secure_credentials",
                "priority": "high",
                "description": "Implementar gestão segura de credenciais",
                "impact": "security"
            })
        
        return recommendations

    # Callback handlers
    async def _on_structure_analysis_request(self, data: Dict[str, Any]):
        """Callback para solicitação de análise estrutural"""
        logging.info(f"📊 Solicitação de análise estrutural recebida: {data}")

    async def _on_health_check_request(self, data: Dict[str, Any]):
        """Callback para solicitação de check de saúde"""
        logging.info(f"🏥 Solicitação de check de saúde recebida: {data}")

    async def _on_dependency_analysis_request(self, data: Dict[str, Any]):
        """Callback para solicitação de análise de dependências"""
        logging.info(f"🔗 Solicitação de análise de dependências recebida: {data}")

    async def get_agent_status(self) -> Dict[str, Any]:
        """Retorna status detalhado do analisador de estrutura"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "is_active": self.is_active,
            "monitoring_active": self.monitoring_active,
            "metrics": {
                "agent_count": self.metrics.agent_count,
                "module_count": self.metrics.module_count,
                "dependency_count": self.metrics.dependency_count,
                "circular_dependencies": self.metrics.circular_dependencies,
                "health_score": self.metrics.health_score,
                "coverage_percentage": self.metrics.coverage_percentage,
                "last_analysis": self.metrics.last_analysis.isoformat() if self.metrics.last_analysis else None,
                "issues_count": len(self.metrics.issues_found),
                "recommendations_count": len(self.metrics.recommendations)
            },
            "analysis_history_size": len(self.analysis_history),
            "dependency_graph_size": len(self.dependency_graph),
            "agent_registry_size": len(self.agent_registry),
            "module_registry_size": len(self.module_registry)
        }

# Factory function para criar agentes analisadores
def create_structure_analyzer_agents() -> List[BaseNetworkAgent]:
    """
    Cria agentes analisadores de estrutura
    Retorna lista com StructureAnalyzerAgent
    """
    return [StructureAnalyzerAgent("structure_analyzer_001")]

# Instância global para compatibilidade
structure_analyzer = StructureAnalyzerAgent("structure_analyzer_001")

# Logging final
logging.info("🔍 StructureAnalyzerAgent criado e pronto para integração no ALSHAM QUANTUM")
