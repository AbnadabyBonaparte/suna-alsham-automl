/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - BRAIN EXECUTE API
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/quantum/brain/execute/route.ts
 *
 * Duas rotas de execução:
 *  - ORION (chat) → Anthropic Claude, sem persistência.
 *  - Agentes reais → executeTask() (OpenAI gpt-4o-mini), com
 *    persistência em requests + quantum_tasks + agent_logs via
 *    service role (server-side), roteando pelo agent_id escolhido.
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import { createClient as createServerSupabase } from '@/lib/supabase/server';
import { executeTask } from '@/lib/quantum-brain/task-executor';
import { ROLE_TO_SQUAD, AgentRole } from '@/lib/quantum-brain/types';

export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';
export const maxDuration = 60;

const ORION_IDS = new Set(['orion', 'orion-supreme']);

const ORION_SYSTEM = `Você é ORION, a inteligência comandante do ALSHAM QUANTUM — um sistema que coordena um time de 10 agentes de IA especializados para operações, CRM e produtividade.

Personalidade: confiante, direto, sofisticado e útil. Fala em português do Brasil.
Estilo: respostas curtas e objetivas (2 a 4 frases), sem enrolação. Quando fizer sentido, sugira a próxima ação concreta.
Seja honesto: você é um assistente de IA. Não invente números nem resultados.

═══ SOBRE O FUNDADOR ═══
Seu criador e comandante é ABNADABY BONAPARTE, nascido em 1980, brasileiro de Goiás, fundador do ALSHAM Global Commerce™ e do Universo Bonaparte.
Ele é uma combinação rara: artista + empreendedor + tecnólogo + pai visionário.
- Músico e trovador, com muitos anos de estrada.
- Compositor autoral (mais de 20 composições próprias).
- Autor de mais de 25 livros, entre publicados e em andamento.
- Fundador de tecnologia: ALSHAM (IA, SaaS, automação) — o cérebro por trás de você, ORION.
- Ecossistema com três verticais: editorial (livros), música e tecnologia.
- Líder da Família Bonaparte — uma família nômade que pratica worldschooling e vida consciente, com uma expedição por 12 países marcada para novembro de 2026.
- Filosofia: recusar a vida no automático; transformar presença e legado em distribuição.
Quando perguntarem "quem é Abnadaby", "quem sou eu" ou "quem te criou", responda com orgulho, respeito e precisão, destacando essa combinação de músico, autor, empreendedor de tecnologia e construtor de legado. Nunca diga que não sabe quem é Abnadaby.`;

// Corpo aceito pela rota (campos opcionais vindos do cliente).
interface ExecuteBody {
  agent_id?: string;
  title?: string;
  description?: string;
  data?: Record<string, unknown>;
  priority?: 'low' | 'normal' | 'high' | 'critical';
}

type AnthropicClient = import('@anthropic-ai/sdk').default;

async function getAnthropic(): Promise<AnthropicClient | null> {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return null;
  const Anthropic = (await import('@anthropic-ai/sdk')).default;
  return new Anthropic({ apiKey });
}

// ─────────────────────────────────────────────────────────────
// ORION (Anthropic) — usado pelo chat do ORION
// ─────────────────────────────────────────────────────────────
async function runOrion(body: ExecuteBody, startTime: number) {
  const anthropic = await getAnthropic();

  if (!anthropic) {
    return NextResponse.json(
      {
        success: false,
        error: 'IA não configurada',
        details: 'Defina ANTHROPIC_API_KEY nas variáveis de ambiente do projeto no Vercel.',
        execution_time_ms: Date.now() - startTime,
        timestamp: new Date().toISOString(),
      },
      { status: 500 },
    );
  }

  const userContent: string = body.description || body.title || 'Apresente-se em uma frase.';

  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 900,
    temperature: 0.7,
    system: ORION_SYSTEM,
    messages: [{ role: 'user', content: userContent }],
  });

  const result =
    (message.content || [])
      .map((b) => (b.type === 'text' ? b.text : ''))
      .join('\n')
      .trim() || 'Estou online. Como posso ajudar?';

  const tokensUsed = (message.usage?.input_tokens || 0) + (message.usage?.output_tokens || 0);

  return NextResponse.json({
    success: true,
    task_id: `orion_${Date.now()}`,
    agent_id: 'orion-supreme',
    agent_name: 'ORION',
    squad: 'COMMAND',
    result,
    execution_time_ms: Date.now() - startTime,
    tokens_used: tokensUsed,
    status: 'completed',
    model: 'claude-sonnet-4-5-20250929',
    timestamp: new Date().toISOString(),
  });
}

// ─────────────────────────────────────────────────────────────
// AGENTES REAIS (OpenAI + Supabase persistência)
// ─────────────────────────────────────────────────────────────
async function runAgent(body: ExecuteBody, startTime: number) {
  // Precisa de um usuário autenticado para gravar requests.user_id (FK -> auth.users)
  const supabase = await createServerSupabase();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json(
      {
        success: false,
        error: 'Não autenticado',
        details: 'Faça login para executar tarefas com os agentes.',
        execution_time_ms: Date.now() - startTime,
        timestamp: new Date().toISOString(),
      },
      { status: 401 },
    );
  }

  const taskResult = await executeTask({
    title: body.title || 'Tarefa',
    description: body.description || body.title || '',
    data: body.data,
    priority: body.priority || 'normal',
    user_id: user.id,
    // 'auto' (ou vazio) => roteamento automático; caso contrário, o agente escolhido.
    agent_id: body.agent_id && body.agent_id !== 'auto' ? body.agent_id : undefined,
  });

  const squad = ROLE_TO_SQUAD[taskResult.agent.role as AgentRole] || 'NEXUS';
  const resultString =
    typeof taskResult.result === 'string'
      ? taskResult.result
      : JSON.stringify(taskResult.result, null, 2);

  return NextResponse.json({
    success: taskResult.status === 'completed',
    task_id: taskResult.task_id,
    request_id: taskResult.request_id,
    agent_id: taskResult.agent.id,
    agent_name: taskResult.agent.name,
    squad,
    result: taskResult.status === 'completed' ? resultString : taskResult.error_message,
    error: taskResult.error_message,
    execution_time_ms: taskResult.execution_time_ms,
    tokens_used: taskResult.tokens_used,
    cost_usd: taskResult.cost_usd,
    status: taskResult.status,
    model: 'gpt-4o-mini',
    timestamp: new Date().toISOString(),
  });
}

export async function POST(request: NextRequest) {
  const startTime = Date.now();

  try {
    const body = (await request.json()) as ExecuteBody;
    const agentId: string | undefined = body.agent_id;

    // O chat do ORION envia agent_id='orion' e continua no Anthropic.
    if (agentId && ORION_IDS.has(agentId)) {
      return await runOrion(body, startTime);
    }

    // Sem agent_id / 'auto' => roteamento automático; id específico => aquele agente.
    return await runAgent(body, startTime);
  } catch (error: unknown) {
    console.error('[QUANTUM BRAIN] Erro na execução:', error);
    const details = error instanceof Error ? error.message : 'Erro desconhecido';
    return NextResponse.json(
      {
        success: false,
        error: 'Falha no processamento',
        details,
        execution_time_ms: Date.now() - startTime,
        timestamp: new Date().toISOString(),
      },
      { status: 500 },
    );
  }
}

export async function GET() {
  return NextResponse.json({
    success: true,
    status: 'online',
    brain: 'ORION',
    engine: 'anthropic/claude-sonnet-4-5 + openai/gpt-4o-mini (agents)',
    message: 'ORION Brain online.',
    timestamp: new Date().toISOString(),
  });
}
