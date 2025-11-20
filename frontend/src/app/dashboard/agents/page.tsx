"use client";

import { useState } from "react";
import { useQuantumStore } from "@/lib/store";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Filter, Shield, Brain, Server, MessageSquare, Activity, Zap } from "lucide-react";

export default function AgentsPage() {
  const { agents } = useQuantumStore();
  const [filter, setFilter] = useState("ALL");
  const [search, setSearch] = useState("");

  // Filtragem Lógica
  const filteredAgents = agents.filter(agent => {
    const matchesSearch = agent.name.toLowerCase().includes(search.toLowerCase());
    const matchesFilter = filter === "ALL" || agent.role === filter;
    return matchesSearch && matchesFilter;
  });

  const getIcon = (role: string) => {
    switch(role) {
      case 'GUARD': return Shield;
      case 'CORE': return Zap;
      case 'ANALYST': return Brain;
      default: return Server;
    }
  };

  return (
    <div className="p-8 space-y-8 min-h-screen bg-black/50">
      
      {/* Header Tático */}
      <div className="flex flex-col md:flex-row justify-between items-end gap-4 border-b border-white/10 pb-6">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <Shield className="h-8 w-8 text-red-500" />
            Sentinelas & Operações
          </h1>
          <p className="text-zinc-400 mt-2 font-mono text-sm">
            Gerenciamento Ativo da Frota Neural ({agents.length} Unidades)
          </p>
        </div>
        
        <div className="flex gap-2">
           <div className="relative">
             <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-500" />
             <Input 
               placeholder="Buscar unidade..." 
               className="pl-9 bg-zinc-900/50 border-zinc-800 text-white w-64 focus:border-purple-500/50 transition-all"
               onChange={(e) => setSearch(e.target.value)}
             />
           </div>
        </div>
      </div>

      {/* Filtros */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {['ALL', 'CORE', 'GUARD', 'SPECIALIST', 'ANALYST'].map((role) => (
          <Button
            key={role}
            variant="outline"
            onClick={() => setFilter(role)}
            className={`border-zinc-800 hover:bg-zinc-800 transition-all ${filter === role ? 'bg-white text-black border-white' : 'bg-transparent text-zinc-400'}`}
          >
            {role}
          </Button>
        ))}
      </div>

      {/* Grid de Agentes */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
        {filteredAgents.map((agent) => {
          const Icon = getIcon(agent.role);
          return (
            <Card key={agent.id} className="bg-zinc-900/30 border-white/5 hover:border-purple-500/30 hover:bg-zinc-900/50 transition-all duration-300 group cursor-pointer relative overflow-hidden">
              
              {/* Barra de Status Lateral */}
              <div className={`absolute left-0 top-0 bottom-0 w-1 ${agent.efficiency > 90 ? 'bg-green-500' : agent.efficiency > 70 ? 'bg-blue-500' : 'bg-amber-500'}`} />

              <div className="p-5 pl-7">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-white/5 group-hover:bg-purple-500/20 transition-colors">
                      <Icon className="h-5 w-5 text-zinc-300 group-hover:text-purple-300" />
                    </div>
                    <div>
                      <h3 className="font-bold text-white group-hover:text-purple-200 transition-colors">{agent.name}</h3>
                      <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">{agent.role} UNIT</p>
                    </div>
                  </div>
                  <Badge variant="outline" className={`${agent.status === 'PROCESSING' ? 'text-blue-400 border-blue-500/30 animate-pulse' : 'text-zinc-500 border-zinc-800'}`}>
                    {agent.status}
                  </Badge>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between text-xs text-zinc-400">
                    <span>Integridade Neural</span>
                    <span className="text-white font-mono">{agent.efficiency.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-black/50 h-1 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-purple-600 to-blue-500 transition-all duration-1000" 
                      style={{ width: `${agent.efficiency}%` }} 
                    />
                  </div>
                  
                  <div className="pt-3 mt-3 border-t border-white/5 flex items-center justify-between">
                    <span className="text-xs font-mono text-zinc-500 truncate max-w-[150px]">
                      Task: {agent.currentTask}
                    </span>
                    <span className="text-[10px] text-zinc-600">
                      {agent.lastActive}
                    </span>
                  </div>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
