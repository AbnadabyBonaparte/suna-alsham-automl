-- ============================================
-- ALSHAM QUANTUM - PROFILES STRIPE COLUMNS
-- Migration: 20260710_profiles_stripe_columns
-- ============================================
-- O webhook do Stripe grava a assinatura em public.profiles.
-- Para tratar customer.subscription.updated/deleted precisamos
-- mapear o customer/subscription do Stripe -> profile.
-- ============================================

ALTER TABLE public.profiles
  ADD COLUMN IF NOT EXISTS stripe_customer_id TEXT,
  ADD COLUMN IF NOT EXISTS stripe_subscription_id TEXT;

CREATE INDEX IF NOT EXISTS idx_profiles_stripe_customer_id
  ON public.profiles(stripe_customer_id);

-- ============================================
-- Migration Complete! 💳
-- ============================================
