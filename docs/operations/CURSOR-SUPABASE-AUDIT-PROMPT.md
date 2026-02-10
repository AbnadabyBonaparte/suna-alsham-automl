# PROMPT PARA CURSOR - AUDITORIA COMPLETA DO SUPABASE

> Cole este prompt inteiro no Cursor com acesso ao Supabase conectado.
> Ele vai gerar um relatório completo do estado real do backend.

---

## PROMPT:

```
Você é um auditor técnico. Preciso que você faça uma análise COMPLETA e HONESTA do nosso Supabase.
ZERO suposições - apenas o que existe DE VERDADE no banco. Consulte tudo diretamente.

Execute TODAS as queries abaixo e me retorne os resultados EXATOS. Não invente, não assuma, não arredonde.

### 1. TABELAS - O que realmente existe?

```sql
SELECT
  schemaname,
  tablename,
  hasindexes,
  hasrules,
  hastriggers
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

Depois para CADA tabela encontrada:

```sql
SELECT
  table_name,
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
```

### 2. CONTAGEM DE REGISTROS - Dados reais em cada tabela

Para CADA tabela pública, execute:

```sql
SELECT 'nome_da_tabela' as tabela, COUNT(*) as total FROM nome_da_tabela;
```

Me dê uma tabela com: nome_tabela | total_registros | está_vazia?

### 3. TABELA DE AGENTES - Estado real

```sql
-- Quantos agentes existem de verdade?
SELECT COUNT(*) as total_agents FROM agents;

-- Status breakdown
SELECT status, COUNT(*) as count
FROM agents
GROUP BY status
ORDER BY count DESC;

-- Tipos/categorias
SELECT type, COUNT(*) as count
FROM agents
GROUP BY type
ORDER BY count DESC;

-- Squad breakdown
SELECT squad, COUNT(*) as count
FROM agents
GROUP BY squad
ORDER BY count DESC;

-- Média de eficiência real
SELECT
  AVG(efficiency) as avg_efficiency,
  MIN(efficiency) as min_efficiency,
  MAX(efficiency) as max_efficiency,
  STDDEV(efficiency) as stddev_efficiency
FROM agents;

-- Agentes criados por data
SELECT
  DATE(created_at) as dia,
  COUNT(*) as criados
FROM agents
GROUP BY DATE(created_at)
ORDER BY dia DESC
LIMIT 30;

-- Sample de 5 agentes para ver estrutura real
SELECT * FROM agents LIMIT 5;
```

### 4. RLS POLICIES - Segurança real

```sql
SELECT
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
```

Me diga:
- Quantas tabelas TÊM RLS habilitado?
- Quantas NÃO TÊM?
- Alguma tabela pública está ABERTA sem proteção?

### 5. INDEXES - Performance

```sql
SELECT
  schemaname,
  tablename,
  indexname,
  indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```

Total de indexes? Alguma tabela grande sem index?

### 6. FUNCTIONS - O que existe no banco?

```sql
SELECT
  routine_name,
  routine_type,
  data_type
FROM information_schema.routines
WHERE routine_schema = 'public'
ORDER BY routine_name;
```

### 7. TRIGGERS - Automações reais

```sql
SELECT
  trigger_name,
  event_manipulation,
  event_object_table,
  action_statement,
  action_timing
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY event_object_table, trigger_name;
```

### 8. EDGE FUNCTIONS - Quais estão deployadas?

Liste TODAS as Edge Functions que existem no Supabase Dashboard:
- Nome
- Status (ativa/inativa)
- Última execução
- Logs recentes (últimas 24h)

### 9. CRON JOBS - O que está rodando?

```sql
SELECT * FROM cron.job ORDER BY jobname;
```

```sql
-- Últimas execuções
SELECT
  jobid,
  job_pid,
  status,
  return_message,
  start_time,
  end_time
FROM cron.job_run_details
ORDER BY start_time DESC
LIMIT 20;
```

