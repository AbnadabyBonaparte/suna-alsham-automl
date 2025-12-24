-- ═══════════════════════════════════════════════════════════════
-- DUMP 13: SEQUÊNCIAS (Auto-increment)
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Lista todas as sequências do schema público.
-- ═══════════════════════════════════════════════════════════════

SELECT
  sequence_schema,
  sequence_name,
  data_type,
  start_value,
  minimum_value,
  maximum_value,
  increment,
  cycle_option
FROM information_schema.sequences
WHERE sequence_schema = 'public'
ORDER BY sequence_name;

