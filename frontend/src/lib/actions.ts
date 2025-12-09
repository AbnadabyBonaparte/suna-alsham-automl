'use server'

import { createClient } from '@/lib/supabase/server';

export async function toggleSystemMode(mode: 'TURBO' | 'SAFE' | 'STOP') {
  console.log(`[COMMAND] Switching system to: ${mode}`);

  try {
    const supabase = await createClient();
    // Tenta logar na tabela system_logs (se existir)
    const { error } = await supabase
      .from('system_logs')
      .insert([
        { 
          event_type: 'COMMAND_OVERRIDE', 
          message: `Operador ativou modo: ${mode}`,
          severity: mode === 'STOP' ? 'CRITICAL' : 'INFO',
          timestamp: new Date().toISOString()
        }
      ]);

    if (error) {
      // Fallback silencioso se a tabela não existir ainda
      console.warn("Log skipped (Table missing?):", error.message);
    }

    return { success: true, mode };
  } catch (err) {
    console.error("Falha ao enviar comando:", err);
    return { success: false, error: 'Database Connection Failed' };
  }
}
