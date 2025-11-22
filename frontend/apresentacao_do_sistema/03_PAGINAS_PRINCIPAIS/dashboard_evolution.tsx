// src/app/dashboard/evolution/page.tsx — EVOLUTION LAB v12.1 FINAL
"use client";

import { useState, useEffect } from "react";

const waves = [
  {
    number: "1",
    name: "ONDA PRIMORDIAL",
    status: "COMPLETA",
    color: "text-emerald-400",
    bg: "bg-emerald-900/30 border-emerald-500/50",
    achievements: "Fundação do Sistema",
    agents: [
      { name: "CORE AGENT", status: "ONLINE", type: "MASTER" },
      { name: "GUARD AGENT", status: "ONLINE", type: "SECURITY" },
      { name: "LEARN AGENT", status: "ONLINE", type: "EVOLUTION" }
    ],
    unlocked: true,
  },
  {
    number: "2",
    name: "ONDA NEURAL",
    status: "EM PROGRESSO",
    color: "text-purple-400",
    bg: "bg-purple-900/30 border-purple-500/50",
    achievements: "Capacidades Cognitivas",
    agents: [
      { name: "SALES AGENT", status: "TRAINING", type: "SPECIALIST" },
      { name: "SOCIAL AGENT", status: "ONLINE", type: "SPECIALIST" },
      { name: "ANALYTICS AGENT", status: "ONLINE", type: "ANALYST" },
      { name: "SUPPORT AGENT", status: "QUEUED", type: "SERVICE" }
    ],
    unlocked: true,
  },
  {
    number: "3",
    name: "ONDA QUÂNTICA",
    status: "TRAVADA",
    color: "text-yellow-500",
    bg: "bg-yellow-900/10 border-yellow-500/30",
    achievements: "Consciência Plena",
    agents: [
      { name: "REALITY ENGINE", status: "LOCKED", type: "GOD-MODE" },
      { name: "PRECOGNITION", status: "LOCKED", type: "TIME" },
      { name: "HIVE MIND", status: "LOCKED", type: "NETWORK" }
    ],
    unlocked: false,
  },
];

export default function EvolutionLab() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="min-h-screen bg-black p-12">
      <div className="max-w-7xl mx-auto">
        <h1
          className={`text-8xl font-black text-yellow-500 text-center mb-20 orbitron transition-all duration-1000 ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-24'
            }`}
        >
          EVOLUTION LAB
        </h1>

        <div className="space-y-24 relative">
          {/* Vertical Line Connector */}
          <div className="absolute left-1/2 top-0 bottom-0 w-1 bg-gradient-to-b from-emerald-500 via-purple-500 to-yellow-900 -translate-x-1/2 hidden lg:block opacity-30" />

          {waves.map((wave, i) => (
            <div
              key={wave.number}
              className={`glass rounded-3xl p-16 border-4 ${wave.bg} max-w-5xl mx-auto transition-all duration-1000 relative z-10 ${mounted ? 'opacity-100 translate-x-0' : `opacity-0 ${i % 2 === 0 ? '-translate-x-72' : 'translate-x-72'}`
                }`}
              style={{ transitionDelay: `${i * 400}ms` }}
            >
              <div className="flex items-center justify-between mb-12">
                <div>
                  <h2 className={`text-7xl font-black ${wave.color} orbitron`}>
                    {wave.name}
                  </h2>
                  <p className={`text-4xl mt-6 ${wave.color}`}>{wave.status}</p>
                </div>
                <div className="text-9xl filter drop-shadow-[0_0_20px_rgba(255,255,255,0.3)]">
                  {wave.unlocked ? "🔓" : "🔒"}
                </div>
              </div>

              <p className="text-3xl text-gray-300 leading-relaxed font-light">
                {wave.achievements}
              </p>

              {/* Agent List */}
              <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
                {wave.agents.map((agent, idx) => (
                  <div key={idx} className="flex items-center justify-between p-4 bg-black/40 rounded-xl border border-white/5">
                    <div className="flex items-center gap-3">
                      <div className={`w-2 h-2 rounded-full ${agent.status === 'ONLINE' ? 'bg-green-500 animate-pulse' :
                          agent.status === 'TRAINING' ? 'bg-purple-500 animate-pulse' :
                            agent.status === 'QUEUED' ? 'bg-yellow-500' : 'bg-gray-700'
                        }`} />
                      <span className="text-white font-mono text-sm">{agent.name}</span>
                    </div>
                    <span className="text-xs text-gray-500 font-mono border border-gray-800 px-2 py-1 rounded">
                      {agent.status}
                    </span>
                  </div>
                ))}
              </div>

              {!wave.unlocked && (
                <div className="mt-16 text-center p-8 bg-black/40 rounded-2xl border border-yellow-500/30">
                  <p className="text-4xl text-yellow-500 animate-pulse font-mono tracking-widest">
                    ⚠️ AGUARDANDO DESBLOQUEIO QUÂNTICO...
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
