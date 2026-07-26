-- ============================================
-- ALSHAM QUANTUM · HUNTER X.1 — Memória e Missões do Caçador
-- Migration: 20260726_hunter_x1_init
-- ============================================
-- Cria a MEMÓRIA dos irmãos: as 6 tabelas que o HUNTER lê e escreve.
-- Corresponde à FASE 1 do roadmap (agents/hunter/DOSSIE.md, Parte 10).
--
-- >>> DIVERGÊNCIA CANÔNICA DECLARADA (Lei 7 / honestidade) <<<
-- As tabelas hunter_* NÃO seguem o padrão RLS permissivo das demais tabelas
-- do Quantum (USING(true) + GRANT ALL TO anon). Por decreto do dossiê
-- (Partes 4 e 8), a memória dos irmãos NÃO é pública:
--   - anon .......... NEGADO (sem policy, sem grant)
--   - service_role .. ESCREVE (runtime do HUNTER; bypassa RLS)
--   - authenticated . apenas LÊ (o Tribunal/dashboard)
-- A Ronda do SENTINELA valida isso com uma query anônima real (prova dos nove).
-- ============================================

create extension if not exists vector;

-- ============================================
-- 1. A MISSÃO — o que o caçador lê todo dia antes de sair
-- ============================================
create table if not exists public.hunter_missions (
  id            bigint generated always as identity primary key,
  version       int not null,
  status        text not null default 'draft'
                check (status in ('draft','proposed','active','retired')),
  mission_md    text not null,
  sources       jsonb not null,
  scoring_rules jsonb not null,
  created_by    text not null,               -- 'founder' | 'hunter-proposal'
  approved_by   text,
  created_at    timestamptz default now(),
  activated_at  timestamptz,
  unique (version)
);

-- ============================================
-- 2. A CAÇA — cada execução diária
-- ============================================
create table if not exists public.hunter_hunts (
  id            bigint generated always as identity primary key,
  mission_id    bigint references public.hunter_missions(id),
  started_at    timestamptz default now(),
  finished_at   timestamptz,
  status        text default 'running'
                check (status in ('running','done','failed','partial')),
  sources_ok    int default 0,
  sources_fail  int default 0,
  items_seen    int default 0,
  items_kept    int default 0,
  items_queued  int default 0,               -- Lei 8: o que ficou pra amanhã
  report_path   text,
  cost_usd      numeric(8,4),
  notes         text
);

-- ============================================
-- 3. A FILA DE QUARENTENA (Lei 8) — itens brutos não triados hoje
--    (API fora, timeout). Primeira carga da caça seguinte.
-- ============================================
create table if not exists public.hunter_raw_queue (
  id            bigint generated always as identity primary key,
  hunt_id       bigint references public.hunter_hunts(id),
  source        text not null,
  url           text not null,
  raw_payload   jsonb not null,              -- carga inerte (Lei 3)
  queued_reason text not null,               -- 'llm_down','timeout','rate'
  processed     boolean default false,
  created_at    timestamptz default now()
);
create index if not exists idx_hunter_raw_queue_unprocessed
  on public.hunter_raw_queue (processed) where processed = false;

-- ============================================
-- 4. O ACHADO — cada peça de alimento trazida
-- ============================================
create table if not exists public.hunter_findings (
  id            bigint generated always as identity primary key,
  hunt_id       bigint references public.hunter_hunts(id),
  kind          text not null check (kind in
                ('tech','paper','tool','pattern','soul','threat','market')),
  title         text not null,
  url           text not null,
  source        text not null,
  summary_md    text not null,               -- resumo próprio (não cópia)
  relevance     int not null check (relevance between 0 and 100),
  relevance_why text not null,
  single_source boolean default true,
  license       text,                        -- p/ kind tool/tech (LEXIS)
  embedding     vector(1024),
  verdict       text default 'pending' check (verdict in
                ('pending','adopt','watch','discard')),
  verdict_by    text,
  verdict_note  text,
  verdict_at    timestamptz,
  created_at    timestamptz default now()
);
create index if not exists idx_hunter_findings_embedding
  on public.hunter_findings using hnsw (embedding vector_cosine_ops);
