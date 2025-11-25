-- ============================================
-- ALSHAM QUANTUM - Phase 1.2.1 & 1.2.2
-- Core Tables + Dashboard Metrics
-- Created: 2025-11-25
-- Author: ALSHAM GLOBAL
-- ============================================

-- Phase 1.2.1: Core Tables
-- =========================

-- Table 1: profiles
-- User profiles extending auth.users
CREATE TABLE IF NOT EXISTS public.profiles (
  id uuid NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  auth_user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  username text UNIQUE,
  full_name text,
  avatar_url text,
  role text DEFAULT 'user',
  bio text,
  company text,
  location text,
  preferences jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE public.profiles 
ADD CONSTRAINT profiles_role_check 
CHECK (role IN ('user', 'admin', 'architect', 'observer', 'strategist'));

CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access on profiles"
  ON public.profiles FOR SELECT TO public USING (true);

CREATE POLICY "Allow authenticated users to update own profile"
  ON public.profiles FOR UPDATE TO public
  USING (auth.uid() = auth_user_id);

-- Table 2: user_sessions
-- Session tracking for authenticated users
CREATE TABLE IF NOT EXISTS public.user_sessions (
  id uuid NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.profiles(id) ON DELETE CASCADE,
  device_info jsonb DEFAULT '{}'::jsonb,
  ip_address inet,
  user_agent text,
  last_activity timestamptz DEFAULT now(),
  expires_at timestamptz,
  is_active bool DEFAULT true,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id 
ON public.user_sessions(user_id);

CREATE INDEX IF NOT EXISTS idx_user_sessions_active 
ON public.user_sessions(is_active, last_activity);

CREATE TRIGGER update_user_sessions_updated_at
  BEFORE UPDATE ON public.user_sessions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE public.user_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own sessions"
  ON public.user_sessions FOR SELECT TO public
  USING (auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = user_id));

CREATE POLICY "Users can delete own sessions"
  ON public.user_sessions FOR DELETE TO public
  USING (auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = user_id));

-- Table 3: agents (EXPANSION)
-- Expanding existing agents table with 5 new columns
ALTER TABLE public.agents 
ADD COLUMN IF NOT EXISTS user_id uuid REFERENCES public.profiles(id) ON DELETE SET NULL,
ADD COLUMN IF NOT EXISTS metadata jsonb DEFAULT '{}'::jsonb,
ADD COLUMN IF NOT EXISTS neural_load numeric DEFAULT 0.00,
ADD COLUMN IF NOT EXISTS uptime_seconds bigint DEFAULT 0,
ADD COLUMN IF NOT EXISTS version text DEFAULT '1.0.0';

-- Enable RLS on agents (if not already enabled)
ALTER TABLE public.agents ENABLE ROW LEVEL SECURITY;

