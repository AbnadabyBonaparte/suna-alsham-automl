**DOSSIÊ FORENSE – PROBLEMA DE LOGIN ALSHAM QUANTUM**

1. **Resumo Executivo**
- Owner não consegue acessar `/dashboard` em `quantum.alshamglobal.com.br` após login.
- Auth migrou para modelo server-side (middleware + helper SSR), mas o client ainda usa `@supabase/supabase-js` puro; evidência forte de que o cookie `sb-*-auth-token` não é criado no browser, fazendo o middleware bloquear.
- Este dossiê mapeia fluxo completo, código relevante, envs conhecidos, scripts de teste e próximos passos para isolar se o problema está em Supabase (auth/profiles/RLS) ou no Next (cookies/middleware/helper).

2. **Arquitetura de Auth Atual**
- Login client-side: página `/login` usa `AuthContext.signIn` → `supabase.auth.signInWithPassword` → `router.push('/dashboard')`.
- Middleware (`src/middleware.ts`): bloqueia `/dashboard*` se não houver cookie `sb-*-auth-token`, exceto quando `NEXT_PUBLIC_DEV_MODE=true`.
- Server helper (`requireDashboardAccess`): via `@supabase/ssr`, lê sessão, carrega `profiles(id=session.user.id)` e aplica regra founder/enterprise/active. Redireciona para `/login`, `/onboarding` ou `/pricing`.
- Dashboard layout: Server Component chama helper e injeta props no `DashboardShell` client-only.
- Diagrama textual:
  - Cliente → `signInWithPassword` (Supabase) → sessão armazenada (localStorage; sem cookie) → `router.push('/dashboard')`
  - Middleware → procura cookie `sb-*-auth-token` → se ausente, redireciona `/login`
  - Server `/dashboard` → `requireDashboardAccess()` → `supabase.auth.getSession()` via cookies → `profiles` → regra de acesso → `/dashboard` ou redirect (`/onboarding`/`/pricing`)

3. **Ambientes e Variáveis de Ambiente**
- Uso no código:
  - `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY`: usados em client e server (`AuthContext`, `supabase.ts`, `requireDashboardAccess`, APIs).
  - `SUPABASE_SERVICE_ROLE_KEY`: usado em `supabase-admin.ts` (server) e **pior** em `lib/lazy-clients.ts` (fallback no browser), risco de vazamento se definido em builds client.
  - `NEXT_PUBLIC_DEV_MODE`: bypass total no middleware e mocks em AuthContext/useSubscription.
- Estado local conhecido:
  - `.env.local` não fornecido; exemplos em `frontend/env.example` e `frontend/dev.env.example` (placeholders).
- Vercel (`alsham-quantum`): **não executado** (`vercel env ls`) por falta de credenciais; precisa ser rodado pelo owner.
- Supabase project_ref: **não confirmado** aqui; scripts de dump sugerem projeto “suna-core”, mas requer checagem via CLI/service role.
- Tabela sugerida (preencher ao rodar comandos):

| Ambiente | URL Supabase | ANON key (prefixo) | project_ref | Observações |
| --- | --- | --- | --- | --- |
| Local (.env.local) | ? | ? | ? | Confirmar `.env.local`; evitar expor SERVICE_ROLE no client |
| Vercel Dev | ? | ? | ? | Rodar `vercel env ls --environment=development` |
| Vercel Preview | ? | ? | ? | Rodar `vercel env ls --environment=preview` |
| Vercel Prod | ? | ? | ? | Rodar `vercel env ls --environment=production` |

4. **Estado do Supabase**
- Policies esperadas (dump `scripts/supabase-dump/05-rls-policies.sql`): select próprio (`auth.uid() = id`), founders leem todos (`is_founder()`), update próprio. Conferir no banco real via `pg_policies`.
- Triggers: script `06-triggers.sql` lista triggers (ex.: criação de profile pós-signup); precisa execução real.
- Dados de usuários-chave: sem consulta real. Usar `09-dados-profiles.sql` e `10-dados-auth-users.sql` como modelos de query para verificar `casamondestore@gmail.com` e `abnadabybonaparte@gmail.com` (id, founder_access, subscription_*).
- Redirect allowed: não verificado; checar domínio `https://quantum.alshamglobal.com.br` no painel Supabase.

5. **Fluxo de Execução e Logging**
- Client:
  - Login form (`app/login/page.tsx`) chama `signIn` do AuthContext; exibe mensagens de erro mas não loga detalhes no console.
  - AuthContext (`contexts/AuthContext.tsx`) só loga erros ao carregar metadata; não loga erro de `signInWithPassword`.
- Server:
  - Middleware loga ausência de cookie e respeita `NEXT_PUBLIC_DEV_MODE`.
  - `requireDashboardAccess` loga sessão/perfil/hasAccess apenas se `NEXT_PUBLIC_DEV_MODE==='true'`.
