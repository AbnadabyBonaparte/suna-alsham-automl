-- ============================================================================
-- QUANTUM — COTA DE EXPERIMENTAÇÃO E JANELA DE GARANTIA
-- Migration: 20260728_quota_garantia
-- ============================================================================
-- Fecha o vazamento "usa o mês de token e pede reembolso". Registra, por
-- usuário, quando a garantia começou e se ele confirmou a permanência. O uso
-- é MEDIDO pela tabela `requests` (já tem user_id + created_at) — sem duplicar
-- fonte de verdade; só criamos o índice que torna a contagem barata.
--
-- Aditiva e idempotente (IF NOT EXISTS). Aplicar é ato do fundador.
-- ============================================================================

ALTER TABLE public.profiles
  ADD COLUMN IF NOT EXISTS guarantee_started_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS guarantee_waived     BOOLEAN NOT NULL DEFAULT false;

COMMENT ON COLUMN public.profiles.guarantee_started_at IS
  'Início da janela de garantia (1ª ativação de assinatura). Gravado uma vez pelo webhook.';
COMMENT ON COLUMN public.profiles.guarantee_waived IS
  'true = usuário confirmou permanência e renunciou à garantia de 30 dias (libera a cota). Só vale após os 7 dias legais.';

-- Índice que torna barata a contagem de uso por usuário na janela.
CREATE INDEX IF NOT EXISTS idx_requests_user_created
  ON public.requests(user_id, created_at);

-- ============================================================================
-- Depois de aplicar: o webhook grava guarantee_started_at na 1ª ativação e a
-- rota de execução conta requests desde essa data para aplicar a cota.
-- Ver frontend/src/lib/quota.ts e docs/produtos/GARANTIA-COM-COTA.md.
-- ============================================================================
