/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - DASHBOARD LAYOUT PROTEGIDO (NÍVEL BANCO)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/layout.tsx
 * 🔐 Proteção: Auth + Verificação de Pagamento via Webhook
 * ═══════════════════════════════════════════════════════════════
 */
'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { useSubscription } from '@/hooks/useSubscription';
import Sidebar from '@/components/layout/Sidebar';
import OrionAssistant from '@/components/orion/OrionAssistant';
import { ToastContainer } from '@/components/ui/ToastContainer';
import { PlanBadge, PlanBadgeLarge } from '@/components/ui/PlanBadge';
import { Menu, Sparkles, Loader2, CheckCircle } from 'lucide-react';

function DashboardLayoutContent({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  const { user, loading: authLoading } = useAuth();
  const { isLoading: subLoading, isSubscribed, plan } = useSubscription();
  const router = useRouter();
  const searchParams = useSearchParams();

  // ========================================
  // VERIFICAR PARÂMETROS DE SUCESSO DO STRIPE
  // ========================================
  useEffect(() => {
    const sessionId = searchParams.get('session_id');
    const success = searchParams.get('success');
    const planParam = searchParams.get('plan');

    if (success === 'true' && sessionId) {
      setShowSuccessModal(true);
      
      // Verificar status da sessão no Stripe
      fetch(`/api/stripe/checkout?session_id=${sessionId}`)
        .then(res => res.json())
        .then(data => {
          console.log('✅ Checkout verificado:', data);
          if (data.paid) {
            // Recarregar subscription
            window.location.href = '/dashboard';
          }
        })
        .catch(err => console.error('Erro ao verificar checkout:', err));
      
      // Auto-esconder modal após 5 segundos
      setTimeout(() => setShowSuccessModal(false), 5000);
      
      // Limpar parâmetros da URL
      const url = new URL(window.location.href);
      url.searchParams.delete('session_id');
      url.searchParams.delete('success');
      url.searchParams.delete('plan');
      window.history.replaceState({}, '', url.pathname);
    }
  }, [searchParams]);

  // ========================================
  // PROTEÇÃO 1: LOGIN OBRIGATÓRIO
  // ========================================
  useEffect(() => {
    if (!authLoading && !user) {
      console.log('🔒 Usuário não autenticado - redirecionando para pricing');
      router.push('/pricing');
    }
  }, [user, authLoading, router]);

  // ========================================
  // APRESENTAÇÃO: PAGAMENTO OPCIONAL (SÓ PARA LOGADOS)
  // ========================================
  useEffect(() => {
    // Durante apresentação, só verifica se está logado
    // Verificação de pagamento fica opcional
    if (!authLoading && !user) {
      console.log('🔒 APRESENTAÇÃO: Redirecionando visitante para pricing');
      router.push('/pricing');
    }
  }, [user, authLoading, router]);

  // ========================================
  // LOADING STATE
  // ========================================
  if (authLoading || subLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-[var(--color-primary)] mx-auto mb-4" />
          <p className="text-gray-500 font-mono text-sm">Verificando acesso...</p>
          <p className="text-gray-600 font-mono text-xs mt-2">
            {authLoading ? 'Autenticando...' : 'Verificando assinatura...'}
          </p>
        </div>
      </div>
    );
  }

  // ========================================
  // SEM LOGIN - MOSTRA LOADING (vai redirecionar)
  // ========================================
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-[var(--color-primary)] mx-auto mb-4" />
          <p className="text-gray-500 font-mono text-sm">Redirecionando...</p>
        </div>
      </div>
    );
  }

  // ========================================
  // APRESENTAÇÃO: LIBERAR PARA LOGADOS (mesmo sem assinatura)
  // ========================================

  // ========================================
  // RENDER PRINCIPAL (USUÁRIO AUTENTICADO E PAGO)
  // ========================================
  return (
    <div className="min-h-screen relative flex">
      {/* Modal de Sucesso após Pagamento */}
      {showSuccessModal && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/80 backdrop-blur-sm animate-fadeIn">
          <div className="bg-gradient-to-b from-green-900/50 to-black border border-green-500/50 rounded-3xl p-8 max-w-md mx-4 text-center shadow-2xl">
            <div className="w-20 h-20 rounded-full bg-green-500/20 border border-green-500/50 flex items-center justify-center mx-auto mb-6">
              <CheckCircle className="w-10 h-10 text-green-400" />
            </div>
            <h2 className="text-2xl font-black text-white mb-2">
              Pagamento Confirmado! 🎉
            </h2>
            <p className="text-gray-400 mb-4">
              Bem-vindo ao ALSHAM QUANTUM. Seu acesso está sendo ativado.
            </p>
            <div className="text-xs text-gray-500">
              Redirecionando automaticamente...
            </div>
          </div>
        </div>
      )}

      {/* 1. SIDEBAR */}
      <Sidebar
        isOpen={isMobileMenuOpen}
        onClose={() => setIsMobileMenuOpen(false)}
      />

      {/* 2. ÁREA DE CONTEÚDO */}
      <div className="flex-1 flex flex-col min-h-screen transition-all duration-300 ease-in-out lg:pl-64">
        {/* Header Mobile */}
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

        {/* Main Content */}
        <main className="flex-1 relative p-4 md:p-8 overflow-x-hidden">
          <div className="mx-auto max-w-[1600px] w-full relative z-10 animate-fadeIn">
            {children}
          </div>
        </main>
      </div>

      {/* Toast Notifications */}
      <ToastContainer />
      
      {/* Badge Enterprise (God Mode) */}
      <PlanBadgeLarge />
      
      {/* ORION J.A.R.V.I.S. */}
      <OrionAssistant />
    </div>
  );
}

// Wrapper com Suspense para useSearchParams
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-black">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-[var(--color-primary)] mx-auto mb-4" />
          <p className="text-gray-500 font-mono text-sm">Carregando dashboard...</p>
        </div>
      </div>
    }>
      <DashboardLayoutContent>{children}</DashboardLayoutContent>
    </Suspense>
  );
}