- Plano de coleta de evidências (executar em preview):
  1) Setar `NEXT_PUBLIC_DEV_MODE=true`.
  2) Abrir aba anônima → `/login` → logar com `casamondestore@gmail.com`.
  3) Capturar: console do browser (`[AUTH][CLIENT]` se adicionar), cookies `sb-*-auth-token`, e logs Vercel (`[AUTH][DEV] session/profile/hasAccess` do helper, logs de middleware).
  4) Rodar `scripts/test-auth-flow.ts` local com senha real para saber se Supabase autentica.

6. **Hipóteses e Análise Técnica**
- H1 (mais forte): **Cookie Supabase ausente no browser.** Client usa `createClient` de `@supabase/supabase-js` puro, que persiste sessão em localStorage e não grava o cookie `sb-*-auth-token` exigido pelo middleware/server helper. Sinal: middleware só checa cookie, não localStorage. Teste: após login, inspecionar cookies; se ausentes, trocar para `@supabase/ssr` (`createBrowserClient`/`createClientComponentClient`) ou ajustar middleware para aceitar token via header.
- H2: **Mismatch de env/Projeto Supabase.** Se Vercel estiver apontando para outro projeto, o login pode criar sessão válida mas `profiles` não contém o usuário → helper redireciona para `/onboarding`. Teste: `vercel env ls` + `test-auth-flow.ts` + query `profiles`/`auth.users` no project_ref correto.
- H3: **RLS/Triggers desalinhados.** Se policies não forem as esperadas ou profile não for criado, `supabase.from('profiles').eq('id', user.id).single()` falha → redirect `/onboarding`. Teste: queries de policies/triggers/dados usando service role.
- H4: **DEV_MODE ativado inadvertidamente.** Se `NEXT_PUBLIC_DEV_MODE=true` em prod, middleware e helper liberam/bypass, mascarando problemas; se false e cookie faltando, bloqueia sempre. Confirmar env real.

7. **Plano de Ação Sugerido**
- Checar envs Vercel (`vercel env ls` para dev/preview/prod) e `.env.local`; garantir mesma URL/key do Supabase alvo; remover SERVICE_ROLE de variáveis públicas.
- Executar `scripts/test-auth-flow.ts` com senha real para confirmar autenticação Supabase (se falhar, problema é no Supabase/credenciais).
- Verificar cookies após login em produção; se ausentes, migrar client para `@supabase/ssr` (browser client) ou ajustar middleware para aceitar sessão via header; manter helper SSR para regra de acesso.
- Validar policies/triggers/dados em Supabase via scripts de dump (05, 06, 09, 10, 16); garantir profile 1:1 com `auth.users`.
- Habilitar logging temporário (`NEXT_PUBLIC_DEV_MODE=true` em preview) para capturar `[AUTH][DEV]` e console do browser; documentar.
- Após correções, rodar `npm run build` no `frontend/` e testar fluxo completo (email/password e OAuth) em preview antes de promover.

8. **Anexos**
- Snapshot git: `branch main`, estado sujo com `frontend/scripts/test-auth-flow.ts` e diretório `suna-alsham-automl` não trackeado; últimos commits: `5b5c1db chore(auth): adicionar logs de dev...`, `bf891af chore(supabase): adicionar scripts de dump`, `6e1f74a chore(supabase): alinhar RLS...`, `2bb6698 Merge...`.
- Código relevante:
  - Middleware cookie check:

```45:107:frontend/src/middleware.ts
  const isDevMode = process.env.NEXT_PUBLIC_DEV_MODE === 'true';
  ...
  const hasSupabaseAuthCookie = cookies.some((cookie) =>
    cookie.name.startsWith('sb-') && cookie.name.endsWith('-auth-token'),
  );
  if (!hasSupabaseAuthCookie) {
    const url = req.nextUrl.clone();
    url.pathname = '/login';
    url.searchParams.set('redirect', pathname);
    return NextResponse.redirect(url);
  }
```

  - Helper SSR e regra de acesso:

```50:107:frontend/src/lib/auth/server.ts
export async function requireDashboardAccess(): Promise<DashboardAccess> {
  const supabase = createServerSupabaseClient();
  const { data: { session } } = await supabase.auth.getSession();
  if (!session || !session.user) redirect('/login?redirect=/dashboard');
  const { data: profile, error } = await supabase
    .from('profiles')
    .select('id, username, full_name, avatar_url, subscription_plan, subscription_status, founder_access, billing_cycle, subscription_end, created_at, updated_at')
    .eq('id', user.id)
    .single();
  if (error || !profile) redirect('/onboarding');
  const hasAccess =
    profile.founder_access === true ||
    (profile.subscription_plan === 'enterprise' && profile.subscription_status === 'active') ||
    profile.subscription_status === 'active';
  if (!hasAccess) redirect('/pricing?reason=payment_required');
  return { profile, user, hasFounderAccess, isEnterprise, hasAccess };
}
```

  - AuthContext client-side (sem cookie helper):

```146:200:frontend/src/contexts/AuthContext.tsx
    const signIn = async (email: string, password: string) => {
        const supabase = getSupabaseClient(); // createClient de @supabase/supabase-js (localStorage)
        const { error } = await supabase.auth.signInWithPassword({ email, password });
        if (!error) {
            const { data: { user } } = await supabase.auth.getUser();
            if (user) { const metadata = await loadUserMetadata(user.id); setMetadata(metadata); }
            router.push('/dashboard');
        }
        return { error };
    };
```

  - Login page (fluxo email/password + OAuth):

