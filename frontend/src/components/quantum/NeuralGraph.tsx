"use client";

import { useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Sphere, Line } from "@react-three/drei";

function Node({ position, color }: any) {
  const ref = useRef<any>();
  
  useFrame((state) => {
    // Animação leve baseada no tempo
    const t = state.clock.getElapsedTime();
    if (ref.current) {
      ref.current.scale.setScalar(1 + Math.sin(t * 1.5 + position[0]) * 0.15);
    }
  });

  return (
    <Sphere ref={ref} args={[0.15, 16, 16]} position={position}>
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={1.5} toneMapped={false} />
    </Sphere>
  );
}

function Connections({ nodes }: { nodes: any[] }) {
  // Otimização: Gera todas as linhas como um único objeto se possível, 
  // mas aqui manteremos Lines individuais por simplicidade visual, com geometria leve.
  const lines = useMemo(() => {
    const connections = [];
    for (let i = 0; i < nodes.length; i++) {
      // Conecta apenas aos vizinhos mais próximos para evitar caos visual
      const targets = nodes.slice(i + 1, i + 3); 
      for (const target of targets) {
        connections.push({ start: nodes[i].position, end: target.position });
      }
    }
    return connections;
  }, [nodes]);

  return (
    <>
      {lines.map((line, i) => (
        <Line
          key={i}
          points={[line.start, line.end]}
          color="white"
          lineWidth={0.5}
          transparent
          opacity={0.15}
        />
      ))}
    </>
  );
}

function Brain() {
  const agents = useMemo(() => {
    return new Array(57).fill(0).map(() => ({
      position: [
        (Math.random() - 0.5) * 8,
        (Math.random() - 0.5) * 8,
        (Math.random() - 0.5) * 8
      ] as [number, number, number],
      color: Math.random() > 0.6 ? "#a855f7" : Math.random() > 0.3 ? "#3b82f6" : "#22c55e"
    }));
  }, []);

  return (
    <group>
      {agents.map((agent, i) => (
        <Node key={i} position={agent.position} color={agent.color} />
      ))}
      <Connections nodes={agents} />
    </group>
  );
}

export default function NeuralGraph() {
  return (
    <div className="h-[calc(100vh-6rem)] w-full bg-black/50 relative overflow-hidden rounded-xl border border-white/10 backdrop-blur-sm">
      
      <div className="absolute top-4 left-4 z-10 pointer-events-none">
        <h2 className="text-2xl font-bold text-white/90 tracking-tight">Neural Nexus</h2>
        <div className="flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"/>
            <p className="text-xs text-purple-300 font-mono">57 Active Nodes • GPU Optimized</p>
        </div>
      </div>

      {/* Configurações Robustas de GPU */}
      <Canvas 
        camera={{ position: [0, 0, 12], fov: 50 }} 
        dpr={[1, 1.5]} // Limita resolução em telas retina para performance
        gl={{ 
            antialias: true, 
            powerPreference: "default",
            preserveDrawingBuffer: true 
        }}
      >
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <Brain />
        <OrbitControls 
            autoRotate 
            autoRotateSpeed={0.8} 
            enableZoom={true} 
            enablePan={false}
            maxDistance={20}
            minDistance={5}
        />
      </Canvas>
    </div>
  );
}
