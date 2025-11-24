# 🚀 ALSHAM QUANTUM - ROADMAP TO PERFECTION

**Project:** ALSHAM 360° PRIMA - Enterprise CRM Platform  
**Current Status:** v13.3 (Visual Complete, Backend Incomplete)  
**Target:** Production-Ready 10/10 System  
**Architecture:** Next.js 16 + React 19 + Supabase + TypeScript

---

## 📑 TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Current Architecture](#current-architecture)
3. [Target Architecture](#target-architecture)
4. [Execution Order](#execution-order)
5. [Phase 1: Foundation & Backend](#phase-1-foundation--backend)
6. [Phase 2: Authentication & Security](#phase-2-authentication--security)
7. [Phase 3: State Management & Data Flow](#phase-3-state-management--data-flow)
8. [Phase 4: Core Features Implementation](#phase-4-core-features-implementation)
9. [Phase 5: Advanced Integrations](#phase-5-advanced-integrations)
10. [Phase 6: Performance Optimization](#phase-6-performance-optimization)
11. [Phase 7: Testing & Quality](#phase-7-testing--quality)
12. [Phase 8: DevOps & Deployment](#phase-8-devops--deployment)
13. [Phase 9: Polish & Accessibility](#phase-9-polish--accessibility)
14. [Phase 10: Documentation & Handoff](#phase-10-documentation--handoff)
15. [Final Checklist](#final-checklist)

---

## PROJECT OVERVIEW

### What We Have
- ✅ 26 pages with stunning visual design
- ✅ Canvas-based animations (18+ implementations)
- ✅ Responsive UI with glassmorphism
- ✅ Theme system (9 variants)
- ✅ TypeScript setup
- ✅ Supabase client configured
- ✅ Basic routing structure

### What's Missing
- ❌ Backend integration (95% mockado)
- ❌ Real authentication
- ❌ Database schema
- ❌ State management
- ❌ Error handling
- ❌ Testing infrastructure
- ❌ CI/CD pipeline
- ❌ Monitoring & analytics

---

## CURRENT ARCHITECTURE

```
Frontend (Next.js 16)
├── 26 Pages (Visual Complete)
│   ├── Auth: Login, Onboarding
│   ├── Core: Dashboard, Agents, Agent Detail
│   ├── Operations: Requests, Sales, Support, Social, Value
│   ├── Intelligence: Orion, Nexus, Evolution, Void, Singularity
│   ├── Analytics: Analytics, Network
│   └── Infrastructure: Matrix, Containment, Gamification, API, Settings, Admin
├── Components: Sidebar, Layout
├── Styling: Tailwind + CSS Variables
└── Data: 95% Mocked

Backend (Supabase - Minimal)
├── Agents table (only one connected)
└── Client configured
```

---

## TARGET ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  Next.js 16 + React 19 + TypeScript + Tailwind             │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Pages    │  │ Components │  │   Hooks    │           │
│  │  (26+)     │  │  (Shared)  │  │ (Custom)   │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│         │              │                │                   │
│  ┌──────▼──────────────▼────────────────▼────────┐        │
│  │         State Management (Zustand)             │        │
│  │  + React Query + Optimistic Updates            │        │
│  └────────────────────────┬────────────────────────┘        │
└───────────────────────────┼─────────────────────────────────┘
                            │
                   ┌────────▼────────┐
                   │   API LAYER     │
                   │  (tRPC/REST)    │
                   └────────┬────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      BACKEND (Supabase)                      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │     Auth     │  │   Storage    │     │
│  │   (30+ TB)   │  │   (JWT/SSO)  │  │   (Files)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Realtime    │  │   Functions  │  │     RLS      │     │
│  │ (WebSocket)  │  │  (Edge Fns)  │  │  (Security)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────────┬───────────────────────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         │                                   │
┌────────▼────────┐              ┌───────────▼──────────┐
│  INTEGRATIONS   │              │    EXTERNAL APIs     │
│                 │              │                      │
│ • n8n Workflows │              │ • OpenAI (Orion)    │
│ • Email (SMTP)  │              │ • Anthropic (Claude)│
│ • Stripe (Pay)  │              │ • Google (OAuth)    │
│ • Twilio (SMS)  │              │ • GitHub (Auth)     │
└─────────────────┘              │ • Twitter (Social)  │
                                 │ • Cloudflare (CDN)  │
                                 └─────────────────────┘
```

---

## EXECUTION ORDER

**CRITICAL PATH (Must be sequential):**
```
1. Database Schema → 2. Auth System → 3. State Management → 
4. Core CRUD → 5. Real-time → 6. Integrations → 
7. Performance → 8. Testing → 9. Deploy
```

**PARALLEL TRACKS (Can be done simultaneously):**
```
Track A: Backend (Schema, Auth, API)
Track B: Frontend (State, Error Handling, Loading States)
Track C: DevOps (CI/CD, Monitoring)
Track D: Quality (Tests, Accessibility)
```

---

## PHASE 1: FOUNDATION & BACKEND

### 1.1 Environment Setup

#### 1.1.1 Configure Environment Variables
```bash
# Create .env.local
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# External APIs
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# Integrations
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
N8N_WEBHOOK_URL=
RESEND_API_KEY=

# Monitoring
SENTRY_DSN=
SENTRY_AUTH_TOKEN=
```

#### 1.1.2 Setup Development Tools
- Install and configure ESLint with strict rules
- Setup Prettier with team conventions
- Configure Husky for pre-commit hooks
- Setup commitlint for conventional commits
- Install and configure VSCode extensions

#### 1.1.3 Project Structure Refinement
```
/frontend
├── /src
│   ├── /app                 # Next.js 16 App Router
│   ├── /components
│   │   ├── /ui              # shadcn/ui components
│   │   ├── /layout          # Layout components
│   │   ├── /canvas          # Canvas animations
│   │   └── /shared          # Shared components
│   ├── /lib
│   │   ├── /supabase        # Supabase client & utils
│   │   ├── /store           # Zustand stores
│   │   ├── /hooks           # Custom React hooks
│   │   ├── /utils           # Utility functions
│   │   ├── /validations     # Zod schemas
│   │   └── /constants       # Constants & configs
│   ├── /types               # TypeScript types
│   ├── /styles              # Global styles
│   └── /public              # Static assets
├── /tests
│   ├── /unit                # Unit tests
│   ├── /integration         # Integration tests
│   └── /e2e                 # End-to-end tests
└── /docs                    # Documentation
```

---

### 1.2 Supabase Database Schema

#### 1.2.1 Core Tables

**Users & Authentication**
```sql
-- profiles (extends auth.users)
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE,
  full_name TEXT,
  avatar_url TEXT,
  role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin', 'architect', 'observer', 'strategist')),
  bio TEXT,
  company TEXT,
  location TEXT,
  preferences JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- user_sessions (track active sessions)
CREATE TABLE public.user_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  device_info JSONB,
  ip_address INET,
  last_activity TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Agents System**
```sql
-- agents (already exists, expand it)
ALTER TABLE public.agents ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES public.profiles(id);
ALTER TABLE public.agents ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;
ALTER TABLE public.agents ADD COLUMN IF NOT EXISTS neural_load DECIMAL(5,2) DEFAULT 0;
ALTER TABLE public.agents ADD COLUMN IF NOT EXISTS uptime_seconds BIGINT DEFAULT 0;
ALTER TABLE public.agents ADD COLUMN IF NOT EXISTS version TEXT DEFAULT '1.0.0';

-- agent_logs (for Matrix/Void pages)
CREATE TABLE public.agent_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_id UUID REFERENCES public.agents(id) ON DELETE CASCADE,
  log_level TEXT CHECK (log_level IN ('info', 'warning', 'error', 'critical')),
  message TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- agent_connections (for Neural Nexus)
CREATE TABLE public.agent_connections (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_a_id UUID REFERENCES public.agents(id) ON DELETE CASCADE,
  agent_b_id UUID REFERENCES public.agents(id) ON DELETE CASCADE,
  connection_type TEXT DEFAULT 'neural',
  strength DECIMAL(5,2) DEFAULT 1.0,
  latency_ms INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(agent_a_id, agent_b_id)
);
```

**Dashboard & Metrics**
```sql
-- system_metrics (for Dashboard/Analytics)
CREATE TABLE public.system_metrics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  metric_type TEXT NOT NULL,
  metric_value DECIMAL(20,2),
  metadata JSONB,
  recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create hypertable for time-series data (if using TimescaleDB extension)
-- SELECT create_hypertable('system_metrics', 'recorded_at');

-- network_nodes (for Network/Panopticon)
CREATE TABLE public.network_nodes (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  location_lat DECIMAL(10,6),
  location_lon DECIMAL(10,6),
  load_percentage DECIMAL(5,2) DEFAULT 0,
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'degraded', 'offline')),
  region TEXT,
  metadata JSONB,
  last_ping TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Sales & CRM**
```sql
-- deals (for Sales Engine)
CREATE TABLE public.deals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.profiles(id),
  client_name TEXT NOT NULL,
  value DECIMAL(15,2) NOT NULL,
  status TEXT DEFAULT 'lead' CHECK (status IN ('lead', 'negotiation', 'closed', 'lost')),
  probability INT DEFAULT 50 CHECK (probability >= 0 AND probability <= 100),
  stage TEXT,
  close_date DATE,
  notes TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- deal_activities (timeline)
CREATE TABLE public.deal_activities (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  deal_id UUID REFERENCES public.deals(id) ON DELETE CASCADE,
  user_id UUID REFERENCES public.profiles(id),
  activity_type TEXT NOT NULL,
  description TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Support System**
```sql
-- support_tickets (for Support Ops)
CREATE TABLE public.support_tickets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.profiles(id),
  subject TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
  priority TEXT DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'critical')),
  sentiment_score DECIMAL(5,2),
  assigned_to UUID REFERENCES public.profiles(id),
  resolved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ticket_messages (conversations)
CREATE TABLE public.ticket_messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  ticket_id UUID REFERENCES public.support_tickets(id) ON DELETE CASCADE,
  user_id UUID REFERENCES public.profiles(id),
  message TEXT NOT NULL,
  is_internal BOOLEAN DEFAULT false,
  attachments JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Social Media**
```sql
-- social_posts (for Social Pulse)
CREATE TABLE public.social_posts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  platform TEXT NOT NULL CHECK (platform IN ('twitter', 'reddit', 'instagram', 'linkedin')),
  external_id TEXT,
  author TEXT,
  content TEXT,
  likes_count INT DEFAULT 0,
  shares_count INT DEFAULT 0,
  comments_count INT DEFAULT 0,
  sentiment_score DECIMAL(5,2),
  trending_score DECIMAL(10,2),
  metadata JSONB,
  posted_at TIMESTAMPTZ,
  fetched_at TIMESTAMPTZ DEFAULT NOW()
);

-- social_trends (hashtags/topics)
CREATE TABLE public.social_trends (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  tag TEXT NOT NULL,
  volume INT DEFAULT 0,
  sentiment TEXT CHECK (sentiment IN ('positive', 'negative', 'neutral')),
  metadata JSONB,
  recorded_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Gamification**
```sql
-- user_stats (XP, Level, etc)
CREATE TABLE public.user_stats (
  user_id UUID PRIMARY KEY REFERENCES public.profiles(id) ON DELETE CASCADE,
  xp INT DEFAULT 0,
  level INT DEFAULT 1,
  total_points INT DEFAULT 0,
  rank INT,
  badges JSONB DEFAULT '[]'::jsonb,
  achievements JSONB DEFAULT '[]'::jsonb,
  streak_days INT DEFAULT 0,
  last_active_date DATE,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- achievements (definitions)
CREATE TABLE public.achievements (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  icon TEXT,
  rarity TEXT CHECK (rarity IN ('common', 'rare', 'epic', 'legendary')),
  points INT DEFAULT 0,
  criteria JSONB,
  unlocked_count INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- user_achievements (unlocked)
CREATE TABLE public.user_achievements (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  achievement_id TEXT REFERENCES public.achievements(id),
  unlocked_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, achievement_id)
);

-- leaderboard (materialized view or table)
CREATE TABLE public.leaderboard (
  rank INT,
  user_id UUID REFERENCES public.profiles(id),
  username TEXT,
  total_xp INT,
  level INT,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**API & Requests**
```sql
-- api_requests (for API Playground logging)
CREATE TABLE public.api_requests (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.profiles(id),
  method TEXT NOT NULL,
  endpoint TEXT NOT NULL,
  status_code INT,
  latency_ms INT,
  request_body JSONB,
  response_body JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- automation_requests (for Requests/Fabrication page)
CREATE TABLE public.automation_requests (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.profiles(id),
  title TEXT NOT NULL,
  description TEXT,
  parameters JSONB,
  status TEXT DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed')),
  priority TEXT DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high')),
  result JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Security & Containment**
```sql
-- security_threats (for Containment page)
CREATE TABLE public.security_threats (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  threat_type TEXT NOT NULL,
  source_ip INET,
  severity TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  description TEXT,
  blocked BOOLEAN DEFAULT false,
  metadata JSONB,
  detected_at TIMESTAMPTZ DEFAULT NOW()
);

-- system_defcon_log (DEFCON level changes)
CREATE TABLE public.system_defcon_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  level INT CHECK (level >= 1 AND level <= 5),
  changed_by UUID REFERENCES public.profiles(id),
  reason TEXT,
  changed_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Financial**
```sql
-- transactions (for Value Dash)
CREATE TABLE public.transactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.profiles(id),
  type TEXT CHECK (type IN ('credit', 'debit')),
  amount DECIMAL(15,2) NOT NULL,
  currency TEXT DEFAULT 'USD',
  description TEXT,
  category TEXT,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed')),
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- user_balance (virtual wallet)
CREATE TABLE public.user_balance (
  user_id UUID PRIMARY KEY REFERENCES public.profiles(id) ON DELETE CASCADE,
  balance DECIMAL(15,2) DEFAULT 0,
  currency TEXT DEFAULT 'USD',
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**AI & Orion**
```sql
-- ai_conversations (for Orion AI)
CREATE TABLE public.ai_conversations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES public.profiles(id),
  model TEXT NOT NULL,
  title TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ai_messages (chat history)
CREATE TABLE public.ai_messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID REFERENCES public.ai_conversations(id) ON DELETE CASCADE,
  role TEXT CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  tokens_used INT,
  model TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### 1.2.2 Indexes (Performance)
```sql
-- Indexes for common queries
CREATE INDEX idx_agents_user_id ON public.agents(user_id);
CREATE INDEX idx_agents_status ON public.agents(status);
CREATE INDEX idx_agent_logs_agent_id ON public.agent_logs(agent_id);
CREATE INDEX idx_agent_logs_created_at ON public.agent_logs(created_at DESC);
CREATE INDEX idx_deals_user_id ON public.deals(user_id);
CREATE INDEX idx_deals_status ON public.deals(status);
CREATE INDEX idx_support_tickets_user_id ON public.support_tickets(user_id);
CREATE INDEX idx_support_tickets_status ON public.support_tickets(status);
CREATE INDEX idx_social_posts_platform ON public.social_posts(platform);
CREATE INDEX idx_social_posts_posted_at ON public.social_posts(posted_at DESC);
CREATE INDEX idx_transactions_user_id ON public.transactions(user_id);
CREATE INDEX idx_user_achievements_user_id ON public.user_achievements(user_id);
CREATE INDEX idx_ai_conversations_user_id ON public.ai_conversations(user_id);
CREATE INDEX idx_ai_messages_conversation_id ON public.ai_messages(conversation_id);
```

#### 1.2.3 Row Level Security (RLS)
```sql
-- Enable RLS on all tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.deals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.support_tickets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_conversations ENABLE ROW LEVEL SECURITY;

-- Profiles: Users can read all, update own
CREATE POLICY "Public profiles are viewable by everyone"
  ON public.profiles FOR SELECT
  USING (true);

CREATE POLICY "Users can update own profile"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id);

-- Agents: Users can CRUD own agents
CREATE POLICY "Users can view own agents"
  ON public.agents FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own agents"
  ON public.agents FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own agents"
  ON public.agents FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own agents"
  ON public.agents FOR DELETE
  USING (auth.uid() = user_id);

-- Admin override (admins see everything)
CREATE POLICY "Admins can see all agents"
  ON public.agents FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- Similar policies for other tables...
-- (Repeat pattern for deals, tickets, etc.)

-- System metrics: Read-only for users, full access for admins
CREATE POLICY "Users can view system metrics"
  ON public.system_metrics FOR SELECT
  USING (true);

CREATE POLICY "Only admins can insert metrics"
  ON public.system_metrics FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );
```

#### 1.2.4 Database Functions
```sql
-- Function: Update updated_at timestamp
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON public.agents
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- (Apply to: deals, support_tickets, ai_conversations, etc.)

-- Function: Calculate user level from XP
CREATE OR REPLACE FUNCTION public.calculate_level(xp INT)
RETURNS INT AS $$
BEGIN
  RETURN FLOOR(SQRT(xp / 100)) + 1;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: Award XP and check for level up
CREATE OR REPLACE FUNCTION public.award_xp(
  p_user_id UUID,
  p_xp INT
)
RETURNS TABLE(new_level INT, leveled_up BOOLEAN) AS $$
DECLARE
  v_old_level INT;
  v_new_level INT;
  v_old_xp INT;
BEGIN
  -- Get current stats
  SELECT level, xp INTO v_old_level, v_old_xp
  FROM public.user_stats
  WHERE user_id = p_user_id;

  -- If no record, create one
  IF NOT FOUND THEN
    INSERT INTO public.user_stats (user_id, xp, level)
    VALUES (p_user_id, p_xp, calculate_level(p_xp))
    RETURNING level INTO v_new_level;
    
    RETURN QUERY SELECT v_new_level, true;
    RETURN;
  END IF;

  -- Update XP
  UPDATE public.user_stats
  SET xp = xp + p_xp,
      level = calculate_level(xp + p_xp)
  WHERE user_id = p_user_id
  RETURNING level INTO v_new_level;

  RETURN QUERY SELECT v_new_level, (v_new_level > v_old_level);
END;
$$ LANGUAGE plpgsql;

-- Function: Update leaderboard (call periodically)
CREATE OR REPLACE FUNCTION public.refresh_leaderboard()
RETURNS void AS $$
BEGIN
  TRUNCATE public.leaderboard;
  
  INSERT INTO public.leaderboard (rank, user_id, username, total_xp, level)
  SELECT
    ROW_NUMBER() OVER (ORDER BY us.xp DESC) as rank,
    us.user_id,
    p.username,
    us.xp as total_xp,
    us.level
  FROM public.user_stats us
  JOIN public.profiles p ON p.id = us.user_id
  ORDER BY us.xp DESC
  LIMIT 100;
END;
$$ LANGUAGE plpgsql;
```

#### 1.2.5 Realtime Configuration
```sql
-- Enable realtime for critical tables
ALTER PUBLICATION supabase_realtime ADD TABLE public.agents;
ALTER PUBLICATION supabase_realtime ADD TABLE public.agent_logs;
ALTER PUBLICATION supabase_realtime ADD TABLE public.system_metrics;
ALTER PUBLICATION supabase_realtime ADD TABLE public.support_tickets;
ALTER PUBLICATION supabase_realtime ADD TABLE public.ai_messages;
ALTER PUBLICATION supabase_realtime ADD TABLE public.leaderboard;
```

#### 1.2.6 Seed Data
```sql
-- Insert default achievements
INSERT INTO public.achievements (id, title, description, icon, rarity, points, criteria) VALUES
('genesis_architect', 'Genesis Architect', 'Created your first Agent', 'Cpu', 'legendary', 1000, '{"agents_created": 1}'),
('neural_master', 'Neural Master', 'Reached 1000 neural connections', 'Network', 'epic', 500, '{"connections": 1000}'),
('void_walker', 'Void Walker', 'Survived a Kernel Panic', 'Ghost', 'rare', 300, '{"kernel_panics_survived": 1}'),
('diamond_hands', 'Diamond Hands', 'Accumulated $1M in value', 'Diamond', 'epic', 750, '{"total_value": 1000000}'),
('security_breaker', 'Security Breaker', 'Defeated the defense system', 'Lock', 'rare', 400, '{"defenses_broken": 1}'),
('time_traveler', 'Time Traveler', '99.9% uptime for 1 year', 'Clock', 'legendary', 2000, '{"uptime_days": 365, "uptime_percentage": 99.9}');

-- Insert sample network nodes
INSERT INTO public.network_nodes (id, name, location_lat, location_lon, load_percentage, status, region) VALUES
('US-EAST', 'New York Core', 40.7128, -74.0060, 89, 'active', 'North America'),
('EU-WEST', 'London Edge', 51.5074, -0.1278, 45, 'active', 'Europe'),
('ASIA-PAC', 'Tokyo Prime', 35.6762, 139.6503, 67, 'active', 'Asia'),
('SA-EAST', 'Sao Paulo Hub', -23.5505, -46.6333, 92, 'active', 'South America'),
('AUS-SE', 'Sydney Node', -33.8688, 151.2093, 34, 'active', 'Oceania'),
('RU-NORTH', 'Moscow Relay', 55.7558, 37.6173, 78, 'active', 'Europe');
```

---

### 1.3 Supabase Edge Functions

#### 1.3.1 Setup Edge Functions Directory
```bash
# Initialize Supabase functions
supabase functions new process-webhook
supabase functions new send-email
supabase functions new ai-completion
supabase functions new calculate-sentiment
supabase functions new award-achievement
```

#### 1.3.2 Webhook Processor (n8n integration)
```typescript
// supabase/functions/process-webhook/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  try {
    const { type, payload } = await req.json()
    
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    switch(type) {
      case 'new_lead':
        // Process new lead from n8n
        await supabase.from('deals').insert({
          client_name: payload.name,
          value: payload.value,
          status: 'lead',
          metadata: payload
        })
        break
        
      case 'support_ticket':
        // Create support ticket
        await supabase.from('support_tickets').insert({
          subject: payload.subject,
          description: payload.description,
          status: 'open'
        })
        break
        
      default:
        throw new Error(`Unknown webhook type: ${type}`)
    }

    return new Response(JSON.stringify({ success: true }), {
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    })
  }
})
```

#### 1.3.3 Email Sender (Resend integration)
```typescript
// supabase/functions/send-email/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async (req) => {
  const { to, subject, html } = await req.json()
  
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${Deno.env.get('RESEND_API_KEY')}`
    },
    body: JSON.stringify({
      from: 'ALSHAM Quantum <noreply@alsham.quantum>',
      to: [to],
      subject,
      html
    })
  })

  const data = await res.json()
  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

#### 1.3.4 AI Completion Proxy
```typescript
// supabase/functions/ai-completion/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async (req) => {
  const { model, messages } = await req.json()
  
  let apiUrl = ''
  let headers = {}
  let body = {}
  
  switch(model) {
    case 'gpt-4-turbo':
      apiUrl = 'https://api.openai.com/v1/chat/completions'
      headers = {
        'Authorization': `Bearer ${Deno.env.get('OPENAI_API_KEY')}`,
        'Content-Type': 'application/json'
      }
      body = { model: 'gpt-4-turbo-preview', messages }
      break
      
    case 'claude-3-5-sonnet':
      apiUrl = 'https://api.anthropic.com/v1/messages'
      headers = {
        'x-api-key': Deno.env.get('ANTHROPIC_API_KEY'),
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json'
      }
      body = {
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 1024,
        messages
      }
      break
      
    default:
      throw new Error('Unsupported model')
  }
  
  const response = await fetch(apiUrl, {
    method: 'POST',
    headers,
    body: JSON.stringify(body)
  })
  
  const data = await response.json()
  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

---

## PHASE 2: AUTHENTICATION & SECURITY

### 2.1 Supabase Auth Configuration

#### 2.1.1 Enable Auth Providers
- Navigate to Supabase Dashboard → Authentication → Providers
- Enable Email/Password (already enabled)
- Configure Google OAuth:
  - Add Google Client ID and Secret
  - Set redirect URL: `https://your-project.supabase.co/auth/v1/callback`
- Configure GitHub OAuth:
  - Add GitHub Client ID and Secret
  - Set callback URL
- Enable Magic Link (optional)

#### 2.1.2 Auth Email Templates
- Customize confirmation email template
- Customize password reset template
- Customize magic link template
- Add branding (ALSHAM logo, colors)

#### 2.1.3 Auth Hooks (Database Triggers)
```sql
-- Create profile automatically on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, username, full_name, avatar_url)
  VALUES (
    NEW.id,
    NEW.raw_user_meta_data->>'username',
    NEW.raw_user_meta_data->>'full_name',
    NEW.raw_user_meta_data->>'avatar_url'
  );
  
  -- Initialize user stats
  INSERT INTO public.user_stats (user_id, xp, level)
  VALUES (NEW.id, 0, 1);
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

---

### 2.2 Frontend Auth Implementation

#### 2.2.1 Create Auth Context
```typescript
// /lib/auth/AuthContext.tsx
'use client'

import { createContext, useContext, useEffect, useState } from 'react'
import { User, Session } from '@supabase/supabase-js'
import { supabase } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'

interface AuthContextType {
  user: User | null
  session: Session | null
  profile: Profile | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signInWithGoogle: () => Promise<void>
  signInWithGithub: () => Promise<void>
  signOut: () => Promise<void>
  signUp: (email: string, password: string, metadata: any) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<Session | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setUser(session?.user ?? null)
      if (session?.user) {
        fetchProfile(session.user.id)
      }
      setLoading(false)
    })

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
      setUser(session?.user ?? null)
      if (session?.user) {
        fetchProfile(session.user.id)
      } else {
        setProfile(null)
      }
    })

    return () => subscription.unsubscribe()
  }, [])

  const fetchProfile = async (userId: string) => {
    const { data } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', userId)
      .single()
    setProfile(data)
  }

  const signIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    if (error) throw error
    router.push('/dashboard')
  }

  const signInWithGoogle = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`
      }
    })
    if (error) throw error
  }

  const signInWithGithub = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'github',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`
      }
    })
    if (error) throw error
  }

  const signOut = async () => {
    const { error } = await supabase.auth.signOut()
    if (error) throw error
    router.push('/login')
  }

  const signUp = async (email: string, password: string, metadata: any) => {
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: metadata
      }
    })
    if (error) throw error
    router.push('/onboarding')
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        session,
        profile,
        loading,
        signIn,
        signInWithGoogle,
        signInWithGithub,
        signOut,
        signUp,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
