═══════════════════════════════════════════════════════════════
🤖 ANTIGRAVITY - PHASE 4.1: ADD MISSING COLUMNS TO AGENTS
═══════════════════════════════════════════════════════════════
📅 Data: 2025-11-25
🎯 Objetivo: Adicionar 2 colunas à tabela agents (efficiency, current_task)

⚠️  REGRA CRÍTICA:
- NÃO DROPAR tabela agents
- NÃO DELETAR os 139 agentes
- APENAS ADD COLUMN (adicionar colunas)
- Validar ANTES e DEPOIS

═══════════════════════════════════════════════════════════════

## 🔍 VALIDAÇÃO PRÉ-EXECUÇÃO (RODAR PRIMEIRO)

Execute no Supabase SQL Editor:

```sql
-- Confirmar que temos 139 agentes
SELECT COUNT(*) FROM agents;
-- Esperado: 139

-- Ver estrutura atual
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'agents' 
AND table_schema = 'public'
ORDER BY ordinal_position;
```

**❓ CHECKPOINT:** Confirmar com usuário antes de continuar.

═══════════════════════════════════════════════════════════════

## 📝 SQL A EXECUTAR (COPIAR E COLAR NO SUPABASE)

```sql
-- ============================================
-- ADD COLUMNS: efficiency & current_task
-- Para página de Agents mostrar dados completos
-- ============================================

-- 1. Adicionar coluna efficiency (0-100%)
ALTER TABLE public.agents 
ADD COLUMN IF NOT EXISTS efficiency float DEFAULT 95.0;

-- 2. Adicionar coluna current_task (texto livre)
ALTER TABLE public.agents 
ADD COLUMN IF NOT EXISTS current_task text DEFAULT 'Standby mode';

-- 3. Popular com valores variados (para parecer real)
-- Distribuir efficiency entre 75-100%
UPDATE public.agents 
SET efficiency = 75 + (RANDOM() * 25)::int
WHERE efficiency IS NULL OR efficiency = 95.0;

-- 4. Atribuir tarefas interessantes baseado no squad
UPDATE public.agents 
SET current_task = CASE 
  WHEN squad = 'CORE' THEN 
    CASE (RANDOM() * 3)::int
      WHEN 0 THEN 'Sincronizando matriz neural'
      WHEN 1 THEN 'Orquestrando 47 processos'
      ELSE 'Otimizando performance sistêmica'
    END
  WHEN squad = 'GUARD' THEN 
    CASE (RANDOM() * 3)::int
      WHEN 0 THEN 'Varredura de ameaças em tempo real'
      WHEN 1 THEN 'Monitorando 1,248 endpoints'
      ELSE 'Análise de padrões suspeitos'
    END
  WHEN squad = 'ANALYST' THEN 
    CASE (RANDOM() * 3)::int
      WHEN 0 THEN 'Processando big data: 2.3TB'
      WHEN 1 THEN 'Prevendo tendências de mercado'
      ELSE 'Correlacionando datasets complexos'
    END
  WHEN squad = 'SPECIALIST' THEN 
    CASE (RANDOM() * 3)::int
      WHEN 0 THEN 'Otimizando pipeline de vendas'
      WHEN 1 THEN 'Gerando relatórios de KPIs'
      ELSE 'Automatizando workflow crítico'
    END
  WHEN squad = 'CHAOS' THEN 
    CASE (RANDOM() * 3)::int
      WHEN 0 THEN 'Testando limites do sistema'
      WHEN 1 THEN 'Simulando cenários extremos'
      ELSE 'Injetando aleatoriedade controlada'
    END
  ELSE 'Aguardando comando'
END
WHERE current_task = 'Standby mode' OR current_task IS NULL;

-- 5. Alguns agentes CORE com efficiency alta
UPDATE public.agents 
SET efficiency = 98 + (RANDOM() * 2)::int
WHERE squad = 'CORE' 
AND name ILIKE '%ORCHESTRATOR%'
LIMIT 5;

-- 6. Alguns agentes em manutenção (efficiency baixa)
UPDATE public.agents 
SET 
  efficiency = 60 + (RANDOM() * 15)::int,
  current_task = 'Manutenção preventiva programada',
  status = 'maintenance'
WHERE squad IN ('ANALYST', 'SPECIALIST')
AND RANDOM() < 0.1
LIMIT 3;

-- ============================================
-- FIM DO SCRIPT
-- ============================================
```

═══════════════════════════════════════════════════════════════

## 🔍 VALIDAÇÃO PÓS-EXECUÇÃO (RODAR DEPOIS)

```sql
-- 1. Confirmar que ainda temos 139 agentes
SELECT COUNT(*) FROM agents;
-- Esperado: 139

-- 2. Ver distribuição de efficiency
SELECT 
  MIN(efficiency) as min_eff,
  MAX(efficiency) as max_eff,
  AVG(efficiency)::numeric(10,2) as avg_eff
FROM agents;
-- Esperado: min ~60, max ~100, avg ~85-90

-- 3. Conferir algumas tarefas
SELECT name, squad, efficiency, current_task 
FROM agents 
ORDER BY RANDOM() 
LIMIT 10;
-- Deve mostrar dados variados

-- 4. Contar por squad
SELECT squad, COUNT(*), AVG(efficiency)::int as avg_eff
FROM agents 
GROUP BY squad 
ORDER BY squad;
```

═══════════════════════════════════════════════════════════════

## ✅ CHECKLIST FINAL

- [ ] SQL executado sem erros
- [ ] SELECT COUNT(*) FROM agents; retorna 139
- [ ] Coluna efficiency existe (60-100%)
- [ ] Coluna current_task existe (textos variados)
- [ ] Distribuição por squad OK
- [ ] Nenhum agente foi deletado

═══════════════════════════════════════════════════════════════
