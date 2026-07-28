/**
 * ═══════════════════════════════════════════════════════════════════════════
 * STRIPE SETUP — cria os 3 produtos/preços mensais + o webhook, idempotente.
 * ═══════════════════════════════════════════════════════════════════════════
 * Valores CONFIRMADOS por VERTEX no código (não presumidos):
 *   env vars  : NEXT_PUBLIC_STRIPE_PRICE_STARTER / _PRO / _ENTERPRISE
 *   webhook   : https://quantum.alshamglobal.com.br/api/stripe/webhook
 *   eventos   : checkout.session.completed, customer.subscription.updated,
 *               customer.subscription.deleted
 *   modo      : subscription (recorrente) · moeda BRL · intervalo month
 *
 * NÃO roda sem a chave. Exige STRIPE_API_KEY (rk_live restrita "Assinaturas
 * recorrentes e faturamento", ou sk_...). Lei 7: sem chave, para e avisa.
 *
 *   STRIPE_API_KEY=rk_live_xxx node scripts/stripe-setup.mjs         # cria/reusa
 *   STRIPE_API_KEY=rk_live_xxx node scripts/stripe-setup.mjs --dry   # só mostra o plano
 *
 * IDEMPOTENTE: procura produto pelo nome e preço pelos atributos antes de criar;
 * não duplica. Webhook: procura pela URL antes de criar.
 * ═══════════════════════════════════════════════════════════════════════════
 */

const KEY = process.env.STRIPE_API_KEY;
const DRY = process.argv.includes('--dry');
const BASE = 'https://api.stripe.com/v1';

const WEBHOOK_URL = 'https://quantum.alshamglobal.com.br/api/stripe/webhook';
const WEBHOOK_EVENTS = [
  'checkout.session.completed',
  'customer.subscription.updated',
  'customer.subscription.deleted',
];

// nome do produto → { envVar, unit_amount (centavos), plano }
const PLANS = [
  { name: 'ALSHAM QUANTUM — Starter',    env: 'NEXT_PUBLIC_STRIPE_PRICE_STARTER',    amount: 99000,  plan: 'starter' },
  { name: 'ALSHAM QUANTUM — Pro',        env: 'NEXT_PUBLIC_STRIPE_PRICE_PRO',        amount: 490000, plan: 'pro' },
  { name: 'ALSHAM QUANTUM — Enterprise', env: 'NEXT_PUBLIC_STRIPE_PRICE_ENTERPRISE', amount: 990000, plan: 'enterprise' },
];
const CURRENCY = 'brl';
const INTERVAL = 'month';

if (!KEY) {
  console.error('⛔ STRIPE_API_KEY ausente. Este script NÃO cria nada sem a chave.');
  console.error('   Rode:  STRIPE_API_KEY=rk_live_... node scripts/stripe-setup.mjs');
  process.exit(1);
}

function form(obj) {
  // codifica objeto (com arrays estilo Stripe: enabled_events[]=...) em x-www-form-urlencoded
  const p = new URLSearchParams();
  for (const [k, v] of Object.entries(obj)) {
    if (Array.isArray(v)) v.forEach((item) => p.append(`${k}[]`, item));
    else p.append(k, String(v));
  }
  return p;
}

async function api(method, path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${KEY}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: body ? form(body) : undefined,
  });
  const json = await res.json();
  if (!res.ok) {
    throw new Error(`Stripe ${method} ${path} → ${res.status}: ${json.error?.message || JSON.stringify(json)}`);
  }
  return json;
}

async function findProductByName(name) {
  const r = await api('GET', '/products?limit=100&active=true');
  return r.data.find((p) => p.name === name) || null;
}

async function findMonthlyPrice(productId, amount) {
  const r = await api('GET', `/prices?product=${productId}&limit=100&active=true`);
  return r.data.find(
    (p) => p.currency === CURRENCY && p.unit_amount === amount && p.recurring?.interval === INTERVAL,
  ) || null;
}

async function findWebhook(url) {
  const r = await api('GET', '/webhook_endpoints?limit=100');
  return r.data.find((w) => w.url === url) || null;
}

async function main() {
  console.log(`=== STRIPE SETUP ${DRY ? '(DRY — só mostra o plano)' : '(criando/reusando)'} · chave ${KEY.slice(0, 8)}… ===\n`);
  const out = {};

  for (const plan of PLANS) {
    let product = await findProductByName(plan.name);
    if (!product) {
      if (DRY) { console.log(`  [criaria] produto "${plan.name}"`); }
      else { product = await api('POST', '/products', { name: plan.name }); console.log(`  [novo]   produto "${plan.name}" → ${product.id}`); }
    } else {
      console.log(`  [existe] produto "${plan.name}" → ${product.id}`);
    }

    let price = product ? await findMonthlyPrice(product.id, plan.amount) : null;
    if (!price) {
      const desc = `R$ ${(plan.amount / 100).toLocaleString('pt-BR')}/mês BRL`;
      if (DRY || !product) { console.log(`  [criaria] preço ${desc} para "${plan.name}"`); }
      else {
        price = await api('POST', '/prices', {
          product: product.id, unit_amount: plan.amount, currency: CURRENCY,
          'recurring[interval]': INTERVAL,
        });
        console.log(`  [novo]   preço ${desc} → ${price.id}`);
      }
    } else {
      console.log(`  [existe] preço ${plan.amount / 100} BRL/mês → ${price.id}`);
    }
    out[plan.env] = price?.id || '(pendente)';
  }

  // Webhook
  let wh = await findWebhook(WEBHOOK_URL);
  let whSecret = '(já existe — o secret só aparece na criação; se precisar, gere um novo endpoint ou role o secret)';
  if (!wh) {
    if (DRY) { console.log(`\n  [criaria] webhook ${WEBHOOK_URL} eventos: ${WEBHOOK_EVENTS.join(', ')}`); }
    else {
      wh = await api('POST', '/webhook_endpoints', { url: WEBHOOK_URL, enabled_events: WEBHOOK_EVENTS });
      whSecret = wh.secret;
      console.log(`\n  [novo]   webhook → ${wh.id}`);
    }
  } else {
    console.log(`\n  [existe] webhook ${WEBHOOK_URL} → ${wh.id}`);
  }

  console.log('\n═══ COLE NA VERCEL (projeto alsham-quantum) ═══');
  for (const plan of PLANS) console.log(`${plan.env} = ${out[plan.env]}`);
  console.log(`STRIPE_WEBHOOK_SECRET = ${whSecret}`);
  console.log('\nDepois de colar: REDEPLOY (as NEXT_PUBLIC_* só entram no build).');
}

main().catch((e) => { console.error(`\n⛔ ${e.message}`); process.exit(1); });
