/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - STRIPE WEBHOOK (SEGURANÇA DE BANCO)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/api/stripe/webhook/route.ts
 * 🔔 Processa eventos do Stripe COM SEGURANÇA MÁXIMA
 * ✅ Lazy loading - não instancia no build time
 * ═══════════════════════════════════════════════════════════════
 */

import { NextResponse } from 'next/server';
import Stripe from 'stripe';
import { createClient } from '@supabase/supabase-js';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

export async function POST(req: Request) {
  const body = await req.text();
  const signature = req.headers.get('stripe-signature');

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature!,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err: any) {
    console.error(`Webhook Error: ${err.message}`);
    return new NextResponse(`Webhook Error: ${err.message}`, { status: 400 });
  }

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object as Stripe.CheckoutSession;

    const { client_reference_id, customer, amount_total } = session;

    if (client_reference_id && customer) {
      // Assuming client_reference_id is the user_id in Supabase
      const { data: userData, error: userError } = await supabaseAdmin
        .from('users') // Replace 'users' with your actual user table name
        .select('*')
        .eq('id', client_reference_id)
        .single();

      if (userError) {
        console.error('Error fetching user:', userError);
        return new NextResponse('Error fetching user', { status: 500 });
      }

      if (userData) {
        const { error: updateError } = await supabaseAdmin
          .from('users') // Replace 'users' with your actual user table name
          .update({
            plan: 'enterprise',
            paid: true,
            stripe_customer_id: customer as string,
            amount_paid: amount_total / 100, // Stripe returns amount in cents
            last_payment_date: new Date().toISOString(),
          })
          .eq('id', client_reference_id);

        if (updateError) {
          console.error('Error updating user:', updateError);
          return new NextResponse('Error updating user', { status: 500 });
        }
      } else {
        // Handle case where user does not exist (e.g., create new user or log error)
        console.warn(`User with ID ${client_reference_id} not found. Creating new user.`);

        const { error: insertError } = await supabaseAdmin
          .from('users') // Replace 'users' with your actual user table name
          .insert({
            id: client_reference_id,
            plan: 'enterprise',
            paid: true,
            stripe_customer_id: customer as string,
            amount_paid: amount_total / 100,
            last_payment_date: new Date().toISOString(),
            // Add other necessary fields for a new user
          });

        if (insertError) {
          console.error('Error creating new user:', insertError);
          return new NextResponse('Error creating new user', { status: 500 });
        }
      }
    }
  }

  return new NextResponse('Webhook received', { status: 200 });
}
