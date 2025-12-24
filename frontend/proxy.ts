/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - PROXY WRAPPER (DESABILITADO)
 * ═══════════════════════════════════════════════════════════════
 * 
 * NOTA: Este arquivo foi DESABILITADO após consolidação do middleware.
 * 
 * A lógica foi consolidada em frontend/src/middleware.ts
 * 
 * Este arquivo é mantido apenas para referência histórica.
 * O Next.js agora usa apenas middleware.ts
 */

import { type NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

// DESABILITADO: Middleware consolidado em src/middleware.ts
// Este arquivo não é mais usado pelo Next.js
export async function proxy(request: NextRequest) {
  // Deixa passar - lógica agora está em middleware.ts
  return NextResponse.next();
}

export const config = {
  matcher: [
    // Matcher vazio - não processa nenhuma rota
    // Middleware consolidado em src/middleware.ts
  ],
};

