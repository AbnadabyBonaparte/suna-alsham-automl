// ═══════════════════════════════════════════════════════════════
// COMPORTAMENTOS POR AGENTE - CONTRATOS TIPADOS (PURO / TESTÁVEL)
// ═══════════════════════════════════════════════════════════════
// Cada agente com comportamento real define:
//   - systemPrompt específico (instrui o LLM a devolver o schema)
//   - buildUserPrompt: monta a mensagem do usuário a partir da tarefa
//   - parse: mapeia a resposta (JSON do LLM) para uma saída TIPADA,
//     normalizando/derivando campos de forma determinística
//   - notConfigured: saída honesta quando não há LLM configurado
//     (nunca inventa dados; para o DATA MINER preserva as métricas
//     REAIS do banco, que não dependem do LLM)
//
// A camada determinística (parse/derivação/agregação) é o que os
// testes unitários exercitam sem chamar o LLM.
// ═══════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────
// Contexto passado para os comportamentos
// ─────────────────────────────────────────────────────────────
export interface BehaviorContext {
  title: string;
  description: string;
  data?: Record<string, unknown>;
  /** Agregado REAL do banco, injetado pelo executor para o DATA MINER. */
  agentStats?: AgentStatsSummary;
}

// ─────────────────────────────────────────────────────────────
// Contratos de saída (tipados) por agente
// ─────────────────────────────────────────────────────────────
export type LeadTier = 'hot' | 'warm' | 'cold';

export interface ScoredLead {
  name: string;
  score: number; // 0-100
  tier: LeadTier; // derivado de forma determinística do score
  rationale: string;
  suggested_action: string;
}

export interface LeadScoringResult {
  task_type: 'lead_scoring';
  configured: boolean;
  message?: string;
  leads: ScoredLead[];
  summary: string;
  next_actions: string[];
}

export type ContentFormat = 'blog' | 'social' | 'email' | 'ad';

export interface ContentPiece {
  format: ContentFormat;
  title: string;
  body: string;
  hashtags: string[];
  cta: string;
}

export interface ContentResult {
  task_type: 'content';
  configured: boolean;
  message?: string;
  topic: string;
  pieces: ContentPiece[];
  next_actions: string[];
}

export interface EmailStep {
  step: number; // reindexado sequencialmente a partir de 1
  delay_days: number; // >= 0
  subject: string;
  body: string;
  goal: string;
}

export interface EmailSequenceResult {
  task_type: 'email_sequence';
  configured: boolean;
  message?: string;
  audience: string;
  steps: EmailStep[];
  total_duration_days: number; // soma determinística dos delay_days
  next_actions: string[];
}

export interface AgentStatsSummary {
  total_agents: number;
  active_agents: number;
  by_role: Record<string, number>;
  average_efficiency: number; // arredondado a 2 casas
}

export interface DataMiningResult {
  task_type: 'data_mining';
  configured: boolean;
  message?: string;
  metrics: AgentStatsSummary; // dados REAIS do banco (Lei da Honestidade)
  insights: string[];
  recommendations: string[];
}

export type AgentContractOutput =
  | LeadScoringResult
  | ContentResult
  | EmailSequenceResult
  | DataMiningResult;

// ─────────────────────────────────────────────────────────────
// Helpers determinísticos (puros)
// ─────────────────────────────────────────────────────────────

const NOT_CONFIGURED_MESSAGE =
  'LLM não configurado. Defina OPENAI_API_KEY nas variáveis de ambiente para gerar este resultado.';

/** Remove cercas ```json e faz parse tolerante. Nunca lança. */
export function parseJsonLoose(content: string | null | undefined): Record<string, unknown> {
  if (!content) return {};
  const cleaned = content.replace(/```json\n?|```/g, '').trim();
  try {
    const parsed = JSON.parse(cleaned);
    return parsed && typeof parsed === 'object' ? (parsed as Record<string, unknown>) : {};
  } catch {
    // tenta extrair o primeiro bloco {...}
    const match = cleaned.match(/\{[\s\S]*\}/);
    if (match) {
      try {
        return JSON.parse(match[0]) as Record<string, unknown>;
      } catch {
        return {};
      }
    }
    return {};
  }
}

