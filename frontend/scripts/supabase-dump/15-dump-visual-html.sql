-- ═══════════════════════════════════════════════════════════════
-- DUMP VISUAL COMPLETO EM HTML
-- ═══════════════════════════════════════════════════════════════
-- Descrição: Gera um HTML bonito com overview de todo o banco.
-- Instruções: Execute, copie o resultado e salve como .html
-- ═══════════════════════════════════════════════════════════════

WITH 
-- Tabelas e colunas
tabelas_info AS (
  SELECT 
    table_name,
    COUNT(*) as num_colunas,
    string_agg(
      column_name || ' (' || udt_name || ')',
      ', '
      ORDER BY ordinal_position
    ) as colunas_lista
  FROM information_schema.columns
  WHERE table_schema = 'public'
  GROUP BY table_name
),
-- RLS Policies
policies_info AS (
  SELECT 
    tablename,
    COUNT(*) as num_policies,
    string_agg(
      policyname || ' [' || cmd || ']',
      ', '
      ORDER BY policyname
    ) as policies_lista
  FROM pg_policies
  WHERE schemaname = 'public'
  GROUP BY tablename
),
-- Foreign Keys
fk_info AS (
  SELECT
    tc.table_name,
    COUNT(*) as num_fks,
    string_agg(
      kcu.column_name || ' → ' || ccu.table_name || '(' || ccu.column_name || ')',
      ', '
      ORDER BY kcu.column_name
    ) as fks_lista
  FROM information_schema.table_constraints AS tc
  JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
  JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
  WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = 'public'
  GROUP BY tc.table_name
),
-- Triggers
triggers_info AS (
  SELECT
    event_object_table,
    COUNT(*) as num_triggers,
    string_agg(
      trigger_name || ' [' || event_manipulation || ']',
      ', '
      ORDER BY trigger_name
    ) as triggers_lista
  FROM information_schema.triggers
  WHERE event_object_schema = 'public'
  GROUP BY event_object_table
),
-- Índices
indices_info AS (
  SELECT
    tablename,
    COUNT(*) as num_indices,
    string_agg(indexname, ', ' ORDER BY indexname) as indices_lista
  FROM pg_indexes
  WHERE schemaname = 'public'
  GROUP BY tablename
),
-- Combina tudo
tabelas_completas AS (
  SELECT
    t.table_name,
    t.num_colunas,
    t.colunas_lista,
    COALESCE(p.num_policies, 0) as num_policies,
    COALESCE(p.policies_lista, 'Nenhuma') as policies_lista,
    COALESCE(fk.num_fks, 0) as num_fks,
    COALESCE(fk.fks_lista, 'Nenhuma') as fks_lista,
    COALESCE(tr.num_triggers, 0) as num_triggers,
    COALESCE(tr.triggers_lista, 'Nenhum') as triggers_lista,
    COALESCE(idx.num_indices, 0) as num_indices,
    COALESCE(idx.indices_lista, 'Nenhum') as indices_lista
  FROM tabelas_info t
  LEFT JOIN policies_info p ON p.tablename = t.table_name
  LEFT JOIN fk_info fk ON fk.table_name = t.table_name
  LEFT JOIN triggers_info tr ON tr.event_object_table = t.table_name
  LEFT JOIN indices_info idx ON idx.tablename = t.table_name
)
SELECT 
  '<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dump Completo Supabase - ALSHAM QUANTUM AutoML</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
      color: #c9d1d9;
      padding: 40px 20px;
      line-height: 1.8;
      min-height: 100vh;
    }
    .container { max-width: 1400px; margin: 0 auto; }
    header {
      background: rgba(88, 166, 255, 0.1);
      border: 2px solid #58a6ff;
      border-radius: 12px;
      padding: 30px;
      margin-bottom: 40px;
      text-align: center;
    }
    h1 {
      color: #58a6ff;
      font-size: 2.5em;
      margin-bottom: 10px;
    }
    .timestamp {
      color: #8b949e;
      font-size: 0.9em;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 15px;
      margin-top: 20px;
    }
    .stat-card {
      background: rgba(30, 30, 30, 0.8);
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 15px;
      text-align: center;
    }
    .stat-number {
      font-size: 2em;
      color: #58a6ff;
      font-weight: bold;
    }
    .stat-label {
      color: #8b949e;
      font-size: 0.85em;
      margin-top: 5px;
    }
    .tables-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
      gap: 20px;
      margin-top: 30px;
    }
    .table-card {
      background: rgba(30, 30, 30, 0.9);
      border: 1px solid #30363d;
      border-radius: 10px;
      padding: 20px;
      transition: all 0.3s ease;
    }
    .table-card:hover {
      border-color: #58a6ff;
      box-shadow: 0 0 20px rgba(88, 166, 255, 0.2);
      transform: translateY(-2px);
    }
    .table-name {
      color: #58a6ff;
      font-size: 1.2em;
      font-weight: bold;
      margin-bottom: 15px;
      padding-bottom: 10px;
      border-bottom: 2px solid #30363d;
    }
    .table-detail {
      margin: 8px 0;
      font-size: 0.9em;
      display: flex;
      gap: 10px;
    }
    .detail-label {
      color: #f0883e;
      font-weight: bold;
      min-width: 100px;
    }
    .detail-value {
      color: #c9d1d9;
    }
    .columns-list {
      background: rgba(0, 0, 0, 0.3);
      border-left: 3px solid #58a6ff;
      padding: 10px;
      margin: 10px 0;
      border-radius: 4px;
      font-size: 0.8em;
      max-height: 120px;
      overflow-y: auto;
      font-family: monospace;
    }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.75em;
      margin: 2px;
    }
    .badge-policy { background: rgba(240, 136, 62, 0.2); color: #f0883e; }
    .badge-fk { background: rgba(79, 161, 79, 0.2); color: #4fa14f; }
    .badge-trigger { background: rgba(200, 100, 200, 0.2); color: #c864c8; }
    .badge-index { background: rgba(100, 150, 200, 0.2); color: #6496c8; }
    .badges-container { margin-top: 10px; }
    footer {
      text-align: center;
      margin-top: 60px;
      padding-top: 20px;
      border-top: 1px solid #30363d;
      color: #8b949e;
      font-size: 0.9em;
    }
    .warning {
      background: rgba(255, 100, 100, 0.1);
      border: 1px solid #f85149;
      border-radius: 8px;
      padding: 15px;
      margin: 20px 0;
      color: #f85149;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>🚀 Dump Completo Supabase</h1>
      <p style="color: #58a6ff; font-size: 1.1em;">ALSHAM QUANTUM AutoML</p>
      <p class="timestamp">Gerado em ' || to_char(now(), 'DD/MM/YYYY HH24:MI:SS') || ' UTC</p>
      <div class="stats">
        <div class="stat-card">
          <div class="stat-number">' || (SELECT COUNT(*) FROM tabelas_completas) || '</div>
          <div class="stat-label">Tabelas</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">' || (SELECT COALESCE(SUM(num_colunas), 0) FROM tabelas_completas) || '</div>
          <div class="stat-label">Colunas</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">' || (SELECT COALESCE(SUM(num_policies), 0) FROM tabelas_completas) || '</div>
          <div class="stat-label">RLS Policies</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">' || (SELECT COALESCE(SUM(num_fks), 0) FROM tabelas_completas) || '</div>
          <div class="stat-label">Foreign Keys</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">' || (SELECT COALESCE(SUM(num_triggers), 0) FROM tabelas_completas) || '</div>
          <div class="stat-label">Triggers</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">' || (SELECT COALESCE(SUM(num_indices), 0) FROM tabelas_completas) || '</div>
          <div class="stat-label">Índices</div>
        </div>
      </div>
    </header>
    
    <div class="warning">
      ⚠️ <strong>ATENÇÃO:</strong> Este documento contém informações sensíveis do banco de dados. Mantenha seguro!
    </div>

    <h2 style="color: #58a6ff; margin: 30px 0 20px;">📊 Tabelas do Schema Público</h2>
    
    <div class="tables-grid">' ||
(
  SELECT string_agg(
    '
      <div class="table-card">
        <div class="table-name">📊 ' || table_name || '</div>
        <div class="table-detail">
          <span class="detail-label">Colunas:</span>
          <span class="detail-value">' || num_colunas || '</span>
        </div>
        <div class="columns-list">' || colunas_lista || '</div>
        <div class="table-detail">
          <span class="detail-label">RLS Policies:</span>
          <span class="detail-value">' || num_policies || '</span>
        </div>
        <div class="table-detail">
          <span class="detail-label">Foreign Keys:</span>
          <span class="detail-value">' || num_fks || '</span>
        </div>
        <div class="table-detail">
          <span class="detail-label">Triggers:</span>
          <span class="detail-value">' || num_triggers || '</span>
        </div>
        <div class="table-detail">
          <span class="detail-label">Índices:</span>
          <span class="detail-value">' || num_indices || '</span>
        </div>
        <div class="badges-container">' ||
          CASE WHEN num_policies > 0 THEN '<span class="badge badge-policy">🔒 RLS</span>' ELSE '' END ||
          CASE WHEN num_fks > 0 THEN '<span class="badge badge-fk">🔗 FK</span>' ELSE '' END ||
          CASE WHEN num_triggers > 0 THEN '<span class="badge badge-trigger">⚡ Trigger</span>' ELSE '' END ||
          CASE WHEN num_indices > 0 THEN '<span class="badge badge-index">📇 Index</span>' ELSE '' END ||
        '</div>
      </div>',
    E'\n'
    ORDER BY table_name
  )
  FROM tabelas_completas
) ||
'
    </div>

    <footer>
      <p>📋 Dump gerado automaticamente via Supabase SQL Editor</p>
      <p>🔒 Este documento contém informações sensíveis - mantenha seguro</p>
      <p style="margin-top: 20px; color: #58a6ff;">
        <strong>ALSHAM QUANTUM AutoML</strong> - Versão MAXIMALISTA COMPLETA 🚀
      </p>
    </footer>
  </div>
</body>
</html>' AS html_completo;

