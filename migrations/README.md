# Database Migrations - ALSHAM QUANTUM

This directory contains SQL migrations for the ALSHAM QUANTUM database schema.

## Migration Strategy

- **UP migrations**: Apply changes to the database
- **DOWN migrations**: Rollback/undo changes

## Applied Migrations

### 20251125_phase_1_2_core_crm_support.sql
**Date Applied:** 2025-11-25  
**Status:** ✅ Applied successfully  
**Phases:** 1.2.1 (Core) + 1.2.2 (Dashboard) + 1.2.3 (CRM) + 1.2.4 (Support)

**Tables Created/Modified:**

#### Phase 1.2.1: Core Tables
1. **profiles** (12 columns) - NEW
   - User profiles extending auth.users
   - RLS enabled with public read, authenticated update
   
2. **user_sessions** (10 columns) - NEW
   - Session tracking for authenticated users
   - 3 indexes for performance
   - RLS with user-specific access
   
3. **agents** (9→14 columns) - EXPANDED
   - Added 5 columns: user_id, metadata, neural_load, uptime_seconds, version
   - **139 agents preserved** ✅
   - RLS enabled with public access
   
4. **agent_logs** (6 columns) - NEW
   - Logging system for agent activities
   - 4 indexes for query performance
   - CHECK constraint on log_level
   
5. **agent_connections** (11 columns) - NEW
   - Neural network connections between agents
   - 6 indexes for graph queries
   - CHECK constraints, UNIQUE constraint
   - Prevents self-connections and duplicates

#### Phase 1.2.2: Dashboard & Metrics
6. **system_metrics** (9 columns) - NEW
   - System-wide metrics for dashboard
   - 5 indexes for time-series queries
   - Category CHECK constraint

7. **network_nodes** (13 columns) - NEW
   - 3D network visualization nodes
   - 3D coordinates (position_x, y, z)
   - 5 indexes including 3D position composite
   - 2 CHECK constraints (node_type, status)
   - 3 RLS policies

#### Phase 1.2.3: CRM Module
8. **deals** (12 columns) - NEW
   - Sales pipeline and deal tracking
   - 6 indexes for CRM queries
   - 2 CHECK constraints (status, probability)
   - 3 RLS policies (user-scoped access)

9. **deal_activities** (7 columns) - NEW
   - Timeline of activities for each deal
   - 5 indexes for timeline queries
   - 1 CHECK constraint (activity_type)
   - 2 RLS policies (inherit deal ownership)

#### Phase 1.2.4: Support Module
10. **support_tickets** (11 columns) - NEW
    - Support ticket management system
    - 6 indexes for ticket queries
    - 2 CHECK constraints (status, priority)
    - 3 RLS policies (user + assignment based)

11. **ticket_messages** (7 columns) - NEW
    - Conversation threads within tickets
    - 5 indexes for message queries
    - 2 RLS policies (inherit ticket access)
    - Supports internal/external messages

**Statistics:**
- Total Tables: 11 (10 new + 1 expanded)
- Total Indexes: 46+
- Total Constraints: 22+
- RLS Policies: 25+
- Agents Preserved: 139/139 ✅
- Phase 1.2.1: COMPLETE ✅
- Phase 1.2.2: COMPLETE ✅
- Phase 1.2.3: COMPLETE ✅
- Phase 1.2.4: COMPLETE ✅

**Rollback:** Use `20251125_phase_1_2_core_crm_support_down.sql`

**Verification:** All tables tested with sample inserts and queries. All constraints validated. Zero data loss.

---

## How to Apply Migrations

### Using Supabase CLI
```bash
supabase db push
```

### Manual Application
```bash
psql -h your-db-host -d your-database -f migrations/20251125_phase_1_2_core_crm_support.sql
```

### Rollback
```bash
psql -h your-db-host -d your-database -f migrations/20251125_phase_1_2_core_crm_support_down.sql
```

---

## Next Phases

- **Phase 1.2.5:** Social Media Module (social_posts, social_trends)
- **Phase 1.2.6:** Gamification Module (user_stats, achievements, leaderboard)
- **Phase 1.2.7:** API Module (api_keys, api_logs, rate_limits)
- **Phase 1.2.8:** Security Module (security_logs, audit_trail)
- **Phase 1.2.9:** Finance Module (transactions, invoices)
- **Phase 1.2.10:** AI Module (ai_models, training_sessions, predictions)

See `ALSHAM QUANTUM - ROADMAP TO PERFECT.md` for complete roadmap.

---

## Database Structure Overview
```
ALSHAM QUANTUM Database (11 Tables)
├── Core System (5 tables)
│   ├── profiles
│   ├── user_sessions
│   ├── agents (139 active)
│   ├── agent_logs
│   └── agent_connections
├── Dashboard & Analytics (2 tables)
│   ├── system_metrics
│   └── network_nodes
├── CRM Module (2 tables)
│   ├── deals
│   └── deal_activities
└── Support Module (2 tables)
    ├── support_tickets
    └── ticket_messages
```

**Total:** 94 columns across 11 tables
**Ready for:** Production deployment