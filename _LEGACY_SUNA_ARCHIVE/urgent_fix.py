#!/usr/bin/env python3
"""
CORREÇÃO URGENTE - ALSHAM QUANTUM
Corrige estrutura de imports + dependências
"""
import os
import sys
import subprocess
import re

class UrgentFixer:
    def __init__(self):
        self.fixes_applied = []
        
    def install_dependencies(self):
        """Instala dependências críticas"""
        print("🔧 INSTALANDO DEPENDÊNCIAS CRÍTICAS...")
        
        dependencies = [
            "PyJWT==2.8.0",
            "networkx==3.2.1", 
            "python-jose[cryptography]==3.3.0"
        ]
        
        for dep in dependencies:
            try:
                print(f"📦 Instalando {dep}...")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', dep
                ], capture_output=True, text=True, check=True)
                print(f"✅ {dep} instalado!")
                self.fixes_applied.append(f"Dependência: {dep}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro instalando {dep}: {e}")
    
    def fix_agent_loader_imports(self):
        """Corrige imports quebrados no agent_loader.py"""
        print("\n🔧 CORRIGINDO IMPORTS NO AGENT_LOADER...")
        
        if not os.path.exists('agent_loader.py'):
            print("❌ agent_loader.py não encontrado!")
            return
        
        with open('agent_loader.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Correções de import paths
        import_fixes = {
            # Remover prefixos incorretos
            'suna_alsham_core.agents.': '',
            'suna_alsham_core.core.': '',
            'suna_alsham_core.': '',
            
            # Imports diretos para arquivos locais
            'from security_guardian_agent import': 'from security_guardian_agent import',
            'from performance_monitor_agent import': 'from performance_monitor_agent import',
            'from meta_cognitive_agents import': 'from meta_cognitive_agents import',
        }
        
        original_content = content
        for old_import, new_import in import_fixes.items():
            if old_import in content:
                content = content.replace(old_import, new_import)
                print(f"   ✅ Corrigido: {old_import} → {new_import}")
                self.fixes_applied.append(f"Import: {old_import}")
        
        # Salvar correções
        if content != original_content:
            with open('agent_loader.py', 'w', encoding='utf-8') as f:
                f.write(content)
            print("   💾 agent_loader.py atualizado!")
    
    def create_missing_core_module(self):
        """Cria módulo core faltando se necessário"""
        print("\n🔧 VERIFICANDO MÓDULO CORE...")
        
        if not os.path.exists('core.py'):
            print("📄 Criando core.py básico...")
            core_content = '''"""
ALSHAM QUANTUM - Core Module
Módulo base para compatibilidade
"""

class QuantumCore:
    def __init__(self):
        self.version = "1.0.0"
        self.status = "operational"
    
    def get_status(self):
        return self.status

# Instância global
quantum_core = QuantumCore()
'''
            with open('core.py', 'w', encoding='utf-8') as f:
                f.write(core_content)
            print("✅ core.py criado!")
            self.fixes_applied.append("Módulo: core.py criado")
    
    def test_imports(self):
        """Testa se os imports críticos funcionam"""
        print("\n🧪 TESTANDO IMPORTS CRÍTICOS...")
        
        test_modules = ['jwt', 'networkx', 'jose']
        
        for module in test_modules:
            try:
                if module == 'jwt':
                    import jwt
                    print(f"✅ {module} - OK (versão: {jwt.__version__})")
                elif module == 'networkx':
                    import networkx
                    print(f"✅ {module} - OK (versão: {networkx.__version__})")
                elif module == 'jose':
                    from jose import jwt as jose_jwt
                    print(f"✅ {module} - OK")
            except ImportError as e:
                print(f"❌ {module} - FALHOU: {e}")
    
    def generate_summary(self):
        """Gera resumo das correções aplicadas"""
        print("\n" + "="*60)
        print("📋 RESUMO DAS CORREÇÕES APLICADAS")
        print("="*60)
        
        if self.fixes_applied:
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"{i:2d}. {fix}")
        else:
            print("❌ Nenhuma correção foi aplicada")
        
        print(f"\nTotal de correções: {len(self.fixes_applied)}")
        
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Execute: python agent_loader.py")
        print("2. Verifique se os 31+ agentes carregam sem erros")
        print("3. Confirme se chegamos aos 36 agentes CORE")

if __name__ == "__main__":
    print("🔧 ALSHAM QUANTUM - CORREÇÃO URGENTE")
    print("="*50)
    
    fixer = UrgentFixer()
    
    # Executar todas as correções
    fixer.install_dependencies()
    fixer.fix_agent_loader_imports()  
    fixer.create_missing_core_module()
    fixer.test_imports()
    fixer.generate_summary()
    
    print("\n✅ CORREÇÕES CONCLUÍDAS!")
    print("Execute agora: python agent_loader.py")