```

#### 2.2.2 Create Auth Callback Handler
```typescript
// /app/auth/callback/route.ts
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')

  if (code) {
    const supabase = createRouteHandlerClient({ cookies })
    await supabase.auth.exchangeCodeForSession(code)
  }

  return NextResponse.redirect(new URL('/dashboard', request.url))
}
```

#### 2.2.3 Update Login Page (Real Auth)
```typescript
// /app/login/page.tsx
'use client'

import { useState } from 'react'
import { useAuth } from '@/lib/auth/AuthContext'
import { toast } from 'sonner'
// ... (keep existing visual components)

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [status, setStatus] = useState<'idle' | 'scanning' | 'success' | 'denied'>('idle')
  const { signIn, signInWithGoogle, signInWithGithub } = useAuth()

  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email || !password) return
    
    setStatus('scanning')
    
    try {
      await signIn(email, password)
      setStatus('success')
      toast.success('Authentication successful!')
    } catch (error: any) {
      setStatus('denied')
      toast.error(error.message || 'Authentication failed')
      setTimeout(() => setStatus('idle'), 2000)
    }
  }

  const handleGoogleLogin = async () => {
    try {
      await signInWithGoogle()
    } catch (error: any) {
      toast.error(error.message)
    }
  }

  const handleGithubLogin = async () => {
    try {
      await signInWithGithub()
    } catch (error: any) {
      toast.error(error.message)
    }
  }

  // ... rest of the component (keep visual elements)
}
```

#### 2.2.4 Create Protected Route Middleware
```typescript
// /middleware.ts
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
  const res = NextResponse.next()
  const supabase = createMiddlewareClient({ req, res })

  const {
    data: { session },
  } = await supabase.auth.getSession()

  // Protected routes
  if (req.nextUrl.pathname.startsWith('/dashboard')) {
    if (!session) {
      return NextResponse.redirect(new URL('/login', req.url))
    }
  }

  // Auth routes (redirect if already logged in)
  if (req.nextUrl.pathname === '/login' || req.nextUrl.pathname === '/signup') {
    if (session) {
      return NextResponse.redirect(new URL('/dashboard', req.url))
    }
  }

  // Admin routes
  if (req.nextUrl.pathname.startsWith('/dashboard/admin')) {
    if (!session) {
      return NextResponse.redirect(new URL('/login', req.url))
    }
    
    // Check if user is admin
    const { data: profile } = await supabase
      .from('profiles')
      .select('role')
      .eq('id', session.user.id)
      .single()
    
    if (profile?.role !== 'admin') {
      return NextResponse.redirect(new URL('/dashboard', req.url))
    }
  }

  return res
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/signup', '/onboarding']
}
```

---

### 2.3 Security Hardening

#### 2.3.1 Input Validation (Zod Schemas)
```typescript
// /lib/validations/schemas.ts
import { z } from 'zod'

