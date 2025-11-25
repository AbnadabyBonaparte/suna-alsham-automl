# Database Migrations - ALSHAM QUANTUM

This directory contains SQL migrations for the ALSHAM QUANTUM database schema.

## Migration Strategy

- **UP migrations**: Apply changes to the database
- **DOWN migrations**: Rollback/undo changes

## Applied Migrations

### 20251125_phase_1_2_core_and_metrics.sql
**Date Applied:** 2025-11-25  
**Status:** ✅ Applied successfully via MCP  
**Phase:** 1.2.1 (Core Tables) + 1.2.2 (Dashboard & Metrics)

**Tables Created/Modified:**
1. **profiles** (12 columns) - NEW
   - User profiles extending auth.users
   - RLS enabled with public read, authenticated update
   
2. **user_sessions** (10 columns) - NEW
   - Session tracking for authenticated users
   - 2 indexes for performance
   - RLS with user-specific access
   
3. **agents** (9→14 columns) - EXPANDED
   - Added 5 columns: user_id, metadata, neural_load, uptime_seconds, version
   - **139 agents preserved** ✅
   - RLS enabled
   
4. **agent_logs** (6 columns) - NEW
   - Logging system for agent activities
   - 3 indexes for query performance
   - CHECK constraint on log_level
   
5. **agent_connections** (11 columns) - NEW
   - Neural network connections between agents
   - 4 indexes for graph queries
   - 4 CHECK constraints, 1 UNIQUE constraint
   - Prevents self-connections and duplicates
   
6. **system_metrics** (9 columns) - NEW
   - System-wide metrics for dashboard
   - 4 indexes for time-series queries
   - Category CHECK constraint

7. **network_nodes** (13 columns) - NEW
   - 3D network visualization nodes
   - 3D coordinates (position_x, y, z)
   - 4 indexes including 3D position composite
   - 2 CHECK constraints (node_type, status)
   - 3 RLS policies

8. **deals** (12 columns) - NEW
   - Sales pipeline and deal tracking
   - 5 indexes for CRM queries
   - 2 CHECK constraints (status, probability)
   - 3 RLS policies (user-scoped access)

9. **deal_activities** (7 columns) - NEW
   - Timeline of activities for each deal
   - 4 indexes for timeline queries
   - 1 CHECK constraint (activity_type)
   - 2 RLS policies (inherit deal ownership)

**Statistics:**
- Total Tables: 9 (8 new + 1 expanded)
- Total Indexes: 35
- Total Constraints: 18+
- RLS Policies: 20
- Agents Preserved: 139/139 ✅
- Phase 1.2.3 CRM: COMPLETE ✅

**Rollback:** Use `20251125_phase_1_2_core_and_metrics_down.sql`

**Verification:** All tables tested with sample inserts and queries. All constraints validated. Zero data loss.

---

## How to Apply Migrations

### Using Supabase CLI
```bash
supabase db push
```

### Manual Application
```bash
psql -h your-db-host -d your-database -f migrations/20251125_phase_1_2_core_and_metrics.sql
```

### Rollback
```bash
psql -h your-db-host -d your-database -f migrations/20251125_phase_1_2_core_and_metrics_down.sql
```

---

## Next Phases

- **Phase 1.2.3:** Network Nodes table
- **Phase 1.2.4:** CRM Tables (deals, deal_activities)
- **Phase 1.2.5:** Support System (tickets, messages)
- **Phase 1.2.6:** Gamification (user_stats, achievements, leaderboard)
- **Phase 1.2.7:** Security & Financial tables

See `ROADMAP TO PERFECT.md` for complete roadmap.
