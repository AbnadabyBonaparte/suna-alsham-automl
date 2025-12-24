# 🏗️ Arquitetura - ALSHAM QUANTUM

**Documentação técnica da arquitetura do sistema.**

---

## 📂 Conteúdo desta Seção

| Documento | Descrição |
|-----------|-----------|
| [SYSTEM-ARCHITECTURE.md](./SYSTEM-ARCHITECTURE.md) | Visão geral do sistema, componentes, fluxos |
| [DATABASE-SCHEMA.md](./DATABASE-SCHEMA.md) | Schema do banco, tabelas, relacionamentos |
| [decisions/](./decisions/) | ADRs - Architecture Decision Records |

---

## 🎯 Visão Geral

### Stack Tecnológico

```
┌─────────────────────────────────────────────────────────┐
│                      FRONTEND                           │
│  Next.js 16 + React 19 + TypeScript 5 + Tailwind CSS   │
│  Zustand (State) + Framer Motion (Animations)          │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                      BACKEND                            │
│  Supabase (PostgreSQL + Auth + Realtime + Storage)     │
│  Edge Functions (Deno) + Cron Jobs (pg_cron)           │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    INFRAESTRUTURA                       │
│  Vercel (Frontend) + Railway (Workers) + GitHub (CI)   │
└─────────────────────────────────────────────────────────┘
```

### Números do Sistema

| Métrica | Valor |
|---------|-------|
| Tabelas no Banco | 27 |
| Colunas Totais | 279+ |
| Indexes | 120+ |
| RLS Policies | 70+ |
| Agentes IA | 139 |
| Páginas Frontend | 25 |
| Zustand Stores | 12 |
| Custom Hooks | 20+ |
| Edge Functions | 3 |
| Cron Jobs | 4 |

---

## 📐 Decisões Arquiteturais (ADRs)

Todas as decisões técnicas importantes são documentadas como ADRs:

| # | Decisão | Impacto |
|---|---------|---------|
| [001](./decisions/001-zustand-over-redux.md) | Zustand over Redux | State management |
| [002](./decisions/002-supabase-over-firebase.md) | Supabase over Firebase | Backend |
| [003](./decisions/003-data-honesty-policy.md) | Data Honesty Policy | Cultura |
| [004](./decisions/004-typescript-strict-mode.md) | TypeScript Strict | Qualidade |
| [005](./decisions/005-faang-level-standards.md) | FAANG Standards | Padrões |
| [006](./decisions/006-no-context-api.md) | No Context API | State |

---

## 🔗 Links Relacionados

- [Políticas de Código](../policies/ARCHITECTURE-STANDARDS.md)
- [Guia de Deploy](../operations/DEPLOYMENT.md)
- [Progresso do Projeto](../project/PROGRESS.md)

