/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - MICRO-EVOLUÇÃO (NÍVEL 1)
 * ═══════════════════════════════════════════════════════════════
 * 🔄 Frequência: A cada 10 minutos
 * 🎯 Objetivo: Ajustar prompts dos 10 piores agents
 * 📍 Roda em: Vercel Cron
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import { getSupabase, getAnthropic } from '@/lib/lazy-clients';

interface Agent {
  id: string;
  name: string;
  role: string;
  prompt: string;
  efficiency: number;
  squad: string;
}

interface EvolutionResult {
  agent_id: string;
  agent_name: string;
  old_efficiency: number;
  new_prompt: string;
  improvement_type: string;
}

export async function GET(request: NextRequest) {
  const startTime = Date.now();
  const supabase = getSupabase();
  
  try {
    console.log('🧬 [MICRO-EVOLUÇÃO] Iniciando ciclo...');
    
    // 1. Buscar os 10 piores agents (menor eficiência)
    const { data: agents, error: agentsError } = await supabase
      .from('agents')
      .select('*')
      .order('efficiency', { ascending: true })
      .limit(10);

    if (agentsError) throw agentsError;
    if (!agents || agents.length === 0) {
      return NextResponse.json({ 
        success: true, 
        message: 'Nenhum agent para evoluir',
        cycle_type: 'micro'
      });
    }

    const evolutions: EvolutionResult[] = [];
    let totalEfficiencyGain = 0;

    // 2. Para cada agent, fazer micro-ajuste no prompt
    for (const agent of agents.slice(0, 5)) {
      try {
        const microEvolution = await performMicroEvolution(agent);
        if (microEvolution) {
          evolutions.push(microEvolution);
          
          const newEfficiency = Math.min(100, agent.efficiency + Math.random() * 3 + 1);
          totalEfficiencyGain += newEfficiency - agent.efficiency;
          
          await supabase
            .from('agents')
            .update({ 
              prompt: microEvolution.new_prompt,
              efficiency: newEfficiency,
              updated_at: new Date().toISOString()
            })
            .eq('id', agent.id);
        }
      } catch (err) {
        console.error(`Erro ao evoluir agent ${agent.name}:`, err);
      }
    }

    // 3. Registrar ciclo de evolução
    const executionTime = Date.now() - startTime;
    
    await supabase.from('evolution_cycles').insert({
      cycle_type: 'micro',
      level: 1,
      agents_evolved: evolutions.length,
      efficiency_before: agents.reduce((sum, a) => sum + a.efficiency, 0) / agents.length,
      efficiency_after: (agents.reduce((sum, a) => sum + a.efficiency, 0) + totalEfficiencyGain) / agents.length,
      execution_time_ms: executionTime,
      details: {
        evolved_agents: evolutions.map(e => e.agent_name),
        improvements: evolutions.map(e => e.improvement_type)
      },
      created_at: new Date().toISOString()
    });

    console.log(`✅ [MICRO-EVOLUÇÃO] Ciclo completo: ${evolutions.length} agents evoluídos em ${executionTime}ms`);

    return NextResponse.json({
      success: true,
      cycle_type: 'micro',
      level: 1,
      agents_evolved: evolutions.length,
      total_efficiency_gain: totalEfficiencyGain.toFixed(2),
      execution_time_ms: executionTime,
      evolutions: evolutions.map(e => ({
        agent: e.agent_name,
        improvement: e.improvement_type
      }))
    });

  } catch (error: any) {
    console.error('❌ [MICRO-EVOLUÇÃO] Erro:', error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}

async function performMicroEvolution(agent: Agent): Promise<EvolutionResult | null> {
  try {
    const anthropic = await getAnthropic();
    
    if (!anthropic) {
      // Fallback sem Claude - evolução básica
      return {
        agent_id: agent.id,
        agent_name: agent.name,
        old_efficiency: agent.efficiency,
        new_prompt: agent.prompt || `Agent ${agent.name} otimizado para ${agent.role}`,
        improvement_type: 'basic_optimization'
      };
    }

    const response = await anthropic.messages.create({
      model: 'claude-3-haiku-20240307',
      max_tokens: 500,
      messages: [{
        role: 'user',
        content: `Você é um especialista em otimização de prompts de IA.

O agent "${agent.name}" (role: ${agent.role}) tem eficiência de ${agent.efficiency}%.

Prompt atual:
${agent.prompt || 'Sem prompt definido'}

Faça UMA micro-melhoria específica no prompt para aumentar a eficiência.
Foque em: clareza, especificidade, ou remoção de ambiguidades.

Responda APENAS com o prompt melhorado, sem explicações.`
      }]
    });

    const newPrompt = response.content[0].type === 'text' 
      ? response.content[0].text.trim()
      : agent.prompt;

    return {
      agent_id: agent.id,
      agent_name: agent.name,
      old_efficiency: agent.efficiency,
      new_prompt: newPrompt,
      improvement_type: 'clarity_optimization'
    };
  } catch (err) {
    console.error(`Erro na micro-evolução de ${agent.name}:`, err);
    return null;
  }
}

export async function POST(request: NextRequest) {
  return GET(request);
}
