-- ============================================
-- ALSHAM QUANTUM - CREATE AGENTS TABLE
-- Migration: 20251223_create_agents_table
-- ============================================
-- Creates the core agents table that the frontend expects
-- ============================================

-- 1. CREATE AGENTS TABLE
CREATE TABLE IF NOT EXISTS public.agents (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('CORE', 'GUARD', 'SPECIALIST', 'ANALYST')),
  status TEXT NOT NULL DEFAULT 'IDLE' CHECK (status IN ('IDLE', 'PROCESSING', 'LEARNING', 'WARNING', 'ERROR')),
  efficiency NUMERIC(5,2) NOT NULL DEFAULT 0.00 CHECK (efficiency >= 0.00 AND efficiency <= 100.00),
  current_task TEXT DEFAULT 'Aguardando comando',
  last_active TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. CREATE INDEXES for performance
CREATE INDEX IF NOT EXISTS idx_agents_role ON public.agents(role);
CREATE INDEX IF NOT EXISTS idx_agents_status ON public.agents(status);
CREATE INDEX IF NOT EXISTS idx_agents_efficiency ON public.agents(efficiency DESC);
CREATE INDEX IF NOT EXISTS idx_agents_last_active ON public.agents(last_active DESC);

-- 3. CREATE TRIGGER for auto-updating updated_at
CREATE TRIGGER update_agents_updated_at
  BEFORE UPDATE ON public.agents
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- 4. ENABLE ROW LEVEL SECURITY
ALTER TABLE public.agents ENABLE ROW LEVEL SECURITY;

-- 5. CREATE RLS POLICIES (Allow public read for now)
CREATE POLICY "Allow public read access on agents"
  ON public.agents FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on agents"
  ON public.agents FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public update on agents"
  ON public.agents FOR UPDATE
  USING (true);

-- 6. GRANT PERMISSIONS
GRANT ALL ON public.agents TO anon, authenticated;

-- ============================================
-- Migration Complete! 🤖
-- Agents table created and ready!
-- ============================================
