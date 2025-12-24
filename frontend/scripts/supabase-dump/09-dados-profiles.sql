-- ═══════════════════════════════════════════════════════════════
-- DUMP 08: DADOS DA TABELA PROFILES
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Dados reais dos profiles de usuários.
-- ⚠️ CUIDADO: Contém dados sensíveis!
-- ═══════════════════════════════════════════════════════════════

SELECT 
  id,
  username,
  full_name,
  avatar_url,
  role,
  subscription_plan,
  subscription_status,
  founder_access,
  created_at,
  updated_at
FROM profiles 
ORDER BY created_at DESC;

