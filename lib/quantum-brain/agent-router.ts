// ═══════════════════════════════════════════════════════════════
// ROTEADOR DE AGENTS - USA ESTRUTURA EXISTENTE
// ═══════════════════════════════════════════════════════════════

import { createClient } from '@/lib/supabase/client';
import { Agent, AgentRole } from './types';

// Palavras-chave para roteamento por ROLE (não squad)
const ROLE_KEYWORDS: Record<AgentRole, string[]> = {
  CORE: [
    'orquestrar', 'coordenar', 'sincronizar', 'master', 'principal',
    'deploy', 'database', 'api', 'gateway', 'load balancer'
  ],
  GUARD: [
    'segurança', 'security', 'proteção', 'backup', 'monitor',
    'vigilância', 'firewall', 'audit', 'compliance'
  ],
  ANALYST: [
    'análise', 'dados', 'relatório', 'previsão', 'insight',
    'metrics', 'performance', 'trend', 'forecast'
  ],
  SPECIALIST: [
    'venda', 'marketing', 'email', 'social', 'conteúdo',
    'lead', 'revenue', 'ads', 'support', 'cache'
  ],
};

// Mapeamento de nomes de agents para tarefas específicas
const AGENT_SPECIALIZATIONS: Record<string, string[]> = {
  'ORCHESTRATOR ALPHA': ['coordenar', 'orquestrar', 'geral'],
  'SECURITY GUARDIAN': ['segurança', 'proteção', 'vulnerabilidade'],
  'DATA MINER': ['dados', 'mineração', 'extração'],
  'LEAD MAGNET': ['lead', 'captura', 'prospecção'],
  'EMAIL SEQUENCE BOT': ['email', 'sequência', 'automação'],
  'REVENUE HUNTER': ['receita', 'venda', 'conversão'],
  'CONTENT CREATOR': ['conteúdo', 'artigo', 'post'],
  'SOCIAL ENGAGER': ['social', 'engajamento', 'rede'],
  'ADS OPTIMIZER': ['anúncio', 'ads', 'campanha'],
  'BACKUP KEEPER': ['backup', 'restauração', 'recovery'],
};

export async function routeToAgent(taskDescription: string): Promise<Agent> {
  const supabase = createClient();
  const lowerDesc = taskDescription.toLowerCase();
  
  // 1. Tentar match por nome do agent (especialização)
  for (const [agentName, keywords] of Object.entries(AGENT_SPECIALIZATIONS)) {
    if (keywords.some(kw => lowerDesc.includes(kw))) {
      const { data: agent } = await supabase
        .from('agents')
        .select('*')
        .eq('name', agentName)
        .eq('status', 'ACTIVE')
        .single();
      
      if (agent) return agent as Agent;
    }
  }
  
  // 2. Match por ROLE
  let targetRole: AgentRole = 'CORE'; // Default
  let bestScore = 0;
  
  for (const [role, keywords] of Object.entries(ROLE_KEYWORDS)) {
    const score = keywords.filter(kw => lowerDesc.includes(kw)).length;
    if (score > bestScore) {
      bestScore = score;
      targetRole = role as AgentRole;
    }
  }
  
  // 3. Buscar agent disponível com maior efficiency
  const { data: agents } = await supabase
    .from('agents')
    .select('*')
    .eq('role', targetRole)
    .eq('status', 'ACTIVE')
    .order('efficiency', { ascending: false })
    .limit(5);
  
  if (agents && agents.length > 0) {
    // Escolher o com menor neural_load entre os top 5
    const sorted = agents.sort((a, b) => a.neural_load - b.neural_load);
    return sorted[0] as Agent;
  }
  
  // 4. Fallback: ORCHESTRATOR ALPHA
  const { data: orchestrator } = await supabase
    .from('agents')
    .select('*')
    .eq('name', 'ORCHESTRATOR ALPHA')
    .single();
  
  if (orchestrator) return orchestrator as Agent;
  
  // 5. Último recurso: qualquer agent ativo
  const { data: anyAgent } = await supabase
    .from('agents')
    .select('*')
    .eq('status', 'ACTIVE')
    .order('efficiency', { ascending: false })
    .limit(1)
    .single();
  
  if (anyAgent) return anyAgent as Agent;
  
  throw new Error('No available agents found');
}

export async function updateAgentStatus(
  agentId: string, 
  status: 'ACTIVE' | 'IDLE' | 'WARNING',
  currentTask?: string
): Promise<void> {
  const supabase = createClient();
  
  await supabase
    .from('agents')
    .update({
      status,
      current_task: currentTask || 'Aguardando comando',
      last_active: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    })
    .eq('id', agentId);
}

export async function incrementNeuralLoad(agentId: string, amount: number = 10): Promise<void> {
  const supabase = createClient();
  
  // Buscar load atual
  const { data: agent } = await supabase
    .from('agents')
    .select('neural_load')
    .eq('id', agentId)
    .single();
  
  if (agent) {
    const newLoad = Math.min(100, (agent.neural_load || 0) + amount);
    await supabase
      .from('agents')
      .update({ neural_load: newLoad })
      .eq('id', agentId);
  }
}

export async function decrementNeuralLoad(agentId: string, amount: number = 10): Promise<void> {
  const supabase = createClient();
  
  const { data: agent } = await supabase
    .from('agents')
    .select('neural_load')
    .eq('id', agentId)
    .single();
  
  if (agent) {
    const newLoad = Math.max(0, (agent.neural_load || 0) - amount);
    await supabase
      .from('agents')
      .update({ neural_load: newLoad })
      .eq('id', agentId);
  }
}
