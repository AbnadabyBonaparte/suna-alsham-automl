# Teste da Esteira de Pagamento — sem compra real

**Data:** 2026-07-29 · **Banco:** suna-core (`vktzdrsigrdnemdshcdp`) · **Deploy:** alsham-quantum.vercel.app
**Método:** simulação de evento + chamada da API real. **Zero cobrança. Zero cartão.**

---

## 1. VERTEX — como um usuário vira assinante

```
/pricing  →  POST /api/stripe/checkout
             (client_reference_id = userId, metadata.planId, mode: subscription)
          →  stripe.checkout.sessions.create  →  URL do Stripe
          →  [pagamento real na página do Stripe]
          →  Stripe dispara checkout.session.completed
          →  POST /api/stripe/webhook  (verifica assinatura com STRIPE_WEBHOOK_SECRET)
          →  UPDATE public.profiles WHERE id = userId:
                subscription_plan, subscription_status='active', billing_cycle,
                stripe_customer_id, stripe_subscription_id
             UPDATE guarantee_started_at = now()  (só na 1ª ativação, WHERE ... IS NULL)
          →  requireDashboardAccess (server.ts):
                hasAccess = founder_access OR email==founder
                            OR (plan=='enterprise' && status=='active')
                            OR status=='active'
```

O elo crítico é `subscription_status='active'` → o dashboard libera.

---

## 2. Ativação (o elo crítico) — PROVADO por simulação no banco

Usuário de teste criado (`quantum-esteira-test@alsham.test`), aplicado o **efeito exato**
do handler `checkout.session.completed`, e depois **removido** (zero lixo).

| Campo | ANTES (sem assinar) | DEPOIS (efeito do webhook) |
|---|---|---|
| subscription_plan | `free` | `pro` |
| subscription_status | `free` | `active` |
| billing_cycle | — | `monthly` |
| stripe_customer_id | `null` | `cus_TEST…` |
| stripe_subscription_id | `null` | `sub_TEST…` |
| guarantee_started_at | `null` | setado (1ª ativação) |
| **has_access_dashboard** | **false** ❌ | **true** ✅ |

Limpeza confirmada: `profiles_left=0, auth_users_left=0`, total voltou a 8 (original).

---

## 3. Checkout Session — PROVADO na API real (sem pagar)

`POST /api/stripe/checkout` no deploy de produção, com os 3 `price_id` reais
(extraídos do bundle público) + header `Origin` (como o browser envia):

| Plano (price_id) | Resultado |
|---|---|
| `price_1Ty9Xg…8qbkJl` | ✅ `cs_live_…` criada |
| `price_1Ty9Xg…SLhOvQF` | ✅ `cs_live_…` criada |
| `price_1Ty9Xh…ZGaE3PCy` | ✅ `cs_live_…` criada |

Prova que a chave `STRIPE_SECRET_KEY` de produção **é válida e tem permissão de
Checkout Sessions** (nenhum erro 401/403) e que os **3 preços existem e estão ativos**
em modo live. Sessões são só links — expiram sem uso, nada é cobrado.

## Webhook — deployado e protegido

`POST /api/stripe/webhook` com evento **forjado** → **HTTP 400** + erro de assinatura
do Stripe. Prova que o endpoint está no ar, **rejeita eventos sem assinatura válida**,
e que `STRIPE_WEBHOOK_SECRET` + envs do Supabase **estão configurados** na Vercel
(senão a resposta seria 500 "Sistema não configurado").

---

## 🔧 Achado (corrigido nesta branch)

`success_url`/`cancel_url` eram montados **só** a partir de `req.headers.get('origin')`.
Sem o header `Origin`, o Stripe recusa com `url_invalid` ("An explicit scheme must be
provided") e o pagamento não inicia. No browser o header existe, mas é frágil.
**Correção:** fallback para `NEXT_PUBLIC_SITE_URL` e, por fim, a URL canônica.

---

## ✅ Veredito

**A esteira está pronta para uma compra real** — com **uma** verificação final que só o
dono pode fechar:

- ✅ Checkout cria sessão (chave válida, permissão OK, 3 preços ativos).
- ✅ Ativação grava os campos certos e libera o dashboard.
- ✅ Webhook no ar e enforçando assinatura; envs presentes.
- ⚠️ **Não verificável sem o dono (Lei 7):** que o valor de `STRIPE_WEBHOOK_SECRET`
  na Vercel seja **o mesmo** secret do endpoint cadastrado no Stripe Dashboard. Se
  divergirem, eventos reais também tomam 400 e a ativação falha silenciosa.
  **Como fechar:** Stripe Dashboard → Developers → Webhooks → seu endpoint →
  "Send test event" (`checkout.session.completed`) e conferir se o profile ativa;
  ou `stripe trigger checkout.session.completed` via Stripe CLI.
