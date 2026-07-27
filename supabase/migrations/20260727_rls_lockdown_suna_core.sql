-- ============================================================================
-- SUNA-CORE — A TRAVA (RLS lockdown)
-- Migration: 20260727_rls_lockdown_suna_core
-- ============================================================================
-- Fecha a leitura anônima do banco `suna-core` (vktzdrsigrdnemdshcdp).
--
-- MOTIVO (AUDITORIA-QUANTUM-27JUL, §3.2): hoje qualquer pessoa na internet
-- lê as 139 linhas de `public.agents` — inclusive `system_prompt` e `metadata`
-- — com a chave anônima. As 219 almas resgatadas serão carregadas justamente
-- em `metadata.system_prompt`. Sem esta trava, carregar a alma = publicar a alma.
--
-- REFERÊNCIA: padrão do Banco do Universo (casa-bonaparte, ospnhmyjsyysirrithfr):
--   · ZERO policies com USING(true)
--   · policies por papel (anon / authenticated), nunca genéricas
--   · helpers de autorização num schema `private`, fora de `public`
-- Copiado de lá, não inventado.
--
-- NÃO QUEBRA O MOTOR:
--   · as 7 rotas de API do motor usam `supabase-admin` → SUPABASE_SERVICE_ROLE_KEY
--     → papel `service_role`, que BYPASSA RLS por definição. Intocado.
--   · os hooks do dashboard (useAgents, useDashboardStats, useAnalytics,
--     useRealtimeAgents) usam o cliente do navegador COM sessão → papel
--     `authenticated`. Recebem policy de leitura explícita abaixo.
--   · a landing (`/`) e `/pricing` NÃO tocam o banco — verificado. Nada
--     público depende de leitura anônima.
-- ============================================================================

begin;

-- ────────────────────────────────────────────────────────────────────────────
-- 1. SCHEMA `private` — helpers de autorização fora do alcance da API
--    (padrão casa-bonaparte: por isso lá não há alerta de SECURITY DEFINER
--     executável por anon)
-- ────────────────────────────────────────────────────────────────────────────
create schema if not exists private;
revoke all on schema private from anon, authenticated;
grant usage on schema private to service_role;

create or replace function private.is_founder()
returns boolean
language sql
stable
security definer
set search_path = public, pg_temp
as $$
  select coalesce((select founder_access from public.profiles where id = auth.uid()), false)
$$;

revoke all on function private.is_founder() from public, anon;
grant execute on function private.is_founder() to authenticated, service_role;

-- ────────────────────────────────────────────────────────────────────────────
-- 2. AS FUNÇÕES SECURITY DEFINER EXISTENTES
--    Hoje: `anon=X` (executáveis por anônimo) e SEM search_path fixo — as duas
--    metades de uma escalada de privilégio.
--    `public.is_founder()` é MANTIDA (a RLS abaixo e o painel a usam), mas
--    passa a ter search_path fixo e deixa de ser executável por anon.
-- ────────────────────────────────────────────────────────────────────────────
create or replace function public.is_founder()
returns boolean
language sql
stable
security definer
set search_path = public, pg_temp
as $$
  select coalesce((select founder_access from public.profiles where id = auth.uid()), false)
$$;

alter function public.handle_new_user() set search_path = public, pg_temp;
alter function public.log_all_changes() set search_path = public, pg_temp;

revoke all on function public.is_founder()      from public, anon;
revoke all on function public.handle_new_user() from public, anon;
revoke all on function public.log_all_changes() from public, anon;

grant execute on function public.is_founder() to authenticated, service_role;
-- handle_new_user e log_all_changes são TRIGGERS: rodam como definer,
-- não precisam de grant a authenticated.
grant execute on function public.handle_new_user() to service_role;
grant execute on function public.log_all_changes() to service_role;

