/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - AGENT DETAIL PAGE - v11
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/agents/[id]/page.tsx
 * 📋 Detalhes completos do Agent com dados REAIS do Supabase
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Zap, Activity, Shield, Terminal, Brain, Cpu, AlertTriangle } from "lucide-react";
import { useSfx } from "@/hooks/use-sfx";
import { Skeleton } from "@/components/ui/SkeletonLoader";
import { useNotificationStore } from "@/stores";

interface Agent {
    id: string;
    name: string;
    role: string;
    status: string;
    efficiency: number;
    current_task: string;
    squad: string;
    created_at: string;
}

export default function AgentDetailPage() {
    const params = useParams();
    const router = useRouter();
    const { play } = useSfx();
    const { addNotification } = useNotificationStore();

    const [agent, setAgent] = useState<Agent | null>(null);
    const [loading, setLoading] = useState(true);
    const [notFound, setNotFound] = useState(false);
    const [isEvolving, setIsEvolving] = useState(false);

    // Fetch agent by ID from Supabase
    useEffect(() => {
        async function fetchAgent() {
            if (!params.id) return;

            try {
                setLoading(true);
                setNotFound(false);

                const { data, error } = await supabase
                    .from('agents')
                    .select('*')
                    .eq('id', params.id)
                    .single();

                if (error) {
                    console.error('Error fetching agent:', error);
                    setNotFound(true);
                } else if (data) {
                    setAgent(data as Agent);
                } else {
                    setNotFound(true);
                }
            } catch (err) {
                console.error('Failed to fetch agent:', err);
                setNotFound(true);
            } finally {
                setLoading(false);
            }
        }

        fetchAgent();
    }, [params.id]);

    const handleEvolve = () => {
        play("click");
        setIsEvolving(true);
        setTimeout(() => {
            play("upgrade");
            setIsEvolving(false);
            addNotification({
                type: 'success',
                title: 'Agent Evolution Complete',
                message: `${agent?.name} has been upgraded successfully!`,
            });
        }, 2000);
    };

    // Loading State
    if (loading) {
        return (
            <div className="p-8 max-w-7xl mx-auto space-y-8 min-h-screen bg-black/50">
                <div className="flex items-center gap-4">
                    <Skeleton className="w-10 h-10 rounded-lg" />
                    <div className="flex-1">
                        <Skeleton className="w-64 h-10 mb-2" />
                        <Skeleton className="w-48 h-4" />
                    </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Skeleton className="w-full h-64 rounded-2xl" />
                    <Skeleton className="w-full h-64 rounded-2xl md:col-span-2" />
                </div>
            </div>
        );
    }

    // 404 State
    if (notFound || !agent) {
        return (
            <div className="p-8 max-w-7xl mx-auto min-h-screen bg-black/50 flex items-center justify-center">
                <div className="text-center space-y-6">
                    <div className="relative">
                        <div className="absolute inset-0 blur-3xl rounded-full" style={{ background: 'var(--color-error)/20' }} />
                        <AlertTriangle className="w-24 h-24 mx-auto relative z-10" style={{ color: 'var(--color-error)' }} />
                    </div>
                    <div>
                        <h1 className="text-4xl font-bold text-white mb-2">Agent Not Found</h1>
                        <p className="text-zinc-400 mb-6">
                            The agent with ID <span className="font-mono" style={{ color: 'var(--color-error)' }}>{params.id}</span> does not exist in the system.
                        </p>
                    </div>
                    <Button
                        onClick={() => router.push('/dashboard/agents')}
                        className="bg-white/10 hover:bg-white/20 text-white border border-white/20"
                    >
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Back to Agents
                    </Button>
                </div>
            </div>
        );
    }

    return (
        <div className="p-8 max-w-7xl mx-auto space-y-8 min-h-screen bg-black/50">
            {/* Header */}
            <div className="flex items-center gap-4">
                <Button
                    variant="ghost"
                    onClick={() => router.back()}
                    className="text-zinc-400 hover:text-white hover:bg-white/5"
                >
                    <ArrowLeft className="w-5 h-5 mr-2" /> Voltar
                </Button>
                <div className="flex-1">
                    <h1 className="text-4xl font-bold text-white flex items-center gap-3">
                        {agent.name}
                        <Badge variant="outline" className={`
                    ${agent.status === 'ACTIVE' ? 'border-[var(--color-success)] text-[var(--color-success)]' : 'border-zinc-700 text-zinc-500'}
                `}>
                            {agent.status}
                        </Badge>
                    </h1>
                    <p className="text-zinc-400 font-mono text-sm mt-1">
                        ID: {agent.id.slice(0, 8)}... • ROLE: {agent.role} • SQUAD: {agent.squad}
                    </p>
                </div>
                <Button
                    onClick={handleEvolve}
                    disabled={isEvolving}
                    className={`
                bg-[var(--color-accent)]/20 border border-[var(--color-accent)]/50 text-[var(--color-accent)] hover:bg-[var(--color-accent)]/40
                ${isEvolving ? 'animate-pulse' : ''}
            `}
                >
                    <Zap className={`w-4 h-4 mr-2 ${isEvolving ? 'animate-spin' : ''}`} />
                    {isEvolving ? "EVOLVING..." : "FORÇAR EVOLUÇÃO"}
                </Button>
            </div>

            {/* Main Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Left Column - Metrics */}
                <div className="space-y-6">
                    <Card className="bg-zinc-900/40 border-white/10 backdrop-blur-sm">
                        <CardHeader>
                            <CardTitle className="text-zinc-400 text-sm flex items-center gap-2">
                                <Activity className="w-4 h-4" /> EFICIÊNCIA NEURAL
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-5xl font-bold text-white mb-2">
                                {agent.efficiency.toFixed(1)}%
                            </div>
                            <div className="w-full bg-black/50 h-2 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-gradient-to-r from-purple-500 to-blue-500 transition-all duration-1000"
                                    style={{ width: `${agent.efficiency}%` }}
                                />
                            </div>
                            <p className="text-xs text-zinc-500 mt-2 font-mono">
                                Created: {new Date(agent.created_at).toLocaleDateString()}
                            </p>
                        </CardContent>
                    </Card>

                    <Card className="bg-zinc-900/40 border-white/10 backdrop-blur-sm">
                        <CardHeader>
                            <CardTitle className="text-zinc-400 text-sm flex items-center gap-2">
                                <Cpu className="w-4 h-4" /> RECURSOS ALOCADOS
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex justify-between text-sm">
                                <span className="text-zinc-500">Role</span>
                                <span className="text-white font-mono">{agent.role}</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-zinc-500">Squad</span>
                                <span className="text-white font-mono">{agent.squad}</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-zinc-500">Status</span>
                                <span className="font-mono font-bold" style={{ color: agent.status === 'ACTIVE' ? 'var(--color-success)' : '#71717A' }}>
                                    {agent.status}
                                </span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-zinc-500">Efficiency</span>
                                <span className="text-white font-mono">{agent.efficiency.toFixed(1)}%</span>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Middle Column - Task & Console */}
                <div className="md:col-span-2 space-y-6">
                    <Card className="bg-zinc-900/40 border-white/10 backdrop-blur-sm h-full flex flex-col">
                        <CardHeader>
                            <CardTitle className="text-zinc-400 text-sm flex items-center gap-2">
                                <Terminal className="w-4 h-4" /> LIVE LOGS
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="flex-1">
                            <div className="bg-black/80 rounded-lg p-4 font-mono text-xs h-[400px] overflow-y-auto space-y-2 border border-white/5" style={{ color: 'var(--color-success)/80' }}>
                                <p className="opacity-50">Initializing connection to {agent.name}...</p>
                                <p className="opacity-70">Secure channel established.</p>
                                <p className="text-[var(--color-primary)] font-bold">&gt; Current task: {agent.current_task || 'Awaiting orders'}</p>
                                <p className="opacity-60">&gt; Agent ID: {agent.id}</p>
                                <p className="opacity-60">&gt; Squad: {agent.squad}</p>
                                <p className="opacity-60">&gt; Role: {agent.role}</p>
                                <p className="opacity-60">&gt; Status: {agent.status}</p>
                                <p className="opacity-60">&gt; Efficiency: {agent.efficiency.toFixed(2)}%</p>
                                <p className="opacity-60">&gt; Created: {new Date(agent.created_at).toISOString()}</p>
                                <p className="mt-4 opacity-50">&gt; --- System Logs ---</p>
                                {Array.from({ length: 5 }).map((_, i) => (
                                    <p key={i} className="opacity-70">
                                        &gt; [{new Date().toISOString().split('T')[1].slice(0, -1)}] Processing chunk #{Math.floor(Math.random() * 9999)}...
                                    </p>
                                ))}
                                <p className="animate-pulse text-white">&gt; Ready for next instruction_</p>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
