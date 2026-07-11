// ═══════════════════════════════════════════════════════════════
// ROTEADOR DE AGENTS - USA ESTRUTURA EXISTENTE (SERVER-ONLY)
// ═══════════════════════════════════════════════════════════════

import { createAdminClient } from '@/lib/supabase/admin';
import { Agent, AgentRole, AgentStatus, ACTIVE_STATUSES } from './types';

// Palavras-chave para roteamento por ROLE (não squad)
const ROLE_KEYWORDS: Record<AgentRole, string[]> = {
  CORE: [
    'orquestrar',
    'coordenar',
    'sincronizar',
    'master',
    'principal',
    'deploy',
    'database',
    'api',
    'gateway',
    'load balancer',
  ],
  GUARD: [
    'segurança',
    'security',
    'proteção',
    'backup',
    'monitor',
    'vigilância',
    'firewall',
    'audit',
    'compliance',
  ],
  ANALYST: [
    'análise',
    'dados',
    'relatório',
    'previsão',
    'insight',
    'metrics',
    'performance',
    'trend',
    'forecast',
  ],
  SPECIALIST: [
    'venda',
    'marketing',
    'email',
    'social',
    'conteúdo',
    'lead',
    'revenue',
    'ads',
    'support',
    'cache',
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

// ─────────────────────────────────────────────────────────────
// ROTEAMENTO PURO (determinístico, sem I/O) — testável isoladamente
// ─────────────────────────────────────────────────────────────

/**
 * Resolve o NOME do agente especialista a partir da descrição da tarefa,
 * casando por palavras-chave de especialização. Determinístico: percorre
 * AGENT_SPECIALIZATIONS na ordem de inserção e retorna o primeiro match.
 */
export function resolveAgentName(taskDescription: string): string | null {
  const lowerDesc = taskDescription.toLowerCase();
  for (const [agentName, keywords] of Object.entries(AGENT_SPECIALIZATIONS)) {
    if (keywords.some((kw) => lowerDesc.includes(kw))) {
      return agentName;
    }
  }
  return null;
}

/**
 * Resolve o ROLE-alvo pela contagem de palavras-chave. Empates mantêm o
 * primeiro role com maior score (ordem: CORE, GUARD, ANALYST, SPECIALIST);
 * sem nenhum match retorna 'CORE' (default).
 */
export function resolveRole(taskDescription: string): AgentRole {
  const lowerDesc = taskDescription.toLowerCase();
  let targetRole: AgentRole = 'CORE';
  let bestScore = 0;
  for (const [role, keywords] of Object.entries(ROLE_KEYWORDS)) {
    const score = keywords.filter((kw) => lowerDesc.includes(kw)).length;
    if (score > bestScore) {
      bestScore = score;
      targetRole = role as AgentRole;
    }
  }
  return targetRole;
}

// Busca um agente específico pelo id (usado quando o usuário escolhe no picker)
export async function getAgentById(agentId: string): Promise<Agent | null> {
  const supabase = createAdminClient();
  const { data } = await supabase.from('agents').select('*').eq('id', agentId).single();
  return (data as Agent) || null;
}

export async function routeToAgent(taskDescription: string): Promise<Agent> {
  const supabase = createAdminClient();

  // 1. Tentar match por nome do agent (especialização) — decisão pura
  const specialistName = resolveAgentName(taskDescription);
  if (specialistName) {
    const { data: agent } = await supabase
      .from('agents')
      .select('*')
      .eq('name', specialistName)
      .in('status', ACTIVE_STATUSES)
      .single();

    if (agent) return agent as Agent;
  }

  // 2. Match por ROLE — decisão pura
  const targetRole = resolveRole(taskDescription);

  // 3. Buscar agent disponível com maior efficiency
  const { data: agents } = await supabase
    .from('agents')
    .select('*')
    .eq('role', targetRole)
    .in('status', ACTIVE_STATUSES)
    .order('efficiency', { ascending: false })
    .limit(5);

  if (agents && agents.length > 0) {
    // Escolher o com menor neural_load entre os top 5
    const sorted = agents.sort((a, b) => (a.neural_load || 0) - (b.neural_load || 0));
    return sorted[0] as Agent;
  }

  // 4. Fallback: ORCHESTRATOR ALPHA
  const { data: orchestrator } = await supabase
    .from('agents')
    .select('*')
    .eq('name', 'ORCHESTRATOR ALPHA')
    .single();

  if (orchestrator) return orchestrator as Agent;

  // 5. Último recurso: qualquer agent operacional
  const { data: anyAgent } = await supabase
    .from('agents')
    .select('*')
    .in('status', ACTIVE_STATUSES)
    .order('efficiency', { ascending: false })
    .limit(1)
    .single();

  if (anyAgent) return anyAgent as Agent;

  throw new Error('No available agents found');
}

export async function updateAgentStatus(
  agentId: string,
  status: AgentStatus,
  currentTask?: string,
): Promise<void> {
  const supabase = createAdminClient();

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
  const supabase = createAdminClient();

  const { data: agent } = await supabase
    .from('agents')
    .select('neural_load')
    .eq('id', agentId)
    .single();

  if (agent) {
    const newLoad = Math.min(100, (agent.neural_load || 0) + amount);
    await supabase.from('agents').update({ neural_load: newLoad }).eq('id', agentId);
  }
}

export async function decrementNeuralLoad(agentId: string, amount: number = 10): Promise<void> {
  const supabase = createAdminClient();

  const { data: agent } = await supabase
    .from('agents')
    .select('neural_load')
    .eq('id', agentId)
    .single();

  if (agent) {
    const newLoad = Math.max(0, (agent.neural_load || 0) - amount);
    await supabase.from('agents').update({ neural_load: newLoad }).eq('id', agentId);
  }
}
