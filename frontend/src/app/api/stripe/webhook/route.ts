/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - STRIPE WEBHOOK
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/stripe/webhook/route.ts
 * 🔔 Sincroniza assinaturas do Stripe com public.profiles
 *    (subscription_plan, subscription_status, founder_access).
 * ✅ Lazy loading - não instancia no build time
 * ═══════════════════════════════════════════════════════════════
 */

import { NextResponse } from 'next/server';
import Stripe from 'stripe';
import { createClient, type SupabaseClient } from '@supabase/supabase-js';

export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

type PlanId = 'free' | 'starter' | 'pro' | 'enterprise';

// Mapeia um Stripe Price ID -> plano, usando as env vars dos preços.
function planFromPriceId(priceId?: string | null): PlanId | null {
  if (!priceId) return null;
  const map: Record<string, PlanId> = {};
  const starter = process.env.NEXT_PUBLIC_STRIPE_PRICE_STARTER;
  const pro = process.env.NEXT_PUBLIC_STRIPE_PRICE_PRO;
  const enterprise = process.env.NEXT_PUBLIC_STRIPE_PRICE_ENTERPRISE;
  if (starter) map[starter] = 'starter';
  if (pro) map[pro] = 'pro';
  if (enterprise) map[enterprise] = 'enterprise';
  return map[priceId] || null;
}

// Traduz o status da subscription do Stripe para o enum de profiles.
function mapSubscriptionStatus(
  status: Stripe.Subscription.Status,
): 'active' | 'inactive' | 'cancelled' | 'past_due' {
  switch (status) {
    case 'active':
    case 'trialing':
      return 'active';
    case 'past_due':
    case 'unpaid':
      return 'past_due';
    case 'canceled':
    case 'incomplete_expired':
      return 'cancelled';
    default:
      return 'inactive';
  }
}

async function updateProfileByCustomer(
  supabaseAdmin: SupabaseClient,
  customerId: string,
  fields: Record<string, unknown>,
): Promise<boolean> {
  const { data, error } = await supabaseAdmin
    .from('profiles')
    .update(fields)
    .eq('stripe_customer_id', customerId)
    .select('id');

  if (error) {
    console.error('Erro ao atualizar profile por customer:', error.message);
    return false;
  }
  return !!(data && data.length);
}

export async function POST(req: Request) {
  const body = await req.text();
  const signature = req.headers.get('stripe-signature');

  const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
  const stripeWebhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!stripeSecretKey || !stripeWebhookSecret || !supabaseUrl || !supabaseServiceKey) {
    console.error('❌ Configuração do Stripe/Supabase incompleta');
    return new NextResponse('Sistema não configurado', { status: 500 });
  }

  const stripe = new Stripe(stripeSecretKey, {
    apiVersion: '2023-10-16' as Stripe.LatestApiVersion,
  });

  const supabaseAdmin = createClient(supabaseUrl, supabaseServiceKey, {
    auth: { persistSession: false },
  });

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, signature!, stripeWebhookSecret);
  } catch (err: any) {
    console.error(`Webhook Error: ${err.message}`);
    return new NextResponse(`Webhook Error: ${err.message}`, { status: 400 });
  }

  try {
    switch (event.type) {
      // ── Assinatura criada via Checkout ──
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session;
        const userId = session.client_reference_id;
        const customerId = session.customer as string | null;
        const subscriptionId = session.subscription as string | null;

        if (!userId) {
          console.warn('checkout.session.completed sem client_reference_id — ignorado.');
          break;
        }

        // Descobrir o plano: metadata primeiro, senão pelo price da subscription.
        let plan = (session.metadata?.planId || session.metadata?.plan) as PlanId | undefined;
        const billingCycle = (session.metadata?.billingCycle as 'monthly' | 'yearly') || 'monthly';

        if (!plan && subscriptionId) {
          const sub = await stripe.subscriptions.retrieve(subscriptionId);
          plan = planFromPriceId(sub.items.data[0]?.price?.id) || undefined;
        }

        const { error } = await supabaseAdmin
          .from('profiles')
          .update({
            subscription_plan: plan || 'pro',
            subscription_status: 'active',
            billing_cycle: billingCycle,
            stripe_customer_id: customerId,
            stripe_subscription_id: subscriptionId,
          })
          .eq('id', userId);

        if (error) {
          console.error('Erro ao atualizar profile (checkout):', error.message);
          return new NextResponse('Error updating profile', { status: 500 });
        }
        break;
      }

      // ── Assinatura alterada (upgrade/downgrade/renovação/past_due) ──
      case 'customer.subscription.updated': {
        const sub = event.data.object as Stripe.Subscription;
        const customerId = sub.customer as string;
        const plan = planFromPriceId(sub.items.data[0]?.price?.id);
        const status = mapSubscriptionStatus(sub.status);

        const fields: Record<string, unknown> = {
          subscription_status: status,
          stripe_subscription_id: sub.id,
          subscription_end: sub.cancel_at
            ? new Date(sub.cancel_at * 1000).toISOString()
            : null,
        };
        if (plan) fields.subscription_plan = plan;

        await updateProfileByCustomer(supabaseAdmin, customerId, fields);
        break;
      }

      // ── Assinatura cancelada/expirada ──
      case 'customer.subscription.deleted': {
        const sub = event.data.object as Stripe.Subscription;
        const customerId = sub.customer as string;

        await updateProfileByCustomer(supabaseAdmin, customerId, {
          subscription_status: 'cancelled',
          subscription_plan: 'free',
          subscription_end: new Date().toISOString(),
        });
        break;
      }

      default:
        // Evento não tratado — apenas confirma o recebimento.
        break;
    }
  } catch (err: any) {
    console.error(`Webhook handler error (${event.type}):`, err?.message);
    return new NextResponse('Webhook handler error', { status: 500 });
  }

  return new NextResponse('Webhook received', { status: 200 });
}
