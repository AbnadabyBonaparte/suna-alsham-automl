import {
  parseJsonLoose,
  tierFromScore,
  aggregateAgentStats,
  getBehavior,
  AGENT_BEHAVIORS,
  type BehaviorContext,
  type LeadScoringResult,
  type ContentResult,
  type EmailSequenceResult,
  type DataMiningResult,
} from '@/lib/quantum-brain/agent-behaviors';

const ctx = (over: Partial<BehaviorContext> = {}): BehaviorContext => ({
  title: 'Tarefa',
  description: 'Descrição',
  ...over,
});

describe('parseJsonLoose', () => {
  it('faz parse de JSON simples', () => {
    expect(parseJsonLoose('{"a":1}')).toEqual({ a: 1 });
  });
  it('remove cercas ```json', () => {
    expect(parseJsonLoose('```json\n{"a":2}\n```')).toEqual({ a: 2 });
  });
  it('extrai bloco {...} embutido em texto', () => {
    expect(parseJsonLoose('resposta: {"a":3} fim')).toEqual({ a: 3 });
  });
  it('retorna {} para lixo ou vazio', () => {
    expect(parseJsonLoose('nao é json')).toEqual({});
    expect(parseJsonLoose('')).toEqual({});
    expect(parseJsonLoose(null)).toEqual({});
  });
});

describe('tierFromScore (determinístico)', () => {
  it.each([
    [100, 'hot'],
    [70, 'hot'],
    [69, 'warm'],
    [40, 'warm'],
    [39, 'cold'],
    [0, 'cold'],
  ])('score %i → %s', (score, tier) => {
    expect(tierFromScore(score as number)).toBe(tier);
  });
});

describe('aggregateAgentStats (agregação real)', () => {
  it('conta total, ativos, por role e média de eficiência', () => {
    const summary = aggregateAgentStats([
      { role: 'CORE', status: 'IDLE', efficiency: 90 },
      { role: 'CORE', status: 'PROCESSING', efficiency: 80 },
      { role: 'GUARD', status: 'ERROR', efficiency: 70 },
      { role: 'ANALYST', status: 'LEARNING', efficiency: 60 },
    ]);
    expect(summary.total_agents).toBe(4);
    expect(summary.active_agents).toBe(3); // ERROR não é ativo
    expect(summary.by_role).toEqual({ CORE: 2, GUARD: 1, ANALYST: 1 });
    expect(summary.average_efficiency).toBe(75);
  });

  it('retorna zeros para lista vazia (Lei da Honestidade — mostra 0)', () => {
    expect(aggregateAgentStats([])).toEqual({
      total_agents: 0,
      active_agents: 0,
      by_role: {},
      average_efficiency: 0,
    });
  });

  it('trata role/efficiency ausentes', () => {
    const s = aggregateAgentStats([{ status: 'IDLE' }, { role: 'GUARD', status: 'IDLE' }]);
    expect(s.by_role).toEqual({ UNKNOWN: 1, GUARD: 1 });
    expect(s.average_efficiency).toBe(0);
  });
});

describe('LEAD MAGNET behavior.parse', () => {
  it('clampa scores 0-100, deriva tier e mapeia campos', () => {
    const raw = JSON.stringify({
      leads: [
        { name: 'ACME', score: 150, rationale: 'grande', suggested_action: 'ligar' },
        { name: 'Beta', score: -5, rationale: 'frio' },
        { name: 'Gama', score: 55 },
      ],
      summary: 'ok',
      next_actions: ['follow-up'],
    });
    const out = getBehavior('lead-magnet')!.parse(raw, ctx()) as LeadScoringResult;
    expect(out.task_type).toBe('lead_scoring');
    expect(out.configured).toBe(true);
    expect(out.leads[0]).toMatchObject({ name: 'ACME', score: 100, tier: 'hot' });
    expect(out.leads[1]).toMatchObject({ score: 0, tier: 'cold' });
    expect(out.leads[2]).toMatchObject({ score: 55, tier: 'warm' });
    expect(out.next_actions).toEqual(['follow-up']);
  });

  it('notConfigured devolve estrutura vazia honesta', () => {
    const out = getBehavior('lead-magnet')!.notConfigured(ctx()) as LeadScoringResult;
    expect(out.configured).toBe(false);
    expect(out.leads).toEqual([]);
    expect(out.message).toMatch(/OPENAI_API_KEY/);
  });
});