Os crons estão FUNCIONANDO ou falhando? Me mostre os erros.

### 10. STORAGE BUCKETS

```sql
SELECT
  id,
  name,
  public,
  file_size_limit,
  allowed_mime_types,
  created_at
FROM storage.buckets;
```

Quantos arquivos em cada bucket?

```sql
SELECT
  bucket_id,
  COUNT(*) as total_files,
  SUM(metadata->>'size')::bigint as total_bytes
FROM storage.objects
GROUP BY bucket_id;
```

### 11. AUTH - Usuários reais

```sql
-- NÃO exponha emails ou dados sensíveis, só contagens
SELECT COUNT(*) as total_users FROM auth.users;

SELECT
  DATE(created_at) as dia,
  COUNT(*) as novos_users
FROM auth.users
GROUP BY DATE(created_at)
ORDER BY dia DESC;

-- Providers configurados
SELECT
  provider,
  COUNT(*) as total
FROM auth.identities
GROUP BY provider;
```

### 12. REALTIME - Está habilitado?

```sql
SELECT * FROM realtime.subscription LIMIT 10;
```

Quais tabelas têm Realtime habilitado no Dashboard?

### 13. MIGRATIONS - Histórico

```sql
SELECT * FROM supabase_migrations.schema_migrations ORDER BY version;
```

### 14. DATABASE SIZE

```sql
SELECT pg_size_pretty(pg_database_size(current_database())) as db_size;

SELECT
  relname as table_name,
  pg_size_pretty(pg_total_relation_size(relid)) as total_size,
  pg_size_pretty(pg_relation_size(relid)) as data_size,
  pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as index_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

---

## FORMATO DO RELATÓRIO

Me retorne EXATAMENTE neste formato:

```
# RELATÓRIO DE AUDITORIA SUPABASE - ALSHAM QUANTUM
Data: [data atual]

## 1. TABELAS
- Total: X tabelas
- [lista com nome e contagem de registros]

## 2. AGENTES
- Total real: X agentes
- Status breakdown: [dados]
- Eficiência média: X%

## 3. SEGURANÇA (RLS)
- Tabelas com RLS: X de Y
- Tabelas ABERTAS: [lista]
- Policies total: X

## 4. INDEXES
- Total: X indexes
- Tabelas sem index: [lista]

## 5. FUNCTIONS/TRIGGERS
- Functions: X
- Triggers: X
- [lista]

## 6. EDGE FUNCTIONS
- Deployadas: X
- Ativas: X
- Falhando: [lista]

## 7. CRON JOBS
- Total: X
- Funcionando: X
- Falhando: X
- [erros recentes]

## 8. STORAGE
- Buckets: X
- Arquivos total: X
- Tamanho total: X

## 9. AUTH
- Usuários: X
- Providers: [lista]

## 10. REALTIME
- Habilitado: sim/não
- Tabelas com realtime: [lista]

## 11. DATABASE
- Tamanho total: X
- Maior tabela: X

## 12. PROBLEMAS ENCONTRADOS
- [lista de problemas reais]

## 13. SCORE FINAL
- Database Design: X/10
- Segurança: X/10
- Performance: X/10
- Dados reais: X/10
- Automação: X/10
- TOTAL: X/50
```

IMPORTANTE:
- NÃO INVENTE NÚMEROS. Se uma query falhar, diga "QUERY FALHOU: [erro]"
- NÃO ASSUMA nada. Se não conseguir verificar, diga "NÃO VERIFICÁVEL"
- Se uma tabela não existir, diga "TABELA NÃO EXISTE"
- Se o cron estiver falhando, mostre os ERROS REAIS
- Seja BRUTALMENTE HONESTO. Prefiro verdades duras a mentiras bonitas.
```

---

**Depois de receber o relatório do Cursor, cole aqui para eu integrar com minha análise do frontend e código.**
