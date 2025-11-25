-- ============================================
-- ALSHAM QUANTUM - Phase 1.2 ROLLBACK
-- Rollback for ALL Phase 1.2 tables
-- Created: 2025-11-25
-- Author: ALSHAM GLOBAL
-- ============================================

-- WARNING: This will DROP tables and remove columns
-- Only run if you need to completely undo Phase 1.2.1-1.2.5

-- Phase 1.2.5: Drop Social Module tables
DROP TABLE IF EXISTS public.social_trends CASCADE;
DROP TABLE IF EXISTS public.social_posts CASCADE;

-- Phase 1.2.4: Drop Support Module tables
DROP TABLE IF EXISTS public.ticket_messages CASCADE;
DROP TABLE IF EXISTS public.support_tickets CASCADE;

-- Phase 1.2.3: Drop CRM Module tables
DROP TABLE IF EXISTS public.deal_activities CASCADE;
DROP TABLE IF EXISTS public.deals CASCADE;

-- Phase 1.2.2: Drop Dashboard & Metrics tables
DROP TABLE IF EXISTS public.network_nodes CASCADE;
DROP TABLE IF EXISTS public.system_metrics CASCADE;

-- Phase 1.2.1: Drop Core Tables (in reverse dependency order)
DROP TABLE IF EXISTS public.agent_connections CASCADE;
DROP TABLE IF EXISTS public.agent_logs CASCADE;

-- Revert agents table expansion (remove 5 added columns)
ALTER TABLE public.agents 
  DROP COLUMN IF EXISTS user_id,
  DROP COLUMN IF EXISTS metadata,
  DROP COLUMN IF EXISTS neural_load,
  DROP COLUMN IF EXISTS uptime_seconds,
  DROP COLUMN IF EXISTS version;

-- Note: You may want to keep RLS enabled depending on your setup
-- Uncomment the line below if you want to disable RLS on agents
-- ALTER TABLE public.agents DISABLE ROW LEVEL SECURITY;

DROP TABLE IF EXISTS public.user_sessions CASCADE;
DROP TABLE IF EXISTS public.profiles CASCADE;

-- ============================================
-- END OF ROLLBACK
-- All Phase 1.2.1-1.2.5 changes reverted
-- Tables dropped: 13
-- Columns removed from agents: 5
-- ============================================