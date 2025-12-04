// frontend/src/app/api/queue/process/route.ts
import { NextResponse } from 'next/server';

// FORÇA O NEXT.JS A NÃO PRÉ-RENDERIZAR ESTA ROTA (OBRIGATÓRIO!)
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';
export const maxDuration = 300; // 5 minutos

export async function POST() {
  return NextResponse.json({
    success: true,
    message: 'ALSHAM QUANTUM Queue Processor - ONLINE',
    status: 'active',
    timestamp: new Date().toISOString(),
    note: 'Processamento real será feito via Railway em breve',
  });
}

export async function GET() {
  return NextResponse.json({
    success: true,
    message: 'ALSHAM QUANTUM Queue Processor - READY',
    timestamp: new Date().toISOString(),
  });
}
