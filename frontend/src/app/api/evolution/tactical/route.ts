/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - EVOLUÇÃO TÁTICA (NÍVEL 2)
 * ═══════════════════════════════════════════════════════════════
 * 🔄 Frequência: A cada 2 horas
 * 🎯 Objetivo: Analisar 30 agents + histórico de performance
 * 📍 Roda em: Vercel Cron / Railway
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import Anthropic from '@anthropic-ai/sdk';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY!,
});

interface Agent {
  id: string;
  name: string;
  role: string;
  prompt: string;
  efficiency: number;
  squad: string;
  total_requests?: number;
  successful_requests?: number;
}

interface TacticalEvolution {
  agent_id: string;
  agent_name: string;
  squad: string;
  old_efficiency: number;
  new_efficiency: number;
  changes: string[];
  reasoning: string;
}

export async function GET(request: NextRequest) {
  const startTime = Date.now();
  
  try {
    console.log('⚔️ [EVOLUÇÃO TÁTICA] Iniciando ciclo...');
    
    // 1. Buscar 30 agents com métricas de performance
    const { data: agents, error: agentsError } = await supabase
      .from('agents')
      .select('*')
      .order('efficiency', { ascending: true })
      .limit(30);

    if (agentsError) throw agentsError;
    if (!agents || agents.length === 0) {
      return NextResponse.json({ 
        success: true, 
        message: 'Nenhum agent para evoluir taticamente',
        cycle_type: 'tactical'
      });
    }

    // 2. Buscar histórico de requests dos últimos 7 dias
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    
    const { data: requests } = await supabase
      .from('requests')
      .select('assigned_agent_id, status, processing_time_ms')
      .gte('created_at', weekAgo.toISOString());

    // 3. Calcular métricas por agent
    const agentMetrics: Map<string, { total: number, success: number, avgTime: number }> = new Map();
    
    (requests || []).forEach(req => {
      if (!req.assigned_agent_id) return;
      const current = agentMetrics.get(req.assigned_agent_id) || { total: 0, success: 0, avgTime: 0 };
      current.total++;
      if (req.status === 'completed') current.success++;
      current.avgTime = (current.avgTime * (current.total - 1) + (req.processing_time_ms || 0)) / current.total;
      agentMetrics.set(req.assigned_agent_id, current);
    });

    // 4. Agrupar agents por squad para evolução coordenada
    const squadGroups: Map<string, Agent[]> = new Map();
    agents.forEach(agent => {
      const squad = agent.squad || 'GENERAL';
      const group = squadGroups.get(squad) || [];
      group.push(agent);
      squadGroups.set(squad, group);
    });

    const evolutions: TacticalEvolution[] = [];
    let totalEfficiencyGain = 0;

    // 5. Evoluir agents de cada squad
    for (const [squad, squadAgents] of squadGroups) {
      // Pegar os 3 piores de cada squad
      const worstAgents = squadAgents.slice(0, 3);
      
      for (const agent of worstAgents) {
        try {
          const metrics = agentMetrics.get(agent.id);
          const evolution = await performTacticalEvolution(agent, metrics, squad);
          
          if (evolution) {
            evolutions.push(evolution);
            totalEfficiencyGain += evolution.new_efficiency - evolution.old_efficiency;
            
            // Atualizar agent
            await supabase
              .from('agents')
              .update({
                prompt: evolution.changes.join('\n\n'),
                efficiency: evolution.new_efficiency,
                updated_at: new Date().toISOString()
              })
              .eq('id', agent.id);
          }
        } catch (err) {
          console.error(`Erro ao evoluir taticamente ${agent.name}:`, err);
        }
      }
    }

    // 6. Registrar ciclo
    const executionTime = Date.now() - startTime;
    
    await supabase.from('evolution_cycles').insert({
      cycle_type: 'tactical',
      level: 2,
      agents_evolved: evolutions.length,
      efficiency_before: agents.reduce((sum, a) => sum + a.efficiency, 0) / agents.length,
      efficiency_after: (agents.reduce((sum, a) => sum + a.efficiency, 0) + totalEfficiencyGain) / agents.length,
      execution_time_ms: executionTime,
      details: {
        squads_analyzed: Array.from(squadGroups.keys()),
        evolved_agents: evolutions.map(e => ({ name: e.agent_name, squad: e.squad, gain: (e.new_efficiency - e.old_efficiency).toFixed(2) })),
        total_requests_analyzed: requests?.length || 0
      },
      created_at: new Date().toISOString()
    });

    console.log(`✅ [EVOLUÇÃO TÁTICA] Ciclo completo: ${evolutions.length} agents em ${executionTime}ms`);

    return NextResponse.json({
      success: true,
      cycle_type: 'tactical',
      level: 2,
      agents_evolved: evolutions.length,
      squads_analyzed: Array.from(squadGroups.keys()),
      total_efficiency_gain: totalEfficiencyGain.toFixed(2),
      execution_time_ms: executionTime,
      evolutions: evolutions.map(e => ({
        agent: e.agent_name,
        squad: e.squad,
        efficiency_gain: (e.new_efficiency - e.old_efficiency).toFixed(2),
        reasoning: e.reasoning
      }))
    });

  } catch (error: any) {
    console.error('❌ [EVOLUÇÃO TÁTICA] Erro:', error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}

async function performTacticalEvolution(
  agent: Agent, 
  metrics: { total: number, success: number, avgTime: number } | undefined,
  squad: string
): Promise<TacticalEvolution | null> {
  try {
    const successRate = metrics ? (metrics.success / metrics.total * 100).toFixed(1) : 'N/A';
    const avgTime = metrics ? metrics.avgTime.toFixed(0) : 'N/A';
    
    const response = await anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022', // Modelo mais capaz para análise tática
      max_tokens: 1000,
      messages: [{
        role: 'user',
        content: `Você é um estrategista de otimização de agents de IA.

**Agent:** ${agent.name}
**Role:** ${agent.role}
**Squad:** ${squad}
**Eficiência atual:** ${agent.efficiency}%
**Taxa de sucesso (7 dias):** ${successRate}%
**Tempo médio de resposta:** ${avgTime}ms

**Prompt atual:**
${agent.prompt || 'Não definido'}

**TAREFA:** Faça uma evolução TÁTICA do prompt considerando:
1. O papel específico do agent no squad ${squad}
2. A taxa de sucesso histórica
3. O tempo de resposta

Responda em JSON:
{
  "new_prompt": "prompt melhorado completo",
  "changes": ["mudança 1", "mudança 2"],
  "reasoning": "explicação da estratégia",
  "expected_efficiency_gain": 5.0
}`
      }]
    });

    const content = response.content[0].type === 'text' ? response.content[0].text : '';
    
    // Tentar parsear JSON
    let result;
    try {
      const jsonMatch = content.match(/\{[\s\S]*\}/);
      result = jsonMatch ? JSON.parse(jsonMatch[0]) : null;
    } catch {
      result = null;
    }

    if (!result) return null;

    const newEfficiency = Math.min(100, agent.efficiency + (result.expected_efficiency_gain || 3));

    return {
      agent_id: agent.id,
      agent_name: agent.name,
      squad: squad,
      old_efficiency: agent.efficiency,
      new_efficiency: newEfficiency,
      changes: result.changes || [result.new_prompt],
      reasoning: result.reasoning || 'Evolução tática aplicada'
    };
  } catch (err) {
    console.error(`Erro na evolução tática de ${agent.name}:`, err);
    return null;
  }
}

export async function POST(request: NextRequest) {
  return GET(request);
}

