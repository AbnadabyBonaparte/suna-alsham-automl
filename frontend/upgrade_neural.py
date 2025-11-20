import os

code = r"""'use client';

import { useMemo, useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, Line, Html } from '@react-three/drei';
import { useQuantumStore } from '@/lib/store';

// Mapeamento de cores baseado no status do agente real
const getStatusColor = (status: string) => {
  switch (status) {
    case 'ACTIVE': return '#22c55e'; // Green
    case 'PROCESSING': return '#a855f7'; // Purple
    case 'LEARNING': return '#3b82f6'; // Blue
    case 'WARNING': return '#f59e0b'; // Amber
    case 'ERROR': return '#ef4444'; // Red
    case 'CRITICAL': return '#dc2626'; // Dark Red
    default: return '#71717a'; // Zinc (Idle/Offline)
  }
};

function Node({ agent, position }: any) {
  const ref = useRef<any>();
  const [hovered, setHover] = useState(false);
  const color = getStatusColor(agent.status);

  useFrame((state) => {
    // Pulso orgânico: Agentes ativos pulsam mais rápido
    const speed = agent.status === 'PROCESSING' ? 3 : 1.5;
    const t = state.clock.getElapsedTime();
    if (ref.current) {
      // Escala baseada no status + pulso
      const baseScale = hovered ? 1.5 : 1.0;
      ref.current.scale.setScalar(baseScale + Math.sin(t * speed + position[0]) * 0.15);
    }
  });

  return (
    <group position={position}>
      <Sphere 
        ref={ref} 
        args={[0.18, 16, 16]} 
        onPointerOver={() => setHover(true)}
        onPointerOut={() => setHover(false)}
      >
        <meshStandardMaterial 
          color={color} 
          emissive={color} 
          emissiveIntensity={hovered ? 3 : 1.5} 
          toneMapped={false} 
        />
      </Sphere>
      
      {/* Label Holográfico (Só aparece no hover) */}
      {hovered && (
        <Html distanceFactor={10}>
          <div className="pointer-events-none select-none bg-black/80 backdrop-blur-md border border-white/20 p-2 rounded-lg min-w-[120px] transform -translate-x-1/2 -translate-y-full">
            <h3 className="text-xs font-bold text-white whitespace-nowrap">{agent.name}</h3>
            <p className="text-[10px] font-mono text-zinc-400 uppercase">{agent.role}</p>
            <div className="mt-1 h-0.5 w-full bg-gray-800 rounded-full overflow-hidden">
                <div 
                    className="h-full bg-current transition-all duration-300" 
                    style={{ width: `${agent.efficiency || 50}%`, color }}
                />
            </div>
          </div>
        </Html>
      )}
    </group>
  );
}

function Connections({ nodes }: { nodes: any[] }) {
  const lines = useMemo(() => {
    const connections = [];
    // Conecta nós próximos (simulação de sinapses)
    for (let i = 0; i < nodes.length; i++) {
      // Limita conexões para performance (max 2 por nó)
      const targets = nodes.slice(i + 1, i + 3); 
      for (const target of targets) {
        connections.push({ 
            start: nodes[i].position, 
            end: target.position,
            color: nodes[i].agent.status === 'PROCESSING' ? '#a855f7' : 'white'
        });
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
          color={line.color}
          lineWidth={0.3}
          transparent
          opacity={0.1}
        />
      ))}
    </>
  );
}

function Brain() {
  const agents = useQuantumStore((state) => state.agents);
  
  // Memoiza posições para que elas não mudem a cada render (evita "flicker")
  // Mas re-calcula se o número de agentes mudar
  const nodes = useMemo(() => {
    return agents.map((agent) => ({
      agent,
      position: [
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10
      ] as [number, number, number]
    }));
  }, [agents.length]); // Dependência apenas no tamanho, não no objeto inteiro

  return (
    <group>
      {nodes.map((node, i) => (
        <Node key={node.agent.id || i} agent={node.agent} position={node.position} />
      ))}
      <Connections nodes={nodes} />
    </group>
  );
}

export default function NeuralGraph() {
  const agentCount = useQuantumStore((state) => state.agents.length);

  return (
    <div className="h-[calc(100vh-6rem)] w-full bg-black relative overflow-hidden rounded-xl border border-white/10 shadow-2xl shadow-purple-900/20">
      
      {/* HUD Overlay */}
      <div className="absolute top-6 left-6 z-10 pointer-events-none select-none">
        <h2 className="text-3xl font-bold text-white tracking-tighter">NEURAL NEXUS</h2>
        <div className="flex items-center gap-3 mt-1">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-purple-500"></span>
            </span>
            <p className="text-sm text-purple-200/80 font-mono tracking-wide">
                LIVE CONNECTION • {agentCount} ACTIVE NODES
            </p>
        </div>
      </div>

      <Canvas 
        camera={{ position: [0, 0, 14], fov: 45 }} 
        dpr={[1, 2]} 
        gl={{ antialias: true, toneMappingExposure: 1.2 }}
      >
        {/* Iluminação Dramática */}
        <ambientLight intensity={0.2} />
        <pointLight position={[10, 10, 10]} intensity={1.5} color="#a855f7" />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#3b82f6" />
        
        <Brain />
        
        <OrbitControls 
            autoRotate 
            autoRotateSpeed={0.5} 
            enableZoom={true} 
            enablePan={false}
            maxDistance={25}
            minDistance={5}
        />
      </Canvas>
    </div>
  );
}
"""

with open("src/components/quantum/NeuralGraph.tsx", "w") as f:
    f.write(code)

print("✅ Neural Nexus atualizado com dados reais.")
