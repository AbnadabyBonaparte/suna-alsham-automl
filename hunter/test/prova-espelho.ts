// ============================================================================
// PROVA DOS NOVE — Fase 4 (O Espelho). Nao toca no banco de producao.
// O teste central: provar que o Espelho NAO CONSEGUE gravar status='active'.
// ============================================================================
import { assertPropostaLegal, insertMissionProposal, ESPELHO_STATUS_UNICO, ESPELHO_AUTOR, type FindingJulgado } from "../src/db.js";
import { medirPorFonte, medirCalibracao, decidir, MIN_VEREDITOS_TOTAL } from "../src/espelho.js";
import { writeEspelho } from "../src/espelho-report.js";
import { readFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const NL = String.fromCharCode(10);
let falhas = 0;
function ok(c: boolean, m: string) {
  console.log((c ? "  [OK]   " : "  [FALHA]") + " " + m);
  if (!c) falhas++;
}
function lanca(fn: () => void, trecho: string, m: string) {
  try {
    fn();
    ok(false, m + " — NAO lancou (trava furada!)");
  } catch (e) {
    const msg = String(e);
    ok(msg.includes(trecho), m + " — lancou: " + msg.slice(0, 95));
  }
}

const SOURCES = { arxiv: true, github: true, hackernews: true };
const base = { version: 3, status: ESPELHO_STATUS_UNICO, mission_md: "x", sources: SOURCES, scoring_rules: {}, created_by: ESPELHO_AUTOR };

console.log(NL + "=== TRAVAS DE LEI — o Espelho so LE, MEDE e PROPOE ===" + NL);

// A trava que mais importa: jamais 'active'.
lanca(() => assertPropostaLegal({ ...base, status: "active" }, SOURCES, 40), "TRAVA DE LEI", "status='active' e REJEITADO");
lanca(() => assertPropostaLegal({ ...base, status: "draft" }, SOURCES, 40), "TRAVA DE LEI", "status='draft' e rejeitado (so 'proposed')");
lanca(() => assertPropostaLegal({ ...base, status: "retired" }, SOURCES, 40), "TRAVA DE LEI", "status='retired' e rejeitado");
// Nao abre mina.
lanca(() => assertPropostaLegal({ ...base, sources: { ...SOURCES, reddit: true } }, SOURCES, 40), "nao abre nem fecha mina", "mina NOVA e rejeitada");
lanca(() => assertPropostaLegal({ ...base, sources: { arxiv: true } }, SOURCES, 40), "nao abre nem fecha mina", "fechar mina e rejeitado");
// Sem evidencia, sem proposta.
lanca(() => assertPropostaLegal(base, SOURCES, 0), "sem evidencia numerica", "proposta com 0 vereditos e rejeitada");
lanca(() => assertPropostaLegal(base, SOURCES, NaN), "sem evidencia numerica", "evidencia NaN e rejeitada");
// Autoria.
lanca(() => assertPropostaLegal({ ...base, created_by: "founder" }, SOURCES, 40), "created_by", "forjar autoria e rejeitado");
// O caminho legal passa.
try {
  assertPropostaLegal(base, SOURCES, 40);
  ok(true, "proposta legal (proposed + minas iguais + evidencia) PASSA");
} catch (e) {
  ok(false, "proposta legal foi barrada: " + String(e));
}

// A trava roda ANTES do banco: com status='active' nenhuma chamada acontece.
console.log(NL + "--- a trava age antes de tocar o banco:");
let tocouBanco = false;
const sbFalso: any = { from: () => { tocouBanco = true; return { insert: () => ({ select: () => ({ single: async () => ({ data: { id: 1 }, error: null }) }) }) }; } };
await insertMissionProposal(sbFalso, base, SOURCES, 40).then(() => ok(tocouBanco, "proposta legal chega ao banco")).catch((e) => ok(false, "legal falhou: " + e));
tocouBanco = false;
await insertMissionProposal(sbFalso, { ...base, status: "active" }, SOURCES, 40)
  .then(() => ok(false, "active gravou no banco — TRAVA FURADA"))
  .catch(() => ok(!tocouBanco, "active lancou SEM nenhuma chamada ao banco"));

// ── Medicao ────────────────────────────────────────────────────────────────
console.log(NL + "=== MEDICAO — taxas e calibracao ===" + NL);
const f = (id: number, source: string, relevance: number, verdict: string, single_source = true): FindingJulgado =>
  ({ id, hunt_id: 1, source, kind: "tool", title: "t" + id, relevance, single_source, verdict, created_at: "2026-07-27T00:00:00Z" });

const amostra: FindingJulgado[] = [
  f(1, "github", 90, "discard"), f(2, "github", 85, "discard"), f(3, "github", 80, "discard"),
  f(4, "github", 75, "adopt"), f(5, "github", 60, "watch"),
  f(6, "arxiv", 90, "adopt"), f(7, "arxiv", 85, "adopt"), f(8, "arxiv", 80, "adopt"),
  f(9, "arxiv", 30, "adopt"), f(10, "arxiv", 20, "adopt"), f(11, "arxiv", 35, "adopt"),
  f(12, "hacker-news", 50, "watch"), f(13, "hacker-news", 40, "pending"),
];
const pf = medirPorFonte(amostra);
const gh = pf.find((x) => x.fonte === "github")!;
const hn = pf.find((x) => x.fonte === "hacker-news")!;
ok(gh.julgados === 5 && gh.discard === 3, "github: 5 julgados, 3 descartes");
ok(Math.round(gh.taxaDescarte! * 100) === 60, "github: taxa de descarte 60%");
ok(hn.pending === 1 && hn.julgados === 1, "pending NAO entra no denominador (hacker-news: 1 julgado, 1 pendente)");
ok(hn.suficiente === false, "mina com poucos vereditos e marcada INSUFICIENTE");
const semVeredito = medirPorFonte([f(99, "x", 50, "pending")])[0];
ok(semVeredito.taxaAdocao === null, "taxa sem denominador e null, nao 0%");

const cal = medirCalibracao(amostra);
ok(cal.julgados === 12, "12 vereditos (o pending fora)");
ok(cal.superestimou.length === 3, "3 superestimados (rel>=71 e descartados)");
ok(cal.subestimou.length === 3, "3 subestimados (rel<41 e adotados)");
// ids 4(75) 6(90) 7(85) 8(80): fonte unica, rel>=71, veredito adopt = 4
ok(cal.fonteUnicaAcimaDoTeto === 7, "7 de fonte unica passaram do teto (rel>=71)");
ok(cal.fonteUnicaAdotada === 4, "4 desses foram ADOTADOS — a regra v2 nao segurou");

// ── Decisao ────────────────────────────────────────────────────────────────
console.log(NL + "=== DECISAO — amostra insuficiente NAO propoe ===" + NL);
const poucos = amostra.slice(0, 4);
const d1 = decidir(medirPorFonte(poucos), medirCalibracao(poucos));
ok(d1.propoe === false, "com 4 vereditos (< " + MIN_VEREDITOS_TOTAL + ") NAO propoe");
ok(d1.motivo.includes("amostra insuficiente"), "motivo diz 'amostra insuficiente': " + d1.motivo.slice(0, 60));

const muitos = [...amostra, ...amostra.map((x, i) => ({ ...x, id: 100 + i }))];
const d2 = decidir(medirPorFonte(muitos), medirCalibracao(muitos));
ok(d2.propoe === true, "com " + medirCalibracao(muitos).julgados + " vereditos e padrao claro, PROPOE");
ok(d2.achados.length > 0, "proposta vem com achados numerados: " + d2.achados.length);
ok(d2.achados.some((a) => a.includes("github") && a.includes("DESCARTE")), "aponta a mina de lixo nominalmente");

// ── Relatorio sempre sai ───────────────────────────────────────────────────
console.log(NL + "=== RELATORIO — presta contas mesmo sem proposta ===" + NL);
const dir = mkdtempSync(join(tmpdir(), "espelho-"));
process.env.HUNTER_REPORT_DIR = dir;
const caminho = writeEspelho({
  date: "2026-07-27", janelaDias: 7, missaoAtiva: 1,
  hunts: [{ id: 4, status: "done", itemsSeen: 89, itemsKept: 14, custo: 0.0291 }],
  totalFindings: poucos.length, porFonte: medirPorFonte(poucos), cal: medirCalibracao(poucos),
  veredito: d1, propostaId: null, versaoProposta: null, minTotal: MIN_VEREDITOS_TOTAL, minFonte: 5,
});
const md = readFileSync(join(dir, "espelho-2026-07-27.md"), "utf8");
ok(caminho === "caça/espelho-2026-07-27.md", "caminho canonico: " + caminho);
ok(md.includes("**NÃO PROPÕE.**"), "relatorio sai mesmo sem proposta");
ok(md.includes("amostra insuficiente"), "relatorio declara a insuficiencia");
ok(md.includes("NÃO VERIFICÁVEL"), "relatorio declara que tracao nao e medivel pelo schema");
ok(md.includes("| `github` |"), "tabela por mina presente");

console.log(NL + (falhas ? "=== " + falhas + " FALHA(S) ===" : "=== TODAS AS PROVAS PASSARAM ==="));
process.exit(falhas ? 1 : 0);