export const agentSchema = z.object({
  name: z.string().min(3).max(100),
  role: z.enum(['CORE', 'GUARD', 'ANALYST', 'SPECIALIST', 'CHAOS']),
  status: z.enum(['ACTIVE', 'IDLE', 'PROCESSING', 'ERROR', 'OFFLINE']),
  efficiency: z.number().min(0).max(100),
  current_task: z.string().max(500).optional(),
})

export const dealSchema = z.object({
  client_name: z.string().min(2).max(200),
  value: z.number().positive(),
  status: z.enum(['lead', 'negotiation', 'closed', 'lost']),
  probability: z.number().min(0).max(100),
  notes: z.string().max(2000).optional(),
})

export const ticketSchema = z.object({
  subject: z.string().min(5).max(200),
  description: z.string().min(10).max(5000),
  priority: z.enum(['low', 'normal', 'high', 'critical']),
})

export const profileUpdateSchema = z.object({
  username: z.string().min(3).max(30).regex(/^[a-zA-Z0-9_]+$/),
  full_name: z.string().min(2).max(100).optional(),
  bio: z.string().max(500).optional(),
  company: z.string().max(100).optional(),
})
```

#### 2.3.2 API Rate Limiting
```typescript
// /lib/rate-limit.ts
import { LRUCache } from 'lru-cache'

type Options = {
  uniqueTokenPerInterval?: number
  interval?: number
}

export function rateLimit(options?: Options) {
  const tokenCache = new LRUCache({
    max: options?.uniqueTokenPerInterval || 500,
    ttl: options?.interval || 60000,
  })

  return {
    check: (limit: number, token: string) =>
      new Promise<void>((resolve, reject) => {
        const tokenCount = (tokenCache.get(token) as number[]) || [0]
        if (tokenCount[0] === 0) {
          tokenCache.set(token, tokenCount)
        }
        tokenCount[0] += 1

        const currentUsage = tokenCount[0]
        const isRateLimited = currentUsage >= limit

        return isRateLimited ? reject() : resolve()
      }),
  }
}

// Usage in API route:
// const limiter = rateLimit({ interval: 60000, uniqueTokenPerInterval: 500 })
// await limiter.check(10, req.headers.get('x-forwarded-for') || 'anonymous')
```

#### 2.3.3 CSRF Protection
```typescript
// Already handled by Next.js + Supabase Auth Helpers
// But add custom headers for extra security

// /lib/api/headers.ts
export const secureHeaders = {
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
}

// Apply in middleware or API routes
```

#### 2.3.4 Content Security Policy
```typescript
// /next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline' https://cdn.jsdelivr.net;
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self' data:;
      connect-src 'self' https://*.supabase.co wss://*.supabase.co https://api.openai.com https://api.anthropic.com;
      frame-ancestors 'none';
    `.replace(/\s{2,}/g, ' ').trim()
  },
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload'
  },
]

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ]
  },
}
```

---

## PHASE 3: STATE MANAGEMENT & DATA FLOW

### 3.1 Zustand Store Setup

#### 3.1.1 Create Store Structure
```typescript
// /lib/store/index.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

// Import slices
import { createAuthSlice, AuthSlice } from './slices/authSlice'
import { createAgentsSlice, AgentsSlice } from './slices/agentsSlice'
import { createDashboardSlice, DashboardSlice } from './slices/dashboardSlice'
import { createNotificationsSlice, NotificationsSlice } from './slices/notificationsSlice'

export type QuantumStore = AuthSlice & AgentsSlice & DashboardSlice & NotificationsSlice

export const useQuantumStore = create<QuantumStore>()(
  devtools(
    persist(
      immer((...a) => ({
        ...createAuthSlice(...a),
        ...createAgentsSlice(...a),
        ...createDashboardSlice(...a),
        ...createNotificationsSlice(...a),
      })),
      {
        name: 'alsham-quantum-storage',
        partialize: (state) => ({
          // Only persist these parts
          auth: state.auth,
          preferences: state.preferences,
        }),
      }
    )
  )
)
```

#### 3.1.2 Auth Slice
```typescript
// /lib/store/slices/authSlice.ts
import { StateCreator } from 'zustand'
import { User, Session } from '@supabase/supabase-js'
import type { QuantumStore } from '../index'

export interface AuthSlice {
  auth: {
    user: User | null
    session: Session | null
    profile: Profile | null
    loading: boolean
  }
  setUser: (user: User | null) => void
  setSession: (session: Session | null) => void
  setProfile: (profile: Profile | null) => void
  setAuthLoading: (loading: boolean) => void
  clearAuth: () => void
}

export const createAuthSlice: StateCreator
  QuantumStore,
  [["zustand/immer", never]],
  [],
  AuthSlice
> = (set) => ({
  auth: {
    user: null,
    session: null,
    profile: null,
    loading: true,
  },
  setUser: (user) =>
    set((state) => {
      state.auth.user = user
    }),
  setSession: (session) =>
    set((state) => {
      state.auth.session = session
    }),
  setProfile: (profile) =>
    set((state) => {
      state.auth.profile = profile
    }),
  setAuthLoading: (loading) =>
    set((state) => {
      state.auth.loading = loading
    }),
  clearAuth: () =>
    set((state) => {
      state.auth = {
        user: null,
        session: null,
        profile: null,
        loading: false,
      }
    }),
})
```

