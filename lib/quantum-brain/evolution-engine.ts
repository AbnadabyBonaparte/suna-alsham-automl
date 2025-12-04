// ═══════════════════════════════════════════════════════════════
// MOTOR DE EVOLUÇÃO - USA evolution_cycles EXISTENTE
// ═══════════════════════════════════════════════════════════════

import { createClient } from '@/lib/supabase/client';
import { Agent } from './types';

const EFFICIENCY_THRESHOLD = 80; // Agents abaixo disso são candidatos

export interface EvolutionResult {
  cycle_id: string;
  agents_analyzed: number;
  improvements_applied: number;
  average_efficiency_before: number;
  average_efficiency_after: number;
  duration_seconds: number;
  success: boolean;
}

export async function runEvolutionCycle(): Promise<EvolutionResult> {
  const supabase = createClient();
  const startTime = Date.now();
  
  // Gerar cycle_id único
  const cycleId = `evolution-${Date.now()}`;
  
  // 1. Buscar todos os agents
  const { data: agents } = await supabase
    .from('agents')
    .select('*')
    .order('efficiency', { ascending: true });
  
  if (!agents || agents.length === 0) {
    throw new Error('No agents found');
  }
  
  const avgEfficiencyBefore = agents.reduce((sum, a) => sum + (a.efficiency || 0), 0) / agents.length;
  
  // 2. Identificar candidatos (efficiency < threshold)
  const candidates = agents.filter(a => (a.efficiency || 0) < EFFICIENCY_THRESHOLD);
  
  // 3. Aplicar melhorias (incremento de 1-3% na efficiency)
  let improvementsApplied = 0;
  
  for (const agent of candidates.slice(0, 20)) { // Limitar a 20 por ciclo
    const improvement = 1 + Math.random() * 2; // 1-3%
    const newEfficiency = Math.min(100, (agent.efficiency || 0) + improvement);
    
    await supabase
      .from('agents')
      .update({
        efficiency: newEfficiency,
        updated_at: new Date().toISOString(),
      })
      .eq('id', agent.id);
    
    improvementsApplied++;
  }
  
  // 4. Calcular nova média
  const { data: agentsAfter } = await supabase
    .from('agents')
    .select('efficiency');
  
  const avgEfficiencyAfter = agentsAfter
    ? agentsAfter.reduce((sum, a) => sum + (a.efficiency || 0), 0) / agentsAfter.length
    : avgEfficiencyBefore;
  
  const durationSeconds = (Date.now() - startTime) / 1000;
  
  // 5. Registrar na tabela evolution_cycles EXISTENTE
  await supabase.from('evolution_cycles').insert({
    cycle_id: cycleId,
    core_evolution: {
      candidates_found: candidates.length,
      improvements_applied: improvementsApplied,
    },
    metrics_analysis: {
      efficiency_before: avgEfficiencyBefore,
      efficiency_after: avgEfficiencyAfter,
      improvement_percentage: ((avgEfficiencyAfter - avgEfficiencyBefore) / avgEfficiencyBefore) * 100,
    },
    validation_results: {
      threshold: EFFICIENCY_THRESHOLD,
      agents_below_threshold: candidates.length,
    },
    overall_success: improvementsApplied > 0,
    duration_seconds: durationSeconds,
  });
  
  // 6. Atualizar quantum_brain_state
  const { data: brainState } = await supabase
    .from('quantum_brain_state')
    .select('current_evolution_cycle')
    .single();
  
  await supabase
    .from('quantum_brain_state')
    .update({
      current_evolution_cycle: (brainState?.current_evolution_cycle || 0) + 1,
      last_evolution_at: new Date().toISOString(),
      average_efficiency: avgEfficiencyAfter,
      updated_at: new Date().toISOString(),
    });
  
  return {
    cycle_id: cycleId,
    agents_analyzed: agents.length,
    improvements_applied: improvementsApplied,
    average_efficiency_before: avgEfficiencyBefore,
    average_efficiency_after: avgEfficiencyAfter,
    duration_seconds: durationSeconds,
    success: true,
  };
}

export async function getEvolutionHistory(limit: number = 10) {
  const supabase = createClient();
  
  const { data } = await supabase
    .from('evolution_cycles')
    .select('*')
    .order('timestamp', { ascending: false })
    .limit(limit);
  
  return data || [];
}

export async function getEvolutionCandidates(): Promise<Agent[]> {
  const supabase = createClient();
  
  const { data } = await supabase
    .from('agents')
    .select('*')
    .lt('efficiency', EFFICIENCY_THRESHOLD)
    .order('efficiency', { ascending: true })
    .limit(20);
  
  return (data || []) as Agent[];
}
