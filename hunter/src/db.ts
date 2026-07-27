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

export async function getPendingFindings(sb: SupabaseClient, currentHuntId: number): Promise<PendingFinding[]> {
  const { data, error } = await sb
    .from("hunter_findings")
    .select("id,hunt_id,kind,title,url,source,relevance,created_at")
    .eq("verdict", "pending")
    .neq("hunt_id", currentHuntId)
    .order("relevance", { ascending: false })
    .limit(200);
  if (error) throw new Error("getPendingFindings: " + error.message);
  return (data ?? []) as PendingFinding[];
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
export async function existingHunterIssueTitles(): Promise<Set<string>> {
  const tok = config.ghToken();
  const repo = config.repo();
  const titles = new Set<string>();
  if (!tok || !repo) return titles;
  for (let page = 1; page <= 5; page++) {
    const res = await fetch(
      "https://api.github.com/repos/" + repo + "/issues?labels=hunter&state=all&per_page=100&page=" + page,
      { headers: { Authorization: "Bearer " + tok, Accept: "application/vnd.github+json", "User-Agent": "HunterX1" } }
    );
    if (!res.ok) {
      console.error("existingHunterIssueTitles HTTP " + res.status);
      break;
    }
    const arr = (await res.json()) as any[];
    for (const i of arr) if (i?.title) titles.add(String(i.title));
    if (arr.length < 100) break;
  }
  return titles;
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