#### 3.1.3 Agents Slice
```typescript
// /lib/store/slices/agentsSlice.ts
import { StateCreator } from 'zustand'
import { supabase } from '@/lib/supabase/client'
import type { QuantumStore } from '../index'

export interface AgentsSlice {
  agents: Agent[]
  agentsLoading: boolean
  agentsError: string | null
  selectedAgent: Agent | null
  fetchAgents: () => Promise<void>
  createAgent: (agent: Partial<Agent>) => Promise<Agent>
  updateAgent: (id: string, updates: Partial<Agent>) => Promise<void>
  deleteAgent: (id: string) => Promise<void>
  selectAgent: (agent: Agent | null) => void
  subscribeToAgents: () => () => void
}

export const createAgentsSlice: StateCreator
  QuantumStore,
  [["zustand/immer", never]],
  [],
  AgentsSlice
> = (set, get) => ({
  agents: [],
  agentsLoading: false,
  agentsError: null,
  selectedAgent: null,

  fetchAgents: async () => {
    set((state) => {
      state.agentsLoading = true
      state.agentsError = null
    })

    try {
      const { data, error } = await supabase
        .from('agents')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) throw error

      set((state) => {
        state.agents = data || []
        state.agentsLoading = false
      })
    } catch (error: any) {
      set((state) => {
        state.agentsError = error.message
        state.agentsLoading = false
      })
    }
  },

  createAgent: async (agent) => {
    const { data, error } = await supabase
      .from('agents')
      .insert(agent)
      .select()
      .single()

    if (error) throw error

    set((state) => {
      state.agents.unshift(data)
    })

    return data
  },

  updateAgent: async (id, updates) => {
    const { error } = await supabase
      .from('agents')
      .update(updates)
      .eq('id', id)

    if (error) throw error

    set((state) => {
      const index = state.agents.findIndex((a) => a.id === id)
      if (index !== -1) {
        state.agents[index] = { ...state.agents[index], ...updates }
      }
    })
  },

  deleteAgent: async (id) => {
    const { error } = await supabase.from('agents').delete().eq('id', id)

    if (error) throw error

    set((state) => {
      state.agents = state.agents.filter((a) => a.id !== id)
      if (state.selectedAgent?.id === id) {
        state.selectedAgent = null
      }
    })
  },

  selectAgent: (agent) =>
    set((state) => {
      state.selectedAgent = agent
    }),

  subscribeToAgents: () => {
    const channel = supabase
      .channel('agents-changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'agents' },
        (payload) => {
          const { eventType, new: newRecord, old: oldRecord } = payload

          set((state) => {
            switch (eventType) {
              case 'INSERT':
                state.agents.unshift(newRecord as Agent)
                break
              case 'UPDATE':
                const updateIndex = state.agents.findIndex(
                  (a) => a.id === newRecord.id
                )
                if (updateIndex !== -1) {
                  state.agents[updateIndex] = newRecord as Agent
                }
                break
              case 'DELETE':
                state.agents = state.agents.filter((a) => a.id !== oldRecord.id)
                break
            }
          })
        }
      )
      .subscribe()

    return () => {
      channel.unsubscribe()
    }
  },
})
```

#### 3.1.4 Dashboard Slice
```typescript
// /lib/store/slices/dashboardSlice.ts
import { StateCreator } from 'zustand'
import type { QuantumStore } from '../index'

export interface DashboardSlice {
  systemMetrics: {
    activeAgents: number
    roi: number
    savings: number
    systemLoad: number
    quantumStability: number
    uptime: number
  }
  networkNodes: NetworkNode[]
  fetchSystemMetrics: () => Promise<void>
  fetchNetworkNodes: () => Promise<void>
}

export const createDashboardSlice: StateCreator
  QuantumStore,
  [["zustand/immer", never]],
  [],
  DashboardSlice
> = (set) => ({
  systemMetrics: {
    activeAgents: 0,
    roi: 0,
    savings: 0,
    systemLoad: 0,
    quantumStability: 100,
    uptime: 99.9,
  },
  networkNodes: [],

  fetchSystemMetrics: async () => {
    // Implementation
  },

  fetchNetworkNodes: async () => {
    const { data } = await supabase.from('network_nodes').select('*')
    set((state) => {
      state.networkNodes = data || []
    })
  },
})
```

#### 3.1.5 Notifications Slice
```typescript
// /lib/store/slices/notificationsSlice.ts
import { StateCreator } from 'zustand'
import { toast } from 'sonner'
import type { QuantumStore } from '../index'

interface Notification {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  message: string
  read: boolean
  createdAt: Date
}

export interface NotificationsSlice {
  notifications: Notification[]
  unreadCount: number
  addNotification: (notif: Omit<Notification, 'id' | 'createdAt' | 'read'>) => void
  markAsRead: (id: string) => void
  markAllAsRead: () => void
  clearNotifications: () => void
}

export const createNotificationsSlice: StateCreator
  QuantumStore,
  [["zustand/immer", never]],
  [],
  NotificationsSlice
> = (set) => ({
  notifications: [],
  unreadCount: 0,

  addNotification: (notif) => {
    const newNotif: Notification = {
      ...notif,
      id: crypto.randomUUID(),
      read: false,
      createdAt: new Date(),
    }

    set((state) => {
      state.notifications.unshift(newNotif)
      state.unreadCount += 1
    })

    // Show toast
    toast[notif.type](notif.title, {
      description: notif.message,
    })
  },

  markAsRead: (id) =>
    set((state) => {
      const notif = state.notifications.find((n) => n.id === id)
      if (notif && !notif.read) {
        notif.read = true
        state.unreadCount -= 1
      }
    }),

  markAllAsRead: () =>
    set((state) => {
      state.notifications.forEach((n) => (n.read = true))
      state.unreadCount = 0
    }),

  clearNotifications: () =>
    set((state) => {
      state.notifications = []
      state.unreadCount = 0
    }),
})
```

---

### 3.2 React Query Setup

#### 3.2.1 Configure Query Client
```typescript
// /lib/react-query/client.ts
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      cacheTime: 1000 * 60 * 30, // 30 minutes
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})
```

#### 3.2.2 Create Query Provider
```typescript
// /lib/react-query/QueryProvider.tsx
'use client'

import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { queryClient } from './client'

export function QueryProvider({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
```

#### 3.2.3 Custom Hooks with React Query
```typescript
// /lib/hooks/useAgents.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase/client'
import { toast } from 'sonner'

export function useAgents() {
  return useQuery({
    queryKey: ['agents'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('agents')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) throw error
      return data as Agent[]
    },
  })
}

export function useCreateAgent() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (agent: Partial<Agent>) => {
      const { data, error } = await supabase
        .from('agents')
        .insert(agent)
        .select()
        .single()

      if (error) throw error
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] })
      toast.success('Agent created successfully!')
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to create agent')
    },
  })
}

export function useUpdateAgent() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({ id, updates }: { id: string; updates: Partial<Agent> }) => {
      const { error } = await supabase
        .from('agents')
        .update(updates)
        .eq('id', id)

      if (error) throw error
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] })
      toast.success('Agent updated!')
    },
    onError: (error: any) => {
      toast.error(error.message)
    },
  })
}

export function useDeleteAgent() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (id: string) => {
      const { error } = await supabase.from('agents').delete().eq('id', id)
      if (error) throw error
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] })
      toast.success('Agent deleted')
    },
  })
}
```

---

### 3.3 Error Handling System

#### 3.3.1 Error Boundary Component
```typescript
// /components/ErrorBoundary.tsx
'use client'

import React from 'react'
import { AlertTriangle, RefreshCw } from 'lucide-react'

interface ErrorBoundaryProps {
  children: React.ReactNode
  fallback?: React.ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends React.Component
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo)
    // Send to Sentry or other error tracking service
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <div className="min-h-screen flex items-center justify-center bg-black p-8">
          <div className="max-w-md w-full bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl p-8 text-center">
            <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-red-500/20 flex items-center justify-center">
              <AlertTriangle className="w-8 h-8 text-red-500" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">System Error</h2>
            <p className="text-gray-400 mb-6">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="px-6 py-3 bg-[var(--color-primary)] text-black font-bold rounded-xl hover:bg-[var(--color-accent)] transition-all flex items-center gap-2 mx-auto"
            >
              <RefreshCw className="w-4 h-4" />
              Reload System
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
```

#### 3.3.2 Global Error Handler
```typescript
// /lib/errors/handler.ts
import { toast } from 'sonner'

export class AppError extends Error {
  constructor(
    message: string,
    public code?: string,
    public statusCode?: number
  ) {
    super(message)
    this.name = 'AppError'
  }
}

export function handleError(error: unknown) {
  if (error instanceof AppError) {
    toast.error(error.message)
    return
  }

  if (error instanceof Error) {
    toast.error(error.message)
    console.error(error)
    return
  }

  toast.error('An unexpected error occurred')
  console.error(error)
}

// Usage:
// try {
//   await someOperation()
// } catch (error) {
//   handleError(error)
// }
```

#### 3.3.3 Toast Provider
```typescript
// /components/ToastProvider.tsx
'use client'

import { Toaster } from 'sonner'

export function ToastProvider() {
  return (
    <Toaster
      position="top-right"
      expand={true}
      richColors
      closeButton
      theme="dark"
      toastOptions={{
        style: {
          background: 'rgba(0, 0, 0, 0.9)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(20px)',
        },
      }}
    />
  )
}
```

---

### 3.4 Loading States

#### 3.4.1 Skeleton Components
```typescript
// /components/ui/skeleton.tsx
export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={`animate-pulse rounded-md bg-white/10 ${className}`}
    />
  )
}

// Usage examples:
export function AgentCardSkeleton() {
  return (
    <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
      <div className="flex items-center gap-4 mb-4">
        <Skeleton className="w-12 h-12 rounded-xl" />
        <div className="flex-1">
          <Skeleton className="h-4 w-32 mb-2" />
          <Skeleton className="h-3 w-20" />
        </div>
      </div>
      <Skeleton className="h-20 w-full mb-4" />
      <Skeleton className="h-2 w-full" />
    </div>
  )
}
```

#### 3.4.2 Loading Overlay
```typescript
// /components/ui/loading-overlay.tsx
import { Loader2 } from 'lucide-react'

export function LoadingOverlay({ message }: { message?: string }) {
  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="text-center">
        <Loader2 className="w-12 h-12 text-[var(--color-primary)] animate-spin mx-auto mb-4" />
        {message && (
          <p className="text-white font-mono text-sm">{message}</p>
        )}
      </div>
    </div>
  )
}
```

---

## PHASE 4: CORE FEATURES IMPLEMENTATION

### 4.1 Connect All Pages to Backend

For each of the 26 pages, we need to:

1. Replace mock data with real Supabase queries
2. Implement CRUD operations
3. Add real-time subscriptions where needed
4. Add loading and error states
5. Add optimistic updates

#### 4.1.1 Agents Page (Already done, but improve)
```typescript
// /app/dashboard/agents/page.tsx
'use client'

import { useAgents, useDeleteAgent } from '@/lib/hooks/useAgents'
import { AgentCardSkeleton } from '@/components/ui/skeleton'
import { ErrorBoundary } from '@/components/ErrorBoundary'

export default function AgentsPage() {
  const { data: agents, isLoading, error } = useAgents()
  const deleteAgent = useDeleteAgent()

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
        {Array.from({ length: 6 }).map((_, i) => (
          <AgentCardSkeleton key={i} />
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center text-red-400">
        Error loading agents: {error.message}
      </div>
    )
  }

  return (
    <ErrorBoundary>
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
        {agents?.map((agent) => (
          <AgentCard
            key={agent.id}
            agent={agent}
            onDelete={() => deleteAgent.mutate(agent.id)}
          />
        ))}
      </div>
    </ErrorBoundary>
  )
}
```

#### 4.1.2 Dashboard Page (Connect Metrics)
```typescript
// /app/dashboard/page.tsx
'use client'

import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase/client'

export default function DashboardPage() {
  const { data: metrics } = useQuery({
    queryKey: ['dashboard-metrics'],
    queryFn: async () => {
      // Fetch active agents count
      const { count: activeAgents } = await supabase
        .from('agents')
        .select('*', { count: 'exact', head: true })
        .eq('status', 'ACTIVE')

      // Fetch total deals value (closed)
      const { data: deals } = await supabase
        .from('deals')
        .select('value')
        .eq('status', 'closed')
      
      const totalRevenue = deals?.reduce((sum, d) => sum + d.value, 0) || 0

      // Fetch threats blocked
      const { count: threatsBlocked } = await supabase
        .from('security_threats')
        .select('*', { count: 'exact', head: true })
        .eq('blocked', true)

      return {
        activeAgents: activeAgents || 0,
        totalRevenue,
        threatsBlocked: threatsBlocked || 0,
        // ... other metrics
      }
    },
    refetchInterval: 30000, // Refetch every 30s
  })

  return (
    // ... render with real data
  )
}
```

