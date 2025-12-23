# ADR-005: FAANG-Level Standards

**Status:** ✅ Aceita  
**Data:** 2025-11-25  
**Decisores:** ALSHAM GLOBAL Leadership

---

## Contexto

ALSHAM QUANTUM não é um projeto comum. É a fundação de uma empresa que pretende ser bilionária. Código medíocre não é aceitável.

Precisávamos definir um padrão de qualidade que:
- Escale para milhões de usuários
- Seja mantido por anos
- Permita onboarding rápido de novos devs
- Resista a auditorias técnicas

---

## Decisão

**Adotar padrões de qualidade equivalentes a Google, Meta, Stripe, Vercel, Linear.**

Isso significa:
- Código que passa em code review de Big Tech
- Arquitetura que escala sem rewrite
- Documentação que permite onboarding em < 1 dia
- Testes que garantem estabilidade
- CI/CD que previne bugs em produção

---

## Alternativas Consideradas

### 1. "Move Fast and Break Things"
- **Prós:** 
  - Velocidade inicial
  - Menos burocracia
- **Contras:** 
  - Dívida técnica explosiva
  - Rewrite inevitável
  - Bugs em produção

### 2. Padrão Startup Comum
- **Prós:**
  - Mais rápido
  - Menos rigoroso
- **Contras:**
  - Não escala
  - Difícil de manter
  - Onboarding lento

### 3. FAANG-Level ✅
- **Prós:**
  - Escala infinita
  - Manutenção fácil
  - Onboarding rápido
  - Auditorias passam
  - Investidores impressionados
- **Contras:**
  - Mais tempo inicial
  - Mais rigor

---

## Consequências

### Positivas
- ✅ Código mantido por anos sem rewrite
- ✅ Novos devs produtivos em < 1 dia
- ✅ Bugs reduzidos em 90%
- ✅ Performance previsível
- ✅ Auditorias técnicas passam
- ✅ Investidores confiam na engenharia

### Negativas
- ⚠️ Tempo inicial maior
- ⚠️ Mais rigor no code review
- ⚠️ Curva de aprendizado para devs júnior

---

## Implementação

### 1. Code Style
```typescript
// Naming
ComponentName      // PascalCase para componentes
useHookName        // camelCase com 'use' para hooks
CONSTANT_VALUE     // UPPER_SNAKE_CASE para constantes
functionName       // camelCase para funções
```

### 2. Error Handling
```typescript
// ✅ OBRIGATÓRIO - Try/catch em async
async function fetchData() {
  try {
    const { data, error } = await supabase.from('table').select('*');
    if (error) throw error;
    return data;
  } catch (err) {
    console.error('fetchData failed:', err);
    // Notificar usuário ou sistema de monitoramento
    throw err;
  }
}
```

### 3. Performance
```typescript
// ✅ OBRIGATÓRIO - Memoização para cálculos pesados
const expensiveResult = useMemo(() => {
  return heavyCalculation(data);
}, [data]);

// ✅ OBRIGATÓRIO - React.memo para componentes puros
const AgentCard = React.memo(function AgentCard({ agent }: Props) {
  return <div>{agent.name}</div>;
});

// ✅ OBRIGATÓRIO - Debounce para inputs
const debouncedSearch = useMemo(
  () => debounce((term: string) => search(term), 300),
  []
);
```

### 4. Git Commits
```bash
# Formato: type(scope): description
feat(agents): add filter by squad
fix(auth): resolve cookie session issue
docs(readme): update deployment instructions
refactor(dashboard): extract metrics hook
perf(network): optimize graph rendering
test(requests): add CRUD integration tests
chore(deps): update supabase to 2.x
```

### 5. Security
```typescript
// ✅ OBRIGATÓRIO - Nunca commitar keys
// .env.local (gitignored)
SUPABASE_SERVICE_ROLE_KEY=xxx

// ✅ OBRIGATÓRIO - Validar inputs
const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
});

// ✅ OBRIGATÓRIO - RLS em todas as tabelas
ALTER TABLE public.agents ENABLE ROW LEVEL SECURITY;
```

---

## Checklist de Code Review

Antes de aprovar qualquer PR:

- [ ] TypeScript strict passa
- [ ] Zero erros de ESLint
- [ ] Naming conventions seguidas
- [ ] Zustand para estado compartilhado
- [ ] Error handling em async
- [ ] Performance otimizada (memo, debounce)
- [ ] Sem dados mockados em produção
- [ ] Commit message convencional
- [ ] Documentação atualizada

**Se QUALQUER item falhar → PR REJEITADO**

---

## Referências

- [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Vercel Engineering Blog](https://vercel.com/blog)
- [ARCHITECTURE-STANDARDS.md](../../policies/ARCHITECTURE-STANDARDS.md)

