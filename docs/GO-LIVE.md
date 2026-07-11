# 🚀 GO-LIVE — ALSHAM QUANTUM (suna-alsham-automl)

Guia passo-a-passo para colocar a plataforma **no ar com os 10 agentes reais rodando** e o
billing (Stripe) ativo.
Tempo estimado: **~40–60 min** de configuração (o código já está pronto — aqui só ligamos chaves e banco).

> **Regra de ouro:** nunca cole segredos reais em arquivos versionados. Tudo abaixo vai nas
> **Environment Variables da Vercel** (Production), não no repositório. A `SUPABASE_SERVICE_ROLE_KEY`
> e a `STRIPE_SECRET_KEY` são **server-only** — nunca prefixe com `NEXT_PUBLIC_`.

> **Onde fica o produto:** o app Next.js vive em `frontend/`. Não existe `package.json` na raiz do
> monorepo — todos os comandos `npm` rodam dentro de `frontend/`.

---

## 0. Pré-requisitos (contas)

| Conta | Para quê | Obrigatória? |
|---|---|---|
| **Supabase** | banco (Postgres) + Auth + os 10 agentes | ✅ sim |
| **OpenAI** | motor dos 10 agentes (`task-executor`, `gpt-4o-mini`) | ✅ sim |
| **Anthropic** | chat do agente **ORION** (`claude-sonnet-4-5`) | ✅ sim |
| **Stripe** | billing / assinaturas (Starter · Pro · Enterprise) | ✅ sim (se for cobrar) |
| **Vercel** | onde o frontend roda (já conectado ao repo) | ✅ sim |

---

## 1. Supabase — criar projeto e pegar as chaves (5 min)

1. Crie um projeto em **supabase.com → New project**.
2. Vá em **Project Settings → API** e copie:
   - **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
   - **anon / public key** → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - **service_role key** (seção *Project API keys*, revele com "Reveal") → `SUPABASE_SERVICE_ROLE_KEY`

> ⚠️ A `service_role` **ignora RLS** e é o que permite o motor de agentes gravar resultados no banco.
> É **secreta**: só entra em variável de ambiente server-side, nunca no client.

---

## 2. Aplicar as migrations — **NA ORDEM** (10 min)

No **Supabase → SQL Editor**, cole e rode o conteúdo de cada arquivo **nesta sequência exata**.
A ordem importa: a tabela `agents` precisa existir antes das colunas/tarefas que a referenciam.

| # | Arquivo | O que cria |
|---|---|---|
| 1 | `supabase/migrations/20251223_create_agents_table.sql` | tabela `agents` (base dos 10 agentes) |
| 2 | `supabase/migrations/20260710_quantum_tasks_and_agent_columns.sql` | tabela de tarefas quânticas + colunas extras em `agents` |
| 3 | `supabase/migrations/20260710_profiles_stripe_columns.sql` | colunas de billing (Stripe) em `profiles` |

Depois das 3 migrations, **rode o seed** para popular os 10 agentes:

| Seed | Arquivo | O que faz |
|---|---|---|
| 4 | `supabase/seed_agents.sql` | insere os **10 agentes reais** na tabela `agents` |

> ✅ **Os 10 agentes só aparecem/rodam** depois de: (2) as 3 migrations aplicadas na ordem, (3) o
> `seed_agents.sql` rodado, e (4) a `SUPABASE_SERVICE_ROLE_KEY` configurada no ambiente. Sem o
> service-role key, o motor não consegue gravar e os agentes ficam inertes.

---

## 3. Chaves de IA (5 min)

| Provedor | Onde obter | Usado por |
|---|---|---|
| **OpenAI** | https://platform.openai.com/api-keys (`sk-...`) | os 10 agentes (`task-executor`) |
| **Anthropic** | https://console.anthropic.com → API Keys (`sk-ant-...`) | chat do ORION (`claude-sonnet-4-5`) |

---

## 4. Stripe — billing (10 min)

1. No **Stripe Dashboard**, crie 3 **Products** com um **Price** recorrente cada: **Starter**, **Pro**,
   **Enterprise**. Copie o `price_...` de cada um.
2. Em **Developers → API keys**, copie a **Secret key** (`sk_...`) e a **Publishable key** (`pk_...`).
3. Configure o **webhook** apontando para `https://SEU-DOMINIO/api/stripe/webhook` e copie o
   **Signing secret** (`whsec_...`).

