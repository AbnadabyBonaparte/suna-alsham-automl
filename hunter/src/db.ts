import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import { config } from "./config.js";
import { NL } from "./util.js";

export function db(): SupabaseClient {
  return createClient(config.supabaseUrl(), config.supabaseKey(), { auth: { persistSession: false } });
}

export async function getActiveMission(sb: SupabaseClient) {
  const { data, error } = await sb
    .from("hunter_missions")
    .select("*")
    .eq("status", "active")
    .order("version", { ascending: false })
    .limit(1);
  if (error) throw new Error("getActiveMission: " + error.message);
  return data?.[0] ?? null;
}

export async function createHunt(sb: SupabaseClient, missionId: number): Promise<number> {
  const { data, error } = await sb.from("hunter_hunts").insert({ mission_id: missionId, status: "running" }).select("id").single();
  if (error) throw new Error("createHunt: " + error.message);
  return data.id as number;
}

export async function closeHunt(sb: SupabaseClient, id: number, patch: Record<string, unknown>) {
  const { error } = await sb.from("hunter_hunts").update({ ...patch, finished_at: new Date().toISOString() }).eq("id", id);
  if (error) throw new Error("closeHunt: " + error.message);
}

export async function getQuarantine(sb: SupabaseClient) {
  const { data, error } = await sb.from("hunter_raw_queue").select("*").eq("processed", false).limit(500);
  if (error) throw new Error("getQuarantine: " + error.message);
  return data ?? [];
}

export async function enqueueRaw(sb: SupabaseClient, huntId: number, source: string, url: string, payload: unknown, reason: string) {
  const { error } = await sb.from("hunter_raw_queue").insert({ hunt_id: huntId, source, url, raw_payload: payload, queued_reason: reason });
  if (error) throw new Error("enqueueRaw: " + error.message);
}

export async function markProcessed(sb: SupabaseClient, ids: number[]) {
  if (!ids.length) return;
  const { error } = await sb.from("hunter_raw_queue").update({ processed: true }).in("id", ids);
  if (error) throw new Error("markProcessed: " + error.message);
}

export async function matchFinding(sb: SupabaseClient, embedding: number[], threshold: number): Promise<boolean> {
  const { data, error } = await sb.rpc("hunter_match_finding", { query_embedding: JSON.stringify(embedding), match_threshold: threshold });
  if (error) throw new Error("matchFinding: " + error.message);
  return Array.isArray(data) && data.length > 0;
}

export async function insertFinding(sb: SupabaseClient, row: Record<string, unknown>): Promise<number> {
  const { data, error } = await sb.from("hunter_findings").insert(row).select("id").single();
  if (error) throw new Error("insertFinding: " + error.message);
  return data.id as number;
}

export async function insertEdges(sb: SupabaseClient, findingId: number, edges: any[]) {
  if (!edges.length) return;
  const rows = edges.map((e) => ({ finding_id: findingId, subject: e.subject, relation: e.relation, object: e.object, confidence: e.confidence }));
  const { error } = await sb.from("hunter_edges").insert(rows);
  if (error) throw new Error("insertEdges: " + error.message);
}

export async function insertSoul(sb: SupabaseClient, findingId: number, soul: any) {
  const { error } = await sb.from("souls_catalog").insert({ finding_id: findingId, name: soul.name, origin: soul.origin, capsule_draft: soul.capsule_draft ?? null, status: "candidate" });
  if (error) throw new Error("insertSoul: " + error.message);
}

// ── FASE 3 · peca 2 — RESSURGIR OS PENDENTES ────────────────────────────────
// Todo achado de caca ANTERIOR que ainda nao recebeu veredito. Sem isto, o
// pending de ontem some do relatorio de hoje e nunca chega ao tribunal.
export type PendingFinding = {
  id: number;
  hunt_id: number | null;
  kind: string;
  title: string;
  url: string;
  source: string;
  relevance: number;
  created_at: string;
};

export const PENDING_PAGE = 500;

