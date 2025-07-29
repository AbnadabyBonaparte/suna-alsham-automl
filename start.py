import time
import sys

print("--- INICIANDO TESTE 'HELLO WORLD' ---")
print(f"Versão do Python: {sys.version}")
print("Teste de log simples. Se você está vendo isso, o CMD do Docker e o Railway estão funcionando.")
print("O sistema irá dormir por 60 segundos para nos dar tempo de ler o log.")
print("--- TESTE CONCLUÍDO ---")

# Mantém o container vivo por um minuto para podermos ler os logs
time.sleep(60)

# Sai com sucesso
sys.exit(0)
