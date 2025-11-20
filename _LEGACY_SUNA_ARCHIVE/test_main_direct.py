#!/usr/bin/env python3
"""
Testa o main_complete_system_v2.py e mostra erros
"""

import sys
import traceback
import subprocess

print("🔍 TESTANDO MAIN_COMPLETE_SYSTEM_V2.PY", flush=True)
print("="*50, flush=True)

# Método 1: Tentar importar
print("\n1️⃣ Tentando importar o módulo...", flush=True)
try:
    import main_complete_system_v2
    print("✅ Import bem-sucedido!", flush=True)
except Exception as e:
    print(f"❌ Erro no import: {e}", flush=True)
    print("Traceback:", flush=True)
    traceback.print_exc()

# Método 2: Executar como subprocess
print("\n2️⃣ Tentando executar como subprocess...", flush=True)
try:
    result = subprocess.run(
        [sys.executable, "main_complete_system_v2.py"],
        capture_output=True,
        text=True,
        timeout=10
    )
    print(f"Return code: {result.returncode}", flush=True)
    if result.stdout:
        print("STDOUT:", flush=True)
        print(result.stdout, flush=True)
    if result.stderr:
        print("STDERR:", flush=True)
        print(result.stderr, flush=True)
except subprocess.TimeoutExpired:
    print("❌ Timeout após 10 segundos", flush=True)
except Exception as e:
    print(f"❌ Erro executando: {e}", flush=True)

# Método 3: Ver o conteúdo do arquivo
print("\n3️⃣ Primeiras 20 linhas do arquivo:", flush=True)
try:
    with open("main_complete_system_v2.py", "r") as f:
        lines = f.readlines()[:20]
        for i, line in enumerate(lines, 1):
            print(f"{i:2d}: {line.rstrip()}", flush=True)
    print(f"\n📊 Total de linhas: {len(open('main_complete_system_v2.py').readlines())}", flush=True)
except Exception as e:
    print(f"❌ Erro lendo arquivo: {e}", flush=True)

print("\n✅ Teste concluído!", flush=True)
