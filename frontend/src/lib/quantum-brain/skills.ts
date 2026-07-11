// ═══════════════════════════════════════════════════════════════
// SKILLS - CAPACIDADES REUTILIZÁVEIS (COMPOSABILIDADE)
// ═══════════════════════════════════════════════════════════════
// Uma skill é uma capacidade nomeada provida por um agente. O
// orquestrador resolve skill → agente para compor um plano. É a
// camada que torna os agentes componíveis (como subagentes).
//
// `requiresLLM: false` significa que a skill produz uma saída
// determinística ÚTIL mesmo sem chave de LLM (ex.: agregação real de
// métricas). As demais precisam do LLM para produzir resultado.
// ═══════════════════════════════════════════════════════════════

export type SkillId = 'aggregate-stats' | 'score-leads' | 'generate-copy' | 'build-sequence';

export interface SkillDef {
  id: SkillId;
  summary: string;
  /** Agente que provê a skill (SSOT do mapeamento skill → agente). */
  agentId: string;
  /** false = produz saída determinística real mesmo sem LLM. */
  requiresLLM: boolean;
}

export const SKILLS: Record<SkillId, SkillDef> = {
  'aggregate-stats': {
    id: 'aggregate-stats',
    summary: 'Agrega métricas reais da frota de agentes (contagens, ativos, eficiência média).',
    agentId: 'data-miner',
    requiresLLM: false, // agregação é determinística; o LLM só enriquece com insights
  },
  'score-leads': {
    id: 'score-leads',
    summary: 'Pontua e qualifica leads (0-100) e deriva a faixa (hot/warm/cold).',
    agentId: 'lead-magnet',
    requiresLLM: true,
  },
  'generate-copy': {
    id: 'generate-copy',
    summary: 'Gera conteúdo multi-formato (blog/social/email/ad) para um segmento.',
    agentId: 'content-creator',
    requiresLLM: true,
  },
  'build-sequence': {
    id: 'build-sequence',
    summary: 'Monta uma sequência de e-mails ordenada com atrasos e objetivos.',
    agentId: 'email-sequence-bot',
    requiresLLM: true,
  },
};

/** Resolve o agente que provê uma skill. */
export function resolveAgentForSkill(skill: SkillId): string {
  return SKILLS[skill].agentId;
}

/** Indica se a skill precisa de LLM para produzir resultado. */
export function skillRequiresLLM(skill: SkillId): boolean {
  return SKILLS[skill].requiresLLM;
}

/** Lista as skills providas por um agente. */
export function skillsForAgent(agentId: string): SkillId[] {
  return (Object.values(SKILLS) as SkillDef[])
    .filter((s) => s.agentId === agentId)
    .map((s) => s.id);
}
