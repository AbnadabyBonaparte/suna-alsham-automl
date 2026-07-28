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
  const { priceId, userId, planId, billingCycle, termsAcceptedAt } = await req.json();

  // ── Guarda 1: sem priceId válido, NÃO cobra. Erro claro, não Stripe 500 opaco.
  // Sem os NEXT_PUBLIC_STRIPE_PRICE_* na Vercel, priceId chega '' — barra aqui.
  if (!priceId || typeof priceId !== 'string' || !priceId.startsWith('price_')) {
    console.error('❌ priceId ausente/inválido — plano não configurado (falta env NEXT_PUBLIC_STRIPE_PRICE_*)');
    return NextResponse.json(
      { error: 'Plano ainda não está disponível para compra. Tente novamente em instantes ou fale com o suporte.' },
      { status: 400 },
    );
  }

  // ── Guarda 2: sem userId, o webhook não sabe QUEM pagou → pagaria sem ganhar
  // acesso. Exige usuário logado antes de cobrar.
  if (!userId || typeof userId !== 'string') {
    return NextResponse.json(
      { error: 'Entre na sua conta antes de assinar — assim liberamos seu acesso após o pagamento.' },
      { status: 401 },
    );
  }

  // Verificar se as chaves estão configuradas
  const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
  if (!stripeSecretKey) {
    console.error('❌ STRIPE_SECRET_KEY não configurada');
    return NextResponse.json({ error: 'Sistema de pagamento não configurado.' }, { status: 500 });
  }

  const stripe = new Stripe(stripeSecretKey, {
    apiVersion: '2023-10-16' as Stripe.LatestApiVersion,
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
      metadata: {
        planId: planId || '',
        billingCycle: billingCycle || 'monthly',
        // Registro de consentimento aos termos (LGPD/CDC) — data/hora do aceite.
        termsAcceptedAt: typeof termsAcceptedAt === 'string' ? termsAcceptedAt : new Date().toISOString(),
      },
    });

    return NextResponse.json({ url: session.url });
  } catch (error: any) {
    // Revela a causa real (nunca engole). O erro cru vai pro log do servidor.
    const code = error?.code || error?.type || 'unknown';
    const raw = error?.raw?.message || error?.message || 'erro desconhecido';
    console.error('❌ Stripe checkout.sessions.create falhou:', code, '—', raw);

    // Causa comum: chave restrita (rk_live de billing) sem permissão de Checkout.
    const isPermission = error?.type === 'StripePermissionError' || error?.statusCode === 403;
    const isAuth = error?.type === 'StripeAuthenticationError' || error?.statusCode === 401;
    const message = isPermission
      ? 'A chave do Stripe não tem permissão para criar Checkout Sessions. Use a secret key padrão (sk_live_…) ou uma chave restrita com "Checkout Sessions: Write".'
      : isAuth
        ? 'A chave do Stripe (STRIPE_SECRET_KEY) é inválida ou de outro modo (test/live). Confira o valor na Vercel.'
        : `Não foi possível iniciar o pagamento: ${raw}`;

    return NextResponse.json({ error: message, code }, { status: error?.statusCode || 500 });
  }
}

// ========================================
// GET: Verificar status da sessão
// ========================================
export async function GET(request: Request) {
    const url = new URL(request.url);
    const sessionId = url.searchParams.get('session_id');

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
            apiVersion: '2023-10-16' as Stripe.LatestApiVersion,
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
