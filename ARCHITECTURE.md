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

---

### 2️⃣ TYPESCRIPT

**RULE:** Strict mode, no 'any', all types explicit

**FORBIDDEN:** any, implicit types, non-null assertions without checks

---

### 3️⃣ ERROR HANDLING

**RULE:** All async operations in try/catch with user notification

---

### 4️⃣ PERFORMANCE

**RULE:** useMemo for expensive calcs, React.memo for components, debounce inputs

---

### 5️⃣ DATA HONESTY

**RULE:** Show real data or 0. Never mock in production.

---

### 6️⃣ NAMING

- Components: PascalCase
- Hooks/Stores: camelCase with 'use'
- Constants: UPPER_SNAKE_CASE
- Functions: camelCase

---

### 7️⃣ GIT COMMITS

**Format:** type(scope): description

Types: feat, fix, docs, refactor, perf, test, chore

---

### 8️⃣ SECURITY

**RULE:** No committed keys, validate all inputs, RLS on tables

---

## ✅ CODE REVIEW CHECKLIST

Before ANY commit:
- [ ] TypeScript strict passes
- [ ] No ESLint errors
- [ ] Follows naming
- [ ] Uses Zustand store
- [ ] Has error handling
- [ ] Performance optimized
- [ ] No mocked data
- [ ] Conventional commit

**If ANY fails → REJECTED**

---

**Last Updated:** 2025-11-25  
**Enforced by:** ALSHAM GLOBAL  
**Compliance:** 100% MANDATORY
