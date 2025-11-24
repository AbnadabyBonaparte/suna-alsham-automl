"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Activity, ShieldCheck, Zap } from "lucide-react";

export default function Home() {
  return (
    <main className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden font-sans">
      {/* Background agora vem do RealityBackground no layout.tsx */}
      
      <div className="z-10 flex flex-col items-center text-center px-4 animate-in fade-in zoom-in duration-1000">
        
        {/* Badge de Status */}
        <div 
          className="mb-6 inline-flex items-center rounded-full px-4 py-1.5 text-xs font-medium backdrop-blur-md border"
          style={{
            borderColor: 'var(--color-primary)',
            backgroundColor: 'rgba(0, 0, 0, 0.3)',
            color: 'var(--color-primary)',
          }}
        >
          <span className="mr-2 flex h-1.5 w-1.5 relative">
            <span 
              className="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"
              style={{ backgroundColor: 'var(--color-primary)' }}
            />
            <span 
              className="relative inline-flex rounded-full h-1.5 w-1.5"
              style={{ backgroundColor: 'var(--color-primary)' }}
            />
          </span>
          SISTEMA ONLINE • v13.3 REALITY CODEX
        </div>

        {/* Título Principal */}
        <h1 
          className="text-5xl md:text-8xl font-bold tracking-tighter mb-6"
          style={{ 
            color: 'var(--color-text)',
            textShadow: '0 0 40px var(--color-glow)',
          }}
        >
          ALSHAM{' '}
          <span 
            style={{
              color: 'var(--color-primary)',
              textShadow: '0 0 60px var(--color-primary)',
            }}
          >
            QUANTUM
          </span>
        </h1>

        {/* Subtítulo */}
        <p 
          className="max-w-[600px] text-lg mb-8 leading-relaxed"
          style={{ color: 'var(--color-textSecondary)' }}
        >
          O Primeiro Organismo Digital Auto-Evolutivo.
          <br/>
          <span style={{ color: 'var(--color-text)', fontWeight: 600 }}>
            139 Agentes Reais. 21 Páginas. ROI de 2.847%.
          </span>
        </p>

        {/* Botões de Ação - COM NAVEGAÇÃO FORÇADA */}
        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={() => {
              console.log('🚀 Navegando para /dashboard');
              window.location.href = '/dashboard';
            }}
            className="text-lg px-8 py-6 font-bold transition-all hover:scale-105 rounded-lg cursor-pointer"
            style={{
              backgroundColor: 'var(--color-primary)',
              color: '#FFFFFF',
              boxShadow: '0 0 30px var(--color-glow)',
              border: 'none',
            }}
          >
            ACESSAR COCKPIT
          </button>
          
          <button
            onClick={() => {
              console.log('📖 Abrindo documentação');
              // Implementar depois
            }}
            className="text-lg px-8 py-6 backdrop-blur-sm transition-all hover:scale-105 rounded-lg cursor-pointer"
            style={{
              borderWidth: '1px',
              borderStyle: 'solid',
              borderColor: 'var(--color-border)',
              color: 'var(--color-text)',
              backgroundColor: 'var(--color-surface)',
            }}
          >
            DOCUMENTAÇÃO
          </button>
        </div>

        {/* Cards de Estatísticas */}
        <div 
          className="mt-16 grid grid-cols-3 gap-8 text-sm p-6 rounded-xl w-full max-w-2xl backdrop-blur-xl"
          style={{
            backgroundColor: 'var(--color-surface)',
            borderWidth: '1px',
            borderStyle: 'solid',
            borderColor: 'var(--color-border)',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
          }}
        >
          <div className="flex flex-col items-center gap-2">
            <Activity 
              className="h-5 w-5" 
              style={{ color: 'var(--color-success)' }} 
            />
            <span 
              className="font-mono font-bold text-xl" 
              style={{ color: 'var(--color-text)' }}
            >
              R$ 4.7B
            </span>
            <span 
              className="text-xs" 
              style={{ color: 'var(--color-textSecondary)' }}
            >
              ECONOMIA
            </span>
          </div>

          <div className="flex flex-col items-center gap-2">
            <Zap 
              className="h-5 w-5" 
              style={{ color: 'var(--color-primary)' }} 
            />
            <span 
              className="font-mono font-bold text-xl" 
              style={{ color: 'var(--color-text)' }}
            >
              99.98%
            </span>
            <span 
              className="text-xs" 
              style={{ color: 'var(--color-textSecondary)' }}
            >
              UPTIME
            </span>
          </div>

          <div className="flex flex-col items-center gap-2">
            <ShieldCheck 
              className="h-5 w-5" 
              style={{ color: 'var(--color-accent)' }} 
            />
            <span 
              className="font-mono font-bold text-xl" 
              style={{ color: 'var(--color-text)' }}
            >
              139
            </span>
            <span 
              className="text-xs" 
              style={{ color: 'var(--color-textSecondary)' }}
            >
              AGENTES
            </span>
          </div>
        </div>
      </div>
    </main>
  );
}
