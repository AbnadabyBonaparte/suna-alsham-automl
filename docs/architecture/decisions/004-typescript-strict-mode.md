# ADR-004: TypeScript Strict Mode

**Status:** ✅ Aceita  
**Data:** 2025-11-20  
**Decisores:** ALSHAM GLOBAL Tech Team

---

## Contexto

TypeScript oferece diferentes níveis de rigor:
- Modo padrão (permissivo)
- Modo strict (rigoroso)
- Configurações individuais

Precisávamos decidir qual nível adotar para o projeto.

---

## Decisão

**TypeScript strict mode obrigatório. Zero `any`. Tipos explícitos sempre.**

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

---

## Alternativas Consideradas

### 1. Modo Padrão (Permissivo)
- **Prós:** 
  - Mais rápido para desenvolver
  - Menos erros de compilação
  - Mais flexível
- **Contras:** 
  - Bugs em runtime
  - `any` se espalha
  - Autocompletar ruim

### 2. Strict Parcial
- **Prós:**
  - Meio termo
  - Gradual adoption
- **Contras:**
  - Inconsistência
  - Difícil de manter

### 3. Strict Total ✅
- **Prós:**
  - Bugs detectados em compile time
  - Autocompletar excelente
  - Refactoring seguro
  - Documentação viva
  - Onboarding facilitado
- **Contras:**
  - Mais tempo inicial
  - Curva de aprendizado

---

## Consequências

### Positivas
- ✅ 90% menos bugs em runtime
- ✅ Refactoring com confiança
- ✅ IDE mostra erros instantaneamente
- ✅ Tipos servem como documentação
- ✅ Novos devs entendem o código mais rápido
- ✅ Autocompletar funciona perfeitamente

### Negativas
- ⚠️ Tempo inicial maior para tipar tudo
- ⚠️ Alguns pacotes npm não têm tipos
- ⚠️ Curva de aprendizado para devs júnior

---

## Implementação

### Padrões Obrigatórios

```typescript
// ✅ CORRETO - Tipos explícitos
interface Agent {
  id: string;
  name: string;
  efficiency: number;
  status: 'running' | 'stopped' | 'warning';
}

function processAgent(agent: Agent): ProcessResult {
  // ...
}

// ❌ PROIBIDO - any
function processAgent(agent: any): any {
  // ...
}

// ❌ PROIBIDO - Tipos implícitos
function processAgent(agent) {
  // ...
}
```

### Null Checks
```typescript
// ✅ CORRETO - Null check explícito
const agent = agents.find(a => a.id === id);
if (!agent) {
  throw new Error('Agent not found');
}
// agent é garantido não-null aqui

// ❌ PROIBIDO - Non-null assertion sem check
const agent = agents.find(a => a.id === id)!;
```

### Tipos de Retorno
```typescript
// ✅ CORRETO - Retorno explícito
async function fetchAgents(): Promise<Agent[]> {
  const { data } = await supabase.from('agents').select('*');
  return data || [];
}

// ❌ PROIBIDO - Retorno implícito
async function fetchAgents() {
  const { data } = await supabase.from('agents').select('*');
  return data;
}
```

---

## Verificação

### Build Check
```bash
npm run build
# Deve passar sem erros de tipo
```

### Buscar Violações
```bash
# Buscar 'any' no código
grep -r "any" src/ --include="*.ts" --include="*.tsx"

# Buscar @ts-ignore
grep -r "@ts-ignore" src/ --include="*.ts" --include="*.tsx"

# Buscar non-null assertions suspeitos
grep -r "!\." src/ --include="*.ts" --include="*.tsx"
```

---

## Referências

- [TypeScript Strict Mode](https://www.typescriptlang.org/tsconfig#strict)
- [tsconfig.json do projeto](../../../frontend/tsconfig.json)

