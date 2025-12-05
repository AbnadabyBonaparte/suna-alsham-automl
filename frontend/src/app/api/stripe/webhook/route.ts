/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - STRIPE WEBHOOK
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/stripe/webhook/route.ts
 * 🔔 Processa eventos do Stripe (pagamento, cancelamento, etc)
 * ═══════════════════════════════════════════════════════════════
 */

import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { createClient } from '@supabase/supabase-js';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || '', {
    apiVersion: '2025-04-30.basil',
});

const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL || '',
    process.env.SUPABASE_SERVICE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
);

export async function POST(request: NextRequest) {
    const body = await request.text();
    const signature = request.headers.get('stripe-signature');

    if (!signature) {
        return NextResponse.json({ error: 'Missing signature' }, { status: 400 });
    }

    let event: Stripe.Event;

    try {
        event = stripe.webhooks.constructEvent(
            body,
            signature,
            process.env.STRIPE_WEBHOOK_SECRET || ''
        );
    } catch (err: any) {
        console.error('Webhook signature verification failed:', err.message);
        return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
    }

    try {
        switch (event.type) {
            case 'checkout.session.completed': {
                const session = event.data.object as Stripe.Checkout.Session;
                await handleCheckoutCompleted(session);
                break;
            }

            case 'customer.subscription.created':
            case 'customer.subscription.updated': {
                const subscription = event.data.object as Stripe.Subscription;
                await handleSubscriptionUpdate(subscription);
                break;
            }

            case 'customer.subscription.deleted': {
                const subscription = event.data.object as Stripe.Subscription;
                await handleSubscriptionCanceled(subscription);
                break;
            }

            case 'invoice.payment_succeeded': {
                const invoice = event.data.object as Stripe.Invoice;
                await handlePaymentSucceeded(invoice);
                break;
            }

            case 'invoice.payment_failed': {
                const invoice = event.data.object as Stripe.Invoice;
                await handlePaymentFailed(invoice);
                break;
            }

            default:
                console.log(`Unhandled event type: ${event.type}`);
        }

        return NextResponse.json({ received: true });

    } catch (error: any) {
        console.error('Webhook processing error:', error);
        return NextResponse.json(
            { error: 'Webhook handler failed' },
            { status: 500 }
        );
    }
}

async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
    const customerId = session.customer as string;
    const customerEmail = session.customer_details?.email;
    const planId = session.metadata?.planId || 'starter';
    const billingCycle = session.metadata?.billingCycle || 'monthly';

    console.log(`✅ Checkout completed for ${customerEmail}, plan: ${planId}`);

    if (!customerEmail) return;

    // Criar ou atualizar profile no Supabase
    const { error } = await supabase
        .from('profiles')
        .upsert({
            email: customerEmail,
            stripe_customer_id: customerId,
            subscription_plan: planId,
            subscription_status: 'active',
            billing_cycle: billingCycle,
            subscription_start: new Date().toISOString(),
            updated_at: new Date().toISOString(),
        }, {
            onConflict: 'email'
        });

    if (error) {
        console.error('Error upserting profile:', error);
    }

    // Registrar evento
    await supabase.from('subscription_events').insert({
        customer_email: customerEmail,
        stripe_customer_id: customerId,
        event_type: 'checkout_completed',
        plan_id: planId,
        billing_cycle: billingCycle,
        amount: session.amount_total,
        created_at: new Date().toISOString(),
    });
}

async function handleSubscriptionUpdate(subscription: Stripe.Subscription) {
    const customerId = subscription.customer as string;
    const status = subscription.status;
    const planId = subscription.metadata?.planId;

    console.log(`📝 Subscription updated for customer ${customerId}, status: ${status}`);

    // Atualizar status da subscription
    const { error } = await supabase
        .from('profiles')
        .update({
            subscription_status: status,
            updated_at: new Date().toISOString(),
        })
        .eq('stripe_customer_id', customerId);

    if (error) {
        console.error('Error updating subscription:', error);
    }
}

async function handleSubscriptionCanceled(subscription: Stripe.Subscription) {
    const customerId = subscription.customer as string;

    console.log(`❌ Subscription canceled for customer ${customerId}`);

    // Atualizar status
    const { error } = await supabase
        .from('profiles')
        .update({
            subscription_status: 'canceled',
            subscription_end: new Date().toISOString(),
            updated_at: new Date().toISOString(),
        })
        .eq('stripe_customer_id', customerId);

    if (error) {
        console.error('Error canceling subscription:', error);
    }
}

async function handlePaymentSucceeded(invoice: Stripe.Invoice) {
    const customerId = invoice.customer as string;
    const amount = invoice.amount_paid;

    console.log(`💰 Payment succeeded for customer ${customerId}, amount: ${amount}`);

    // Registrar pagamento
    await supabase.from('payments').insert({
        stripe_customer_id: customerId,
        stripe_invoice_id: invoice.id,
        amount: amount,
        currency: invoice.currency,
        status: 'succeeded',
        created_at: new Date().toISOString(),
    });
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
    const customerId = invoice.customer as string;

    console.log(`⚠️ Payment failed for customer ${customerId}`);

    // Registrar falha
    await supabase.from('payments').insert({
        stripe_customer_id: customerId,
        stripe_invoice_id: invoice.id,
        amount: invoice.amount_due,
        currency: invoice.currency,
        status: 'failed',
        created_at: new Date().toISOString(),
    });

    // Atualizar status
    await supabase
        .from('profiles')
        .update({
            subscription_status: 'past_due',
            updated_at: new Date().toISOString(),
        })
        .eq('stripe_customer_id', customerId);
}

