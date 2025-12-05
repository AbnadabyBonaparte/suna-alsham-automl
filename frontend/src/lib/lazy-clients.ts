/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - LAZY CLIENT INITIALIZATION
 * ═══════════════════════════════════════════════════════════════
 * 🔒 Evita erros de build ao não inicializar clients no top-level
 * ═══════════════════════════════════════════════════════════════
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';

// Cached instances
let supabaseInstance: SupabaseClient | null = null;
let anthropicInstance: any = null;
let octokitInstance: any = null;

/**
 * Get Supabase client (lazy initialization)
 */
export function getSupabase(): SupabaseClient {
  if (!supabaseInstance) {
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const key = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    
    if (!url || !key) {
      throw new Error('Supabase configuration missing');
    }
    
    supabaseInstance = createClient(url, key);
  }
  return supabaseInstance;
}

/**
 * Get Anthropic client (lazy initialization)
 */
export async function getAnthropic(): Promise<any> {
  if (!anthropicInstance) {
    const apiKey = process.env.ANTHROPIC_API_KEY;
    
    if (!apiKey) {
      console.warn('ANTHROPIC_API_KEY not configured - Claude features disabled');
      return null;
    }
    
    const Anthropic = (await import('@anthropic-ai/sdk')).default;
    anthropicInstance = new Anthropic({ apiKey });
  }
  return anthropicInstance;
}

/**
 * Get Octokit client (lazy initialization)
 */
export async function getOctokit(): Promise<any> {
  if (!octokitInstance) {
    const token = process.env.GITHUB_TOKEN;
    
    if (!token) {
      console.warn('GITHUB_TOKEN not configured - GitHub features disabled');
      return null;
    }
    
    const { Octokit } = await import('@octokit/rest');
    octokitInstance = new Octokit({ auth: token });
  }
  return octokitInstance;
}

// GitHub config
export const GITHUB_CONFIG = {
  owner: process.env.GITHUB_OWNER || 'AbnadabyBonaparte',
  repo: process.env.GITHUB_REPO || 'suna-alsham-automl',
};

