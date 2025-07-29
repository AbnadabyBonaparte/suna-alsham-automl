import os
import sys
import time

print("--- INICIANDO DIAGNÓSTICO DO CONTAINER ---")
print(f"Data e Hora do Diagnóstico: {time.ctime()}")

# 1. Onde estamos? (Diretório de Trabalho Atual)
current_directory = os.getcwd()
print(f"[*] Diretório de Trabalho Atual: {current_directory}")

# 2. O que tem na pasta principal?
try:
    app_root_contents = os.listdir(current_directory)
    print(f"[*] Conteúdo da Pasta Principal ({current_directory}):")
    for item in app_root_contents:
        print(f"    - {item}")
except Exception as e:
    print(f"[!] Erro ao listar a pasta principal: {e}")

# 3. A pasta que precisamos (domain_modules) existe?
domain_modules_path = os.path.join(current_directory, "domain_modules")
print("\n--- VERIFICAÇÃO PRINCIPAL ---")
if "domain_modules" in app_root_contents:
    print(">>> ✅ SUCESSO: A pasta 'domain_modules' FOI ENCONTRADA!")
    try:
        domain_contents = os.listdir(domain_modules_path)
        print(f"[*] Conteúdo de 'domain_modules': {domain_contents}")
    except Exception as e:
        print(f"[!] Erro ao listar 'domain_modules': {e}")
else:
    print(">>> ❌ FALHA CRÍTICA: A pasta 'domain_modules' NÃO FOI ENCONTRADA NA PASTA PRINCIPAL.")
    print(">>> Causa provável: O arquivo .dockerignore pode estar excluindo a pasta.")

print("--- FIM DO DIAGNÓSTICO ---")

# 4. Sair do programa para vermos apenas o log de diagnóstico.
# O deploy vai falhar de propósito, o que é o que queremos.
sys.exit(1)
