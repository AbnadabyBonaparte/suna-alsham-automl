/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SENTINELAS (AGENTS ROSTER) - THEME AWARE
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/agents/page.tsx
 * 📋 Grid de agentes estilo "Seleção de Personagens" com cores dinâmicas
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useEffect } from "react";
import { useAgentsStore } from "@/stores";
import { supabase } from "@/lib/supabase";

// ÍCONES SVG NATIVOS (Zero dependências externas)
const IconsearchQuery = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8" />
    <path d="m21 21-4.3-4.3" />
  </svg>
);

const IconShield = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z" />
  </svg>
);

const IconZap = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
  </svg>
);

const IconBrain = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z" />
    <path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z" />
    <path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4" />
  </svg>
);

const IconTerminal = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="4 17 10 11 4 5" />
    <line x1="12" x2="20" y1="19" y2="19" />
  </svg>
);

const IconServer = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect width="20" height="8" x="2" y="2" rx="2" ry="2" />
    <rect width="20" height="8" x="2" y="14" rx="2" ry="2" />
    <line x1="6" x2="6.01" y1="6" y2="6" />
    <line x1="6" x2="6.01" y1="18" y2="18" />
  </svg>
);



// Agent type definition matching Supabase schema
interface Agent {
  id: string | number;
  name: string;
  role: string;
  status: string;
  efficiency: number;
  current_task?: string;
  currentTask?: string;
}

// Fallback data if Supabase connection fails
const AGENTS_DATA = [
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

export default function AgentsPage() {
  const store = useAgentsStore();
  const { 
    agents, 
    loading, 
    error, 
    filteredSquadedSquad, 
    searchQueryQuery,
    setAgents,
    setLoading,
    setError,
    setfilteredSquadedSquad,
    setsearchQueryQuery,
    getfilteredSquadedAgents
  } = store;

  // Fetch agents from Supabase on mount
  useEffect(() => {
    async function fetchAgents() {
      try {
        setLoading(true);
        const { data, error: supabaseError } = await supabase
          .from("agents")
          .select("*")
          .order("created_at", { ascending: true });

        if (supabaseError) {
          console.error("Error fetching agents:", supabaseError);
          setError(supabaseError.message);
        } else if (data && data.length > 0) {
          const normalizedData = data.map((agent: any) => ({
            ...agent,
            currentTask: agent.current_task || "Aguardando comando",
          }));
          setAgents(normalizedData);
        }
      } catch (err: any) {
        console.error("Failed to fetch agents:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    if (agents.length === 0) {
      fetchAgents();
    }
  }, []);

  const filteredSquadedAgents = getfilteredSquadedAgents();

  const renderIcon = (role: string) => {
    switch (role) {
      case "GUARD": return <IconShield />;
      case "CORE": return <IconZap />;
      case "ANALYST": return <IconBrain />;
      case "SPECIALIST": return <IconTerminal />;
      default: return <IconServer />;
    }
  };

  return (
    <div className="min-h-screen pb-20 font-sans">
      <div className="max-w-7xl mx-auto">
        {/* HEADER */}
        <div className="flex flex-col md:flex-row justify-between items-start gap-8 mb-12">
          <div>
            <h1 className="text-5xl md:text-7xl font-black text-[var(--color-primary)] tracking-tighter orbitron drop-shadow-[0_0_15px_rgba(var(--color-primary-rgb),0.3)]">
              SENTINELAS
            </h1>
            <p className="text-xl md:text-3xl text-[var(--color-text-secondary)] mt-4 font-mono tracking-widest">
              {agents.length} UNIDADES NEURAIS ATIVAS
            </p>
          </div>

          <div className="relative w-full md:w-96">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">
              <IconsearchQuery />
            </div>
            <input
              type="text"
              placeholder="Buscar unidade..."
              className="w-full pl-14 pr-6 py-4 text-xl bg-black/40 border border-[var(--color-border)]/30 text-white placeholder:text-gray-600 focus:border-[var(--color-primary)] focus:outline-none focus:shadow-[0_0_20px_var(--color-primary)] transition-all rounded-lg"
              value={searchQuery}
              onChange={(e) => setsearchQueryQuery(e.target.value)}
            />
          </div>
        </div>

        {/* FILTROS */}
        <div className="flex gap-4 flex-wrap mb-12">
          {["ALL", "CORE", "GUARD", "ANALYST", "SPECIALIST"].map((f) => (
            <button
              key={f}
              onClick={() => setfilteredSquadedSquad(f)}
              className={`text-lg font-bold px-8 py-4 rounded border-2 transition-all uppercase tracking-wider ${filteredSquad === f
                ? "bg-[var(--color-primary)]/10 text-[var(--color-primary)] border-[var(--color-primary)] shadow-[0_0_30px_var(--color-primary)]"
                : "bg-transparent border-[var(--color-border)]/30 text-gray-400 hover:text-[var(--color-primary)] hover:border-[var(--color-primary)]/70"
                }`}
            >
              {f}
            </button>
          ))}
        </div>

        {/* GRID */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
          {filteredSquadedAgents.map((agent) => {
            return (
              <div
                key={agent.id}
                className="group relative bg-[var(--color-surface)]/60 border-2 border-[var(--color-border)]/20 backdrop-blur-xl hover:border-[var(--color-primary)]/80 hover:shadow-[0_0_50px_var(--color-primary)] transition-all duration-500 rounded-xl overflow-hidden cursor-pointer transform hover:-translate-y-2"
              >
                <div className="p-8">
                  <div className="flex items-start justify-between mb-6">
                    <div className="flex items-center gap-6">
                      <div className="p-4 rounded-2xl bg-black/80 border border-[var(--color-border)]/30 group-hover:scale-110 transition-all text-[var(--color-primary)] shadow-[0_0_15px_var(--color-primary)]">
                        {renderIcon(agent.role)}
                      </div>
                      <div>
                        <h3 className="text-2xl font-black text-white group-hover:text-[var(--color-primary)] transition-colors orbitron tracking-wide">
                          {agent.name}
                        </h3>
                        <span className="inline-block mt-2 text-xs px-3 py-1 bg-black/80 border border-[var(--color-primary)]/40 text-[var(--color-primary)] rounded uppercase font-bold tracking-widest">
                          {agent.role} UNIT
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="mb-6">
                    <span
                      className={`inline-flex items-center px-4 py-1 rounded-full text-sm font-bold border ${agent.status === "ACTIVE"
                        ? "bg-[var(--color-success)]/10 text-[var(--color-success)] border-[var(--color-success)]/50"
                        : agent.status === "PROCESSING"
                          ? "bg-[var(--color-warning)]/10 text-[var(--color-warning)] border-[var(--color-warning)]/50 animate-pulse"
                          : "bg-gray-700/20 text-gray-400 border-gray-700/50"
                        }`}
                    >
                      ● {agent.status}
                    </span>
                  </div>

                  <div className="space-y-6">
                    <div>
                      <div className="flex justify-between text-sm mb-2 font-mono">
                        <span className="text-gray-400">INTEGRIDADE NEURAL</span>
                        <span className="text-[var(--color-primary)] font-bold">{agent.efficiency.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-[var(--color-secondary)] via-[var(--color-primary)] to-[var(--color-accent)]"
                          style={{ width: `${agent.efficiency}%` }}
                        />
                      </div>
                    </div>

                    <div className="pt-6 border-t border-white/10">
                      <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-2">TAREFA ATUAL</p>
                      <p className="text-lg text-gray-300 font-mono leading-relaxed border-l-2 border-[var(--color-primary)] pl-4">
                        &quot;{agent.currentTask}&quot;
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


