"use client";

import { useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Activity, Shield, Zap, Database, Terminal, Cpu } from "lucide-react";
import { useQuantumStore } from "@/lib/store";

export default function DashboardPage() {
  const { agents, metrics, isLive, simulatePulse, toggleLiveMode } = useQuantumStore();

  useEffect(() => {
    const interval = setInterval(() => simulatePulse(), 2000); 
    return () => clearInterval(interval);
  }, [simulatePulse]);

  return (
    <div className="p-8 space-y-8 w-full max-w-[1600px] mx-auto">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-white/10 pb-6 bg-black/20 backdrop-blur-sm sticky top-0 z-40">
        <div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-fuchsia-300 to-white tracking-tight">
            Cockpit de Deus
          </h1>
          <p className="text-zinc-400 mt-1 font-light tracking-wide flex items-center gap-2">
            <span className="inline-block w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            ALSHAM QUANTUM v11.0 <span className="text-zinc-600">|</span> Operacional
          </p>
        </div>
        <div className="flex gap-3">
          <Button 
            variant="outline" 
            className={`border-purple-500/30 bg-purple-500/10 hover:bg-purple-500/20 transition-all ${isLive ? 'text-green-400 border-green-500/30' : 'text-gray-400'}`}
            onClick={toggleLiveMode}
          >
            <Activity className="mr-2 h-4 w-4" />
            {isLive ? "LIVE STREAM" : "PAUSED"}
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
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <Card 
              key={agent.id} 
              className="bg-zinc-900/40 border-white/5 backdrop-blur-sm hover:border-purple-500/50 hover:bg-zinc-900/60 transition-all duration-300 group"
            >
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <div className="space-y-1">
                  <CardTitle className="text-sm font-medium text-zinc-200 group-hover:text-purple-300 transition-colors">
                    {agent.name}
                  </CardTitle>
                  <p className="text-[10px] text-zinc-500 uppercase tracking-wider">{agent.role}</p>
                </div>
                <StatusBadge status={agent.status} />
              </CardHeader>
              <CardContent>
                <div className="flex items-end justify-between mb-2">
                   <div className="text-2xl font-bold text-white">
                     {agent.efficiency.toFixed(1)}%
                   </div>
                   <span className="text-xs text-zinc-500 mb-1">Eficiência</span>
                </div>
                
                <div className="w-full bg-black/50 h-1.5 rounded-full overflow-hidden">
                    <div 
                        className={`h-full transition-all duration-1000 ease-in-out ${getBarColor(agent.efficiency)}`}
                        style={{ width: `${agent.efficiency}%` }}
                    />
                </div>
                
                <div className="mt-4 flex items-center gap-2 text-xs text-zinc-400 bg-black/20 p-2 rounded border border-white/5">
                  <span className="w-1.5 h-1.5 rounded-full bg-purple-500/50"></span>
                  <span className="truncate font-mono text-purple-200/70">{agent.currentTask}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

function KpiCard({ title, value, sub, icon: Icon, color }: any) {
  return (
    <Card className="bg-zinc-900/40 border-white/5 backdrop-blur-sm">
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
        IDLE: "bg-zinc-500/10 text-zinc-400 border-zinc-500/20",
        PROCESSING: "bg-blue-500/10 text-blue-400 border-blue-500/20 animate-pulse",
        LEARNING: "bg-purple-500/10 text-purple-400 border-purple-500/20",
        WARNING: "bg-amber-500/10 text-amber-400 border-amber-500/20",
        ERROR: "bg-red-500/10 text-red-400 border-red-500/20",
    };
    return (
        <Badge variant="outline" className={`${colors[status] || colors.IDLE} border font-mono text-[10px] uppercase`}>
            {status}
        </Badge>
    );
}

function getBarColor(efficiency: number) {
  if (efficiency > 90) return "bg-gradient-to-r from-purple-500 to-blue-500";
  if (efficiency > 70) return "bg-blue-500";
  return "bg-amber-500";
}