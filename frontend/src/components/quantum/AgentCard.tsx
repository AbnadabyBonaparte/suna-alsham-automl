// src/components/quantum/AgentCard.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Terminal } from "lucide-react";

interface Agent {
  id: string;
  name: string;
  role: string;
  status: string;
  efficiency: number;
  currentTask: string;
}

export default function AgentCard({ agent }: { agent: Agent }) {
  const getBarColor = (eff: number) => {
    if (eff >= 90) return "bg-gradient-to-r from-purple-500 to-blue-500 shadow-[0_0_20px_rgba(168,85,247,0.8)]";
    if (eff >= 70) return "bg-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.6)]";
    if (eff >= 40) return "bg-amber-500";
    return "bg-red-500";
  };

  return (
    <Card className="bg-black/40 border-photon-gold/20 backdrop-blur-xl hover:border-photon-gold/60 hover:scale-105 transition-all duration-500 group relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
      
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start">
          <CardTitle className="text-lg font-bold text-photon-gold orbitron">
            {agent.name}
          </CardTitle>
          <Badge className={`text-xs ${
            agent.status === "ACTIVE" ? "bg-emerald-action/20 text-emerald-action" :
            agent.status === "PROCESSING" ? "bg-arcane-purple/20 text-arcane-purple animate-pulse" :
            "bg-gray-500/20 text-gray-400"
          }`}>
            {agent.status}
          </Badge>
        </div>
        <p className="text-xs text-gray-400">{agent.role}</p>
      </CardHeader>

      <CardContent>
        <div className="flex items-end justify-between mb-3">
          <span className="text-3xl font-black text-photon-gold">{agent.efficiency.toFixed(0)}%</span>
          <span className="text-xs text-gray-500">Eficiência</span>
        </div>
        
        <div className="w-full bg-black/60 h-3 rounded-full overflow-hidden">
          <div className={`h-full transition-all duration-1000 ${getBarColor(agent.efficiency)}`} style={{ width: `${agent.efficiency}%` }} />
        </div>

        <div className="mt-4 flex items-center gap-2 text-xs bg-black/40 p-3 rounded border border-photon-gold/10">
          <Terminal className="w-4 h-4 text-arcane-purple" />
          <span className="truncate text-gray-300">{agent.currentTask || "Aguardando comando..."}</span>
        </div>
      </CardContent>
    </Card>
  );
}
