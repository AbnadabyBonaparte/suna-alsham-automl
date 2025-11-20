import os
import json

def check_file(path):
    exists = os.path.exists(path)
    status = "✅ EXISTE" if exists else "❌ AUSENTE"
    print(f"[{status}] {path}")
    return exists

def check_json_version(path, pkg_name):
    if not os.path.exists(path):
        return
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            deps = data.get('dependencies', {})
            ver = deps.get(pkg_name, "Não listado")
            print(f"   ℹ️ {pkg_name}: {ver}")
    except Exception as e:
        print(f"   ⚠️ Erro ao ler JSON: {e}")

print("\n--- 📂 INICIANDO AUDITORIA FORENSE: ALSHAM QUANTUM ---\n")

# Verifica Root do Frontend
base_dir = "frontend"
if not os.path.exists(base_dir):
    print(f"❌ ERRO CRÍTICO: Pasta '{base_dir}' não encontrada. Você está na raiz do repo?")
    base_dir = "." # Tenta na raiz atual
else:
    print(f"✅ Pasta '{base_dir}' detectada.")

# 1. Verifica Dependências Críticas (React 19 / Next 15)
pkg_path = os.path.join(base_dir, "package.json")
if check_file(pkg_path):
    print("   🔍 Verificando Versões do Core:")
    check_json_version(pkg_path, "next")
    check_json_version(pkg_path, "react")
    check_json_version(pkg_path, "@react-three/fiber")
    check_json_version(pkg_path, "@supabase/supabase-js")

# 2. Verifica Estrutura de Pastas (App Router)
print("\n🔍 Verificando Estrutura de Rotas (App Router):")
routes = [
    "app/page.tsx",
    "app/dashboard/page.tsx",
    "app/dashboard/network/page.tsx",
    "app/dashboard/agents/page.tsx",
    "app/dashboard/matrix/page.tsx",
    "app/layout.tsx"
]
for r in routes:
    check_file(os.path.join(base_dir, r))

# 3. Verifica Camada de Dados
print("\n🔍 Verificando Camada de Dados:")
api_path = os.path.join(base_dir, "src/lib/api.ts")
store_path = os.path.join(base_dir, "src/store/useStore.ts")
check_file(api_path)
check_file(store_path)

# 4. Verifica Variáveis de Ambiente
print("\n🔍 Verificando Credenciais:")
env_path = os.path.join(base_dir, ".env.local")
if check_file(env_path):
    print("   ⚠️ O arquivo existe. Verificando se tem conteúdo (sem expor)...")
    with open(env_path, 'r') as f:
        content = f.read()
        has_url = "NEXT_PUBLIC_SUPABASE_URL" in content
        has_key = "NEXT_PUBLIC_SUPABASE_ANON_KEY" in content
        print(f"   -> Contém URL do Supabase? {'✅ Sim' if has_url else '❌ Não'}")
        print(f"   -> Contém Chave Anon? {'✅ Sim' if has_key else '❌ Não'}")
else:
    print("   ❌ Arquivo .env.local NÃO encontrado. O sistema rodará em modo MOCK.")

print("\n--- 🏁 AUDITORIA LOCAL CONCLUÍDA ---")
