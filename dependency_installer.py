#!/usr/bin/env python3
"""
ALSHAM QUANTUM - Correção Automática de Dependências
"""
import subprocess
import sys
import importlib

class DependencyFixer:
    def __init__(self):
        self.missing_deps = []
        self.critical_modules = [
            'jwt', 'PyJWT', 'networkx', 'jose', 'cryptography'
        ]
    
    def check_dependencies(self):
        """Verifica dependências críticas"""
        print("🔍 Verificando dependências críticas...")
        
        for module in self.critical_modules:
            try:
                if module == 'jwt':
                    import jwt
                elif module == 'PyJWT':
                    import jwt
                elif module == 'networkx':
                    import networkx
                elif module == 'jose':
                    import jose
                elif module == 'cryptography':
                    import cryptography
                    
                print(f"✅ {module} - OK")
            except ImportError:
                print(f"❌ {module} - FALTANDO")
                self.missing_deps.append(module)
    
    def install_missing(self):
        """Instala dependências faltando"""
        if not self.missing_deps:
            print("✅ Todas as dependências estão OK!")
            return
        
        print(f"📦 Instalando {len(self.missing_deps)} dependências...")
        
        packages = {
            'jwt': 'PyJWT==2.8.0',
            'PyJWT': 'PyJWT==2.8.0', 
            'networkx': 'networkx==3.2.1',
            'jose': 'python-jose[cryptography]==3.3.0',
            'cryptography': 'cryptography==41.0.7'
        }
        
        for dep in self.missing_deps:
            if dep in packages:
                try:
                    subprocess.check_call([
                        sys.executable, '-m', 'pip', 'install', 
                        packages[dep]
                    ])
                    print(f"✅ {dep} instalado com sucesso!")
                except Exception as e:
                    print(f"❌ Erro instalando {dep}: {e}")

if __name__ == "__main__":
    fixer = DependencyFixer()
    fixer.check_dependencies()
    fixer.install_missing()
