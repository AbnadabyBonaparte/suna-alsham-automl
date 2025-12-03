# 🚀 ALSHAM QUANTUM - Deployment Guide

**Version:** 5.0 (Quantum Enhanced)
**Last Updated:** 2025-12-02

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Migration](#database-migration)
4. [Edge Functions Deployment](#edge-functions-deployment)
5. [Cron Jobs Setup](#cron-jobs-setup)
6. [Seed Data](#seed-data)
7. [Storage Configuration](#storage-configuration)
8. [Frontend Deployment](#frontend-deployment)
9. [Post-Deployment Verification](#post-deployment-verification)
10. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### Required Tools:
- Node.js 20+ (LTS)
- npm 10+
- Supabase account
- Vercel account (optional)
- Git

### Accounts Needed:
- ✅ Supabase project
- ✅ GitHub repository
- ✅ Vercel (for deployment)

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

### 2.3 Configure Environment Variables

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Update `.env.local` with your Supabase credentials:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

## 3. Database Migration

### 3.1 Apply Core Schema

1. Open Supabase SQL Editor: `https://app.supabase.com/project/[PROJECT_ID]/sql`
2. Create a new query
3. Copy contents from `frontend/supabase_schema.sql`
4. Execute the query

### 3.2 Apply Quantum Tables Migration

1. Open Supabase SQL Editor
2. Copy contents from `supabase/migrations/20251202_create_quantum_tables.sql`
3. Execute the query

This creates:
- ✅ deals
- ✅ support_tickets
- ✅ social_posts
- ✅ transactions
- ✅ achievements
- ✅ user_achievements
- ✅ agent_logs
- ✅ agent_interactions
- ✅ system_metrics

### 3.3 Apply Storage Buckets Migration

1. Open Supabase SQL Editor
2. Copy contents from `supabase/migrations/20251202_create_storage_buckets.sql`
3. Execute the query

This creates:
- ✅ avatars (public bucket)
- ✅ documents (private bucket)
- ✅ exports (private bucket)

### 3.4 Repair WARNING Agents (Optional)

1. Open Supabase SQL Editor
2. Copy contents from `supabase/migrations/20251202_repair_warning_agents.sql`
3. Execute the query

---

## 4. Edge Functions Deployment

### 4.1 Prerequisites

Install Supabase CLI:

```bash
npm install -g supabase
```

### 4.2 Login to Supabase

```bash
supabase login
```

### 4.3 Link Project

```bash
supabase link --project-ref [YOUR_PROJECT_REF]
```

### 4.4 Deploy Edge Functions

Deploy all functions:

```bash
# Deploy agent-heartbeat
supabase functions deploy agent-heartbeat

# Deploy system-metrics
supabase functions deploy system-metrics

# Deploy agent-task-processor
supabase functions deploy agent-task-processor
```

### 4.5 Set Environment Variables

Each function needs access to Supabase:

```bash
supabase secrets set SUPABASE_URL=https://your-project.supabase.co
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

---

## 5. Cron Jobs Setup

### 5.1 Enable pg_cron Extension

1. Open Supabase SQL Editor
2. Run:

```sql
CREATE EXTENSION IF NOT EXISTS pg_cron;
```

### 5.2 Configure Cron Jobs

1. Copy contents from `supabase/cron-jobs.sql`
2. **IMPORTANT:** Replace the URLs and API keys with your project details
3. Execute in SQL Editor

This sets up:
- ✅ Agent heartbeat (every 5 minutes)
- ✅ System metrics (every 10 minutes)
- ✅ Task processor (every 3 minutes)
- ✅ Log cleanup (daily at 2 AM)

### 5.3 Verify Cron Jobs

```sql
-- View all scheduled jobs
SELECT * FROM cron.job;

-- View recent job runs
SELECT * FROM cron.job_run_details
ORDER BY start_time DESC
LIMIT 10;
```

---

## 6. Seed Data

### 6.1 Run Seed Script

After migrations are complete, populate the database:

```bash
cd frontend
npx tsx scripts/seed-data.ts
```

This inserts:
- ✅ 10 deals
- ✅ 8 support tickets
- ✅ 15 social posts
- ✅ 12 transactions
- ✅ 10 achievements

### 6.2 Verify Seed Data

```sql
SELECT COUNT(*) FROM deals;           -- Should be 10
SELECT COUNT(*) FROM support_tickets; -- Should be 8
SELECT COUNT(*) FROM social_posts;    -- Should be 15
SELECT COUNT(*) FROM transactions;    -- Should be 12
SELECT COUNT(*) FROM achievements;    -- Should be 10
```

---

## 7. Storage Configuration

### 7.1 Verify Buckets

In Supabase Dashboard → Storage, you should see:
- ✅ avatars (public)
- ✅ documents (private)
- ✅ exports (private)

### 7.2 Test Upload (Optional)

Use the `useStorage` hook in your app:

```typescript
const { uploadFile } = useStorage();

const handleUpload = async (file: File) => {
  const result = await uploadFile('avatars', file);
  console.log('Uploaded:', result);
};
```

---

## 8. Frontend Deployment

### 8.1 Local Development

```bash
cd frontend
npm run dev
```

Visit: `http://localhost:3000`

### 8.2 Production Build

```bash
npm run build
npm run start
```

### 8.3 Deploy to Vercel

#### Option A: Automatic (via GitHub)

1. Push to GitHub
2. Import repository to Vercel
3. Configure environment variables in Vercel dashboard
4. Deploy

#### Option B: Manual

```bash
npm install -g vercel
vercel --prod
```

### 8.4 Environment Variables in Vercel

Add these in Vercel Dashboard → Settings → Environment Variables:

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

## 9. Post-Deployment Verification

### 9.1 Test Core Features

- [ ] Login works
- [ ] Dashboard loads with real data
- [ ] Agents page shows all agents
- [ ] Admin page displays users
- [ ] Sales page shows deals
- [ ] Support page shows tickets

### 9.2 Test Realtime Features

- [ ] Create a new deal → Check if it appears in real-time
- [ ] Update an agent → Verify instant update
- [ ] Create a support ticket → Check realtime notification

### 9.3 Test Edge Functions

Manually trigger functions:

```bash
curl -X POST \
  https://your-project.supabase.co/functions/v1/agent-heartbeat \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Content-Type: application/json"
```

Expected response:
```json
{
  "success": true,
  "message": "Agent heartbeat completed",
  "agents_updated": 9
}
```

### 9.4 Test Cron Jobs

Check job execution:

```sql
SELECT * FROM cron.job_run_details
WHERE jobname IN (
  'alsham-agent-heartbeat',
  'alsham-system-metrics',
  'alsham-task-processor'
)
ORDER BY start_time DESC;
```

### 9.5 Monitor Logs

Check Supabase logs:
- Functions → agent-heartbeat → Logs
- Functions → system-metrics → Logs
- Functions → agent-task-processor → Logs

---

## 10. Troubleshooting

### Issue: Migrations Fail

**Solution:**
1. Check if tables already exist
2. Drop existing tables if safe
3. Re-run migrations

```sql
-- Drop all quantum tables (DANGEROUS)
DROP TABLE IF EXISTS deals CASCADE;
DROP TABLE IF EXISTS support_tickets CASCADE;
-- ... etc
```

### Issue: Edge Functions Not Deploying

**Solution:**
1. Verify Supabase CLI is latest version
2. Check project is linked: `supabase projects list`
3. Re-deploy with verbose logs: `supabase functions deploy function-name --debug`

### Issue: Cron Jobs Not Running

**Solution:**
1. Verify pg_cron extension is enabled
2. Check job status: `SELECT * FROM cron.job;`
3. Verify network policy allows outbound HTTP requests
4. Check Supabase project URL and API key are correct

### Issue: Seed Data Fails

**Solution:**
1. Ensure migrations are applied first
2. Check if tables exist: `\dt` in SQL editor
3. Verify RLS policies allow inserts
4. Try inserting one record manually to debug

### Issue: Realtime Not Working

**Solution:**
1. Verify Realtime is enabled in Supabase Dashboard
2. Check table has realtime enabled
3. Verify RLS policies allow SELECT
4. Check browser console for WebSocket errors

---

## 📞 Support

### Resources:
- **PROGRESS.md** - Full feature list
- **ARCHITECTURE.md** - System architecture
- **MIGRATION-INSTRUCTIONS.md** - Manual migration guide

### Community:
- GitHub Issues: `https://github.com/AbnadabyBonaparte/suna-alsham-automl/issues`
- Supabase Docs: `https://supabase.com/docs`
- Next.js Docs: `https://nextjs.org/docs`

---

**Deployment Guide Version:** 1.0
**Created:** 2025-12-02
**Status:** ✅ Production-Ready