// Devolve os pendentes E o total real. Sem o total, um teto silencioso
// reintroduziria o proprio bug que esta secao existe para matar: achado some
// da fila e ninguem percebe. Se truncar, o relatorio DIZ que truncou (Lei 7).
export async function getPendingFindings(
  sb: SupabaseClient,
  currentHuntId: number
): Promise<{ items: PendingFinding[]; total: number }> {
  const { data, error, count } = await sb
    .from("hunter_findings")
    .select("id,hunt_id,kind,title,url,source,relevance,created_at", { count: "exact" })
    // hunt_id NULL nao e "a caca atual": em SQL, NULL <> x da NULL e a linha
    // sumiria. Achado inserido a mao com hunt_id vazio tem de aparecer.
    .or("hunt_id.neq." + currentHuntId + ",hunt_id.is.null")
    .eq("verdict", "pending")
    .order("relevance", { ascending: false })
    .limit(PENDING_PAGE);
  if (error) throw new Error("getPendingFindings: " + error.message);
  const items = (data ?? []) as PendingFinding[];
  return { items, total: count ?? items.length };
}

// ── FASE 3 · peca 4 — CHECAGENS DA RONDA ────────────────────────────────────
export async function lastFinishedHunt(sb: SupabaseClient) {
  const { data, error } = await sb
    .from("hunter_hunts")
    .select("id,status,started_at,finished_at")
    .in("status", ["done", "partial"])
    .not("finished_at", "is", null)
    .order("finished_at", { ascending: false })
    .limit(1);
  if (error) throw new Error("lastFinishedHunt: " + error.message);
  return data?.[0] ?? null;
}

// A COLHEITA, nao a porta. lastFinishedHunt responde "rodou?"; esta responde
// "trouxe alguma coisa?". Sao perguntas diferentes: 17 cacas seguidas rodaram
// (status partial, exit 0, PR aberto) e nao trouxeram nada — e todo vigia
// passou verde porque so perguntava a primeira.
export type HuntYield = {
  id: number;
  status: string;
  finished_at: string;
  items_kept: number;
  items_queued: number;
  cost_usd: number;
};

export async function recentHunts(sb: SupabaseClient, limit = 7): Promise<HuntYield[]> {
  const { data, error } = await sb
    .from("hunter_hunts")
    .select("id,status,finished_at,items_kept,items_queued,cost_usd")
    .in("status", ["done", "partial"])
    .not("finished_at", "is", null)
    .order("finished_at", { ascending: false })
    .limit(limit);
  if (error) throw new Error("recentHunts: " + error.message);
  return (data ?? []).map((h) => ({
    id: Number(h.id),
    status: String(h.status),
    finished_at: String(h.finished_at),
    items_kept: Number(h.items_kept ?? 0),
    items_queued: Number(h.items_queued ?? 0),
    cost_usd: Number(h.cost_usd ?? 0),
  }));
}

// Quantas cacas fechadas seguidas, a partir da mais recente, vieram vazias.
// Vazia = nada mantido E custo zero (o custo zero prova que a analise nem rodou).
export function streakVazio(hunts: HuntYield[]): number {
  let n = 0;
  for (const h of hunts) {
    if (h.items_kept === 0 && h.cost_usd === 0) n++;
    else break;
  }
  return n;
}

export async function quarantineDepth(sb: SupabaseClient): Promise<number> {
  const { count, error } = await sb
    .from("hunter_raw_queue")
    .select("id", { count: "exact", head: true })
    .eq("processed", false);
  if (error) throw new Error("quarantineDepth: " + error.message);
  return count ?? 0;
}

// Query ANONIMA real contra a memoria dos irmaos. Prova, nao promessa:
// se voltar linha, a RLS falhou. Erro ou vazio = negado corretamente.
export async function anonReadsHunterTables(url: string, anonKey: string): Promise<{ leak: boolean; detail: string }> {
  const anon = createClient(url, anonKey, { auth: { persistSession: false } });
  const tabelas = ["hunter_findings", "hunter_hunts", "hunter_missions", "hunter_raw_queue", "hunter_edges", "souls_catalog"];
  const vazados: string[] = [];
  const negados: string[] = [];
  for (const tb of tabelas) {
    const { data, error } = await anon.from(tb).select("id").limit(1);
    if (error) negados.push(tb + " (erro: " + error.message.slice(0, 40) + ")");
    else if (Array.isArray(data) && data.length > 0) vazados.push(tb + " (" + data.length + " linha)");
    else negados.push(tb + " (vazio)");
  }
  return { leak: vazados.length > 0, detail: vazados.length ? "VAZOU: " + vazados.join(", ") : "negado em " + negados.length + "/" + tabelas.length };
}

