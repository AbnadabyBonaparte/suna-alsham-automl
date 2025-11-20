import os

content = r"""'use server'

import { createClient } from '@supabase/supabase-js';

// Inicializa cliente server-side (seguro)
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const supabase = createClient(supabaseUrl, supabaseKey);

export async function toggleSystemMode(mode: 'TURBO' | 'SAFE' | 'STOP') {
  console.log(`[COMMAND] Switching system to: ${mode}`);

  try {
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
"""

with open("src/lib/actions.ts", "w") as f:
    f.write(content)

print("✅ src/lib/actions.ts restaurado com sucesso.")
