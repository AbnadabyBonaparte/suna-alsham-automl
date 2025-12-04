/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - AGENT AUTO-EVOLUTION LAB
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/evolution/page.tsx
 * 🧬 Sistema de Auto-Evolução de Agents usando Claude API
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect } from 'react';
import { useNotificationStore } from '@/stores/useNotificationStore';
import {
    Dna, Brain, TrendingDown, Zap, X, Check, AlertTriangle,
    Clock, Target, Activity, History, ChevronRight, Sparkles,
    RefreshCw, CheckCircle2, XCircle, ArrowRight
} from 'lucide-react';

interface AgentCandidate {
  agent_id: string;
  agent_name: string;
  agent_role: string;
  total_requests: number;
  successful_requests: number;
  failed_requests: number;
  success_rate: number;
  avg_processing_time_ms: number;
  current_efficiency: number;
  evolution_count: number;
  last_evolved_at: string | null;
  recommendation: 'urgent' | 'recommended' | 'stable';
  issues: string[];
}

interface Proposal {
  proposal_id: string;
  agent_id: string;
  agent_name: string;
  current_prompt: string;
  proposed_prompt: string;
  analysis: {
    weaknesses: string[];
    improvements: string[];
    expected_gain: string;
    confidence: 'high' | 'medium' | 'low';
    reasoning: string;
  };
}

interface EvolutionHistory {
  id: string;
  agent_id: string;
  status: 'pending' | 'approved' | 'rejected' | 'merged';
  created_at: string;
  analysis: any;
}