// ── Issues ──────────────────────────────────────────────────────────────────
// Titulos ja existentes com label 'hunter' (open+closed). Usa a API de listagem,
// nao a de busca: listagem e imediata, busca tem atraso de indexacao e
// deixaria passar duplicata na mesma caca.
export async function existingHunterIssueTitles(): Promise<{ titles: Set<string>; completa: boolean }> {
  const tok = config.ghToken();
  const repo = config.repo();
  const titles = new Set<string>();
  if (!tok || !repo) return { titles, completa: false };
  const MAX_PAGINAS = 10;
  let completa = false;
  for (let page = 1; page <= MAX_PAGINAS; page++) {
    const res = await fetch(
      "https://api.github.com/repos/" + repo + "/issues?labels=hunter&state=all&per_page=100&page=" + page,
      { headers: { Authorization: "Bearer " + tok, Accept: "application/vnd.github+json", "User-Agent": "HunterX1" } }
    );
    if (!res.ok) {
      console.error("existingHunterIssueTitles HTTP " + res.status);
      return { titles, completa: false };
    }
    const arr = (await res.json()) as any[];
    for (const i of arr) if (i?.title) titles.add(String(i.title));
    // So e completa se a ultima pagina veio curta. Estourar o teto de paginas
    // significa que existem issues que nao vimos — e dai poderiamos reabrir
    // uma ameaca ja aberta. Melhor declarar do que fingir que viu tudo.
    if (arr.length < 100) {
      completa = true;
      break;
    }
  }
  return { titles, completa };
}

export async function createIssue(title: string, body: string): Promise<string | null> {
  const tok = config.ghToken();
  const repo = config.repo();
  if (!tok || !repo) {
    console.error("createIssue: sem GITHUB_TOKEN/REPOSITORY — pulando");
    return null;
  }
  const res = await fetch("https://api.github.com/repos/" + repo + "/issues", {
    method: "POST",
    headers: { Authorization: "Bearer " + tok, Accept: "application/vnd.github+json", "User-Agent": "HunterX1" },
    body: JSON.stringify({ title, body, labels: ["hunter"] }),
  });
  if (!res.ok) {
    console.error("createIssue HTTP " + res.status + ": " + (await res.text()));
    return null;
  }
  const j = (await res.json()) as any;
  return j?.html_url ?? null;
}

// ── FASE 3 · peca 3 — ISSUE DE AMEACA ───────────────────────────────────────
// kind='threat' e relevance>=90 abre issue NA MESMA CACA. Idempotente pelo
// titulo exato: se ja existe issue 'hunter' com esse titulo, nao reabre.
export const THREAT_RELEVANCE_MIN = 90;

export function threatIssueTitle(title: string): string {
  return "[HUNTER] Ameaça: " + title;
}

export async function openThreatIssue(
  seen: Set<string>,
  f: { title: string; url: string; source: string; relevance: number; relevance_why: string; summary_md: string }
): Promise<{ created: boolean; reason: string; issueUrl: string | null }> {
  const titulo = threatIssueTitle(f.title);
  if (seen.has(titulo)) return { created: false, reason: "issue ja existe", issueUrl: null };
  const corpo = [
    "## 🚨 Ameaça detectada pelo HUNTER X.1",
    "",
    "**Relevância:** " + f.relevance + "/100" + (f.relevance_why ? " — " + f.relevance_why : ""),
    "**Fonte:** " + f.source,
    "**URL:** " + f.url,
    "",
    "### Resumo",
    "",
    f.summary_md,
    "",
    "---",
    "_Aberta automaticamente na própria caça (não esperou o relatório). O veredito é do fundador._",
  ].join(NL);
  const issueUrl = await createIssue(titulo, corpo);
  seen.add(titulo);
  return { created: true, reason: "aberta", issueUrl };
}

