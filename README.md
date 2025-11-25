# 🚀 ALSHAM QUANTUM - Enterprise AI CRM Platform

**Next-generation CRM platform with AI-powered agents, real-time analytics, and quantum-inspired interface.**

[![Vercel Deploy](https://img.shields.io/badge/Vercel-Deploy-black?logo=vercel)](https://quantum.alshamglobal.com.br)
[![Next.js 16](https://img.shields.io/badge/Next.js-16.0.3-black?logo=next.js)](https://nextjs.org/)
[![React 19](https://img.shields.io/badge/React-19.2.0-blue?logo=react)](https://react.dev/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-green?logo=supabase)](https://supabase.com/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development](#development)
- [Deployment](#deployment)
- [Database Schema](#database-schema)
- [Authentication](#authentication)

---

## 🎯 Overview

ALSHAM QUANTUM is an enterprise-grade CRM platform featuring:

- **139 AI Agents** organized in specialized squads
- **26 Database Tables** with full RLS security
- **Real-time Dashboard** with WebSocket updates
- **Neural Network Visualization** with 3D graphics
- **Gamification System** with XP, levels, and achievements
- **Multi-module Architecture** (Sales, Support, Social, Analytics)

**Current Status:** Phase 2.1 Complete | ~28% Total Progress

---

## ✨ Features

### 🤖 AI Agent System
- 139 active agents across 5 squads (CORE, GUARD, ANALYST, SPECIALIST, CHAOS)
- Real-time agent monitoring and control
- Neural connection mapping
- Agent evolution tracking

### 📊 Analytics & Dashboards
- Real-time system metrics
- 3D network visualization (Panopticon)
- Social media sentiment analysis
- Predictive analytics

### 💼 CRM Modules
- **Sales Engine:** Pipeline management, deal tracking
- **Support Ops:** Ticket system with sentiment analysis
- **Social Pulse:** Multi-platform monitoring
- **Value Dashboard:** Financial transactions and invoicing

### 🎮 Gamification
- XP and leveling system
- Achievements and badges
- Global leaderboard
- Streak tracking

### 🔒 Security
- Row Level Security (RLS) on all tables
- JWT-based authentication
- Session management
- Audit logging

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 16 with Turbopack
- **UI Library:** React 19
- **Styling:** Tailwind CSS
- **Animations:** Canvas API, Three.js
- **Icons:** Lucide React

### Backend
- **Database:** Supabase (PostgreSQL)
- **Auth:** Supabase Auth
- **Real-time:** Supabase Realtime

### DevOps
- **Hosting:** Vercel
- **Version Control:** GitHub
- **CI/CD:** Vercel Auto-Deploy

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Supabase account

### Installation

1. Clone and install
\\\ash
git clone https://github.com/AbnadabyBonaparte/suna-alsham-automl.git
cd suna-alsham-automl/frontend
npm install
\\\

2. Setup environment
\\\ash
cp .env.example .env.local
\\\

Edit with your credentials:
\\\nv
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_key
\\\

3. Apply database migrations (Supabase SQL Editor)
\\\
migrations/20251125_phase_1_2_complete.sql
\\\

4. Run dev server
\\\ash
npm run dev
\\\

Open [http://localhost:3000](http://localhost:3000)

---

## 📁 Project Structure

\\\
frontend/
├── src/
│   ├── app/              # Next.js pages
│   ├── components/       # React components
│   ├── contexts/         # Auth, Theme
│   ├── lib/              # Supabase client
│   └── types/            # TypeScript types
├── migrations/           # Database migrations
└── .env.example          # Environment template
\\\

---

## 🗄️ Database Schema

**26 Tables | 279 Columns | 120+ Indexes | 70+ RLS Policies**

- Core: profiles, agents (139), sessions, logs
- Modules: CRM, Support, Social, Gamification
- Security: audit_log, security_events
- Finance: transactions, invoices
- AI: models, training, predictions

See [migrations/README.md](migrations/README.md)

---

## 🔐 Authentication

**Supabase Auth** with:

- ✅ Email/Password
- ✅ Google OAuth
- ✅ GitHub OAuth
- ✅ Protected routes
- ✅ Auto profile creation

---

## 📈 Progress

\\\
✅ Phase 1.2: Database (26 tables)
✅ Phase 2.1: Authentication (100%)
⏳ Phase 3: State Management
⏳ Phase 4: Core Features
\\\

**Overall:** ~28%

---

## 📄 License

Proprietary © 2025 ALSHAM GLOBAL

---

**Built with 💎 by ALSHAM GLOBAL**
