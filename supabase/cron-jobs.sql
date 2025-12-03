-- ============================================
-- ALSHAM QUANTUM - Cron Jobs Setup
-- Automated tasks using pg_cron extension
-- ============================================

-- NOTE: This file requires manual execution in Supabase SQL Editor
-- Supabase project URL: https://vktzdrsigrdnemdshcdp.supabase.co

-- ============================================
-- ENABLE pg_cron EXTENSION (if not already enabled)
-- ============================================

CREATE EXTENSION IF NOT EXISTS pg_cron;

-- ============================================
-- CRON JOB 1: Agent Heartbeat (Every 5 minutes)
-- ============================================

-- Remove existing job if it exists
SELECT cron.unschedule('alsham-agent-heartbeat');

-- Schedule agent heartbeat to run every 5 minutes
SELECT cron.schedule(
  'alsham-agent-heartbeat',
  '*/5 * * * *',  -- Every 5 minutes
  $$
  SELECT net.http_post(
    url := 'https://vktzdrsigrdnemdshcdp.supabase.co/functions/v1/agent-heartbeat',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'Authorization', 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZrdHpkcnNpZ3JkbmVtZHNoY2RwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4MzMyODksImV4cCI6MjA2ODQwOTI4OX0.W5n4HbmQqUcGe_tmRPBBfiDhVWcDwK6KF8FrQiR11jc'
    ),
    body := '{}'::jsonb
  ) AS request_id;
  $$
);

-- ============================================
-- CRON JOB 2: System Metrics (Every 10 minutes)
-- ============================================

-- Remove existing job if it exists
SELECT cron.unschedule('alsham-system-metrics');

-- Schedule system metrics collection every 10 minutes
SELECT cron.schedule(
  'alsham-system-metrics',
  '*/10 * * * *',  -- Every 10 minutes
  $$
  SELECT net.http_post(
    url := 'https://vktzdrsigrdnemdshcdp.supabase.co/functions/v1/system-metrics',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'Authorization', 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZrdHpkcnNpZ3JkbmVtZHNoY2RwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4MzMyODksImV4cCI6MjA2ODQwOTI4OX0.W5n4HbmQqUcGe_tmRPBBfiDhVWcDwK6KF8FrQiR11jc'
    ),
    body := '{}'::jsonb
  ) AS request_id;
  $$
);

-- ============================================
-- CRON JOB 3: Agent Task Processor (Every 3 minutes)
-- ============================================

-- Remove existing job if it exists
SELECT cron.unschedule('alsham-task-processor');

-- Schedule task processor every 3 minutes
SELECT cron.schedule(
  'alsham-task-processor',
  '*/3 * * * *',  -- Every 3 minutes
  $$
  SELECT net.http_post(
    url := 'https://vktzdrsigrdnemdshcdp.supabase.co/functions/v1/agent-task-processor',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'Authorization', 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZrdHpkcnNpZ3JkbmVtZHNoY2RwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4MzMyODksImV4cCI6MjA2ODQwOTI4OX0.W5n4HbmQqUcGe_tmRPBBfiDhVWcDwK6KF8FrQiR11jc'
    ),
    body := '{}'::jsonb
  ) AS request_id;
  $$
);

-- ============================================
-- CRON JOB 4: Cleanup Old Logs (Daily at 2 AM)
-- ============================================

-- Remove existing job if it exists
SELECT cron.unschedule('alsham-cleanup-logs');

-- Schedule cleanup of old logs daily at 2 AM
SELECT cron.schedule(
  'alsham-cleanup-logs',
  '0 2 * * *',  -- Daily at 2 AM
  $$
  DELETE FROM public.system_logs
  WHERE timestamp < NOW() - INTERVAL '30 days';

  DELETE FROM public.agent_logs
  WHERE created_at < NOW() - INTERVAL '30 days';
  $$
);

-- ============================================
-- VERIFY CRON JOBS
-- ============================================

-- View all scheduled cron jobs
SELECT * FROM cron.job;

-- View cron job run history (last 10 runs)
SELECT * FROM cron.job_run_details
ORDER BY start_time DESC
LIMIT 10;

-- ============================================
-- MANUAL CRON JOB MANAGEMENT
-- ============================================

-- To manually run a job (for testing):
-- SELECT cron.schedule('job_name', '* * * * *', 'SELECT 1');

-- To unschedule a job:
-- SELECT cron.unschedule('job_name');

-- To view active jobs:
-- SELECT * FROM cron.job;

-- To view job execution history:
-- SELECT * FROM cron.job_run_details WHERE jobid = [job_id] ORDER BY start_time DESC;

-- ============================================
-- Cron Jobs Setup Complete! ⏰
-- ============================================

/*
SUMMARY OF SCHEDULED JOBS:

1. alsham-agent-heartbeat
   - Frequency: Every 5 minutes
   - Purpose: Update agent status and efficiency

2. alsham-system-metrics
   - Frequency: Every 10 minutes
   - Purpose: Collect system health metrics

3. alsham-task-processor
   - Frequency: Every 3 minutes
   - Purpose: Process agent tasks and interactions

4. alsham-cleanup-logs
   - Frequency: Daily at 2 AM
   - Purpose: Remove logs older than 30 days
*/
