-- ============================================================================
-- QUANTUM — COLUNAS DE ASSINATURA EM public.profiles (o elo pós-pagamento)
-- Migration: 20260728_profiles_subscription_columns
-- ============================================================================
-- ⚠️ BLOQUEIO PROVADO (Lei da Contra-Prova, contra o banco vivo suna-core em
--    28/jul/2026): public.profiles TEM subscription_plan, subscription_status
--    e founder_access — mas NÃO tem billing_cycle, subscription_end,
--    stripe_customer_id nem stripe_subscription_id. A migration
--    20260710_profiles_stripe_columns NUNCA foi aplicada.
--
-- Consequência sem estas colunas — o checkout "funciona" mas a venda não fecha:
--   1. O webhook (checkout.session.completed) faz UPDATE profiles SET
--      subscription_status='active', billing_cycle=…, stripe_customer_id=… .
--      Postgres REJEITA o UPDATE inteiro (coluna inexistente, 42703) → 500 pro
--      Stripe → o profile NUNCA vira 'active' → o cliente PAGA e não ganha acesso.
--   2. requireDashboardAccess() faz SELECT … billing_cycle, subscription_end …
--      Esse SELECT também falha → profile vira default (free/inactive) → nenhum
--      assinante pago passa no portão (só o fundador, que entra por e-mail).
--
-- Esta migration é ADITIVA e IDEMPOTENTE (IF NOT EXISTS). Não altera dado
-- existente. É o passo 1 da ativação do checkout — aplicar é ato do fundador.
-- ============================================================================

ALTER TABLE public.profiles
  ADD COLUMN IF NOT EXISTS stripe_customer_id      TEXT,
  ADD COLUMN IF NOT EXISTS stripe_subscription_id  TEXT,
  ADD COLUMN IF NOT EXISTS billing_cycle           TEXT,
  ADD COLUMN IF NOT EXISTS subscription_end        TIMESTAMPTZ;

-- billing_cycle só aceita os dois valores que o webhook grava (null continua ok).
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'profiles_billing_cycle_check'
  ) THEN
    ALTER TABLE public.profiles
      ADD CONSTRAINT profiles_billing_cycle_check
      CHECK (billing_cycle IS NULL OR billing_cycle IN ('monthly', 'yearly'));
  END IF;
END $$;

-- Índice para o webhook achar o profile pelo customer do Stripe
-- (customer.subscription.updated/deleted mapeiam por stripe_customer_id).
CREATE INDEX IF NOT EXISTS idx_profiles_stripe_customer_id
  ON public.profiles(stripe_customer_id);

COMMENT ON COLUMN public.profiles.billing_cycle IS
  'Ciclo de cobranca (monthly|yearly), gravado pelo webhook do Stripe.';
COMMENT ON COLUMN public.profiles.subscription_end IS
  'Fim da assinatura (cancel_at do Stripe), gravado pelo webhook.';

-- ============================================================================
-- Depois de aplicar: o webhook consegue gravar e o portão consegue ler.
-- Sem isto, nenhuma venda real fecha. Ver docs/produtos/ATIVAR-CHECKOUT.md.
-- ============================================================================