function clampScore(value: unknown): number {
  const n = typeof value === 'number' ? value : Number(value);
  if (!Number.isFinite(n)) return 0;
  return Math.max(0, Math.min(100, Math.round(n)));
}

/** Faixa determinística a partir do score. */
export function tierFromScore(score: number): LeadTier {
  if (score >= 70) return 'hot';
  if (score >= 40) return 'warm';
  return 'cold';
}

function asString(value: unknown, fallback = ''): string {
  if (typeof value === 'string') return value;
  if (value == null) return fallback;
  return String(value);
}

function asStringArray(value: unknown): string[] {
  if (Array.isArray(value)) {
    return value.map((v) => asString(v)).filter((s) => s.length > 0);
  }
  if (typeof value === 'string' && value.trim().length > 0) return [value.trim()];
  return [];
}

function asRecordArray(value: unknown): Record<string, unknown>[] {
  if (!Array.isArray(value)) return [];
  return value.filter((v): v is Record<string, unknown> => !!v && typeof v === 'object');
}

const CONTENT_FORMATS: ContentFormat[] = ['blog', 'social', 'email', 'ad'];
function normalizeFormat(value: unknown): ContentFormat {
  const f = asString(value).toLowerCase().trim();
  return (CONTENT_FORMATS as string[]).includes(f) ? (f as ContentFormat) : 'social';
}

function nonNegativeInt(value: unknown): number {
  const n = typeof value === 'number' ? value : Number(value);
  if (!Number.isFinite(n)) return 0;
  return Math.max(0, Math.round(n));
}

// ─────────────────────────────────────────────────────────────
// Agregação REAL de agentes (usada pelo DATA MINER) — determinística
// ─────────────────────────────────────────────────────────────
export interface AgentStatRow {
  role?: string | null;
  status?: string | null;
  efficiency?: number | null;
}

const ACTIVE = new Set(['IDLE', 'PROCESSING', 'LEARNING']);

/** Mapeia linhas cruas da tabela agents em um resumo agregado real. */
export function aggregateAgentStats(rows: AgentStatRow[]): AgentStatsSummary {
  const total = rows.length;
  let active = 0;
  let effSum = 0;
  const byRole: Record<string, number> = {};

  for (const row of rows) {
    if (ACTIVE.has((row.status || '') as string)) active++;
    effSum += typeof row.efficiency === 'number' ? row.efficiency : 0;
    const role = (row.role || 'UNKNOWN') as string;
    byRole[role] = (byRole[role] || 0) + 1;
  }

  const avg = total > 0 ? Math.round((effSum / total) * 100) / 100 : 0;

  return {
    total_agents: total,
    active_agents: active,
    by_role: byRole,
    average_efficiency: avg,
  };
}

// ─────────────────────────────────────────────────────────────
// Contrato de comportamento
// ─────────────────────────────────────────────────────────────
export interface AgentBehavior {
  id: string;
  agentName: string;
  /** Descrição curta do que o agente faz (para docs/UI). */
  summary: string;
  /** Se true, o executor injeta agentStats reais no contexto. */
  needsAgentStats?: boolean;
  systemPrompt: string;
  buildUserPrompt(ctx: BehaviorContext): string;
  parse(rawContent: string, ctx: BehaviorContext): AgentContractOutput;
  notConfigured(ctx: BehaviorContext): AgentContractOutput;
}

function baseTaskBlock(ctx: BehaviorContext): string {
  return `TAREFA: ${ctx.title}
DESCRIÇÃO: ${ctx.description}
DADOS: ${JSON.stringify(ctx.data || {})}`;
}

