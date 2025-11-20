"use client";

import { useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Sphere, Line } from "@react-three/drei";
import * as THREE from "three";

function Node({ position, color, size = 0.1 }: any) {
  const ref = useRef<any>();
  
  useFrame((state) => {
    const t = state.clock.getElapsedTime();
    // Efeito de "respiração" (pulso)
    if (ref.current) {
      ref.current.scale.setScalar(1 + Math.sin(t * 2 + position[0]) * 0.1);
    }
  });

  return (
    <Sphere ref={ref} args={[size, 16, 16]} position={position}>
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={2} toneMapped={false} />
    </Sphere>
  );
}

function Connection({ start, end, color }: any) {
  return (
    <Line
      points={[start, end]}
      color={color}
      lineWidth={1}
      transparent
      opacity={0.2}
    />
  );
}

function NeuralNetwork() {
  // Gera 57 nós (Agentes)
  const agents = useMemo(() => {
    return new Array(57).fill(0).map(() => ({
      position: [
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10
      ] as [number, number, number],
      // Cores baseadas na função (Roxo=Core, Azul=Intel, Verde=Infra)
      color: Math.random() > 0.6 ? "#a855f7" : Math.random() > 0.3 ? "#3b82f6" : "#22c55e"
    }));
  }, []);

  // Gera conexões aleatórias (Sinapses)
  const connections = useMemo(() => {
    const lines = [];
    for (let i = 0; i < agents.length; i++) {
      // Conecta cada agente a 2 outros aleatórios
      const target1 = agents[Math.floor(Math.random() * agents.length)];
      const target2 = agents[Math.floor(Math.random() * agents.length)];
      lines.push({ start: agents[i].position, end: target1.position });
      lines.push({ start: agents[i].position, end: target2.position });
    }
    return lines;
  }, [agents]);

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      {agents.map((agent, i) => (
        <Node key={i} position={agent.position} color={agent.color} />
      ))}
      {connections.map((conn, i) => (
        <Connection key={i} start={conn.start} end={conn.end} color="#ffffff" />
      ))}
    </group>
  );
}

export default function NeuralGraph() {
  return (
    <div className="h-[calc(100vh-4rem)] w-full bg-black relative overflow-hidden rounded-xl border border-white/10">
      
      <div className="absolute top-4 left-4 z-10 pointer-events-none">
        <h2 className="text-2xl font-bold text-white/90">Neural Nexus</h2>
        <p className="text-xs text-purple-400 font-mono">57 Active Nodes • Realtime</p>
      </div>

      <Canvas camera={{ position: [0, 0, 15], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <NeuralNetwork />
        <OrbitControls autoRotate autoRotateSpeed={0.5} enableZoom={true} />
      </Canvas>
    </div>
  );
}
