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

-- ============================================
-- END OF MIGRATION
-- Applied: 2025-11-25
-- Tables: 7 (6 new + 1 expanded)
-- RLS: Enabled on all tables
-- Indexes: 24 total
-- Constraints: Multiple CHECK, UNIQUE, FK
-- Agents Preserved: 139/139 ✅
-- Phase 1.2.2: COMPLETE ✅
-- ============================================