#### 4.1.3 Sales Engine (Connect Deals)
```typescript
// /app/dashboard/sales/page.tsx
'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase/client'

function useDeals() {
  return useQuery({
    queryKey: ['deals'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('deals')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(20)

      if (error) throw error
      return data as Deal[]
    },
  })
}

function useCreateDeal() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (deal: Partial<Deal>) => {
      const { data, error } = await supabase
        .from('deals')
        .insert(deal)
        .select()
        .single()

      if (error) throw error
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deals'] })
    },
  })
}

export default function SalesPage() {
  const { data: deals, isLoading } = useDeals()
  const createDeal = useCreateDeal()

  // ... rest of implementation
}
```

#### 4.1.4 Support Ops (Connect Tickets)
```typescript
// Similar pattern for tickets
function useSupportTickets() {
  return useQuery({
    queryKey: ['support-tickets'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('support_tickets')
        .select(`
          *,
          assigned_to:profiles!assigned_to(username, avatar_url)
        `)
        .order('created_at', { ascending: false })

      if (error) throw error
      return data
    },
  })
}

// Subscribe to new tickets in real-time
useEffect(() => {
  const channel = supabase
    .channel('tickets-changes')
    .on(
      'postgres_changes',
      { event: 'INSERT', schema: 'public', table: 'support_tickets' },
      (payload) => {
        toast.success('New support ticket received!')
        queryClient.invalidateQueries({ queryKey: ['support-tickets'] })
      }
    )
    .subscribe()

  return () => {
    channel.unsubscribe()
  }
}, [])
```

#### 4.1.5 Social Pulse (External API Integration)
```typescript
// /app/dashboard/social/page.tsx
// This requires external API (Twitter, Reddit)
// For now, implement with mock data that looks real

function useSocialFeed() {
  return useQuery({
    queryKey: ['social-feed'],
    queryFn: async () => {
      // Option 1: Use stored posts from DB (scraped earlier)
      const { data } = await supabase
        .from('social_posts')
        .select('*')
        .order('posted_at', { ascending: false })
        .limit(50)

      return data

      // Option 2: Call Edge Function that proxies Twitter API
      // const res = await fetch('/api/social/fetch-posts')
      // return res.json()
    },
    refetchInterval: 60000, // Every minute
  })
}

// Sentiment calculation
function useSocialSentiment() {
  return useQuery({
    queryKey: ['social-sentiment'],
    queryFn: async () => {
      const { data } = await supabase
        .from('social_posts')
        .select('sentiment_score')
      
      const avg = data?.reduce((sum, p) => sum + (p.sentiment_score || 0), 0) / data.length
      return Math.round(avg)
    },
  })
}
```

#### 4.1.6 Gamification (Connect XP System)
```typescript
// /app/dashboard/gamification/page.tsx
function useUserStats() {
  const { user } = useAuth()
  
  return useQuery({
    queryKey: ['user-stats', user?.id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('user_stats')
        .select('*')
        .eq('user_id', user?.id)
        .single()

      if (error) throw error
      return data
    },
    enabled: !!user,
  })
}

function useAchievements() {
  return useQuery({
    queryKey: ['achievements'],
    queryFn: async () => {
      const { data } = await supabase
        .from('achievements')
        .select(`
          *,
          user_achievements!left(unlocked_at)
        `)
      return data
    },
  })
}

function useLeaderboard() {
  return useQuery({
    queryKey: ['leaderboard'],
    queryFn: async () => {
      const { data } = await supabase
        .from('leaderboard')
        .select('*')
        .order('rank', { ascending: true })
        .limit(100)
      return data
    },
  })
}

// Award XP function
async function awardXP(userId: string, amount: number, reason: string) {
  const { data } = await supabase.rpc('award_xp', {
    p_user_id: userId,
    p_xp: amount
  })
  
  if (data.leveled_up) {
    toast.success(`Level Up! You're now level ${data.new_level}!`, {
      icon: '🎉',
    })
  }
}
```

#### 4.1.7 Orion AI (Connect OpenAI/Anthropic)
```typescript
// /app/dashboard/orion/page.tsx
import { useChat } from 'ai/react' // Vercel AI SDK

export default function OrionPage() {
  const [selectedModel, setSelectedModel] = useState('claude-3-5-sonnet')
  
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/ai/chat',
    body: {
      model: selectedModel,
    },
  })

  // ... rest of UI
}

// /app/api/ai/chat/route.ts
import { StreamingTextResponse, OpenAIStream, AnthropicStream } from 'ai'
import OpenAI from 'openai'
import Anthropic from '@anthropic-ai/sdk'

export async function POST(req: Request) {
  const { messages, model } = await req.json()

  if (model.startsWith('gpt')) {
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
    const response = await openai.chat.completions.create({
      model: model,
      messages,
      stream: true,
    })
    const stream = OpenAIStream(response)
    return new StreamingTextResponse(stream)
  }

  if (model.startsWith('claude')) {
    const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })
    const response = await anthropic.messages.stream({
      model: model,
      max_tokens: 1024,
      messages,
    })
    const stream = AnthropicStream(response)
    return new StreamingTextResponse(stream)
  }

  return new Response('Model not supported', { status: 400 })
}
```

#### 4.1.8 Value Dash (Connect Stripe)
```typescript
// /app/dashboard/value/page.tsx
function useUserBalance() {
  const { user } = useAuth()
  
  return useQuery({
    queryKey: ['user-balance', user?.id],
    queryFn: async () => {
      const { data } = await supabase
        .from('user_balance')
        .select('*')
        .eq('user_id', user?.id)
        .single()
      return data
    },
  })
}

function useTransactions() {
  const { user } = useAuth()
  
  return useQuery({
    queryKey: ['transactions', user?.id],
    queryFn: async () => {
      const { data } = await supabase
        .from('transactions')
        .select('*')
        .eq('user_id', user?.id)
        .order('created_at', { ascending: false })
        .limit(50)
      return data
    },
  })
}

// Stripe checkout
async function createCheckoutSession(amount: number) {
  const res = await fetch('/api/stripe/checkout', {
    method: 'POST',
    body: JSON.stringify({ amount }),
  })
  const { url } = await res.json()
  window.location.href = url
}
```

#### 4.1.9 Network (Connect Live Nodes)
```typescript
// /app/dashboard/network/page.tsx
function useNetworkNodes() {
  return useQuery({
    queryKey: ['network-nodes'],
    queryFn: async () => {
      const { data } = await supabase
        .from('network_nodes')
        .select('*')
      return data as NetworkNode[]
    },
    refetchInterval: 5000, // Every 5s
  })
}

// Ping nodes in background
useEffect(() => {
  const pingNodes = async () => {
    // Call Edge Function to ping all nodes
    await fetch('/api/network/ping-all', { method: 'POST' })
  }
  
  const interval = setInterval(pingNodes, 30000)
  return () => clearInterval(interval)
}, [])
```

#### 4.1.10 Containment (Connect Security)
```typescript
// /app/dashboard/containment/page.tsx
function useSecurityThreats() {
  return useQuery({
    queryKey: ['security-threats'],
    queryFn: async () => {
      const { data } = await supabase
        .from('security_threats')
        .select('*')
        .order('detected_at', { ascending: false })
        .limit(100)
      return data
    },
  })
}

function useDefconLevel() {
  return useQuery({
    queryKey: ['defcon-level'],
    queryFn: async () => {
      const { data } = await supabase
        .from('system_defcon_log')
        .select('level')
        .order('changed_at', { ascending: false })
        .limit(1)
        .single()
      return data?.level || 5
    },
  })
}

function useUpdateDefcon() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ level, reason }: { level: number; reason: string }) => {
      const { error } = await supabase.from('system_defcon_log').insert({
        level,
        reason,
      })
      if (error) throw error
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['defcon-level'] })
    },
  })
}
```

#### 4.1.11 Admin God Mode (Implement Safely)
```typescript
// /app/dashboard/admin/page.tsx
// IMPORTANT: This route should be protected by middleware (already done)

function useAdminStats() {
  return useQuery({
    queryKey: ['admin-stats'],
    queryFn: async () => {
      // Total users
      const { count: totalUsers } = await supabase
        .from('profiles')
        .select('*', { count: 'exact', head: true })

      // Active sessions
      const { count: activeSessions } = await supabase
        .from('user_sessions')
        .select('*', { count: 'exact', head: true })
        .gt('expires_at', new Date().toISOString())

      // System metrics
      const { data: metrics } = await supabase
        .from('system_metrics')
        .select('*')
        .order('recorded_at', { ascending: false })
        .limit(1)

      return {
        totalUsers: totalUsers || 0,
        activeSessions: activeSessions || 0,
        metrics: metrics?.[0],
      }
    },
  })
}

// Dangerous actions (require confirmation)
function useSystemPurge() {
  return useMutation({
    mutationFn: async (targetTable: string) => {
      // Only admins can call this
      const { error } = await supabase.rpc('admin_purge_table', {
        table_name: targetTable
      })
      if (error) throw error
    },
  })
}
```

---

### 4.2 Implement Real-Time Features

#### 4.2.1 Live Dashboard Updates
```typescript
// /app/dashboard/page.tsx
useEffect(() => {
  // Subscribe to system metrics changes
  const channel = supabase
    .channel('dashboard-updates')
    .on(
      'postgres_changes',
      { event: '*', schema: 'public', table: 'system_metrics' },
      () => {
        queryClient.invalidateQueries({ queryKey: ['dashboard-metrics'] })
      }
    )
    .on(
      'postgres_changes',
      { event: '*', schema: 'public', table: 'agents' },
      () => {
        queryClient.invalidateQueries({ queryKey: ['agents'] })
      }
    )
    .subscribe()

  return () => {
    channel.unsubscribe()
  }
}, [])
```

#### 4.2.2 Live Leaderboard
```typescript
// /app/dashboard/gamification/page.tsx
useEffect(() => {
  const channel = supabase
    .channel('leaderboard-updates')
    .on(
      'postgres_changes',
      { event: '*', schema: 'public', table: 'user_stats' },
      async () => {
        // Refresh leaderboard
        await supabase.rpc('refresh_leaderboard')
        queryClient.invalidateQueries({ queryKey: ['leaderboard'] })
      }
    )
    .subscribe()

  return () => channel.unsubscribe()
}, [])
```

#### 4.2.3 Live Support Tickets
```typescript
// /app/dashboard/support/page.tsx
useEffect(() => {
  const channel = supabase
    .channel('support-updates')
    .on(
      'postgres_changes',
      { event: 'INSERT', schema: 'public', table: 'support_tickets' },
      (payload) => {
        toast.info('New support ticket!', {
          description: payload.new.subject,
        })
        queryClient.invalidateQueries({ queryKey: ['support-tickets'] })
      }
    )
    .on(
      'postgres_changes',
      { event: 'UPDATE', schema: 'public', table: 'support_tickets' },
      (payload) => {
        if (payload.new.status === 'resolved') {
          toast.success('Ticket resolved!', {
            description: payload.new.subject,
          })
        }
        queryClient.invalidateQueries({ queryKey: ['support-tickets'] })
      }
    )
    .subscribe()

  return () => channel.unsubscribe()
}, [])
```

---

### 4.3 Background Jobs & Cron

#### 4.3.1 Setup Vercel Cron Jobs
```json
// vercel.json
{
  "crons": [
    {
      "path": "/api/cron/refresh-leaderboard",
      "schedule": "*/5 * * * *"
    },
    {
      "path": "/api/cron/ping-network-nodes",
      "schedule": "*/1 * * * *"
    },
    {
      "path": "/api/cron/fetch-social-posts",
      "schedule": "*/15 * * * *"
    },
    {
      "path": "/api/cron/calculate-metrics",
      "schedule": "*/10 * * * *"
    }
  ]
}
```

#### 4.3.2 Cron Route: Refresh Leaderboard
```typescript
// /app/api/cron/refresh-leaderboard/route.ts
import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

