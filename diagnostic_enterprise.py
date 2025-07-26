#!/usr/bin/env python3
"""
Diagnóstico Enterprise para SUNA-ALSHAM
Identifica problemas reais sem gambiarras
"""

import os
import sys
import time
import asyncio
import traceback
import psutil
import json
from datetime import datetime
import logging

# Configurar logging profissional
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)8s] %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('diagnostic_enterprise.log')
    ]
)

class EnterpriseDiagnostic:
    """Diagnóstico de nível enterprise - sem atalhos"""
    
    def __init__(self):
        self.logger = logging.getLogger('EnterpriseDiagnostic')
        self.start_time = time.time()
        self.diagnostics = {
            'timestamp': datetime.now().isoformat(),
            'environment': {},
            'imports': {},
            'memory': {},
            'startup_sequence': [],
            'errors': [],
            'recommendations': []
        }
    
    def check_environment(self):
        """Verifica ambiente completo"""
        self.logger.info("="*60)
        self.logger.info("DIAGNÓSTICO ENTERPRISE - SUNA-ALSHAM v2.0")
        self.logger.info("="*60)
        
        # Informações do sistema
        self.diagnostics['environment'] = {
            'python_version': sys.version,
            'platform': sys.platform,
            'cpu_count': os.cpu_count(),
            'working_directory': os.getcwd(),
            'python_path': sys.path[:5],  # Primeiros 5 paths
            'env_vars': {
                'OPENAI_API_KEY': 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT_SET',
                'PORT': os.getenv('PORT', 'NOT_SET'),
                'PYTHONUNBUFFERED': os.getenv('PYTHONUNBUFFERED', 'NOT_SET')
            }
        }
        
        self.logger.info(f"Python: {sys.version}")
        self.logger.info(f"CPUs: {os.cpu_count()}")
        self.logger.info(f"Working Dir: {os.getcwd()}")
    
    def check_memory(self):
        """Monitora uso de memória"""
        try:
            memory = psutil.virtual_memory()
            self.diagnostics['memory']['initial'] = {
                'total_mb': memory.total / 1024 / 1024,
                'available_mb': memory.available / 1024 / 1024,
                'percent': memory.percent
            }
            self.logger.info(f"Memory: {memory.available / 1024 / 1024:.0f}MB available ({memory.percent}% used)")
        except Exception as e:
            self.logger.error(f"Memory check failed: {e}")
    
    def test_imports_sequence(self):
        """Testa sequência real de imports"""
        self.logger.info("\n🔍 TESTANDO SEQUÊNCIA DE IMPORTS:")
        
        import_sequence = [
            ('logging', 'standard'),
            ('asyncio', 'standard'),
            ('fastapi', 'web_framework'),
            ('uvicorn', 'web_server'),
            ('numpy', 'heavy_computation'),
            ('pandas', 'data_processing'),
            ('openai', 'ai_service'),
            ('redis', 'cache'),
            ('psutil', 'monitoring'),
            ('multi_agent_network', 'core_system'),
            ('main_complete_system_v2', 'main_system')
        ]
        
        for module_name, category in import_sequence:
            start = time.time()
            try:
                __import__(module_name)
                elapsed = time.time() - start
                self.diagnostics['imports'][module_name] = {
                    'status': 'success',
                    'time': elapsed,
                    'category': category
                }
                self.logger.info(f"✅ {module_name:.<30} {elapsed:.2f}s")
                
                # Alerta se demorar muito
                if elapsed > 5.0:
                    self.logger.warning(f"   ⚠️ {module_name} demorou {elapsed:.2f}s!")
                    
            except ImportError as e:
                self.diagnostics['imports'][module_name] = {
                    'status': 'failed',
                    'error': str(e),
                    'category': category
                }
                self.logger.error(f"❌ {module_name:.<30} FAILED: {e}")
            except Exception as e:
                self.diagnostics['imports'][module_name] = {
                    'status': 'error',
                    'error': str(e),
                    'category': category
                }
                self.logger.error(f"❌ {module_name:.<30} ERROR: {e}")
    
    async def test_startup_sequence(self):
        """Simula sequência completa de startup"""
        self.logger.info("\n🚀 TESTANDO SEQUÊNCIA DE STARTUP:")
        
        try:
            # 1. Importar FastAPI
            self.log_step("Importing FastAPI")
            from fastapi import FastAPI
            app = FastAPI()
            
            # 2. Importar sistema principal
            self.log_step("Importing main system")
            try:
                from main_complete_system_v2 import SUNAAlshamSystemV2
                system_class_available = True
            except ImportError as e:
                self.logger.error(f"Cannot import SUNAAlshamSystemV2: {e}")
                system_class_available = False
                self.diagnostics['errors'].append({
                    'type': 'import_error',
                    'module': 'SUNAAlshamSystemV2',
                    'error': str(e)
                })
            
            # 3. Criar instância do sistema
            if system_class_available:
                self.log_step("Creating system instance")
                system = SUNAAlshamSystemV2()
                
                # 4. Inicializar (com timeout)
                self.log_step("Initializing system (30s timeout)")
                try:
                    await asyncio.wait_for(
                        system.initialize_complete_system(),
                        timeout=30.0
                    )
                    self.logger.info("✅ System initialized successfully!")
                except asyncio.TimeoutError:
                    self.logger.error("❌ System initialization TIMEOUT after 30s")
                    self.diagnostics['errors'].append({
                        'type': 'timeout',
                        'stage': 'initialization',
                        'timeout': 30
                    })
            
            # 5. Testar endpoint health
            @app.get("/health")
            async def health():
                return {"status": "healthy", "timestamp": datetime.now().isoformat()}
            
            self.logger.info("✅ Health endpoint created")
            
        except Exception as e:
            self.logger.error(f"❌ Startup sequence failed: {e}")
            self.logger.error(traceback.format_exc())
            self.diagnostics['errors'].append({
                'type': 'startup_failure',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
    
    def log_step(self, step: str):
        """Registra passo com timing"""
        elapsed = time.time() - self.start_time
        self.diagnostics['startup_sequence'].append({
            'step': step,
            'elapsed': elapsed
        })
        self.logger.info(f"⏱️ [{elapsed:.2f}s] {step}")
    
    def analyze_results(self):
        """Analisa resultados e gera recomendações"""
        self.logger.info("\n📊 ANÁLISE DE RESULTADOS:")
        
        # Verificar imports lentos
        slow_imports = [
            (name, data['time']) 
            for name, data in self.diagnostics['imports'].items() 
            if data.get('status') == 'success' and data.get('time', 0) > 2.0
        ]
        
        if slow_imports:
            self.logger.warning(f"⚠️ {len(slow_imports)} imports lentos detectados")
            for name, time in slow_imports:
                self.logger.warning(f"   - {name}: {time:.2f}s")
            
            self.diagnostics['recommendations'].append({
                'issue': 'slow_imports',
                'solution': 'Consider lazy loading or import optimization',
                'modules': [name for name, _ in slow_imports]
            })
        
        # Verificar erros críticos
        critical_errors = [e for e in self.diagnostics['errors'] if e.get('type') in ['import_error', 'startup_failure']]
        if critical_errors:
            self.logger.error(f"❌ {len(critical_errors)} erros críticos encontrados")
            self.diagnostics['recommendations'].append({
                'issue': 'critical_errors',
                'solution': 'Fix import and startup errors before deployment',
                'errors': critical_errors
            })
        
        # Verificar timeout
        timeout_errors = [e for e in self.diagnostics['errors'] if e.get('type') == 'timeout']
        if timeout_errors:
            self.logger.warning("⚠️ Sistema não inicializa em tempo hábil")
            self.diagnostics['recommendations'].append({
                'issue': 'initialization_timeout',
                'solution': 'Implement progressive initialization or increase resources',
                'details': 'System takes too long to initialize all components'
            })
    
    def save_report(self):
        """Salva relatório detalhado"""
        report_file = 'diagnostic_enterprise_report.json'
        with open(report_file, 'w') as f:
            json.dump(self.diagnostics, f, indent=2)
        self.logger.info(f"\n💾 Relatório salvo: {report_file}")
        
        # Resumo executivo
        self.logger.info("\n" + "="*60)
        self.logger.info("RESUMO EXECUTIVO:")
        self.logger.info("="*60)
        
        total_errors = len(self.diagnostics['errors'])
        total_recommendations = len(self.diagnostics['recommendations'])
        
        if total_errors == 0:
            self.logger.info("✅ Sistema sem erros críticos")
        else:
            self.logger.error(f"❌ {total_errors} erros encontrados")
        
        if total_recommendations > 0:
            self.logger.warning(f"⚠️ {total_recommendations} recomendações de melhoria")
        
        elapsed_total = time.time() - self.start_time
        self.logger.info(f"\n⏱️ Tempo total de diagnóstico: {elapsed_total:.2f}s")

async def main():
    """Executa diagnóstico completo"""
    diagnostic = EnterpriseDiagnostic()
    
    # 1. Verificar ambiente
    diagnostic.check_environment()
    
    # 2. Verificar memória
    diagnostic.check_memory()
    
    # 3. Testar imports
    diagnostic.test_imports_sequence()
    
    # 4. Testar startup
    await diagnostic.test_startup_sequence()
    
    # 5. Analisar resultados
    diagnostic.analyze_results()
    
    # 6. Salvar relatório
    diagnostic.save_report()

if __name__ == "__main__":
    asyncio.run(main())
