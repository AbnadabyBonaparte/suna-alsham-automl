-- ============================================
-- ALSHAM QUANTUM - Phase 1.2.1 & 1.2.2 ROLLBACK
-- Rollback for Core Tables + Dashboard Metrics
-- Created: 2025-11-25
-- Author: ALSHAM GLOBAL
-- ============================================

-- WARNING: This will DROP tables and remove columns
-- Only run if you need to completely undo Phase 1.2.1, 1.2.2 & 1.2.3

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

-- Disable RLS on agents if it wasn't enabled before
-- Note: You may want to keep RLS enabled depending on your setup
-- ALTER TABLE public.agents DISABLE ROW LEVEL SECURITY;

DROP TABLE IF EXISTS public.user_sessions CASCADE;
DROP TABLE IF EXISTS public.profiles CASCADE;

-- ============================================
-- END OF ROLLBACK
-- All Phase 1.2.1 & 1.2.2 changes reverted
-- ============================================

-- Phase 1.2.4: Support Module
-- ============================

-- Table 10: support_tickets
CREATE TABLE IF NOT EXISTS public.support_tickets (
  id uuid NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.profiles(id) ON DELETE CASCADE,
  subject text NOT NULL,
  description text,
  status text DEFAULT 'open',
  priority text DEFAULT 'normal',
  sentiment_score numeric(5,2),
  assigned_to uuid REFERENCES public.profiles(id),
  resolved_at timestamptz,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE public.support_tickets
ADD CONSTRAINT support_tickets_status_check
CHECK (status IN ('open', 'in_progress', 'resolved', 'closed'));

ALTER TABLE public.support_tickets
ADD CONSTRAINT support_tickets_priority_check
CHECK (priority IN ('low', 'normal', 'high', 'critical'));

CREATE INDEX IF NOT EXISTS idx_support_tickets_user_id ON public.support_tickets(user_id);
CREATE INDEX IF NOT EXISTS idx_support_tickets_status ON public.support_tickets(status);
CREATE INDEX IF NOT EXISTS idx_support_tickets_priority ON public.support_tickets(priority);
CREATE INDEX IF NOT EXISTS idx_support_tickets_assigned ON public.support_tickets(assigned_to);
CREATE INDEX IF NOT EXISTS idx_support_tickets_created ON public.support_tickets(created_at DESC);

CREATE TRIGGER update_support_tickets_updated_at
  BEFORE UPDATE ON public.support_tickets
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE public.support_tickets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own tickets"
  ON public.support_tickets FOR SELECT TO public
  USING (
    auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = user_id)
    OR auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = assigned_to)
  );

CREATE POLICY "Users can create tickets"
  ON public.support_tickets FOR INSERT TO public
  WITH CHECK (auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = user_id));

CREATE POLICY "Assigned users can update tickets"
  ON public.support_tickets FOR UPDATE TO public
  USING (auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = assigned_to));

-- Table 11: ticket_messages
CREATE TABLE IF NOT EXISTS public.ticket_messages (
  id uuid NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  ticket_id uuid NOT NULL REFERENCES public.support_tickets(id) ON DELETE CASCADE,
  user_id uuid REFERENCES public.profiles(id),
  message text NOT NULL,
  is_internal boolean DEFAULT false,
  attachments jsonb,
  created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ticket_messages_ticket_id ON public.ticket_messages(ticket_id);
CREATE INDEX IF NOT EXISTS idx_ticket_messages_user_id ON public.ticket_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_ticket_messages_created ON public.ticket_messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ticket_messages_internal ON public.ticket_messages(is_internal) WHERE is_internal = true;

ALTER TABLE public.ticket_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view messages of accessible tickets"
  ON public.ticket_messages FOR SELECT TO public
  USING (
    EXISTS (
      SELECT 1 FROM support_tickets st
      WHERE st.id = ticket_messages.ticket_id 
      AND (
        auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = st.user_id)
        OR auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = st.assigned_to)
      )
    )
  );

CREATE POLICY "Users can insert messages on accessible tickets"
  ON public.ticket_messages FOR INSERT TO public
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM support_tickets st
      WHERE st.id = ticket_messages.ticket_id 
      AND (
        auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = st.user_id)
        OR auth.uid() = (SELECT auth_user_id FROM profiles WHERE id = st.assigned_to)
      )
    )
  );