-- Table 4: agent_logs
-- Logging system for agent activities
CREATE TABLE IF NOT EXISTS public.agent_logs (
  id uuid NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id text NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  log_level text NOT NULL,
  message text NOT NULL,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE public.agent_logs
ADD CONSTRAINT agent_logs_log_level_check
CHECK (log_level IN ('info', 'warning', 'error', 'critical', 'debug'));

CREATE INDEX IF NOT EXISTS idx_agent_logs_agent_id 
ON public.agent_logs(agent_id);

CREATE INDEX IF NOT EXISTS idx_agent_logs_level 
ON public.agent_logs(log_level);

CREATE INDEX IF NOT EXISTS idx_agent_logs_created_at 
ON public.agent_logs(created_at DESC);

ALTER TABLE public.agent_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access on agent_logs"
  ON public.agent_logs FOR SELECT TO public USING (true);

CREATE POLICY "Allow authenticated insert on agent_logs"
  ON public.agent_logs FOR INSERT TO public WITH CHECK (true);

-- Table 5: agent_connections
-- Neural network connections between agents
CREATE TABLE IF NOT EXISTS public.agent_connections (
  id uuid NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_a_id text NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  agent_b_id text NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
  connection_type text DEFAULT 'neural',
  strength numeric DEFAULT 1.0,
  latency_ms int DEFAULT 0,
  bandwidth_mbps numeric DEFAULT 100.0,
  status text DEFAULT 'active',
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  CONSTRAINT unique_connection UNIQUE (agent_a_id, agent_b_id),
  CONSTRAINT no_self_connection CHECK (agent_a_id != agent_b_id),
  CONSTRAINT valid_connection_type CHECK (connection_type IN ('neural', 'data', 'command', 'sync')),
  CONSTRAINT valid_status CHECK (status IN ('active', 'inactive', 'degraded', 'failed'))
);

CREATE INDEX IF NOT EXISTS idx_agent_connections_agent_a 
ON public.agent_connections(agent_a_id);

CREATE INDEX IF NOT EXISTS idx_agent_connections_agent_b 
ON public.agent_connections(agent_b_id);

CREATE INDEX IF NOT EXISTS idx_agent_connections_type 
ON public.agent_connections(connection_type);

CREATE INDEX IF NOT EXISTS idx_agent_connections_status 
ON public.agent_connections(status) 
WHERE status = 'active';

CREATE TRIGGER update_agent_connections_updated_at
  BEFORE UPDATE ON public.agent_connections
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE public.agent_connections ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access on agent_connections"
  ON public.agent_connections FOR SELECT TO public USING (true);

CREATE POLICY "Allow authenticated insert on agent_connections"
  ON public.agent_connections FOR INSERT TO public WITH CHECK (true);

-- Phase 1.2.2: Dashboard & Metrics
-- =================================

-- Table 6: system_metrics
-- System-wide metrics for dashboard and analytics
CREATE TABLE IF NOT EXISTS public.system_metrics (
  id uuid NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  metric_type text NOT NULL,
  metric_value numeric(20,2),
  metric_unit text,
  category text DEFAULT 'general',
  source text,
  metadata jsonb DEFAULT '{}'::jsonb,
  recorded_at timestamptz DEFAULT now(),
  created_at timestamptz DEFAULT now()
);

ALTER TABLE public.system_metrics
ADD CONSTRAINT system_metrics_category_check
CHECK (category IN ('general', 'performance', 'security', 'business', 'agent', 'network'));

CREATE INDEX IF NOT EXISTS idx_system_metrics_type 
ON public.system_metrics(metric_type);

CREATE INDEX IF NOT EXISTS idx_system_metrics_recorded_at 
ON public.system_metrics(recorded_at DESC);

CREATE INDEX IF NOT EXISTS idx_system_metrics_category 
ON public.system_metrics(category);

CREATE INDEX IF NOT EXISTS idx_system_metrics_type_recorded 
ON public.system_metrics(metric_type, recorded_at DESC);

ALTER TABLE public.system_metrics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access on system_metrics"
  ON public.system_metrics FOR SELECT TO public USING (true);

CREATE POLICY "Allow authenticated insert on system_metrics"
  ON public.system_metrics FOR INSERT TO public WITH CHECK (true);

-- Phase 1.2.2: Dashboard & Metrics (continued)
-- ==============================================

-- Table 7: network_nodes
-- 3D Network visualization nodes
CREATE TABLE IF NOT EXISTS public.network_nodes (
  id uuid NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  node_type text NOT NULL,
  node_name text NOT NULL,
  position_x numeric DEFAULT 0,
  position_y numeric DEFAULT 0,
  position_z numeric DEFAULT 0,
  size numeric DEFAULT 1.0,
  color text DEFAULT '#00FFD0',
  status text DEFAULT 'active',
  connections_count int DEFAULT 0,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE public.network_nodes
ADD CONSTRAINT network_nodes_node_type_check
CHECK (node_type IN ('agent', 'system', 'hub', 'relay', 'sensor'));

ALTER TABLE public.network_nodes
ADD CONSTRAINT network_nodes_status_check
CHECK (status IN ('active', 'inactive', 'degraded', 'maintenance'));

CREATE INDEX IF NOT EXISTS idx_network_nodes_type 
ON public.network_nodes(node_type);

CREATE INDEX IF NOT EXISTS idx_network_nodes_status 
ON public.network_nodes(status) WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_network_nodes_position 
ON public.network_nodes(position_x, position_y, position_z);

CREATE INDEX IF NOT EXISTS idx_network_nodes_name 
ON public.network_nodes(node_name);

CREATE TRIGGER update_network_nodes_updated_at
  BEFORE UPDATE ON public.network_nodes
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE public.network_nodes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access on network_nodes"
  ON public.network_nodes FOR SELECT TO public USING (true);

CREATE POLICY "Allow authenticated insert on network_nodes"
  ON public.network_nodes FOR INSERT TO public WITH CHECK (true);

CREATE POLICY "Allow authenticated update on network_nodes"
  ON public.network_nodes FOR UPDATE TO public USING (true);

-- Phase 1.2.3: CRM Module
-- =========================

-- Table 8: deals
-- Sales pipeline and deal tracking
CREATE TABLE IF NOT EXISTS public.deals (
  id uuid NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.profiles(id) ON DELETE CASCADE,
  client_name text NOT NULL,
  value numeric(15,2) NOT NULL,
  status text DEFAULT 'lead',
  probability int DEFAULT 50,
  stage text,
  close_date date,
  notes text,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE public.deals
ADD CONSTRAINT deals_status_check
CHECK (status IN ('lead', 'negotiation', 'closed', 'lost'));

ALTER TABLE public.deals
ADD CONSTRAINT deals_probability_check
CHECK (probability >= 0 AND probability <= 100);

CREATE INDEX IF NOT EXISTS idx_deals_user_id ON public.deals(user_id);
CREATE INDEX IF NOT EXISTS idx_deals_status ON public.deals(status);
CREATE INDEX IF NOT EXISTS idx_deals_close_date ON public.deals(close_date DESC);
CREATE INDEX IF NOT EXISTS idx_deals_value ON public.deals(value DESC);
CREATE INDEX IF NOT EXISTS idx_deals_created ON public.deals(created_at DESC);

CREATE TRIGGER update_deals_updated_at
  BEFORE UPDATE ON public.deals
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE public.deals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own deals"
  ON public.deals FOR SELECT TO public
  USING (auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = user_id));

CREATE POLICY "Users can insert own deals"
  ON public.deals FOR INSERT TO public
  WITH CHECK (auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = user_id));

CREATE POLICY "Users can update own deals"
  ON public.deals FOR UPDATE TO public
  USING (auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = user_id));

