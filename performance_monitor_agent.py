import logging
import time
import psutil
import gc
import sys
import tracemalloc
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
import ast
import subprocess
import os
from contextlib import contextmanager
from multi_agent_network import BaseNetworkAgent, AgentType

logger = logging.getLogger(__name__)

class PerformanceMonitorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['performance_monitoring', 'benchmarking', 'memory_analysis', 'execution_profiling']
        self.status = 'active'
        self.benchmark_history = []
        self.memory_snapshots = []
        self.performance_baselines = {}
        logger.info(f"✅ {self.agent_id} inicializado com capacidades de monitoramento de performance")

    def benchmark_code_execution(self, code: str, iterations: int = 100) -> Dict:
        """Executa benchmark de performance de um código"""
        try:
            # Compilar código para execução
            compiled_code = compile(code, '<string>', 'exec')
            
            # Medições de performance
            execution_times = []
            memory_usage = []
            
            # Iniciar monitoramento de memória
            tracemalloc.start()
            gc.collect()  # Limpar garbage collector
            
            # Executar benchmark
            for i in range(iterations):
                # Snapshot inicial de memória
                memory_before = tracemalloc.get_traced_memory()[0]
                
                # Medir tempo de execução
                start_time = time.perf_counter()
                
                try:
                    # Executar código em namespace isolado
                    namespace = {}
                    exec(compiled_code, namespace)
                except Exception as e:
                    logger.warning(f"⚠️ Erro na execução {i+1}: {e}")
                    continue
                
                end_time = time.perf_counter()
                
                # Snapshot final de memória
                memory_after = tracemalloc.get_traced_memory()[0]
                
                # Armazenar métricas
                execution_times.append((end_time - start_time) * 1000)  # em ms
                memory_usage.append(memory_after - memory_before)  # em bytes
                
                # Pequena pausa entre execuções
                time.sleep(0.001)
            
            tracemalloc.stop()
            
            # Calcular estatísticas
            if execution_times:
                benchmark_result = {
                    "timestamp": datetime.now().isoformat(),
                    "iterations": len(execution_times),
                    "execution_stats": {
                        "min_time_ms": min(execution_times),
                        "max_time_ms": max(execution_times),
                        "avg_time_ms": sum(execution_times) / len(execution_times),
                        "total_time_ms": sum(execution_times)
                    },
                    "memory_stats": {
                        "min_memory_bytes": min(memory_usage) if memory_usage else 0,
                        "max_memory_bytes": max(memory_usage) if memory_usage else 0,
                        "avg_memory_bytes": sum(memory_usage) / len(memory_usage) if memory_usage else 0,
                        "total_memory_bytes": sum(memory_usage) if memory_usage else 0
                    },
                    "performance_score": self._calculate_performance_score(execution_times, memory_usage),
                    "code_complexity": self._analyze_code_complexity(code)
                }
                
                self.benchmark_history.append(benchmark_result)
                logger.info(f"📊 Benchmark concluído: {benchmark_result['execution_stats']['avg_time_ms']:.2f}ms média")
                
                return benchmark_result
            else:
                return {"error": "Nenhuma execução bem-sucedida"}
                
        except Exception as e:
            logger.error(f"❌ Erro no benchmark: {e}")
            return {"error": str(e)}

    def compare_performance(self, old_code: str, new_code: str, iterations: int = 50) -> Dict:
        """Compara performance entre duas versões do código"""
        try:
            logger.info("📊 Iniciando comparação de performance...")
            
            # Benchmark da versão antiga
            old_benchmark = self.benchmark_code_execution(old_code, iterations)
            if "error" in old_benchmark:
                return {"error": f"Erro na versão antiga: {old_benchmark['error']}"}
            
            # Benchmark da versão nova
            new_benchmark = self.benchmark_code_execution(new_code, iterations)
            if "error" in new_benchmark:
                return {"error": f"Erro na versão nova: {new_benchmark['error']}"}
            
            # Calcular melhorias
            old_avg_time = old_benchmark["execution_stats"]["avg_time_ms"]
            new_avg_time = new_benchmark["execution_stats"]["avg_time_ms"]
            
            old_avg_memory = old_benchmark["memory_stats"]["avg_memory_bytes"]
            new_avg_memory = new_benchmark["memory_stats"]["avg_memory_bytes"]
            
            time_improvement = ((old_avg_time - new_avg_time) / old_avg_time) * 100
            memory_improvement = ((old_avg_memory - new_avg_memory) / old_avg_memory) * 100 if old_avg_memory > 0 else 0
            
            comparison_result = {
                "timestamp": datetime.now().isoformat(),
                "old_performance": old_benchmark,
                "new_performance": new_benchmark,
                "improvements": {
                    "time_improvement_percent": time_improvement,
                    "memory_improvement_percent": memory_improvement,
                    "performance_gain": time_improvement + (memory_improvement * 0.3),  # Peso maior para tempo
                    "is_better": time_improvement > 0 or memory_improvement > 0
                },
                "recommendation": self._generate_performance_recommendation(time_improvement, memory_improvement)
            }
            
            logger.info(f"📈 Comparação concluída: {time_improvement:+.1f}% tempo, {memory_improvement:+.1f}% memória")
            return comparison_result
            
        except Exception as e:
            logger.error(f"❌ Erro na comparação: {e}")
            return {"error": str(e)}

    def monitor_system_resources(self) -> Dict:
        """Monitora recursos do sistema"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memória
            memory = psutil.virtual_memory()
            
            # Disco
            disk = psutil.disk_usage('/')
            
            # Processos Python
            python_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if 'python' in proc.info['name'].lower():
                        python_processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            system_stats = {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "usage_percent": cpu_percent,
                    "core_count": cpu_count,
                    "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
                },
                "memory": {
                    "total_gb": memory.total / (1024**3),
                    "available_gb": memory.available / (1024**3),
                    "used_percent": memory.percent,
                    "free_gb": memory.free / (1024**3)
                },
                "disk": {
                    "total_gb": disk.total / (1024**3),
                    "used_gb": disk.used / (1024**3),
                    "free_gb": disk.free / (1024**3),
                    "usage_percent": (disk.used / disk.total) * 100
                },
                "python_processes": len(python_processes),
                "system_health": self._assess_system_health(cpu_percent, memory.percent, disk.used/disk.total*100)
            }
            
            self.memory_snapshots.append(system_stats)
            return system_stats
            
        except Exception as e:
            logger.error(f"❌ Erro monitorando sistema: {e}")
            return {"error": str(e)}

    def analyze_code_efficiency(self, file_path: str) -> Dict:
        """Analisa eficiência de um arquivo de código"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"Arquivo não encontrado: {file_path}"}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Análise estática
            tree = ast.parse(code)
            
            # Métricas de complexidade
            complexity_metrics = self._analyze_code_complexity(code)
            
            # Detectar padrões ineficientes
            inefficient_patterns = self._detect_inefficient_patterns(code)
            
            # Análise de imports
            import_analysis = self._analyze_imports(tree)
            
            # Análise de funções
            function_analysis = self._analyze_functions(tree)
            
            efficiency_report = {
                "file_path": file_path,
                "timestamp": datetime.now().isoformat(),
                "complexity_metrics": complexity_metrics,
                "inefficient_patterns": inefficient_patterns,
                "import_analysis": import_analysis,
                "function_analysis": function_analysis,
                "efficiency_score": self._calculate_efficiency_score(
                    complexity_metrics, inefficient_patterns, import_analysis
                ),
                "optimization_suggestions": self._generate_optimization_suggestions(
                    inefficient_patterns, complexity_metrics
                )
            }
            
            return efficiency_report
            
        except Exception as e:
            logger.error(f"❌ Erro analisando eficiência: {e}")
            return {"error": str(e)}

    def _calculate_performance_score(self, execution_times: List[float], memory_usage: List[int]) -> float:
        """Calcula score de performance (0-100, maior é melhor)"""
        try:
            if not execution_times:
                return 0.0
            
            avg_time = sum(execution_times) / len(execution_times)
            avg_memory = sum(memory_usage) / len(memory_usage) if memory_usage else 0
            
            # Score baseado em tempo (peso 70%)
            time_score = max(0, 100 - (avg_time * 10))  # Penaliza tempos altos
            
            # Score baseado em memória (peso 30%)
            memory_score = max(0, 100 - (avg_memory / 1024))  # Penaliza uso alto de memória
            
            final_score = (time_score * 0.7) + (memory_score * 0.3)
            return min(100.0, max(0.0, final_score))
            
        except Exception:
            return 50.0  # Score neutro em caso de erro

    def _analyze_code_complexity(self, code: str) -> Dict:
        """Analisa complexidade do código"""
        try:
            tree = ast.parse(code)
            
            # Contadores
            lines_of_code = len([line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')])
            functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            loops = len([node for node in ast.walk(tree) if isinstance(node, (ast.For, ast.While))])
            conditions = len([node for node in ast.walk(tree) if isinstance(node, ast.If)])
            
            # Complexidade ciclomática básica
            cyclomatic_complexity = 1 + conditions + loops
            
            return {
                "lines_of_code": lines_of_code,
                "functions": functions,
                "classes": classes,
                "loops": loops,
                "conditions": conditions,
                "cyclomatic_complexity": cyclomatic_complexity,
                "complexity_level": self._classify_complexity(cyclomatic_complexity)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro analisando complexidade: {e}")
            return {}

    def _detect_inefficient_patterns(self, code: str) -> List[Dict]:
        """Detecta padrões ineficientes no código"""
        patterns = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # String concatenation in loops
            if '+=' in line and any(loop_keyword in lines[max(0, i-5):i] for loop_keyword in ['for ', 'while ']):
                patterns.append({
                    "pattern": "string_concatenation_in_loop",
                    "line": i,
                    "severity": "medium",
                    "description": "String concatenation in loop - consider using join()",
                    "suggestion": "Use ''.join() or list comprehension"
                })
            
            # Nested loops
            if 'for ' in line and any('for ' in l for l in lines[max(0, i-3):i]):
                patterns.append({
                    "pattern": "nested_loops",
                    "line": i,
                    "severity": "high",
                    "description": "Nested loops detected - potential O(n²) complexity",
                    "suggestion": "Consider algorithmic optimization or vectorization"
                })
            
            # Global variables in functions
            if 'global ' in line:
                patterns.append({
                    "pattern": "global_variable",
                    "line": i,
                    "severity": "low",
                    "description": "Global variable usage",
                    "suggestion": "Consider parameter passing or class attributes"
                })
        
        return patterns

    def _analyze_imports(self, tree: ast.AST) -> Dict:
        """Analisa imports do código"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        
        return {
            "total_imports": len(imports),
            "unique_imports": len(set(imports)),
            "imports_list": list(set(imports))
        }

    def _analyze_functions(self, tree: ast.AST) -> Dict:
        """Analisa funções do código"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Contar argumentos
                args_count = len(node.args.args)
                
                # Contar linhas da função
                func_lines = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
                
                functions.append({
                    "name": node.name,
                    "args_count": args_count,
                    "lines": func_lines
                })
        
        return {
            "total_functions": len(functions),
            "avg_function_length": sum(f["lines"] for f in functions) / len(functions) if functions else 0,
            "functions_with_many_args": len([f for f in functions if f["args_count"] > 5])
        }

    def _calculate_efficiency_score(self, complexity: Dict, patterns: List, imports: Dict) -> float:
        """Calcula score de eficiência do código"""
        try:
            score = 100.0
            
            # Penalizar complexidade alta
            if complexity.get("cyclomatic_complexity", 0) > 10:
                score -= (complexity["cyclomatic_complexity"] - 10) * 2
            
            # Penalizar padrões ineficientes
            for pattern in patterns:
                if pattern["severity"] == "high":
                    score -= 15
                elif pattern["severity"] == "medium":
                    score -= 10
                else:
                    score -= 5
            
            # Penalizar muitos imports
            if imports.get("total_imports", 0) > 20:
                score -= (imports["total_imports"] - 20) * 0.5
            
            return max(0.0, min(100.0, score))
            
        except Exception:
            return 50.0

    def _generate_optimization_suggestions(self, patterns: List, complexity: Dict) -> List[str]:
        """Gera sugestões de otimização"""
        suggestions = []
        
        # Sugestões baseadas em padrões
        pattern_types = [p["pattern"] for p in patterns]
        
        if "string_concatenation_in_loop" in pattern_types:
            suggestions.append("Replace string concatenation in loops with join() method")
        
        if "nested_loops" in pattern_types:
            suggestions.append("Optimize nested loops using better algorithms or data structures")
        
        # Sugestões baseadas em complexidade
        if complexity.get("cyclomatic_complexity", 0) > 15:
            suggestions.append("Break down complex functions into smaller, more manageable pieces")
        
        if complexity.get("functions", 0) == 0:
            suggestions.append("Consider organizing code into functions for better modularity")
        
        return suggestions

    def _classify_complexity(self, cyclomatic_complexity: int) -> str:
        """Classifica nível de complexidade"""
        if cyclomatic_complexity <= 5:
            return "low"
        elif cyclomatic_complexity <= 10:
            return "medium"
        elif cyclomatic_complexity <= 20:
            return "high"
        else:
            return "very_high"

    def _assess_system_health(self, cpu: float, memory: float, disk: float) -> str:
        """Avalia saúde do sistema"""
        if cpu > 90 or memory > 90 or disk > 95:
            return "critical"
        elif cpu > 70 or memory > 80 or disk > 85:
            return "warning"
        elif cpu > 50 or memory > 60 or disk > 70:
            return "moderate"
        else:
            return "good"

    def _generate_performance_recommendation(self, time_improvement: float, memory_improvement: float) -> str:
        """Gera recomendação baseada na melhoria de performance"""
        if time_improvement > 20 and memory_improvement > 10:
            return "Excellent optimization - significant improvements in both time and memory"
        elif time_improvement > 10:
            return "Good time optimization - consider further memory improvements"
        elif memory_improvement > 10:
            return "Good memory optimization - consider further time improvements"
        elif time_improvement > 0 or memory_improvement > 0:
            return "Minor improvements detected - optimization successful"
        else:
            return "No significant improvement - consider alternative optimization strategies"

    def generate_performance_report(self) -> str:
        """Gera relatório de performance"""
        if not self.benchmark_history:
            return "📊 Nenhum benchmark executado ainda"
        
        report = f"📊 RELATÓRIO DE PERFORMANCE - {self.agent_id}\n"
        report += "=" * 60 + "\n\n"
        
        total_benchmarks = len(self.benchmark_history)
        avg_score = sum(b.get("performance_score", 0) for b in self.benchmark_history) / total_benchmarks
        
        report += f"🔬 Total de benchmarks: {total_benchmarks}\n"
        report += f"📈 Score médio de performance: {avg_score:.1f}/100\n\n"
        
        # Últimos 3 benchmarks
        for i, benchmark in enumerate(self.benchmark_history[-3:], 1):
            timestamp = benchmark.get("timestamp", "")[:19]
            avg_time = benchmark.get("execution_stats", {}).get("avg_time_ms", 0)
            score = benchmark.get("performance_score", 0)
            
            report += f"🔬 BENCHMARK {i} - {timestamp}:\n"
            report += f"   ⏱️ Tempo médio: {avg_time:.2f}ms\n"
            report += f"   📊 Score: {score:.1f}/100\n"
            report += f"   🔍 Complexidade: {benchmark.get('code_complexity', {}).get('complexity_level', 'unknown')}\n\n"
        
        return report

def create_performance_monitor_agent(message_bus, num_instances=1) -> List['PerformanceMonitorAgent']:
    """Cria agente de monitoramento de performance"""
    agents = []
    try:
        logger.info("📊 Criando PerformanceMonitorAgent...")
        
        agent_id = "performance_monitor_001"
        agent = PerformanceMonitorAgent(agent_id, AgentType.SPECIALIZED, message_bus)
        
        # Registrar no MessageBus
        if hasattr(message_bus, 'register_agent'):
            message_bus.register_agent(agent_id, agent)
        
        agents.append(agent)
        logger.info(f"✅ {len(agents)} agente de monitoramento criado")
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro criando PerformanceMonitorAgent: {e}")
        return []