export async function GET(request: Request) {
  // Verify cron secret
  const authHeader = request.headers.get('authorization')
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 })
  }

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )

  await supabase.rpc('refresh_leaderboard')

  return NextResponse.json({ success: true })
}
```

#### 4.3.3 Cron Route: Ping Network Nodes
```typescript
// /app/api/cron/ping-network-nodes/route.ts
export async function GET(request: Request) {
  // Verify cron secret
  const authHeader = request.headers.get('authorization')
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 })
  }

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )

  const { data: nodes } = await supabase.from('network_nodes').select('*')

  for (const node of nodes || []) {
    // Simulate ping (or actual network ping)
    const latency = Math.random() * 100
    const load = Math.random() * 100

    await supabase
      .from('network_nodes')
      .update({
        load_percentage: load,
        last_ping: new Date().toISOString(),
      })
      .eq('id', node.id)
  }

  return NextResponse.json({ success: true, pinged: nodes?.length })
}
```

---

## PHASE 5: ADVANCED INTEGRATIONS

### 5.1 n8n Automation Workflows

#### 5.1.1 Setup n8n Instance
- Deploy n8n (self-hosted or n8n.cloud)
- Connect to Supabase webhook endpoint
- Create workflow templates

#### 5.1.2 Workflow: Lead Capture
```
Webhook Trigger (n8n) 
  → Validate Data 
  → Deduplicate (Check Supabase) 
  → Insert to Supabase (deals table) 
  → Send Email (Resend) 
  → Notify Slack (optional)
```

#### 5.1.3 Workflow: Support Ticket Auto-Assign
```
Supabase Trigger (new ticket) 
  → Calculate Sentiment (OpenAI) 
  → Assign to Agent (based on load) 
  → Send Email to Assignee 
  → Update Supabase
```

#### 5.1.4 Workflow: Daily Reports
```
Cron Trigger (daily 9am) 
  → Fetch Metrics (Supabase) 
  → Generate Report (Template) 
  → Send Email (Resend) 
  → Post to Slack
```

---

### 5.2 Email System (Resend)

#### 5.2.1 Setup Resend
- Create account at resend.com
- Verify domain (alsham.quantum)
- Get API key
- Add to .env

#### 5.2.2 Email Templates
```typescript
// /lib/emails/templates.ts
export const emailTemplates = {
  welcome: (name: string) => ({
    subject: 'Welcome to ALSHAM Quantum',
    html: `
      <div style="font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #00FFD0;">Welcome, ${name}!</h1>
        <p>Your quantum journey begins now...</p>
      </div>
    `
  }),
  
  passwordReset: (resetLink: string) => ({
    subject: 'Reset Your ALSHAM Password',
    html: `
      <div>
        <h2>Password Reset Request</h2>
        <p>Click the link below to reset your password:</p>
        <a href="${resetLink}">Reset Password</a>
      </div>
    `
  }),
  
  achievementUnlocked: (achievement: string) => ({
    subject: '🏆 Achievement Unlocked!',
    html: `
      <div>
        <h1>Congratulations!</h1>
        <p>You've unlocked: <strong>${achievement}</strong></p>
      </div>
    `
  }),
}
```

#### 5.2.3 Send Email Function
```typescript
// /lib/emails/send.ts
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

export async function sendEmail({
  to,
  subject,
  html,
}: {
  to: string
  subject: string
  html: string
}) {
  try {
    const { data, error } = await resend.emails.send({
      from: 'ALSHAM Quantum <noreply@alsham.quantum>',
      to: [to],
      subject,
      html,
    })

    if (error) {
      console.error('Email send error:', error)
      throw error
    }

    return data
  } catch (error) {
    console.error('Failed to send email:', error)
    throw error
  }
}
```

---

### 5.3 Stripe Integration (Payments)

#### 5.3.1 Setup Stripe
- Create Stripe account
- Get API keys (test & live)
- Setup webhook endpoint
- Add to .env

#### 5.3.2 Checkout Session
```typescript
// /app/api/stripe/checkout/route.ts
import { NextResponse } from 'next/server'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-11-20.acacia',
})

export async function POST(req: Request) {
  const { amount } = await req.json()

  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [
      {
        price_data: {
          currency: 'usd',
          product_data: {
            name: 'ALSHAM Credits',
          },
          unit_amount: amount * 100, // cents
        },
        quantity: 1,
      },
    ],
    mode: 'payment',
    success_url: `${req.headers.get('origin')}/dashboard/value?success=true`,
    cancel_url: `${req.headers.get('origin')}/dashboard/value?canceled=true`,
  })

  return NextResponse.json({ url: session.url })
}
```

#### 5.3.3 Webhook Handler
```typescript
// /app/api/stripe/webhook/route.ts
import { NextResponse } from 'next/server'
import Stripe from 'stripe'
import { supabase } from '@/lib/supabase/admin'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(req: Request) {
  const body = await req.text()
  const sig = req.headers.get('stripe-signature')!

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err: any) {
    return new Response(`Webhook Error: ${err.message}`, { status: 400 })
  }

  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object as Stripe.Checkout.Session
      
      // Add credit to user balance
      await supabase.from('transactions').insert({
        user_id: session.client_reference_id,
        type: 'credit',
        amount: session.amount_total! / 100,
        status: 'completed',
        metadata: { stripe_session_id: session.id },
      })

      await supabase.rpc('update_user_balance', {
        p_user_id: session.client_reference_id,
        p_amount: session.amount_total! / 100,
      })
      break

    default:
      console.log(`Unhandled event type ${event.type}`)
  }

  return NextResponse.json({ received: true })
}
```

---

### 5.4 Social Media APIs

#### 5.4.1 Twitter API Integration
```typescript
// /app/api/social/fetch-twitter/route.ts
// Note: Requires Twitter API v2 access

import { NextResponse } from 'next/server'

export async function GET() {
  const bearer = process.env.TWITTER_BEARER_TOKEN

  const response = await fetch(
    'https://api.twitter.com/2/tweets/search/recent?query=AI OR quantum computing&max_results=100',
    {
      headers: {
        Authorization: `Bearer ${bearer}`,
      },
    }
  )

  const data = await response.json()

  // Store in Supabase
  for (const tweet of data.data || []) {
    await supabase.from('social_posts').upsert({
      platform: 'twitter',
      external_id: tweet.id,
      author: tweet.author_id,
      content: tweet.text,
      posted_at: tweet.created_at,
    })
  }

  return NextResponse.json({ imported: data.data?.length || 0 })
}
```

#### 5.4.2 Reddit API Integration
```typescript
// /app/api/social/fetch-reddit/route.ts
export async function GET() {
  const response = await fetch(
    'https://www.reddit.com/r/artificial/hot.json?limit=100',
    {
      headers: {
        'User-Agent': 'ALSHAM Quantum/1.0',
      },
    }
  )

  const data = await response.json()

  for (const post of data.data.children) {
    const p = post.data
    await supabase.from('social_posts').upsert({
      platform: 'reddit',
      external_id: p.id,
      author: p.author,
      content: `${p.title}\n\n${p.selftext}`,
      likes_count: p.ups,
      comments_count: p.num_comments,
      posted_at: new Date(p.created_utc * 1000).toISOString(),
    })
  }

  return NextResponse.json({ imported: data.data.children.length })
}
```

---

## PHASE 6: PERFORMANCE OPTIMIZATION

### 6.1 Canvas Optimization

#### 6.1.1 OffscreenCanvas (Web Workers)
```typescript
// /lib/canvas/workers/neural-nexus.worker.ts
self.onmessage = function (e) {
  const { nodes, rotation } = e.data

  // Perform heavy 3D calculations here
  const projectedNodes = nodes.map((node: any) => {
    // Rotation matrices
    const sinX = Math.sin(rotation.x)
    const cosX = Math.cos(rotation.x)
    const sinY = Math.sin(rotation.y)
    const cosY = Math.cos(rotation.y)

    // Rotate Y
    const x1 = node.x * cosY - node.z * sinY
    const z1 = node.z * cosY + node.x * sinY

    // Rotate X
    const y2 = node.y * cosX - z1 * sinX
    const z2 = z1 * cosX + node.y * sinX

    // Perspective
    const scale = 600 / (600 + z2)
    const px = x1 * scale
    const py = y2 * scale

    return { ...node, px, py, scale, z: z2 }
  })

  self.postMessage(projectedNodes)
}

// Usage in component:
const worker = new Worker(new URL('@/lib/canvas/workers/neural-nexus.worker.ts', import.meta.url))

useEffect(() => {
  worker.postMessage({ nodes, rotation })
  
  worker.onmessage = (e) => {
    setProjectedNodes(e.data)
  }

  return () => worker.terminate()
}, [nodes, rotation])
```

#### 6.1.2 RequestAnimationFrame Throttling
```typescript
// /lib/canvas/utils.ts
export function useAnimationFrame(callback: (deltaTime: number) => void, fps: number = 60) {
  const requestRef = useRef<number>()
  const previousTimeRef = useRef<number>()
  const fpsInterval = 1000 / fps

  const animate = (time: number) => {
    if (previousTimeRef.current !== undefined) {
      const deltaTime = time - previousTimeRef.current

      if (deltaTime >= fpsInterval) {
        callback(deltaTime)
        previousTimeRef.current = time - (deltaTime % fpsInterval)
      }
    } else {
      previousTimeRef.current = time
    }

    requestRef.current = requestAnimationFrame(animate)
  }

  useEffect(() => {
    requestRef.current = requestAnimationFrame(animate)
    return () => {
      if (requestRef.current) {
        cancelAnimationFrame(requestRef.current)
      }
    }
  }, [callback, fps])
}

// Usage:
useAnimationFrame((deltaTime) => {
  // Render canvas at 30fps instead of 60fps
  renderCanvas()
}, 30)
```

#### 6.1.3 Lazy Load Heavy Pages
```typescript
// /app/dashboard/layout.tsx
import dynamic from 'next/dynamic'

// Lazy load heavy pages with loading state
const NeuralNexusPage = dynamic(() => import('./nexus/page'), {
  loading: () => <PageSkeleton />,
  ssr: false, // Disable SSR for canvas-heavy pages
})

const EvolutionPage = dynamic(() => import('./evolution/page'), {
  loading: () => <PageSkeleton />,
  ssr: false,
})
```

---

### 6.2 Bundle Optimization

#### 6.2.1 Next.js Config
```javascript
// next.config.js
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['lucide-react', '@supabase/supabase-js'],
  },

  webpack: (config, { isServer }) => {
    if (!isServer) {
      // Don't bundle these on client
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      }
    }

    return config
  },

  images: {
    domains: ['your-supabase-project.supabase.co'],
    formats: ['image/avif', 'image/webp'],
  },
}

module.exports = nextConfig
```

#### 6.2.2 Dynamic Imports for Large Components
```typescript
// Instead of:
import { OrionHead } from '@/components/canvas/OrionHead'

// Do:
const OrionHead = dynamic(() => import('@/components/canvas/OrionHead'), {
  ssr: false,
  loading: () => <Skeleton className="w-full h-96" />
})
```

#### 6.2.3 Bundle Analyzer
```bash
npm install @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer(nextConfig)

# Run:
ANALYZE=true npm run build
```

---

### 6.3 Database Optimization

#### 6.3.1 Add Composite Indexes
```sql
-- For complex queries
CREATE INDEX idx_agents_user_status ON public.agents(user_id, status);
CREATE INDEX idx_deals_user_status_value ON public.deals(user_id, status, value DESC);
CREATE INDEX idx_tickets_assigned_status ON public.support_tickets(assigned_to, status);
CREATE INDEX idx_social_platform_date ON public.social_posts(platform, posted_at DESC);
```

#### 6.3.2 Materialized Views for Dashboards
```sql
-- Create materialized view for dashboard stats
CREATE MATERIALIZED VIEW dashboard_stats AS
SELECT
  COUNT(DISTINCT a.id) FILTER (WHERE a.status = 'ACTIVE') as active_agents,
  COUNT(DISTINCT u.id) as total_users,
  COALESCE(SUM(d.value) FILTER (WHERE d.status = 'closed'), 0) as total_revenue,
  COUNT(DISTINCT st.id) FILTER (WHERE st.blocked = true) as threats_blocked