-- ────────────────────────────────────────────────────────────────────────────
-- 3. RLS LIGADA EM TUDO — inclusive na quantum_audit_log
--    (hoje é o único ERROR dos advisors: `rls_disabled_in_public`)
-- ────────────────────────────────────────────────────────────────────────────
do $$
declare r record;
begin
  for r in
    select c.relname
    from pg_class c
    where c.relnamespace = 'public'::regnamespace
      and c.relkind = 'r'
      and not c.relrowsecurity
  loop
    execute format('alter table public.%I enable row level security', r.relname);
    raise notice 'RLS ligada em public.%', r.relname;
  end loop;
end $$;

-- ────────────────────────────────────────────────────────────────────────────
-- 4. O CORTE — anon perde TUDO em TODAS as tabelas de `public`
--    É a linha que fecha o buraco da auditoria.
-- ────────────────────────────────────────────────────────────────────────────
do $$
declare r record;
begin
  for r in
    select c.relname
    from pg_class c
    where c.relnamespace = 'public'::regnamespace and c.relkind = 'r'
  loop
    execute format('revoke all on public.%I from anon', r.relname);
  end loop;
end $$;

revoke all on all sequences in schema public from anon;
revoke all on all functions in schema public from anon;
revoke usage on schema public from anon;

-- Default para objetos futuros: anon já nasce sem nada.
alter default privileges in schema public revoke all on tables    from anon;
alter default privileges in schema public revoke all on sequences from anon;
alter default privileges in schema public revoke all on functions from anon;

-- ────────────────────────────────────────────────────────────────────────────
-- 5. FORA AS POLICIES `USING(true)` — 25 portas destrancadas com cadeado
--    de enfeite. Removidas antes de recriar as reais.
-- ────────────────────────────────────────────────────────────────────────────
do $$
declare r record;
begin
  for r in
    select schemaname, tablename, policyname
    from pg_policies
    where schemaname = 'public'
      and (qual = 'true' or with_check = 'true')
      -- as policies do HUNTER já nascem corretas (authenticated-only, sem
      -- USING(true)); ficam de fora por segurança
      and tablename not like 'hunter\_%'
      and tablename <> 'souls_catalog'
  loop
    execute format('drop policy if exists %I on public.%I', r.policyname, r.tablename);
    raise notice 'policy USING(true) removida: %.%', r.tablename, r.policyname;
  end loop;
end $$;

-- ────────────────────────────────────────────────────────────────────────────
-- 6. AS POLICIES REAIS
-- ────────────────────────────────────────────────────────────────────────────

-- 6.1 · TABELAS COM DONO (`user_id`): o dono vê e mexe no que é dele.
--       O fundador enxerga tudo. Anônimo não existe aqui.
do $$
declare r record;
begin
  for r in
    select c.relname as t
    from pg_class c
    join information_schema.columns col
      on col.table_schema = 'public' and col.table_name = c.relname
     and col.column_name = 'user_id'
    where c.relnamespace = 'public'::regnamespace and c.relkind = 'r'
      and c.relname not like 'hunter\_%'
  loop
    execute format('drop policy if exists %I on public.%I', r.t || '_dono_rw', r.t);
    execute format($f$
      create policy %I on public.%I
      as permissive for all to authenticated
      using (user_id = (select auth.uid()) or public.is_founder())
      with check (user_id = (select auth.uid()) or public.is_founder())
    $f$, r.t || '_dono_rw', r.t);
    execute format('grant select, insert, update, delete on public.%I to authenticated', r.t);
  end loop;
end $$;

-- 6.2 · `profiles`: o dono é a própria linha (id = auth.uid()).
--       handle_new_user() grava id = auth_user_id = auth.users.id — verificado
--       nos 8 perfis existentes, todos batem.
drop policy if exists profiles_dono_rw on public.profiles;
create policy profiles_dono_rw on public.profiles
  as permissive for all to authenticated
  using (id = (select auth.uid()) or public.is_founder())
  with check (id = (select auth.uid()) or public.is_founder());
grant select, insert, update, delete on public.profiles to authenticated;

