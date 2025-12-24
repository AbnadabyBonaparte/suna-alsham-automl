# 🔄 SESSION HANDOFF - ALSHAM QUANTUM

**Critical context transfer document for next developer or AI assistant.**

---

## 🚨 READ THIS FIRST

You are taking over an **~85% complete enterprise application** with strict quality standards.

**User Profile:**
- Company: ALSHAM GLOBAL
- Location: Fortaleza, Ceará, Brazil
- Language: Portuguese (comfortable with English)
- Skill Level: Technical leader with strong opinions
- Work Style: Methodical, values quality over speed
- Expectations: FAANG-level code, complete explanations

---

## 📊 Current State

### What's Working (DON'T BREAK!)

| Component | Status | Notes |
|-----------|--------|-------|
| Dashboard | ✅ 100% | Real metrics, live latency |
| Agents Page | ✅ 100% | 139 agents, filters, modals |
| Agent Detail | ✅ 100% | Real data by ID |
| Requests | ✅ 100% | Full CRUD |
| Analytics | ✅ 100% | Real graphs |
| Evolution | ✅ 100% | DNA + real data |
| Network | ✅ 100% | Real Supabase latency |
| API Tester | ✅ 100% | Syntax highlighting |
| Settings | ✅ 100% | 4 tabs, saves to DB |
| Admin | ✅ 100% | God mode, real users |
| Sales | ✅ 100% | Pipeline, ECG chart |
| Support | ✅ 100% | Tickets, hexagonal hive |
| Authentication | ⚠️ 90% | Cookie issue (see below) |

### What's NOT Working

| Issue | Severity | Status |
|-------|----------|--------|
| Login cookie/session | 🔴 Critical | See [runbook](./runbooks/auth-login-failure.md) |
| OAuth providers | 🟡 Medium | Configured, not enabled |
| 9 "Coming Soon" pages | 🟢 Low | Visual placeholders |

---

## 🎯 Project Philosophy

### The Golden Rules

1. **DATA HONESTY IS LAW**
   - NEVER suggest fake data
   - Show 0 when there's 0
   - Real latency > fake numbers

2. **FAANG-LEVEL QUALITY**
   - Read [ARCHITECTURE-STANDARDS.md](../policies/ARCHITECTURE-STANDARDS.md) FIRST
   - TypeScript strict, no `any`
   - Conventional commits ALWAYS

3. **ZUSTAND FOR EVERYTHING**
   - No Redux, no Context API
   - 12 stores already created
   - Follow existing patterns

4. **INCREMENTAL DEVELOPMENT**
   - Test locally (`npm run dev`)
   - Build before commit (`npm run build`)
   - Test in production after deploy

---

## 🛠️ Technical Stack

```
Frontend:
├── Next.js 16.0.3 (App Router + Turbopack)
├── React 19.2.0
├── TypeScript 5.x (strict mode)
├── Tailwind CSS
└── Zustand 5.x (12 stores)

Backend:
├── Supabase (PostgreSQL + Auth + Realtime)
├── 27 tables, 70+ RLS policies
└── 3 Edge Functions, 4 Cron Jobs

Deployment:
├── Vercel (auto-deploy on push)
├── Production: quantum.alshamglobal.com.br
└── Build time: ~30 seconds
```

---

## 📋 Common Commands

```powershell
# Navigate to project
cd "C:\Users\abnad\OneDrive\Área de Trabalho\SUNA\ALSHAM QUANTUM REVIVER\suna-alsham-automl"

# Start dev server
cd frontend
npm run dev
# Access: http://localhost:3000

# Build for production
npm run build

# Commit changes
cd ..
git add -A
git commit -m "type(scope): description"
git push origin main
```

---

## ⚠️ Common Pitfalls

### DON'T DO THIS
- ❌ Skip local testing before commit
- ❌ Use `any` type in TypeScript
- ❌ Suggest fake/mocked data
- ❌ Use Context API for state
- ❌ Forget to read ARCHITECTURE-STANDARDS.md

### DO THIS
- ✅ Test locally ALWAYS
- ✅ Build before commit
- ✅ Use Zustand for state
- ✅ Follow existing patterns
- ✅ Ask before major changes

---

## 📂 Key Files

| File | Purpose |
|------|---------|
| `docs/policies/ARCHITECTURE-STANDARDS.md` | Mandatory code standards |
| `docs/policies/HONESTY.md` | Data honesty policy |
| `docs/project/PROGRESS.md` | Current progress |
| `docs/architecture/decisions/` | ADRs |
| `frontend/src/stores/` | All Zustand stores |
| `frontend/src/hooks/` | Custom hooks |

---

## 🎯 Next Session Recommendations

### High Priority
1. **Fix Login Cookie Issue** - See [runbook](./runbooks/auth-login-failure.md)
2. **Enable OAuth** - Google/GitHub configured, needs activation

### Medium Priority
3. **Complete 9 "Coming Soon" pages**
4. **Add real-time WebSocket updates**

### Low Priority
5. **Implement agent workers** (Phase 7)
6. **Add comprehensive tests**

---

## 💬 Communication Style

**Good:**
- Clear, direct explanations
- Technical details when relevant
- Show code examples
- Explain WHY, not just WHAT
- Portuguese when appropriate

**Bad:**
- Vague answers
- Skip testing steps
- Incomplete code
- Ignore standards

---

## ✅ Pre-Flight Checklist

**Before Starting:**
- [ ] Read [ARCHITECTURE-STANDARDS.md](../policies/ARCHITECTURE-STANDARDS.md)
- [ ] Check [PROGRESS.md](../project/PROGRESS.md)
- [ ] Review similar existing code

**Before Committing:**
- [ ] Tested locally (`npm run dev`)
- [ ] Build passes (`npm run build`)
- [ ] Conventional commit message

**After Deploy:**
- [ ] Wait 30 seconds
- [ ] Test in production
- [ ] Verify data loads

---

## 🚀 You Got This!

The project is in excellent shape. Follow the standards, test your changes, and you'll do great.

**Remember:**
- Read before you code
- Test before you commit
- Ask before you assume

---

**Document Version:** 2.0  
**Last Updated:** 2025-12-23  
**Status:** 🟢 Ready for handoff

