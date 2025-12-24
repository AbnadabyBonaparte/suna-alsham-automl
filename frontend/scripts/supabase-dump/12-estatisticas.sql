-- ═══════════════════════════════════════════════════════════════
-- DUMP 11: ESTATÍSTICAS GERAIS DO BANCO
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Tamanho das tabelas, número de colunas e constraints.
-- ═══════════════════════════════════════════════════════════════

SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as tamanho_total,
  pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as tamanho_dados,
  (SELECT COUNT(*) FROM information_schema.columns 
   WHERE table_schema = schemaname AND table_name = tablename) as num_colunas,
  (SELECT COUNT(*) FROM information_schema.table_constraints 
   WHERE table_schema = schemaname AND table_name = tablename) as num_constraints
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

