-- ═══════════════════════════════════════════════════════════════
-- MIGRATION: Adicionar campos de onboarding à tabela profiles
-- Data: 2023-12-09
-- Descrição: Adiciona campo onboarding_completed para controlar
--            o fluxo de onboarding e evitar loops infinitos
-- ═══════════════════════════════════════════════════════════════

-- Adicionar campo onboarding_completed (padrão FALSE)
ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE;

-- Criar índice para otimizar queries de verificação
CREATE INDEX IF NOT EXISTS idx_profiles_onboarding_completed
ON public.profiles(onboarding_completed);

-- Atualizar founder para já ter completado onboarding (para testes)
UPDATE public.profiles
SET onboarding_completed = TRUE
WHERE founder_access = TRUE;

-- Comentário da coluna
COMMENT ON COLUMN public.profiles.onboarding_completed IS
'Indica se o usuário completou o processo de onboarding (seleção de role)';
