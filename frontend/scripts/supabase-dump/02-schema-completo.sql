-- ═══════════════════════════════════════════════════════════════
-- DUMP 01: SCHEMA COMPLETO (Tabelas + Colunas + Tipos)
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Lista todas as tabelas, colunas, tipos de dados,
--            defaults, nullable, etc.
-- ═══════════════════════════════════════════════════════════════

SELECT 
  table_name,
  column_name,
  ordinal_position,
  udt_name as data_type,
  is_nullable,
  column_default,
  character_maximum_length,
  numeric_precision,
  numeric_scale
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;

