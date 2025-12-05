/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - STRIPE CHECKOUT API
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/stripe/checkout/route.ts
 * 💳 Cria sessão de checkout Stripe
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

// Preços dos planos (em centavos - BRL)
const PRICE_CONFIG = {
    starter: {
        monthly: 99000,  // R$990
        yearly: 990000,  // R$9.900 (10x)
        name: 'ALSHAM QUANTUM - Starter',
    },
    pro: {
        monthly: 490000,  // R$4.900
        yearly: 4900000,  // R$49.000 (10x)
        name: 'ALSHAM QUANTUM - Pro',
    },
    enterprise: {
        monthly: 990000,   // R$9.900
        yearly: 9900000,   // R$99.000 (10x)
        name: 'ALSHAM QUANTUM - Enterprise',
    }
};

export async function POST(request: NextRequest) {
    try {
        const { planId, billingCycle = 'monthly' } = await request.json();

        // Validar plano
        if (!planId || !['starter', 'pro', 'enterprise'].includes(planId)) {
            return NextResponse.json(
                { error: 'Plano inválido' },
                { status: 400 }
            );
        }

        // Verificar chave do Stripe
        const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
        if (!stripeSecretKey) {
            console.error('STRIPE_SECRET_KEY não configurada');
            return NextResponse.json(
                { error: 'Configuração de pagamento não disponível. Entre em contato com o suporte.' },
                { status: 500 }
            );
        }

        const stripe = new Stripe(stripeSecretKey, {
            apiVersion: '2025-04-30.basil',
        });

        const plan = PRICE_CONFIG[planId as keyof typeof PRICE_CONFIG];
        const price = billingCycle === 'yearly' ? plan.yearly : plan.monthly;

        // Criar sessão de checkout
        const session = await stripe.checkout.sessions.create({
            payment_method_types: ['card'],
            line_items: [
                {
                    price_data: {
                        currency: 'brl',
                        product_data: {
                            name: plan.name,
                            description: `Plano ${planId.toUpperCase()} - ${billingCycle === 'monthly' ? 'Mensal' : 'Anual'}`,
                            images: ['https://quantum.alshamglobal.com.br/og-image.png'],
                        },
                        unit_amount: price,
                        recurring: {
                            interval: billingCycle === 'monthly' ? 'month' : 'year',
                        },
                    },
                    quantity: 1,
                },
            ],
            mode: 'subscription',
            success_url: `${process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'}/dashboard?success=true&plan=${planId}`,
            cancel_url: `${process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'}/pricing?canceled=true`,
            metadata: {
                planId,
                billingCycle,
            },
            allow_promotion_codes: true,
            billing_address_collection: 'required',
            customer_creation: 'always',
            locale: 'pt-BR',
        });

        return NextResponse.json({ url: session.url });

    } catch (error: any) {
        console.error('Stripe checkout error:', error);
        return NextResponse.json(
            { error: error.message || 'Erro ao criar sessão de pagamento' },
            { status: 500 }
        );
    }
}