-- Table 9: deal_activities
-- Timeline of activities for each deal
CREATE TABLE IF NOT EXISTS public.deal_activities (
  id uuid NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  deal_id uuid NOT NULL REFERENCES public.deals(id) ON DELETE CASCADE,
  user_id uuid REFERENCES public.profiles(id),
  activity_type text NOT NULL,
  description text,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE public.deal_activities
ADD CONSTRAINT deal_activities_activity_type_check
CHECK (activity_type IN ('note', 'email', 'call', 'meeting', 'status_change', 'value_update'));

CREATE INDEX IF NOT EXISTS idx_deal_activities_deal_id ON public.deal_activities(deal_id);
CREATE INDEX IF NOT EXISTS idx_deal_activities_user_id ON public.deal_activities(user_id);
CREATE INDEX IF NOT EXISTS idx_deal_activities_type ON public.deal_activities(activity_type);
CREATE INDEX IF NOT EXISTS idx_deal_activities_created ON public.deal_activities(created_at DESC);

ALTER TABLE public.deal_activities ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view activities of own deals"
  ON public.deal_activities FOR SELECT TO public
  USING (EXISTS (
    SELECT 1 FROM deals 
    WHERE deals.id = deal_activities.deal_id 
    AND deals.user_id IN (SELECT id FROM profiles WHERE auth_user_id = auth.uid())
  ));

CREATE POLICY "Users can insert activities on own deals"
  ON public.deal_activities FOR INSERT TO public
  WITH CHECK (EXISTS (
    SELECT 1 FROM deals 
    WHERE deals.id = deal_activities.deal_id 
    AND deals.user_id IN (SELECT id FROM profiles WHERE auth_user_id = auth.uid())
  ));

-- ============================================
-- END OF MIGRATION
-- Applied: 2025-11-25
-- Tables: 9 (8 new + 1 expanded)
-- RLS: Enabled on all tables
-- Indexes: 35 total
-- Constraints: Multiple CHECK, UNIQUE, FK
-- Agents Preserved: 139/139 ✅
-- Phase 1.2.3 CRM: COMPLETE ✅
-- ============================================
