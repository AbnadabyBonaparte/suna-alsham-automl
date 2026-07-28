/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM — /api/subscription/confirm-stay
 * ═══════════════════════════════════════════════════════════════
 * O usuário confirma que fica e renuncia à garantia comercial de 30 dias.
 * Isso libera a cota de experimentação (o limite abre para a franquia do
 * plano). A renúncia só tem efeito APÓS os 7 dias legais (o direito de
 * arrependimento do CDC é inrenunciável) — quem decide isso é quota.ts.
 * ═══════════════════════════════════════════════════════════════
 */

import { NextResponse } from 'next/server';
import { createClient as createServerSupabase } from '@/lib/supabase/server';
import { createAdminClient } from '@/lib/supabase/admin';

export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

export async function POST() {
  const supabase = await createServerSupabase();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: 'Faça login para confirmar.' }, { status: 401 });
  }

  const { error } = await createAdminClient()
    .from('profiles')
    .update({ guarantee_waived: true })
    .eq('id', user.id);

  if (error) {
    return NextResponse.json({ error: 'Não foi possível registrar a confirmação.' }, { status: 500 });
  }

  return NextResponse.json({
    ok: true,
    message: 'Permanência confirmada. Cota liberada. A garantia legal de 7 dias, se ainda vigente, permanece por lei.',
  });
}
