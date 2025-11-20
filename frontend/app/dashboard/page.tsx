"use client";

import { useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Activity, Shield, Zap, Database, Terminal } from "lucide-react";
import { useQuantumStore } from "@/lib/store";

export default function DashboardPage() {
  const { agents, metrics, isLive, simulatePulse, toggleLiveMode } = useQuantumStore();

  useEffect(() => {
    const interval = setInterval(() => {
      simulatePulse();
    }, 2000); 
    return () => clearInterval(interval);
  }, [simulatePulse]);

  return (
    <div className="p-8 space-y-8 min-h-screen bg-black text-white/90 font-sans selection:bg-purple-500/30">
      
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-white/10 pb-6">
        <div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-fuchsia-300 to-white tracking-tight">
            Cockpit de Deus
          </h1>
          <p className="text-white/50 mt-1 font-light tracking-wide">
            Sistema ALSHAM QUANTUM v11.0 <span className="text-green-500 mx-2">•</span> Online
          </p>
        </div>
        <div className="flex gap-3">
          <Button 
            variant="outline" 
            className={`border-purple-500/30 hover:bg-purple-900/20 transition-all ${isLive ? 'text-green-400 border-green-500/30 animate-pulse' : 'text-gray-400'}`}
            onClick={toggleLiveMode}
          >
            <Activity className="mr-2 h-4 w-4" />
            {isLive ? "LIVE STREAM: ON" : "STREAM PAUSED"}
          </Button>
          <Button className="bg-white text-black hover:bg-gray-200 font-medium">
            <Zap className="mr-2 h-4 w-4 fill-black" /> Iniciar Onda 2
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KpiCard title="ROI Total" value={`${metrics.roi}%`} sub="+12% hoje" icon={Activity} color="text-purple-400" />
        <KpiCard title="Economia Gerada" value={`R$ ${metrics.savings}B`} sub="Acumulado Global" icon={Database} color="text-green-400" />
        <KpiCard title="Carga do Sistema" value={`${metrics.systemLoad.toFixed(1)}%`} sub="Capacidade Neural" icon={Zap} color="text-amber-400" />
        <KpiCard title="Agentes Ativos" value={metrics.activeAgents.toString()} sub="Rede Neural" icon={Shield} color="text-blue-400" />
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-white/80 flex items-center gap-2">
            <Terminal className="h-5 w-5 text-purple-500" />
            Status da Rede Neural
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <Card 
              key={agent.id} 
              className="bg-black/40 border-white/10 backdrop-blur-md hover:border-purple-500/50 transition-all duration-500 group"
            >
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-white/70 group-hover:text-purple-300 transition-colors">
                  {agent.name}
                </CardTitle>
                <StatusBadge status={agent.status} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white mb-1">
                  {agent.efficiency.toFixed(1)}% <span className="text-xs font-normal text-white/30">Eficiência</span>
                </div>
                <p className="text-xs text-white/40 font-mono mt-2">
                  Task: <span className="text-purple-300/80">{agent.currentTask}</span>
                </p>
                <div className="w-full bg-white/5 h-1 mt-4 rounded-full overflow-hidden">
                    <div 
                        className="bg-purple-500 h-full transition-all duration-1000 ease-in-out" 
                        style={{ width: `${agent.efficiency}%` }}
                    />
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
    <Card className="bg-black/40 border-white/10 backdrop-blur-md hover:bg-white/5 transition-colors">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-white/60">{title}</CardTitle>
        <Icon className={`h-4 w-4 ${color}`} />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-white">{value}</div>
        <p className="text-xs text-white/40">{sub}</p>
      </CardContent>
    </Card>
  );
}

function StatusBadge({ status }: { status: string }) {
    const colors: Record<string, string> = {
        IDLE: "bg-gray-500/10 text-gray-400 border-gray-500/20",
        PROCESSING: "bg-blue-500/10 text-blue-400 border-blue-500/20 animate-pulse",
        LEARNING: "bg-purple-500/10 text-purple-400 border-purple-500/20",
        WARNING: "bg-amber-500/10 text-amber-400 border-amber-500/20",
        ERROR: "bg-red-500/10 text-red-400 border-red-500/20",
    };
    return (
        <Badge variant="outline" className={`${colors[status] || colors.IDLE} border font-mono text-[10px]`}>
            {status}
        </Badge>
    );
}
