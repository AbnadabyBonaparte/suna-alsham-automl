/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - STRIPE CHECKOUT API (SEGURO)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/stripe/checkout/route.ts
 * 💳 Cria sessão de checkout Stripe COM SESSION_ID no redirect
 * ✅ Segurança: Acesso só liberado após webhook confirmar
 * ═══════════════════════════════════════════════════════════════
 */

import { NextResponse } from 'next/server';
import Stripe from 'stripe';

export async function POST(req: Request) {
  const { priceId, userId } = await req.json();

  // Verificar se as chaves estão configuradas
  const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
  if (!stripeSecretKey) {
    console.error('❌ STRIPE_SECRET_KEY não configurada');
    return new NextResponse('Sistema não configurado', { status: 500 });
  }

  const stripe = new Stripe(stripeSecretKey, {
    apiVersion: '2023-10-16',
  });

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: priceId, // Stripe Price ID for the Enterprise plan
          quantity: 1,
        },
      ],
      mode: 'subscription',
      success_url: `${req.headers.get('origin')}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${req.headers.get('origin')}/pricing`,
      client_reference_id: userId, // Pass user ID to webhook
      metadata: { plan: 'enterprise' }, // Pass plan info to webhook
    });

    return NextResponse.json({ url: session.url });
  } catch (error: any) {
    console.error('Error creating checkout session:', error);
    return new NextResponse(`Error creating checkout session: ${error.message}`, { status: 500 });
  }
}

// ========================================
// GET: Verificar status da sessão
// ========================================
export async function GET(request: Request) {
    const sessionId = request.nextUrl.searchParams.get('session_id');

    if (!sessionId) {
        return NextResponse.json(
            { error: 'session_id é obrigatório' },
            { status: 400 }
        );
    }

    try {
        const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
        if (!stripeSecretKey) {
            return NextResponse.json(
                { error: 'Sistema não configurado' },
                { status: 500 }
            );
        }

        const stripe = new Stripe(stripeSecretKey, {
            apiVersion: '2025-04-30.basil',
        });

        const session = await stripe.checkout.sessions.retrieve(sessionId);

        return NextResponse.json({
            status: session.payment_status,
            customer_email: session.customer_details?.email,
            plan: session.metadata?.planId,
            paid: session.payment_status === 'paid',
        });

    } catch (error: any) {
        console.error('❌ Error retrieving session:', error);
        return NextResponse.json(
            { error: 'Sessão não encontrada' },
            { status: 404 }
        );
    }
}
