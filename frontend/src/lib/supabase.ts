import { createClient } from '@supabase/supabase-js';

// Tenta pegar as chaves do ambiente
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

// Se não tiver chaves (ainda não configuradas na Vercel), cria um cliente nulo para não quebrar o build
export const supabase = (supabaseUrl && supabaseAnonKey) 
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;