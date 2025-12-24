**MAPA DE INFRA E VARIÁVEIS DE AMBIENTE – ALSHAM QUANTUM**

> Guia definitivo para reconstruir envs em local, Vercel (Dev/Preview/Prod), Supabase e (opcional) GitHub Secrets. Baseado apenas em variáveis presentes no código/repo.

---

## 1. Tabela Mestre de Variáveis

### Core – Supabase / Auth / Dashboard
| Nome | Onde é usada (arquivos principais) | Tipo | Ambientes | Obrigatoriedade | Função / Descrição | Exemplo seguro |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT_PUBLIC_SUPABASE_URL | `src/lib/auth/server.ts`, `middleware.ts`, `contexts/AuthContext.tsx`, `lib/supabase.ts`, `lib/actions.ts`, `app/api/requests/create`, `app/auth/callback`, `scripts/test-auth-flow.ts`, `scripts/seed-demo-mega.ts`, `lib/lazy-clients.ts`, `dashboard/analytics` | public | local, vercel-dev/preview/prod | Crítica (login, dashboard, APIs) | URL do projeto Supabase (mesmo de `auth.users`/`profiles`) | https://<project>.supabase.co |
| NEXT_PUBLIC_SUPABASE_ANON_KEY | mesmas refs acima | public | local, vercel-dev/preview/prod | Crítica | Chave anon Supabase (cliente) | sbp_anon_xxx |
| SUPABASE_SERVICE_ROLE_KEY | `lib/supabase-admin.ts`, `lib/lazy-clients.ts` (cuidado fallback no browser), `app/api/stripe/webhook`, `scripts/seed-demo-mega.ts` | server | local (scripts), vercel (APIs/webhooks) | Crítica para seeds/webhook; não expor | Chave service role do Supabase | sbp_service_role_xxx |
| NEXT_PUBLIC_DEV_MODE | `middleware.ts`, `lib/auth/server.ts`, `contexts/AuthContext.tsx`, `hooks/useSubscription.ts` | public | local, vercel-dev/preview (evitar em prod) | Opcional (bypass/mocks) | Bypass de auth/payment para debug | true/false |
| TEST_SUPABASE_EMAIL | `scripts/test-auth-flow.ts` | server/script | local | Opcional (teste) | Email para script de teste | casamondestore@gmail.com |
| TEST_SUPABASE_PASSWORD | `scripts/test-auth-flow.ts` | server/script | local | Opcional (teste) | Senha para script de teste | (preencher) |

### Pagamentos / Stripe
| Nome | Onde é usada | Tipo | Ambientes | Obrigatoriedade | Função | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY | `lib/stripe.ts` | public | local, vercel-dev/preview/prod | Crítica p/ checkout | Publishable key | pk_test_xxx |
| STRIPE_SECRET_KEY | `app/api/stripe/checkout`, `app/api/stripe/webhook` | server | local, vercel-dev/preview/prod | Crítica | Secret key | sk_test_xxx |
| STRIPE_WEBHOOK_SECRET | `app/api/stripe/webhook` | server | local, vercel-dev/preview/prod | Crítica p/ validar webhook | Assinatura webhook | whsec_xxx |

### IA / Provedores
| Nome | Onde é usada | Tipo | Ambientes | Obrigatoriedade | Função | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| OPENAI_API_KEY | `app/api/quantum/brain/execute`, `lib/process-request-service.ts`, `app/api/process-request` | server | local, vercel-dev/preview/prod | Crítica para features OpenAI | Chave OpenAI | sk-... |
| ANTHROPIC_API_KEY | `app/api/evolution/propose`, `lib/lazy-clients.ts` | server | local, vercel-dev/preview/prod | Opcional (features Anthropic) | Chave Anthropic | sk-ant-... |

### GitHub / Auxiliares
| Nome | Onde é usada | Tipo | Ambientes | Obrigatoriedade | Função | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| GITHUB_TOKEN | `lib/lazy-clients.ts` | server | local/CI | Opcional | Acesso API GitHub (features auxiliares) | ghp_xxx |
| GITHUB_OWNER | `lib/lazy-clients.ts` | server | local/CI | Opcional | Owner para chamadas GitHub | AbnadabyBonaparte |
| GITHUB_REPO | `lib/lazy-clients.ts` | server | local/CI | Opcional | Repo alvo | suna-alsham-automl |

### Diversos / Legado
| Nome | Onde é usada | Tipo | Status | Função | Exemplo |
| --- | --- | --- | --- | --- | --- |
| NEXT_PUBLIC_API_URL / NEXT_PUBLIC_SYSTEM_VERSION / NEXT_PUBLIC_ENV | `repair_connection.py` (legado) | public | Legado (não usar) | Variáveis de conexão/flag antigas | https://api.exemplo.com |
| RESEND_API_KEY, TWITTER_BEARER_TOKEN, CRON_SECRET, ANALYZE | Apenas citadas em doc “ROADMAP” (não no código ativo) | server | Legado | Não configurar a menos que necessário para features futuras | - |

