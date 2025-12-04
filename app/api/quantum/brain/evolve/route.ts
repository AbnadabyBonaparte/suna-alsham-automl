import { NextResponse } from 'next/server';
import { runEvolutionCycle, getEvolutionCandidates, getEvolutionHistory } from '@/lib/quantum-brain';

export async function POST() {
  try {
    const result = await runEvolutionCycle();
    return NextResponse.json(result);
  } catch (error) {
    console.error('Evolution error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function GET() {
  try {
    const [candidates, history] = await Promise.all([
      getEvolutionCandidates(),
      getEvolutionHistory(5),
    ]);
    
    return NextResponse.json({ candidates, history });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
