import os

# 1. CONTEÚDO DA SIDEBAR (LIMPO)
sidebar_code = """
"use client";

import { Button } from "@/components/ui/button";
import { Shield, Brain, Server, MessageSquare, LayoutDashboard, Network, Terminal, Settings, Zap } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const menuItems = [
  { name: "Cockpit", icon: LayoutDashboard, path: "/dashboard", color: "text-white" },
  { name: "Neural Nexus", icon: Network, path: "/dashboard/network", color: "text-pink-500" },
  { name: "Sentinelas", icon: Shield, path: "/dashboard/agents", color: "text-red-400" },
  { name: "Matrix / Logs", icon: Terminal, path: "/dashboard/matrix", color: "text-green-500" },
  { name: "Inteligência", icon: Brain, path: "/dashboard/intelligence", color: "text-blue-400" },
  { name: "Infraestrutura", icon: Server, path: "/dashboard/infrastructure", color: "text-green-400" },
  { name: "Comunicação", icon: MessageSquare, path: "/dashboard/communication", color: "text-purple-400" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="h-screen w-64 bg-black/95 border-r border-white/10 flex flex-col p-4 backdrop-blur-xl z-50">
      <div className="mb-8 flex items-center gap-3 px-2">
        <div className="h-8 w-8 rounded-full bg-gradient-to-br from-purple-600 to-blue-600 animate-pulse shadow-[0_0_15px_rgba(168,85,247,0.5)]" />
        <div>
            <h2 className="font-bold text-white tracking-wider">ALSHAM</h2>
            <p className="text-[10px] text-white/50 tracking-[0.2em]">QUANTUM v11</p>
        </div>
      </div>

      <nav className="space-y-2 flex-1">
        {menuItems.map((item) => {
          const isActive = pathname === item.path;
          return (
            <Link key={item.path} href={item.path}>
              <Button
                variant="ghost"
                className={`w-full justify-start gap-3 mb-1 transition-all duration-300 ${
                  isActive 
                    ? "bg-white/10 border border-white/5 text-white shadow-[0_0_15px_rgba(255,255,255,0.1)]" 
                    : "text-gray-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <item.icon className={`h-4 w-4 ${isActive ? item.color : "text-gray-500"}`} />
                <span className="font-light tracking-wide">{item.name}</span>
              </Button>
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto space-y-2 pt-4 border-t border-white/10">
         <Button variant="outline" className="w-full justify-start gap-2 border-purple-500/30 text-purple-400 hover:bg-purple-500/10 hover:text-purple-200 transition-colors">
            <Zap className="h-4 w-4" />
            Turbo Mode
         </Button>
         <Button variant="ghost" className="w-full justify-start gap-2 text-gray-500 hover:text-white">
            <Settings className="h-4 w-4" />
            Settings
         </Button>
      </div>
    </div>
  );
}
"""

# 2. CONTEÚDO DA PÁGINA DE AGENTES (LIMPO)
agents_page_code = """
"use client";

import { useState } from "react";
import { useQuantumStore } from "@/lib/store";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Shield, Brain, Server, Zap } from "lucide-react";

export default function AgentsPage() {
  const { agents } = useQuantumStore();
  const [filter, setFilter] = useState("ALL");
  const [search, setSearch] = useState("");

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

      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
        {filteredAgents.map((agent) => {
          const Icon = getIcon(agent.role);
          return (
            <Card key={agent.id} className="bg-zinc-900/30 border-white/5 hover:border-purple-500/30 hover:bg-zinc-900/50 transition-all duration-300 group cursor-pointer relative overflow-hidden">
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
"""

# 3. FUNÇÃO PARA ESCREVER OS ARQUIVOS
def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Arquivo RECRIADO com sucesso: {path}")
    except Exception as e:
        print(f"❌ Erro ao criar {path}: {e}")

# EXECUÇÃO
print("🛠️ Iniciando reparo forense dos arquivos corrompidos...")
write_file("src/components/layout/Sidebar.tsx", sidebar_code)
write_file("src/app/dashboard/agents/page.tsx", agents_page_code)
print("🏁 Reparo concluído. Pode fazer o commit agora.")
