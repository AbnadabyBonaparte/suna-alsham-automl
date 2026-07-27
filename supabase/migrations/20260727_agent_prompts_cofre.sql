-- ============================================================================
-- O COFRE DA ALMA — 2ª camada da tranca
-- Migration: 20260727_agent_prompts_cofre
-- ============================================================================
-- A 1ª tranca (20260727_rls_lockdown_suna_core, PR #51) fechou o ANÔNIMO.
-- Sobrou uma fresta, apontada na própria auditoria do #51:
--
--   usuário LOGADO no plano free ainda lê `public.agents` inteiro — os 139
--   registros, com `metadata` e `system_prompt`. Provado hoje:
--     set role authenticated + jwt de usuário free  ->  139 linhas, metadata visível
--
-- E é exatamente em `metadata.system_prompt` que os prompts iriam morar.
--
-- ── POR QUE (b) E NÃO (a) ────────────────────────────────────────────────────
-- (a) grant por coluna em `agents` foi DESCARTADO com prova: dois hooks do
--     painel usam `.select('*')` (useAgents.ts:21, useRealtimeAgents.ts:36) e
--     em Postgres o `SELECT *` falha INTEIRO se faltar privilégio em UMA coluna.
--     Aplicar (a) hoje derruba o painel.
--
-- (b) tabela separada. Segura porque o motor INTEIRO já roda como service_role:
--       task-executor.ts:7      import { createAdminClient } from '@/lib/supabase/admin'
--       agent-router.ts:5       idem
--       evolution-engine.ts:5   idem
--       metrics-collector.ts:6  idem
--     `createAdminClient` usa SUPABASE_SERVICE_ROLE_KEY. Nenhum caminho do
--     motor depende de anon ou authenticated para ler prompt.
--
-- (b) é ainda melhor que (a) por construção: o cofre não tem grant NENHUM para
-- anon/authenticated e não tem policy alguma. Não existe erro futuro de policy
-- que o exponha — para vazar seria preciso conceder grant de propósito.
-- ============================================================================

create table if not exists public.agent_prompts (
  agent_id       text primary key references public.agents(id) on delete cascade,
  system_prompt  text not null,
  fonte_slug     text,                 -- a pasta da alma: agents/<slug>/
  fonte_arquivo  text,                 -- o arquivo exato de onde saiu
  fonte_linhagem text check (fonte_linhagem in ('skill-claude','notion','manual')),
  atualizado_em  timestamptz not null default now(),
  atualizado_por text not null default 'carga-almas'
);

comment on table public.agent_prompts is
  'COFRE — PI da ALSHAM. Sem grant para anon/authenticated e sem policy: só service_role alcanca. NUNCA expor via PostgREST a cliente.';

alter table public.agent_prompts enable row level security;

-- Zero policy = zero linha para quem não bypassa RLS.
-- Zero grant = barrado antes mesmo da RLS (erro 42501).
revoke all on public.agent_prompts from public, anon, authenticated;
grant select, insert, update, delete on public.agent_prompts to service_role;

-- Placas na porta errada, para a próxima pessoa não repetir o erro.
comment on column public.agents.metadata is
  'PUBLICO para usuario logado (policy agents_leitura_auth). NAO gravar segredo aqui: use public.agent_prompts.';
comment on column public.agents.system_prompt is
  'PUBLICO para usuario logado. NAO gravar prompt proprietario aqui: use public.agent_prompts.';

-- ============================================================================
-- ⚠️ O QUE ESTA MIGRATION *NÃO* FAZ (Lei 7)
-- ============================================================================
-- A fresta de `agents.metadata` continua ABERTA para usuário logado — só ficou
-- INÓCUA, porque o segredo deixa de morar lá. Fechá-la de fato exige trocar os
-- dois `.select('*')` por lista de colunas e então aplicar grant por coluna.
-- Enquanto isso não acontecer: NÃO gravar prompt proprietário em `agents`.
-- ============================================================================
