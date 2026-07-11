// ═══════════════════════════════════════════════════════════════
// EXECUTOR DE TASKS - USA TABELAS EXISTENTES + quantum_tasks
// SERVER-ONLY (usa service role para ignorar RLS nos inserts)
// ═══════════════════════════════════════════════════════════════

import OpenAI from 'openai';
import { createAdminClient } from '@/lib/supabase/admin';
import { Agent } from './types';
import {
  routeToAgent,
  getAgentById,
  updateAgentStatus,
  incrementNeuralLoad,
  decrementNeuralLoad,
} from './agent-router';
import {
  getBehavior,
  aggregateAgentStats,
  parseJsonLoose,
  type AgentBehavior,
  type BehaviorContext,
  type AgentStatRow,
} from './agent-behaviors';

// Custos gpt-4o-mini (USD por 1K tokens)
const COST_PER_1K_INPUT = 0.00015;
const COST_PER_1K_OUTPUT = 0.0006;

/** Cálculo de custo determinístico (exportado para testes). */
export function computeCost(inputTokens: number, outputTokens: number): number {
  const input = Number.isFinite(inputTokens) ? Math.max(0, inputTokens) : 0;
  const output = Number.isFinite(outputTokens) ? Math.max(0, outputTokens) : 0;
  return (input / 1000) * COST_PER_1K_INPUT + (output / 1000) * COST_PER_1K_OUTPUT;
}

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

const SYSTEM_USER_ID = '00000000-0000-0000-0000-000000000000';

export interface TaskInput {
  title: string;
  description: string;
  data?: Record<string, unknown>;
  priority?: 'low' | 'normal' | 'high' | 'critical';
  user_id?: string;
  agent_id?: string; // quando o usuário escolhe um agente específico no picker
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
  result: unknown;
  execution_time_ms: number;
  tokens_used: number;
  cost_usd: number;
  status: 'completed' | 'failed';
  error_message?: string;
}

function getApiKey(): string | undefined {
  return process.env.OPENAI_API_KEY;
}

