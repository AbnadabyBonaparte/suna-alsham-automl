# diagnostic_complete.py
import os
import sys
import json
import subprocess
from datetime import datetime

print("🔍 DIAGNÓSTICO COMPLETO SUNA-ALSHAM")
print(f"⏰ Executado em: {datetime.now()}")
print("="*60)

# 1. Verificar Python e ambiente
print("\n📌 AMBIENTE:")
print(f"Python: {sys.version}")
print(f"Path: {sys.executable}")
print(f"Working Dir: {os.getcwd()}")

# 2. Listar TODOS os arquivos
print("\n📁 ESTRUTURA COMPLETA:")
for root, dirs, files in os.walk('.'):
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for f in files:
        if f.endswith('.py'):
            print(f"{subindent}{f}")

# 3. Verificar dependências
print("\n📦 DEPENDÊNCIAS:")
deps = ['psutil', 'redis', 'aiohttp', 'autopep8', 'openai']
for dep in deps:
    try:
        __import__(dep)
        print(f"✅ {dep} instalado")
    except:
        print(f"❌ {dep} FALTANDO")

# 4. Tentar importar cada módulo
print("\n🔧 TESTE DE IMPORTS:")
modules = [
    'multi_agent_network',
    'specialized_agents',
    'ai_powered_agents',
    'core_agents_v3',
    'system_agents',
    'service_agents',
    'meta_cognitive_agents'
]

for mod in modules:
    try:
        __import__(mod)
        print(f"✅ {mod} importado")
    except Exception as e:
        print(f"❌ {mod}: {str(e)}")

# 5. Salvar relatório
report = {
    "timestamp": str(datetime.now()),
    "python_version": sys.version,
    "working_dir": os.getcwd(),
    "files_found": [],
    "import_errors": []
}

with open('diagnostic_report.json', 'w') as f:
    json.dump(report, f, indent=2)

print("\n💾 Relatório salvo: diagnostic_report.json")
