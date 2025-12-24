-- ═══════════════════════════════════════════════════════════════
-- DUMP 07: STORAGE BUCKETS
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Lista todos os buckets de storage,
--            se são públicos, limites de tamanho, etc.
-- ═══════════════════════════════════════════════════════════════

SELECT
  id,
  name,
  owner,
  public,
  created_at,
  updated_at,
  file_size_limit,
  allowed_mime_types
FROM storage.buckets
ORDER BY name;

