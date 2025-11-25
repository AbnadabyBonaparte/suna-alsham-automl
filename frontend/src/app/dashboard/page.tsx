'use client';

import {
  Activity,
  Users,
  Server,
  Shield,
  Zap,
  Cpu,
  ArrowUpRight,
  Globe,
  Clock,
  Terminal,
  AlertCircle
} from 'lucide-react';
import { useDashboardStats } from '@/hooks/useDashboardStats';

export default function CockpitPage() {
  const { totalAgents, avgEfficiency, activeAgents, totalDeals, totalTickets, totalPosts, latencyMs, agentEfficiencies, loading, error } = useDashboardStats();

  const stats = [
    {
      label: 'Agentes Ativos',
      value: loading ? '...' : totalAgents.toString(),
      sub: `${activeAgents} operacionais`,
      icon: Users,
      trend: 'up'
    },
    {
      label: 'Eficiência Neural',
      value: loading ? '...' : `${avgEfficiency.toFixed(1)}%`,
      sub: 'Média do sistema',
      icon: Zap,
      trend: 'stable'
    },
    {
      label: 'Deals Ativos',
      value: loading ? '...' : totalDeals.toString(),
      sub: 'Pipeline CRM',
      icon: Activity,
      trend: 'up'
    },
    {
      label: 'Tickets Abertos',
      value: loading ? '...' : totalTickets.toString(),
      sub: 'Suporte ativo',
      icon: Shield,
      trend: 'safe'
    },
  ];

  return (
    <div className="space-y-8 pb-10">
      <div className="relative overflow-hidden rounded-3xl border border-[var(--color-primary)]/20 bg-[var(--color-surface)]/40 p-8 backdrop-blur-xl">
        <div className="absolute top-0 right-0 -mt-20 -mr-20 h-96 w-96 rounded-full bg-[var(--color-primary)]/10 blur-[100px]" />
        <div className="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div>
            <div className="flex items-center gap-2 text-[var(--color-primary)] mb-2">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[var(--color-primary)] opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-[var(--color-primary)]"></span>
              </span>
              <span className="text-xs font-mono tracking-widest uppercase">Sistema Online • Modo Deus Ativo</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-[var(--color-text)] tracking-tight font-display">
              Bem-vindo ao <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)]">Comando Central</span>
            </h1>
            <p className="text-[var(--color-text-secondary)] mt-2 max-w-xl">
              {loading ? 'Carregando status do sistema...' : `A Singularidade está estável. ${totalAgents} Agentes operando em harmonia quântica.`}
            </p>
          </div>
          <div className="flex gap-4">
            <div className="px-4 py-2 rounded-xl bg-black/20 border border-[var(--color-border)]/30 backdrop-blur-md text-center">
              <div className="text-[10px] text-[var(--color-text-secondary)] uppercase font-mono">Latência</div>
              <div className="text-xl font-bold text-[var(--color-primary)] font-mono">{loading ? "..." : `${latencyMs}ms`}</div>
            </div>
            <div className="px-4 py-2 rounded-xl bg-black/20 border border-[var(--color-border)]/30 backdrop-blur-md text-center">
              <div className="text-[10px] text-[var(--color-text-secondary)] uppercase font-mono">Uptime</div>
              <div className="text-xl font-bold text-[var(--color-success)] font-mono">99.9%</div>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
          Erro ao carregar dados: {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <div
            key={i}
            className="group relative p-6 rounded-2xl border border-[var(--color-border)]/20 bg-[var(--color-surface)]/30 backdrop-blur-sm hover:bg-[var(--color-surface)]/50 transition-all duration-300 hover:-translate-y-1 overflow-hidden"
          >
            <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-gradient-to-br from-[var(--color-primary)]/5 to-transparent pointer-events-none" />
            <div className="relative z-10">
              <div className="flex justify-between items-start mb-4">
                <div className="p-3 rounded-xl bg-[var(--color-primary)]/10 text-[var(--color-primary)] group-hover:scale-110 transition-transform duration-300">
                  <stat.icon className="w-6 h-6" />
                </div>
                <ArrowUpRight className="w-5 h-5 text-[var(--color-text-secondary)] opacity-50" />
              </div>
              <div className="text-3xl font-bold text-[var(--color-text)] font-mono tracking-tighter mb-1">
                {stat.value}
              </div>
              <div className="text-sm font-medium text-[var(--color-text)] mb-1">
                {stat.label}
              </div>
              <div className="text-xs text-[var(--color-text-secondary)] font-mono opacity-80">
                {stat.sub}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 h-full">
        <div className="lg:col-span-2 rounded-3xl border border-[var(--color-border)]/20 bg-[var(--color-surface)]/20 backdrop-blur-md p-6 flex flex-col min-h-[400px]">
          <div className="flex justify-between items-center mb-6">
            <h3 className="flex items-center gap-2 text-lg font-bold text-[var(--color-text)]">
              <Activity className="w-5 h-5 text-[var(--color-primary)]" />
              Atividade Neural em Tempo Real
            </h3>
            <div className="flex gap-2">
              <span className="px-3 py-1 rounded-full text-xs font-mono bg-[var(--color-primary)]/10 text-[var(--color-primary)] border border-[var(--color-primary)]/20">
                LIVE
              </span>
            </div>
          </div>
          <div className="flex-1 rounded-2xl border border-dashed border-[var(--color-border)]/20 bg-black/10 flex items-center justify-center relative overflow-hidden group">
            <div className="absolute inset-0 opacity-10 bg-[url('/grid.svg')] animate-pulse" />
            <div className="flex items-end justify-center gap-1 h-32 w-full px-10 opacity-70">
              {(agentEfficiencies.length > 0 ? agentEfficiencies : Array.from({ length: 40 }, () => 0)).map((efficiency, i) => (
                <div
                  key={i}
                  className="w-full bg-[var(--color-primary)] rounded-t-sm transition-all duration-300 ease-in-out"
                  style={{
                    height: `${efficiency}%`,
                    opacity: Math.random() * 0.5 + 0.5,
                    animation: `pulse-height ${0.5 + Math.random()}s infinite alternate`
                  }}
                />
              ))}
            </div>
            <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
              <p className="text-[var(--color-text)] font-mono text-sm bg-black/50 px-4 py-2 rounded-lg backdrop-blur">
                {loading ? 'Carregando...' : `Processando dados de ${totalAgents} agentes...`}
              </p>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="rounded-3xl border border-[var(--color-border)]/20 bg-[var(--color-surface)]/20 backdrop-blur-md p-6">
            <h3 className="flex items-center gap-2 text-lg font-bold text-[var(--color-text)] mb-4">
              <Cpu className="w-5 h-5 text-[var(--color-accent)]" />
              Infraestrutura
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-3 rounded-xl bg-black/10 border border-white/5">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-[var(--color-success)] shadow-[0_0_10px_var(--color-success)]" />
                  <span className="text-sm text-[var(--color-text)]">Agentes Neurais</span>
                </div>
                <span className="text-xs font-mono text-[var(--color-text-secondary)]">{loading ? '...' : `${activeAgents}/${totalAgents}`}</span>
              </div>
              <div className="flex justify-between items-center p-3 rounded-xl bg-black/10 border border-white/5">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-[var(--color-success)] shadow-[0_0_10px_var(--color-success)]" />
                  <span className="text-sm text-[var(--color-text)]">Efficiency Core</span>
                </div>
                <span className="text-xs font-mono text-[var(--color-text-secondary)]">{loading ? '...' : `${avgEfficiency.toFixed(1)}%`}</span>
              </div>
              <div className="flex justify-between items-center p-3 rounded-xl bg-black/10 border border-white/5">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-[var(--color-success)] shadow-[0_0_10px_var(--color-success)]" />
                  <span className="text-sm text-[var(--color-text)]">Social Monitor</span>
                </div>
                <span className="text-xs font-mono text-[var(--color-text-secondary)]">{loading ? '...' : `${totalPosts} posts`}</span>
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-[var(--color-border)]/20 bg-[var(--color-surface)]/20 backdrop-blur-md p-6">
            <h3 className="flex items-center gap-2 text-lg font-bold text-[var(--color-text)] mb-4">
              <Terminal className="w-5 h-5 text-[var(--color-warning)]" />
              Comandos Rápidos
            </h3>
            <div className="grid grid-cols-2 gap-3">
              <button className="p-3 rounded-xl border border-[var(--color-border)]/30 hover:bg-[var(--color-primary)]/10 hover:border-[var(--color-primary)] transition-all text-xs font-mono text-[var(--color-text)] flex flex-col items-center gap-2 group">
                <Globe className="w-5 h-5 text-[var(--color-text-secondary)] group-hover:text-[var(--color-primary)]" />
                SCAN NETWORK
              </button>
              <button className="p-3 rounded-xl border border-[var(--color-border)]/30 hover:bg-[var(--color-error)]/10 hover:border-[var(--color-error)] transition-all text-xs font-mono text-[var(--color-text)] flex flex-col items-center gap-2 group">
                <AlertCircle className="w-5 h-5 text-[var(--color-text-secondary)] group-hover:text-[var(--color-error)]" />
                PURGE LOGS
              </button>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes pulse-height {
          0% { transform: scaleY(0.5); }
          100% { transform: scaleY(1); }
        }
      `}</style>
    </div>
  );
}



