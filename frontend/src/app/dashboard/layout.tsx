/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - DASHBOARD LAYOUT
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/layout.tsx
 * 📋 Estrutura: Sidebar fixa à esquerda + Conteúdo à direita
 * ═══════════════════════════════════════════════════════════════
 */

import Sidebar from '@/components/layout/Sidebar';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* 1. A Sidebar fica fixa na esquerda */}
      <Sidebar />

      {/* 2. Área de Conteúdo Principal */}
      <main className="flex-1 relative flex flex-col overflow-hidden">
        
        {/* Scroll Area para o conteúdo */}
        <div className="flex-1 overflow-y-auto overflow-x-hidden p-6 md:p-8 scroll-smooth">
          {/* 
              z-10 é CRÍTICO aqui: garante que o texto fique ACIMA 
              do background animado (RealityBackground) 
          */}
          <div className="mx-auto max-w-7xl w-full relative z-10 animate-fadeIn">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}
