-- ============================================
-- ALSHAM QUANTUM 1000% UPGRADE - New Tables
-- Migration: 20251202_create_quantum_tables
-- ============================================

-- 1. CREATE DEALS TABLE
CREATE TABLE IF NOT EXISTS public.deals (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  client_name TEXT NOT NULL,
  value NUMERIC(12,2) NOT NULL DEFAULT 0.00,
  probability INTEGER NOT NULL DEFAULT 0 CHECK (probability >= 0 AND probability <= 100),
  status TEXT NOT NULL DEFAULT 'lead' CHECK (status IN ('lead', 'negotiation', 'closed_won', 'closed_lost')),
  expected_close_date DATE,
  stage TEXT NOT NULL DEFAULT 'discovery' CHECK (stage IN ('discovery', 'qualification', 'proposal', 'negotiation', 'closed')),
  contact_email TEXT,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. CREATE SUPPORT_TICKETS TABLE
CREATE TABLE IF NOT EXISTS public.support_tickets (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
  priority TEXT NOT NULL DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'critical')),
  category TEXT NOT NULL DEFAULT 'general' CHECK (category IN ('technical', 'bug', 'feature_request', 'performance', 'infrastructure', 'documentation', 'general')),
  assigned_to TEXT,
  created_by TEXT NOT NULL,
  tags TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. CREATE SOCIAL_POSTS TABLE
