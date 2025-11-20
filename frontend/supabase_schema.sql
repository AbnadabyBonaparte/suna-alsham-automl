
-- 1. TABELA DE AGENTES (SENTINELAS)
create table public.agents (
  id uuid not null default gen_random_uuid (),
  name text not null,
  role text not null,
  status text not null default 'idle'::text, 
  battery integer not null default 100,
  tasks_completed integer not null default 0,
  last_active timestamp with time zone null default now(),
  constraint agents_pkey primary key (id)
);

-- 2. TABELA DE LOGS (THE MATRIX)
create table public.system_logs (
  id uuid not null default gen_random_uuid (),
  timestamp timestamp with time zone not null default now(),
  level text not null, 
  message text not null,
  source text not null, 
  constraint system_logs_pkey primary key (id)
);

-- 3. INSERIR DADOS INICIAIS (SEED)
insert into public.agents (name, role, status, battery, tasks_completed) values
  ('Alpha-01', 'Orchestrator', 'active', 98, 1402),
  ('Beta-Construct', 'Builder', 'active', 85, 890),
  ('Gamma-Ray', 'Security', 'warning', 45, 300),
  ('Delta-Flow', 'Analyst', 'idle', 100, 0),
  ('Omega-Prime', 'Core', 'active', 99, 50000);

insert into public.system_logs (level, message, source) values
  ('INFO', 'ALSHAM QUANTUM v11.0 Initialization Sequence Started', 'KERNEL'),
  ('WARN', 'Network latency detected in Sector 7', 'NET_WATCH'),
  ('INFO', 'Connection to Neural Nexus established', 'CORE');
