# ADR-006: No Context API for State Management

**Status:** ✅ Aceita  
**Data:** 2025-11-25  
**Decisores:** ALSHAM GLOBAL Tech Team

---

## Contexto

React Context API é frequentemente usado para state management. No entanto, para aplicações enterprise como ALSHAM QUANTUM, precisávamos avaliar se é a escolha correta.

---

## Decisão

**NÃO usar Context API para state management. Usar Zustand exclusivamente.**

Exceção única: AuthContext legado (será migrado para Zustand).

```typescript
// ❌ PROIBIDO
const MyContext = createContext<State | null>(null);

export function MyProvider({ children }) {
  const [state, setState] = useState(initialState);
  return (
    <MyContext.Provider value={{ state, setState }}>
      {children}
    </MyContext.Provider>
  );
}

// ✅ OBRIGATÓRIO
import { create } from 'zustand';

export const useMyStore = create<MyStore>()((set) => ({
  state: initialState,
  setState: (newState) => set({ state: newState }),
}));
```

---

## Alternativas Consideradas

### 1. Context API
- **Prós:** 
  - Nativo do React
  - Sem dependências
  - Simples para casos básicos
- **Contras:** 
  - Re-renders em cascata
  - Não escala
  - Sem DevTools
  - Difícil de debugar
  - Performance ruim

### 2. Context + useReducer
- **Prós:**
  - Mais estruturado que Context puro
  - Pattern conhecido (Redux-like)
- **Contras:**
  - Ainda tem re-renders
  - Boilerplate
  - Sem persist nativo

### 3. Zustand ✅
- **Prós:**
  - Zero re-renders desnecessários
  - DevTools integrado
  - Persist nativo
  - TypeScript excelente
  - Simples de usar
  - Escala bem
- **Contras:**
  - Dependência externa

---

## Consequências

### Positivas
- ✅ Performance superior (selective re-renders)
- ✅ DevTools para debugging
- ✅ Persist para localStorage trivial
- ✅ Código mais limpo
- ✅ Escala para 100+ stores
- ✅ Consistência no codebase

### Negativas
- ⚠️ AuthContext legado precisa ser migrado
- ⚠️ Devs precisam aprender Zustand

---

## Problema do Context API

### Re-renders em Cascata
```typescript
// Context API - PROBLEMA
const AppContext = createContext(null);

function App() {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('dark');
  const [agents, setAgents] = useState([]);
  
  // PROBLEMA: Qualquer mudança re-renderiza TODOS os consumers
  return (
    <AppContext.Provider value={{ user, theme, agents, setUser, setTheme, setAgents }}>
      <Dashboard />   {/* Re-renderiza quando theme muda */}
      <AgentList />   {/* Re-renderiza quando user muda */}
      <Settings />    {/* Re-renderiza quando agents muda */}
    </AppContext.Provider>
  );
}
```

### Zustand - Solução
```typescript
// Zustand - CORRETO
const useUserStore = create((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}));

const useThemeStore = create((set) => ({
  theme: 'dark',
  setTheme: (theme) => set({ theme }),
}));

// Cada componente só re-renderiza quando SEU estado muda
function Dashboard() {
  const theme = useThemeStore((s) => s.theme); // Só re-renderiza com theme
  return <div className={theme}>...</div>;
}

function AgentList() {
  const agents = useAgentsStore((s) => s.agents); // Só re-renderiza com agents
  return <ul>{agents.map(...)}</ul>;
}
```

---

## Migração do AuthContext

### Estado Atual (Legado)
```typescript
// contexts/AuthContext.tsx - SERÁ MIGRADO
export const AuthContext = createContext<AuthContextType | null>(null);
```

### Estado Futuro
```typescript
// stores/useAuthStore.ts - MIGRAR PARA ISSO
export const useAuthStore = create<AuthStore>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        session: null,
        setUser: (user) => set({ user }),
        setSession: (session) => set({ session }),
        signOut: () => set({ user: null, session: null }),
      }),
      { name: 'auth-storage' }
    ),
    { name: 'AuthStore' }
  )
);
```

---

## Referências

- [ADR-001: Zustand over Redux](./001-zustand-over-redux.md)
- [Why Context is Not Good for State Management](https://blog.isquaredsoftware.com/2021/01/context-redux-differences/)
- [Zustand vs Context Performance](https://github.com/pmndrs/zustand/discussions/912)

