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
import { db, lastFinishedHunt, quarantineDepth, anonReadsHunterTables, createIssue, recentHunts, streakVazio } from "./db.js";
import { config } from "./config.js";
import { NL } from "./util.js";

// `??` so cai no default para undefined/null. Actions injeta STRING VAZIA
// quando a variable nao existe (`${{ vars.X }}` sem X definido), e Number("")
// e 0 — o teto colapsava para zero e a Ronda daria FALHA no primeiro item que
// entrasse na quarentena. Provado no primeiro run real: "Teto: 0".
function tetoQuarentena(): number {
  const v = (process.env.HUNTER_QUARANTINE_MAX ?? "").trim();
  const n = v ? Number(v) : NaN;
  return Number.isFinite(n) && n > 0 ? n : 500;
}
const QUARENTENA_TETO = tetoQuarentena();
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

// ANTI-CEGUEIRA (licao da 1a Curadoria Mensal, 17/08/2026).
// checarCacaRecente pergunta "a caca rodou?" — e por 17 dias a resposta foi
// SIM enquanto a colheita era ZERO: a triagem caia com HTTP 429, o codigo
// engolia, fechava a caca como `partial`, saia com exit 0 e ainda abria o PR
// diario. Verde em todo lugar, nada no banco.
// Esta checagem pergunta a outra metade: "a caca TROUXE alguma coisa?".
// Custo zero e a prova de que a analise nem chegou a rodar — uma caca que
// pensou custa dinheiro. Falha ja no DIA 1, nao no decimo setimo.
async function checarColheita(sb: any): Promise<Check> {
  const promessa = "toda caca fechada traz colheita — items_kept > 0, ou custo > 0 provando que a analise rodou";
  try {
    const hunts = await recentHunts(sb, 7);
    if (!hunts.length) return { nome: "HUNTER trouxe colheita", promessa, prova: "nenhuma caca fechada no banco", status: "FALHA" };
    const ultima = hunts[0];
    const vazia = ultima.items_kept === 0 && ultima.cost_usd === 0;
    const streak = streakVazio(hunts);
    const detalhe =
      "caca #" + ultima.id + " status=" + ultima.status + " items_kept=" + ultima.items_kept + " items_queued=" + ultima.items_queued + " custo=US$ " + ultima.cost_usd.toFixed(4) + (streak > 1 ? " · " + streak + " cacas vazias seguidas" : "");
    return { nome: "HUNTER trouxe colheita", promessa, prova: detalhe, status: vazia ? "FALHA" : "OK" };
  } catch (e) {
    return { nome: "HUNTER trouxe colheita", promessa, prova: "query falhou: " + String(e).slice(0, 120), status: "NAO VERIFICADO" };
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
  const checks: Check[] = [await checarCacaRecente(sb), await checarColheita(sb), await checarRls(), await checarQuarentena(sb)];

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
