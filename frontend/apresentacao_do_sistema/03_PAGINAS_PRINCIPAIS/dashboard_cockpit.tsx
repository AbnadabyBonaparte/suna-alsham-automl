"use client";

import { motion } from "framer-motion";
import MegaCounter from "@/components/MegaCounter";
import AgentCard from "@/components/AgentCard";
import { Sparkles, TrendingUp, Shield, Zap } from "lucide-react";
import Link from "next/link";

export default function Dashboard() {
  const agents = [
    { name: "Orion Prime", role: "Coordenador", status: "active" as const, efficiency: 98 },
    { name: "Nexus Flow", role: "Automação", status: "processing" as const, efficiency: 85 },
    { name: "Aegis Core", role: "Segurança", status: "idle" as const, efficiency: 100 },
    { name: "Quantum V", role: "Análise", status: "active" as const, efficiency: 92 },
  ];

  return (
    <div className="min-h-screen p-4 md:p-8 pb-24">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-12 flex flex-col md:flex-row justify-between items-end border-b border-[var(--color-glass-border)] pb-6"
      >
        <div>
          <h1 className="text-4xl md:text-6xl font-orbitron font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-[var(--color-neon-blue)] mb-2">
            DASHBOARD SUPREMO
          </h1>
          <p className="text-[var(--color-quantum-purple)] tracking-widest uppercase text-sm">
            Sistema Unificado de Navegação Autônoma
          </p>
        </div>
        <div className="flex gap-4 mt-4 md:mt-0">
          <div className="text-right">
            <div className="text-xs text-gray-400 uppercase">Status do Sistema</div>
            <div className="text-[var(--color-neon-blue)] font-orbitron flex items-center gap-2 justify-end">
              <span className="w-2 h-2 bg-[var(--color-neon-blue)] rounded-full animate-pulse" />
              ONLINE
            </div>
          </div>
        </div>
      </motion.div>

      {/* Mega Counters Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <MegaCounter label="Ciclos Quânticos" value="8,492" subtext="+12% vs última hora" />
        <MegaCounter label="Valor do Sistema" value="R$ 1.2M" subtext="ROI Projetado: 450%" />
        <MegaCounter label="Eficiência Global" value="94.8%" subtext="Otimização em tempo real" />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Agents Section */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-orbitron flex items-center gap-2">
              <Sparkles className="text-[var(--color-photon-gold)]" />
              Agentes Ativos
            </h2>
            <Link href="/dashboard/agents" className="text-sm text-[var(--color-neon-blue)] hover:underline">
              Ver Todos
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {agents.map((agent, idx) => (
              <AgentCard key={idx} {...agent} />
            ))}
          </div>
        </div>

        {/* Side Panel */}
        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-xl">
            <h3 className="font-orbitron text-lg mb-4 flex items-center gap-2 text-[var(--color-neon-blue)]">
              <TrendingUp className="w-5 h-5" />
              Métricas em Tempo Real
            </h3>
            <div className="space-y-4">
              {[
                { label: "Throughput", value: "1.2 GB/s", color: "bg-blue-500" },
                { label: "Latência", value: "12ms", color: "bg-green-500" },
                { label: "Erros", value: "0.01%", color: "bg-red-500" },
              ].map((metric, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                  <span className="text-gray-400 text-sm">{metric.label}</span>
                  <span className="font-orbitron text-white">{metric.value}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="glass-panel p-6 rounded-xl border border-[var(--color-photon-gold)]/30">
            <h3 className="font-orbitron text-lg mb-4 flex items-center gap-2 text-[var(--color-photon-gold)]">
              <Shield className="w-5 h-5" />
              Segurança
            </h3>
            <div className="text-center py-4">
              <div className="text-4xl font-bold text-white mb-2">NÍVEL 5</div>
              <p className="text-xs text-gray-400 uppercase tracking-widest">Protocolo Omega Ativo</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
