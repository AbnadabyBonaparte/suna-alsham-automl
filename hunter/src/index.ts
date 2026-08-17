import {
  db,
  getActiveMission,
  createHunt,
  closeHunt,
  getQuarantine,
  enqueueRaw,
  markProcessed,
  matchFinding,
  insertFinding,
  insertEdges,
  insertSoul,
  createIssue,
  getPendingFindings,
  existingHunterIssueTitles,
  openThreatIssue,
  THREAT_RELEVANCE_MIN,
} from "./db.js";
import { collectAll } from "./sources.js";
import { triageBatch, analyze, embed, cost } from "./ai.js";
import { writeReport, type ReportItem, type PendingItem } from "./report.js";
import { config } from "./config.js";
import { todayUTC, NL } from "./util.js";
import type { RawItem } from "./types.js";

// FASE 3 · peca 2: a fila pendente nunca derruba a caca — se a query falhar,
// o relatorio sai com a secao vazia e a falha vira NAO VERIFICADO (Lei 7).
async function pendentes(sb: any, huntId: number, failNotes: string[]): Promise<{ items: PendingItem[]; total: number }> {
  try {
    return await getPendingFindings(sb, huntId);
  } catch (e) {
    console.error("[hunter] fila pendente falhou:", String(e));
    failNotes.push("fila pendente NAO VERIFICADA (" + String(e).slice(0, 80) + ")");
    return { items: [], total: 0 };
  }
}

async function pendentesFin(sb: any, huntId: number, failNotes: string[]) {
  const p = await pendentes(sb, huntId, failNotes);
  return { pending: p.items, pendingTotal: p.total };
}

type Fin = {
  date: string;
  itemsSeen: number;
  itemsKept: number;
  itemsQueued: number;
  sourcesOk: number;
  sourcesFail: number;
  failNotes: string[];
  status: string;
  findings: ReportItem[];
  pending: PendingItem[];
  pendingTotal: number;
};

async function finalize(sb: any, huntId: number, r: Fin) {
  const costUsd = cost.usd();
  const gold = r.findings.slice().sort((a, b) => b.relevance - a.relevance)[0];
  const reportPath = writeReport({
    date: r.date,
    itemsSeen: r.itemsSeen,
    itemsKept: r.itemsKept,
    itemsQueued: r.itemsQueued,
    sourcesOk: r.sourcesOk,
    sourcesFail: r.sourcesFail,
    failNotes: r.failNotes,
    status: r.status,
    findings: r.findings,
    pending: r.pending,
    pendingTotal: r.pendingTotal,
    costUsd,
    costNote: cost.tokensNote(),
    gold: gold ? "[" + gold.relevance + "] " + gold.title : "",
  });
  await closeHunt(sb, huntId, {
    status: r.status,
    sources_ok: r.sourcesOk,
    sources_fail: r.sourcesFail,
    items_seen: r.itemsSeen,
    items_kept: r.itemsKept,
    items_queued: r.itemsQueued,
    cost_usd: Number(costUsd.toFixed(4)),
    report_path: reportPath,
    notes: r.failNotes.join(" · ") || null,
  });
  console.log("Caca " + r.date + " status=" + r.status + " vistos=" + r.itemsSeen + " trazidos=" + r.itemsKept + " quarentena=" + r.itemsQueued + " custo=US$" + costUsd.toFixed(4));
}

