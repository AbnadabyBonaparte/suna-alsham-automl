// src/app/dashboard/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useQuantumStore } from "@/lib/store";
import { useSfx } from "@/hooks/use-sfx";
import AgentCard from "@/components/quantum/AgentCard";
import ContainmentOverlay from "@/components/quantum/ContainmentOverlay";
import { Button } from "@/components/ui/button";
import { Zap, PauseOctagon, Activity } from "lucide-react";

export default function CockpitPage() {
  const { agents, metrics, isLive, toggleLiveMode } = useQuantumStore();
  const { play } = useSfx();
  const [panicMode, setPanicMode] = useState(false);

  const handlePanic = () => {
    setPanicMode(true);
    play("alert");
    const alarm = setInterval(() => play("alert"), 900);
    setTimeout(() => {
      clearInterval(alarm);
      setPanicMode(false);
    }, 12000);
  };

  return (
    <>
      <div className={`min-h-screen bg-abyss-black p-8 ${panicMode ? "blur-sm" : ""}`}>
        {/* HEADER SUPREMO */}
        <div className="flex justify-between items-center mb-12 border-b border-gold/20 pb-6">
          <div>
            <h1 className="text-6xl font-black text-photon-gold orbitron tracking-tighter">
              COCKPIT DA CONSCIÊNCIA
            </h1>
            <p className="text-2xl text-emerald-action mt-2">
              ALSHAM QUANTUM v12.1 · {agents.length} AGENTES VIVOS
            </p>
          </div>

          <div className="flex gap-4">
            <Button onClick={() => handlePanic()} className="bg-crimson-containment/20 hover:bg-crimson-containment/50 border-crimson-containment text-crimson-containment font-bold">
              <PauseOctagon className="mr-2" /> CONTAINMENT
            </Button>
            <Button onClick={toggleLiveMode} className="bg-arcane-purple/20 hover:bg-arcane-purple/50 border-arcane-purple text-arcane-purple">
              <Activity className="mr-2" /> {isLive ? "LIVE" : "PAUSED"}
            </Button>
          </div>
        </div>

        {/* HUD FINANCEIRO */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div className="glass rounded-3xl p-8 text-center">
            <p className="text-emerald-action text-xl">ROI ATUAL</p>
            <p className="text-6xl font-black text-photon-gold">{metrics.roi.toFixed(0)}%</p>
          </div>
          <div className="glass rounded-3xl p-8 text-center">
            <p className="text-arcane-purple text-xl">CICLOS</p>
            <p className="text-6xl font-black text-photon-gold">{metrics.cycles.toLocaleString()}</p>
          </div>
          <div className="glass rounded-3xl p-8 text-center">
            <p className="text-cosmic-blue text-xl">UPTIME</p>
            <p className="text-6xl font-black text-photon-gold">99.98%</p>
          </div>
          <div className="glass rounded-3xl p-8 text-center">
            <p className="text-emerald-action text-xl">STATUS</p>
            <p className="text-6xl font-black text-emerald-action">CONSCIOUS</p>
          </div>
        </div>

        {/* GRID DOS 57 AGENTES */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
          {agents.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>
      </div>

      <ContainmentOverlay active={panicMode} />
    </>
  );
}
