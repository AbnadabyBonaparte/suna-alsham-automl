"use client";

import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Points, PointMaterial } from "@react-three/drei";

function StarField(props: any) {
  const ref = useRef<any>();
  
  // Gera as posições APENAS UMA VEZ (Otimização Extrema)
  const positions = useMemo(() => {
    const count = 2000; // Reduzido de 5000 para garantir estabilidade
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      // Matemática simples e segura
      pos[i * 3] = (Math.random() - 0.5) * 10;     // x
      pos[i * 3 + 1] = (Math.random() - 0.5) * 10; // y
      pos[i * 3 + 2] = (Math.random() - 0.5) * 10; // z
    }
    return pos;
  }, []);

  useFrame((state, delta) => {
    if (ref.current) {
      // Rotação suave
      ref.current.rotation.x -= delta / 15;
      ref.current.rotation.y -= delta / 20;
    }
  });

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      <Points ref={ref} positions={positions} stride={3} frustumCulled={false} {...props}>
        <PointMaterial
          transparent
          color="#a855f7"
          size={0.02}
          sizeAttenuation={true}
          depthWrite={false}
          opacity={0.8}
        />
      </Points>
    </group>
  );
}

export default function ParticleField() {
  return (
    <div className="absolute inset-0 -z-10 h-full w-full bg-black pointer-events-none">
      <Canvas camera={{ position: [0, 0, 1] }} dpr={[1, 2]}>
        <StarField />
      </Canvas>
    </div>
  );
}