---

## 2. .env.local (mínimo para rodar login/dashboard)
```bash
# .env.local (exemplo seguro)
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sbp_anon_xxx
SUPABASE_SERVICE_ROLE_KEY=sbp_service_role_xxx   # só se rodar webhooks/scripts
NEXT_PUBLIC_DEV_MODE=false                      # opcional; true para bypass em dev
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx   # se testar checkout
STRIPE_SECRET_KEY=sk_test_xxx                    # se testar API checkout
STRIPE_WEBHOOK_SECRET=whsec_xxx                  # se testar webhook (com tunnel)
OPENAI_API_KEY=sk-...                            # se usar features de IA
ANTHROPIC_API_KEY=sk-ant-...                     # opcional
```

---

## 3. Vercel – por ambiente

### Development
- Obrigatórias: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`.
- Recomendadas: `NEXT_PUBLIC_DEV_MODE=true` (apenas dev/preview), `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`.
- Server-only: `STRIPE_WEBHOOK_SECRET`, `SUPABASE_SERVICE_ROLE_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GITHUB_TOKEN` (se usar).
- Nunca expor `SUPABASE_SERVICE_ROLE_KEY` como `NEXT_PUBLIC_`.

### Preview
- Obrigatórias: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`.
- Server-only: `STRIPE_WEBHOOK_SECRET`, `SUPABASE_SERVICE_ROLE_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`.
- Opcional: `NEXT_PUBLIC_DEV_MODE=true` para debug (retirar em produção).

### Production
- Obrigatórias: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`.
- Server-only críticos: `STRIPE_WEBHOOK_SECRET`, `SUPABASE_SERVICE_ROLE_KEY`, `OPENAI_API_KEY` (se usado), `ANTHROPIC_API_KEY` (se usado), `GITHUB_TOKEN` (se usado).
- Não usar `NEXT_PUBLIC_DEV_MODE=true` em produção.

---

## 4. Supabase – alinhamento necessário
- Project URL e anon key: devem casar com `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY`.
- Service role key: usada em webhooks (Stripe), seeds e scripts server-side; nunca expor no browser.
- Redirect URLs a cadastrar (OAuth/auth callback):
  - Produção: `https://quantum.alshamglobal.com.br/auth/callback`
  - Preview: `https://<preview>.vercel.app/auth/callback` (se aplicável)
  - Dev: `http://localhost:3000/auth/callback`
- Policies/trigger já corrigidas:
  - Trigger `on_auth_user_created` cria profile no signup.
  - Profiles: select próprio, founders leem todos (sem recursão), update próprio.
- Dependência: `requireDashboardAccess` espera `profiles.id = auth.users.id`; se faltar profile, redireciona `/onboarding`.

---

## 5. GitHub Secrets (atual)
- Não há `.github/workflows` no repo; nenhum secret em uso.
- Se vier a usar Actions no futuro: típicos `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`, `SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `OPENAI_API_KEY` (conforme pipeline).

---

## 6. Checklists

### Checklist – reconstruir .env.local
- Copiar `frontend/env.example` para `.env.local`.
- Preencher `NEXT_PUBLIC_SUPABASE_URL` e `NEXT_PUBLIC_SUPABASE_ANON_KEY` do projeto correto.
- (Opcional scripts/webhook) `SUPABASE_SERVICE_ROLE_KEY`.
- Stripe (se for testar): `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`.
- IA (se usar): `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`.
- Ajustar `NEXT_PUBLIC_DEV_MODE` (true para bypass em dev, false para fluxo real).

### Checklist – configurar envs no Vercel (Dev/Preview/Prod)
- Adicionar: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`.
- Adicionar Stripe: `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`.
- Adicionar server-only: `SUPABASE_SERVICE_ROLE_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GITHUB_TOKEN` (se usar).
- Em Dev/Preview: `NEXT_PUBLIC_DEV_MODE=true` se precisar de bypass; não usar em Prod.
- Redeploy após salvar envs.

### Checklist – conferir Supabase
- Confirmar URL/keys batendo com envs (anon + service role).
- Verificar Redirect URLs (prod/preview/dev) para `/auth/callback`.
- Conferir trigger `on_auth_user_created` e policies de `profiles`.
- Garantir `profiles.id` existente para usuários ativos.

### Checklist – GitHub Secrets (opcional)
- Se criar Actions: definir `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`, `SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `OPENAI_API_KEY` conforme pipeline.

---

## 7. Notas finais
- Chaves Supabase: anon e service role devem ser do MESMO projeto onde estão `auth.users` e `profiles`.
- Service role nunca deve ser `NEXT_PUBLIC_`; hoje há fallback em `lib/lazy-clients.ts` que usa service role se presente – mantenha essa key apenas em server/edge.
- Se, mesmo com envs corretas e redeploy, não aparecer `auth/v1/token` ou `sb-...` no storage após login, revisar build/envs do Vercel ou ajustar o client para usar `@supabase/ssr` (browser) ou adaptar middleware para aceitar token/Authorization em vez de cookie.

