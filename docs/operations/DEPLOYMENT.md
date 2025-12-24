# 🚀 ALSHAM QUANTUM - Deployment Guide

**Version:** 5.0 (Quantum Enhanced)  
**Last Updated:** 2025-12-23

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Local Development](#local-development)
4. [Production Deployment](#production-deployment)
5. [Database Migration](#database-migration)
6. [Edge Functions](#edge-functions)
7. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### Required Tools
- Node.js 20+ (LTS)
- npm 10+
- Git
- PowerShell (Windows) or Terminal (Mac/Linux)

### Accounts Needed
- ✅ Supabase project
- ✅ GitHub repository
- ✅ Vercel account

### Environment Variables
See [ENVIRONMENT-VARIABLES.md](./ENVIRONMENT-VARIABLES.md) for complete list.

---

## 2. Environment Setup

### 2.1 Clone Repository

```bash
git clone https://github.com/AbnadabyBonaparte/suna-alsham-automl.git
cd suna-alsham-automl/frontend
```

### 2.2 Install Dependencies

```bash
npm install
```

### 2.3 Configure Environment

```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

## 3. Local Development

### Start Development Server

```bash
cd frontend
npm run dev
```

Visit: [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
```

### Run Production Build Locally

```bash
npm run start
```

---

## 4. Production Deployment

### Automatic (Recommended)

1. Push to GitHub main branch
2. Vercel auto-deploys
3. Wait ~30 seconds
4. Test at production URL

```bash
git add -A
git commit -m "feat(scope): description"
git push origin main
```

### Manual

```bash
npm install -g vercel
vercel --prod
```

### Environment Variables in Vercel

Add in Vercel Dashboard → Settings → Environment Variables:

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

## 5. Database Migration

### Apply Core Schema

1. Open Supabase SQL Editor
2. Copy contents from `frontend/supabase_schema.sql`
3. Execute the query

### Apply Quantum Tables

1. Copy from `supabase/migrations/20251202_create_quantum_tables.sql`
2. Execute in SQL Editor

### Run Seed Data

```bash
cd frontend
npx tsx scripts/seed-data.ts
```

---

## 6. Edge Functions

### Deploy Functions

```bash
supabase login
supabase link --project-ref [YOUR_PROJECT_REF]
supabase functions deploy agent-heartbeat
supabase functions deploy system-metrics
supabase functions deploy agent-task-processor
```

### Set Secrets

```bash
supabase secrets set SUPABASE_URL=https://your-project.supabase.co
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

---

## 7. Troubleshooting

### Build Fails

```powershell
cd frontend
Remove-Item -Recurse -Force .next
Remove-Item -Recurse -Force node_modules
npm install
npm run build
```

### Supabase Connection Error

1. Check `.env.local` has correct keys
2. Verify RLS policies in Supabase dashboard
3. Check user is authenticated

### Login Not Working

See [auth-login-failure runbook](./runbooks/auth-login-failure.md)

### Deployment Fails on Vercel

1. Check Vercel Dashboard → Deployments → Logs
2. Verify environment variables are set
3. Check build output for errors

---

## 📞 Support

- [PROGRESS.md](../project/PROGRESS.md) - Current status
- [HANDOFF.md](./HANDOFF.md) - Context transfer
- [runbooks/](./runbooks/) - Incident procedures

---

**Deployment Guide Version:** 2.0  
**Created:** 2025-12-02  
**Updated:** 2025-12-23  
**Status:** ✅ Production-Ready

