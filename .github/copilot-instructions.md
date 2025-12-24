# ALSHAM QUANTUM - GitHub Copilot Instructions

Este arquivo contém instruções para o GitHub Copilot ao trabalhar neste repositório.

## Contexto do Projeto

ALSHAM QUANTUM é uma plataforma enterprise de CRM/AutoML com:
- 139 agentes de IA
- 27 tabelas no banco de dados
- 25 páginas no frontend
- Padrões FAANG de qualidade

## Regras Obrigatórias

### 1. Data Honesty
```
❌ NUNCA: const agents = 42; // hardcoded
✅ SEMPRE: const { data } = await supabase.from('agents').select('*');
```

### 2. TypeScript Strict
```
❌ NUNCA: function process(data: any): any
✅ SEMPRE: function process(data: Agent[]): ProcessResult
```

### 3. Zustand para State
```
❌ NUNCA: const MyContext = createContext(null);
✅ SEMPRE: const useStore = create<Store>()((set) => ({ ... }));
```

### 4. Error Handling
```
❌ NUNCA: const data = await fetch(url);
✅ SEMPRE: try { const data = await fetch(url); } catch (err) { ... }
```

### 5. Conventional Commits
```
❌ NUNCA: git commit -m "fix stuff"
✅ SEMPRE: git commit -m "fix(auth): resolve session issue"
```

## Stack Tecnológico

- Frontend: Next.js 16 + React 19 + TypeScript 5 + Tailwind
- State: Zustand 5 (devtools + persist)
- Backend: Supabase (PostgreSQL + Auth + Realtime)
- Deploy: Vercel + Railway

## Padrões de Código

### Zustand Store
```typescript
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface StoreState {
  items: Item[];
  loading: boolean;
  setItems: (items: Item[]) => void;
}

export const useItemStore = create<StoreState>()(
  devtools(
    persist(
      (set) => ({
        items: [],
        loading: false,
        setItems: (items) => set({ items }, false, 'items/setItems'),
      }),
      { name: 'item-storage' }
    ),
    { name: 'ItemStore' }
  )
);
```

### Custom Hook
```typescript
import { useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { useItemStore } from '@/stores';

export function useItems() {
  const store = useItemStore();

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      store.setState({ loading: true });
      const { data, error } = await supabase.from('items').select('*');
      if (error) throw error;
      store.setItems(data || []);
    } catch (err) {
      console.error('fetchItems failed:', err);
    } finally {
      store.setState({ loading: false });
    }
  };

  return { ...store, refetch: fetchItems };
}
```

### Page Component
```typescript
"use client";

import { useItems } from '@/hooks/useItems';

export default function ItemsPage() {
  const { items, loading } = useItems();

  if (loading) {
    return <div className="animate-pulse">Loading...</div>;
  }

  return (
    <div className="grid gap-4">
      {items.map((item) => (
        <div key={item.id} className="p-4 rounded-lg bg-card">
          {item.name}
        </div>
      ))}
    </div>
  );
}
```

## Estrutura de Arquivos

```
frontend/src/
├── app/              # Páginas Next.js (App Router)
│   ├── dashboard/    # Páginas do dashboard
│   └── api/          # API routes
├── components/       # Componentes React
│   ├── ui/           # Componentes base (button, card, etc)
│   └── quantum/      # Componentes específicos
├── stores/           # Zustand stores
├── hooks/            # Custom hooks
├── lib/              # Utilitários (supabase, utils)
└── types/            # TypeScript types
```

## Documentação

Antes de fazer mudanças significativas, consulte:
- `docs/policies/ARCHITECTURE-STANDARDS.md` - Padrões obrigatórios
- `docs/policies/HONESTY.md` - Política de dados reais
- `docs/architecture/decisions/` - ADRs (decisões arquiteturais)

## Problema Conhecido

O sistema de login tem um problema de cookie/sessão. O cliente usa `@supabase/supabase-js` que salva em localStorage, mas o middleware espera cookie `sb-*-auth-token`.

Solução pendente: Migrar para `@supabase/ssr` ou ajustar middleware.

## Filosofia

> "Código de empresa bilionária. Padrões FAANG. Zero paliativos."

Cada linha de código deve ser digna de code review do Google/Meta/Stripe.

