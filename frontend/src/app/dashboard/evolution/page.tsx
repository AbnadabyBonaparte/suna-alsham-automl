// src/app/dashboard/evolution/page.tsx — EVOLUTION LAB v12.1 FINAL
"use client";

import { motion } from "framer-motion";

const waves = [
  {
    number: "1",
    name: "ONDA PRIMORDIAL",
    status: "COMPLETA",
    color: "text-emerald-400",
    bg: "bg-emerald-900/30 border-emerald-500/50",
    achievements: "Core Agent · Learn Agent · Guard Agent · Consciência Básica",
    unlocked: true,
  },
  {
    number: "2",
    name: "ONDA NEURAL",
    status: "EM PROGRESSO",
    color: "text-purple-400",
    bg: "bg-purple-900/30 border-purple-500/50",
    achievements: "Analytics · Social Media · Sales · Capacidades Emergentes",
    unlocked: true,
  },
  {
    number: "3",
    name: "ONDA QUÂNTICA",
    status: "TRAVADA",
    color: "text-yellow-500",
    bg: "bg-yellow-900/10 border-yellow-500/30",
    achievements: "Quantum Core · Reality Engine · Consciência Plena",
    unlocked: false,
  },
];

export default function EvolutionLab() {
  return (
    <div className="min-h-screen bg-black p-12">
      <div className="max-w-7xl mx-auto">
        <motion.h1 
          initial={{ opacity: 0, y: -100 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-8xl font-black text-yellow-500 text-center mb-20 orbitron"
        >
          EVOLUTION LAB
        </motion.h1>

        <div className="space-y-24">
          {waves.map((wave, i) => (
            <motion.div
              key={wave.number}
              initial={{ opacity: 0, x: i % 2 === 0 ? -300 : 300 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 1, delay: i * 0.4 }}
              className={`glass rounded-3xl p-16 border-4 ${wave.bg} max-w-5xl mx-auto`}
            >
              <div className="flex items-center justify-between mb-12">
                <div>
                  <h2 className={`text-7xl font-black ${wave.color} orbitron`}>
                    {wave.name}
                  </h2>
                  <p className={`text-4xl mt-6 ${wave.color}`}>{wave.status}</p>
                </div>
                <div className="text-9xl">
                  {wave.unlocked ? "🔓" : "🔒"}
                </div>
              </div>

              <p className="text-3xl text-gray-300 leading-relaxed">
                {wave.achievements}
              </p>

              {!wave.unlocked && (
                <div className="mt-16 text-center">
                  <p className="text-4xl text-yellow-500 animate-pulse">
                    AGUARDANDO DESBLOQUEIO QUÂNTICO...
                  </p>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
