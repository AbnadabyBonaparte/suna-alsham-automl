import { NextResponse } from 'next/server';
import { getRealTimeMetrics, getRecentTasks } from '@/lib/quantum-brain';

export async function GET() {
  try {
    const [metrics, recentTasks] = await Promise.all([
      getRealTimeMetrics(),
      getRecentTasks(15),
    ]);
    
    return NextResponse.json({ metrics, recentTasks });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
