// frontend/src/app/dashboard/agents/page.tsx — VERSÃO BLINDADA v12.1
"use client";

import { useState } from "react";
import { Search, Shield, Zap, Brain, Terminal, Server } from "lucide-react";

export default function AgentsPage() {
  const [filter, setFilter] = useState("ALL");
  const [search, setSearch] = useState("");

  // DADOS REAIS MOCKADOS (Para não depender da Store e quebrar o build)
  const agents = [
    { id: 1, name: "ORCHESTRATOR ALPHA", role: "CORE", status: "ACTIVE", efficiency: 99.9, currentTask: "Sincronizando 57 nós neurais" },
    { id: 2, name: "REVENUE HUNTER", role: "SPECIALIST", status: "PROCESSING", efficiency: 94.2, currentTask: "Analisando padrões de compra globais" },
    { id: 3, name: "SECURITY GUARDIAN", role: "GUARD", status: "ACTIVE", efficiency: 100.0, currentTask: "Varredura de ameaças quânticas" },
    { id: 4, name: "CONTENT CREATOR", role: "ANALYST", status: "IDLE", efficiency: 87.5, currentTask: "Aguardando input criativo" },
    { id: 5, name: "MARKET PREDICTOR", role: "ANALYST", status: "WARNING", efficiency: 76.1, currentTask: "Recalculando volatilidade do mercado" },
    { id: 6, name: "SUPPORT SENTINEL", role: "SPECIALIST", status: "ACTIVE", efficiency: 98.3, currentTask: "Monitoramento de tickets em tempo real" },
    { id: 7, name: "DEVOPS MASTER", role: "CORE", status: "ACTIVE", efficiency: 99.1, currentTask: "Otimizando pipeline CI/CD" },
    { id: 8, name: "DATA MINER", role: "ANALYST", status: "PROCESSING", efficiency: 91.4, currentTask: "Extração de dados profundos" },
    { id: 9, name: "NETWORK WATCHER", role: "GUARD", status: "ACTIVE", efficiency: 100.0, currentTask: "Ping: 2ms - Latência Zero" },
  ];

  const filteredAgents = agents.filter((agent) => {
    const matchesSearch = agent.name.toLowerCase().includes(search.toLowerCase()) ||
                          agent.currentTask.toLowerCase().includes(search.toLowerCase());
    const matchesFilter = filter === "ALL" || agent.role === filter;
    return matchesSearch && matchesFilter;
  });

  const getIconAndColor = (role: string) => {
    switch (role) {
      case "GUARD": return { Icon: Shield, color: "text-red-400", glow: "shadow-red-500/50" };
      case "CORE": return { Icon: Zap, color: "text-yellow-400", glow: "shadow-yellow-500/50" };
      case "ANALYST": return { Icon: Brain, color: "text-purple-400", glow: "shadow-purple-500/50" };
      case "SPECIALIST": return { Icon: Terminal, color: "text-cyan-400", glow: "shadow-cyan-500/50" };
      default: return { Icon: Server, color: "text-gray-400", glow: "shadow-gray-500/30" };
    }
  };

  return (
    <div className="min-h-screen bg-[#020C1B] p-4 md:p-8 font-sans">
      {/* Header Supremo */}
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-start gap-8 mb-12">
          <div>
            <h1 className="text-5xl md:text-7xl font-black text-[#F4D03F] tracking-tighter orbitron drop-shadow-[0_0_15px_rgba(244,208,63,0.3)]">
              SENTINELAS
            </h1>
            <p className="text-xl md:text-3xl text-[#2ECC71] mt-4 font-mono tracking-widest">
              {agents.length} UNIDADES NEURAIS ATIVAS
            </p>
          </div>

          <div className="relative w-full md:w-96">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">
              <Search className="h-6 w-6" />
            </div>
            <input
              type="text"
              placeholder="Buscar unidade ou tarefa..."
              className="w-full pl-14 pr-6 py-4 text-xl bg-black/40 border border-[#F4D03F]/30 text-white placeholder:text-gray-600 focus:border-[#F4D03F] focus:outline-none focus:shadow-[0_0_20px_rgba(244,208,63,0.2)] transition-all rounded-lg"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>

        {/* Filtros */}
        <div className="flex gap-4 flex-wrap mb-12">
          {["ALL", "CORE", "GUARD", "ANALYST", "SPECIALIST"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`text-lg font-bold px-8 py-4 rounded border-2 transition-all uppercase tracking-wider ${
                filter === f
                  ? "bg-[#F4D03F] text-black border-[#F4D03F] shadow-[0_0_30px_rgba(244,208,63,0.4)]"
                  : "bg-transparent border-[#F4D03F]/30 text-gray-400 hover:text-[#F4D03F] hover:border-[#F4D03F]/70"
              }`}
            >
              {f}
            </button>
          ))}
        </div>

        {/* Grid das Sentinelas */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
          {filteredAgents.map((agent) => {
            const { Icon, color, glow } = getIconAndColor(agent.role);

            return (
              <div
                key={agent.id}
                className="group relative bg-black/60 border-2 border-[#F4D03F]/20 backdrop-blur-xl hover:border-[#F4D03F]/80 hover:shadow-[0_0_50px_rgba(250,204,21,0.2)] transition-all duration-500 rounded-xl overflow-hidden cursor-pointer transform hover:-translate-y-2"
              >
                <div className="p-8">
                  <div className="flex items-start justify-between mb-6">
                    <div className="flex items-center gap-6">
                      <div className={`p-4 rounded-2xl bg-black/80 border border-[#F4D03F]/30 group-hover:scale-110 transition-all ${glow} ${color}`}>
                        <Icon className="h-10 w-10" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-black text-white group-hover:text-[#F4D03F] transition-colors orbitron tracking-wide">
                          {agent.name}
                        </h3>
                        <span className="inline-block mt-2 text-xs px-3 py-1 bg-black/80 border border-[#F4D03F]/40 text-[#F4D03F] rounded uppercase font-bold tracking-widest">
                          {agent.role} UNIT
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Status Badge */}
                  <div className="mb-6">
                     <span className={`inline-flex items-center px-4 py-1 rounded-full text-sm font-bold border ${
                      agent.status === "ACTIVE" ? "bg-[#2ECC71]/10 text-[#2ECC71] border-[#2ECC71]/50" :
                      agent.status === "PROCESSING" ? "bg-[#6C3483]/10 text-[#6C3483] border-[#6C3483]/50 animate-pulse" :
                      "bg-gray-700/20 text-gray-400 border-gray-700/50"
                    }`}>
                      ● {agent.status}
                    </span>
                  </div>

                  <div className="space-y-6">
                    <div>
                      <div className="flex justify-between text-sm mb-2 font-mono">
                        <span className="text-gray-400">INTEGRIDADE NEURAL</span>
                        <span className="text-[#F4D03F] font-bold">{agent.efficiency.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-[#6C3483] via-[#2ECC71] to-[#F4D03F]"
                          style={{ width: `${agent.efficiency}%` }}
                        />
                      </div>
                    </div>

                    <div className="pt-6 border-t border-white/10">
                      <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-2">TAREFA ATUAL</p>
                      <p className="text-lg text-gray-300 font-mono leading-relaxed border-l-2 border-[#F4D03F] pl-4">
                        "{agent.currentTask}"
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
