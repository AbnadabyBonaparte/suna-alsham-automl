// ============================================================================
// PROVA DOS NOVE — Fase 3, pecas 2 e 3 (sem tocar no banco de producao)
// ============================================================================
// Exercita as rotinas REAIS (writeReport, openThreatIssue) com dados de teste.
// Nao substitui a caca real; prova que o CAMINHO DE CODIGO existe e funciona.
// ============================================================================
import { writeReport, type PendingItem } from "../src/report.js";
import { openThreatIssue, threatIssueTitle } from "../src/db.js";
import { readFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const NL = String.fromCharCode(10);
let falhas = 0;
function ok(cond: boolean, msg: string) {
  console.log((cond ? "  [OK]   " : "  [FALHA]") + " " + msg);
  if (!cond) falhas++;
}

// ── PECA 2: os pendentes orfaos do hunt #3 (ids 21-24) ressurgem ────────────
console.log(NL + "=== PECA 2 — FILA PENDENTE DE JULGAMENTO ===" + NL);
const pendentes: PendingItem[] = [
  { id: 21, hunt_id: 3, relevance: 88, kind: "tool",  title: "Orfao A do hunt #3", url: "https://ex.com/21", source: "github",     created_at: "2026-07-26T10:00:00Z" },
  { id: 22, hunt_id: 3, relevance: 74, kind: "paper", title: "Orfao B do hunt #3", url: "https://ex.com/22", source: "arxiv",      created_at: "2026-07-26T10:00:00Z" },
  { id: 23, hunt_id: 3, relevance: 91, kind: "threat",title: "Orfao C do hunt #3", url: "https://ex.com/23", source: "hackernews", created_at: "2026-07-26T10:00:00Z" },
  { id: 24, hunt_id: 3, relevance: 55, kind: "tech",  title: "Orfao D | com pipe", url: "https://ex.com/24", source: "github",     created_at: "2026-07-26T10:00:00Z" },
];
const dir = mkdtempSync(join(tmpdir(), "hunter-prova-"));
process.env.HUNTER_REPORT_DIR = dir;
writeReport({
  date: "2026-07-27", itemsSeen: 0, itemsKept: 0, itemsQueued: 0,
  sourcesOk: 3, sourcesFail: 0, failNotes: [], costUsd: 0, costNote: "teste",
  status: "done", gold: "", findings: [], pending: pendentes,
});
const md = readFileSync(join(dir, "2026-07-27.md"), "utf8");
console.log(md.slice(md.indexOf("## FILA PENDENTE")).trim() + NL);
ok(md.includes("## FILA PENDENTE DE JULGAMENTO"), "secao FILA PENDENTE presente");
for (const id of [21, 22, 23, 24]) ok(new RegExp("\\| " + id + " \\|").test(md), "id " + id + " ressurgiu no relatorio");
const ordem = [21, 22, 23, 24].map((i) => md.indexOf("| " + i + " |"));
ok(ordem[2] < ordem[0] && ordem[0] < ordem[1] && ordem[1] < ordem[3], "ordenado por relevancia desc (23:91 > 21:88 > 22:74 > 24:55)");
ok(md.includes("4 achado(s) de caças anteriores"), "contagem honesta no cabecalho da secao");

// ── PECA 3: ameaca >=90 abre issue, e nao reabre a mesma ────────────────────
console.log(NL + "=== PECA 3 — ISSUE AUTOMATICA DE AMEACA ===" + NL);
const chamadas: any[] = [];
process.env.GITHUB_TOKEN = "token-de-teste";
process.env.GITHUB_REPOSITORY = "AbnadabyBonaparte/suna-alsham-automl";
(globalThis as any).fetch = async (_u: string, init: any) => {
  chamadas.push(JSON.parse(init.body));
  return { ok: true, status: 201, json: async () => ({ html_url: "https://github.com/x/issues/999" }) } as any;
};
const ameaca = { title: "CVE critica em dependencia do Santuario", url: "https://ex.com/threat", source: "hackernews", relevance: 96, relevance_why: "afeta a stack em producao", summary_md: "Resumo proprio da ameaca." };
const conhecidas = new Set<string>();
const r1 = await openThreatIssue(conhecidas, ameaca);
ok(r1.created === true, "1a vez: issue ABERTA (" + r1.reason + ")");
ok(chamadas.length === 1, "exatamente 1 chamada HTTP de criacao");
ok(chamadas[0].title === "[HUNTER] Ameaça: " + ameaca.title, "titulo no formato canonico: " + chamadas[0].title);
ok(chamadas[0].body.includes("96/100"), "corpo traz a relevancia");
ok(chamadas[0].body.includes(ameaca.url), "corpo traz a url");
ok(chamadas[0].body.includes("Resumo proprio da ameaca."), "corpo traz o resumo");
ok(chamadas[0].labels.includes("hunter"), "issue etiquetada 'hunter'");

const r2 = await openThreatIssue(conhecidas, ameaca);
ok(r2.created === false, "2a vez: NAO reabriu (" + r2.reason + ")");
ok(chamadas.length === 1, "idempotente — continua 1 chamada HTTP");

const jaExistia = new Set<string>([threatIssueTitle(ameaca.title)]);
const r3 = await openThreatIssue(jaExistia, ameaca);
ok(r3.created === false, "issue preexistente no repo: NAO reabriu (" + r3.reason + ")");
ok(chamadas.length === 1, "idempotente entre cacas — continua 1 chamada HTTP");

console.log(NL + (falhas ? "=== " + falhas + " FALHA(S) ===" : "=== TODAS AS PROVAS PASSARAM ==="));
process.exit(falhas ? 1 : 0);
