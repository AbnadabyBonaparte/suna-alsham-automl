-- ═══════════════════════════════════════════════════════════════
-- DUMP 09: DADOS DA TABELA AUTH.USERS
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Metadados dos usuários autenticados.
-- ⚠️ CUIDADO: Contém dados sensíveis!
-- ═══════════════════════════════════════════════════════════════

SELECT 
  id, 
  email, 
  created_at, 
  last_sign_in_at, 
  email_confirmed_at,
  raw_user_meta_data as user_metadata
FROM auth.users 
ORDER BY created_at DESC;

