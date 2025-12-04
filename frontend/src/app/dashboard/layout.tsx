/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - DASHBOARD LAYOUT RESPONSIVO + PROTEGIDO
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/layout.tsx
 * 📋 Estrutura: Sidebar fixa + Conteúdo à direita + Auth Guard + ORION
 * ═══════════════════════════════════════════════════════════════
 */
'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import Sidebar from '@/components/layout/Sidebar';
import OrionAssistant from '@/components/orion/OrionAssistant';
import { ToastContainer } from '@/components/ui/ToastContainer';
import { Menu, Sparkles, Loader2 } from 'lucide-react';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { user, loading } = useAuth();
  const router = useRouter();

  // PROTEÇÃO: Redireciona para login se não estiver autenticado
  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  // Loading state enquanto verifica auth
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-[var(--color-primary)] mx-auto mb-4" />
          <p className="text-gray-500 font-mono text-sm">Verificando acesso...</p>
        </div>
      </div>
    );
  }

  // Se não estiver logado, não renderiza nada (vai redirecionar)
  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen relative flex">
      {/* 1. SIDEBAR (Controlada por estado no mobile, sempre visível no desktop) */}
      <Sidebar
        isOpen={isMobileMenuOpen}
        onClose={() => setIsMobileMenuOpen(false)}
      />

      {/* 2. ÁREA DE CONTEÚDO */}
      {/* lg:pl-64 é a chave: empurra o conteúdo 256px para a direita em telas grandes */}
      <div className="flex-1 flex flex-col min-h-screen transition-all duration-300 ease-in-out lg:pl-64">
        {/* Header Mobile (Só aparece em telas pequenas - lg:hidden) */}
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
        </header>

        {/* Main Content Scrollable */}
        <main className="flex-1 relative p-4 md:p-8 overflow-x-hidden">
          {/* Container centralizado para telas ultra-wide */}
          {/* z-10 garante que o texto fique acima do background de partículas */}
          <div className="mx-auto max-w-[1600px] w-full relative z-10 animate-fadeIn">
            {children}
          </div>
        </main>
      </div>

      {/* Global Toast Notifications */}
      <ToastContainer />
      
      {/* ORION J.A.R.V.I.S. - Assistente Global */}
      <OrionAssistant />
    </div>
  );
}