export default function EvolutionPage() {
    const { addNotification } = useNotificationStore();

    const [loading, setLoading] = useState(true);
    const [analyzing, setAnalyzing] = useState(false);
    const [candidates, setCandidates] = useState<AgentCandidate[]>([]);
    const [history, setHistory] = useState<EvolutionHistory[]>([]);

    // Modal de proposta
    const [showProposalModal, setShowProposalModal] = useState(false);
    const [currentProposal, setCurrentProposal] = useState<Proposal | null>(null);
    const [proposing, setProposing] = useState(false);
    const [applying, setApplying] = useState(false);

    // Tabs
    const [activeTab, setActiveTab] = useState<'candidates' | 'history'>('candidates');

    // 1. Carregar candidatos e histórico
    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            // Buscar candidatos
            const candidatesRes = await fetch('/api/evolution/analyze');
            const candidatesData = await candidatesRes.json();

            if (candidatesData.success) {
                setCandidates(candidatesData.candidates || []);
            }

            // Buscar histórico
            const historyRes = await fetch('/api/evolution/apply');
            const historyData = await historyRes.json();

            if (historyData.success) {
                setHistory(historyData.proposals || []);
            }
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
            addNotification('Erro ao carregar dados de evolução', 'error');
        } finally {
            setLoading(false);
        }
    };

    // 2. Analisar agent com Claude
    const handleAnalyzeAgent = async (agentId: string, agentName: string) => {
        setProposing(true);
        setAnalyzing(true);

        try {
            const res = await fetch('/api/evolution/propose', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ agent_id: agentId }),
            });

            const data = await res.json();

            if (data.success) {
                setCurrentProposal({
                    proposal_id: data.proposal_id,
                    agent_id: agentId,
                    agent_name: agentName,
                    current_prompt: data.current_prompt,
                    proposed_prompt: data.proposed_prompt,
                    analysis: data.analysis,
                });
                setShowProposalModal(true);
                addNotification(`Proposta de evolução gerada para ${agentName}!`, 'success');
            } else {
                addNotification(`Erro: ${data.error}`, 'error');
            }
        } catch (error) {
            console.error('Erro ao analisar agent:', error);
            addNotification('Erro ao analisar agent com Claude', 'error');
        } finally {
            setProposing(false);
            setAnalyzing(false);
        }
    };

    // 3. Aprovar ou rejeitar evolução
    const handleApplyEvolution = async (action: 'approve' | 'reject') => {
        if (!currentProposal) return;

        setApplying(true);

        try {
            const res = await fetch('/api/evolution/apply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    proposal_id: currentProposal.proposal_id,
                    action,
                }),
            });

            const data = await res.json();

            if (data.success) {
                if (action === 'approve') {
                    addNotification(`🧬 Agent ${currentProposal.agent_name} evoluído com sucesso!`, 'success');
                } else {
                    addNotification(`Proposta para ${currentProposal.agent_name} rejeitada`, 'info');
                }
                setShowProposalModal(false);
                setCurrentProposal(null);
                loadData(); // Recarregar dados
            } else {
                addNotification(`Erro: ${data.error}`, 'error');
            }
        } catch (error) {
            console.error('Erro ao aplicar evolução:', error);
            addNotification('Erro ao processar ação', 'error');
        } finally {
            setApplying(false);
        }
    };

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col gap-6 p-2 overflow-hidden">
            {/* HEADER */}
            <div className="flex items-center justify-between px-4">
                <div className="flex items-center gap-4">
                    <div className="p-3 rounded-xl bg-purple-500/20 border border-purple-500">
                        <Dna className="w-7 h-7 text-purple-400" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold text-white tracking-tight font-display">
                            EVOLUTION LAB
                        </h1>
                        <p className="text-sm text-gray-400 font-mono">
                            Auto-evolução de agents com Claude API
                        </p>
                    </div>
                </div>

                <button
                    onClick={loadData}
                    disabled={loading}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[var(--color-primary)]/10 border border-[var(--color-primary)] text-[var(--color-primary)] hover:bg-[var(--color-primary)]/20 transition disabled:opacity-50"
                >
                    <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                    Atualizar
                </button>
            </div>

            {/* TABS */}
            <div className="flex gap-2 px-4">
                <button
                    onClick={() => setActiveTab('candidates')}
                    className={`px-6 py-3 rounded-lg font-bold text-sm transition flex items-center gap-2 ${
                        activeTab === 'candidates'
                            ? 'bg-[var(--color-primary)] text-black'
                            : 'bg-white/5 text-gray-400 hover:bg-white/10'
                    }`}
                >
                    <Target className="w-4 h-4" />
                    Candidatos ({candidates.length})
                </button>
                <button
                    onClick={() => setActiveTab('history')}
                    className={`px-6 py-3 rounded-lg font-bold text-sm transition flex items-center gap-2 ${
                        activeTab === 'history'
                            ? 'bg-[var(--color-primary)] text-black'
                            : 'bg-white/5 text-gray-400 hover:bg-white/10'
                    }`}
                >
                    <History className="w-4 h-4" />
                    Histórico ({history.length})
                </button>
            </div>

            {/* CONTENT */}
            <div className="flex-1 overflow-y-auto px-4">
                {loading ? (
                    <div className="flex items-center justify-center h-full">
                        <div className="flex flex-col items-center gap-4">
                            <RefreshCw className="w-12 h-12 text-[var(--color-primary)] animate-spin" />
                            <p className="text-gray-400">Carregando dados de evolução...</p>
                        </div>
                    </div>
                ) : (
                    <>
                        {/* TAB: CANDIDATOS */}
                        {activeTab === 'candidates' && (
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                                {candidates.length === 0 ? (
                                    <div className="col-span-full flex flex-col items-center justify-center h-64 bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl">
                                        <CheckCircle2 className="w-16 h-16 text-emerald-400 mb-4" />
                                        <p className="text-xl font-bold text-white">Todos os agents estão saudáveis!</p>
                                        <p className="text-sm text-gray-400 mt-2">Nenhum candidato para evolução identificado</p>
                                    </div>
                                ) : (
                                    candidates.map((candidate) => (
                                        <div
                                            key={candidate.agent_id}
                                            className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-[var(--color-primary)]/50 transition group"
                                        >
                                            {/* Header */}
                                            <div className="flex items-start justify-between mb-4">
                                                <div>
                                                    <h3 className="text-lg font-bold text-white">{candidate.agent_name}</h3>
                                                    <p className="text-xs text-gray-400 font-mono">{candidate.agent_role}</p>
                                                </div>
                                                <div className={`px-3 py-1 rounded-full text-xs font-bold ${
                                                    candidate.recommendation === 'urgent'
                                                        ? 'bg-red-500/20 text-red-400 border border-red-500'
                                                        : 'bg-yellow-500/20 text-yellow-400 border border-yellow-500'
                                                }`}>
                                                    {candidate.recommendation === 'urgent' ? '🔴 URGENTE' : '⚠️ RECOMENDADO'}
                                                </div>
                                            </div>

                                            {/* Métricas */}
                                            <div className="grid grid-cols-3 gap-4 mb-4">
                                                <div>
                                                    <div className="text-xs text-gray-400 mb-1">Taxa de Sucesso</div>
                                                    <div className={`text-2xl font-bold ${
                                                        candidate.success_rate >= 75 ? 'text-emerald-400' :
                                                        candidate.success_rate >= 50 ? 'text-yellow-400' : 'text-red-400'
                                                    }`}>
                                                        {candidate.success_rate.toFixed(1)}%
                                                    </div>
                                                </div>
                                                <div>
                                                    <div className="text-xs text-gray-400 mb-1">Requests</div>
                                                    <div className="text-2xl font-bold text-white">{candidate.total_requests}</div>
                                                </div>
                                                <div>
                                                    <div className="text-xs text-gray-400 mb-1">Evoluções</div>
                                                    <div className="text-2xl font-bold text-[var(--color-primary)]">{candidate.evolution_count}</div>
                                                </div>
                                            </div>

                                            {/* Issues */}
                                            <div className="mb-4 space-y-1">
                                                {candidate.issues.slice(0, 3).map((issue, i) => (
                                                    <div key={i} className="flex items-start gap-2 text-xs text-gray-400">
                                                        <AlertTriangle className="w-3 h-3 text-yellow-500 mt-0.5 flex-shrink-0" />
                                                        <span>{issue}</span>
                                                    </div>
                                                ))}
                                            </div>

                                            {/* Action Button */}
                                            <button
                                                onClick={() => handleAnalyzeAgent(candidate.agent_id, candidate.agent_name)}
                                                disabled={proposing}
                                                className="w-full px-4 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold text-sm hover:from-purple-600 hover:to-pink-600 transition disabled:opacity-50 flex items-center justify-center gap-2 group-hover:scale-105"
                                            >
                                                <Brain className="w-4 h-4" />
                                                Analisar com Claude
                                                <Sparkles className="w-4 h-4" />
                                            </button>
                                        </div>
                                    ))
                                )}
                            </div>
                        )}

                        {/* TAB: HISTÓRICO */}
                        {activeTab === 'history' && (
                            <div className="space-y-3">
                                {history.length === 0 ? (
                                    <div className="flex flex-col items-center justify-center h-64 bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl">
                                        <History className="w-16 h-16 text-gray-600 mb-4" />
                                        <p className="text-xl font-bold text-white">Nenhuma evolução aplicada ainda</p>
                                        <p className="text-sm text-gray-400 mt-2">O histórico aparecerá aqui</p>
                                    </div>
                                ) : (
                                    history.map((item) => (
                                        <div
                                            key={item.id}
                                            className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-xl p-4 flex items-center justify-between"
                                        >
                                            <div className="flex items-center gap-4">
                                                <div className={`p-2 rounded-lg ${
                                                    item.status === 'merged' ? 'bg-emerald-500/20 text-emerald-400' :
                                                    item.status === 'rejected' ? 'bg-red-500/20 text-red-400' :
                                                    'bg-yellow-500/20 text-yellow-400'
                                                }`}>
                                                    {item.status === 'merged' ? <CheckCircle2 className="w-5 h-5" /> :
                                                     item.status === 'rejected' ? <XCircle className="w-5 h-5" /> :
                                                     <Clock className="w-5 h-5" />}
                                                </div>
                                                <div>
                                                    <div className="text-sm font-bold text-white">Agent: {item.agent_id}</div>
                                                    <div className="text-xs text-gray-400">
                                                        {new Date(item.created_at).toLocaleString('pt-BR')}
                                                    </div>
                                                </div>
                                            </div>
                                            <div className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${
                                                item.status === 'merged' ? 'bg-emerald-500/20 text-emerald-400' :
                                                item.status === 'rejected' ? 'bg-red-500/20 text-red-400' :
                                                'bg-yellow-500/20 text-yellow-400'
                                            }`}>
                                                {item.status === 'merged' ? '✅ Aplicado' :
                                                 item.status === 'rejected' ? '❌ Rejeitado' : '⏳ Pendente'}
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        )}
                    </>
                )}
            </div>

            {/* MODAL DE PROPOSTA */}
            {showProposalModal && currentProposal && (
                <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-[#02040a] border border-white/20 rounded-3xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
                        {/* Header */}
                        <div className="p-6 border-b border-white/10 flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <div className="p-2 rounded-lg bg-purple-500/20 border border-purple-500">
                                    <Sparkles className="w-6 h-6 text-purple-400" />
                                </div>
                                <div>
                                    <h2 className="text-2xl font-bold text-white">Proposta de Evolução</h2>
                                    <p className="text-sm text-gray-400">{currentProposal.agent_name}</p>
                                </div>
                            </div>
                            <button
                                onClick={() => setShowProposalModal(false)}
                                className="p-2 hover:bg-white/10 rounded-lg transition"
                            >
                                <X className="w-6 h-6 text-gray-400" />
                            </button>
                        </div>

                        {/* Content */}
                        <div className="flex-1 overflow-y-auto p-6 space-y-6">
                            {/* Análise */}
                            <div className="bg-black/40 border border-white/10 rounded-xl p-6">
                                <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                                    <Brain className="w-5 h-5 text-purple-400" />
                                    Análise do Claude
                                </h3>

                                {/* Confidence */}
                                <div className="mb-4">
                                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                                        currentProposal.analysis.confidence === 'high' ? 'bg-emerald-500/20 text-emerald-400' :
                                        currentProposal.analysis.confidence === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                                        'bg-red-500/20 text-red-400'
                                    }`}>
                                        Confiança: {currentProposal.analysis.confidence}
                                    </span>
                                    <span className="ml-3 text-sm text-gray-400">
                                        Ganho esperado: {currentProposal.analysis.expected_gain}
                                    </span>
                                </div>

                                {/* Weaknesses */}
                                <div className="mb-4">
                                    <div className="text-sm font-bold text-red-400 mb-2">❌ Fraquezas Identificadas:</div>
                                    <ul className="list-disc list-inside space-y-1 text-sm text-gray-300">
                                        {currentProposal.analysis.weaknesses.map((w, i) => (
                                            <li key={i}>{w}</li>
                                        ))}
                                    </ul>
                                </div>

                                {/* Improvements */}
                                <div className="mb-4">
                                    <div className="text-sm font-bold text-emerald-400 mb-2">✅ Melhorias Propostas:</div>
                                    <ul className="list-disc list-inside space-y-1 text-sm text-gray-300">
                                        {currentProposal.analysis.improvements.map((imp, i) => (
                                            <li key={i}>{imp}</li>
                                        ))}
                                    </ul>
                                </div>

                                {/* Reasoning */}
                                {currentProposal.analysis.reasoning && (
                                    <div className="mt-4 p-4 bg-white/5 rounded-lg">
                                        <div className="text-xs font-bold text-gray-400 mb-2">Justificativa:</div>
                                        <p className="text-sm text-gray-300">{currentProposal.analysis.reasoning}</p>
                                    </div>
                                )}
                            </div>

                            {/* Diff de Prompts */}
                            <div className="grid grid-cols-2 gap-4">
                                {/* Current Prompt */}
                                <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4">
                                    <div className="text-sm font-bold text-red-400 mb-3 flex items-center gap-2">
                                        <X className="w-4 h-4" />
                                        Prompt Atual
                                    </div>
                                    <div className="bg-black/40 rounded-lg p-4 font-mono text-xs text-gray-300 max-h-64 overflow-y-auto whitespace-pre-wrap">
                                        {currentProposal.current_prompt}
                                    </div>
                                </div>

                                {/* Proposed Prompt */}
                                <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-4">
                                    <div className="text-sm font-bold text-emerald-400 mb-3 flex items-center gap-2">
                                        <Check className="w-4 h-4" />
                                        Prompt Proposto
                                    </div>
                                    <div className="bg-black/40 rounded-lg p-4 font-mono text-xs text-gray-300 max-h-64 overflow-y-auto whitespace-pre-wrap">
                                        {currentProposal.proposed_prompt}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Footer Actions */}
                        <div className="p-6 border-t border-white/10 flex gap-3">
                            <button
                                onClick={() => handleApplyEvolution('reject')}
                                disabled={applying}
                                className="flex-1 px-6 py-4 rounded-xl bg-red-500/20 border border-red-500 text-red-400 font-bold hover:bg-red-500/30 transition disabled:opacity-50 flex items-center justify-center gap-2"
                            >
                                <XCircle className="w-5 h-5" />
                                Rejeitar
                            </button>
                            <button
                                onClick={() => handleApplyEvolution('approve')}
                                disabled={applying}
                                className="flex-1 px-6 py-4 rounded-xl bg-gradient-to-r from-emerald-500 to-cyan-500 text-white font-bold hover:from-emerald-600 hover:to-cyan-600 transition disabled:opacity-50 flex items-center justify-center gap-2"
                            >
                                <CheckCircle2 className="w-5 h-5" />
                                {applying ? 'Aplicando...' : 'Aprovar e Aplicar'}
                                <Zap className="w-5 h-5" />
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Loading Overlay */}
            {analyzing && (
                <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-40 flex items-center justify-center">
                    <div className="bg-[#02040a] border border-purple-500 rounded-2xl p-8 flex flex-col items-center gap-4">
                        <Brain className="w-16 h-16 text-purple-400 animate-pulse" />
                        <div className="text-xl font-bold text-white">Claude está analisando...</div>
                        <p className="text-sm text-gray-400">Gerando proposta de evolução inteligente</p>
                    </div>
                </div>
            )}
        </div>
    );
}
