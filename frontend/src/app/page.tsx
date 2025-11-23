import Link from "next/link";
import ParticleField from "@/components/quantum/ParticleField";
import { Button } from "@/components/ui/button";
import { Activity, ShieldCheck, Zap } from "lucide-react";

export default function Home() {
  return (
    <main className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden font-sans">
      <ParticleField />
      <div className="z-10 flex flex-col items-center text-center px-4 animate-in fade-in zoom-in duration-1000">
        
        {/* Status Badge - Usando variáveis do tema */}
        <div 
          className="mb-6 inline-flex items-center rounded-full px-3 py-1 text-xs font-medium backdrop-blur-md"
          style={{
            border: '1px solid var(--accent-subtle)',
            background: 'var(--accent-subtle)',
            color: 'var(--accent)',
          }}
        >
          <span className="mr-2 flex h-1.5 w-1.5 relative">
            <span 
              className="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"
              style={{ background: 'var(--accent)' }}
            />
            <span 
              className="relative inline-flex rounded-full h-1.5 w-1.5"
              style={{ background: 'var(--accent)' }}
            />
          </span>
          SISTEMA ONLINE • v13.3 REALITY CODEX
        </div>

        {/* Title - Usando variáveis do tema */}
        <h1 
          className="text-5xl md:text-8xl font-bold tracking-tighter mb-6"
          style={{ 
            color: 'var(--text-primary)',
            textShadow: 'var(--glow-text)',
            fontFamily: 'var(--font-display)',
          }}
        >
          ALSHAM{' '}
          <span 
            className="text-transparent bg-clip-text"
            style={{
              backgroundImage: 'linear-gradient(to right, var(--accent), var(--accent-hover))',
              WebkitBackgroundClip: 'text',
            }}
          >
            QUANTUM
          </span>
        </h1>

        {/* Description */}
        <p 
          className="max-w-[600px] text-lg mb-8 leading-relaxed"
          style={{ color: 'var(--text-muted)' }}
        >
          O Primeiro Organismo Digital Auto-Evolutivo.
          <br/>
          <span style={{ color: 'var(--text-primary)' }}>
            139 Agentes Reais. 21 Páginas. ROI de 2.847%.
          </span>
        </p>

        {/* Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          <Link href="/dashboard">
            <Button 
              className="text-lg px-8 py-6 font-bold transition-all hover:scale-105"
              style={{
                background: 'var(--accent)',
                color: 'var(--text-inverse)',
                boxShadow: 'var(--glow)',
              }}
            >
              ACESSAR COCKPIT
            </Button>
          </Link>
          <Button 
            variant="outline" 
            className="text-lg px-8 py-6 backdrop-blur-sm"
            style={{
              border: '1px solid var(--border)',
              color: 'var(--text-secondary)',
              background: 'var(--bg-panel)',
            }}
          >
            DOCUMENTAÇÃO
          </Button>
        </div>

        {/* Stats Grid */}
        <div 
          className="mt-16 grid grid-cols-3 gap-8 text-sm p-6 rounded-xl w-full max-w-2xl"
          style={{
            background: 'var(--card-bg)',
            border: '1px solid var(--card-border)',
            backdropFilter: 'var(--backdrop-blur)',
          }}
        >
          <div className="flex flex-col items-center gap-2">
            <Activity className="h-5 w-5" style={{ color: 'var(--success)' }} />
            <span 
              className="font-mono font-bold"
              style={{ color: 'var(--text-primary)' }}
            >
              R$ 4.7B
            </span>
            <span style={{ color: 'var(--text-muted)' }}>ECONOMIA</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <Zap className="h-5 w-5" style={{ color: 'var(--accent)' }} />
            <span 
              className="font-mono font-bold"
              style={{ color: 'var(--text-primary)' }}
            >
              99.98%
            </span>
            <span style={{ color: 'var(--text-muted)' }}>UPTIME</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <ShieldCheck className="h-5 w-5" style={{ color: 'var(--accent-hover)' }} />
            <span 
              className="font-mono font-bold"
              style={{ color: 'var(--text-primary)' }}
            >
              139
            </span>
            <span style={{ color: 'var(--text-muted)' }}>AGENTES</span>
          </div>
        </div>
      </div>
    </main>
  );
}
