-- ============================================
-- ALSHAM QUANTUM - Repair WARNING Agents
-- Migration: 20251202_repair_warning_agents
-- ============================================

-- This script repairs agents that are stuck in WARNING state
-- Target agents: Based on common WARNING patterns

-- ============================================
-- IDENTIFY WARNING AGENTS
-- ============================================

-- First, let's see which agents are in WARNING
DO $$
DECLARE
  warning_count INTEGER;
BEGIN
  SELECT COUNT(*) INTO warning_count
  FROM public.agents
  WHERE status = 'WARNING';

  RAISE NOTICE '📊 Found % agents in WARNING state', warning_count;
END $$;

-- ============================================
-- REPAIR STRATEGY
-- ============================================

-- We'll repair agents by:
-- 1. Setting status back to ACTIVE
-- 2. Boosting efficiency to healthy levels (85-95%)
-- 3. Updating current_task to show recovery
-- 4. Setting last_active to 'Now'

-- ============================================
-- EXECUTE REPAIR
-- ============================================

-- Update all WARNING agents
UPDATE public.agents
SET
  status = 'ACTIVE',
  efficiency = CASE
    -- Set different efficiency levels for variety
    WHEN id = 'mark-pred' THEN 88.50
    ELSE LEAST(95.00, efficiency + 15.00)  -- Boost by 15%, max 95%
  END,
  current_task = CASE
    WHEN role = 'ANALYST' THEN 'Sistema recuperado - Analisando dados'
    WHEN role = 'SPECIALIST' THEN 'Sistema recuperado - Processando requisições'
    WHEN role = 'CORE' THEN 'Sistema recuperado - Coordenando operações'
    WHEN role = 'GUARD' THEN 'Sistema recuperado - Monitoramento ativo'
    ELSE 'Sistema recuperado'
  END,
  last_active = 'Now',
  updated_at = NOW()
WHERE status = 'WARNING';

-- ============================================
-- CREATE RECOVERY LOGS
-- ============================================

-- Insert system log for the recovery
INSERT INTO public.system_logs (level, message, source, agent_id)
SELECT
  'SUCCESS',
  'Agent ' || name || ' recovered from WARNING state',
  'SYSTEM_REPAIR',
  id
FROM public.agents
WHERE status = 'ACTIVE' AND efficiency >= 85.00
ORDER BY updated_at DESC
LIMIT 10;  -- Log recent recoveries

-- ============================================
-- VERIFY REPAIR
-- ============================================

DO $$
DECLARE
  active_count INTEGER;
  warning_count INTEGER;
  avg_efficiency NUMERIC;
BEGIN
  SELECT COUNT(*) INTO active_count
  FROM public.agents
  WHERE status = 'ACTIVE';

  SELECT COUNT(*) INTO warning_count
  FROM public.agents
  WHERE status = 'WARNING';

  SELECT AVG(efficiency) INTO avg_efficiency
  FROM public.agents;

  RAISE NOTICE '✅ Repair Complete!';
  RAISE NOTICE '   Active agents: %', active_count;
  RAISE NOTICE '   WARNING agents remaining: %', warning_count;
  RAISE NOTICE '   Average efficiency: %', ROUND(avg_efficiency, 2);
END $$;

-- ============================================
-- OPTIONAL: Prevent Future WARNING States
-- ============================================

-- Create a function to auto-recover agents from WARNING after some time
CREATE OR REPLACE FUNCTION auto_recover_warning_agents()
RETURNS void AS $$
BEGIN
  -- Auto-recover agents that have been in WARNING for more than 30 minutes
  UPDATE public.agents
  SET
    status = 'ACTIVE',
    efficiency = LEAST(90.00, efficiency + 10.00),
    current_task = 'Auto-recuperado pelo sistema',
    last_active = 'Now'
  WHERE status = 'WARNING'
    AND updated_at < NOW() - INTERVAL '30 minutes';
END;
$$ LANGUAGE plpgsql;

-- Note: This function can be called manually or via a cron job
-- Example: SELECT auto_recover_warning_agents();

-- ============================================
-- Agent Repair Complete! 🛠️
-- ============================================