```112:199:frontend/src/app/login/page.tsx
    const handleEmailLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setStatus('scanning');
        const { error } = await signIn(email, password);
        if (error) { setStatus('denied'); setErrorMessage(error.message || 'Authentication failed'); }
        else { setStatus('success'); /* router.push dentro de signIn */ }
    };
    const handleGoogleLogin = async () => {
        const { data, error } = await supabase.auth.signInWithOAuth({
            provider: 'google',
            options: { redirectTo: `${window.location.origin}/auth/callback` }
        });
        ...
    };
```

  - RLS esperada:

```9:26:frontend/scripts/supabase-dump/05-rls-policies.sql
CREATE POLICY "Users can read own profile" ON public.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Founders can read all profiles" ON public.profiles FOR SELECT USING (is_founder() = true);
CREATE POLICY "Allow authenticated users to update own profile" ON public.profiles FOR UPDATE USING (auth.uid() = id) WITH CHECK (auth.uid() = id);
```

  - Script de teste criado: `frontend/scripts/test-auth-flow.ts` (usa `signInWithPassword`, loga sessão truncada).

9. **Comandos/Scripts úteis**
- Snapshot git: `git status -sb`, `git log -5 --oneline`.
- Env Vercel (owner): `vercel link` → `vercel env ls --environment=production|preview|development`.
- Supabase SQL (service role): executar queries dos arquivos `05-rls-policies.sql`, `06-triggers.sql`, `09-dados-profiles.sql`, `10-dados-auth-users.sql`, `16-fix-rls-profiles.sql`.
- Teste de login isolado: `cd frontend && npx tsx scripts/test-auth-flow.ts` (definir `TEST_SUPABASE_PASSWORD` e, opcionalmente, `TEST_SUPABASE_EMAIL`).

10. **Limitações desta análise**
- Sem acesso às envs Vercel/Supabase reais; não foi possível confirmar project_ref, chaves e policies ativas.
- Não foram coletados logs em produção nem cookies reais; hipóteses baseadas no código atual.

11. **Registro de Execução (08/12/2025)**
- SQL aplicadas no Supabase:
  - Criada função/trigger `handle_new_user` + `on_auth_user_created` para auto-criação de profile no signup (SELECT em `pg_trigger` retornou a trigger ativa).
  - Policies reescritas para tabelas que usavam `auth_user_id` (api_keys, api_logs, deal_activities, deals, invoices, rate_limits, transactions, user_sessions, user_stats, support_tickets, ticket_messages, predictions) passando a usar `auth.uid()`/`user_id`.
  - Policy recursiva de profiles removida e recriada: `Founders can read all profiles` agora usa `(SELECT founder_access FROM profiles WHERE id = auth.uid()) = true`.
- Dados verificados:
  - `auth.users` (casamondestore@gmail.com): id `e85d6aca-d65b-4452-9a84-a7995bf1cda8`, last_sign_in_at 2025-12-08.
  - `profiles` (mesmo id): subscription_plan=enterprise, subscription_status=active, founder_access=true. Totais: 7 users, 7 profiles.
- Teste direto Supabase (browser, supabase-js UMD):
  - `createClient(url, anon).auth.signInWithPassword` retornou sessão com `hasSession: true`, prefixo de token `eyJhbGciOiJI` → Supabase autentica OK com URL/anon/senha corretos.
- Vercel (projeto `alsham-quantum`):
  - Envs configuradas: `NEXT_PUBLIC_SUPABASE_URL=https://vktzdrsigrdnemdshcdp.supabase.co`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` válida, `SUPABASE_SERVICE_ROLE_KEY` setada. Root: `frontend`.
  - Pendente redeploy para que o build atual use essas envs (no browser ainda aparece `NEXT_PUBLIC_DEV_MODE: undefined`).
- Teste de login no app (produção, aba anônima):
  - Nenhuma chamada `auth/v1/token`, nenhum `sb-...` em localStorage/cookies; `NEXT_PUBLIC_DEV_MODE` undefined no console → indica build sem envs injetadas.
  - Conclusão: Supabase está OK; o frontend não está consumindo as envs no deployment atual, portanto não dispara o login.

12. **Próximos passos imediatos**
- Redeploy do projeto `alsham-quantum` em Vercel para aplicar `NEXT_PUBLIC_SUPABASE_URL` e `NEXT_PUBLIC_SUPABASE_ANON_KEY` no bundle (root `frontend`). Depois testar login:
  - Esperado: requisição `POST .../auth/v1/token?grant_type=password` e chave `sb-vktzdrsigrdnemdshcdp-auth-token` no storage.
- Se após redeploy ainda não houver cookie/token, ajustar o client para usar `@supabase/ssr` no browser (ou criar endpoint server-side que seta cookie) ou adaptar o middleware para aceitar sessão via header/token em vez de cookie.