> **Teste primeiro em modo Test** (`sk_test_...` / `pk_test_...`), valide o fluxo, e só então
> troque para as chaves **Live**.

---

## 5. Setar as variáveis na Vercel (10 min)

**Vercel → seu projeto → Settings → Environment Variables** (Production).

### Obrigatórias — banco + agentes

| Variável | Valor |
|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Project URL do Passo 1 |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | anon key do Passo 1 |
| `SUPABASE_SERVICE_ROLE_KEY` | service_role key do Passo 1 (server-only) |
| `OPENAI_API_KEY` | `sk-...` (Passo 3) |
| `ANTHROPIC_API_KEY` | `sk-ant-...` (Passo 3) |

### Obrigatórias — billing (Stripe)

| Variável | Valor |
|---|---|
| `STRIPE_SECRET_KEY` | `sk_...` (server-only) |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` (Passo 4) |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | `pk_...` |
| `NEXT_PUBLIC_STRIPE_PRICE_STARTER` | `price_...` do plano Starter |
| `NEXT_PUBLIC_STRIPE_PRICE_PRO` | `price_...` do plano Pro |
| `NEXT_PUBLIC_STRIPE_PRICE_ENTERPRISE` | `price_...` do plano Enterprise |

### Recomendadas / opcionais

| Variável | Valor |
|---|---|
| `NEXT_PUBLIC_APP_URL` | URL pública do app (ex.: `https://app.alshamglobal.com.br`) |
| `GOOGLE_API_KEY` | se for usar features Google/Gemini |
| `RESEND_API_KEY` | notificações por e-mail |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | social login (opcional) |
| `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` | social login (opcional) |
| `SENTRY_DSN` | monitoramento (opcional) |

> A lista completa (com todas as opcionais) está em `.env.example` na raiz do repo.

---

## 6. Redeploy

Depois de salvar as variáveis, force um **Redeploy** na Vercel (Deployments → ⋯ → Redeploy) para
que as `NEXT_PUBLIC_*` sejam embutidas no build.

---

## 7. Smoke test — provar que está no ar (5–10 min)

- [ ] Abrir o app → login/cadastro funciona (cria `profile`).
- [ ] Abrir a página de **Agentes** → os **10 agentes** aparecem (vindo da tabela `agents`).
- [ ] Disparar uma **task** para um agente → o `task-executor` (OpenAI) processa e grava o resultado.
- [ ] Abrir o chat do **ORION** → responde via Anthropic (`claude-sonnet-4-5`).
- [ ] Ir ao **billing / upgrade de plano** → o Stripe Checkout abre com o `price_...` correto.
- [ ] Pagar em **modo Test** (cartão `4242 4242 4242 4242`) → o webhook confirma e o plano atualiza em `profiles`.

Se os 6 itens passam, **a plataforma está operacional.** 🎉

---

## Troubleshooting rápido

| Sintoma | Causa provável | Correção |
|---|---|---|
| Página de agentes **vazia** | seed não rodado ou migrations fora de ordem | rodar Passo 2 (3 migrations na ordem + `seed_agents.sql`) |
| Agentes existem mas **não executam tasks** | `SUPABASE_SERVICE_ROLE_KEY` ausente | setar a service_role no ambiente + redeploy |
| Erro `relation "agents" does not exist` | migration 1 não aplicada antes das outras | reaplicar na ordem exata do Passo 2 |
| Chat do ORION falha | `ANTHROPIC_API_KEY` ausente/errada | conferir chave `sk-ant-...` |
| Task fica pendente / erro de IA | `OPENAI_API_KEY` ausente/sem crédito | conferir chave e billing na OpenAI |
| Checkout não abre | falta `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` ou o `price_...` do plano | setar as 4 vars públicas do Stripe + redeploy |
| Plano não atualiza após pagar | webhook não configurado / `STRIPE_WEBHOOK_SECRET` errado | conferir endpoint `/api/stripe/webhook` e o `whsec_...` |
| `git commit` falha com `ENOENT ... package.json` | hook `pre-commit` rodando na raiz do monorepo | já corrigido — o hook faz `cd frontend` antes do lint-staged (não use `--no-verify`) |

---

**Checklist de go-live:** Supabase ✅ · 3 migrations na ordem + seed ✅ · OpenAI + Anthropic ✅ ·
Stripe (4 vars públicas + secret + webhook) ✅ · env na Vercel ✅ · redeploy ✅ · smoke test ✅ →
**10 agentes rodando + cobrando.**
