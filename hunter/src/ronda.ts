// ============================================================================
// FASE 3 · peca 4 — AS CHECAGENS DO HUNTER NA RONDA
// ============================================================================
// A Ronda das Duas Cascatas e DOUTRINA (skill/canon), nao um workflow deste
// repo. Este arquivo e o BRACO EXECUTAVEL das checagens do cacador: a Ronda
// (ou o workflow ronda-hunter.yml) roda `npm run ronda` e recebe a prova.
//
// Lei da Contra-Prova: cada checagem compara o que o canon PROMETE com o que
// o mundo vivo ENTREGA. Nada aqui e opiniao — sao tres queries reais.
//
// Read-only por lei: detecta e relata. Nao corrige, nao escreve, nao deleta.
// ============================================================================
import { db, lastFinishedHunt, quarantineDepth, anonReadsHunterTables, createIssue } from "./db.js";
import { config } from "./config.js";
import { NL } from "./util.js";

const QUARENTENA_TETO = Number(process.env.HUNTER_QUARANTINE_MAX ?? 500);
const CACA_MAX_HORAS = 24;

type Check = {
  nome: string;
  promessa: string;
  prova: string;
  status: "OK" | "FALHA" | "NAO VERIFICADO";
};

async function checarCacaRecente(sb: any): Promise<Check> {
  const promessa = "HUNTER roda todo dia 06:30 BRT — a ultima caca fechada tem menos de " + CACA_MAX_HORAS + "h";
  try {
    const h = await lastFinishedHunt(sb);
    if (!h) return { nome: "HUNTER rodou nas ultimas 24h", promessa, prova: "nenhuma caca com status done/partial no banco", status: "FALHA" };
    const horas = (Date.now() - new Date(h.finished_at).getTime()) / 3600000;
    const detalhe = "caca #" + h.id + " status=" + h.status + " fechada ha " + horas.toFixed(1) + "h (" + h.finished_at + ")";
    return { nome: "HUNTER rodou nas ultimas 24h", promessa, prova: detalhe, status: horas < CACA_MAX_HORAS ? "OK" : "FALHA" };
  } catch (e) {
    return { nome: "HUNTER rodou nas ultimas 24h", promessa, prova: "query falhou: " + String(e).slice(0, 120), status: "NAO VERIFICADO" };
  }
}

async function checarRls(): Promise<Check> {
  const promessa = "migration 20260726_hunter_x1_init declara: anon NEGADO nas 6 tabelas hunter_*";
  const anonKey = (process.env.SUPABASE_ANON_KEY ?? "").trim();
  if (!anonKey) {
    return {
      nome: "RLS das tabelas hunter_* nega anonimo",
      promessa,
      prova: "SUPABASE_ANON_KEY ausente — query anonima real nao foi executada",
      status: "NAO VERIFICADO",
    };
  }
  try {
    const r = await anonReadsHunterTables(config.supabaseUrl(), anonKey);
    return { nome: "RLS das tabelas hunter_* nega anonimo", promessa, prova: r.detail, status: r.leak ? "FALHA" : "OK" };
  } catch (e) {
    return { nome: "RLS das tabelas hunter_* nega anonimo", promessa, prova: "query anonima falhou: " + String(e).slice(0, 120), status: "NAO VERIFICADO" };
  }
}

async function checarQuarentena(sb: any): Promise<Check> {
  const promessa = "Lei 8: a quarentena e transitoria — a caca seguinte a esvazia. Teto: " + QUARENTENA_TETO + " itens nao processados";
  try {
    const n = await quarantineDepth(sb);
    return {
      nome: "quarentena nao cresce sem limite",
      promessa,
      prova: n + " item(ns) em hunter_raw_queue com processed=false (teto " + QUARENTENA_TETO + ")",
      status: n <= QUARENTENA_TETO ? "OK" : "FALHA",
    };
  } catch (e) {
    return { nome: "quarentena nao cresce sem limite", promessa, prova: "query falhou: " + String(e).slice(0, 120), status: "NAO VERIFICADO" };
  }
}

async function main() {
  const sb = db();
  const checks: Check[] = [await checarCacaRecente(sb), await checarRls(), await checarQuarentena(sb)];

  const L: string[] = [];
  L.push("=== RONDA · CHECAGENS DO HUNTER X.1 ===");
  L.push("(Lei da Contra-Prova: promessa do canon x prova do mundo vivo)");
  L.push("");
  for (const c of checks) {
    L.push("[" + c.status + "] " + c.nome);
    L.push("   promessa: " + c.promessa);
    L.push("   prova...: " + c.prova);
    L.push("");
  }
  const falhas = checks.filter((c) => c.status === "FALHA");
  const naoVer = checks.filter((c) => c.status === "NAO VERIFICADO");
  const cega = naoVer.length === checks.length;
  L.push("RESULTADO: " + checks.filter((c) => c.status === "OK").length + " OK · " + falhas.length + " FALHA · " + naoVer.length + " NAO VERIFICADO");
  // NAO VERIFICADO nao e OK (Lei 7). Se a Ronda nao conseguiu provar NADA,
  // ela esta cega — e uma ronda cega nao pode passar por verde.
  if (cega) L.push("ATENCAO: a Ronda nao provou nada — checagens cegas contam como falha.");
  else if (naoVer.length) L.push("ATENCAO: " + naoVer.length + " checagem(ns) sem prova — nao confundir com OK.");
  const saida = L.join(NL);
  console.log(saida);

  // Detecta -> relata. A Ronda nunca corrige sozinha.
  const alarme = falhas.length > 0 || cega;
  if (alarme && (process.env.RONDA_OPEN_ISSUE ?? "").toLowerCase() === "true") {
    await createIssue(
      "[RONDA] HUNTER fora do canon: " + (falhas.length ? falhas.map((f) => f.nome).join(" · ") : "Ronda cega (nada pode ser provado)"),
      ["## 🛰️ A Ronda encontrou divergencia entre o canon e o mundo vivo", "", "```", saida, "```", "", "_Read-only por lei: a Ronda detecta e relata. A correcao vai por branch + PR + merge do fundador._"].join(NL)
    );
  }
  process.exit(alarme ? 1 : 0);
}

main();
