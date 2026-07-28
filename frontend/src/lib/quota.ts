/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM — COTA DE EXPERIMENTAÇÃO (garantia anti-vazamento)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/lib/quota.ts
 *
 * O problema: garantia de reembolso generosa (bom pra vender) SEM virar
 * "usa o mês inteiro de token e pede o dinheiro de volta" (vazamento).
 *
 * O modelo (prática de mercado — free-trial cap + money-back):
 *  · Janela legal (0–7 dias, CDC art. 49): reembolso INTEGRAL e
 *    INCONDICIONAL. Uso limitado à cota Q (o limite é do SERVIÇO, não do
 *    direito de reembolso — o reembolso continua incondicional).
 *  · Janela comercial (8–30 dias): reembolso disponível enquanto o uso ≤ Q.
 *    O usuário pode CONFIRMAR que fica (renuncia à garantia de 30 dias) e a
 *    cota abre para a franquia cheia do plano. Sem confirmar, segue capado.
 *  · Após 30 dias: cliente efetivado, franquia cheia; garantia expirada.
 *  · Fundador (founder_access): ilimitado sempre.
 *
 * A TRAVA anti-vazamento: enquanto QUALQUER reembolso é possível, o uso
 * nunca passa de Q. Logo, o custo máximo de token de honrar um reembolso é Q.
 *
 * Esta função é PURA — recebe estado e devolve decisão. Zero I/O, zero token.
 * Testável em dry-run (ver scripts/prova-cota-garantia.ts).
 * ═══════════════════════════════════════════════════════════════
 */

export type PlanId = 'free' | 'starter' | 'pro' | 'enterprise';

export const GUARANTEE_LEGAL_DAYS = 7; // CDC art. 49 — arrependimento
export const GUARANTEE_TOTAL_DAYS = 30; // garantia comercial estendida
const DAY_MS = 24 * 60 * 60 * 1000;

/**
 * Cota de experimentação por plano (nº de execuções de agente durante a
 * janela de garantia). Números escolhidos por GENESIS a partir do custo real
 * de token medido: uma execução custa ~R$0,007 (agente gpt-4o-mini) a
 * ~R$0,083 (chat ORION). Ver docs/produtos/GARANTIA-COM-COTA.md §custo.
 */
export const EXPERIMENTATION_QUOTA: Record<PlanId, number> = {
  free: 20,
  starter: 100,
  pro: 300,
  enterprise: 500,
};

export interface UsageState {
  plan: PlanId;
  founderAccess: boolean;
  /** ISO string do início da garantia (1ª ativação). null = sem janela ativa. */
  guaranteeStartedAt: string | null;
  /** true se o usuário confirmou que fica (renunciou à garantia de 30 dias). */
  guaranteeWaived: boolean;
  /** execuções já feitas na janela (contagem de requests desde o início). */
  usageInWindow: number;
  /** momento da avaliação (ms). Injetado para ser testável/determinístico. */
  nowMs: number;
}

export interface QuotaDecision {
  allowed: boolean;
  reason: 'founder' | 'sem-janela' | 'dentro-da-cota' | 'cota-atingida' | 'garantia-renunciada' | 'efetivado';
  plan: PlanId;
  quota: number;
  usage: number;
  dayInWindow: number;
  withinLegalWindow: boolean;
  withinGuarantee: boolean;
  /** o usuário pode renunciar à garantia p/ liberar a cota? (só dias 8–30) */
  canWaive: boolean;
  /** ainda tem direito a reembolso? (legal 7d sempre; comercial 30d se uso ≤ Q) */
  refundEligible: boolean;
  message: string;
}

export function evaluateUsage(s: UsageState): QuotaDecision {
  const quota = EXPERIMENTATION_QUOTA[s.plan] ?? EXPERIMENTATION_QUOTA.free;
  const base = {
    plan: s.plan,
    quota,
    usage: s.usageInWindow,
    dayInWindow: 0,
    withinLegalWindow: false,
    withinGuarantee: false,
    canWaive: false,
  };

  // Fundador nunca é limitado.
  if (s.founderAccess) {
    return { ...base, allowed: true, reason: 'founder', refundEligible: false, message: 'Acesso de fundador — sem limite.' };
  }

  // Sem janela de garantia registrada (ex.: conta legada) — não bloqueia.
  if (!s.guaranteeStartedAt) {
    return { ...base, allowed: true, reason: 'sem-janela', refundEligible: false, message: 'Sem janela de garantia ativa.' };
  }

  const startMs = Date.parse(s.guaranteeStartedAt);
  const dayInWindow = Math.floor((s.nowMs - startMs) / DAY_MS);
  const withinLegalWindow = s.nowMs < startMs + GUARANTEE_LEGAL_DAYS * DAY_MS;
  const withinGuarantee = s.nowMs < startMs + GUARANTEE_TOTAL_DAYS * DAY_MS;
  const canWaive = withinGuarantee && !withinLegalWindow; // renúncia só vale após os 7 dias legais

  // Passou dos 30 dias: cliente efetivado, franquia cheia, garantia expirada.
  if (!withinGuarantee) {
    return {
      ...base, dayInWindow, withinLegalWindow: false, withinGuarantee: false, canWaive: false,
      allowed: true, reason: 'efetivado', refundEligible: false,
      message: 'Período de garantia encerrado — acesso pleno do plano.',
    };
  }

  // Dentro da garantia e já renunciou (só efetivo após os 7 dias legais): cota aberta.
  if (canWaive && s.guaranteeWaived) {
    return {
      ...base, dayInWindow, withinLegalWindow, withinGuarantee, canWaive: true,
      allowed: true, reason: 'garantia-renunciada', refundEligible: false,
      message: 'Você confirmou a permanência — cota liberada, sem garantia de 30 dias.',
    };
  }

  // Dentro da garantia, cota vale. Reembolso disponível enquanto uso ≤ Q.
  const allowed = s.usageInWindow < quota;
  const refundEligible = withinLegalWindow || s.usageInWindow <= quota;
  return {
    ...base, dayInWindow, withinLegalWindow, withinGuarantee, canWaive,
    allowed,
    reason: allowed ? 'dentro-da-cota' : 'cota-atingida',
    refundEligible,
    message: allowed
      ? `Avaliação: ${s.usageInWindow}/${quota} execuções usadas.`
      : canWaive
        ? `Cota de avaliação atingida (${quota}). Confirme a permanência para liberar o uso pleno do plano.`
        : `Cota de avaliação atingida (${quota}). O limite abre ao fim da janela de garantia.`,
  };
}
