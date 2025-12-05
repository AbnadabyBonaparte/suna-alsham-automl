/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - AGENT AUTO-EVOLUTION LAB (THEME-AWARE)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/evolution/page.tsx
 * 🧬 Sistema de Auto-Evolução de Agents usando Claude API
 * 🎨 100% SUBMISSO AOS TEMAS - USA VARIÁVEIS CSS
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect } from 'react';
import { useNotificationStore } from '@/stores/useNotificationStore';
import { useTheme } from '@/contexts/ThemeContext';
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
    const { themeConfig } = useTheme();
    const colors = themeConfig.colors;

    const [loading, setLoading] = useState(true);
    const [analyzing, setAnalyzing] = useState(false);
    const [candidates, setCandidates] = useState<AgentCandidate[]>([]);
    const [history, setHistory] = useState<EvolutionHistory[]>([]);

    const [showProposalModal, setShowProposalModal] = useState(false);
    const [currentProposal, setCurrentProposal] = useState<Proposal | null>(null);
    const [proposing, setProposing] = useState(false);
    const [applying, setApplying] = useState(false);

    const [activeTab, setActiveTab] = useState<'candidates' | 'history'>('candidates');

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const candidatesRes = await fetch('/api/evolution/analyze');
            const candidatesData = await candidatesRes.json();

            if (candidatesData.success) {
                setCandidates(candidatesData.candidates || []);
            }

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
                loadData();
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
                    <div 
                        className="p-3 rounded-xl"
                        style={{
                            background: `${colors.primary}/20`,
                            border: `1px solid ${colors.primary}`
                        }}
                    >
                        <Dna className="w-7 h-7" style={{ color: colors.primary }} />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight font-display" style={{ color: colors.text }}>
                            EVOLUTION LAB
                        </h1>
                        <p className="text-sm font-mono" style={{ color: colors.textSecondary }}>
                            Auto-evolução de agents com Claude API
                        </p>
                    </div>
                </div>

                <button
                    onClick={loadData}
                    disabled={loading}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg transition disabled:opacity-50"
                    style={{
                        background: `${colors.primary}/10`,
                        border: `1px solid ${colors.primary}`,
                        color: colors.primary
                    }}
                >
                    <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                    Atualizar
                </button>
            </div>

            {/* TABS */}
            <div className="flex gap-2 px-4">
                <button
                    onClick={() => setActiveTab('candidates')}
                    className="px-6 py-3 rounded-lg font-bold text-sm transition flex items-center gap-2"
                    style={{
                        background: activeTab === 'candidates' ? colors.primary : `${colors.surface}`,
                        color: activeTab === 'candidates' ? colors.background : colors.textSecondary,
                        border: `1px solid ${activeTab === 'candidates' ? colors.primary : colors.border}`
                    }}
                >
                    <Target className="w-4 h-4" />
                    Candidatos ({candidates.length})
                </button>
                <button
                    onClick={() => setActiveTab('history')}
                    className="px-6 py-3 rounded-lg font-bold text-sm transition flex items-center gap-2"
                    style={{
                        background: activeTab === 'history' ? colors.primary : `${colors.surface}`,
                        color: activeTab === 'history' ? colors.background : colors.textSecondary,
                        border: `1px solid ${activeTab === 'history' ? colors.primary : colors.border}`
                    }}
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
                            <RefreshCw className="w-12 h-12 animate-spin" style={{ color: colors.primary }} />
                            <p style={{ color: colors.textSecondary }}>Carregando dados de evolução...</p>
                        </div>
                    </div>
                ) : (
                    <>
                        {activeTab === 'candidates' && (
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                                {candidates.length === 0 ? (
                                    <div 
                                        className="col-span-full flex flex-col items-center justify-center h-64 backdrop-blur-xl rounded-2xl"
                                        style={{
                                            background: `${colors.surface}/40`,
                                            border: `1px solid ${colors.border}/10`
                                        }}
                                    >
                                        <CheckCircle2 className="w-16 h-16 mb-4" style={{ color: colors.success }} />
                                        <p className="text-xl font-bold" style={{ color: colors.text }}>Todos os agents estão saudáveis!</p>
                                        <p className="text-sm mt-2" style={{ color: colors.textSecondary }}>Nenhum candidato para evolução identificado</p>
                                    </div>
                                ) : (
                                    candidates.map((candidate) => (
                                        <div
                                            key={candidate.agent_id}
                                            className="backdrop-blur-xl rounded-2xl p-6 transition group"
                                            style={{
                                                background: `${colors.surface}/40`,
                                                border: `1px solid ${colors.border}/10`
                                            }}
                                        >
                                            <div className="flex items-start justify-between mb-4">
                                                <div>
                                                    <h3 className="text-lg font-bold" style={{ color: colors.text }}>{candidate.agent_name}</h3>
                                                    <p className="text-xs font-mono" style={{ color: colors.textSecondary }}>{candidate.agent_role}</p>
                                                </div>
                                                <div 
                                                    className="px-3 py-1 rounded-full text-xs font-bold"
                                                    style={{
                                                        background: candidate.recommendation === 'urgent' 
                                                            ? `${colors.error}/20` 
                                                            : `${colors.warning}/20`,
                                                        color: candidate.recommendation === 'urgent' 
                                                            ? colors.error 
                                                            : colors.warning,
                                                        border: `1px solid ${candidate.recommendation === 'urgent' ? colors.error : colors.warning}`
                                                    }}
                                                >
                                                    {candidate.recommendation === 'urgent' ? '🔴 URGENTE' : '⚠️ RECOMENDADO'}
                                                </div>
                                            </div>

                                            <div className="grid grid-cols-3 gap-4 mb-4">
                                                <div>
                                                    <div className="text-xs mb-1" style={{ color: colors.textSecondary }}>Taxa de Sucesso</div>
                                                    <div 
                                                        className="text-2xl font-bold"
                                                        style={{
                                                            color: candidate.success_rate >= 75 ? colors.success :
                                                                   candidate.success_rate >= 50 ? colors.warning : colors.error
                                                        }}
                                                    >
                                                        {candidate.success_rate.toFixed(1)}%
                                                    </div>
                                                </div>
                                                <div>
                                                    <div className="text-xs mb-1" style={{ color: colors.textSecondary }}>Requests</div>
                                                    <div className="text-2xl font-bold" style={{ color: colors.text }}>{candidate.total_requests}</div>
                                                </div>
                                                <div>
                                                    <div className="text-xs mb-1" style={{ color: colors.textSecondary }}>Evoluções</div>
                                                    <div className="text-2xl font-bold" style={{ color: colors.primary }}>{candidate.evolution_count}</div>
                                                </div>
                                            </div>

                                            <div className="mb-4 space-y-1">
                                                {candidate.issues.slice(0, 3).map((issue, i) => (
                                                    <div key={i} className="flex items-start gap-2 text-xs" style={{ color: colors.textSecondary }}>
                                                        <AlertTriangle className="w-3 h-3 mt-0.5 flex-shrink-0" style={{ color: colors.warning }} />
                                                        <span>{issue}</span>
                                                    </div>
                                                ))}
                                            </div>

                                            <button
                                                onClick={() => handleAnalyzeAgent(candidate.agent_id, candidate.agent_name)}
                                                disabled={proposing}
                                                className="w-full px-4 py-3 rounded-lg font-bold text-sm transition disabled:opacity-50 flex items-center justify-center gap-2"
                                                style={{
                                                    background: `linear-gradient(to right, ${colors.primary}, ${colors.accent})`,
                                                    color: 'white'
                                                }}
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

                        {activeTab === 'history' && (
                            <div className="space-y-3">
                                {history.length === 0 ? (
                                    <div 
                                        className="flex flex-col items-center justify-center h-64 backdrop-blur-xl rounded-2xl"
                                        style={{
                                            background: `${colors.surface}/40`,
                                            border: `1px solid ${colors.border}/10`
                                        }}
                                    >
                                        <History className="w-16 h-16 mb-4" style={{ color: colors.textSecondary }} />
                                        <p className="text-xl font-bold" style={{ color: colors.text }}>Nenhuma evolução aplicada ainda</p>
                                        <p className="text-sm mt-2" style={{ color: colors.textSecondary }}>O histórico aparecerá aqui</p>
                                    </div>
                                ) : (
                                    history.map((item) => (
                                        <div
                                            key={item.id}
                                            className="backdrop-blur-xl rounded-xl p-4 flex items-center justify-between"
                                            style={{
                                                background: `${colors.surface}/40`,
                                                border: `1px solid ${colors.border}/10`
                                            }}
                                        >
                                            <div className="flex items-center gap-4">
                                                <div 
                                                    className="p-2 rounded-lg"
                                                    style={{
                                                        background: item.status === 'merged' ? `${colors.success}/20` :
                                                                   item.status === 'rejected' ? `${colors.error}/20` :
                                                                   `${colors.warning}/20`,
                                                        color: item.status === 'merged' ? colors.success :
                                                               item.status === 'rejected' ? colors.error :
                                                               colors.warning
                                                    }}
                                                >
                                                    {item.status === 'merged' ? <CheckCircle2 className="w-5 h-5" /> :
                                                     item.status === 'rejected' ? <XCircle className="w-5 h-5" /> :
                                                     <Clock className="w-5 h-5" />}
                                                </div>
                                                <div>
                                                    <div className="text-sm font-bold" style={{ color: colors.text }}>Agent: {item.agent_id}</div>
                                                    <div className="text-xs" style={{ color: colors.textSecondary }}>
                                                        {new Date(item.created_at).toLocaleString('pt-BR')}
                                                    </div>
                                                </div>
                                            </div>
                                            <div 
                                                className="px-3 py-1 rounded-full text-xs font-bold uppercase"
                                                style={{
                                                    background: item.status === 'merged' ? `${colors.success}/20` :
                                                               item.status === 'rejected' ? `${colors.error}/20` :
                                                               `${colors.warning}/20`,
                                                    color: item.status === 'merged' ? colors.success :
                                                           item.status === 'rejected' ? colors.error :
                                                           colors.warning
                                                }}
                                            >
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
                <div className="fixed inset-0 backdrop-blur-sm z-50 flex items-center justify-center p-4" style={{ background: `${colors.background}/80` }}>
                    <div 
                        className="rounded-3xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col"
                        style={{
                            background: colors.background,
                            border: `1px solid ${colors.border}/20`
                        }}
                    >
                        {/* Header */}
                        <div className="p-6 flex items-center justify-between" style={{ borderBottom: `1px solid ${colors.border}/10` }}>
                            <div className="flex items-center gap-3">
                                <div 
                                    className="p-2 rounded-lg"
                                    style={{
                                        background: `${colors.primary}/20`,
                                        border: `1px solid ${colors.primary}`
                                    }}
                                >
                                    <Sparkles className="w-6 h-6" style={{ color: colors.primary }} />
                                </div>
                                <div>
                                    <h2 className="text-2xl font-bold" style={{ color: colors.text }}>Proposta de Evolução</h2>
                                    <p className="text-sm" style={{ color: colors.textSecondary }}>{currentProposal.agent_name}</p>
                                </div>
                            </div>
                            <button
                                onClick={() => setShowProposalModal(false)}
                                className="p-2 rounded-lg transition"
                                style={{ color: colors.textSecondary }}
                            >
                                <X className="w-6 h-6" />
                            </button>
                        </div>

                        {/* Content */}
                        <div className="flex-1 overflow-y-auto p-6 space-y-6">
                            {/* Análise */}
                            <div 
                                className="rounded-xl p-6"
                                style={{
                                    background: `${colors.surface}/40`,
                                    border: `1px solid ${colors.border}/10`
                                }}
                            >
                                <h3 className="text-lg font-bold mb-4 flex items-center gap-2" style={{ color: colors.text }}>
                                    <Brain className="w-5 h-5" style={{ color: colors.primary }} />
                                    Análise do Claude
                                </h3>

                                <div className="mb-4">
                                    <span 
                                        className="px-3 py-1 rounded-full text-xs font-bold"
                                        style={{
                                            background: currentProposal.analysis.confidence === 'high' ? `${colors.success}/20` :
                                                       currentProposal.analysis.confidence === 'medium' ? `${colors.warning}/20` :
                                                       `${colors.error}/20`,
                                            color: currentProposal.analysis.confidence === 'high' ? colors.success :
                                                   currentProposal.analysis.confidence === 'medium' ? colors.warning :
                                                   colors.error
                                        }}
                                    >
                                        Confiança: {currentProposal.analysis.confidence}
                                    </span>
                                    <span className="ml-3 text-sm" style={{ color: colors.textSecondary }}>
                                        Ganho esperado: {currentProposal.analysis.expected_gain}
                                    </span>
                                </div>

                                <div className="mb-4">
                                    <div className="text-sm font-bold mb-2" style={{ color: colors.error }}>❌ Fraquezas Identificadas:</div>
                                    <ul className="list-disc list-inside space-y-1 text-sm" style={{ color: colors.text }}>
                                        {currentProposal.analysis.weaknesses.map((w, i) => (
                                            <li key={i}>{w}</li>
                                        ))}
                                    </ul>
                                </div>

                                <div className="mb-4">
                                    <div className="text-sm font-bold mb-2" style={{ color: colors.success }}>✅ Melhorias Propostas:</div>
                                    <ul className="list-disc list-inside space-y-1 text-sm" style={{ color: colors.text }}>
                                        {currentProposal.analysis.improvements.map((imp, i) => (
                                            <li key={i}>{imp}</li>
                                        ))}
                                    </ul>
                                </div>

                                {currentProposal.analysis.reasoning && (
                                    <div 
                                        className="mt-4 p-4 rounded-lg"
                                        style={{ background: `${colors.surface}` }}
                                    >
                                        <div className="text-xs font-bold mb-2" style={{ color: colors.textSecondary }}>Justificativa:</div>
                                        <p className="text-sm" style={{ color: colors.text }}>{currentProposal.analysis.reasoning}</p>
                                    </div>
                                )}
                            </div>

                            {/* Diff */}
                            <div className="grid grid-cols-2 gap-4">
                                <div 
                                    className="rounded-xl p-4"
                                    style={{
                                        background: `${colors.error}/10`,
                                        border: `1px solid ${colors.error}/30`
                                    }}
                                >
                                    <div className="text-sm font-bold mb-3 flex items-center gap-2" style={{ color: colors.error }}>
                                        <X className="w-4 h-4" />
                                        Prompt Atual
                                    </div>
                                    <div 
                                        className="rounded-lg p-4 font-mono text-xs max-h-64 overflow-y-auto whitespace-pre-wrap"
                                        style={{ background: `${colors.background}/40`, color: colors.text }}
                                    >
                                        {currentProposal.current_prompt}
                                    </div>
                                </div>

                                <div 
                                    className="rounded-xl p-4"
                                    style={{
                                        background: `${colors.success}/10`,
                                        border: `1px solid ${colors.success}/30`
                                    }}
                                >
                                    <div className="text-sm font-bold mb-3 flex items-center gap-2" style={{ color: colors.success }}>
                                        <Check className="w-4 h-4" />
                                        Prompt Proposto
                                    </div>
                                    <div 
                                        className="rounded-lg p-4 font-mono text-xs max-h-64 overflow-y-auto whitespace-pre-wrap"
                                        style={{ background: `${colors.background}/40`, color: colors.text }}
                                    >
                                        {currentProposal.proposed_prompt}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Footer */}
                        <div className="p-6 flex gap-3" style={{ borderTop: `1px solid ${colors.border}/10` }}>
                            <button
                                onClick={() => handleApplyEvolution('reject')}
                                disabled={applying}
                                className="flex-1 px-6 py-4 rounded-xl font-bold transition disabled:opacity-50 flex items-center justify-center gap-2"
                                style={{
                                    background: `${colors.error}/20`,
                                    border: `1px solid ${colors.error}`,
                                    color: colors.error
                                }}
                            >
                                <XCircle className="w-5 h-5" />
                                Rejeitar
                            </button>
                            <button
                                onClick={() => handleApplyEvolution('approve')}
                                disabled={applying}
                                className="flex-1 px-6 py-4 rounded-xl font-bold text-white transition disabled:opacity-50 flex items-center justify-center gap-2"
                                style={{
                                    background: `linear-gradient(to right, ${colors.success}, ${colors.accent})`
                                }}
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
                <div 
                    className="fixed inset-0 backdrop-blur-sm z-40 flex items-center justify-center"
                    style={{ background: `${colors.background}/80` }}
                >
                    <div 
                        className="rounded-2xl p-8 flex flex-col items-center gap-4"
                        style={{
                            background: colors.background,
                            border: `1px solid ${colors.primary}`
                        }}
                    >
                        <Brain className="w-16 h-16 animate-pulse" style={{ color: colors.primary }} />
                        <div className="text-xl font-bold" style={{ color: colors.text }}>Claude está analisando...</div>
                        <p className="text-sm" style={{ color: colors.textSecondary }}>Gerando proposta de evolução inteligente</p>
                    </div>
                </div>
            )}
        </div>
    );
}
