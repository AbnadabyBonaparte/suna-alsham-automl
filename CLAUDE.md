# 🤖 CLAUDE.md - Instruções para IA

**Este arquivo é lido automaticamente por Claude (Anthropic) e outros assistentes de IA.**

---

## 🚨 LEIA PRIMEIRO - REGRAS INVIOLÁVEIS

### 1. DATA HONESTY (Lei Suprema)
```
NUNCA sugira dados fake em produção.
NUNCA hardcode métricas (12ms, 99.9%, 42 agentes).
SEMPRE mostre 0 quando é 0.
SEMPRE use queries reais ao banco.
```

### 2. PADRÕES FAANG
```
SEMPRE TypeScript strict (zero 'any').
SEMPRE Zustand para state (NUNCA Context API).
SEMPRE try/catch em async.
SEMPRE conventional commits.
```

### 3. ANTES DE CODAR
```
LEIA docs/policies/ARCHITECTURE-STANDARDS.md
LEIA docs/policies/HONESTY.md
VERIFIQUE docs/project/PROGRESS.md para estado atual
```

---

## 📂 Estrutura do Projeto

```
suna-alsham-automl/
├── frontend/                 # Next.js 16 + React 19
│   ├── src/
│   │   ├── app/              # 25 páginas (App Router)
│   │   ├── components/       # Componentes React
│   │   ├── stores/           # 12 Zustand stores
│   │   ├── hooks/            # 20+ custom hooks
│   │   └── lib/              # Supabase, utils
│   └── docs/                 # Docs legados (migrar para /docs)
├── backend/                  # FastAPI (Python)
├── supabase/                 # Migrations + Edge Functions
├── docs/                     # 📚 DOCUMENTAÇÃO PRINCIPAL
│   ├── architecture/         # Decisões técnicas + ADRs
│   ├── operations/           # Deploy, handoff, runbooks
│   ├── policies/             # Padrões obrigatórios
│   └── project/              # Progresso, changelog
└── *.md                      # Docs de alto nível
```

---

## 🎯 Estado Atual do Projeto

| Métrica | Valor |
|---------|-------|
| Progresso | ~85% |
| Páginas Funcionais | 16 de 25 |
| Agentes Configurados | 139 |
| Tabelas no Banco | 27 |
| Zustand Stores | 12 |

### ⚠️ Problema Crítico Atual
**Login/Cookie:** O cliente usa `@supabase/supabase-js` (localStorage) mas o middleware espera cookie. Sessão não persiste entre requests server-side.

---

## 🛠️ Stack Tecnológico

```yaml
Frontend:
  - Next.js: 16.0.3 (App Router + Turbopack)
  - React: 19.2.0
  - TypeScript: 5.x (strict mode)
  - Tailwind CSS: 3.x
  - Zustand: 5.x (state management)
  - Framer Motion: (animações)

Backend:
  - Supabase: PostgreSQL + Auth + Realtime + Storage
  - Edge Functions: Deno runtime
  - Cron Jobs: pg_cron

Deploy:
  - Frontend: Vercel
  - Workers: Railway
  - Database: Supabase Cloud
```

---

## 📋 Padrões de Código

### Zustand Store (OBRIGATÓRIO)
```typescript
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface MyStore {
  data: Data[];
  loading: boolean;
  setData: (data: Data[]) => void;
}

export const useMyStore = create<MyStore>()(
  devtools(
    persist(
      (set) => ({
        data: [],
        loading: false,
        setData: (data) => set({ data }, false, 'my/setData'),
      }),
      { name: 'my-storage' }
    ),
    { name: 'MyStore' }
  )
);
```

### Custom Hook (OBRIGATÓRIO)
```typescript
import { useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { useMyStore } from '@/stores';

export function useMyData() {
  const { data, loading, setData } = useMyStore();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      useMyStore.setState({ loading: true });
      const { data, error } = await supabase.from('table').select('*');
      if (error) throw error;
      setData(data || []);
    } catch (err) {
      console.error('fetchData failed:', err);
    } finally {
      useMyStore.setState({ loading: false });
    }
  };

  return { data, loading, refetch: fetchData };
}
```

### Página (OBRIGATÓRIO)
```typescript
"use client";

import { useMyData } from '@/hooks/useMyData';

export default function MyPage() {
  const { data, loading } = useMyData();

  if (loading) return <LoadingSkeleton />;

  return (
    <div>
      {data.map(item => (
        <Card key={item.id}>{item.name}</Card>
      ))}
    </div>
  );
}
```

---

## ❌ O QUE NUNCA FAZER

```typescript
// ❌ NUNCA - Dados fake
const agents = 42;
const latency = 12;

// ❌ NUNCA - any
function process(data: any): any { }

// ❌ NUNCA - Context API para state
const MyContext = createContext(null);

// ❌ NUNCA - useState para estado compartilhado
const [globalData, setGlobalData] = useState([]);

// ❌ NUNCA - Async sem try/catch
const data = await supabase.from('table').select('*');

// ❌ NUNCA - Console.log em produção
console.log('debug:', data);

// ❌ NUNCA - Commits sem padrão
git commit -m "fix stuff"
```

---

## ✅ O QUE SEMPRE FAZER

```typescript
// ✅ SEMPRE - Dados reais
const { data } = await supabase.from('agents').select('*');
const count = data?.length || 0;

// ✅ SEMPRE - Tipos explícitos
function process(data: Agent[]): ProcessResult { }

// ✅ SEMPRE - Zustand
const useStore = create<Store>()((set) => ({ ... }));

// ✅ SEMPRE - Try/catch
try {
  const { data, error } = await supabase.from('table').select('*');
  if (error) throw error;
} catch (err) {
  console.error('Operation failed:', err);
}

// ✅ SEMPRE - Conventional commits
git commit -m "feat(agents): add filter by squad"
git commit -m "fix(auth): resolve session cookie issue"
```

---

## 📚 Documentação Essencial

| Documento | Caminho | Quando Ler |
|-----------|---------|------------|
| Padrões de Arquitetura | `docs/policies/ARCHITECTURE-STANDARDS.md` | Antes de qualquer código |
| Política de Honestidade | `docs/policies/HONESTY.md` | Antes de mostrar dados |
| Progresso Atual | `docs/project/PROGRESS.md` | Para saber estado atual |
| Guia de Deploy | `docs/operations/DEPLOYMENT.md` | Para fazer deploy |
| Handoff | `docs/operations/HANDOFF.md` | Para contexto completo |
| ADRs | `docs/architecture/decisions/` | Para entender decisões |

---

## 🔧 Comandos Úteis

```powershell
# Desenvolvimento
cd frontend
npm run dev          # http://localhost:3000

# Build
npm run build        # Testar antes de commit

# Deploy
git add -A
git commit -m "type(scope): description"
git push origin main # Vercel deploya automaticamente

# Verificar tipos
npx tsc --noEmit
```

---

## 🎖️ Filosofia

> "ALSHAM QUANTUM não é um projeto. É a fundação de uma empresa bilionária.
> Cada linha de código deve ser digna de code review do Google."

**Princípios:**
1. **Honestidade** - Dados reais, sempre
2. **Qualidade** - FAANG-level, sem exceções
3. **Escalabilidade** - Código que dura anos
4. **Documentação** - Próximo dev entende em < 1 dia

---

**Versão:** 1.0.0  
**Atualizado:** 2025-12-23  
**Mantido por:** ALSHAM GLOBAL

