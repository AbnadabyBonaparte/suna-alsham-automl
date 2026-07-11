import OpenAI from 'openai';
import { createAdminClient } from '@/lib/supabase/admin';
import { getAgentById } from '@/lib/quantum-brain/agent-router';
import { decomposeObjective, orchestrate } from '@/lib/quantum-brain/orchestrator';
import {
  SKILLS,
  resolveAgentForSkill,
  skillsForAgent,
  type SkillId,
} from '@/lib/quantum-brain/skills';
import { AGENT_BEHAVIORS } from '@/lib/quantum-brain/agent-behaviors';
import type {
  DataMiningResult,
  LeadScoringResult,
  ContentResult,
  EmailSequenceResult,
} from '@/lib/quantum-brain/agent-behaviors';

jest.mock('openai');
jest.mock('@/lib/supabase/admin', () => ({ createAdminClient: jest.fn() }));
jest.mock('@/lib/quantum-brain/agent-router', () => ({
  routeToAgent: jest.fn(),
  getAgentById: jest.fn(),
  updateAgentStatus: jest.fn().mockResolvedValue(undefined),
  incrementNeuralLoad: jest.fn().mockResolvedValue(undefined),
  decrementNeuralLoad: jest.fn().mockResolvedValue(undefined),
}));

// ─────────────────────────────────────────────────────────────
// Parte pura: decomposição (Objetivo → Plan)
// ─────────────────────────────────────────────────────────────
describe('decomposeObjective (puro, determinístico)', () => {
  it('objetivo amplo → pipeline completo de 4 passos encadeados', () => {
    const plan = decomposeObjective('Lançar campanha de crescimento ponta a ponta');
    expect(plan.steps.map((s) => s.skill)).toEqual([
      'aggregate-stats',
      'score-leads',
      'generate-copy',
      'build-sequence',
    ]);
    expect(plan.steps.map((s) => s.id)).toEqual(['step-1', 'step-2', 'step-3', 'step-4']);
    // Cadeia de dependências linear.
    expect(plan.steps[0].dependsOn).toEqual([]);
    expect(plan.steps[1].dependsOn).toEqual(['step-1']);
    expect(plan.steps[3].dependsOn).toEqual(['step-3']);
    expect(plan.steps.map((s) => s.agentName)).toEqual([
      'DATA MINER',
      'LEAD MAGNET',
      'CONTENT CREATOR',
      'EMAIL SEQUENCE BOT',
    ]);
  });

  it('objetivo estreito → subconjunto na ordem canônica', () => {
    const plan = decomposeObjective('pontuar leads e montar sequência de email');
    expect(plan.steps.map((s) => s.skill)).toEqual(['score-leads', 'build-sequence']);
    expect(plan.steps[0].dependsOn).toEqual([]);
    expect(plan.steps[1].dependsOn).toEqual(['step-1']); // reindexado
  });

  it('objetivo de um único formato → um passo sem dependências', () => {
    const plan = decomposeObjective('apenas gerar conteúdo para o blog');
    expect(plan.steps).toHaveLength(1);
    expect(plan.steps[0].skill).toBe('generate-copy');
    expect(plan.steps[0].requiresLLM).toBe(true);
  });
});

// ─────────────────────────────────────────────────────────────
// Skills: resolução skill → agente + consistência com behaviors
// ─────────────────────────────────────────────────────────────
describe('skills (resolução e consistência)', () => {
  it('resolve skill → agente correto', () => {
    expect(resolveAgentForSkill('aggregate-stats')).toBe('data-miner');
    expect(resolveAgentForSkill('score-leads')).toBe('lead-magnet');
    expect(resolveAgentForSkill('generate-copy')).toBe('content-creator');
    expect(resolveAgentForSkill('build-sequence')).toBe('email-sequence-bot');
  });

  it('skillsForAgent lista as skills de um agente', () => {
    expect(skillsForAgent('data-miner')).toEqual(['aggregate-stats']);
  });

  it('aggregate-stats é determinística (não requer LLM); as demais requerem', () => {
    expect(SKILLS['aggregate-stats'].requiresLLM).toBe(false);
    expect(SKILLS['score-leads'].requiresLLM).toBe(true);
    expect(SKILLS['generate-copy'].requiresLLM).toBe(true);
    expect(SKILLS['build-sequence'].requiresLLM).toBe(true);
  });

  it('behavior.provides é consistente com o registro de skills (sem drift)', () => {
    for (const behavior of Object.values(AGENT_BEHAVIORS)) {
      for (const skill of behavior.provides) {
        expect(SKILLS[skill].agentId).toBe(behavior.id);
      }
    }
  });
});

