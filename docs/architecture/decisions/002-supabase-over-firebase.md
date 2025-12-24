# ADR-002: Supabase over Firebase

**Status:** ✅ Aceita  
**Data:** 2025-11-20  
**Decisores:** ALSHAM GLOBAL Tech Team

---

## Contexto

O ALSHAM QUANTUM precisa de:
- Banco de dados relacional robusto
- Autenticação enterprise-grade
- Real-time subscriptions
- Storage para arquivos
- Edge Functions para lógica server-side
- Row Level Security (RLS) para multi-tenancy

---

## Decisão

**Usar Supabase como backend principal.**

```typescript
// Cliente Supabase
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
```

---

## Alternativas Consideradas

### 1. Firebase
- **Prós:** 
  - Ecossistema Google
  - Firestore escalável
  - Auth robusto
  - Hosting integrado
- **Contras:** 
  - NoSQL (difícil queries complexas)
  - Vendor lock-in forte
  - Pricing imprevisível
  - Sem SQL nativo

### 2. PlanetScale + Clerk + Upstash
- **Prós:** 
  - MySQL serverless
  - Auth dedicado (Clerk)
  - Cache Redis (Upstash)
- **Contras:** 
  - 3 serviços para gerenciar
  - Mais complexidade
  - Mais custos

### 3. Supabase ✅
- **Prós:**
  - PostgreSQL completo (SQL real)
  - Auth integrado
  - Realtime nativo
  - Storage incluído
  - Edge Functions (Deno)
  - RLS para segurança
  - Open source (sem lock-in)
  - Pricing previsível
  - Dashboard excelente
- **Contras:**
  - Menos maduro que Firebase
  - Comunidade menor

---

## Consequências

### Positivas
- ✅ SQL completo para queries complexas
- ✅ RLS elimina necessidade de middleware de auth em cada query
- ✅ Realtime subscriptions nativo
- ✅ Um único serviço (simplifica ops)
- ✅ Open source (podemos self-host se necessário)
- ✅ PostgreSQL = skills transferíveis
- ✅ Edge Functions para lógica server-side

### Negativas
- ⚠️ Menos recursos de aprendizado que Firebase
- ⚠️ Comunidade menor
- ⚠️ Algumas features ainda em beta

---

## Implementação

### Schema Atual
```
27 tabelas
279+ colunas
120+ indexes
70+ RLS policies
8+ triggers
3 storage buckets
3 edge functions
4 cron jobs
```

### Tabelas Principais
```sql
-- Core
profiles, agents, agent_logs, user_sessions

-- Business
deals, support_tickets, social_posts, transactions

-- System
system_metrics, audit_log, api_keys
```

### RLS Pattern
```sql
-- Usuário vê apenas seus dados
CREATE POLICY "Users see own data" ON table_name
FOR SELECT USING (auth.uid() = user_id);

-- Founders veem tudo
CREATE POLICY "Founders see all" ON table_name
FOR SELECT USING (
  (SELECT founder_access FROM profiles WHERE id = auth.uid()) = true
);
```

---

## Referências

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase vs Firebase](https://supabase.com/alternatives/supabase-vs-firebase)
- [migrations/](../../../migrations/)

