export const NL = String.fromCharCode(10);

export async function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

export async function fetchRetry(url: string, init: RequestInit = {}, attempts = 3): Promise<Response> {
  let lastErr: unknown;
  for (let i = 0; i < attempts; i++) {
    try {
      const res = await fetch(url, init);
      if (res.status >= 500 || res.status === 429) throw new Error("HTTP " + res.status);
      return res;
    } catch (e) {
      lastErr = e;
      if (i < attempts - 1) await sleep(1000 * Math.pow(2, i));
    }
  }
  throw new Error("falha apos " + attempts + " tentativas: " + String(lastErr));
}

export function since24h(): Date {
  return new Date(Date.now() - 24 * 3600 * 1000);
}

export function todayUTC(): string {
  return new Date().toISOString().slice(0, 10);
}

export function collapse(s: string): string {
  return s.split(NL).join(" ").split(String.fromCharCode(9)).join(" ").trim();
}