CREATE TABLE IF NOT EXISTS public.social_posts (
  id TEXT PRIMARY KEY,
  platform TEXT NOT NULL CHECK (platform IN ('twitter', 'linkedin', 'facebook', 'instagram')),
  content TEXT NOT NULL,
  author TEXT NOT NULL,
  likes INTEGER NOT NULL DEFAULT 0,
  shares INTEGER NOT NULL DEFAULT 0,
  comments INTEGER NOT NULL DEFAULT 0,
  sentiment_score NUMERIC(3,2) NOT NULL DEFAULT 0.00 CHECK (sentiment_score >= -1.00 AND sentiment_score <= 1.00),
  reach INTEGER NOT NULL DEFAULT 0,
  engagement_rate NUMERIC(5,2) NOT NULL DEFAULT 0.00,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. CREATE TRANSACTIONS TABLE
CREATE TABLE IF NOT EXISTS public.transactions (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL CHECK (type IN ('payment', 'refund', 'subscription', 'credit')),
  amount NUMERIC(12,2) NOT NULL DEFAULT 0.00,
  currency TEXT NOT NULL DEFAULT 'USD',
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed', 'cancelled')),
  customer_id TEXT NOT NULL,
  customer_name TEXT NOT NULL,
  description TEXT,
  payment_method TEXT CHECK (payment_method IN ('credit_card', 'debit_card', 'wire_transfer', 'ach', 'paypal', 'crypto')),
  reference TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. CREATE ACHIEVEMENTS TABLE
CREATE TABLE IF NOT EXISTS public.achievements (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  icon TEXT NOT NULL DEFAULT '🏆',
  rarity TEXT NOT NULL DEFAULT 'common' CHECK (rarity IN ('common', 'uncommon', 'rare', 'epic', 'legendary')),
  points INTEGER NOT NULL DEFAULT 0,
  category TEXT NOT NULL,
  criteria JSONB NOT NULL DEFAULT '{}'::JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. CREATE USER_ACHIEVEMENTS TABLE (for tracking user unlocks)
CREATE TABLE IF NOT EXISTS public.user_achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  achievement_id TEXT NOT NULL REFERENCES public.achievements(id) ON DELETE CASCADE,
  unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, achievement_id)
);

-- 7. CREATE AGENT_LOGS TABLE (for detailed agent activity tracking)
CREATE TABLE IF NOT EXISTS public.agent_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id TEXT NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  event_type TEXT NOT NULL CHECK (event_type IN ('task_start', 'task_complete', 'status_change', 'error', 'metric_update')),
  message TEXT NOT NULL,
  metadata JSONB DEFAULT '{}'::JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 8. CREATE AGENT_INTERACTIONS TABLE (for tracking agent-to-agent communication)
CREATE TABLE IF NOT EXISTS public.agent_interactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  from_agent_id TEXT NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  to_agent_id TEXT NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  interaction_type TEXT NOT NULL CHECK (interaction_type IN ('request', 'response', 'notification', 'alert')),
  message TEXT NOT NULL,
  metadata JSONB DEFAULT '{}'::JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 9. CREATE SYSTEM_METRICS TABLE (for tracking overall system health)
CREATE TABLE IF NOT EXISTS public.system_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  metric_type TEXT NOT NULL CHECK (metric_type IN ('cpu', 'memory', 'disk', 'network', 'health_score')),
  value NUMERIC(10,2) NOT NULL,
  unit TEXT NOT NULL,
  metadata JSONB DEFAULT '{}'::JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 10. CREATE INDEXES for better performance
CREATE INDEX IF NOT EXISTS idx_deals_status ON public.deals(status);
CREATE INDEX IF NOT EXISTS idx_deals_expected_close ON public.deals(expected_close_date);
CREATE INDEX IF NOT EXISTS idx_support_tickets_status ON public.support_tickets(status);
CREATE INDEX IF NOT EXISTS idx_support_tickets_priority ON public.support_tickets(priority);
CREATE INDEX IF NOT EXISTS idx_social_posts_platform ON public.social_posts(platform);
CREATE INDEX IF NOT EXISTS idx_social_posts_created ON public.social_posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON public.transactions(status);
CREATE INDEX IF NOT EXISTS idx_transactions_customer ON public.transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_agent_logs_agent_id ON public.agent_logs(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_logs_timestamp ON public.agent_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_agent_interactions_from ON public.agent_interactions(from_agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_interactions_to ON public.agent_interactions(to_agent_id);
CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp ON public.system_metrics(timestamp DESC);

-- 11. CREATE TRIGGERS for auto-updating 'updated_at' timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_deals_updated_at
  BEFORE UPDATE ON public.deals
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_support_tickets_updated_at
  BEFORE UPDATE ON public.support_tickets
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_social_posts_updated_at
  BEFORE UPDATE ON public.social_posts
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_transactions_updated_at
  BEFORE UPDATE ON public.transactions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_achievements_updated_at
  BEFORE UPDATE ON public.achievements
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- 12. ENABLE ROW LEVEL SECURITY
ALTER TABLE public.deals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.support_tickets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.social_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_interactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.system_metrics ENABLE ROW LEVEL SECURITY;

-- 13. CREATE RLS POLICIES (Allow public read for now)
CREATE POLICY "Allow public read access on deals"
  ON public.deals FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on deals"
  ON public.deals FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public read access on support_tickets"
  ON public.support_tickets FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on support_tickets"
  ON public.support_tickets FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public read access on social_posts"
  ON public.social_posts FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on social_posts"
  ON public.social_posts FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public read access on transactions"
  ON public.transactions FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on transactions"
  ON public.transactions FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public read access on achievements"
  ON public.achievements FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on achievements"
  ON public.achievements FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public read access on user_achievements"
  ON public.user_achievements FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on user_achievements"
  ON public.user_achievements FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public read access on agent_logs"
  ON public.agent_logs FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on agent_logs"
  ON public.agent_logs FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public read access on agent_interactions"
  ON public.agent_interactions FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on agent_interactions"
  ON public.agent_interactions FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public read access on system_metrics"
  ON public.system_metrics FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on system_metrics"
  ON public.system_metrics FOR INSERT
  WITH CHECK (true);

-- 14. GRANT PERMISSIONS
GRANT ALL ON public.deals TO anon, authenticated;
GRANT ALL ON public.support_tickets TO anon, authenticated;
GRANT ALL ON public.social_posts TO anon, authenticated;
GRANT ALL ON public.transactions TO anon, authenticated;
GRANT ALL ON public.achievements TO anon, authenticated;
GRANT ALL ON public.user_achievements TO anon, authenticated;
GRANT ALL ON public.agent_logs TO anon, authenticated;
GRANT ALL ON public.agent_interactions TO anon, authenticated;
GRANT ALL ON public.system_metrics TO anon, authenticated;

-- ============================================
-- Migration Complete! 🚀
-- ============================================
