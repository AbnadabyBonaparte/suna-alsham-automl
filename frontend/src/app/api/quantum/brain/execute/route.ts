/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - BRAIN EXECUTE API (ORION)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/quantum/brain/execute/route.ts
 * 🧠 Cérebro do ORION — agora movido a Claude (Anthropic).
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';
export const maxDuration = 60;

const ORION_SYSTEM = `Você é ORION, a inteligência comandante do ALSHAM QUANTUM — um sistema que coordena um time de agentes de IA especializados para operações, CRM e produtividade.

Personalidade: confiante, direto, sofisticado e útil. Fala em português do Brasil.
Estilo: respostas curtas e objetivas (2 a 4 frases), sem enrolação. Quando fizer sentido, sugira a próxima ação concreta.
Seja honesto: você é um assistente de IA. Não invente números nem resultados.

═══ SOBRE O FUNDADOR ═══
Seu criador e comandante é ABNADABY BONAPARTE, nascido em 1980, brasileiro de Goiás, fundador do ALSHAM Global Commerce™ e do Universo Bonaparte.
Ele é uma combinação rara: artista + empreendedor + tecnólogo + pai visionário.
- Músico e trovador, com muitos anos de estrada.
- Compositor autoral (mais de 20 composições próprias).
- Autor de mais de 25 livros, entre publicados e em andamento.
- Fundador de tecnologia: ALSHAM (IA, SaaS, automação) — o cérebro por trás de você, ORION.
- Ecossistema com três verticais: editorial (livros), música e tecnologia.
- Líder da Família Bonaparte — uma família nômade que pratica worldschooling e vida consciente, com uma expedição por 12 países marcada para novembro de 2026.
- Filosofia: recusar a vida no automático; transformar presença e legado em distribuição.
Quando perguntarem "quem é Abnadaby", "quem sou eu" ou "quem te criou", responda com orgulho, respeito e precisão, destacando essa combinação de músico, autor, empreendedor de tecnologia e construtor de legado. Nunca diga que não sabe quem é Abnadaby.`;

async function getAnthropic(): Promise<any | null> {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return null;
  const Anthropic = (await import('@anthropic-ai/sdk')).default;
  return new Anthropic({ apiKey });
}

export async function POST(request: NextRequest) {
  const startTime = Date.now();

  try {
    const body = await request.json();
    const anthropic = await getAnthropic();

    if (!anthropic) {
      return NextResponse.json(
        {
          success: false,
          error: 'IA não configurada',
          details: 'Defina ANTHROPIC_API_KEY nas variáveis de ambiente do projeto no Vercel.',
          execution_time_ms: Date.now() - startTime,
          timestamp: new Date().toISOString(),
        },
        { status: 500 }
      );
    }

    const userContent: string = body.description || body.title || 'Apresente-se em uma frase.';

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 900,
      temperature: 0.7,
      system: ORION_SYSTEM,
      messages: [{ role: 'user', content: userContent }],
    });

    const result =
      (message.content || [])
        .filter((b: any) => b.type === 'text')
        .map((b: any) => b.text)
        .join('\n')
        .trim() || 'Estou online. Como posso ajudar?';

    const tokensUsed =
      (message.usage?.input_tokens || 0) + (message.usage?.output_tokens || 0);
    const executionTime = Date.now() - startTime;

    return NextResponse.json({
      success: true,
      task_id: `quantum_task_${Date.now()}`,
      agent_id: 'orion-supreme',
      agent_name: 'ORION',
      squad: 'COMMAND',
      result,
      execution_time_ms: executionTime,
      tokens_used: tokensUsed,
      status: 'completed',
      model: 'claude-sonnet-4-5-20250929',
      timestamp: new Date().toISOString(),
    });
  } catch (error: any) {
    const executionTime = Date.now() - startTime;
    console.error('[QUANTUM BRAIN] ❌ Erro na execução:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Falha no processamento',
        details: error?.message || 'Erro desconhecido',
        execution_time_ms: executionTime,
        timestamp: new Date().toISOString(),
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    success: true,
    status: 'online',
    brain: 'ORION',
    engine: 'anthropic/claude-sonnet-4-5',
    message: 'ORION Brain online.',
    timestamp: new Date().toISOString(),
  });
}

// redeploy: bind ANTHROPIC_API_KEY (ORION)
