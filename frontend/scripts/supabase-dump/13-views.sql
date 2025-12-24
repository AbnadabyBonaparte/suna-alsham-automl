-- ═══════════════════════════════════════════════════════════════
-- DUMP 12: VIEWS CUSTOMIZADAS
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Lista todas as views do schema público.
-- ═══════════════════════════════════════════════════════════════

SELECT
  table_schema,
  table_name,
  view_definition
FROM information_schema.views
WHERE table_schema = 'public'
ORDER BY table_name;

