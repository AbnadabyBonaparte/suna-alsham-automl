# 🚀 ALSHAM QUANTUM - Enterprise AI CRM Platform

**Next-generation CRM platform with AI-powered agents, real-time analytics, and quantum-inspired interface.**

[![Vercel Deploy](https://img.shields.io/badge/Vercel-Deploy-black?logo=vercel)](https://quantum.alshamglobal.com.br)
[![Next.js 16](https://img.shields.io/badge/Next.js-16.0.3-black?logo=next.js)](https://nextjs.org/)
[![React 19](https://img.shields.io/badge/React-19.2.0-blue?logo=react)](https://react.dev/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-green?logo=supabase)](https://supabase.com/)
[![HUNTER X.1](https://img.shields.io/badge/HUNTER%20X.1-ca%C3%A7a%20di%C3%A1ria%20ativa-brightgreen)](caça/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [🏹 HUNTER X.1 — O Caçador está vivo](#-hunter-x1--o-caçador-está-vivo)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Status](#project-status)
- [Getting Started](#getting-started)
- [Development Philosophy](#development-philosophy)

---

## 🎯 Overview

ALSHAM QUANTUM is an enterprise-grade CRM platform featuring:

- **139 AI Agents** configured and ready for activation
- **26 Database Tables** with full RLS security
- **Real-time Dashboard** with live metrics from Supabase
- **100% Honest Data** - No mocked values in production
- **Multi-module Architecture** (Sales, Support, Social, Analytics)

**Current Status:** Phase 4.2 Complete | ~40% Total Progress

---

## 🏹 HUNTER X.1 — O Caçador está vivo

> *"Um caçador roda todos os dias os lugares mais propícios do mundo, lê a sua missão,
> executa, traz alimento — novas almas, novas tecnologias — e ao voltar sugere melhorias
> na própria missão. E nós somos os juízes."* — Abnadaby Bonaparte

O **HUNTER X.1** é o Caçador do Santuário: uma infraestrutura de inteligência que roda
**sozinha, todos os dias**, via GitHub Actions. Ele varre Hacker News, GitHub e arXiv,
faz triagem + análise + embeddings de cada achado, e abre um **PR "fila do tribunal"** —
o veredito e o merge são sempre do fundador (Lei 7: nada entra sem julgamento humano).

### ⏰ Está rodando agora (crons reais)

| Rotina | Workflow | Cron (UTC) | Horário BRT | O que faz |
|---|---|---|---|---|
| **Caça diária** | `.github/workflows/hunter.yml` | `30 9 * * *` | 06:30 | Sai, caça, abre o PR da fila do tribunal |
| **Ronda** | `.github/workflows/ronda-hunter.yml` | `0 9 * * *` | 06:00 | Checagens de saúde antes da caça |
| **O Espelho** | `.github/workflows/espelho.yml` | `0 10 * * 5` | sex 07:00 | Autocrítica semanal do próprio Hunter |

### 🩸 Provas de vida (caças reais, verificáveis no repo)

| Data | Vistos | Trazidos | Custo | 🥇 OURO DO DIA | Registro |
|---|---|---|---|---|---|
| **2026-07-29** | 165 | 18 | US$ 0,0488 | `cracken-ai/blacksea` (honeypot anti-LLM) | [PR #68](https://github.com/AbnadabyBonaparte/suna-alsham-automl/pull/68) |
| **2026-07-27** | 89 | 14 | US$ 0,0291 | *Distill & serve models at half the cost* | [`caça/2026-07-27.md`](caça/2026-07-27.md) |
| **2026-07-26** | 84 | 20 | US$ 0,0381 | *Integrate any CLI agent into any terminal* | [`caça/2026-07-26.md`](caça/2026-07-26.md) |

Cada relatório traz o custo real em dólar, os tokens gastos e as fontes que falharam
(ex.: em 27/07 o arXiv caiu com `HTTP 503` e foi marcado **NÃO VERIFICADO** — honestidade
brutal, não se maquia falha). Os relatórios ficam em [`caça/`](caça/); a alma do agente
em [`agents/hunter/`](agents/hunter/) e o dossiê em [`docs/DOSSIE-HUNTER-X1.md`](docs/DOSSIE-HUNTER-X1.md).

### 🛠️ Como foi construído (PRs reais, mergeados)

Fase 2 (#28) → runner em Node 22 (#29) → análise resiliente (#31) → arestas best-effort
(#33) → regra da missão v2 (#39) → Fase 3 "O Relógio" / cron (#45) → tetos & quarentena
da fila (#46) → **Fase 4 "O Espelho"** — autocrítica semanal (#47).

---

## ✨ Features

### 🤖 AI Agent System
- 139 agents configured across 5 squads (CORE, GUARD, ANALYST, SPECIALIST, CHAOS)
- Real-time efficiency monitoring from database
- Agent status tracking (currently 0 operational - system in configuration)
- Ready for worker implementation

### 📊 Real-Time Dashboard
- ✅ **Live Latency:** Actual Supabase response time
- ✅ **Real Uptime:** Calculated since 2024-11-20 (project start)
- ✅ **Agent Metrics:** Direct database queries
- ✅ **Neural Graph:** Real efficiency data visualization
- ✅ **Zero Mocked Data:** Complete honesty in all metrics

### 💼 CRM Modules (Ready for Population)
- **Sales Engine:** Pipeline management, deal tracking
- **Support Ops:** Ticket system with sentiment analysis
- **Social Pulse:** Multi-platform monitoring
- **Value Dashboard:** Financial transactions

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 16 with Turbopack
- **UI Library:** React 19
- **Styling:** Tailwind CSS + Custom Themes (7 realities)
- **State:** React Hooks + Custom hooks
- **Icons:** Lucide React

### Backend
- **Database:** Supabase (PostgreSQL)
- **Auth:** Supabase Auth with auto-profile creation
- **Real-time:** Live data fetching
- **Security:** Row Level Security on all tables

### DevOps
- **Hosting:** Vercel (auto-deploy from main)
- **CI/CD:** GitHub → Vercel pipeline
- **Monitoring:** Real-time metrics dashboard

---

## 📈 Project Status

### Completed Phases
```
✅ Phase 1.2: Database Schema (26 tables, 279 columns)
✅ Phase 2.1: Authentication (real login, OAuth ready)
✅ Phase 4.1: Agents Page (139 agents, real data integration)
✅ Phase 4.2: Dashboard (100% real metrics, zero mocked data)
```

### Current Progress: ~40%

### Pending Phases
```
⏳ Phase 2.2: OAuth Configuration (Google/GitHub)
⏳ Phase 5: Advanced Features (real-time updates, notifications)
⏳ Phase 6: AI Integration (connect LLM to agents)
⏳ Phase 7: Worker Implementation (make agents operational)
```

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Supabase account
- Vercel account (for deployment)

### Local Development

1. Clone and install
```bash
git clone https://github.com/AbnadabyBonaparte/suna-alsham-automl.git
cd suna-alsham-automl/frontend
npm install
```

2. Environment setup
```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=your_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_key
```

3. Run development server
```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000)

---

## 💎 Development Philosophy

### Honesty First

This project follows a **strict honesty policy**:

- ❌ No mocked data in production
- ❌ No fake metrics
- ❌ No simulated activity
- ✅ All numbers are real database queries
- ✅ All metrics are calculated values
- ✅ System shows 0 when nothing is running

**Why?**  
Professional integrity. When presenting to engineers or clients, every metric can be verified in the database.

### Demo Environment

For demonstrations, we maintain a separate **demo account** with:
- Populated deals, tickets, posts
- Simulated agent activity
- Clear "DEMO MODE" banner
- No confusion with production data

---

## 🗄️ Database

**26 Tables | 279 Columns | 120+ Indexes**

- Core: profiles, agents (139), sessions
- Modules: CRM, Support, Social, Gamification
- Security: audit_log, RLS policies
- Finance: transactions, invoices

See `migrations/README.md` for details.

---

## 🔐 Authentication

**Supabase Auth** with:
- ✅ Email/Password login
- ✅ Auto-profile creation trigger
- ⏳ Google OAuth (configured, not enabled)
- ⏳ GitHub OAuth (configured, not enabled)

---

## 📊 Current Metrics (Live)

As of deployment:
- **Agents Configured:** 139
- **Agents Operational:** 0 (awaiting worker implementation)
- **Database Latency:** ~900-1200ms
- **System Uptime:** 100% (since 2024-11-20)
- **Tables:** 26
- **Users:** Active authentication system

---

## 🏗️ Architecture

This project follows **Enterprise-Grade Architecture Standards**.

See [ARCHITECTURE.md](ARCHITECTURE.md) for:
- Mandatory patterns
- Code organization
- TypeScript standards  
- State management rules
- FAANG-level practices

**TL;DR:** Every line of code follows Vercel/Stripe/Linear quality standards.

---

## 📄 License

Proprietary © 2025 ALSHAM GLOBAL

---

**Built with 💎 by ALSHAM GLOBAL**  
**Honesty • Quality • Innovation**

