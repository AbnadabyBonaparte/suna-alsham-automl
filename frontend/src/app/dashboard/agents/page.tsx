// frontend/src/app/dashboard/agents/page.tsx — SENTINELAS v12.1 FINAL (100% FUNCIONAL SEM FRAMER MOTION)
"use client";

import { useState } from "react";
import { useQuantumStore } from "@/lib/store";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Shield, Brain, Zap, Terminal, Server } from "lucide-react";

export default function AgentsPage() {
  const { agents } = useQuantumStore();
  const [filter, setFilter] = useState("ALL");
  const [search, setSearch] = useState("");

  const filteredAgents = agents.filter((agent) => {
    const matchesSearch = agent.name.toLowerCase().includes(search.toLowerCase()) ||
                          agent.currentTask?.toLowerCase().includes(search.toLowerCase());
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
    <div className="min-h-screen bg-black p-8">
      {/* Header Supremo */}
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-start gap-8 mb-12">
          <div>
            <h1 className="text-7xl font-black text-yellow-500 orbitron tracking-tighter">
              SENTINELAS
            </h1>
            <p className="text-3xl text-green-400 mt-4 font-mono">
              {agents.length} UNIDADES NEURAIS ATIVAS
            </p>
          </div>

          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-6 w-6 text-gray-500" />
            <Input
              placeholder="Buscar unidade ou tarefa..."
              className="pl-14 pr-6 py-7 text-xl bg-black/40 border-yellow-500/30 text-white placeholder:text-gray-600 focus:border-yellow-500/70 transition-all w-96"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>

        {/* Filtros */}
        <div className="flex gap-4 flex-wrap mb-12">
          {["ALL", "CORE", "GUARD", "ANALYST", "SPECIALIST"].map((f) => (
            <Button
              key={f}
              variant={filter === f ? "default" : "outline"}
              onClick={() => setFilter(f)}
              className={`text-xl px-8 py-6 transition-all ${
                filter === f
                  ? "bg-yellow-500 text-black hover:bg-yellow-400 shadow-[0_0_30px_rgba(250,204,21,0.6)]"
                  : "border-yellow-500/30 text-gray-400 hover:text-yellow-500 hover:border-yellow-500/70"
              }`}
            >
              {f}
            </Button>
          ))}
        </div>

        {/* Grid das Sentinelas */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
          {filteredAgents.map((agent) => {
            const { Icon, color, glow } = getIconAndColor(agent.role);

            return (
              <Card
                key={agent.id}
                className={`bg-black/60 border-2 border-yellow-500/20 backdrop-blur-xl hover:border-yellow-500/80 hover:shadow-[0_0_50px_rgba(250,204,21,0.4)] transition-all duration-500 group cursor-pointer overflow-hidden relative transform hover:-translate-y-4`}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-transparent via-purple-900/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />

                <div className="p-8">
                  <div className="flex items-start justify-between mb-6">
                    <div className="flex items-center gap-6">
                      <div className={`p-4 rounded-2xl bg-black/60 border-2 border-yellow-500/30 group-hover:scale-110 transition-all ${glow}`}>
                        <Icon className={`h-12 w-12 ${color}`} />
                      </div>
                      <div>
                        <h3 className="text-3xl font-black text-yellow-500 orbitron">
                          {agent.name}
                        </h3>
                        <Badge className="mt-2 text-lg px-4 py-2 bg-black/60 border-yellow-500/50 text-yellow-400">
                          {agent.role} UNIT
                        </Badge>
                      </div>
                    </div>
                    <Badge className={`text-xl px-6 py-3 ${
                      agent.status === "ACTIVE" ? "bg-green-500/20 text-green-400 border-green-500/50" :
                      agent.status === "PROCESSING" ? "bg-purple-500/20 text-purple-400 border-purple-500/50 animate-pulse" :
                      "bg-gray-700/20 text-gray-400 border-gray-700/50"
                    }`}>
                      {agent.status}
                    </Badge>
                  </div>

                  <div className="space-y-6">
                    <div>
                      <div className="flex justify-between text-lg mb-2">
                        <span className="text-gray-400">Integridade Neural</span>
                        <span className="text-yellow-500 font-black text-2xl">{agent.efficiency.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-black/80 h-6 rounded-full overflow-hidden border border-yellow-500/20">
                        <div 
                          className="h-full bg-gradient-to-r from-purple-600 via-blue-500 to-green-500 transition-all duration-2000 ease-out"
                          style={{ width: `${agent.efficiency}%` }}
                        />
                      </div>
                    </div>

                    <div className="pt-6 border-t border-yellow-500/20">
                      <p className="text-sm text-gray-500 mb-2">Tarefa Atual</p>
                      <p className="text-xl text-gray-300 font-mono leading-relaxed">
                        "{agent.currentTask || "Aguardando comando do Criador..."}"
                      </p>
                    </div>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}