// ─────────────────────────────────────────────────────────────
// Harness: executeTask real com OpenAI/Supabase/router mockados
// ─────────────────────────────────────────────────────────────
function createSupabaseMock() {
  let currentTable = '';
  const singleResults: Record<string, unknown> = {
    requests: { data: { id: 'req-1' }, error: null },
    quantum_tasks: { data: { id: 'task-1' }, error: null },
  };
  const manyResults: Record<string, unknown> = {};
  const builder: Record<string, jest.Mock> & {
    single: jest.Mock;
    then: (r: (v: unknown) => unknown) => unknown;
  } = {} as never;
  const chain = ['select', 'insert', 'update', 'delete', 'eq', 'in', 'order', 'limit', 'gte', 'lt'];
  chain.forEach((m) => {
    builder[m] = jest.fn(() => builder);
  });
  builder.single = jest.fn(() =>
    Promise.resolve(singleResults[currentTable] ?? { data: null, error: null }),
  );
  builder.then = (resolve) => resolve(manyResults[currentTable] ?? { data: [], error: null });
  const from = jest.fn((table: string) => {
    currentTable = table;
    return builder;
  });
  return {
    client: { from },
    setMany: (table: string, value: unknown) => {
      manyResults[table] = value;
    },
  };
}

const AGENTS: Record<string, Record<string, unknown>> = {
  'data-miner': {
    id: 'data-miner',
    name: 'DATA MINER',
    role: 'ANALYST',
    efficiency: 88,
    neural_load: 0,
    metadata: {},
  },
  'lead-magnet': {
    id: 'lead-magnet',
    name: 'LEAD MAGNET',
    role: 'SPECIALIST',
    efficiency: 86,
    neural_load: 0,
    metadata: {},
  },
  'content-creator': {
    id: 'content-creator',
    name: 'CONTENT CREATOR',
    role: 'SPECIALIST',
    efficiency: 85,
    neural_load: 0,
    metadata: {},
  },
  'email-sequence-bot': {
    id: 'email-sequence-bot',
    name: 'EMAIL SEQUENCE BOT',
    role: 'SPECIALIST',
    efficiency: 87,
    neural_load: 0,
    metadata: {},
  },
};

interface CreateCall {
  system: string;
  user: string;
}
const createCalls: CreateCall[] = [];
const mockCreate = jest.fn();

function llmResponseFor(system: string): string {
  if (system.includes('DATA MINER')) {
    return JSON.stringify({ insights: ['9/10 ativos'], recommendations: ['revisar 1'] });
  }
  if (system.includes('LEAD MAGNET')) {
    return JSON.stringify({
      leads: [{ name: 'ACME_HOT', score: 92, rationale: 'fit alto', suggested_action: 'ligar' }],
      summary: 'ok',
      next_actions: ['follow-up'],
    });
  }
  if (system.includes('CONTENT CREATOR')) {
    return JSON.stringify({
      topic: 'GrowthTopic',
      pieces: [{ format: 'email', title: 'T', body: 'B', hashtags: [], cta: 'Buy' }],
      next_actions: [],
    });
  }
  if (system.includes('EMAIL SEQUENCE BOT')) {
    return JSON.stringify({
      audience: 'quentes',
      steps: [{ delay_days: 0, subject: 'S1', body: 'B1', goal: 'ativar' }],
      next_actions: [],
    });
  }
  return '{}';
}

