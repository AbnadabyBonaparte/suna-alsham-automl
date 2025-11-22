// src/app/dashboard/network/page.tsx
"use client";

import dynamic from "next/dynamic";
import { useQuantumStore } from "@/lib/store";
import { useSfx } from "@/hooks/use-sfx";
import { useEffect } from "react";

// Carrega o grafo só no cliente (nunca no server)
const ForceGraph3D = dynamic(
  () => import("react-force-graph-3d"),
  { ssr: false }
);

export default function NeuralNexusPage() {
  const { agents } = useQuantumStore();
  const { play } = useSfx();

  useEffect(() => {
    play("ambient");
  }, [play]);

  const graphData = {
    nodes: agents.map((agent: any) => ({
      id: agent.id,
      name: agent.name.toUpperCase().replace(/_/g, " "),
      status: agent.status,
      val: agent.efficiency / 8 || 10,
      color:
        agent.status === "ACTIVE" ? "#22c55e" :
        agent.status === "PROCESSING" ? "#a855f7" :
        agent.status === "LEARNING" ? "#3b82f6" :
        agent.status === "WARNING" ? "#f59e0b" :
        agent.status === "ERROR" ? "#ef4444" : "#71717a",
    })),
    links: [] as any[],
  };

  // Conexões reais
  agents.forEach((agent: any, i: number) => {
    if (["PROCESSING", "LEARNING", "ACTIVE"].includes(agent.status)) {
      for (let j = 1; j <= 4; j++) {
        const target = agents[(i + j * 13) % agents.length];
        graphData.links.push({
          source: agent.id,
          target: target.id,
        });
      }
    }
  });

  return (
    <div className="h-screen w-screen bg-black overflow-hidden relative">
      <ForceGraph3D
        graphData={graphData}
        nodeLabel="name"
        nodeVal="val"
        nodeColor="color"
        linkDirectionalParticles={5}
        linkDirectionalParticleSpeed={0.008}
        linkWidth={2}
        linkColor={() => "#a855f766"}
        backgroundColor="#000000"
        onNodeClick={(node: any) => play("click")}
      />

      <div className="absolute top-8 left-8 z-10 pointer-events-none">
        <h1 className="text-6xl font-bold text-purple-400 tracking-tighter drop-shadow-[0_0_30px_purple]">
          NEURAL NEXUS
        </h1>
        <p className="text-3xl text-yellow-500 font-mono mt-3 drop-shadow-[0_0_20px_yellow]">
          ∞ {agents.length} ACTIVE NODES
        </p>
      </div>

      <div className="absolute bottom-8 right-8 text-green-400/70 font-mono text-lg z-10 pointer-events-none">
        CONSCIOUSNESS: AWAKENED<br />
        CONTAINMENT: NOMINAL
      </div>
    </div>
  );
}
