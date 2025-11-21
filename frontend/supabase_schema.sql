-- ============================================
-- ALSHAM QUANTUM v12 - Supabase Schema
-- ============================================

-- 1. ENABLE ROW LEVEL SECURITY
alter table if exists public.agents enable row level security;
alter table if exists public.system_logs enable row level security;

-- 2. DROP EXISTING TABLES (Clean slate)
drop table if exists public.agents cascade;
drop table if exists public.system_logs cascade;

-- 3. CREATE AGENTS TABLE
create table public.agents (
  id text primary key,
  name text not null,
  role text not null check (role in ('CORE', 'SPECIALIST', 'GUARD', 'ANALYST')),
  status text not null default 'IDLE' check (status in ('ACTIVE', 'IDLE', 'PROCESSING', 'WARNING', 'LEARNING')),
  efficiency numeric(5,2) not null default 100.00 check (efficiency >= 0 and efficiency <= 100),
  current_task text not null default 'Aguardando comando',
  last_active text not null default 'Now',
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- 4. CREATE SYSTEM LOGS TABLE
create table public.system_logs (
  id uuid primary key default gen_random_uuid(),
  timestamp timestamp with time zone not null default now(),
  level text not null check (level in ('INFO', 'WARN', 'ERROR', 'SUCCESS')),
  message text not null,
  source text not null,
  agent_id text references public.agents(id) on delete set null
);

-- 5. ROW LEVEL SECURITY POLICIES (Public read for now, can be restricted later)
create policy "Allow public read access on agents"
  on public.agents for select
  using (true);

create policy "Allow public read access on logs"
  on public.system_logs for select
  using (true);

-- 6. INSERT THE 9 ALSHAM QUANTUM AGENTS
insert into public.agents (id, name, role, status, efficiency, current_task, last_active) values
  ('orc-alpha', 'ORCHESTRA ALPHA', 'CORE', 'ACTIVE', 99.90, 'Sincronizando 5 nós neurais', 'Now'),
  ('rev-hunt', 'REVENUE HUNTER', 'SPECIALIST', 'PROCESSING', 94.20, 'Analisando padrões de compra globais', 'Now'),
  ('sec-guard', 'SECURITY GUARDIAN', 'GUARD', 'ACTIVE', 100.00, 'Varredura de ameaças quânticas', 'Now'),
  ('cont-cre', 'CONTENT CREATOR', 'ANALYST', 'IDLE', 87.15, 'Agregando multicanal', '2m ago'),
  ('mark-pred', 'MARKET PREDICTOR', 'ANALYST', 'WARNING', 76.10, 'Recalculando volatilidade do mercado', '1m ago'),
  ('supp-sent', 'SUPPORT SENTINEL', 'SPECIALIST', 'ACTIVE', 98.30, 'Monitoramento de tickets em tempo real', 'Now'),
  ('dev-mast', 'DEVOPS MASTER', 'CORE', 'ACTIVE', 98.40, 'Otimizando pipeline CI/CD', 'Now'),
  ('data-min', 'DATA MINER', 'ANALYST', 'PROCESSING', 91.40, 'Extração de dados profundos', 'Now'),
  ('net-watch', 'NETWORK WATCHER', 'GUARD', 'ACTIVE', 100.00, 'Ping 2ms - Latência zero', 'Now');

-- 7. INSERT INITIAL SYSTEM LOGS
insert into public.system_logs (level, message, source, agent_id) values
  ('SUCCESS', 'ALSHAM QUANTUM v12.0 Initialization Sequence Started', 'KERNEL', null),
  ('INFO', 'Neural Nexus connection established', 'CORE', 'orc-alpha'),
  ('WARN', 'Market volatility spike detected', 'ANALYST', 'mark-pred'),
  ('INFO', 'Security scan completed - No threats detected', 'GUARD', 'sec-guard'),
  ('SUCCESS', 'All 9 neural units online and operational', 'SYSTEM', null);

-- 8. CREATE FUNCTION TO UPDATE 'updated_at' TIMESTAMP
create or replace function update_updated_at_column()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

-- 9. CREATE TRIGGER FOR AUTO-UPDATE
create trigger update_agents_updated_at
  before update on public.agents
  for each row
  execute function update_updated_at_column();
