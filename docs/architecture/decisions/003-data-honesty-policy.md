# ADR-003: Data Honesty Policy

**Status:** ✅ Aceita  
**Data:** 2025-11-25  
**Decisores:** ALSHAM GLOBAL Leadership

---

## Contexto

Durante o desenvolvimento, surgiu a tentação de:
- Mostrar dados fake para "impressionar"
- Simular atividade de agentes que não estão rodando
- Hardcodar métricas bonitas (99.9% uptime, 12ms latência)
- Misturar dados de demo com produção

Isso é prática comum na indústria, mas decidimos ser diferentes.

---

## Decisão

**NUNCA mostrar dados fake em produção. Mostrar 0 quando é 0.**

```typescript
// ❌ PROIBIDO
const activeAgents = 42; // hardcoded

// ✅ OBRIGATÓRIO
const { data: agents } = await supabase
  .from('agents')
  .select('*')
  .eq('status', 'running');
const activeAgents = agents?.length || 0; // pode ser 0, e tá ok
```

---

## Alternativas Consideradas

### 1. Dados Fake em Produção
- **Prós:** 
  - Dashboard sempre "bonito"
  - Impressiona visitantes
  - Mais fácil de implementar
- **Contras:** 
  - Mentira
  - Impossível debugar problemas reais
  - Perde confiança quando descobrem
  - Engenheiros não confiam nos dados

### 2. Modo Demo Separado
- **Prós:**
  - Demo com dados fake claramente marcado
  - Produção 100% real
- **Contras:**
  - Dois ambientes para manter

### 3. Honestidade Total ✅
- **Prós:**
  - Confiança total nos dados
  - Debug facilitado
  - Integridade profissional
  - Investidores podem verificar tudo
- **Contras:**
  - Dashboard pode mostrar 0
  - Menos "impressionante" inicialmente

---

## Consequências

### Positivas
- ✅ Qualquer métrica pode ser verificada no banco
- ✅ Engenheiros confiam nos dashboards
- ✅ Investidores veem a realidade
- ✅ Bugs são detectados imediatamente
- ✅ Cultura de integridade
- ✅ Força a equipe a construir features reais

### Negativas
- ⚠️ Dashboard mostra "0 operational agents" (porque é verdade)
- ⚠️ Latência real (~900ms) vs fake (12ms)
- ⚠️ Menos "wow factor" inicial

---

## Implementação

### O que Mostramos (Real)
```typescript
// Latência real medida
const start = performance.now();
await supabase.from('agents').select('count');
const latency = performance.now() - start;

// Uptime calculado
const projectStart = new Date('2024-11-20');
const uptime = calculateUptime(projectStart);

// Contagens reais
const { count: agentCount } = await supabase
  .from('agents')
  .select('*', { count: 'exact', head: true });
```

### O que NÃO Mostramos
```typescript
// ❌ NUNCA
const fakeMetrics = {
  latency: 12,        // fake
  uptime: 99.99,      // fake
  activeAgents: 100,  // fake
  requests: 50000,    // fake
};
```

### Ambiente Demo (Separado)
```typescript
// Se precisar demo, usar conta separada
// demo@alshamglobal.com.br
// Com banner claro: "🎭 DEMO MODE"
// NUNCA misturar com produção
```

---

## Comunicação

### Para Técnicos
> "0 agentes operacionais porque não temos workers rodando ainda. 
> Quando implementarmos, o número será real."

### Para Stakeholders
> "Priorizamos integridade. Cada métrica é verificável no banco.
> Sem fumaça e espelhos."

### Para Investidores
> "Mostramos a realidade. Quando dissermos 1000 agentes ativos,
> você pode verificar no banco."

---

## Referências

- [HONESTY.md](../../policies/HONESTY.md) - Documento completo da política
- Inspiração: Stripe, Linear, Vercel (empresas conhecidas por honestidade)