FROM agents a
CROSS JOIN profiles u
CROSS JOIN deals d
CROSS JOIN security_threats st;

-- Refresh periodically (via cron)
REFRESH MATERIALIZED VIEW dashboard_stats;
```

#### 6.3.3 Query Optimization
```typescript
// Bad: N+1 query problem
const agents = await supabase.from('agents').select('*')
for (const agent of agents.data) {
  const logs = await supabase.from('agent_logs').select('*').eq('agent_id', agent.id)
}

// Good: Single query with join
const { data } = await supabase
  .from('agents')
  .select(`
    *,
    logs:agent_logs(*)
  `)
```

---

### 6.4 Caching Strategy

#### 6.4.1 React Query Cache Configuration
```typescript
// /lib/react-query/client.ts
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      cacheTime: 1000 * 60 * 30, // 30 minutes
      refetchOnWindowFocus: false,
      retry: (failureCount, error: any) => {
        // Don't retry on 4xx errors
        if (error?.status >= 400 && error?.status < 500) {
          return false
        }
        return failureCount < 3
      },
    },
  },
})
```

#### 6.4.2 Service Worker for API Caching
```typescript
// /public/sw.js
const CACHE_NAME = 'alsham-quantum-v1'
const CACHE_URLS = [
  '/',
  '/dashboard',
  // ... static assets
]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CACHE_URLS)
    })
  )
})

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request)
    })
  )
})
```

#### 6.4.3 CDN Configuration (Vercel)
```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/images/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/api/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, s-maxage=60, stale-while-revalidate=120',
          },
        ],
      },
    ]
  },
}
```

---

## PHASE 7: TESTING & QUALITY

### 7.1 Unit Tests (Vitest)

#### 7.1.1 Setup Vitest
```bash
npm install -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/jest-dom
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

```typescript
// tests/setup.ts
import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

afterEach(() => {
  cleanup()
})
```

#### 7.1.2 Test Examples
```typescript
// tests/unit/components/AgentCard.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { AgentCard } from '@/components/AgentCard'

describe('AgentCard', () => {
  const mockAgent = {
    id: '1',
    name: 'Test Agent',
    role: 'CORE',
    status: 'ACTIVE',
    efficiency: 95,
    current_task: 'Processing data',
  }

  it('renders agent information correctly', () => {
    render(<AgentCard agent={mockAgent} />)
    
    expect(screen.getByText('Test Agent')).toBeInTheDocument()
    expect(screen.getByText('CORE')).toBeInTheDocument()
    expect(screen.getByText('95%')).toBeInTheDocument()
  })

  it('calls onDelete when delete button is clicked', () => {
    const onDelete = vi.fn()
    render(<AgentCard agent={mockAgent} onDelete={onDelete} />)
    
    const deleteButton = screen.getByRole('button', { name: /delete/i })
    fireEvent.click(deleteButton)
    
    expect(onDelete).toHaveBeenCalledWith(mockAgent.id)
  })
})
```

```typescript
// tests/unit/lib/store/agentsSlice.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { useQuantumStore } from '@/lib/store'

describe('AgentsSlice', () => {
  beforeEach(() => {
    useQuantumStore.setState({ agents: [] })
  })

  it('adds agent to store', () => {
    const { agents } = useQuantumStore.getState()
    expect(agents).toHaveLength(0)

    // ... test add logic
  })
})
```

---

### 7.2 Integration Tests

#### 7.2.1 API Route Tests
```typescript
// tests/integration/api/agents.test.ts
import { describe, it, expect } from 'vitest'
import { POST, GET } from '@/app/api/agents/route'

describe('/api/agents', () => {
  it('creates a new agent', async () => {
    const request = new Request('http://localhost:3000/api/agents', {
      method: 'POST',
      body: JSON.stringify({
        name: 'Test Agent',
        role: 'CORE',
      }),
    })

    const response = await POST(request)
    const data = await response.json()

    expect(response.status).toBe(201)
    expect(data.name).toBe('Test Agent')
  })

  it('returns 400 for invalid data', async () => {
    const request = new Request('http://localhost:3000/api/agents', {
      method: 'POST',
      body: JSON.stringify({ name: '' }), // Invalid
    })

    const response = await POST(request)
    expect(response.status).toBe(400)
  })
})
```

---

### 7.3 E2E Tests (Playwright)

#### 7.3.1 Setup Playwright
```bash
npm install -D @playwright/test
npx playwright install
```

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
})
```

#### 7.3.2 E2E Test Examples
```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('should login successfully', async ({ page }) => {
    await page.goto('/login')
    
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    
    await expect(page).toHaveURL('/dashboard')
    await expect(page.locator('h1')).toContainText('Welcome')
  })

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login')
    
    await page.fill('input[type="email"]', 'wrong@example.com')
    await page.fill('input[type="password"]', 'wrongpass')
    await page.click('button[type="submit"]')
    
    await expect(page.locator('[role="alert"]')).toBeVisible()
  })
})
```

```typescript
// tests/e2e/agents.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Agents Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login first
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard')
  })

  test('should create a new agent', async ({ page }) => {
    await page.goto('/dashboard/agents')
    
    await page.click('button:has-text("Create Agent")')
    await page.fill('input[name="name"]', 'E2E Test Agent')
    await page.selectOption('select[name="role"]', 'CORE')
    await page.click('button[type="submit"]')
    
    await expect(page.locator('text=E2E Test Agent')).toBeVisible()
  })

  test('should delete an agent', async ({ page }) => {
    await page.goto('/dashboard/agents')
    
    const firstAgent = page.locator('[data-testid="agent-card"]').first()
    await firstAgent.hover()
    await firstAgent.locator('button[aria-label="Delete"]').click()
    await page.click('button:has-text("Confirm")')
    
    await expect(page.locator('text=Agent deleted')).toBeVisible()
  })
})
```

---

### 7.4 Visual Regression Testing

#### 7.4.1 Setup Percy (or Chromatic)
```bash
npm install -D @percy/cli @percy/playwright
```

```typescript
// tests/visual/dashboard.spec.ts
import percySnapshot from '@percy/playwright'
import { test } from '@playwright/test'

test('Dashboard visual regression', async ({ page }) => {
  await page.goto('/dashboard')
  await percySnapshot(page, 'Dashboard - Default State')
  
  // Change theme
  await page.click('[data-testid="theme-switcher"]')
  await percySnapshot(page, 'Dashboard - Dark Theme')
})
```

---

### 7.5 Accessibility Testing

#### 7.5.1 Install axe-core
```bash
npm install -D @axe-core/playwright
```

```typescript
// tests/a11y/dashboard.spec.ts
import { test, expect } from '@playwright/test'
import { injectAxe, checkA11y } from 'axe-playwright'

test('Dashboard accessibility', async ({ page }) => {
  await page.goto('/dashboard')
  await injectAxe(page)
  
  await checkA11y(page, null, {
    detailedReport: true,
    detailedReportOptions: {
      html: true,
    },
  })
})
```

---

## PHASE 8: DEVOPS & DEPLOYMENT

### 8.1 CI/CD Pipeline (GitHub Actions)

#### 8.1.1 Main Workflow
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run lint

  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run type-check

  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run test:unit
      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/

  build:
    runs-on: ubuntu-latest
    needs: [lint, type-check, unit-tests]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v3
        with:
          name: build
          path: .next/

  deploy-preview:
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v3
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

  deploy-production:
    runs-on: ubuntu-latest
    needs: [build, e2e-tests]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID}}
          vercel-args: '--prod'
```

---

### 8.2 Environment Management

#### 8.2.1 Environment Files
```bash
# .env.local (development)
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...

# .env.preview (staging)
NEXT_PUBLIC_SUPABASE_URL=https://staging-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...

# .env.production
NEXT_PUBLIC_SUPABASE_URL=https://project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
```

#### 8.2.2 Vercel Environment Variables
- Add all environment variables in Vercel dashboard
- Separate configs for Preview/Production
- Sensitive keys should be encrypted

---

### 8.3 Monitoring & Logging

#### 8.3.1 Sentry Setup
```bash
npm install @sentry/nextjs
```

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  integrations: [
    new Sentry.BrowserTracing(),
    new Sentry.Replay({
      maskAllText: false,
      blockAllMedia: false,
    }),
  ],
})
```

```typescript
// sentry.server.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
})
```

#### 8.3.2 Vercel Analytics
```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}
```

#### 8.3.3 Custom Logging
```typescript
// /lib/logger.ts
import * as Sentry from '@sentry/nextjs'

export const logger = {
  info: (message: string, data?: any) => {
    console.log(`[INFO] ${message}`, data)
  },
  
  warn: (message: string, data?: any) => {
    console.warn(`[WARN] ${message}`, data)
    Sentry.captureMessage(message, {
      level: 'warning',
      extra: data,
    })
  },
  
  error: (message: string, error?: Error, data?: any) => {
    console.error(`[ERROR] ${message}`, error, data)
    Sentry.captureException(error || new Error(message), {
      extra: data,
    })
  },
}
```

---

## PHASE 9: POLISH & ACCESSIBILITY

### 9.1 Accessibility Improvements

#### 9.1.1 Add ARIA Labels
```typescript
// Update all interactive elements
<button
  onClick={handleClick}
  aria-label="Create new agent"
  aria-describedby="tooltip-create"
>
  <Plus className="w-4 h-4" />
</button>

<input
  type="text"
  aria-label="Search agents"
  aria-describedby="search-help"
  placeholder="Search..."
/>
```

#### 9.1.2 Keyboard Navigation
```typescript
// /components/ui/Dialog.tsx
'use client'

import { useEffect, useRef } from 'react'
import { X } from 'lucide-react'

export function Dialog({ isOpen, onClose, children }) {
  const dialogRef = useRef<HTMLDivElement>(null)
  const previousFocus = useRef<HTMLElement | null>(null)

  useEffect(() => {
    if (isOpen) {
      // Save previous focus
      previousFocus.current = document.activeElement as HTMLElement
      
      // Focus first focusable element in dialog
      const firstFocusable = dialogRef.current?.querySelector<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
      firstFocusable?.focus()

      // Trap focus inside dialog
      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          onClose()
        }
        
        if (e.key === 'Tab') {
          const focusable = Array.from(
            dialogRef.current?.querySelectorAll<HTMLElement>(
              'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            ) || []
          )
          
          const first = focusable[0]
          const last = focusable[focusable.length - 1]
          
          if (e.shiftKey && document.activeElement === first) {
            e.preventDefault()
            last?.focus()
          } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault()
            first?.focus()
          }
        }
      }

      document.addEventListener('keydown', handleKeyDown)
      return () => {
        document.removeEventListener('keydown', handleKeyDown)
        previousFocus.current?.focus()
      }
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <div
      className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center"
      role="dialog"
      aria-modal="true"
      aria-labelledby="dialog-title"
    >
      <div ref={dialogRef} className="bg-black/90 border border-white/10 rounded-2xl p-6 max-w-md w-full">
        <button
          onClick={onClose}
          aria-label="Close dialog"
          className="absolute top-4 right-4"
        >
          <X className="w-5 h-5" />
        </button>
        {children}
      </div>
    </div>
  )
}
```

#### 9.1.3 Screen Reader Announcements
```typescript
// /components/ui/ScreenReaderOnly.tsx
export function ScreenReaderOnly({ children }: { children: React.ReactNode }) {
  return (
    <span className="sr-only">
      {children}
    </span>
  )
}

