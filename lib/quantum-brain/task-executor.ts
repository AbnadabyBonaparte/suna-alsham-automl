// ═══════════════════════════════════════════════════════════════
// EXECUTOR DE TASKS - USA TABELAS EXISTENTES + quantum_tasks
// ═══════════════════════════════════════════════════════════════

import OpenAI from 'openai';
import { createClient } from '@/lib/supabase/client';
import { Agent, QuantumTask, Request } from './types';
import { routeToAgent, updateAgentStatus, incrementNeuralLoad, decrementNeuralLoad } from './agent-router';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Custos gpt-4o-mini
const COST_PER_1K_INPUT = 0.00015;
const COST_PER_1K_OUTPUT = 0.0006;

// System prompts por ROLE (fallback se não tiver no metadata)
const DEFAULT_PROMPTS: Record<string, string> = {
  CORE: `Você é um agente CORE do ALSHAM QUANTUM, responsável por coordenação e operações críticas do sistema.
Você executa tarefas de infraestrutura, deploy, APIs e sincronização.
Responda sempre em JSON estruturado com: { "action": "...", "result": {...}, "status": "success|error" }`,

  GUARD: `Você é um agente GUARD do ALSHAM QUANTUM, responsável por segurança e proteção do sistema.
Você monitora ameaças, valida acessos, audita operações e protege dados.
Responda sempre em JSON estruturado com: { "security_assessment": {...}, "risk_level": "low|medium|high", "recommendations": [...] }`,

  ANALYST: `Você é um agente ANALYST do ALSHAM QUANTUM, responsável por análise de dados e geração de insights.
Você processa métricas, identifica padrões, gera relatórios e faz previsões.
Responda sempre em JSON estruturado com: { "analysis": {...}, "insights": [...], "recommendations": [...] }`,

  SPECIALIST: `Você é um agente SPECIALIST do ALSHAM QUANTUM, especialista em operações de negócio.
Você executa tarefas de vendas, marketing, suporte, conteúdo e automação.
Responda sempre em JSON estruturado com: { "task_type": "...", "result": {...}, "next_actions": [...] }`,
};

export interface TaskInput {
  title: string;
  description: string;
  data?: Record<string, any>;
  priority?: 'low' | 'normal' | 'high' | 'critical';
  user_id?: string;
}

export interface TaskResult {
  task_id: string;
  request_id?: string;
  agent: {
    id: string;
    name: string;
    role: string;
    efficiency: number;
  };
  result: any;
  execution_time_ms: number;
  tokens_used: number;
  cost_usd: number;
  status: 'completed' | 'failed';
  error_message?: string;
}

