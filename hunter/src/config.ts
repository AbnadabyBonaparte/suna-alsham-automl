function req(name: string): string {
  const v = process.env[name];
  if (!v || !v.trim()) throw new Error("Segredo/variavel ausente: " + name);
  return v.trim();
}
function opt(name: string, def = ""): string {
  return (process.env[name] ?? def).trim();
}
function num(name: string, def: number): number {
  const v = process.env[name];
  const n = v ? Number(v) : NaN;
  return Number.isFinite(n) ? n : def;
}

export const config = {
  supabaseUrl: () => req("SUPABASE_URL"),
  supabaseKey: () => req("SUPABASE_SERVICE_ROLE_KEY"),
  aiBaseUrl: () => {
    const u = req("HUNTER_AI_BASE_URL");
    return u.endsWith("/") ? u.slice(0, -1) : u;
  },
  aiKey: () => req("HUNTER_AI_API_KEY"),
  triageModel: () => req("HUNTER_TRIAGE_MODEL"),
  analysisModel: () => req("HUNTER_ANALYSIS_MODEL"),
  embedModel: () => req("HUNTER_EMBED_MODEL"),
  ghToken: () => opt("GITHUB_TOKEN") || opt("HUNTER_GH_TOKEN"),
  repo: () => opt("GITHUB_REPOSITORY"),
  simulateAnalysisFailure: () => opt("HUNTER_SIMULATE_ANALYSIS_FAILURE").toLowerCase() === "true",
  triageCap: () => num("HUNTER_TRIAGE_CAP", 300),
  finalistsCap: () => num("HUNTER_FINALISTS_CAP", 20),
  dedupThreshold: () => num("HUNTER_DEDUP_THRESHOLD", 0.92),
  perSourceLimit: () => num("HUNTER_PER_SOURCE_LIMIT", 60),
  embedDims: () => num("HUNTER_EMBED_DIMS", 1024),
  priceTriageIn: () => num("HUNTER_PRICE_TRIAGE_IN", 0),
  priceTriageOut: () => num("HUNTER_PRICE_TRIAGE_OUT", 0),
  priceAnalysisIn: () => num("HUNTER_PRICE_ANALYSIS_IN", 0),
  priceAnalysisOut: () => num("HUNTER_PRICE_ANALYSIS_OUT", 0),
  priceEmbed: () => num("HUNTER_PRICE_EMBED", 0),
};
