-- ═══════════════════════════════════════════════════════════════
-- DUMP 06: FUNÇÕES / PROCEDURES
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Lista todas as funções customizadas do banco.
-- ═══════════════════════════════════════════════════════════════

SELECT
  routine_schema,
  routine_name,
  routine_type,
  data_type as return_type,
  routine_definition
FROM information_schema.routines
WHERE routine_schema = 'public'
ORDER BY routine_name;

