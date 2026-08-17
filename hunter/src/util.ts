export const NL = String.fromCharCode(10);

export async function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

// Teto de espera por tentativa. Um Retry-After honesto de provedor cabe aqui;
// um valor absurdo (ou hostil) nao trava a caca por horas.
const MAX_BACKOFF_MS = 60_000;

// Le Retry-After (segundos ou data HTTP). Retorna null quando ausente/invalido.
function retryAfterMs(res: Response): number | null {
  const raw = res.headers.get("retry-after");
  if (!raw) return null;
  const secs = Number(raw);
  if (Number.isFinite(secs) && secs >= 0) return Math.min(secs * 1000, MAX_BACKOFF_MS);
  const at = Date.parse(raw);
  if (Number.isFinite(at)) return Math.min(Math.max(at - Date.now(), 0), MAX_BACKOFF_MS);
  return null;
}

// Le o corpo sem nunca derrubar o diagnostico: se falhar, devolve string vazia.
async function bodyPeek(res: Response): Promise<string> {
  try {
    return (await res.text()).slice(0, 500);
  } catch {
    return "";
  }
}

export async function fetchRetry(url: string, init: RequestInit = {}, attempts = 5): Promise<Response> {
  let lastErr: unknown;
  for (let i = 0; i < attempts; i++) {
    let waitMs = Math.min(1000 * Math.pow(2, i), MAX_BACKOFF_MS);
    try {
      const res = await fetch(url, init);
      if (res.status >= 500 || res.status === 429) {
        // O CORPO E A PROVA. A versao anterior lancava so "HTTP 429" e jogava
        // fora a mensagem do provedor — que e o unico texto capaz de separar
        // cota esgotada de limite por minuto. 17 dias de caca vazia passaram
        // sem diagnostico por causa disso. Nunca mais descartar o corpo.
        const body = await bodyPeek(res);
        const hinted = retryAfterMs(res);
        if (hinted !== null) waitMs = hinted;
        throw new Error("HTTP " + res.status + (body ? ": " + body : "") + (hinted !== null ? " [retry-after " + hinted + "ms]" : ""));
      }
      return res;
    } catch (e) {
      lastErr = e;
      if (i < attempts - 1) await sleep(waitMs);
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
