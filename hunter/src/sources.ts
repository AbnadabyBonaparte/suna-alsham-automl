import { XMLParser } from "fast-xml-parser";
import type { RawItem } from "./types.js";
import { config } from "./config.js";
import { fetchRetry, since24h, collapse } from "./util.js";

const UA = "HunterX1/1.0 (+https://github.com/AbnadabyBonaparte/suna-alsham-automl)";

export type SourceResult = { source: string; ok: boolean; items: RawItem[]; error?: string };

export async function collectAll(): Promise<SourceResult[]> {
  const runners = [arxiv, github, hackernews];
  const out: SourceResult[] = [];
  for (const r of runners) {
    try {
      out.push(await r());
    } catch (e) {
      out.push({ source: r.name, ok: false, items: [], error: String(e) });
    }
  }
  return out;
}

async function arxiv(): Promise<SourceResult> {
  const q = encodeURIComponent("cat:cs.AI OR cat:cs.CL OR cat:cs.MA");
  const url =
    "http://export.arxiv.org/api/query?search_query=" +
    q +
    "&sortBy=submittedDate&sortOrder=descending&max_results=" +
    config.perSourceLimit();
  const res = await fetchRetry(url, { headers: { "User-Agent": UA } });
  const xml = await res.text();
  const parser = new XMLParser();
  const feed = parser.parse(xml)?.feed;
  const raw = feed?.entry ? (Array.isArray(feed.entry) ? feed.entry : [feed.entry]) : [];
  const cutoff = since24h();
  const items: RawItem[] = [];
  for (const e of raw) {
    const published = new Date(e.published);
    if (published < cutoff) continue;
    items.push({
      source: "arxiv",
      url: String(e.id),
      title: collapse(String(e.title ?? "")),
      rawText: collapse(String(e.summary ?? "")),
    });
  }
  return { source: "arxiv", ok: true, items };
}

async function github(): Promise<SourceResult> {
  const d = since24h().toISOString().slice(0, 10);
  const query = "(agent OR \"ai agent\" OR llm OR mcp) created:>=" + d;
  const url =
    "https://api.github.com/search/repositories?q=" +
    encodeURIComponent(query) +
    "&sort=stars&order=desc&per_page=" +
    config.perSourceLimit();
  const headers: Record<string, string> = {
    "User-Agent": UA,
    Accept: "application/vnd.github+json",
  };
  const tok = config.ghToken();
  if (tok) headers["Authorization"] = "Bearer " + tok;
  const res = await fetchRetry(url, { headers });
  const json: any = await res.json();
  const items: RawItem[] = (json.items ?? []).map((r: any) => ({
    source: "github",
    url: r.html_url,
    title: r.full_name,
    rawText: collapse(
      (r.description ?? "") +
        " | estrelas:" +
        (r.stargazers_count ?? 0) +
        " | licenca:" +
        (r.license?.spdx_id ?? "?") +
        " | lang:" +
        (r.language ?? "?")
    ),
  }));
  return { source: "github", ok: true, items };
}

async function hackernews(): Promise<SourceResult> {
  const ts = Math.floor(since24h().getTime() / 1000);
  const url =
    "https://hn.algolia.com/api/v1/search_by_date?tags=story&query=" +
    encodeURIComponent("AI agent") +
    "&numericFilters=created_at_i>" +
    ts +
    "&hitsPerPage=" +
    config.perSourceLimit();
  const res = await fetchRetry(url, { headers: { "User-Agent": UA } });
  const json: any = await res.json();
  const items: RawItem[] = (json.hits ?? []).map((h: any) => ({
    source: "hacker-news",
    url: h.url || "https://news.ycombinator.com/item?id=" + h.objectID,
    title: h.title ?? "(sem titulo)",
    rawText: collapse((h.title ?? "") + " " + (h.story_text ?? "") + " | " + (h.points ?? 0) + " pts"),
  }));
  return { source: "hacker-news", ok: true, items };
}
