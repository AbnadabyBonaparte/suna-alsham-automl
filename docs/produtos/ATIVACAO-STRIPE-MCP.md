# 🔌 Ativação do Stripe via MCP — o que ligou e o que ficou

> O fundador pediu: usar os conectores, não só preparar. Aqui está o alcance real de cada MCP (Lei 7 — testado, não presumido), o que ficou LIGADO via MCP, e a lista mínima que ainda é do fundador.
>
> **Data:** 28/jul/2026.

---

## Alcance REAL de cada MCP (declarado antes de agir)

| Conector | O que EU consigo fazer | O que NÃO consigo |
|---|---|---|
| **Supabase MCP** | ✅ **Tudo que precisei:** aplicar migration (DDL), executar SQL, rodar advisors. | — |
| **Vercel MCP** | ✅ **Ler:** listar times/projetos, deployments, logs, analytics. Deploy de projeto novo a partir de arquivos. | ❌ **Não existe tool para escrever env var** de um projeto existente, nem para redeploy do projeto existente. |
| **Stripe MCP** | ❌ **Não existe conector Stripe nesta sessão.** | ❌ Criar produto/preço, cadastrar webhook, pegar chaves — nada. |

**Conclusão honesta:** a única ativação que dava pra fazer via MCP era a **migration da cota** (Supabase). Produtos, preços, webhook e env vars **dependem do fundador** — não por preguiça, mas porque o Stripe MCP não existe e o Vercel MCP não escreve env var. **Não inventei nenhuma credencial.**

---

## 1. ✅ FEITO via MCP — migration da cota aplicada (Supabase)

Apliquei `20260728_quota_garantia.sql` no banco `suna-core` (`vktzdrsigrdnemdshcdp`).

**Antes → Depois (contra-prova read-after-write):**
- `profiles.guarantee_started_at` (timestamptz) — ❌ ausente → ✅ criada
- `profiles.guarantee_waived` (boolean, default false) — ❌ ausente → ✅ criada
- índice `idx_requests_user_created` — ✅ criado
- RLS: `enabled=true`, **10 policies** (inalteradas) · `profiles` **8 linhas** (intactas) · `service_role` DML completo
- Advisors de segurança: **0 ERROR** (o único INFO é o cofre `agent_prompts`, sem policy por design)

**Prova da esteira (custo zero — WHERE false, 0 linhas tocadas):**
- O `UPDATE` de ativação do assinante (`subscription_status='active'`, billing_cycle, stripe_*) → **statement válido**.
- O `UPDATE` que grava `guarantee_started_at` na 1ª ativação → **válido**.
- A `SELECT count` da cota (uso na janela) → **roda**.

→ Com as colunas no lugar, quando o Stripe confirmar um pagamento, o assinante é ativado e a cota passa a valer. **A esteira do lado do banco está pronta.**

> As duas migrations do checkout agora estão **aplicadas** no suna-core: `20260728_profiles_subscription_columns` (elo pós-pagamento, aplicada antes) e `20260728_quota_garantia` (cota, aplicada agora).

---

## 2. ⛔ NÃO deu via MCP — Stripe (não há conector)

Estes passos **são do fundador** (painel Stripe). Crie em **modo Test** primeiro, depois **Live**:

**Produtos e preços — recorrentes, MENSAIS, moeda BRL:**
| Produto | Preço | Intervalo |
|---|---|---|
| ALSHAM QUANTUM — Starter | R$ 990,00 | monthly |
| ALSHAM QUANTUM — Pro | R$ 4.900,00 | monthly |
| ALSHAM QUANTUM — Enterprise | R$ 9.900,00 | monthly |

Copie os 3 `price_...` gerados.

> ⚠️ **Lei 7 — só mensal por enquanto.** O código envia **um único `priceId` por plano**, independente do toggle mensal/anual da tela. Criar preço anual no Stripe **não** basta: o botão "Anual" ainda cobraria o preço mensal. Anual é uma **mudança de código** (segundo conjunto de price IDs + escolha por `billingCycle`), não só configuração. Recomendo ativar **mensal** agora; anual entra depois como tarefa de código.

**Webhook (o handler já trata estes eventos):**
- URL: `https://quantum.alshamglobal.com.br/api/stripe/webhook`
- Eventos: `checkout.session.completed` · `customer.subscription.updated` · `customer.subscription.deleted`
- Copie o `whsec_...` gerado.

---

## 3. ⛔ NÃO deu via MCP — env vars na Vercel (MCP não escreve env)

O Vercel MCP **lê** mas não escreve env var. Você cadastra no painel:
**Projeto:** `alsham-quantum` (`prj_F6h3VVYDIU3CBl3gT9x1fb03EyNX`, team `team_GaoyoGePPKNFDUMfZPM0YAVr`) → Settings → Environment Variables.

| Env var | Valor | Tipo |
|---|---|---|
| `NEXT_PUBLIC_STRIPE_PRICE_STARTER` | `price_...` Starter | pública |
| `NEXT_PUBLIC_STRIPE_PRICE_PRO` | `price_...` Pro | pública |
| `NEXT_PUBLIC_STRIPE_PRICE_ENTERPRISE` | `price_...` Enterprise | pública |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | `pk_live_...` (Stripe → API keys) | pública |
| `STRIPE_SECRET_KEY` | `sk_live_...` | 🔒 secreta |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` (passo 2) | 🔒 secreta |

Depois: **Redeploy** (as `NEXT_PUBLIC_*` só entram no bundle no build). O Vercel MCP também não redeploya o projeto existente — o clique é seu.

---

## 4. Estado da esteira — o que já está ligado

| Elo | Estado |
|---|---|
| Colunas de assinatura + cota no banco | ✅ **ligado (via MCP)** |
| Webhook → ativa assinante → cota | ✅ código no ar; provado no banco |
| Portão `requireDashboardAccess` lê as colunas | ✅ ligado |
| Produtos/preços no Stripe | ⛔ **falta o fundador** |
| Env vars + redeploy na Vercel | ⛔ **falta o fundador** |
| Webhook cadastrado no Stripe | ⛔ **falta o fundador** |

---

## O que ficou LIGADO via MCP
- ✅ Migration da cota aplicada no suna-core, com contra-prova, RLS intacta e advisors 0 ERROR.
- ✅ Esteira do banco provada (ativação + cota) a custo zero.

## A lista MÍNIMA que ainda é do fundador
1. Criar os **3 produtos/preços mensais** no Stripe (BRL) → copiar os `price_...`.
2. Cadastrar o **webhook** (URL + 3 eventos) → copiar o `whsec_...`.
3. Colar as **6 env vars** na Vercel (as 4 públicas + `STRIPE_SECRET_KEY` + `STRIPE_WEBHOOK_SECRET`) e **redeploy**.
4. **1 compra de teste** com cartão de teste do Stripe (`4242 4242 4242 4242`) para provar ponta a ponta.

Nada além disso. As chaves secretas são as únicas coisas que, por segurança, só você deve colar — e eu não as inventei.

---
*Ativação Stripe via MCP · ALSHAM QUANTUM · Universo Bonaparte · ALSHAM Global.*
