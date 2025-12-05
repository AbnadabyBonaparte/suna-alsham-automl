'use client';

import { useState } from 'react';
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
  AlertCircle,
  X,
  CheckCircle,
  Send,
  Sparkles
} from 'lucide-react';
import { useDashboardStats } from '@/hooks/useDashboardStats';
import { useNotificationStore } from '@/stores';
import RequestsQueue from '@/components/RequestsQueue';

interface ConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
  confirmText: string;
  isDestructive?: boolean;
}

function ConfirmModal({ isOpen, onClose, onConfirm, title, message, confirmText, isDestructive }: ConfirmModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-md bg-[var(--color-surface)]/95 backdrop-blur-xl border border-[var(--color-border)]/30 rounded-3xl p-8 shadow-2xl">
        <button
          onClick={onClose}
          className="absolute top-6 right-6 text-gray-400 hover:text-white transition-colors"
        >
          <X className="w-6 h-6" />
        </button>

        <div className="mb-6">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center mb-4" style={{ background: isDestructive ? 'var(--color-error)/10' : 'var(--color-primary)/10', color: isDestructive ? 'var(--color-error)' : 'var(--color-primary)' }}>
            {isDestructive ? <AlertCircle className="w-6 h-6" /> : <Globe className="w-6 h-6" />}
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">{title}</h2>
          <p className="text-gray-400 leading-relaxed">{message}</p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white py-3 px-6 transition-all font-bold"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              onConfirm();
              onClose();
            }}
            className="flex-1 text-black font-bold py-3 px-6 rounded-xl transition-all"
            style={{ background: isDestructive ? 'var(--color-error)' : 'var(--color-primary)' }}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function CockpitPage() {
  const { totalAgents, avgEfficiency, activeAgents, totalDeals, totalTickets, totalPosts, latencyMs, agentEfficiencies, uptimePercent, loading, error } = useDashboardStats();
  const { addNotification } = useNotificationStore();

  const [scanModalOpen, setScanModalOpen] = useState(false);
  const [purgeModalOpen, setPurgeModalOpen] = useState(false);

  // Request Form State
  const [requestTitle, setRequestTitle] = useState('');
  const [requestDescription, setRequestDescription] = useState('');
  const [requestPriority, setRequestPriority] = useState<'low' | 'normal' | 'high' | 'urgent'>('normal');
  const [isSubmittingRequest, setIsSubmittingRequest] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

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

  const handleScanNetwork = () => {
    addNotification({
      type: 'info',
      title: 'Network Scan Initiated',
      message: 'Scanning all network nodes and quantum connections...',
    });

    // Simular scan
    setTimeout(() => {
      addNotification({
        type: 'success',
        title: 'Network Scan Complete',
        message: `All ${totalAgents} agents online. No anomalies detected.`,
      });
    }, 2000);
  };

  const handlePurgeLogs = () => {
    addNotification({
      type: 'warning',
      title: 'Purging System Logs',
      message: 'Cleaning old log entries from database...',
    });

    // Simular purge
    setTimeout(() => {
      addNotification({
        type: 'success',
        title: 'Logs Purged Successfully',
        message: 'System logs cleaned. Storage optimized.',
      });
    }, 1500);
  };

  const handleCreateRequest = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!requestTitle.trim()) {
      addNotification({
        type: 'error',
        title: 'Erro ao criar request',
        message: 'O título é obrigatório',
      });
      return;
    }

    setIsSubmittingRequest(true);

    try {
      const response = await fetch('/api/requests/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: requestTitle,
          description: requestDescription,
          priority: requestPriority,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Erro ao criar request');
      }

      addNotification({
        type: 'success',
        title: 'Request Criada!',
        message: 'Sua request será processada em breve...',
      });

      // Limpar formulário
      setRequestTitle('');
      setRequestDescription('');
      setRequestPriority('normal');

      // Trigger refresh da queue
      setRefreshTrigger(prev => prev + 1);

    } catch (error: any) {
      console.error('Erro ao criar request:', error);
      addNotification({
        type: 'error',
        title: 'Erro ao criar request',
        message: error.message || 'Tente novamente',
      });
    } finally {
      setIsSubmittingRequest(false);
    }
  };

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
            <div className="px-4 py-2 rounded-xl bg-black/20 border border-[var(--color-border)]/30 backdrop-blur-md text-center hover:scale-105 transition-transform">
              <div className="text-[10px] text-[var(--color-text-secondary)] uppercase font-mono">Latência</div>
              <div className="text-xl font-bold text-[var(--color-primary)] font-mono">{loading ? "..." : `${latencyMs}ms`}</div>
            </div>
            <div className="px-4 py-2 rounded-xl bg-black/20 border border-[var(--color-border)]/30 backdrop-blur-md text-center hover:scale-105 transition-transform">
              <div className="text-[10px] text-[var(--color-text-secondary)] uppercase font-mono">Uptime</div>
              <div className="text-xl font-bold text-[var(--color-success)] font-mono">{loading ? "..." : `${uptimePercent.toFixed(1)}%`}</div>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl text-sm" style={{ background: 'var(--color-error)/10', border: '1px solid var(--color-error)/20', color: 'var(--color-error)' }}>
          Erro ao carregar dados: {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <div
            key={i}
            className="group relative p-6 rounded-2xl border border-[var(--color-border)]/20 bg-[var(--color-surface)]/30 backdrop-blur-sm hover:bg-[var(--color-surface)]/50 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(var(--color-primary-rgb),0.15)] overflow-hidden cursor-pointer"
          >
            <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-gradient-to-br from-[var(--color-primary)]/5 to-transparent pointer-events-none" />
            <div className="relative z-10">
              <div className="flex justify-between items-start mb-4">
                <div className="p-3 rounded-xl bg-[var(--color-primary)]/10 text-[var(--color-primary)] group-hover:scale-110 transition-transform duration-300">
                  <stat.icon className="w-6 h-6" />
                </div>
                <ArrowUpRight className="w-5 h-5 text-[var(--color-text-secondary)] opacity-50 group-hover:opacity-100 transition-opacity" />
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
              <span className="px-3 py-1 rounded-full text-xs font-mono bg-[var(--color-primary)]/10 text-[var(--color-primary)] border border-[var(--color-primary)]/20 animate-pulse">
                LIVE
              </span>
            </div>
          </div>
          <div className="flex-1 rounded-2xl border border-dashed border-[var(--color-border)]/20 bg-black/10 flex items-center justify-center relative overflow-hidden group">
            <div className="absolute inset-0 opacity-10 bg-[url('/grid.svg')] animate-pulse" />
            <div className="flex items-end justify-center gap-1 h-32 w-full px-10 opacity-70">
              {(activeAgents > 0 && agentEfficiencies.length > 0 ? agentEfficiencies : Array.from({ length: 40 }, () => 5)).map((efficiency, i) => (
                <div
                  key={i}
                  className="w-full bg-[var(--color-primary)] rounded-t-sm transition-all duration-300 ease-in-out hover:opacity-100"
                  style={{
                    height: `${efficiency}%`,
                    opacity: Math.random() * 0.5 + 0.5,
                    animation: `pulse-height ${0.5 + Math.random()}s infinite alternate`
                  }}
                  title={`Agent ${i + 1}: ${efficiency}% efficiency`}
                />
              ))}
            </div>
            <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
              <p className="text-[var(--color-text)] font-mono text-sm bg-black/50 px-4 py-2 rounded-lg backdrop-blur">
                {loading ? 'Carregando...' : `Processando dados de ${totalAgents} agentes em tempo real`}
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
              <div className="flex justify-between items-center p-3 rounded-xl bg-black/10 border border-white/5 hover:bg-black/20 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-[var(--color-success)] shadow-[0_0_10px_var(--color-success)] animate-pulse" />
                  <span className="text-sm text-[var(--color-text)]">Agentes Neurais</span>
                </div>
                <span className="text-xs font-mono text-[var(--color-text-secondary)]">{loading ? '...' : `${activeAgents}/${totalAgents}`}</span>
              </div>
              <div className="flex justify-between items-center p-3 rounded-xl bg-black/10 border border-white/5 hover:bg-black/20 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-[var(--color-success)] shadow-[0_0_10px_var(--color-success)] animate-pulse" />
                  <span className="text-sm text-[var(--color-text)]">Efficiency Core</span>
                </div>
                <span className="text-xs font-mono text-[var(--color-text-secondary)]">{loading ? '...' : `${avgEfficiency.toFixed(1)}%`}</span>
              </div>
              <div className="flex justify-between items-center p-3 rounded-xl bg-black/10 border border-white/5 hover:bg-black/20 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-[var(--color-success)] shadow-[0_0_10px_var(--color-success)] animate-pulse" />
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
              <button
                onClick={() => setScanModalOpen(true)}
                className="p-3 rounded-xl border border-[var(--color-border)]/30 hover:bg-[var(--color-primary)]/10 hover:border-[var(--color-primary)] hover:scale-105 transition-all text-xs font-mono text-[var(--color-text)] flex flex-col items-center gap-2 group"
              >
                <Globe className="w-5 h-5 text-[var(--color-text-secondary)] group-hover:text-[var(--color-primary)]" />
                SCAN NETWORK
              </button>
              <button
                onClick={() => setPurgeModalOpen(true)}
                className="p-3 rounded-xl border border-[var(--color-border)]/30 hover:bg-[var(--color-error)]/10 hover:border-[var(--color-error)] hover:scale-105 transition-all text-xs font-mono text-[var(--color-text)] flex flex-col items-center gap-2 group"
              >
                <AlertCircle className="w-5 h-5 text-[var(--color-text-secondary)] group-hover:text-[var(--color-error)]" />
                PURGE LOGS
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Request Creation & Queue Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Create Request Form */}
        <div className="lg:col-span-1 rounded-3xl border border-[var(--color-border)]/20 bg-[var(--color-surface)]/20 backdrop-blur-md p-6">
          <h3 className="flex items-center gap-2 text-lg font-bold text-[var(--color-text)] mb-4">
            <Sparkles className="w-5 h-5 text-[var(--color-primary)]" />
            Nova Request
          </h3>
          <form onSubmit={handleCreateRequest} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-[var(--color-text)] mb-2">
                Título *
              </label>
              <input
                type="text"
                value={requestTitle}
                onChange={(e) => setRequestTitle(e.target.value)}
                placeholder="Ex: Analisar dados de vendas"
                className="w-full px-4 py-3 rounded-xl bg-black/20 border border-[var(--color-border)]/30 text-[var(--color-text)] placeholder-gray-500 focus:outline-none focus:border-[var(--color-primary)] transition-colors"
                disabled={isSubmittingRequest}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-[var(--color-text)] mb-2">
                Descrição
              </label>
              <textarea
                value={requestDescription}
                onChange={(e) => setRequestDescription(e.target.value)}
                placeholder="Descreva o que você precisa..."
                rows={4}
                className="w-full px-4 py-3 rounded-xl bg-black/20 border border-[var(--color-border)]/30 text-[var(--color-text)] placeholder-gray-500 focus:outline-none focus:border-[var(--color-primary)] transition-colors resize-none"
                disabled={isSubmittingRequest}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-[var(--color-text)] mb-2">
                Prioridade
              </label>
              <select
                value={requestPriority}
                onChange={(e) => setRequestPriority(e.target.value as any)}
                className="w-full px-4 py-3 rounded-xl bg-black/20 border border-[var(--color-border)]/30 text-[var(--color-text)] focus:outline-none focus:border-[var(--color-primary)] transition-colors cursor-pointer"
                disabled={isSubmittingRequest}
              >
                <option value="low">Baixa</option>
                <option value="normal">Normal</option>
                <option value="high">Alta</option>
                <option value="urgent">Urgente</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={isSubmittingRequest || !requestTitle.trim()}
              className="w-full bg-[var(--color-primary)] hover:bg-[var(--color-primary)]/80 disabled:bg-gray-600 disabled:cursor-not-allowed text-black font-bold py-3 px-6 rounded-xl transition-all flex items-center justify-center gap-2"
            >
              {isSubmittingRequest ? (
                <>
                  <Sparkles className="w-5 h-5 animate-spin" />
                  Criando...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  Criar Request
                </>
              )}
            </button>
          </form>
        </div>

        {/* Requests Queue */}
        <div className="lg:col-span-2">
          <RequestsQueue refreshTrigger={refreshTrigger} />
        </div>
      </div>

      {/* Modals */}
      <ConfirmModal
        isOpen={scanModalOpen}
        onClose={() => setScanModalOpen(false)}
        onConfirm={handleScanNetwork}
        title="Scan Network"
        message={`Initiate a complete network scan across all ${totalAgents} quantum nodes? This will verify connectivity and check for anomalies.`}
        confirmText="Start Scan"
      />

      <ConfirmModal
        isOpen={purgeModalOpen}
        onClose={() => setPurgeModalOpen(false)}
        onConfirm={handlePurgeLogs}
        title="Purge System Logs"
        message="This will permanently delete old system logs to free up storage. This action cannot be undone."
        confirmText="Purge Now"
        isDestructive
      />

      <style jsx>{`
        @keyframes pulse-height {
          0% { transform: scaleY(0.5); }
          100% { transform: scaleY(1); }
        }
      `}</style>
    </div>
  );
}
