#!/usr/bin/env python3
"""
ALSHAM QUANTUM - Correção Robusta Railway
Versão otimizada para ambiente de produção
"""
import os
import sys
import subprocess
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RailwayFixer:
    def __init__(self):
        self.project_root = Path.cwd()
        self.fixes_log = []
        logger.info("🚀 Iniciando correção ALSHAM QUANTUM")
        
    def install_dependencies_railway(self):
        """Instala dependências otimizado para Railway"""
        logger.info("📦 INSTALANDO DEPENDÊNCIAS NO RAILWAY...")
        
        # Comandos otimizados para Railway
        commands = [
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
            [sys.executable, '-m', 'pip', 'install', 'PyJWT==2.8.0'],
            [sys.executable, '-m', 'pip', 'install', 'networkx==3.2.1'],
            [sys.executable, '-m', 'pip', 'install', 'python-jose[cryptography]==3.3.0'],
        ]
        
        for cmd in commands:
            try:
                logger.info(f"Executando: {' '.join(cmd)}")
                result = subprocess.run(cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=120,  # 2 minutos timeout
                    cwd=self.project_root
                )
                
                if result.returncode == 0:
                    logger.info(f"✅ Comando executado com sucesso")
                    self.fixes_log.append(f"Dependência instalada: {cmd[-1]}")
                else:
                    logger.error(f"❌ Erro: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                logger.error(f"⏰ Timeout executando: {' '.join(cmd)}")
            except Exception as e:
                logger.error(f"💥 Exceção: {e}")
    
    def create_requirements_file(self):
        """Cria requirements.txt com dependências essenciais"""
        logger.info("📄 Criando requirements.txt...")
        
        requirements = [
            "PyJWT==2.8.0",
            "networkx==3.2.1", 
            "python-jose[cryptography]==3.3.0",
            "cryptography>=3.4.8",
            "fastapi",
            "uvicorn",
            "psycopg2-binary",
            "sqlalchemy",
            "pydantic"
        ]
        
        req_file = self.project_root / "requirements.txt"
        
        try:
            with open(req_file, 'w') as f:
                for req in requirements:
                    f.write(f"{req}\n")
            
            logger.info(f"✅ requirements.txt criado: {req_file}")
            self.fixes_log.append("requirements.txt criado")
            
        except Exception as e:
            logger.error(f"❌ Erro criando requirements.txt: {e}")
    
    def create_core_module(self):
        """Cria módulo core faltando"""
        logger.info("🔧 Criando módulo core...")
        
        # Criar estrutura de diretórios se necessário
        suna_dir = self.project_root / "suna_alsham_core"
        suna_dir.mkdir(exist_ok=True)
        
        # Criar __init__.py
        init_file = suna_dir / "__init__.py"
        with open(init_file, 'w') as f:
            f.write('"""ALSHAM QUANTUM Core Package"""\n')
        
        # Criar core.py
        core_file = suna_dir / "core.py"
        core_content = '''"""
ALSHAM QUANTUM - Core Module
Módulo central para compatibilidade e coordenação
"""
import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class QuantumCore:
    """Núcleo central do sistema ALSHAM QUANTUM"""
    
    def __init__(self):
        self.version = "2.0.0"
        self.status = "operational"
        self.agents = {}
        self.initialized_at = datetime.now()
        logger.info("🚀 QuantumCore inicializado")
    
    def register_agent(self, agent_id: str, agent_info: Dict[str, Any]):
        """Registra um agente no core"""
        self.agents[agent_id] = agent_info
        logger.info(f"✅ Agente registrado: {agent_id}")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do sistema"""
        return {
            "version": self.version,
            "status": self.status,
            "agents_count": len(self.agents),
            "uptime": (datetime.now() - self.initialized_at).total_seconds()
        }
    
    def list_agents(self) -> List[str]:
        """Lista agentes registrados"""
        return list(self.agents.keys())

# Instância global
quantum_core = QuantumCore()

def get_core():
    """Retorna instância do core"""
    return quantum_core
'''
        
        try:
            with open(core_file, 'w', encoding='utf-8') as f:
                f.write(core_content)
            
            logger.info(f"✅ Core module criado: {core_file}")
            self.fixes_log.append("Módulo core.py criado")
            
        except Exception as e:
            logger.error(f"❌ Erro criando core.py: {e}")
    
    def fix_import_structure(self):
        """Corrige estrutura de imports nos arquivos existentes"""
        logger.info("🔧 Corrigindo estrutura de imports...")
        
        # Buscar arquivos Python no diretório atual
        python_files = list(self.project_root.glob("*.py"))
        
        import_corrections = {
            "suna_alsham_core.agents.": "",
            "suna_alsham_core.core.": "suna_alsham_core.core.",
            "suna_alsham_core.": "",
        }
        
        for py_file in python_files:
            if py_file.name in ['urgent_fix.py', 'railway_fix.py']:
                continue  # Pular scripts de correção
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Aplicar correções
                for old_pattern, new_pattern in import_corrections.items():
                    if old_pattern in content:
                        content = content.replace(old_pattern, new_pattern)
                        logger.info(f"   📝 {py_file.name}: {old_pattern} → {new_pattern}")
                
                # Salvar se houve mudanças
                if content != original_content:
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    logger.info(f"   💾 Arquivo atualizado: {py_file.name}")
                    self.fixes_log.append(f"Imports corrigidos: {py_file.name}")
                    
            except Exception as e:
                logger.error(f"❌ Erro processando {py_file.name}: {e}")
    
    def verify_fixes(self):
        """Verifica se as correções foram aplicadas"""
        logger.info("🧪 VERIFICANDO CORREÇÕES...")
        
        # Testar imports críticos
        test_modules = [
            ('jwt', 'PyJWT'),
            ('networkx', 'NetworkX'),
            ('jose.jwt', 'Python-JOSE')
        ]
        
        working_modules = []
        failed_modules = []
        
        for module_path, module_name in test_modules:
            try:
                if module_path == 'jwt':
                    import jwt
                    working_modules.append(f"{module_name} v{jwt.__version__}")
                elif module_path == 'networkx':
                    import networkx as nx
                    working_modules.append(f"{module_name} v{nx.__version__}")
                elif module_path == 'jose.jwt':
                    from jose import jwt as jose_jwt
                    working_modules.append(f"{module_name} OK")
                    
            except ImportError as e:
                failed_modules.append(f"{module_name}: {e}")
        
        # Verificar se core module foi criado
        try:
            from suna_alsham_core.core import quantum_core
            working_modules.append("Core Module OK")
        except ImportError as e:
            failed_modules.append(f"Core Module: {e}")
        
        # Relatório final
        logger.info("="*60)
        logger.info("📋 RELATÓRIO DE VERIFICAÇÃO")
        logger.info("="*60)
        
        if working_modules:
            logger.info("✅ MÓDULOS FUNCIONANDO:")
            for module in working_modules:
                logger.info(f"   - {module}")
        
        if failed_modules:
            logger.info("❌ MÓDULOS COM PROBLEMAS:")
            for module in failed_modules:
                logger.info(f"   - {module}")
        
        logger.info(f"\n📊 CORREÇÕES APLICADAS ({len(self.fixes_log)}):")
        for i, fix in enumerate(self.fixes_log, 1):
            logger.info(f"{i:2d}. {fix}")
        
        return len(failed_modules) == 0
    
    def run_complete_fix(self):
        """Executa correção completa"""
        logger.info("🔥 INICIANDO CORREÇÃO COMPLETA RAILWAY")
        
        try:
            # Passo 1: Criar requirements
            self.create_requirements_file()
            
            # Passo 2: Instalar dependências  
            self.install_dependencies_railway()
            
            # Passo 3: Criar módulo core
            self.create_core_module()
            
            # Passo 4: Corrigir imports
            self.fix_import_structure()
            
            # Passo 5: Verificar tudo
            success = self.verify_fixes()
            
            if success:
                logger.info("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
                logger.info("▶️  Execute agora: python agent_loader.py")
            else:
                logger.warning("⚠️  Correção concluída mas alguns problemas persistem")
                
        except Exception as e:
            logger.error(f"💥 Erro durante correção: {e}")
            raise

if __name__ == "__main__":
    fixer = RailwayFixer()
    fixer.run_complete_fix()