export async function executeTask(input: TaskInput): Promise<TaskResult> {
  const supabase = createClient();
  const startTime = Date.now();
  
  // 1. Criar request na fila (tabela existente)
  const { data: request, error: reqError } = await supabase
    .from('requests')
    .insert({
      user_id: input.user_id || '00000000-0000-0000-0000-000000000000', // System user
      title: input.title,
      description: input.description,
      status: 'processing',
      priority: input.priority || 'normal',
    })
    .select()
    .single();
  
  if (reqError) {
    throw new Error(`Failed to create request: ${reqError.message}`);
  }
  
  // 2. Rotear para agent apropriado
  const agent = await routeToAgent(`${input.title} ${input.description}`);
  
  // 3. Criar registro em quantum_tasks
  const { data: task, error: taskError } = await supabase
    .from('quantum_tasks')
    .insert({
      request_id: request.id,
      agent_id: agent.id,
      input: {
        title: input.title,
        description: input.description,
        data: input.data,
      },
      status: 'processing',
    })
    .select()
    .single();
  
  if (taskError) {
    throw new Error(`Failed to create task: ${taskError.message}`);
  }
  
  // 4. Atualizar status do agent
  await updateAgentStatus(agent.id, 'ACTIVE', `Executando: ${input.title}`);
  await incrementNeuralLoad(agent.id, 15);
  
  try {
    // 5. Obter system prompt (do metadata ou default)
    const systemPrompt = agent.metadata?.system_prompt || DEFAULT_PROMPTS[agent.role] || DEFAULT_PROMPTS.SPECIALIST;
    
    // 6. Executar via OpenAI
    const completion = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: systemPrompt },
        {
          role: 'user',
          content: `TAREFA: ${input.title}

DESCRIÇÃO: ${input.description}

DADOS ADICIONAIS: ${JSON.stringify(input.data || {})}

Execute a tarefa e responda em JSON estruturado.`,
        },
      ],
      temperature: 0.7,
      max_tokens: 2000,
    });
    
    const executionTime = Date.now() - startTime;
    const tokensUsed = completion.usage?.total_tokens || 0;
    const inputTokens = completion.usage?.prompt_tokens || 0;
    const outputTokens = completion.usage?.completion_tokens || 0;
    const cost = (inputTokens / 1000) * COST_PER_1K_INPUT + (outputTokens / 1000) * COST_PER_1K_OUTPUT;
    
    // 7. Parse resultado
    let result: any;
    try {
      const content = completion.choices[0]?.message?.content || '{}';
      result = JSON.parse(content.replace(/```json\n?|\n?```/g, '').trim());
    } catch {
      result = { raw_response: completion.choices[0]?.message?.content };
    }
    
    // 8. Atualizar quantum_tasks
    await supabase
      .from('quantum_tasks')
      .update({
        output: result,
        status: 'completed',
        execution_time_ms: executionTime,
        tokens_used: tokensUsed,
        cost_usd: cost,
        completed_at: new Date().toISOString(),
      })
      .eq('id', task.id);
    
    // 9. Atualizar request original
    await supabase
      .from('requests')
      .update({ status: 'completed', updated_at: new Date().toISOString() })
      .eq('id', request.id);
    
    // 10. Atualizar agent
    await updateAgentStatus(agent.id, 'ACTIVE', 'Aguardando comando');
    await decrementNeuralLoad(agent.id, 15);
    
    // 11. Criar log (tabela existente)
    await supabase.from('agent_logs').insert({
      agent_id: agent.id,
      log_level: 'INFO',
      message: `Task completed: ${input.title}`,
      metadata: {
        task_id: task.id,
        execution_time_ms: executionTime,
        tokens_used: tokensUsed,
      },
    });
    
    return {
      task_id: task.id,
      request_id: request.id,
      agent: {
        id: agent.id,
        name: agent.name,
        role: agent.role,
        efficiency: agent.efficiency,
      },
      result,
      execution_time_ms: executionTime,
      tokens_used: tokensUsed,
      cost_usd: cost,
      status: 'completed',
    };
    
  } catch (error) {
    const executionTime = Date.now() - startTime;
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    
    // Atualizar como falha
    await supabase
      .from('quantum_tasks')
      .update({
        status: 'failed',
        error_message: errorMessage,
        execution_time_ms: executionTime,
        completed_at: new Date().toISOString(),
      })
      .eq('id', task.id);
    
    await supabase
      .from('requests')
      .update({ status: 'failed', updated_at: new Date().toISOString() })
      .eq('id', request.id);
    
    await updateAgentStatus(agent.id, 'WARNING', `Erro: ${errorMessage.slice(0, 50)}`);
    await decrementNeuralLoad(agent.id, 15);
    
    // Log de erro
    await supabase.from('agent_logs').insert({
      agent_id: agent.id,
      log_level: 'ERROR',
      message: `Task failed: ${input.title}`,
      metadata: { error: errorMessage, task_id: task.id },
    });
    
    return {
      task_id: task.id,
      request_id: request.id,
      agent: {
        id: agent.id,
        name: agent.name,
        role: agent.role,
        efficiency: agent.efficiency,
      },
      result: null,
      execution_time_ms: executionTime,
      tokens_used: 0,
      cost_usd: 0,
      status: 'failed',
      error_message: errorMessage,
    };
  }
}
