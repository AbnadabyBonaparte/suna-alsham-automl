import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import { config } from "./config.js";

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

export async function createIssue(title: string, body: string) {
  const tok = config.ghToken();
  const repo = config.repo();
  if (!tok || !repo) {
    console.error("createIssue: sem GITHUB_TOKEN/REPOSITORY — pulando");
    return;
  }
  const res = await fetch("https://api.github.com/repos/" + repo + "/issues", {
    method: "POST",
    headers: { Authorization: "Bearer " + tok, Accept: "application/vnd.github+json", "User-Agent": "HunterX1" },
    body: JSON.stringify({ title, body, labels: ["hunter"] }),
  });
  if (!res.ok) console.error("createIssue HTTP " + res.status + ": " + (await res.text()));
}
