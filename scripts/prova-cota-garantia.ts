/**
 * ═══════════════════════════════════════════════════════════════════════════
 * PROVA (DRY-RUN) — A COTA DE GARANTIA. Zero token, zero banco.
 * ═══════════════════════════════════════════════════════════════════════════
 * Exercita a lógica pura de quota.ts em cenários-chave e imprime o custo
 * máximo de token de honrar um reembolso. Não chama IA, não toca no banco.
 *
 *   npx tsx scripts/prova-cota-garantia.ts
 * ═══════════════════════════════════════════════════════════════════════════
 */
import { evaluateUsage, EXPERIMENTATION_QUOTA, type PlanId } from '../frontend/src/lib/quota';

const DAY = 24 * 60 * 60 * 1000;
const START = Date.parse('2026-07-01T00:00:00Z');
const at = (d: number) => START + d * DAY;

function show(label: string, s: Parameters<typeof evaluateUsage>[0]) {
  const d = evaluateUsage(s);
  const flag = d.allowed ? 'PODE ' : 'BARRA';
  console.log(
    `  ${flag} | ${label.padEnd(46)} uso=${String(d.usage).padStart(4)}/${d.quota} ` +
    `dia=${String(d.dayInWindow).padStart(2)} reembolso=${d.refundEligible ? 'sim' : 'não '} · ${d.reason}`,
  );
}

console.log('=== PROVA DA COTA DE GARANTIA (dry-run, sem token, sem banco) ===\n');
console.log('Cotas por plano:', JSON.stringify(EXPERIMENTATION_QUOTA), '\n');

const base = { plan: 'pro' as PlanId, founderAccess: false, guaranteeStartedAt: new Date(START).toISOString(), guaranteeWaived: false };

console.log('Plano PRO (cota 300):');
show('dia 1, 10 usos — avaliando', { ...base, usageInWindow: 10, nowMs: at(1) });
show('dia 3, 300 usos — cota cheia na janela legal', { ...base, usageInWindow: 300, nowMs: at(3) });
show('dia 10, 300 usos — cota cheia, sem confirmar', { ...base, usageInWindow: 300, nowMs: at(10) });
show('dia 10, 300 usos — CONFIRMOU permanência', { ...base, guaranteeWaived: true, usageInWindow: 300, nowMs: at(10) });
show('dia 3, 300 usos — CONFIRMOU (mas legal, não vale)', { ...base, guaranteeWaived: true, usageInWindow: 300, nowMs: at(3) });
show('dia 31, 5000 usos — efetivado, fora da garantia', { ...base, usageInWindow: 5000, nowMs: at(31) });

console.log('\nFundador (ilimitado):');
show('dia 10, 99999 usos', { ...base, founderAccess: true, usageInWindow: 99999, nowMs: at(10) });

console.log('\nConta sem janela (legada):');
show('sem guarantee_started_at', { ...base, guaranteeStartedAt: null, usageInWindow: 99999, nowMs: at(10) });

// ── Custo máximo de honrar um reembolso: no máximo Q execuções ──
console.log('\n=== CUSTO MÁXIMO DE UM REEMBOLSO (o teto é a cota Q) ===');
const BRL = 5.5; // câmbio de referência USD→BRL
const CUSTO_AGENTE_USD = 0.00135; // gpt-4o-mini, chamada cheia (~1k in + 2k out)
const CUSTO_ORION_USD = 0.015;    // chat ORION (Claude), ~500 in + 900 out
for (const plan of ['starter', 'pro', 'enterprise'] as PlanId[]) {
  const q = EXPERIMENTATION_QUOTA[plan];
  const agente = (q * CUSTO_AGENTE_USD * BRL).toFixed(2);
  const orion = (q * CUSTO_ORION_USD * BRL).toFixed(2);
  console.log(`  ${plan.padEnd(11)} Q=${String(q).padStart(3)} → tokens no pior caso: R$ ${agente} (agentes) a R$ ${orion} (tudo ORION)`);
}
console.log('\nComparado aos planos (R$ 990 / 4.900 / 9.900), o token de um reembolso é < 1% a ~4%. Não sangra.');
