import { createClient, SupabaseClient } from '@supabase/supabase-js';

// Lazy initialization - só cria o cliente quando for realmente usado
let _supabase: SupabaseClient | null = null;

export function getSupabase(): SupabaseClient {
  if (_supabase) {
    return _supabase;
  }

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error('Missing Supabase environment variables');
  }

  _supabase = createClient(supabaseUrl, supabaseAnonKey);
  return _supabase;
}

// Export para retrocompatibilidade
// NOTA: Não use diretamente no escopo do módulo, use getSupabase() dentro de funções
export const supabase = {
  get client() {
    return getSupabase();
  }
};
