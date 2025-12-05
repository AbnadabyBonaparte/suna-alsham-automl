


-- ============================================
-- AUTH TRIGGERS (Phase 2.1)
-- Auto-create profile and user_stats on signup
-- Added: 2025-11-25
-- ============================================

-- Function: Handle new user registration
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  -- Create profile
  INSERT INTO public.profiles (id, username, full_name, avatar_url)
  VALUES (
    NEW.id,
    NEW.raw_user_meta_data->>'username',
    NEW.raw_user_meta_data->>'full_name',
    NEW.raw_user_meta_data->>'avatar_url'
  );
  
  -- Initialize user stats (gamification)
  INSERT INTO public.user_stats (user_id, xp, level)
  VALUES (NEW.id, 0, 1);
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger: Execute on new user signup
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================
-- ALSHAM QUANTUM - SUBSCRIPTION & FOUNDER ACCESS MIGRATION
-- Added: 2025-12-05
-- Add subscription fields and founder access
-- ============================================

-- Add subscription fields to profiles table
ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS subscription_plan TEXT DEFAULT 'free' CHECK (subscription_plan IN ('free', 'starter', 'pro', 'enterprise')),
ADD COLUMN IF NOT EXISTS subscription_status TEXT DEFAULT 'inactive' CHECK (subscription_status IN ('active', 'inactive', 'cancelled', 'past_due')),
ADD COLUMN IF NOT EXISTS billing_cycle TEXT DEFAULT 'monthly' CHECK (billing_cycle IN ('monthly', 'yearly')),
ADD COLUMN IF NOT EXISTS subscription_end TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS founder_access BOOLEAN DEFAULT false;

-- Set founder access for the owner
UPDATE public.profiles
SET founder_access = true,
    subscription_plan = 'enterprise',
    subscription_status = 'active'
WHERE id IN (
    SELECT id FROM auth.users WHERE email = 'casamondestore@gmail.com'
);

-- ============================================
-- MIGRATION UPDATED: 2025-11-25 (with subscription fields)
-- Phase 1.2: Database Schema - COMPLETE (26 tables)
-- Phase 2.1: Authentication - COMPLETE (trigger added)
-- Phase 2.2: Subscription System - COMPLETE
-- Total Project Progress: ~35%
-- ============================================
