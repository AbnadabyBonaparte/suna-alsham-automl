-- ========================================
-- MIGRATION: Fix RLS Policies and Create Profile Trigger
-- Date: 2025-12-08
-- Author: Cursor (via Manus)
-- ========================================
-- This migration fixes 3 critical issues:
-- 1. Create trigger for automatic profile creation on signup
-- 2. Fix RLS policies that referenced non-existent auth_user_id column
-- 3. Fix recursive policy that used is_founder() function
-- ========================================

-- ========================================
-- AÇÃO 1: Criar Trigger de Auto-Criação de Profile
-- ========================================

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (
    id,
    email,
    created_at,
    subscription_status,
    subscription_plan,
    founder_access
  )
  VALUES (
    new.id,
    new.email,
    now(),
    'free',
    'free',
    false
  );
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ========================================
-- AÇÃO 2: Corrigir RLS Policies
-- ========================================

-- Remover policies com auth_user_id (vão falhar)
DROP POLICY IF EXISTS "Users can delete own api keys" ON api_keys;
DROP POLICY IF EXISTS "Users can insert own api keys" ON api_keys;
DROP POLICY IF EXISTS "Users can update own api keys" ON api_keys;
DROP POLICY IF EXISTS "Users can view own api keys" ON api_keys;
DROP POLICY IF EXISTS "Users can view own api logs" ON api_logs;
DROP POLICY IF EXISTS "Users can insert activities on own deals" ON deal_activities;
DROP POLICY IF EXISTS "Users can view activities of own deals" ON deal_activities;
DROP POLICY IF EXISTS "Users can insert own deals" ON deals;
DROP POLICY IF EXISTS "Users can update own deals" ON deals;
DROP POLICY IF EXISTS "Users can view own deals" ON deals;
DROP POLICY IF EXISTS "Users can insert own invoices" ON invoices;
DROP POLICY IF EXISTS "Users can update own invoices" ON invoices;
DROP POLICY IF EXISTS "Users can view own invoices" ON invoices;
DROP POLICY IF EXISTS "Users can view own rate limits" ON rate_limits;
DROP POLICY IF EXISTS "Users can view own transactions" ON transactions;
DROP POLICY IF EXISTS "Users can delete own sessions" ON user_sessions;
DROP POLICY IF EXISTS "Users can view own sessions" ON user_sessions;
DROP POLICY IF EXISTS "Users can insert own stats" ON user_stats;
DROP POLICY IF EXISTS "Users can update own stats" ON user_stats;
DROP POLICY IF EXISTS "Assigned users can update tickets" ON support_tickets;
DROP POLICY IF EXISTS "Users can create tickets" ON support_tickets;
DROP POLICY IF EXISTS "Users can view own tickets" ON support_tickets;
DROP POLICY IF EXISTS "Users can insert messages on accessible tickets" ON ticket_messages;
DROP POLICY IF EXISTS "Users can view messages of accessible tickets" ON ticket_messages;
DROP POLICY IF EXISTS "Users can view own predictions" ON predictions;

-- Recriar policies com lógica CORRETA
CREATE POLICY "Users can delete own api keys"
  ON api_keys FOR DELETE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own api keys"
  ON api_keys FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own api keys"
  ON api_keys FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can view own api keys"
  ON api_keys FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can view own api logs"
  ON api_logs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert activities on own deals"
  ON deal_activities FOR INSERT
  WITH CHECK (EXISTS (SELECT 1 FROM deals WHERE deals.id = deal_activities.deal_id AND deals.user_id = auth.uid()));

CREATE POLICY "Users can view activities of own deals"
  ON deal_activities FOR SELECT
  USING (EXISTS (SELECT 1 FROM deals WHERE deals.id = deal_activities.deal_id AND deals.user_id = auth.uid()));

CREATE POLICY "Users can insert own deals"
  ON deals FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own deals"
  ON deals FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can view own deals"
  ON deals FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own invoices"
  ON invoices FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own invoices"
  ON invoices FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can view own invoices"
  ON invoices FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can view own rate limits"
  ON rate_limits FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can view own transactions"
  ON transactions FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own sessions"
  ON user_sessions FOR DELETE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can view own sessions"
  ON user_sessions FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own stats"
  ON user_stats FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own stats"
  ON user_stats FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Assigned users can update tickets"
  ON support_tickets FOR UPDATE
  USING (auth.uid() = assigned_to);

CREATE POLICY "Users can create tickets"
  ON support_tickets FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own tickets"
  ON support_tickets FOR SELECT
  USING (auth.uid() = user_id OR auth.uid() = assigned_to);

CREATE POLICY "Users can insert messages on accessible tickets"
  ON ticket_messages FOR INSERT
  WITH CHECK (EXISTS (
    SELECT 1 FROM support_tickets st
    WHERE st.id = ticket_messages.ticket_id
      AND (auth.uid() = st.user_id OR auth.uid() = st.assigned_to)
  ));

CREATE POLICY "Users can view messages of accessible tickets"
  ON ticket_messages FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM support_tickets st
    WHERE st.id = ticket_messages.ticket_id
      AND (auth.uid() = st.user_id OR auth.uid() = st.assigned_to)
  ));

CREATE POLICY "Users can view own predictions"
  ON predictions FOR SELECT
  USING (auth.uid() = user_id OR user_id IS NULL);

-- ========================================
-- AÇÃO 3: Corrigir Policy Recursiva
-- ========================================

DROP POLICY IF EXISTS "Founders can read all profiles" ON profiles;

CREATE POLICY "Founders can read all profiles"
  ON profiles FOR SELECT
  USING (
    (SELECT founder_access FROM profiles WHERE id = auth.uid()) = true
  );

-- ========================================
-- Verificações
-- ========================================

-- Verificar trigger criada
-- SELECT * FROM pg_trigger WHERE tgname = 'on_auth_user_created';

-- Verificar policies criadas
-- SELECT tablename, policyname, cmd FROM pg_policies
-- WHERE tablename IN ('api_keys', 'api_logs', 'deals', 'invoices', 'user_sessions', 'support_tickets', 'profiles')
-- ORDER BY tablename, policyname;