// ─────────────────────────────────────────────────────────────
// LEAD MAGNET — lead scoring estruturado
// ─────────────────────────────────────────────────────────────
const leadMagnet: AgentBehavior = {
  id: 'lead-magnet',
  agentName: 'LEAD MAGNET',
  summary:
    'Qualifica e pontua leads (0-100), deriva a faixa (hot/warm/cold) e sugere a próxima ação de prospecção.',
  systemPrompt:
    'Você é LEAD MAGNET, especialista em qualificação de leads. A partir da tarefa e dos dados fornecidos, ' +
    'pontue cada lead de 0 a 100 e justifique. Responda SOMENTE em JSON válido no formato: ' +
    '{ "leads": [{ "name": string, "score": number, "rationale": string, "suggested_action": string }], ' +
    '"summary": string, "next_actions": string[] }. Nunca invente números que não consiga justificar.',
  buildUserPrompt(ctx) {
    return `${baseTaskBlock(ctx)}\n\nPontue os leads e devolva o JSON do contrato.`;
  },
  parse(rawContent, ctx) {
    const json = parseJsonLoose(rawContent);
    const leads: ScoredLead[] = asRecordArray(json.leads).map((l) => {
      const score = clampScore(l.score);
      return {
        name: asString(l.name, 'Lead sem nome'),
        score,
        tier: tierFromScore(score),
        rationale: asString(l.rationale),
        suggested_action: asString(l.suggested_action),
      };
    });
    return {
      task_type: 'lead_scoring',
      configured: true,
      leads,
      summary: asString(json.summary) || `${leads.length} lead(s) avaliado(s) para: ${ctx.title}`,
      next_actions: asStringArray(json.next_actions),
    };
  },
  notConfigured() {
    return {
      task_type: 'lead_scoring',
      configured: false,
      message: NOT_CONFIGURED_MESSAGE,
      leads: [],
      summary: '',
      next_actions: [],
    };
  },
};

// ─────────────────────────────────────────────────────────────
// CONTENT CREATOR — conteúdo multi-formato com schema
// ─────────────────────────────────────────────────────────────
const contentCreator: AgentBehavior = {
  id: 'content-creator',
  agentName: 'CONTENT CREATOR',
  summary:
    'Gera conteúdo em múltiplos formatos (blog/social/email/ad), cada peça com título, corpo, hashtags e CTA.',
  systemPrompt:
    'Você é CONTENT CREATOR, especialista em conteúdo. Produza peças em múltiplos formatos ' +
    '(blog, social, email, ad). Responda SOMENTE em JSON válido no formato: ' +
    '{ "topic": string, "pieces": [{ "format": "blog"|"social"|"email"|"ad", "title": string, ' +
    '"body": string, "hashtags": string[], "cta": string }], "next_actions": string[] }.',
  buildUserPrompt(ctx) {
    return `${baseTaskBlock(ctx)}\n\nCrie ao menos 2 formatos diferentes e devolva o JSON do contrato.`;
  },
  parse(rawContent, ctx) {
    const json = parseJsonLoose(rawContent);
    const pieces: ContentPiece[] = asRecordArray(json.pieces).map((p) => ({
      format: normalizeFormat(p.format),
      title: asString(p.title),
      body: asString(p.body),
      hashtags: asStringArray(p.hashtags),
      cta: asString(p.cta),
    }));
    return {
      task_type: 'content',
      configured: true,
      topic: asString(json.topic) || ctx.title,
      pieces,
      next_actions: asStringArray(json.next_actions),
    };
  },
  notConfigured(ctx) {
    return {
      task_type: 'content',
      configured: false,
      message: NOT_CONFIGURED_MESSAGE,
      topic: ctx.title,
      pieces: [],
      next_actions: [],
    };
  },
};

