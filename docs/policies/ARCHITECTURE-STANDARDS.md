# 🏗️ ARCHITECTURE STANDARDS - ALSHAM QUANTUM

**🚨 MANDATORY FOR 100% OF THE PROJECT - NO EXCEPTIONS 🚨**

---

## ⚠️ CRITICAL NOTICE

**THIS IS NOT A SUGGESTION. THIS IS LAW.**

Every single line of code in this project - past, present, and future - MUST follow these standards.

**Scope:**
- ✅ ALL new features
- ✅ ALL bug fixes  
- ✅ ALL refactoring
- ✅ ALL existing code (will be migrated)
- ✅ ALL pull requests
- ✅ ALL commits

**Enforcement:**
- Any code not following these standards WILL BE REJECTED
- Existing code not meeting standards MUST BE REFACTORED
- No compromise. No shortcuts. No exceptions.

---

## 🎯 WHY ENTERPRISE-GRADE?

**We build like FAANG companies: Google, Meta, Stripe, Vercel, Linear**

This ensures:
- Code maintainable for years
- New developers onboard in <1 day
- Bugs reduced by 90%
- Performance predictable
- System scales without rewrite

---

## 📋 MANDATORY STANDARDS

### 1️⃣ STATE MANAGEMENT

**RULE:** All shared state uses Zustand with devtools + persist

**Example:**
```typescript
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

export const useMyStore = create<MyStore>()(
  devtools(
    persist(
      (set, get) => ({
        data: null,
        loading: false,
        
        setData: (data) => set({ data }, false, 'my/setData'),
        getData: () => get().data,
      }),
      { name: 'my-storage' }
    ),
    { name: 'MyStore' }
  )
);
```

**FORBIDDEN:** useState for shared data, Context API, global variables

**ADR:** [001-zustand-over-redux](../architecture/decisions/001-zustand-over-redux.md), [006-no-context-api](../architecture/decisions/006-no-context-api.md)

---

### 2️⃣ TYPESCRIPT

**RULE:** Strict mode, no 'any', all types explicit

```typescript
// ✅ CORRECT
interface Agent {
  id: string;
  name: string;
  efficiency: number;
}

function processAgent(agent: Agent): ProcessResult {
  // ...
}

// ❌ FORBIDDEN
function processAgent(agent: any): any {
  // ...
}
```

**FORBIDDEN:** any, implicit types, non-null assertions without checks

**ADR:** [004-typescript-strict-mode](../architecture/decisions/004-typescript-strict-mode.md)

---

### 3️⃣ ERROR HANDLING

**RULE:** All async operations in try/catch with user notification

```typescript
// ✅ CORRECT
async function fetchData() {
  try {
    const { data, error } = await supabase.from('table').select('*');
    if (error) throw error;
    return data;
  } catch (err) {
    console.error('fetchData failed:', err);
    toast.error('Failed to load data');
    throw err;
  }
}

// ❌ FORBIDDEN
async function fetchData() {
  const { data } = await supabase.from('table').select('*');
  return data;
}
```

---

### 4️⃣ PERFORMANCE

**RULE:** useMemo for expensive calcs, React.memo for components, debounce inputs

```typescript
// ✅ CORRECT
const expensiveResult = useMemo(() => {
  return heavyCalculation(data);
}, [data]);

const AgentCard = React.memo(function AgentCard({ agent }: Props) {
  return <div>{agent.name}</div>;
});

const debouncedSearch = useMemo(
  () => debounce((term: string) => search(term), 300),
  []
);
```

---

### 5️⃣ DATA HONESTY

**RULE:** Show real data or 0. Never mock in production.

```typescript
// ✅ CORRECT
const { data: agents } = await supabase
  .from('agents')
  .select('*')
  .eq('status', 'running');
const activeCount = agents?.length || 0; // Can be 0, and that's OK

// ❌ FORBIDDEN
const activeCount = 42; // Hardcoded fake data
```

**ADR:** [003-data-honesty-policy](../architecture/decisions/003-data-honesty-policy.md)

**Policy:** [HONESTY.md](./HONESTY.md)

---

### 6️⃣ NAMING

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `AgentCard`, `DashboardShell` |
| Hooks/Stores | camelCase with 'use' | `useAgents`, `useAgentsStore` |
| Constants | UPPER_SNAKE_CASE | `MAX_AGENTS`, `API_URL` |
| Functions | camelCase | `fetchAgents`, `processData` |
| Files (components) | PascalCase | `AgentCard.tsx` |
| Files (utils) | camelCase | `supabase.ts`, `utils.ts` |

---

### 7️⃣ GIT COMMITS

**Format:** `type(scope): description`

**Types:**
| Type | When to use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Adding tests |
| `chore` | Maintenance |

**Examples:**
```bash
feat(agents): add filter by squad
fix(auth): resolve session cookie issue
docs(readme): update deployment instructions
refactor(dashboard): extract metrics hook
```

---

### 8️⃣ SECURITY

**RULE:** No committed keys, validate all inputs, RLS on tables

```typescript
// ✅ CORRECT - Environment variables
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// ✅ CORRECT - Input validation
const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
});

// ❌ FORBIDDEN - Hardcoded keys
const supabase = createClient(
  'https://xxx.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
);
```

---

## ✅ CODE REVIEW CHECKLIST

Before ANY commit:
- [ ] TypeScript strict passes (`npm run build`)
- [ ] No ESLint errors
- [ ] Follows naming conventions
- [ ] Uses Zustand store (not Context)
- [ ] Has error handling (try/catch)
- [ ] Performance optimized (memo, debounce)
- [ ] No mocked data in production
- [ ] Conventional commit message

**If ANY fails → REJECTED**

See full checklist: [CODE-REVIEW-CHECKLIST.md](./CODE-REVIEW-CHECKLIST.md)

---

## 📚 Related Documents

- [ADR-001: Zustand over Redux](../architecture/decisions/001-zustand-over-redux.md)
- [ADR-003: Data Honesty Policy](../architecture/decisions/003-data-honesty-policy.md)
- [ADR-004: TypeScript Strict Mode](../architecture/decisions/004-typescript-strict-mode.md)
- [ADR-005: FAANG-Level Standards](../architecture/decisions/005-faang-level-standards.md)
- [ADR-006: No Context API](../architecture/decisions/006-no-context-api.md)
- [HONESTY.md](./HONESTY.md)

---

**Last Updated:** 2025-12-23  
**Enforced by:** ALSHAM GLOBAL  
**Compliance:** 100% MANDATORY

