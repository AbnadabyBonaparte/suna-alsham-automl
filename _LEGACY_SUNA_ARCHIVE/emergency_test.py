#!/usr/bin/env python3
"""
TESTE DE EMERGÊNCIA - SUNA-ALSHAM
Descobre porque o container não inicia
"""

import os
import sys
import time

print("🚨 TESTE DE EMERGÊNCIA INICIADO", flush=True)
print(f"⏰ Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
print("="*50, flush=True)

# 1. Informações básicas
print("\n📌 AMBIENTE:", flush=True)
print(f"Python: {sys.version}", flush=True)
print(f"Working Dir: {os.getcwd()}", flush=True)
print(f"Files in root: {len(os.listdir('.'))}", flush=True)

# 2. Listar arquivos Python
print("\n📁 ARQUIVOS PYTHON:", flush=True)
py_files = [f for f in os.listdir('.') if f.endswith('.py')]
for f in py_files[:10]:  # Primeiros 10
    print(f"  - {f}", flush=True)

# 3. Verificar arquivo principal
print("\n🔍 VERIFICANDO ARQUIVO PRINCIPAL:", flush=True)
if os.path.exists('main_complete_system_v2.py'):
    print("✅ main_complete_system_v2.py EXISTE", flush=True)
    size = os.path.getsize('main_complete_system_v2.py')
    print(f"   Tamanho: {size} bytes", flush=True)
else:
    print("❌ main_complete_system_v2.py NÃO ENCONTRADO!", flush=True)

# 4. Teste de imports básicos
print("\n📦 TESTE DE IMPORTS:", flush=True)
try:
    import asyncio
    print("✅ asyncio OK", flush=True)
except:
    print("❌ asyncio FALHOU", flush=True)

try:
    import logging
    print("✅ logging OK", flush=True)
except:
    print("❌ logging FALHOU", flush=True)

# 5. Keep alive por 30 segundos
print("\n💓 MANTENDO VIVO POR 30 SEGUNDOS...", flush=True)
for i in range(6):
    print(f"   Alive {i*5}/30 segundos...", flush=True)
    time.sleep(5)

print("\n✅ TESTE CONCLUÍDO!", flush=True)
print("Se você vir esta mensagem, o Python está funcionando!", flush=True)
