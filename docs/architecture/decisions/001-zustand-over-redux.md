# ADR-001: Zustand over Redux

**Status:** ✅ Aceita  
**Data:** 2025-11-25  
**Decisores:** ALSHAM GLOBAL Tech Team

---

## Contexto

O ALSHAM QUANTUM precisa de gerenciamento de estado global para:
- 139 agentes de IA com status em tempo real
- Dashboard com métricas live
- Múltiplas páginas compartilhando dados
- Preferências de usuário persistidas

Precisávamos escolher entre as opções disponíveis no ecossistema React.

---

## Decisão

**Usar Zustand como única solução de state management.**

```typescript
// Padrão adotado
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

export const useAgentsStore = create<AgentsStore>()(
  devtools(
    persist(
      (set, get) => ({
        agents: [],
        loading: false,
        setAgents: (agents) => set({ agents }, false, 'agents/setAgents'),
      }),
      { name: 'agents-storage' }
    ),
    { name: 'AgentsStore' }
  )
);
```

---

## Alternativas Consideradas

### 1. Redux Toolkit
- **Prós:** Ecossistema maduro, DevTools excelentes, muita documentação
- **Contras:** Boilerplate excessivo, curva de aprendizado, slices/reducers/actions

### 2. Jotai
- **Prós:** Atômico, simples, bom para estado derivado
- **Contras:** Menos maduro, menos padrões estabelecidos

### 3. React Context API
- **Prós:** Nativo, sem dependências
- **Contras:** Re-renders desnecessários, não escala, sem DevTools

### 4. Zustand ✅
- **Prós:** 
  - Zero boilerplate
  - DevTools integrado
  - Persist middleware nativo
  - TypeScript first-class
  - 2KB gzipped
  - Não causa re-renders desnecessários
- **Contras:** 
  - Menos conhecido que Redux
  - Menos middleware disponível

---

## Consequências

### Positivas
- ✅ Código 70% menor que equivalente Redux
- ✅ Onboarding de devs em minutos (vs horas com Redux)
- ✅ DevTools funcionando out-of-the-box
- ✅ Persist para localStorage trivial
- ✅ TypeScript inference excelente
- ✅ Performance superior (selective re-renders)

### Negativas
- ⚠️ Devs acostumados com Redux precisam adaptar
- ⚠️ Menos recursos de aprendizado disponíveis
- ⚠️ Middleware ecosystem menor

---

## Implementação

### Stores Criadas (12 total)
```
useAgentsStore      - 139 agentes
useDashboardStore   - Métricas real-time
useRequestsStore    - CRUD de requests
useSalesStore       - Pipeline de vendas
useSupportStore     - Tickets de suporte
useAnalyticsStore   - Analytics
useAuthStore        - Autenticação
useProfileStore     - Perfil do usuário
useUIStore          - Preferências UI
useAppStore         - Estado global
useLoadingStore     - Estados de loading
useNotificationStore - Notificações
```

### Padrão Obrigatório
```typescript
// SEMPRE usar devtools para debugging
// SEMPRE usar persist para dados que precisam sobreviver refresh
// SEMPRE nomear actions para rastreabilidade
set({ data }, false, 'store/actionName')
```

---

## Referências

- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [Why Zustand over Redux](https://blog.logrocket.com/zustand-vs-redux/)
- [ARCHITECTURE.md](../../policies/ARCHITECTURE-STANDARDS.md)

