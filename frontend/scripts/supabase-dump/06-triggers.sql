-- ═══════════════════════════════════════════════════════════════
-- DUMP 05: TRIGGERS
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Lista todos os triggers automáticos do banco,
--            como criação de profile após signup.
-- ═══════════════════════════════════════════════════════════════

SELECT
  trigger_name,
  event_object_schema,
  event_object_table,
  event_manipulation,
  action_timing,
  action_orientation,
  action_statement
FROM information_schema.triggers
WHERE event_object_schema = 'public'
ORDER BY event_object_table, trigger_name;

