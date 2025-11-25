-- ============================================
-- ALSHAM QUANTUM - Phase 1.2 ROLLBACK
-- Rollback for ALL 10 phases (26 tables)
-- Created: 2025-11-25
-- Author: ALSHAM GLOBAL
-- ============================================

-- WARNING: This will DROP all tables

-- ============================================
-- AUTH TRIGGERS ROLLBACK (Phase 2.1)
-- Remove auth trigger and function
-- ============================================

-- Drop trigger first
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Drop function
DROP FUNCTION IF EXISTS public.handle_new_user();
 and remove columns
-- Only run if you need to completely undo ALL Phase 1.2 changes

-- Phase 1.2.10: Drop AI Module tables
DROP TABLE IF EXISTS public.predictions CASCADE;
DROP TABLE IF EXISTS public.training_data CASCADE;
DROP TABLE IF EXISTS public.ai_models CASCADE;

-- Phase 1.2.9: Drop Finance Module tables
DROP TABLE IF EXISTS public.invoices CASCADE;
DROP TABLE IF EXISTS public.transactions CASCADE;

-- Phase 1.2.8: Drop Security Module tables
DROP TABLE IF EXISTS public.audit_log CASCADE;
DROP TABLE IF EXISTS public.security_events CASCADE;

-- Phase 1.2.7: Drop API Module tables
DROP TABLE IF EXISTS public.rate_limits CASCADE;
DROP TABLE IF EXISTS public.api_logs CASCADE;
DROP TABLE IF EXISTS public.api_keys CASCADE;

-- Phase 1.2.6: Drop Gamification Module tables
DROP TABLE IF EXISTS public.leaderboard CASCADE;
DROP TABLE IF EXISTS public.achievements CASCADE;
DROP TABLE IF EXISTS public.user_stats CASCADE;

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
-- All Phase 1.2.1-1.2.10 changes reverted
-- Tables dropped: 26 (25 tables + 5 columns from agents)
-- Database returned to pre-migration state
-- Note: Agent data (139 agents) will remain in reverted agents table
-- ============================================
