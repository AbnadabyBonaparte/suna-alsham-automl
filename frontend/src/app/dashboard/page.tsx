// frontend/src/app/dashboard/page.tsx — VERSÃO FINAL 100% FUNCIONAL
"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Activity, Shield, Zap, Database, Terminal, Cpu, PauseOctagon } from "lucide-react";
import { useQuantumStore } from "@/lib/store";
import { toggleSystemMode } from "@/lib/actions";
import { useSfx } from "@/hooks/use-sfx";

export default function DashboardPage() {
  const { agents, metrics, isLive, simulatePulse, toggleLiveMode } = useQuantumStore();
  const { play } = useSfx();
  const [isPending, setIsPending] = useState(false);
  const [panicMode, setPanicMode] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => simulatePulse(), 2000);
    return () => clearInterval(interval);
  }, [simulatePulse]);

  const handleCommand = async (mode: "TURBO" | "STOP") => {
    setIsPending(true);
    play(mode === "STOP" ? "alert" : "click");

    if (mode === "STOP") {
      setPanicMode(true);
      const submarineAlarm = setInterval(() => play("alert"), 900);
      setTimeout(() => {
        clearInterval(submarineAlarm);
        setPanicMode(false);
      }, 12000);
    }

    try {
      const result = await toggleSystemMode(mode);
      if (result.success) play("ambient");
    } catch (error) {
      console.error("Erro crítico:", error);
      play("alert");
    } finally {
      setIsPending(false);
    }
  };

  function getBarColor(efficiency: number) {
    if (efficiency >= 90) return "bg-gradient-to-r from-purple-500 to-blue-500 shadow-[0_0_10px_rgba(168,85,247,0.5)]";
    if (efficiency >= 70) return "bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.4)]";
    if (efficiency >= 40) return "bg-amber-500";
    return "bg-red-500";
  }

  return (
    <>
      <div className={`p-8 space-y-8 w-full max-w-[1600px] mx-auto transition-all duration-500 ${panicMode ? "blur-sm" : ""}`}>
        {/* Header Tático */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-white/10 pb-6 bg-black/20 backdrop-blur-sm sticky top-0 z-40">
          <div>
            <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-fuchsia-300 to-white tracking-tight">
              Cockpit de Deus
            </h1>
            <p className="text-zinc-400 mt-1 font-light tracking-wide flex items-center gap-2">
              <span className={`inline-block w-2 h-2 rounded-full ${isLive ? "bg-green-500 animate-pulse" : "bg-red-500"}`}></span>
              ALSHAM QUANTUM v12.1 <span className="text-zinc-600">|</span> Operacional
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Button onClick={() => handleCommand("TURBO")} disabled={isPending || panicMode} className="bg-purple-600/20 hover:bg-purple-600/40 text-purple-300 border border-purple-500/30 transition-all">
              <Zap className="mr-2 h-4 w-4" /> TURBO MODE
            </Button>
            <Button variant="destructive" onClick={() => handleCommand("STOP")} disabled={isPending || panicMode} className="bg-red-900/20 hover:bg-red-900/40 text-red-400 border border-red-500/30 font-bold">
              <PauseOctagon className="mr-2 h-4 w-4" /> CONTAINMENT
            </Button>
            <Button variant="outline" onClick={() => { play("click"); toggleLiveMode(); }} className={`border-purple-500/30 bg-purple-500/10 hover:bg-purple-500/20 transition-all ${isLive ? "text-green-400 border-green-500/30" : "text-gray-400"}`}>
              <Activity className="mr-2 h-4 w-4" /> {isLive ? "LIVE STREAM" : "PAUSED"}
            </Button>
          </div>
        </div>

        {/* KPI Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KpiCard title="ROI Total" value={`${metrics.roi}%`} sub="+12% hoje" icon={Activity} color="text-purple-400" />
          <KpiCard title="Economia" value={`R$ ${metrics.savings}B`} sub="Acumulado Global" icon={Database} color="text-green-400" />
          <KpiCard title="Carga Neural" value={`${metrics.systemLoad.toFixed(1)}%`} sub="Capacidade de CPU" icon={Cpu} color="text-amber-400" />
          <KpiCard title="Agentes" value={metrics.activeAgents.toString()} sub="Rede Ativa" icon={Shield} color="text-blue-400" />
        </div>

        {/* Agents Grid */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-white flex items-center gap-3">
              <Terminal className="h-6 w-6 text-purple-500" />
              Rede Neural Ativa
            </h2>
            <Badge variant="outline" className="bg-zinc-900 text-zinc-500 border-zinc-800">
              {agents.length} NÓS CONECTADOS
            </Badge>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            {agents.map((agent) => (
              <Card key={agent.id} className="bg-zinc-900/40 border-white/5 backdrop-blur-sm hover:border-purple-500/50 hover:bg-zinc-900/60 transition-all duration-300 group relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-r from-purple-500/0 via-purple-500/5 to-purple-500/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000 pointer-events-none" />
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <div className="space-y-1">
                    <CardTitle className="text-sm font-medium text-zinc-200 group-hover:text-purple-300 transition-colors flex items-center gap-2">
                      {agent.name}
                      {agent.status === "ACTIVE" && <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />}
                    </CardTitle>
                    <p className="text-[10px] text-zinc-500 uppercase tracking-wider font-mono">{agent.role}</p>
                  </div>
                  <StatusBadge status={agent.status} />
                </CardHeader>
                <CardContent>
                  <div className="flex items-end justify-between mb-2">
                    <div className="text-2xl font-bold text-white font-mono">{agent.efficiency ? agent.efficiency.toFixed(0) : 0}%</div>
                    <span className="text-xs text-zinc-500 mb-1">Eficiência</span>
                  </div>
                  <div className="w-full bg-black/50 h-1.5 rounded-full overflow-hidden">
                    <div className={`h-full transition-all duration-1000 ease-in-out ${getBarColor(agent.efficiency || 0)}`} style={{ width: `${agent.efficiency || 0}%` }} />
                  </div>
                  <div className="mt-4 flex items-center gap-2 text-xs text-zinc-400 bg-black/20 p-2 rounded border border-white/5 font-mono">
                    <Terminal className="w-3 h-3 text-purple-500/70" />
                    <span className="truncate text-purple-200/70">{agent.currentTask || "Aguardando instrução..."}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>

      {/* OVERLAY CONTAINMENT */}
      {panicMode && (
        <div className="fixed inset-0 bg-red-900/98 z-[99999] flex items-center justify-center pointer-events-none">
          <div className="text-center animate-pulse">
            <h1 className="text-8xl md:text-9xl font-black text-red-500 drop-shadow-[0_0_80px_red] tracking-tighter">
              CONTAINMENT PROTOCOL ACTIVATED
            </h1>
            <p className="text-2xl text-red-200 mt-12 font-mono tracking-widest">
              ALL SYSTEMS FROZEN • 57 AGENTS CONTAINED
            </p>
          </div>
        </div>
      )}
    </>
  );
}

function KpiCard({ title, value, sub, icon: Icon, color }: any) {
  return (
    <Card className="bg-zinc-900/40 border-white/5 backdrop-blur-sm hover:bg-zinc-900/60 transition-colors">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-zinc-400">{title}</CardTitle>
        <Icon className={`h-4 w-4 ${color}`} />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-white">{value}</div>
        <p className="text-xs text-zinc-500 mt-1">{sub}</p>
      </CardContent>
    </Card>
  );
}

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    ACTIVE: "bg-green-500/10 text-green-400 border-green-500/20",
    IDLE: "bg-zinc-500/10 text-zinc-400 border-zinc-500/20",
    PROCESSING: "bg-blue-500/10 text-blue-400 border-blue-500/20 animate-pulse",
    LEARNING: "bg-purple-500/10 text-purple-400 border-purple-500/20",
    WARNING: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    ERROR: "bg-red-500/10 text-red-400 border-red-500/20",
    CRITICAL: "bg-red-900/20 text-red-500 border-red-500/50 animate-bounce",
  };
  return (
    <Badge variant="outline" className={`${colors[status] || colors.IDLE} border font-mono text-[10px] uppercase tracking-wider`}>
      {status}
    </Badge>
  );
}
