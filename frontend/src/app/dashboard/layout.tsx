/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - DASHBOARD LAYOUT (SERVER + CLIENT SHELL)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/layout.tsx
 * 🔐 Proteção server-side via Supabase + helper requireDashboardAccess
 * ═══════════════════════════════════════════════════════════════
 */

import React from 'react';
import { DashboardShell } from '@/components/dashboard/DashboardShell';
import { requireDashboardAccess } from '@/lib/auth/server';

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { profile, hasFounderAccess, isEnterprise } = await requireDashboardAccess();

  return (
    <DashboardShell
      profile={profile}
      hasFounderAccess={hasFounderAccess}
      isEnterprise={isEnterprise}
    >
      {children}
    </DashboardShell>
  );
}
