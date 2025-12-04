-- ============================================
-- ALSHAM QUANTUM - AGENT AUTO-EVOLUTION SYSTEM
-- Migration: 20251204_agent_evolution_system
-- ============================================
-- Adiciona capacidade de auto-evolução aos agents usando Claude API
-- ============================================

-- 1. ADD EVOLUTION FIELDS TO AGENTS TABLE
ALTER TABLE public.agents
  ADD COLUMN IF NOT EXISTS system_prompt TEXT DEFAULT 'You are an AI agent assistant designed to help with CRM tasks. Be helpful, accurate, and professional.',
  ADD COLUMN IF NOT EXISTS evolution_count INTEGER DEFAULT 0,
  ADD COLUMN IF NOT EXISTS last_evolved_at TIMESTAMPTZ;

-- 2. CREATE EVOLUTION_PROPOSALS TABLE
CREATE TABLE IF NOT EXISTS public.evolution_proposals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id TEXT NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  current_prompt TEXT NOT NULL,
  proposed_prompt TEXT NOT NULL,
  analysis JSONB NOT NULL DEFAULT '{}'::JSONB,
  -- analysis structure:
  -- {
  --   "weaknesses": ["weakness1", "weakness2"],
  --   "improvements": ["improvement1", "improvement2"],
  --   "expected_gain": "10-15%",
  --   "confidence": "high"
  -- }
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'merged')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. CREATE AGENT_METRICS TABLE (para tracking de performance)
CREATE TABLE IF NOT EXISTS public.agent_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id TEXT NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  metric_date DATE NOT NULL DEFAULT CURRENT_DATE,
  requests_processed INTEGER DEFAULT 0,
  requests_successful INTEGER DEFAULT 0,
  requests_failed INTEGER DEFAULT 0,
  avg_processing_time_ms INTEGER DEFAULT 0,
  success_rate NUMERIC(5,2) DEFAULT 0.00,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(agent_id, metric_date)
);

-- 4. ADD AGENT_ID TO REQUESTS TABLE (se não existir)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'requests' AND column_name = 'agent_id'
  ) THEN
    ALTER TABLE public.requests ADD COLUMN agent_id TEXT REFERENCES public.agents(id);
  END IF;
END $$;

-- 5. ADD PROCESSING TIME TO REQUESTS (para métricas)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'requests' AND column_name = 'processing_time_ms'
  ) THEN
    ALTER TABLE public.requests ADD COLUMN processing_time_ms INTEGER;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'requests' AND column_name = 'error_message'
  ) THEN
    ALTER TABLE public.requests ADD COLUMN error_message TEXT;
  END IF;
END $$;

-- 6. CREATE INDEXES for performance
CREATE INDEX IF NOT EXISTS idx_evolution_proposals_agent_id ON public.evolution_proposals(agent_id);
CREATE INDEX IF NOT EXISTS idx_evolution_proposals_status ON public.evolution_proposals(status);
CREATE INDEX IF NOT EXISTS idx_evolution_proposals_created ON public.evolution_proposals(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_agent_metrics_agent_id ON public.agent_metrics(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_metrics_date ON public.agent_metrics(metric_date DESC);

CREATE INDEX IF NOT EXISTS idx_requests_agent_id ON public.requests(agent_id);

-- 7. CREATE TRIGGER for evolution_proposals updated_at
CREATE TRIGGER update_evolution_proposals_updated_at
  BEFORE UPDATE ON public.evolution_proposals
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_metrics_updated_at
  BEFORE UPDATE ON public.agent_metrics
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- 8. ENABLE ROW LEVEL SECURITY
ALTER TABLE public.evolution_proposals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_metrics ENABLE ROW LEVEL SECURITY;

-- 9. CREATE RLS POLICIES (Allow public read for now)
CREATE POLICY "Allow public read access on evolution_proposals"
  ON public.evolution_proposals FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on evolution_proposals"
  ON public.evolution_proposals FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public update on evolution_proposals"
  ON public.evolution_proposals FOR UPDATE
  USING (true);

CREATE POLICY "Allow public read access on agent_metrics"
  ON public.agent_metrics FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on agent_metrics"
  ON public.agent_metrics FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public update on agent_metrics"
  ON public.agent_metrics FOR UPDATE
  USING (true);

-- 10. GRANT PERMISSIONS
GRANT ALL ON public.evolution_proposals TO anon, authenticated;
GRANT ALL ON public.agent_metrics TO anon, authenticated;

-- 11. CREATE FUNCTION TO UPDATE AGENT METRICS (chamado após cada request)
CREATE OR REPLACE FUNCTION update_agent_daily_metrics()
RETURNS TRIGGER AS $$
DECLARE
  today DATE := CURRENT_DATE;
  proc_time INTEGER := COALESCE(NEW.processing_time_ms, 0);
  is_success BOOLEAN := (NEW.status = 'completed');
  is_failed BOOLEAN := (NEW.status = 'failed');
BEGIN
  -- Só atualizar se o request tem agent_id
  IF NEW.agent_id IS NULL THEN
    RETURN NEW;
  END IF;

  -- Inserir ou atualizar métricas do dia
  INSERT INTO public.agent_metrics (
    agent_id,
    metric_date,
    requests_processed,
    requests_successful,
    requests_failed,
    avg_processing_time_ms
  ) VALUES (
    NEW.agent_id,
    today,
    1,
    CASE WHEN is_success THEN 1 ELSE 0 END,
    CASE WHEN is_failed THEN 1 ELSE 0 END,
    proc_time
  )
  ON CONFLICT (agent_id, metric_date) DO UPDATE SET
    requests_processed = agent_metrics.requests_processed + 1,
    requests_successful = agent_metrics.requests_successful + CASE WHEN is_success THEN 1 ELSE 0 END,
    requests_failed = agent_metrics.requests_failed + CASE WHEN is_failed THEN 1 ELSE 0 END,
    avg_processing_time_ms = (
      (agent_metrics.avg_processing_time_ms * agent_metrics.requests_processed + proc_time)
      / (agent_metrics.requests_processed + 1)
    )::INTEGER,
    success_rate = (
      (agent_metrics.requests_successful + CASE WHEN is_success THEN 1 ELSE 0 END)::NUMERIC
      / (agent_metrics.requests_processed + 1)::NUMERIC * 100
    ),
    updated_at = NOW();

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 12. CREATE TRIGGER ON REQUESTS TO UPDATE METRICS
DROP TRIGGER IF EXISTS trigger_update_agent_metrics ON public.requests;
CREATE TRIGGER trigger_update_agent_metrics
  AFTER UPDATE OF status ON public.requests
  FOR EACH ROW
  WHEN (NEW.status IN ('completed', 'failed'))
  EXECUTE FUNCTION update_agent_daily_metrics();

-- ============================================
-- Migration Complete! 🧬
-- Agents can now evolve automatically!
-- ============================================
