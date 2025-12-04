/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - REQUESTS QUEUE COMPONENT
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/RequestsQueue.tsx
 * 📊 Visualiza fila de requests em tempo real
 * 🔄 Auto-refresh a cada 5 segundos
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useState, useEffect } from 'react';
import {
  Clock,
  CheckCircle,
  XCircle,
  Loader2,
  AlertCircle,
  ChevronRight,
  Zap
} from 'lucide-react';

interface Request {
  id: string;
  title: string;
  description: string | null;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  priority: 'low' | 'normal' | 'high' | 'urgent';
  created_at: string;
  updated_at: string;
}

interface RequestsQueueProps {
  refreshTrigger?: number;
}

export default function RequestsQueue({ refreshTrigger = 0 }: RequestsQueueProps) {
  const [requests, setRequests] = useState<Request[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRequests = async () => {
    try {
      const response = await fetch('/api/requests/create');
      if (!response.ok) {
        throw new Error('Erro ao buscar requests');
      }
      const data = await response.json();
      setRequests(data.requests || []);
      setError(null);
    } catch (err: any) {
      console.error('Erro ao buscar requests:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch inicial
  useEffect(() => {
    fetchRequests();
  }, [refreshTrigger]);

  // Auto-refresh a cada 5 segundos
  useEffect(() => {
    const interval = setInterval(() => {
      fetchRequests();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'queued':
        return <Clock className="w-4 h-4 text-yellow-400" />;
      case 'processing':
        return <Loader2 className="w-4 h-4 text-blue-400 animate-spin" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'failed':
        return <XCircle className="w-4 h-4 text-red-400" />;
      default:
        return <AlertCircle className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'queued':
        return 'Na Fila';
      case 'processing':
        return 'Processando';
      case 'completed':
        return 'Completa';
      case 'failed':
        return 'Falhou';
      default:
        return status;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'queued':
        return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
      case 'processing':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
      case 'completed':
        return 'bg-green-500/10 text-green-400 border-green-500/20';
      case 'failed':
        return 'bg-red-500/10 text-red-400 border-red-500/20';
      default:
        return 'bg-gray-500/10 text-gray-400 border-gray-500/20';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'high':
        return 'bg-orange-500/20 text-orange-400 border-orange-500/30';
      case 'normal':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'low':
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'Agora';
    if (diffMins < 60) return `${diffMins}m atrás`;

    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h atrás`;

    const diffDays = Math.floor(diffHours / 24);
    return `${diffDays}d atrás`;
  };

  const queuedRequests = requests.filter(r => r.status === 'queued');
  const processingRequests = requests.filter(r => r.status === 'processing');
  const completedRequests = requests.filter(r => r.status === 'completed').slice(0, 5);
  const failedRequests = requests.filter(r => r.status === 'failed').slice(0, 3);

  if (loading && requests.length === 0) {
    return (
      <div className="rounded-3xl border border-[var(--color-border)]/20 bg-[var(--color-surface)]/20 backdrop-blur-md p-6">
        <div className="flex items-center justify-center h-40">
          <Loader2 className="w-8 h-8 text-[var(--color-primary)] animate-spin" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-3xl border border-red-500/20 bg-red-500/10 backdrop-blur-md p-6">
        <div className="flex items-center gap-3 text-red-400">
          <AlertCircle className="w-5 h-5" />
          <span>Erro ao carregar requests: {error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="rounded-xl border border-yellow-500/20 bg-yellow-500/5 p-4">
          <div className="flex items-center gap-2 text-yellow-400 mb-1">
            <Clock className="w-4 h-4" />
            <span className="text-xs font-mono">NA FILA</span>
          </div>
          <div className="text-2xl font-bold text-white">{queuedRequests.length}</div>
        </div>

        <div className="rounded-xl border border-blue-500/20 bg-blue-500/5 p-4">
          <div className="flex items-center gap-2 text-blue-400 mb-1">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span className="text-xs font-mono">PROCESSANDO</span>
          </div>
          <div className="text-2xl font-bold text-white">{processingRequests.length}</div>
        </div>

        <div className="rounded-xl border border-green-500/20 bg-green-500/5 p-4">
          <div className="flex items-center gap-2 text-green-400 mb-1">
            <CheckCircle className="w-4 h-4" />
            <span className="text-xs font-mono">COMPLETAS</span>
          </div>
          <div className="text-2xl font-bold text-white">{completedRequests.length}</div>
        </div>

        <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4">
          <div className="flex items-center gap-2 text-red-400 mb-1">
            <XCircle className="w-4 h-4" />
            <span className="text-xs font-mono">FALHARAM</span>
          </div>
          <div className="text-2xl font-bold text-white">{failedRequests.length}</div>
        </div>
      </div>

      {/* Queued Requests */}
      {queuedRequests.length > 0 && (
        <div className="rounded-3xl border border-[var(--color-border)]/20 bg-[var(--color-surface)]/20 backdrop-blur-md p-6">
          <h3 className="flex items-center gap-2 text-lg font-bold text-[var(--color-text)] mb-4">
            <Clock className="w-5 h-5 text-yellow-400" />
            Requests na Fila ({queuedRequests.length})
          </h3>
          <div className="space-y-3">
            {queuedRequests.map((request) => (
              <div
                key={request.id}
                className="flex items-start justify-between p-4 rounded-xl border border-[var(--color-border)]/20 bg-black/10 hover:bg-black/20 transition-colors group"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`px-2 py-1 rounded text-xs font-mono border ${getPriorityColor(request.priority)}`}>
                      {request.priority.toUpperCase()}
                    </span>
                    <span className="text-xs text-[var(--color-text-secondary)] font-mono">
                      {formatDate(request.created_at)}
                    </span>
                  </div>
                  <h4 className="text-sm font-semibold text-[var(--color-text)] mb-1">
                    {request.title}
                  </h4>
                  {request.description && (
                    <p className="text-xs text-[var(--color-text-secondary)] line-clamp-2">
                      {request.description}
                    </p>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  {getStatusIcon(request.status)}
                  <ChevronRight className="w-4 h-4 text-[var(--color-text-secondary)] opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Processing Requests */}
      {processingRequests.length > 0 && (
        <div className="rounded-3xl border border-[var(--color-border)]/20 bg-[var(--color-surface)]/20 backdrop-blur-md p-6">
          <h3 className="flex items-center gap-2 text-lg font-bold text-[var(--color-text)] mb-4">
            <Zap className="w-5 h-5 text-blue-400" />
            Processando Agora ({processingRequests.length})
          </h3>
          <div className="space-y-3">
            {processingRequests.map((request) => (
              <div
                key={request.id}
                className="flex items-start justify-between p-4 rounded-xl border border-blue-500/20 bg-blue-500/5 animate-pulse"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`px-2 py-1 rounded text-xs font-mono border ${getPriorityColor(request.priority)}`}>
                      {request.priority.toUpperCase()}
                    </span>
                  </div>
                  <h4 className="text-sm font-semibold text-[var(--color-text)] mb-1">
                    {request.title}
                  </h4>
                </div>
                <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Completed Requests */}
      {completedRequests.length > 0 && (
        <div className="rounded-3xl border border-[var(--color-border)]/20 bg-[var(--color-surface)]/20 backdrop-blur-md p-6">
          <h3 className="flex items-center gap-2 text-lg font-bold text-[var(--color-text)] mb-4">
            <CheckCircle className="w-5 h-5 text-green-400" />
            Últimas Completas
          </h3>
          <div className="space-y-2">
            {completedRequests.map((request) => (
              <div
                key={request.id}
                className="flex items-center justify-between p-3 rounded-xl border border-[var(--color-border)]/10 bg-black/5 hover:bg-black/10 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  <span className="text-sm text-[var(--color-text)]">{request.title}</span>
                </div>
                <span className="text-xs text-[var(--color-text-secondary)] font-mono">
                  {formatDate(request.updated_at)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {requests.length === 0 && (
        <div className="rounded-3xl border border-dashed border-[var(--color-border)]/20 bg-[var(--color-surface)]/10 backdrop-blur-md p-12">
          <div className="text-center">
            <Clock className="w-12 h-12 text-[var(--color-text-secondary)] mx-auto mb-4 opacity-50" />
            <h3 className="text-lg font-semibold text-[var(--color-text)] mb-2">
              Nenhuma request encontrada
            </h3>
            <p className="text-sm text-[var(--color-text-secondary)]">
              Crie sua primeira request usando o formulário acima!
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
