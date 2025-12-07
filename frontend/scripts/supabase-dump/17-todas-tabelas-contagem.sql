-- ═══════════════════════════════════════════════════════════════
-- DUMP EXTRA: CONTAGEM DE LINHAS EM TODAS AS TABELAS
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Mostra quantas linhas cada tabela tem.
-- ═══════════════════════════════════════════════════════════════

SELECT 
  schemaname,
  relname as tablename,
  n_live_tup as row_count
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC;

