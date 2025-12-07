'use client';

import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Menu, Sparkles, CheckCircle } from 'lucide-react';

import Sidebar from '@/components/layout/Sidebar';
import OrionAssistant from '@/components/orion/OrionAssistant';
import { ToastContainer } from '@/components/ui/ToastContainer';
import { PlanBadge, PlanBadgeLarge } from '@/components/ui/PlanBadge';
import type { DashboardProfile } from '@/lib/auth/server';

export interface DashboardShellProps {
  profile: DashboardProfile;
  hasFounderAccess: boolean;
  isEnterprise: boolean;
  children: React.ReactNode;
}

export function DashboardShell({
  profile: _profile,
  hasFounderAccess: _hasFounderAccess,
  isEnterprise: _isEnterprise,
  children,
}: DashboardShellProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const searchParams = useSearchParams();

  useEffect(() => {
    const sessionId = searchParams.get('session_id');
    const success = searchParams.get('success');

    if (success === 'true' && sessionId) {
      setShowSuccessModal(true);

      fetch(`/api/stripe/checkout?session_id=${sessionId}`)
        .then((res) => res.json())
        .then((data) => {
          if (data.paid) {
            window.location.href = '/dashboard';
          }
        })
        .catch((err) => console.error('Erro ao verificar checkout:', err));

      setTimeout(() => setShowSuccessModal(false), 5000);

      const url = new URL(window.location.href);
      url.searchParams.delete('session_id');
      url.searchParams.delete('success');
      url.searchParams.delete('plan');
      window.history.replaceState({}, '', url.pathname + (url.search || ''));
    }
  }, [searchParams]);

  return (
    <div className="min-h-screen relative flex">
      {showSuccessModal && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/80 backdrop-blur-sm animate-fadeIn">
          <div className="bg-gradient-to-b from-green-900/50 to-black border border-green-500/50 rounded-3xl p-8 max-w-md mx-4 text-center shadow-2xl">
            <div className="w-20 h-20 rounded-full bg-green-500/20 border border-green-500/50 flex items-center justify-center mx-auto mb-6">
              <CheckCircle className="w-10 h-10 text-green-400" />
            </div>
            <h2 className="text-2xl font-black text-white mb-2">Pagamento Confirmado! 🎉</h2>
            <p className="text-gray-400 mb-4">Bem-vindo ao ALSHAM QUANTUM. Seu acesso está sendo ativado.</p>
            <div className="text-xs text-gray-500">Redirecionando automaticamente...</div>
          </div>
        </div>
      )}

      <Sidebar isOpen={isMobileMenuOpen} onClose={() => setIsMobileMenuOpen(false)} />

      <div className="flex-1 flex flex-col min-h-screen transition-all duration-300 ease-in-out lg:pl-64">
        <header className="lg:hidden h-16 flex items-center justify-between px-4 border-b border-white/10 bg-black/40 backdrop-blur-md sticky top-0 z-30">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsMobileMenuOpen(true)}
              className="p-2 -ml-2 text-white hover:bg-white/10 rounded-lg transition-colors"
              aria-label="Abrir menu"
            >
              <Menu className="w-6 h-6" />
            </button>
            <span className="font-bold text-white tracking-widest flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[var(--color-primary)]" />
              ALSHAM
            </span>
          </div>
          <PlanBadge />
        </header>

        <main className="flex-1 relative p-4 md:p-8 overflow-x-hidden">
          <div className="mx-auto max-w-[1600px] w-full relative z-10 animate-fadeIn">{children}</div>
        </main>
      </div>

      <ToastContainer />
      <PlanBadgeLarge />
      <OrionAssistant />
    </div>
  );
}
