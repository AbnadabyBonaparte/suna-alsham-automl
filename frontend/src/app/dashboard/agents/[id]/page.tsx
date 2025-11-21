"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useQuantumStore } from "@/lib/store";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Zap, Activity, Shield, Terminal, Brain, Cpu } from "lucide-react";
import { useSfx } from "@/hooks/use-sfx";

export default function AgentDetailPage() {
    const params = useParams();
    const router = useRouter();
    const { agents } = useQuantumStore();
    const { play } = useSfx();
    const [agent, setAgent] = useState<any>(null);
    const [isEvolving, setIsEvolving] = useState(false);

    useEffect(() => {
        if (params.id) {
            const foundAgent = agents.find((a) => a.id === params.id);
            if (foundAgent) {
                setAgent(foundAgent);
            } else {
                // Fallback for demo/mock if ID not found in store (or redirect)
                // For now, let's just show a mock if not found to avoid broken page during dev
                setAgent({
                    id: params.id,
                    name: "UNKNOWN AGENT",
                    role: "UNKNOWN",
                    status: "OFFLINE",
                    efficiency: 0,
                    currentTask: "Signal lost...",
                    logs: []
                });
            }
        }
    }, [params.id, agents]);

    const handleEvolve = () => {
        play("click");
        setIsEvolving(true);
        setTimeout(() => {
            play("upgrade"); // Assuming upgrade sound exists or fallback to another
            setIsEvolving(false);
            // Here we would actually trigger an evolution action in the store
        }, 2000);
    };

    if (!agent) return <div className="p-12 text-center text-zinc-500">Locating Agent Signal...</div>;

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
                    ${agent.status === 'ACTIVE' ? 'border-green-500 text-green-400' : 'border-zinc-700 text-zinc-500'}
                `}>
                            {agent.status}
                        </Badge>
                    </h1>
                    <p className="text-zinc-400 font-mono text-sm mt-1">ID: {agent.id} • ROLE: {agent.role}</p>
                </div>
                <Button
                    onClick={handleEvolve}
                    disabled={isEvolving}
                    className={`
                bg-purple-600/20 border border-purple-500/50 text-purple-300 hover:bg-purple-600/40
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
                                {agent.efficiency?.toFixed(1)}%
                            </div>
                            <div className="w-full bg-black/50 h-2 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-gradient-to-r from-purple-500 to-blue-500 transition-all duration-1000"
                                    style={{ width: `${agent.efficiency}%` }}
                                />
                            </div>
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
                                <span className="text-zinc-500">CPU Core</span>
                                <span className="text-white">Thread #{Math.floor(Math.random() * 12)}</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-zinc-500">Memory</span>
                                <span className="text-white">{(Math.random() * 512).toFixed(0)} MB</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-zinc-500">Uptime</span>
                                <span className="text-white">{(Math.random() * 48).toFixed(1)}h</span>
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
                            <div className="bg-black/80 rounded-lg p-4 font-mono text-xs h-[400px] overflow-y-auto space-y-2 text-green-400/80 border border-white/5">
                                <p className="opacity-50">Initializing connection to {agent.name}...</p>
                                <p className="opacity-70">Secure channel established.</p>
                                <p>&gt; Current task: {agent.currentTask}</p>
                                {Array.from({ length: 8 }).map((_, i) => (
                                    <p key={i} className="opacity-90">
                                        &gt; [{(Math.random() * 1000).toFixed(3)}ms] Processing data chunk #{Math.floor(Math.random() * 9999)}...
                                    </p>
                                ))}
                                <p className="animate-pulse">&gt; Awaiting next instruction_</p>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
