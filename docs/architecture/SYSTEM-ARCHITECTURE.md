# 🏗️ System Architecture - ALSHAM QUANTUM

**Version:** 5.0 (Quantum Enhanced)  
**Last Updated:** 2025-12-23

---

## 📊 System Overview

ALSHAM QUANTUM is an enterprise-grade Multi-Agent AI Platform.

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTS                              │
│  Browser (React 19) │ Mobile (PWA) │ API Consumers          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Vercel)                      │
│  Next.js 16 │ TypeScript 5 │ Tailwind │ Zustand             │
│  App Router │ Turbopack │ Framer Motion                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND (Supabase)                     │
│  PostgreSQL │ Auth │ Realtime │ Storage │ Edge Functions    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      WORKERS (Railway)                      │
│  Evolution Jobs │ Agent Processing │ Cron Tasks             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔢 Numbers

| Component | Count |
|-----------|-------|
| Database Tables | 27 |
| Database Columns | 279+ |
| Indexes | 120+ |
| RLS Policies | 70+ |
| Triggers | 8+ |
| AI Agents | 139 |
| Frontend Pages | 25 |
| Zustand Stores | 12 |
| Custom Hooks | 20+ |
| Edge Functions | 3 |
| Cron Jobs | 4 |
| Storage Buckets | 3 |

---

## 🖥️ Frontend Architecture

### Technology Stack

```yaml
Framework: Next.js 16.0.3
  - App Router
  - Turbopack (dev)
  - Server Components
  - API Routes

UI:
  - React 19.2.0
  - TypeScript 5.x (strict)
  - Tailwind CSS 3.x
  - Framer Motion

State:
  - Zustand 5.x
  - 12 stores with devtools + persist

Components:
  - Custom quantum components
  - Radix UI primitives
  - Lucide icons
```

### Folder Structure

```
frontend/src/
├── app/                    # Next.js App Router
│   ├── dashboard/          # Protected pages
│   │   ├── agents/         # Agent management
│   │   ├── analytics/      # Analytics
│   │   ├── settings/       # User settings
│   │   └── ...
│   ├── api/                # API routes
│   └── (auth)/             # Auth pages
├── components/
│   ├── quantum/            # Custom components
│   ├── ui/                 # Base components
│   └── layout/             # Layout components
├── stores/                 # Zustand stores
├── hooks/                  # Custom hooks
├── lib/                    # Utilities
└── types/                  # TypeScript types
```

### State Management

```typescript
// 12 Zustand Stores
useAgentsStore      // 139 agents
useDashboardStore   // Real-time metrics
useRequestsStore    // CRUD operations
useSalesStore       // Sales pipeline
useSupportStore     // Support tickets
useAnalyticsStore   // Analytics data
useAuthStore        // Authentication
useProfileStore     // User profile
useUIStore          // UI preferences
useAppStore         // Global state
useLoadingStore     // Loading states
useNotificationStore // Notifications
```

---

## 🗄️ Database Architecture

### Core Tables

```sql
-- Authentication & Users
profiles            -- User profiles (1:1 with auth.users)
user_sessions       -- Active sessions
user_stats          -- Gamification stats

-- AI Agents
agents              -- 139 AI agents
agent_logs          -- Activity logs
agent_interactions  -- Agent-to-agent communication

-- Business
deals               -- Sales pipeline
support_tickets     -- Customer support
social_posts        -- Social media
transactions        -- Financial records

-- System
system_metrics      -- Health monitoring
audit_log           -- Security audit
api_keys            -- API authentication
```

### RLS Pattern

```sql
-- Users see own data
CREATE POLICY "Users see own" ON table_name
FOR SELECT USING (auth.uid() = user_id);

-- Founders see all
CREATE POLICY "Founders see all" ON table_name
FOR SELECT USING (
  (SELECT founder_access FROM profiles WHERE id = auth.uid()) = true
);
```

---

## ⚡ Edge Functions

### agent-heartbeat
- **Frequency:** Every 5 minutes
- **Purpose:** Update agent status and efficiency
- **Runtime:** Deno

### system-metrics
- **Frequency:** Every 10 minutes
- **Purpose:** Collect system health metrics

### agent-task-processor
- **Frequency:** Every 3 minutes
- **Purpose:** Process agent tasks and interactions

---

## ⏰ Cron Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| agent-heartbeat | */5 * * * * | Agent status |
| system-metrics | */10 * * * * | System health |
| task-processor | */3 * * * * | Task processing |
| log-cleanup | 0 2 * * * | Daily cleanup |

---

## 📦 Storage Buckets

| Bucket | Type | Size Limit | Purpose |
|--------|------|------------|---------|
| avatars | Public | 5MB | User avatars |
| documents | Private | 50MB | User documents |
| exports | Private | 100MB | Data exports |

---

## 🔐 Security Architecture

### Authentication Flow

```
1. User submits credentials
2. Supabase Auth validates
3. JWT token issued
4. Cookie set (via @supabase/ssr)
5. Middleware validates on each request
6. RLS enforces data access
```

### Security Layers

1. **Transport:** HTTPS everywhere
2. **Authentication:** Supabase Auth (JWT)
3. **Authorization:** RLS policies
4. **API:** Rate limiting
5. **Audit:** Comprehensive logging

---

## 🚀 Deployment Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   GitHub     │────▶│   Vercel     │────▶│  Production  │
│   (main)     │     │   (build)    │     │   (CDN)      │
└──────────────┘     └──────────────┘     └──────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│   Railway    │────▶│   Workers    │
│   (deploy)   │     │   (cron)     │
└──────────────┘     └──────────────┘
```

### Environments

| Environment | URL | Purpose |
|-------------|-----|---------|
| Production | quantum.alshamglobal.com.br | Live |
| Preview | *.vercel.app | PR previews |
| Development | localhost:3000 | Local dev |

---

## 📈 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| First Load | <2s | ✅ |
| Time to Interactive | <3s | ✅ |
| API Latency | <100ms | ~900ms* |
| Realtime Latency | <100ms | ✅ |

*Database latency includes network round-trip to Supabase

---

## 🔗 Related Documents

- [ADRs](./decisions/) - Architecture decisions
- [DEPLOYMENT.md](../operations/DEPLOYMENT.md) - Deploy guide
- [PROGRESS.md](../project/PROGRESS.md) - Current status

---

**Document Version:** 2.0  
**Status:** ✅ Production-Ready

