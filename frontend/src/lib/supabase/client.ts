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

export function createClient(): SupabaseClient {
  // No server (SSR) sempre cria um cliente novo — não há window/lock.
  if (typeof window === 'undefined') {
    return createBrowserClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    );
  }

  if (browserClient) return browserClient;

  browserClient = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );

  return browserClient;
}
