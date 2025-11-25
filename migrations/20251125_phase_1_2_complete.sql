


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
-- MIGRATION UPDATED: 2025-11-25
-- Phase 1.2: Database Schema - COMPLETE (26 tables)
-- Phase 2.1: Authentication - COMPLETE (trigger added)
-- Total Project Progress: ~32%
-- ============================================