-- 6.3 · `hunter_missions` (dono por `created_by`, texto — não é uuid)
drop policy if exists hunter_missions_leitura_auth on public.hunter_missions;

-- 6.4 · CATÁLOGO / SISTEMA (sem coluna de dono): leitura para quem está
--       logado; escrita só pelo service_role (o motor).
--       `agents` está aqui — é o que os hooks do dashboard leem.
do $$
declare r record;
declare tabelas text[] := array[
  'agents','ai_models','agent_connections','agent_interactions','agent_logs',
  'agent_metrics','achievements','audit_trail','containment_actions',
  'emergent_capabilities','evolution_cycles','evolution_proposals',
  'learning_sessions','milestone_tracking','network_nodes','performance_metrics',
  'quantum_brain_state','quantum_tasks','security_logs','social_posts',
  'social_trends','success_criteria','system_logs','system_metrics',
  'training_data','users','validation_results'
];
declare t text;
begin
  foreach t in array tabelas loop
    if exists (select 1 from pg_class c where c.relnamespace='public'::regnamespace and c.relname=t and c.relkind='r') then
      execute format('drop policy if exists %I on public.%I', t || '_leitura_auth', t);
      execute format($f$
        create policy %I on public.%I
        as permissive for select to authenticated
        using (true)
      $f$, t || '_leitura_auth', t);
      execute format('grant select on public.%I to authenticated', t);
      -- escrita: só service_role (que bypassa RLS). authenticated não escreve.
      execute format('revoke insert, update, delete on public.%I from authenticated', t);
    end if;
  end loop;
end $$;

-- 6.5 · `quantum_audit_log`: trilha de auditoria. Só o fundador lê.
drop policy if exists quantum_audit_log_founder on public.quantum_audit_log;
create policy quantum_audit_log_founder on public.quantum_audit_log
  as permissive for select to authenticated
  using (public.is_founder());
grant select on public.quantum_audit_log to authenticated;
revoke insert, update, delete on public.quantum_audit_log from authenticated;

-- ────────────────────────────────────────────────────────────────────────────
-- 7. SERVICE_ROLE — o motor mantém acesso pleno (e bypassa RLS de qualquer forma)
-- ────────────────────────────────────────────────────────────────────────────
grant usage on schema public to service_role;
grant all on all tables    in schema public to service_role;
grant all on all sequences in schema public to service_role;
grant all on all functions in schema public to service_role;
alter default privileges in schema public grant all on tables    to service_role;
alter default privileges in schema public grant all on sequences to service_role;
alter default privileges in schema public grant all on functions to service_role;

-- authenticated precisa enxergar o schema para qualquer policy funcionar
grant usage on schema public to authenticated;

commit;

-- ============================================================================
-- ⚠️ RISCO RESIDUAL DECLARADO (Lei 7) — NÃO resolvido por esta migration
-- ============================================================================
-- Esta trava fecha o ANÔNIMO. Ela NÃO impede que um usuário LOGADO no plano
-- free leia `public.agents.metadata` — e é exatamente ali que as 219 almas
-- serão carregadas.
--
-- O jeito certo seria GRANT por COLUNA (liberar name/role/status/efficiency e
-- reter system_prompt/metadata). NÃO foi feito porque quebraria o painel:
-- `useAgents.ts:21` e `useRealtimeAgents.ts:36` usam `.select('*')`, e em
-- Postgres o `SELECT *` falha inteiro se faltar privilégio em UMA coluna.
--
-- Duas saídas, ambas decisão de dono:
--   (a) trocar os dois `.select('*')` por lista explícita de colunas e então
--       aplicar grant por coluna em `agents`; ou
--   (b) guardar os prompts FORA de `agents`, numa tabela só do fundador.
--
-- Até uma das duas ser feita: NÃO carregar prompt proprietário em
-- `agents.metadata`. A trava do anônimo é necessária, não é suficiente.
-- ============================================================================
