import os

# Código que FORÇA a URL de produção
api_code = """
// ENDEREÇO FIXO DO CÉREBRO (RAILWAY)
// Não usamos mais localhost nem variáveis de ambiente por enquanto para garantir a conexão.
const API_URL = "https://suna-alsham-automl-production.up.railway.app";

export async function fetchSystemStatus() {
  try {
    console.log(`📡 Conectando ao Cérebro em: ${API_URL}...`);
    const res = await fetch(`${API_URL}/api/system/status`, { 
      next: { revalidate: 0 }, // Desativa cache de fetch para dados frescos
      headers: { 'Content-Type': 'application/json' }
    });
    if (!res.ok) throw new Error(`Erro HTTP: ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn("⚠️ Backend Offline ou Bloqueado. Ativando Modo Simulação.");
    return null;
  }
}

export async function fetchAgents() {
  try {
    const res = await fetch(`${API_URL}/api/agents`, { 
      next: { revalidate: 0 },
      headers: { 'Content-Type': 'application/json' }
    });
    if (!res.ok) throw new Error(`Erro HTTP: ${res.status}`);
    const data = await res.json();
    return data.agents || []; // Garante que retorna array
  } catch (error) {
    console.error("❌ Erro ao buscar agentes:", error);
    return []; // Retorna array vazio para não quebrar a UI
  }
}
"""

def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ API Real Configurada: {path}")
    except Exception as e:
        print(f"❌ Erro: {e}")

print("🔗 Forçando conexão direta com Railway...")
write_file("src/lib/api.ts", api_code)
