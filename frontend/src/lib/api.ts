const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchSystemStatus() {
  try {
    // Tenta buscar do backend real
    const res = await fetch(`${API_URL}/api/system/status`, { next: { revalidate: 10 } });
    if (!res.ok) throw new Error('Falha na conexão neural');
    return res.json();
  } catch (error) {
    console.warn("⚠️ Backend Offline. Usando dados de fallback holográficos.");
    return null; // Retorna null para a UI saber que deve usar fallback
  }
}

export async function fetchAgents() {
  try {
    const res = await fetch(`${API_URL}/api/agents`, { next: { revalidate: 5 } });
    if (!res.ok) throw new Error('Falha ao listar agentes');
    return res.json();
  } catch (error) {
    return [];
  }
}