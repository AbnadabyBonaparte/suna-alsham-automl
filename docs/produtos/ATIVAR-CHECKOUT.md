# 💳 ATIVAR O CHECKOUT — guia do fundador

> O código de pagamento está **pronto e correto**. Falta o que só você pode fazer: criar os produtos no Stripe, colar as chaves na Vercel e aplicar uma migration no banco. Siga na ordem. **Nada aqui cobra ninguém** até você terminar e testar.

**Data:** 28/jul/2026 · **Escopo:** ligar a primeira venda real do ALSHAM QUANTUM.

---

## Antes de tudo: o bloqueio invisível (faça o passo 1 ou nada fecha)

A auditoria achou que faltavam só os price IDs. Achamos **um bloqueio maior**: o banco vivo não tem as colunas que o webhook grava depois do pagamento. Sem elas, o cliente **paga e não ganha acesso** — o pior dos mundos. O passo 1 conserta isso.

---

## Passo 1 — Aplicar a migration do banco (o elo pós-pagamento)

O arquivo já está no repo: `supabase/migrations/20260728_profiles_subscription_columns.sql`.

Ele adiciona 4 colunas em `public.profiles` (`stripe_customer_id`, `stripe_subscription_id`, `billing_cycle`, `subscription_end`). É aditivo e seguro — não mexe em nenhum dado existente.

**Como aplicar** (projeto Supabase `suna-core`):
1. Abra o Supabase → seu projeto **suna-core** → **SQL Editor**.
2. Cole o conteúdo do arquivo `20260728_profiles_subscription_columns.sql` e clique **Run**.
3. Deve dizer *Success*. Pronto — o webhook agora consegue gravar e o painel consegue liberar acesso.

> Sem este passo, os passos seguintes ligam a cobrança mas a venda **não fecha**.

---

## Passo 2 — Criar os 3 produtos e preços no Stripe

No painel do Stripe (**modo Test** primeiro, depois **Live**): **Products → Add product**. Crie três, todos **recorrentes / mensais**, moeda **BRL**:

| Produto | Preço | Ciclo |
|---|---|---|
| ALSHAM QUANTUM — Starter | **R$ 990,00** | mensal (recurring) |
| ALSHAM QUANTUM — Pro | **R$ 4.900,00** | mensal (recurring) |
| ALSHAM QUANTUM — Enterprise | **R$ 9.900,00** | mensal (recurring) |

Em cada um, depois de salvar, copie o **Price ID** (começa com `price_...`). Você terá três.

> O código só reconhece um plano se o `price_...` bater com a env var certa (passo 4). Anote qual price é de qual plano.

---

## Passo 3 — Pegar as chaves do Stripe

No Stripe, **Developers → API keys**:
- **Secret key** (`sk_live_...` ou `sk_test_...`) — secreta.
- **Publishable key** (`pk_live_...` ou `pk_test_...`) — pública.

O webhook secret vem no passo 5.

---

## Passo 4 — Colar as env vars na Vercel

No projeto **alsham-quantum** na Vercel → **Settings → Environment Variables**. Cadastre exatamente estes nomes:

| Env var | Valor | Tipo |
|---|---|---|
| `STRIPE_SECRET_KEY` | `sk_live_...` | 🔒 secreta (server) |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` (passo 5) | 🔒 secreta (server) |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | `pk_live_...` | 🌐 pública (vai no bundle) |
| `NEXT_PUBLIC_STRIPE_PRICE_STARTER` | `price_...` do Starter | 🌐 pública |
| `NEXT_PUBLIC_STRIPE_PRICE_PRO` | `price_...` do Pro | 🌐 pública |
| `NEXT_PUBLIC_STRIPE_PRICE_ENTERPRISE` | `price_...` do Enterprise | 🌐 pública |

As de Supabase (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`) já devem estar lá — o resto do sistema funciona. Se o webhook der "Sistema não configurado", confira que `SUPABASE_SERVICE_ROLE_KEY` existe.

> ⚠️ As `NEXT_PUBLIC_*` entram no site na **hora do build**. Depois de cadastrá-las, você **precisa fazer um redeploy** (passo 6) — só assim os price IDs saem do `""` e entram no botão "Assinar".

---

## Passo 5 — Cadastrar o webhook no Stripe

De nada adianta cobrar se o sistema não souber que foi pago. O webhook é quem avisa.

1. Stripe → **Developers → Webhooks → Add endpoint**.
2. **Endpoint URL:** `https://quantum.alshamglobal.com.br/api/stripe/webhook`
3. **Eventos a ouvir:** `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`.
4. Salve. O Stripe mostra um **Signing secret** (`whsec_...`). Copie e cole na env var `STRIPE_WEBHOOK_SECRET` (passo 4).

---

## Passo 6 — Redeploy e teste

1. Na Vercel, **Redeploy** o último deploy (para o build pegar as `NEXT_PUBLIC_*`).
2. Em **modo Test** do Stripe, entre logado na sua conta, vá em `/pricing` e clique **Assinar**.
3. Pague com o cartão de teste `4242 4242 4242 4242`, validade futura, CVC qualquer.
4. Confira: você deve cair no `/dashboard` com acesso liberado. No Supabase, seu `profiles.subscription_status` deve estar `active`.
5. Deu certo no teste? Troque as chaves de `test` para `live` (passos 3–5) e redeploy. Aí a venda é real.

---

## Passo 7 — Antes da primeira venda REAL (parecer LEXIS — jurídico)

Não é opcional: cobrar sem os termos publicados é risco de consumidor (CDC). Ver a seção LEXIS abaixo. O mínimo:
- Publicar **Termos de Assinatura** e **Política de Reembolso/Cancelamento**.
- Fazer as páginas `/terms` e `/privacy` existirem (hoje o rodapé aponta pra elas e dá 404).
- Garantir que a promessa "Garantia de 30 dias / cancele quando quiser" (que já está na tela) tenha respaldo escrito.

---

## Checklist rápido

- [ ] Passo 1 — migration `20260728_profiles_subscription_columns.sql` aplicada no suna-core
- [ ] Passo 2 — 3 produtos/preços criados (990 / 4.900 / 9.900 BRL, mensais)
- [ ] Passo 3 — secret key + publishable key copiadas
- [ ] Passo 4 — 6 env vars na Vercel
- [ ] Passo 5 — webhook cadastrado + `whsec_...` colado
- [ ] Passo 6 — redeploy + teste com cartão de teste passou
- [ ] Passo 7 — termos + política de reembolso publicados

---
*Guia de ativação · ALSHAM QUANTUM · Universo Bonaparte · ALSHAM Global.*