describe('CONTENT CREATOR behavior.parse', () => {
  it('normaliza formato inválido para social e mapeia hashtags', () => {
    const raw = JSON.stringify({
      topic: 'Lançamento',
      pieces: [
        { format: 'blog', title: 'T1', body: 'B1', hashtags: ['#a'], cta: 'Leia' },
        { format: 'tiktok', title: 'T2', body: 'B2' },
      ],
      next_actions: ['revisar'],
    });
    const out = getBehavior('content-creator')!.parse(raw, ctx()) as ContentResult;
    expect(out.pieces[0].format).toBe('blog');
    expect(out.pieces[0].hashtags).toEqual(['#a']);
    expect(out.pieces[1].format).toBe('social'); // fallback
    expect(out.pieces[1].hashtags).toEqual([]);
    expect(out.topic).toBe('Lançamento');
  });
});

describe('EMAIL SEQUENCE BOT behavior.parse', () => {
  it('reindexa passos, clampa delay >= 0 e soma a duração total', () => {
    const raw = JSON.stringify({
      audience: 'Trials',
      steps: [
        { delay_days: 0, subject: 'Bem-vindo', body: 'x', goal: 'ativar' },
        { delay_days: -3, subject: 'Dica', body: 'y', goal: 'engajar' },
        { delay_days: 5, subject: 'Oferta', body: 'z', goal: 'converter' },
      ],
      next_actions: ['medir'],
    });
    const out = getBehavior('email-sequence-bot')!.parse(raw, ctx()) as EmailSequenceResult;
    expect(out.steps.map((s) => s.step)).toEqual([1, 2, 3]);
    expect(out.steps[1].delay_days).toBe(0); // -3 clampado
    expect(out.total_duration_days).toBe(5); // 0 + 0 + 5
    expect(out.audience).toBe('Trials');
  });
});

describe('DATA MINER behavior', () => {
  it('needsAgentStats é true', () => {
    expect(getBehavior('data-miner')!.needsAgentStats).toBe(true);
  });

  it('parse usa métricas REAIS do contexto e insights do LLM', () => {
    const stats = {
      total_agents: 10,
      active_agents: 9,
      by_role: { CORE: 1 },
      average_efficiency: 88.5,
    };
    const raw = JSON.stringify({ insights: ['9/10 ativos'], recommendations: ['revisar 1'] });
    const out = getBehavior('data-miner')!.parse(
      raw,
      ctx({ agentStats: stats }),
    ) as DataMiningResult;
    expect(out.metrics).toEqual(stats); // não inventa números
    expect(out.insights).toEqual(['9/10 ativos']);
  });

  it('notConfigured preserva métricas reais (não depende do LLM)', () => {
    const stats = {
      total_agents: 3,
      active_agents: 3,
      by_role: { GUARD: 3 },
      average_efficiency: 90,
    };
    const out = getBehavior('data-miner')!.notConfigured(
      ctx({ agentStats: stats }),
    ) as DataMiningResult;
    expect(out.configured).toBe(false);
    expect(out.metrics).toEqual(stats);
    expect(out.insights).toEqual([]);
  });
});

describe('registro de comportamentos', () => {
  it('expõe os 4 agentes com comportamento real', () => {
    expect(Object.keys(AGENT_BEHAVIORS).sort()).toEqual([
      'content-creator',
      'data-miner',
      'email-sequence-bot',
      'lead-magnet',
    ]);
  });

  it('getBehavior retorna undefined para agente genérico', () => {
    expect(getBehavior('revenue-hunter')).toBeUndefined();
    expect(getBehavior(null)).toBeUndefined();
  });
});