create index if not exists idx_hunter_findings_pending
  on public.hunter_findings (verdict) where verdict = 'pending';

-- ============================================
-- 5. AS ARESTAS (semente GraphRAG) — conhecimento como rede, não lista
--    Ex.: (ferramenta X) --[resolve]--> (problema Y) --[via]--> (técnica Z)
-- ============================================
create table if not exists public.hunter_edges (
  id            bigint generated always as identity primary key,
  finding_id    bigint references public.hunter_findings(id),
  subject       text not null,
  relation      text not null,               -- 'resolve','usa','substitui',
                                             -- 'compete_com','depende_de'
  object        text not null,
  confidence    int check (confidence between 0 and 100),
  created_at    timestamptz default now()
);
create index if not exists idx_hunter_edges_subject on public.hunter_edges (subject);
create index if not exists idx_hunter_edges_object  on public.hunter_edges (object);

-- ============================================
-- 6. O CATÁLOGO DE ALMAS — candidatos a novos irmãos
-- ============================================
create table if not exists public.souls_catalog (
  id            bigint generated always as identity primary key,
  finding_id    bigint references public.hunter_findings(id),
  name          text not null,
  origin        text not null,
  capsule_draft jsonb,
  status        text default 'candidate' check (status in
                ('candidate','approved','born','rejected')),
  judged_by     text,
  created_at    timestamptz default now()
);

-- ============================================
-- 7. RLS — memória dos irmãos não é pública (decreto: anon NEGADO)
-- ============================================
alter table public.hunter_missions   enable row level security;
alter table public.hunter_hunts       enable row level security;
alter table public.hunter_raw_queue   enable row level security;
alter table public.hunter_findings    enable row level security;
alter table public.hunter_edges       enable row level security;
alter table public.souls_catalog      enable row level security;

-- anon: negado explicitamente (RLS já bloqueia por default; revoke reforça)
revoke all on public.hunter_missions  from anon;
revoke all on public.hunter_hunts     from anon;
revoke all on public.hunter_raw_queue from anon;
revoke all on public.hunter_findings  from anon;
revoke all on public.hunter_edges     from anon;
revoke all on public.souls_catalog    from anon;

-- authenticated (Tribunal/dashboard): apenas leitura
grant select on public.hunter_missions  to authenticated;
grant select on public.hunter_hunts      to authenticated;
grant select on public.hunter_raw_queue  to authenticated;
grant select on public.hunter_findings   to authenticated;
grant select on public.hunter_edges      to authenticated;
grant select on public.souls_catalog     to authenticated;

-- service_role (runtime do HUNTER): controle total (bypassa RLS de qualquer forma)
grant all on public.hunter_missions  to service_role;
grant all on public.hunter_hunts      to service_role;
grant all on public.hunter_raw_queue  to service_role;
grant all on public.hunter_findings   to service_role;
grant all on public.hunter_edges      to service_role;
grant all on public.souls_catalog     to service_role;

-- policies de leitura para authenticated (nenhuma policy para anon = NEGADO)
create policy "hunter_missions_auth_read"  on public.hunter_missions  for select to authenticated using (true);
create policy "hunter_hunts_auth_read"     on public.hunter_hunts      for select to authenticated using (true);
create policy "hunter_raw_queue_auth_read" on public.hunter_raw_queue  for select to authenticated using (true);
create policy "hunter_findings_auth_read"  on public.hunter_findings   for select to authenticated using (true);
create policy "hunter_edges_auth_read"     on public.hunter_edges      for select to authenticated using (true);
create policy "souls_catalog_auth_read"    on public.souls_catalog     for select to authenticated using (true);

-- ============================================
-- Migration Complete! 🎯
-- A memória dos irmãos nasceu DENTRO do santuário.
-- Próximo: aplicar supabase/seed_hunter_mission_v1.sql (decreto do fundador).
-- ============================================
