import { Button } from "@/components/ui/button";
import { Activity, Cpu, ShieldAlert, Zap, Brain, Globe, Database } from "lucide-react";

// Dados Reais baseados no seu README
const agents = [
  { id: 1, name: "Core Agent Evolution", role: "CORE V3", status: "active", load: 88, type: "core" },
  { id: 2, name: "Guard Agent Sentinel", role: "SECURITY", status: "active", load: 42, type: "security" },
  { id: 3, name: "Specialist Alpha", role: "SPECIALIZED", status: "thinking", load: 91, type: "special" },
  { id: 4, name: "Analytics Prime", role: "DATA INTEL", status: "active", load: 65, type: "data" },
  { id: 5, name: "Predictor Omega", role: "FORECASTING", status: "idle", load: 12, type: "data" },
  { id: 6, name: "AI Analyzer Supreme", role: "AI POWERED", status: "active", load: 78, type: "ai" },
  { id: 7, name: "Monitor Vigilant", role: "SYSTEM", status: "active", load: 23, type: "sys" },
  { id: 8, name: "WebSearch Explorer", role: "INTEL", status: "active", load: 56, type: "web" },
];

export default function Dashboard() {
  return (
    <div className="min-h-screen p-8 space-y-8 animate-in fade-in duration-700">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
             <h2 className="text-3xl font-bold tracking-tight text-white text-glow">COCKPIT SUPREMO</h2>
             <span className="px-2 py-1 rounded-full bg-[#6C3483]/20 text-[#6C3483] text-xs border border-[#6C3483]/50">v11.0</span>
          </div>
          <p className="text-muted-foreground">Monitorando Organismo Digital • 57 Agentes Totais</p>
        </div>
        <Button variant="outline" className="bg-black/40 border-[#F4D03F] text-[#F4D03F] hover:bg-[#F4D03F]/10">
          <Zap className="mr-2 h-4 w-4" /> INICIAR ONDA 2
        </Button>
      </div>

      {/* KPIs Reais */}
      <div className="grid gap-4 md:grid-cols-4">
        {[
          { label: "ROI GLOBAL", value: "+2.847%", icon: Activity, color: "text-[#F4D03F]" },
          { label: "CICLOS EVOLUTIVOS", value: "1,847", icon: Zap, color: "text-purple-400" },
          { label: "UPTIME SLA", value: "99.98%", icon: ShieldAlert, color: "text-green-400" },
          { label: "ECONOMIA TOTAL", value: "R$ 4.7B", icon: Database, color: "text-blue-400" },
        ].map((metric, i) => (
          <div key={i} className="glass-panel p-6 rounded-xl flex flex-col justify-between hover:bg-white/5 transition-colors cursor-default">
            <div className="flex items-center justify-between space-y-0 pb-2">
              <span className="text-xs font-medium text-muted-foreground tracking-wider">{metric.label}</span>
              <metric.icon className={`h-4 w-4 ${metric.color}`} />
            </div>
            <div className="text-2xl font-bold text-white">{metric.value}</div>
          </div>
        ))}
      </div>

      {/* Grid de Agentes */}
      <h3 className="text-xl font-semibold text-white mt-8 mb-4 flex items-center gap-2">
        <Brain className="h-5 w-5 text-[#6C3483]" /> Agentes Ativos (Live Feed)
      </h3>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {agents.map((agent) => (
          <div key={agent.id} className="group relative overflow-hidden rounded-xl border border-white/5 bg-black/20 p-5 hover:border-[#F4D03F]/30 hover:bg-black/40 transition-all duration-300">
            
            {/* Status Dot */}
            <div className="absolute top-4 right-4 flex items-center gap-2">
              <span className={`h-1.5 w-1.5 rounded-full ${agent.status === 'active' ? 'bg-[#2ECC71] shadow-[0_0_8px_#2ECC71]' : 'bg-yellow-500'}`} />
            </div>

            <div className="mb-4">
              <div className="text-xs font-mono text-blue-400 mb-1">{agent.role}</div>
              <h3 className="text-lg font-bold text-white group-hover:text-[#F4D03F] transition-colors">{agent.name}</h3>
            </div>

            {/* Barra de Carga */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-[10px] text-muted-foreground uppercase tracking-wider">
                <span>Carga Neural</span>
                <span>{agent.load}%</span>
              </div>
              <div className="h-1 w-full rounded-full bg-white/5">
                <div 
                  className="h-full rounded-full bg-gradient-to-r from-[#6C3483] to-[#F4D03F] opacity-80" 
                  style={{ width: `${agent.load}%` }}
                />
              </div>
            </div>

            {/* Footer do Card */}
            <div className="mt-4 pt-4 border-t border-white/5 flex justify-between items-center opacity-50 group-hover:opacity-100 transition-opacity">
               <span className="text-[10px] text-gray-400">ID: {agent.type}_{agent.id}</span>
               <span className="text-[10px] text-[#F4D03F] cursor-pointer hover:underline">LOGS &rarr;</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
