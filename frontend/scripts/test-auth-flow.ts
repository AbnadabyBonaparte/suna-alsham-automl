import 'dotenv/config';
import { createClient } from '@supabase/supabase-js';

/**
 * Script de verificação isolada do fluxo de login no Supabase.
 * Uso:
 *   1) Copie .env.example -> .env.local e preencha NEXT_PUBLIC_SUPABASE_URL / NEXT_PUBLIC_SUPABASE_ANON_KEY.
 *   2) Defina a senha real via env TEST_SUPABASE_PASSWORD (ou edite a constante abaixo).
 *   3) Rode: npx tsx scripts/test-auth-flow.ts
 *      (ou npx ts-node scripts/test-auth-flow.ts se preferir)
 *
 * ⚠️ Não commitar senhas. O script aborta se a senha permanecer como placeholder.
 */

async function main() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  const email = process.env.TEST_SUPABASE_EMAIL || 'casamondestore@gmail.com';
  const password = process.env.TEST_SUPABASE_PASSWORD || 'SENHA_PLACEHOLDER';

  if (!supabaseUrl || !supabaseAnonKey) {
    console.error('[TEST][AUTH] Defina NEXT_PUBLIC_SUPABASE_URL e NEXT_PUBLIC_SUPABASE_ANON_KEY');
    process.exit(1);
  }

  if (!password || password === 'SENHA_PLACEHOLDER') {
    console.error('[TEST][AUTH] Defina TEST_SUPABASE_PASSWORD com a senha real antes de rodar');
    process.exit(1);
  }

  console.log('==============================================');
  console.log('[TEST][AUTH] Supabase URL:', supabaseUrl);
  console.log('[TEST][AUTH] Email alvo:', email);
  console.log('==============================================');

  const supabase = createClient(supabaseUrl, supabaseAnonKey);

  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  const session = data?.session;
  const sessionSummary = session
    ? {
        user_id: session.user?.id,
        expires_at: session.expires_at,
        access_token_prefix: session.access_token?.slice(0, 8),
        refresh_token_prefix: session.refresh_token?.slice(0, 8),
      }
    : null;

  console.log('[TEST][AUTH] Session summary (prefix only):', sessionSummary);
  console.log('[TEST][AUTH] Raw user object:', data?.user ?? null);

  if (error) {
    console.error('[TEST][AUTH] Error:', {
      message: error.message,
      status: error.status,
      name: error.name,
    });
    process.exitCode = 1;
  } else {
    console.log('[TEST][AUTH] Login OK (session tokens truncados por segurança).');
  }
}

main().catch((err) => {
  console.error('[TEST][AUTH] Unexpected failure:', err);
  process.exit(1);
});








