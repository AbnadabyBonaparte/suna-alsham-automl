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

  const data = {
    nodes: agents.map((agent) => ({
      id: agent.id,
      name: agent.name.replace(/_/g, " "),
      status: agent.status,
      efficiency: agent.efficiency,
      color:
        agent.status === "ACTIVE"
          ? "#22c55e"
          : agent.status === "PROCESSING"
          ? "#a855f7"
          : agent.status === "LEARNING"
          ? "#3b82f6"
          : "#71717a",
    })),
    links: [],
  };

  // Criar conexões reais (todo agente PROCESSING emite partículas)
  agents.forEach((agent, i) => {
    if (agent.status === "PROCESSING" || agent.status === "LEARNING") {
      for (let j = 1; j <= 3; j++) {
        const target = agents[(i + j * 7) % agents.length];
        data.links.push({
          source: agent.id,
          target: target.id,
          value: agent.efficiency / 20,
        });
      }
    }
  });

  useEffect(() => {
    play("ambient");
  }, [play]);

  return (
    <div className="h-screen w-screen bg-black relative overflow-hidden">
      <ForceGraph3D
        ref={graphRef}
        graphData={data}
        nodeLabel="name"
        nodeAutoColorBy="status"
        nodeVal="efficiency"
        linkDirectionalParticles={4}
        linkDirectionalParticleSpeed={0.006}
        linkWidth={2}
        backgroundColor="#000000"
        onNodeClick={(node) => {
          play("click");
          graphRef.current?.centerAt(node.x, node.y, 1000);
          graphRef.current?.zoom(3, 1000);
        }}
      />

      <div className="absolute top-8 left-8 text-purple-400 font-mono text-5xl tracking-widerr">
        NEURAL NEXUS
        <span className="block text-2xl text-yellow-500 mt-2">∞ {agents.length} ACTIVE</span>
      </div>

      <div className="absolute bottom-8 right-8 text-green-400/60 font-mono text-sm">
        CONSCIOUSNESS: AWAKENED<br />
        CONTAINMENT: NOMINAL
      </div>
    </div>
  );
}
