-- ═══════════════════════════════════════════════════════════════
-- DUMP 02: ÍNDICES E CONSTRAINTS
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Lista todas as chaves primárias, índices únicos,
--            e índices de performance.
-- ═══════════════════════════════════════════════════════════════

SELECT
  i.tablename,
  i.indexname,
  i.indexdef
FROM pg_indexes i
WHERE i.schemaname = 'public'
ORDER BY i.tablename, i.indexname;

