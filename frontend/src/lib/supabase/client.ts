import { createBrowserClient } from '@supabase/ssr';
import type { SupabaseClient } from '@supabase/supabase-js';

/**
 * Singleton do cliente Supabase no browser.
 *
 * IMPORTANTE: precisa ser UMA única instância por aba. Criar vários
 * `createBrowserClient` gera múltiplos GoTrueClient disputando o mesmo
 * Web Lock (`sb-<ref>-auth-token`) — isso trava o `signInWithPassword`
 * para sempre (a tela de login fica presa em "SCANNING...").
 */
let browserClient: SupabaseClient | null = null;

// Build-safe fallbacks: `createBrowserClient` throws immediately when URL/key
// are absent, which crashes `next build` prerender (CI/preview have no env).
// Production always sets the real values; these placeholders only exist so the
// module can be constructed at build time — the client is re-created in the
// browser with the real env at runtime.
const SUPABASE_URL =
  process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co';
const SUPABASE_ANON_KEY =
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-anon-key';

export function createClient(): SupabaseClient {
  // No server (SSR) sempre cria um cliente novo — não há window/lock.
  if (typeof window === 'undefined') {
    return createBrowserClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  }

  if (browserClient) return browserClient;

  browserClient = createBrowserClient(SUPABASE_URL, SUPABASE_ANON_KEY);

  return browserClient;
}
