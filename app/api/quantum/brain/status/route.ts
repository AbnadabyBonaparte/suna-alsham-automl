import { NextResponse } from 'next/server';
import { getBrainState, getRoleStats } from '@/lib/quantum-brain';

export async function GET() {
  try {
    const [state, roleStats] = await Promise.all([
      getBrainState(),
      getRoleStats(),
    ]);
    
    return NextResponse.json({
      ...state,
      roles: roleStats,
    });
  } catch (error) {
    console.error('Brain status error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