async function main() {
  const date = todayUTC();
  const sb = db();

  const mission = await getActiveMission(sb);
  if (!mission) {
    await createIssue(
      "🔴 HUNTER: sem missao ativa — caca abortada",
      "A caca de " + date + " nao encontrou missao active em hunter_missions. O cacador nunca improvisa mandato (Lei 7). Ative a missao e redispare."
    );
    console.error("Sem missao ativa. Abortado.");
    process.exit(1);
  }
  if (mission.scoring_rules) process.env.HUNTER_SCORING_HINT = JSON.stringify(mission.scoring_rules).slice(0, 1500);

  const huntId = await createHunt(sb, mission.id);
  const failNotes: string[] = [];

  // FASE 3 · peca 3: titulos de issues 'hunter' ja abertas, para nao duplicar.
  let issuesConhecidas = new Set<string>();
  try {
    const r = await existingHunterIssueTitles();
    issuesConhecidas = r.titles;
    // Listagem incompleta = pode existir issue que nao vimos. Nao silencia:
    // se uma ameaca duplicar, o relatorio ja avisa por que.
    if (!r.completa) failNotes.push("listagem de issues INCOMPLETA (" + issuesConhecidas.size + " vistas) — ameaça pode duplicar");
  } catch (e) {
    console.error("[hunter] listagem de issues falhou:", String(e));
    failNotes.push("listagem de issues NAO VERIFICADA");
  }

  try {
    const quarantine = await getQuarantine(sb);
    const quarantineItems: RawItem[] = quarantine.map((q: any) => ({
      source: q.source,
      url: q.url,
      title: q.raw_payload?.title ?? q.url,
      rawText: q.raw_payload?.rawText ?? "",
    }));
    const quarantineIds: number[] = quarantine.map((q: any) => q.id);

    const results = await collectAll();
    let sourcesOk = 0;
    let sourcesFail = 0;
    const fresh: RawItem[] = [];
    for (const r of results) {
      if (r.ok) {
        sourcesOk++;
        fresh.push(...r.items);
      } else {
        sourcesFail++;
        failNotes.push(r.source + " (" + (r.error ?? "falha") + ")");
      }
    }

    const all = [...quarantineItems, ...fresh];
    const itemsSeen = all.length;

    const cap = config.triageCap();
    const toTriage = all.slice(0, cap);
    const overflow = all.slice(cap);
    let itemsQueued = 0;
    for (const it of overflow) {
      await enqueueRaw(sb, huntId, it.source, it.url, it, "rate");
      itemsQueued++;
    }

    const triage: { idx: number; verdict: string; score: number; has_personal_data: boolean }[] = [];
    try {
      for (let i = 0; i < toTriage.length; i += 25) {
        const batch = toTriage.slice(i, i + 25);
        const res = await triageBatch(batch);
        for (const t of res) triage.push({ idx: t.idx + i, verdict: t.verdict, score: t.score, has_personal_data: t.has_personal_data });
      }
    } catch (e) {
      for (const it of toTriage) {
        await enqueueRaw(sb, huntId, it.source, it.url, it, "llm_down");
        itemsQueued++;
      }
      failNotes.push("triagem caiu: " + String(e));
      console.error("[hunter] triagem caiu:", String(e));
      await markProcessed(sb, quarantineIds);
      await finalize(sb, huntId, { date, itemsSeen, itemsKept: 0, itemsQueued, sourcesOk, sourcesFail, failNotes, status: "partial", findings: [], ...(await pendentesFin(sb, huntId, failNotes)) });
      return;
    }

    const kept = triage.filter((t) => t.verdict !== "lixo" && !t.has_personal_data).sort((a, b) => b.score - a.score);
    const finalists = kept.slice(0, config.finalistsCap());

    const reportItems: ReportItem[] = [];
    let analysisFailed = false;
    let itemsKept = 0;
    for (const t of finalists) {
      const it = toTriage[t.idx];
      if (!it) continue;
      try {
        if (config.simulateAnalysisFailure()) throw new Error("SIMULACAO: falha de analise provocada (teste Lei 8)");
        const vec = await embed(it.title + NL + it.rawText);
        if (await matchFinding(sb, vec, config.dedupThreshold())) continue;
        const a = await analyze(it);
        // insertFinding e a FRONTEIRA de sucesso: se gravou, o achado conta.
        const fid = await insertFinding(sb, {
          hunt_id: huntId,
          kind: a.kind,
          title: it.title,
          url: it.url,
          source: it.source,
          summary_md: a.summary_md,
          relevance: a.relevance,
          relevance_why: a.relevance_why,
          single_source: a.single_source,
          license: a.license ?? null,
          embedding: JSON.stringify(vec),
        });
        itemsKept++;
        reportItems.push({
          relevance: a.relevance,
          kind: a.kind,
          title: it.title,
          source: it.source,
          url: it.url,
          summary_md: a.summary_md,
          single_source: a.single_source,
          license: a.license ?? null,
        });
        // FASE 3 · peca 3 — AMEACA ABRE ISSUE NA MESMA CACA, sem esperar o
        // relatorio. Best-effort: falha aqui nao derruba o achado ja salvo.
        if (a.kind === "threat" && a.relevance >= THREAT_RELEVANCE_MIN) {
          try {
            const r = await openThreatIssue(issuesConhecidas, {
              title: it.title,
              url: it.url,
              source: it.source,
              relevance: a.relevance,
              relevance_why: a.relevance_why,
              summary_md: a.summary_md,
            });
            console.log("[hunter] ameaca rel=" + a.relevance + " · " + r.reason + (r.issueUrl ? " · " + r.issueUrl : "") + " · " + it.title);
          } catch (te) {
            console.error("[hunter] issue de ameaca falhou:", it.url, String(te));
            failNotes.push("issue de ameaca NAO ABERTA para: " + it.title.slice(0, 60));
          }
        }

        // Arestas e alma sao BEST-EFFORT: sua falha nao derruba o achado ja salvo.
        try {
          await insertEdges(sb, fid, a.edges);
          if (a.kind === "soul" && a.soul) await insertSoul(sb, fid, a.soul);
        } catch (ee) {
          console.error("[hunter] arestas/alma falharam (finding salvo):", it.url, String(ee));
        }
      } catch (e) {
        console.error("[hunter] finding falhou:", it.url, String(e));
        await enqueueRaw(sb, huntId, it.source, it.url, it, "llm_down");
        itemsQueued++;
        analysisFailed = true;
      }
    }

    await markProcessed(sb, quarantineIds);
    await finalize(sb, huntId, {
      date,
      itemsSeen,
      itemsKept,
      itemsQueued,
      sourcesOk,
      sourcesFail,
      failNotes,
      status: analysisFailed ? "partial" : "done",
      findings: reportItems,
      ...(await pendentesFin(sb, huntId, failNotes)),
    });
  } catch (e) {
    await closeHunt(sb, huntId, { status: "failed", notes: String(e), cost_usd: Number(cost.usd().toFixed(4)) });
    console.error("Caca falhou:", e);
    process.exit(1);
  }
}

main();
