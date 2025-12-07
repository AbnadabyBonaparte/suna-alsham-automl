-- ═══════════════════════════════════════════════════════════════
-- DUMP 10: DADOS DA TABELA AGENTS
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Dados dos 139 agents do sistema.
-- ═══════════════════════════════════════════════════════════════

SELECT 
  id, 
  name, 
  role, 
  status, 
  efficiency, 
  current_task,
  neural_load,
  version,
  evolution_count,
  user_id,
  created_at,
  updated_at
FROM agents 
ORDER BY name;

