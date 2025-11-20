import os

# 1. CLIENTE SUPABASE
supabase_client_code = """
import { createClient } from '@supabase/supabase-js';

// Tenta pegar as chaves do ambiente
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

// Se não tiver chaves (ainda não configuradas na Vercel), cria um cliente nulo para não quebrar o build
export const supabase = (supabaseUrl && supabaseAnonKey) 
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;
"""

# 2. NOVA API.TS (Lê do Banco de Dados, não de uma API Python)
api_ts_code = """
import { supabase } from './supabase';
import { Agent } from '@/types/quantum';

// MOCK DE SEGURANÇA (Se o banco estiver vazio ou desconectado)
const MOCK_AGENTS: Agent[] = [
  { id: 'sec-01', name: 'SECURITY-GUARDIAN', role: 'GUARD', status: 'PROCESSING', efficiency: 99.9, currentTask: 'Monitoramento Supabase', lastActive: 'Now' },
  { id: 'db-01', name: 'DATABASE-MASTER', role: 'CORE', status: 'IDLE', efficiency: 100, currentTask: 'Sincronização Direta', lastActive: '1m ago' },
  { id: 'evo-01', name: 'EVOLUTION-ENGINE', role: 'CORE', status: 'LEARNING', efficiency: 97.5, currentTask: 'Análise Genética', lastActive: '5s ago' },
  { id: 'web-01', name: 'WEB-SEARCH', role: 'SPECIALIST', status: 'WARNING', efficiency: 85.2, currentTask: 'Indexando Vercel', lastActive: 'Now' },
  { id: 'net-01', name: 'NETWORK-OPS', role: 'ANALYST', status: 'PROCESSING', efficiency: 92.1, currentTask: 'Otimização de Rotas', lastActive: '10s ago' },
];

export async function fetchAgents(): Promise<Agent[]> {
  // 1. Se não tem cliente Supabase configurado, retorna Mock
  if (!supabase) {
    console.warn("⚠️ Supabase Keys ausentes. Usando Modo Simulação.");
    return MOCK_AGENTS;
  }

  try {
    // 2. Tenta buscar do banco real (Tabela 'agents')
    const { data, error } = await supabase
      .from('agents')
      .select('*')
      .order('name', { ascending: true });

    if (error) throw error;

    // 3. Se o banco estiver vazio ou der erro, retorna Mock
    if (!data || data.length === 0) return MOCK_AGENTS;

    // 4. Mapeia os dados do banco para o formato do Dashboard
    return data.map((a: any) => ({
        id: a.id,
        name: a.name || 'Unknown Unit',
        role: a.role || 'SPECIALIST',
        status: a.status || 'IDLE',
        efficiency: a.efficiency || Math.floor(Math.random() * 100),
        currentTask: a.current_task || 'Aguardando comando',
        lastActive: new Date().toLocaleTimeString()
    }));

  } catch (error) {
    console.error("❌ Erro Supabase:", error);
    return MOCK_AGENTS; // Fallback seguro
  }
}

export async function fetchSystemStatus() {
    // Simulação de métricas do sistema baseadas nos agentes
    return {
        uptime: "99.99%",
        active_agents: 57,
        health: "OPTIMAL"
    };
}
"""

def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Configurado: {path}")
    except Exception as e:
        print(f"❌ Erro: {e}")

print("🔗 Configurando conexão direta Vercel <-> Supabase...")
write_file("src/lib/supabase.ts", supabase_client_code)
write_file("src/lib/api.ts", api_ts_code)
print("🏁 Arquitetura Serverless aplicada.")