// ============================================================================
// FASE 4 — O ESPELHO (autocritica semanal)
// ============================================================================
// O Espelho so LE, MEDE e PROPOE. Nunca ativa, nunca abre mina, nunca muda
// score. As travas abaixo sao de CODIGO, nao de disciplina: uma proposta
// ilegal lanca antes de tocar o banco.
// ============================================================================

export type FindingJulgado = {
  id: number;
  hunt_id: number | null;
  source: string;
  kind: string;
  title: string;
  relevance: number;
  single_source: boolean;
  verdict: string;
  created_at: string;
};

export async function getHuntsSince(sb: SupabaseClient, desdeISO: string) {
  const { data, error } = await sb
    .from("hunter_hunts")
    .select("id,status,started_at,finished_at,items_seen,items_kept,items_queued,sources_ok,sources_fail,cost_usd")
    .gte("started_at", desdeISO)
    .order("started_at", { ascending: true });
  if (error) throw new Error("getHuntsSince: " + error.message);
  return data ?? [];
}

export async function getFindingsSince(sb: SupabaseClient, desdeISO: string): Promise<FindingJulgado[]> {
  const { data, error } = await sb
    .from("hunter_findings")
    .select("id,hunt_id,source,kind,title,relevance,single_source,verdict,created_at")
    .gte("created_at", desdeISO)
    .order("created_at", { ascending: true })
    .limit(2000);
  if (error) throw new Error("getFindingsSince: " + error.message);
  return (data ?? []) as FindingJulgado[];
}

export async function getActiveMissionOrThrow(sb: SupabaseClient) {
  const m = await getActiveMission(sb);
  if (!m) throw new Error("sem missao active — o Espelho nao inventa mandato (Lei 7)");
  return m;
}

export async function maxMissionVersion(sb: SupabaseClient): Promise<number> {
  const { data, error } = await sb.from("hunter_missions").select("version").order("version", { ascending: false }).limit(1);
  if (error) throw new Error("maxMissionVersion: " + error.message);
  return (data?.[0]?.version as number) ?? 0;
}

// ── AS TRAVAS DE LEI ────────────────────────────────────────────────────────
export const ESPELHO_STATUS_UNICO = "proposed";
export const ESPELHO_AUTOR = "hunter-proposal";

export type PropostaMissao = {
  version: number;
  status: string;
  mission_md: string;
  sources: unknown;
  scoring_rules: unknown;
  created_by: string;
};

// Lanca ANTES de qualquer escrita. E a trava, nao um aviso.
export function assertPropostaLegal(p: PropostaMissao, sourcesAtivas: unknown, evidencias: number): void {
  if (p.status !== ESPELHO_STATUS_UNICO) {
    throw new Error("TRAVA DE LEI: o Espelho so grava status='" + ESPELHO_STATUS_UNICO + "'. Recebido: '" + p.status + "'. Ativar missao e ato do fundador.");
  }
  if (p.created_by !== ESPELHO_AUTOR) {
    throw new Error("TRAVA DE LEI: proposta do Espelho tem created_by='" + ESPELHO_AUTOR + "'. Recebido: '" + p.created_by + "'.");
  }
  const antes = JSON.stringify(sourcesAtivas ?? null);
  const depois = JSON.stringify(p.sources ?? null);
  if (antes !== depois) {
    throw new Error("TRAVA DE LEI: o Espelho nao abre nem fecha mina. `sources` tem de ser identico ao da missao ativa.");
  }
  if (!Number.isFinite(evidencias) || evidencias <= 0) {
    throw new Error("TRAVA DE LEI: proposta sem evidencia numerica e rejeitada (Lei 7). Vereditos contados: " + evidencias);
  }
}

export async function insertMissionProposal(
  sb: SupabaseClient,
  p: PropostaMissao,
  sourcesAtivas: unknown,
  evidencias: number
): Promise<number> {
  assertPropostaLegal(p, sourcesAtivas, evidencias);
  const { data, error } = await sb.from("hunter_missions").insert(p).select("id").single();
  if (error) throw new Error("insertMissionProposal: " + error.message);
  return data.id as number;
}
