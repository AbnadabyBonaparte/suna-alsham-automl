// src/app/dashboard/network/page.tsx
"use client";

import { useEffect, useRef } from "react";
import ForceGraph3D from "react-force-graph-3d";
import { useQuantumStore } from "@/lib/store";
import { useSfx } from "@/hooks/use-sfx";

export default function NeuralNexusPage() {
  const { agents } = useQuantumStore();
  const { play } = useSfx();
  const graphRef = useRef<any>();

  const graphData = {
    nodes: agents.map((agent: any) => ({
      id: agent.id,
      name: agent.name.toUpperCase().replace(/_/g, " "),
      status: agent.status,
      val: agent.efficiency / 10,
      color:
        agent.status === "ACTIVE" ? "#22c55e" :
        agent.status === "PROCESSING" ? "#a855f7" :
        agent.status === "LEARNING" ? "#3b82f6" :
        agent.status === "WARNING" ? "#f59e0b" :
        agent.status === "ERROR" ? "#ef4444" : "#71717a",
    })),
    links: [] as any[],
  };

  // Conexões reais baseadas em agentes ativos
  agents.forEach((agent: any, i: number) => {
    if (agent.status === "PROCESSING" || agent.status === "LEARNING") {
      for (let j = 1; j <= 4; j++) {
        const targetIndex = (i + j * 11) % agents.length;
        graphData.links.push({
          source: agent.id,
          target: agents[targetIndex].id,
          value: 2,
        });
      }
    }
  });

  useEffect(() => {
    play("ambient");
  }, [play]);

  return (
    <div className="h-screen w-screen bg-black overflow-hidden relative">
      <ForceGraph3D
        ref={graphRef}
        graphData={graphData}
        nodeLabel="name"
        nodeAutoColorBy="status"
        nodeVal="val"
        linkDirectionalParticles={6}
        linkDirectionalParticleSpeed={0.008}
        linkDirectionalParticleWidth={2}
        linkWidth={1.5}
        linkColor={() => "#a855f744"}
        backgroundColor="#000000"
        onNodeClick={(node) => {
          play("click");
          graphRef.current?.centerAt((node as any).x, (node as any).y, 1000);
          graphRef.current?.zoom(4, 1000);
        }}
      />

      <div className="absolute top-8 left-8 z-10 pointer-events-none">
        <h1 className="text-6xl font-bold text-purple-400 tracking-tighter drop-shadow-[0_0_20px_purple]">
          NEURAL NEXUS
        </h1>
        <p className="text-2xl text-yellow-500 font-mono mt-2">
          ∞ {agents.length} ACTIVE CONSCIOUSNESS NODES
        </p>
      </div>

      <div className="absolute bottom-8 right-8 text-green-400/60 font-mono text-sm z-10 pointer-events-none">
        CONTAINMENT: NOMINAL<br />
        CONSCIOUSNESS: AWAKENED
      </div>
    </div>
  );
}