// Usage:
<button>
  <Trash2 className="w-4 h-4" />
  <ScreenReaderOnly>Delete agent</ScreenReaderOnly>
</button>
```

---

### 9.2 Mobile Optimization

#### 9.2.1 Touch-Friendly Targets
```typescript
// Ensure minimum 44x44px touch targets
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      minWidth: {
        'touch': '44px',
      },
      minHeight: {
        'touch': '44px',
      },
    },
  },
}

// Apply to buttons:
<button className="min-w-touch min-h-touch p-3">
  <Icon />
</button>
```

#### 9.2.2 Disable Canvas on Mobile (Fallback)
```typescript
// /lib/hooks/useIsMobile.ts
import { useState, useEffect } from 'react'

export function useIsMobile() {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768)
    }
    
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  return isMobile
}

// Usage in canvas pages:
const isMobile = useIsMobile()

return isMobile ? (
  <SimplifiedView data={data} />
) : (
  <CanvasView data={data} />
)
```

---

### 9.3 SEO Optimization

#### 9.3.1 Metadata
```typescript
// /app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: {
    default: 'ALSHAM Quantum - Enterprise AI CRM',
    template: '%s | ALSHAM Quantum',
  },
  description: 'The most advanced AI-powered CRM system for enterprise automation',
  keywords: ['CRM', 'AI', 'Enterprise', 'Automation', 'Analytics'],
  authors: [{ name: 'ALSHAM Team' }],
  creator: 'ALSHAM Global',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://alsham.quantum',
    siteName: 'ALSHAM Quantum',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    creator: '@alshamquantum',
  },
  robots: {
    index: true,
    follow: true,
  },
}
```

#### 9.3.2 Sitemap
```typescript
// /app/sitemap.ts
import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://alsham.quantum',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 1,
    },
    {
      url: 'https://alsham.quantum/dashboard',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.8,
    },
    // ... add all public pages
  ]
}
```

#### 9.3.3 Robots.txt
```typescript
// /app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/dashboard/', '/api/'],
    },
    sitemap: 'https://alsham.quantum/sitemap.xml',
  }
}
```

---

## PHASE 10: DOCUMENTATION & HANDOFF

### 10.1 Technical Documentation

#### 10.1.1 README.md
```markdown
# ALSHAM QUANTUM v13.3

Enterprise-grade AI-powered CRM platform with quantum computing aesthetics.

## Quick Start

\```bash
# Install dependencies
npm install

# Setup environment variables
cp .env.example .env.local
# Edit .env.local with your keys

# Run development server
npm run dev

# Open http://localhost:3000
\```

## Project Structure

\```
/frontend
├── /src
│   ├── /app                 # Next.js App Router
│   │   ├── /dashboard       # Main dashboard pages
│   │   ├── /api             # API routes
│   │   └── /auth            # Authentication pages
│   ├── /components
│   │   ├── /ui              # shadcn/ui components
│   │   ├── /layout          # Layout components
│   │   └── /canvas          # Canvas animations
│   ├── /lib
│   │   ├── /supabase        # Supabase client
│   │   ├── /store           # Zustand state management
│   │   ├── /hooks           # Custom React hooks
│   │   └── /utils           # Utility functions
│   └── /types               # TypeScript types
├── /tests
│   ├── /unit                # Unit tests (Vitest)
│   ├── /integration         # Integration tests
│   └── /e2e                 # E2E tests (Playwright)
└── /docs                    # Documentation
\```

## Key Features

- ✅ 26 fully functional pages
- ✅ Real-time database with Supabase
- ✅ AI integration (OpenAI, Anthropic)
- ✅ Canvas-based 3D visualizations
- ✅ Theme system (9 themes)
- ✅ Gamification with XP & achievements
- ✅ Complete authentication system
- ✅ Stripe payment integration

## Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Backend**: Supabase (PostgreSQL, Auth, Storage, Realtime)
- **State**: Zustand + React Query
- **AI**: OpenAI, Anthropic Claude
- **Payments**: Stripe
- **Email**: Resend
- **Automation**: n8n
- **Deployment**: Vercel
- **Monitoring**: Sentry, Vercel Analytics

## Available Scripts

\```bash
npm run dev          # Development server
npm run build        # Production build
npm run start        # Production server
npm run lint         # Lint code
npm run type-check   # TypeScript check
npm run test:unit    # Run unit tests
npm run test:e2e     # Run E2E tests
npm run test:a11y    # Run accessibility tests
\```

## Environment Variables

See `.env.example` for all required environment variables.

## Deployment

### Vercel (Recommended)

1. Connect GitHub repository
2. Add environment variables
3. Deploy

### Self-Hosted

\```bash
npm run build
npm run start
\```

## License

Proprietary - ALSHAM Global © 2025
```

#### 10.1.2 API Documentation
```markdown
# API Documentation

## Authentication

All API routes require authentication via Supabase JWT token.

### Headers

\```
Authorization: Bearer <supabase_jwt_token>
Content-Type: application/json
\```

## Endpoints

### Agents

#### GET /api/agents
Get all agents for the authenticated user.

**Response:**
\```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "Agent Name",
      "role": "CORE",
      "status": "ACTIVE",
      "efficiency": 95.5,
      "created_at": "2025-01-01T00:00:00Z"
    }
  ]
}
\```

#### POST /api/agents
Create a new agent.

**Request Body:**
\```json
{
  "name": "My Agent",
  "role": "CORE",
  "current_task": "Processing data"
}
\```

**Response:**
\```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "My Agent",
    ...
  }
}
\```

### AI Completions

#### POST /api/ai/chat
Stream AI completion responses.

**Request Body:**
\```json
{
  "model": "claude-3-5-sonnet",
  "messages": [
    {
      "role": "user",
      "content": "Hello!"
    }
  ]
}
\```

**Response:** Server-Sent Events (SSE) stream

---

For full API documentation, see [API.md](./API.md)
```

#### 10.1.3 CONTRIBUTING.md
```markdown
# Contributing to ALSHAM Quantum

## Development Workflow

1. Create feature branch from `develop`
2. Make changes
3. Write/update tests
4. Run linter and type-check
5. Create Pull Request
6. Wait for CI to pass
7. Request code review
8. Merge after approval

## Code Style

- Use TypeScript strict mode
- Follow ESLint rules
- Use Prettier for formatting
- Write meaningful commit messages (Conventional Commits)

## Commit Messages

\```
feat: add new agent creation flow
fix: resolve theme switching bug
docs: update API documentation
test: add unit tests for AgentCard
refactor: optimize canvas rendering
\```

## Testing

- Write unit tests for all utilities and hooks
- Add integration tests for API routes
- Include E2E tests for critical user flows
- Maintain >70% test coverage

## Pull Request Guidelines

- Keep PRs focused and small
- Include screenshots for UI changes
- Update documentation
- Link related issues
```

---

### 10.2 User Documentation

#### 10.2.1 User Guide
```markdown
# ALSHAM Quantum User Guide

## Getting Started

### Creating Your First Agent

1. Navigate to **Dashboard → Sentinelas**
2. Click **Create Agent** button
3. Fill in agent details:
   - Name
   - Role (CORE, GUARD, ANALYST, SPECIALIST)
   - Initial task
4. Click **Create**

### Understanding the Dashboard

The main dashboard shows:
- **Active Agents**: Number of running agents
- **Efficiency**: Overall system performance
- **ROI**: Return on investment metrics
- **Threats Blocked**: Security statistics

### Using Orion AI

1. Navigate to **Intelligence Layer → Orion AI**
2. Select AI model (GPT-4, Claude, etc.)
3. Type your message or use voice input
4. Receive AI-powered responses

### Gamification System

Earn XP by:
- Creating agents
- Completing tasks
- Achieving milestones

Unlock achievements to climb the leaderboard!

## Troubleshooting

### Agent Not Responding
1. Check agent status
2. Verify network connection
3. Restart agent if needed

### Can't Login
1. Check email/password
2. Reset password if needed
3. Clear browser cache

## Support

For support, contact: support@alsham.quantum
```

---

### 10.3 Deployment Checklist

#### 10.3.1 Pre-Launch Checklist
```markdown
# Pre-Launch Checklist

## Security
- [ ] All API keys in environment variables
- [ ] RLS enabled on all Supabase tables
- [ ] Rate limiting configured
- [ ] HTTPS enforced
- [ ] CSP headers configured
- [ ] Authentication working
- [ ] Admin routes protected

## Performance
- [ ] Lighthouse score >90
- [ ] Bundle size optimized
- [ ] Images optimized
- [ ] Lazy loading implemented
- [ ] Caching configured
- [ ] CDN enabled

## Functionality
- [ ] All 26 pages working
- [ ] Database migrations run
- [ ] Real-time subscriptions working
- [ ] Email system working
- [ ] Payment system tested
- [ ] AI integrations working

## Testing
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Accessibility tests passing
- [ ] Manual testing complete

## Monitoring
- [ ] Sentry configured
- [ ] Analytics setup
- [ ] Error tracking working
- [ ] Performance monitoring
- [ ] Uptime monitoring

## Legal
- [ ] Privacy policy
- [ ] Terms of service
- [ ] Cookie consent
- [ ] GDPR compliance
- [ ] Backup strategy

## Documentation
- [ ] README complete
- [ ] API docs complete
- [ ] User guide complete
- [ ] Admin guide complete
- [ ] Runbook for incidents
```

---

## FINAL CHECKLIST

### ✅ Phase 1: Foundation
- [ ] Environment setup
- [ ] Database schema (30+ tables)
- [ ] Indexes & RLS
- [ ] Edge Functions
- [ ] Seed data

### ✅ Phase 2: Authentication
- [ ] Supabase Auth configured
- [ ] Social login (Google, GitHub)
- [ ] Protected routes
- [ ] Session management
- [ ] Security hardening

### ✅ Phase 3: State Management
- [ ] Zustand store
- [ ] React Query
- [ ] Error boundaries
- [ ] Toast notifications
- [ ] Loading states

### ✅ Phase 4: Core Features
- [ ] All 26 pages connected to backend
- [ ] CRUD operations
- [ ] Real-time subscriptions
- [ ] Background jobs
- [ ] Cron tasks

### ✅ Phase 5: Integrations
- [ ] n8n workflows
- [ ] Email (Resend)
- [ ] Payments (Stripe)
- [ ] Social media APIs
- [ ] AI APIs (OpenAI, Anthropic)

### ✅ Phase 6: Performance
- [ ] Canvas optimization
- [ ] Bundle optimization
- [ ] Database optimization
- [ ] Caching strategy
- [ ] CDN configuration

### ✅ Phase 7: Testing
- [ ] Unit tests (>70% coverage)
- [ ] Integration tests
- [ ] E2E tests
- [ ] Visual regression tests
- [ ] Accessibility tests

### ✅ Phase 8: DevOps
- [ ] CI/CD pipeline
- [ ] Environment management
- [ ] Monitoring (Sentry)
- [ ] Analytics (Vercel)
- [ ] Logging

### ✅ Phase 9: Polish
- [ ] Accessibility (WCAG AA)
- [ ] Mobile optimization
- [ ] SEO optimization
- [ ] Error messages
- [ ] Loading states

### ✅ Phase 10: Documentation
- [ ] Technical docs
- [ ] API docs
- [ ] User guide
- [ ] Deployment guide
- [ ] Runbook

---

## 🎯 SUCCESS CRITERIA

**System is 10/10 when:**

1. ✅ All 26 pages fully functional with real data
2. ✅ Authentication & security working perfectly
3. ✅ Real-time features operational
4. ✅ All integrations live (AI, Payments, Email)
5. ✅ Performance metrics met (Lighthouse >90)
6. ✅ Test coverage >70%
7. ✅ Zero critical bugs
8. ✅ Monitoring & alerting active
9. ✅ Documentation complete
10. ✅ Production deployment successful

---

**Built with 💎 by ALSHAM Global**  
**Target: Enterprise-Grade 10/10 Production System**

---