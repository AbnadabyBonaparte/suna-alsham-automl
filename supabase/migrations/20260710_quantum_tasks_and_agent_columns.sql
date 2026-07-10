-- ============================================
-- ALSHAM QUANTUM - QUANTUM_TASKS + AGENT ENGINE COLUMNS
-- Migration: 20260710_quantum_tasks_and_agent_columns
-- ============================================
-- Habilita o motor real de agentes (task-executor):
--  - Adiciona colunas que o engine escreve na tabela agents
--  - Cria a tabela quantum_tasks (métricas de execução)
--  - Alinha o CHECK de status ao enum usado no código
-- ============================================

-- 1. COLUNAS FALTANTES NA TABELA AGENTS
ALTER TABLE public.agents
  ADD COLUMN IF NOT EXISTS neural_load NUMERIC(5,2) NOT NULL DEFAULT 0.00
    CHECK (neural_load >= 0.00 AND neural_load <= 100.00),
  ADD COLUMN IF NOT EXISTS uptime_seconds BIGINT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS version TEXT NOT NULL DEFAULT 'v1.0.0',
  ADD COLUMN IF NOT EXISTS metadata JSONB NOT NULL DEFAULT '{}'::JSONB;

-- 2. TABELA QUANTUM_TASKS (execuções com métricas)
CREATE TABLE IF NOT EXISTS public.quantum_tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id UUID REFERENCES public.requests(id) ON DELETE SET NULL,
  agent_id TEXT NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  input JSONB NOT NULL DEFAULT '{}'::JSONB,
  output JSONB,
  status TEXT NOT NULL DEFAULT 'processing'
    CHECK (status IN ('queued', 'processing', 'completed', 'failed')),
  error_message TEXT,
  execution_time_ms INTEGER,
  tokens_used INTEGER,
  cost_usd NUMERIC(12,6),
  model_used TEXT NOT NULL DEFAULT 'gpt-4o-mini',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_quantum_tasks_agent_id ON public.quantum_tasks(agent_id);
CREATE INDEX IF NOT EXISTS idx_quantum_tasks_request_id ON public.quantum_tasks(request_id);
CREATE INDEX IF NOT EXISTS idx_quantum_tasks_status ON public.quantum_tasks(status);
CREATE INDEX IF NOT EXISTS idx_quantum_tasks_created_at ON public.quantum_tasks(created_at DESC);

-- 3. RLS: leitura pública para dashboards; escrita fica a cargo do service role
ALTER TABLE public.quantum_tasks ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE schemaname = 'public' AND tablename = 'quantum_tasks'
      AND policyname = 'Allow public read access on quantum_tasks'
  ) THEN
    CREATE POLICY "Allow public read access on quantum_tasks"
      ON public.quantum_tasks FOR SELECT USING (true);
  END IF;
END $$;

GRANT SELECT ON public.quantum_tasks TO anon, authenticated;
GRANT ALL ON public.quantum_tasks TO service_role;

-- ============================================
-- Migration Complete! 🧠
-- quantum_tasks pronta; agents com neural_load/metadata/version/uptime.
-- ============================================
