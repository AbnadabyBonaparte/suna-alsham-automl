-- ============================================
-- ALSHAM QUANTUM - Phase 1.2.1 & 1.2.2 ROLLBACK
-- Rollback for Core Tables + Dashboard Metrics
-- Created: 2025-11-25
-- Author: ALSHAM GLOBAL
-- ============================================

-- WARNING: This will DROP tables and remove columns
-- Only run if you need to completely undo Phase 1.2.1 & 1.2.2

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

-- Disable RLS on agents if it wasn't enabled before
-- Note: You may want to keep RLS enabled depending on your setup
-- ALTER TABLE public.agents DISABLE ROW LEVEL SECURITY;

DROP TABLE IF EXISTS public.user_sessions CASCADE;
DROP TABLE IF EXISTS public.profiles CASCADE;

-- ============================================
-- END OF ROLLBACK
-- All Phase 1.2.1 & 1.2.2 changes reverted
-- ============================================
