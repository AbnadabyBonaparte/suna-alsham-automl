import { NextResponse } from 'next/server';
import { executeTask } from '@/lib/quantum-brain';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    if (!body.title || !body.description) {
      return NextResponse.json(
        { error: 'title and description are required' },
        { status: 400 }
      );
    }
    
    const result = await executeTask({
      title: body.title,
      description: body.description,
      data: body.data,
      priority: body.priority,
      user_id: body.user_id,
    });
    
    return NextResponse.json(result);
  } catch (error) {
    console.error('Execute error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