describe('orchestrate (composição multi-agente ponta a ponta)', () => {
  let sb: ReturnType<typeof createSupabaseMock>;

  beforeEach(() => {
    jest.clearAllMocks();
    createCalls.length = 0;
    process.env.OPENAI_API_KEY = 'test-key';
    sb = createSupabaseMock();
    // DATA MINER agrega estas 2 linhas reais (1 ativo, 1 em ERROR).
    sb.setMany('agents', {
      data: [
        { role: 'CORE', status: 'IDLE', efficiency: 90 },
        { role: 'GUARD', status: 'ERROR', efficiency: 80 },
      ],
      error: null,
    });
    (createAdminClient as jest.Mock).mockReturnValue(sb.client);
    (getAgentById as jest.Mock).mockImplementation((id: string) => Promise.resolve(AGENTS[id]));
    (OpenAI as unknown as jest.Mock).mockImplementation(() => ({
      chat: {
        completions: {
          create: mockCreate,
        },
      },
    }));
    mockCreate.mockImplementation((args: { messages: { role: string; content: string }[] }) => {
      const system = args.messages[0].content;
      const user = args.messages[1].content;
      createCalls.push({ system, user });
      return Promise.resolve({
        usage: { total_tokens: 10, prompt_tokens: 6, completion_tokens: 4 },
        choices: [{ message: { content: llmResponseFor(system) } }],
      });
    });
  });

  it('encadeia data → lead → content → email (saída de um vira input do outro)', async () => {
    const res = await orchestrate({ objective: 'campanha de crescimento', user_id: 'u1' });

    // Plano e passos completos.
    expect(res.configured).toBe(true);
    expect(res.steps.map((s) => s.status)).toEqual([
      'completed',
      'completed',
      'completed',
      'completed',
    ]);

    // DATA MINER executou agregação REAL do banco (2 agentes, 1 ativo).
    const mining = res.steps[0].output as DataMiningResult;
    expect(mining.metrics.total_agents).toBe(2);
    expect(mining.metrics.active_agents).toBe(1);

    // LEAD MAGNET derivou tier hot de forma determinística (score 92).
    const leads = res.steps[1].output as LeadScoringResult;
    expect(leads.leads[0].tier).toBe('hot');

    // Saídas tipadas dos demais.
    expect((res.steps[2].output as ContentResult).topic).toBe('GrowthTopic');
    expect((res.steps[3].output as EmailSequenceResult).audience).toBe('quentes');

    // PROVA DE ENCADEAMENTO: o prompt de cada passo carrega a saída do anterior.
    const leadCall = createCalls.find((c) => c.system.includes('LEAD MAGNET'))!;
    expect(leadCall.user).toContain('aggregate-stats');
    expect(leadCall.user).toContain('total_agents'); // métricas do DATA MINER

    const contentCall = createCalls.find((c) => c.system.includes('CONTENT CREATOR'))!;
    expect(contentCall.user).toContain('ACME_HOT'); // lead vindo do LEAD MAGNET

    const emailCall = createCalls.find((c) => c.system.includes('EMAIL SEQUENCE BOT'))!;
    expect(emailCall.user).toContain('GrowthTopic'); // tópico vindo do CONTENT CREATOR

    // Rastro auditável na ordem correta.
    expect(res.trace.map((t) => t.agentName)).toEqual([
      'DATA MINER',
      'LEAD MAGNET',
      'CONTENT CREATOR',
      'EMAIL SEQUENCE BOT',
    ]);
  });
});

describe('orchestrate (degradação honesta sem OPENAI_API_KEY)', () => {
  let sb: ReturnType<typeof createSupabaseMock>;

  beforeEach(() => {
    jest.clearAllMocks();
    createCalls.length = 0;
    delete process.env.OPENAI_API_KEY;
    sb = createSupabaseMock();
    sb.setMany('agents', {
      data: [
        { role: 'CORE', status: 'IDLE', efficiency: 90 },
        { role: 'GUARD', status: 'ERROR', efficiency: 80 },
      ],
      error: null,
    });
    (createAdminClient as jest.Mock).mockReturnValue(sb.client);
    (getAgentById as jest.Mock).mockImplementation((id: string) => Promise.resolve(AGENTS[id]));
    (OpenAI as unknown as jest.Mock).mockImplementation(() => ({
      chat: { completions: { create: mockCreate } },
    }));
  });

  it('devolve o PLANO completo; skill determinística roda de verdade; LLM marcado', async () => {
    const res = await orchestrate({ objective: 'campanha de crescimento', user_id: 'u1' });

    // Plano completo mesmo sem chave.
    expect(res.plan.steps).toHaveLength(4);
    expect(res.configured).toBe(false);

    // aggregate-stats (determinística) executa de verdade → partial + métricas reais.
    expect(res.steps[0].status).toBe('partial');
    const mining = res.steps[0].output as DataMiningResult;
    expect(mining.metrics.total_agents).toBe(2);
    expect(mining.metrics.active_agents).toBe(1);
    expect(mining.insights).toEqual([]); // sem insights inventados

    // Passos que precisam de LLM ficam pendentes de configuração.
    expect(res.steps.slice(1).map((s) => s.status)).toEqual([
      'requires_configuration',
      'requires_configuration',
      'requires_configuration',
    ]);

    // O LLM NÃO foi chamado.
    expect(mockCreate).not.toHaveBeenCalled();

    // Rastro presente para auditoria.
    expect(res.trace).toHaveLength(4);
  });
});