// ─────────────────────────────────────────────────────────────
// EMAIL SEQUENCE BOT — cadência de e-mails com estrutura real
// ─────────────────────────────────────────────────────────────
const emailSequenceBot: AgentBehavior = {
  id: 'email-sequence-bot',
  agentName: 'EMAIL SEQUENCE BOT',
  summary:
    'Monta uma sequência de e-mails ordenada (passos reindexados, atraso em dias) e calcula a duração total.',
  systemPrompt:
    'Você é EMAIL SEQUENCE BOT, especialista em sequências de e-mail. Crie uma cadência ordenada. ' +
    'Responda SOMENTE em JSON válido no formato: { "audience": string, "steps": [{ "delay_days": number, ' +
    '"subject": string, "body": string, "goal": string }], "next_actions": string[] }.',
  buildUserPrompt(ctx) {
    return `${baseTaskBlock(ctx)}\n\nMonte a sequência de e-mails e devolva o JSON do contrato.`;
  },
  parse(rawContent, ctx) {
    const json = parseJsonLoose(rawContent);
    const steps: EmailStep[] = asRecordArray(json.steps).map((s, i) => ({
      step: i + 1, // reindex determinístico
      delay_days: nonNegativeInt(s.delay_days),
      subject: asString(s.subject),
      body: asString(s.body),
      goal: asString(s.goal),
    }));
    const totalDuration = steps.reduce((sum, s) => sum + s.delay_days, 0);
    return {
      task_type: 'email_sequence',
      configured: true,
      audience: asString(json.audience) || asString(ctx.data?.audience) || ctx.title,
      steps,
      total_duration_days: totalDuration,
      next_actions: asStringArray(json.next_actions),
    };
  },
  notConfigured(ctx) {
    return {
      task_type: 'email_sequence',
      configured: false,
      message: NOT_CONFIGURED_MESSAGE,
      audience: asString(ctx.data?.audience) || ctx.title,
      steps: [],
      total_duration_days: 0,
      next_actions: [],
    };
  },
};

// ─────────────────────────────────────────────────────────────
// DATA MINER — agregação REAL do banco + enriquecimento por LLM
// ─────────────────────────────────────────────────────────────
const EMPTY_STATS: AgentStatsSummary = {
  total_agents: 0,
  active_agents: 0,
  by_role: {},
  average_efficiency: 0,
};

const dataMiner: AgentBehavior = {
  id: 'data-miner',
  agentName: 'DATA MINER',
  summary:
    'Agrega métricas REAIS da frota de agentes (contagens, ativos, média de eficiência) e gera insights sobre elas.',
  needsAgentStats: true,
  systemPrompt:
    'Você é DATA MINER, analista de dados. Você recebe MÉTRICAS REAIS já agregadas do banco. ' +
    'NÃO invente números: baseie-se apenas nas métricas fornecidas. Responda SOMENTE em JSON válido no formato: ' +
    '{ "insights": string[], "recommendations": string[] }.',
  buildUserPrompt(ctx) {
    const stats = ctx.agentStats || EMPTY_STATS;
    return `${baseTaskBlock(ctx)}\n\nMÉTRICAS REAIS (não invente números):\n${JSON.stringify(
      stats,
      null,
      2,
    )}\n\nGere insights e recomendações e devolva o JSON do contrato.`;
  },
  parse(rawContent, ctx) {
    const json = parseJsonLoose(rawContent);
    return {
      task_type: 'data_mining',
      configured: true,
      metrics: ctx.agentStats || EMPTY_STATS,
      insights: asStringArray(json.insights),
      recommendations: asStringArray(json.recommendations),
    };
  },
  notConfigured(ctx) {
    // As métricas são reais e NÃO dependem do LLM — preservamos.
    return {
      task_type: 'data_mining',
      configured: false,
      message: NOT_CONFIGURED_MESSAGE,
      metrics: ctx.agentStats || EMPTY_STATS,
      insights: [],
      recommendations: [],
    };
  },
};

// ─────────────────────────────────────────────────────────────
// Registro
// ─────────────────────────────────────────────────────────────
export const AGENT_BEHAVIORS: Record<string, AgentBehavior> = {
  [leadMagnet.id]: leadMagnet,
  [contentCreator.id]: contentCreator,
  [emailSequenceBot.id]: emailSequenceBot,
  [dataMiner.id]: dataMiner,
};

/** Retorna o comportamento tipado do agente, se houver. */
export function getBehavior(agentId: string | null | undefined): AgentBehavior | undefined {
  if (!agentId) return undefined;
  return AGENT_BEHAVIORS[agentId];
}