export async function executeTask(input: TaskInput): Promise<TaskResult> {
  const supabase = createAdminClient();
  const startTime = Date.now();

  const apiKey = getApiKey();

  // 1. Criar request na fila (tabela existente)
  const { data: request, error: reqError } = await supabase
    .from('requests')
    .insert({
      user_id: input.user_id || SYSTEM_USER_ID,
      title: input.title,
      description: input.description,
      status: 'processing',
      priority: input.priority === 'critical' ? 'high' : input.priority || 'normal',
    })
    .select()
    .single();

  if (reqError) {
    throw new Error(`Failed to create request: ${reqError.message}`);
  }

  // 2. Selecionar agent: id explícito do picker OU roteamento automático
  let agent: Agent | null = null;
  if (input.agent_id) {
    agent = await getAgentById(input.agent_id);
  }
  if (!agent) {
    agent = await routeToAgent(`${input.title} ${input.description}`);
  }

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
      model_used: 'gpt-4o-mini',
    })
    .select()
    .single();

  if (taskError) {
    throw new Error(`Failed to create task: ${taskError.message}`);
  }

  // 4. Atualizar status do agent (ocupado)
  await updateAgentStatus(agent.id, 'PROCESSING', `Executando: ${input.title}`);
  await incrementNeuralLoad(agent.id, 15);

  // 4b. Resolver comportamento tipado do agente (se houver) e montar contexto.
  const behavior: AgentBehavior | undefined = getBehavior(agent.id);
  const behaviorCtx: BehaviorContext = {
    title: input.title,
    description: input.description,
    data: input.data,
  };

  // Comportamentos que dependem de métricas reais (ex.: DATA MINER) recebem
  // agregado REAL do banco — nunca dados inventados (Lei da Honestidade).
  if (behavior?.needsAgentStats) {
    const { data: statsRows } = await supabase.from('agents').select('role, status, efficiency');
    behaviorCtx.agentStats = aggregateAgentStats((statsRows as AgentStatRow[] | null) || []);
  }

  // 4c. Degradação graciosa: sem chave de LLM, devolvemos um resultado claro
  // pedindo configuração — nunca dados fake. O agente volta a IDLE.
  if (!apiKey) {
    const degradedOutput: unknown = behavior
      ? behavior.notConfigured(behaviorCtx)
      : {
          configured: false,
          message:
            'LLM não configurado. Defina OPENAI_API_KEY nas variáveis de ambiente para executar tarefas.',
        };
    const executionTime = Date.now() - startTime;

    await supabase
      .from('quantum_tasks')
      .update({
        output: degradedOutput,
        status: 'failed',
        error_message: 'LLM_NOT_CONFIGURED',
        execution_time_ms: executionTime,
        completed_at: new Date().toISOString(),
      })
      .eq('id', task.id);

    await supabase
      .from('requests')
      .update({ status: 'failed', updated_at: new Date().toISOString() })
      .eq('id', request.id);

    await updateAgentStatus(agent.id, 'IDLE', 'Aguardando comando');
    await decrementNeuralLoad(agent.id, 15);

    await supabase.from('agent_logs').insert({
      agent_id: agent.id,
      event_type: 'not_configured',
      message: `Task not configured (no LLM key): ${input.title}`,
      metadata: { task_id: task.id, contract: behavior?.id || null },
    });

    return {
      task_id: task.id,
      request_id: request.id,
      agent: { id: agent.id, name: agent.name, role: agent.role, efficiency: agent.efficiency },
      result: degradedOutput,
      execution_time_ms: executionTime,
      tokens_used: 0,
      cost_usd: 0,
      status: 'failed',
      error_message:
        'LLM não configurado. Defina OPENAI_API_KEY nas variáveis de ambiente para executar tarefas.',
    };
  }

  const openai = new OpenAI({ apiKey });

  try {
    // 5. Montar prompts: comportamento tipado tem prioridade sobre o default por role.
    const systemPrompt = behavior
      ? behavior.systemPrompt
      : (agent.metadata?.system_prompt as string | undefined) ||
        DEFAULT_PROMPTS[agent.role] ||
        DEFAULT_PROMPTS.SPECIALIST;

    const userPrompt = behavior
      ? behavior.buildUserPrompt(behaviorCtx)
      : `TAREFA: ${input.title}

DESCRIÇÃO: ${input.description}

DADOS ADICIONAIS: ${JSON.stringify(input.data || {})}

Execute a tarefa e responda em JSON estruturado.`;

    // 6. Executar via OpenAI
    const completion = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt },
      ],
      temperature: 0.7,
      max_tokens: 2000,
    });

    const executionTime = Date.now() - startTime;
    const tokensUsed = completion.usage?.total_tokens || 0;
    const inputTokens = completion.usage?.prompt_tokens || 0;
    const outputTokens = completion.usage?.completion_tokens || 0;
    const cost = computeCost(inputTokens, outputTokens);

    // 7. Parse/map resultado: comportamento tipado devolve o contrato estruturado;
    // caso contrário, parse tolerante do JSON do LLM.
    const content = completion.choices[0]?.message?.content || '{}';
    let result: unknown;
    if (behavior) {
      result = behavior.parse(content, behaviorCtx);
    } else {
      const parsed = parseJsonLoose(content);
      result = Object.keys(parsed).length > 0 ? parsed : { raw_response: content };
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

    // 10. Atualizar agent (liberado)
    await updateAgentStatus(agent.id, 'IDLE', 'Aguardando comando');
    await decrementNeuralLoad(agent.id, 15);

    // 11. Criar log (tabela existente usa event_type, não log_level)
    await supabase.from('agent_logs').insert({
      agent_id: agent.id,
      event_type: 'task_complete',
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
      event_type: 'error',
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
