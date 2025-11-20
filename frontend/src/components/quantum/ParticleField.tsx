"use client";

import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Points, PointMaterial } from "@react-three/drei";
import * as random from "maath/random/dist/maath-random.cjs";

function Stars(props: any) {
  const ref = useRef<any>();
  
  // Otimização e Blindagem Matemática
  const [sphere] = useMemo(() => {
    // Gera 5000 pontos numa esfera de raio 1.5
    // A blindagem garante que Float32Array seja usado corretamente
    const data = random.inSphere(new Float32Array(5000), { radius: 1.5 });
    
    // Verificação de Segurança: Remove NaNs (Blindagem contra erro do Three.js)
    for (let i = 0; i < data.length; i++) {
      if (isNaN(data[i])) data[i] = 0; 
    }
    
    return [data];
  }, []);

  useFrame((state, delta) => {
    if (ref.current) {
      ref.current.rotation.x -= delta / 10;
      ref.current.rotation.y -= delta / 15;
    }
  });

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      <Points ref={ref} positions={sphere} stride={3} frustumCulled={false} {...props}>
        <PointMaterial
          transparent
          color="#a855f7" // Roxo Neon
          size={0.002}
          sizeAttenuation={true}
          depthWrite={false}
        />
      </Points>
    </group>
  );
}

export default function ParticleField() {
  return (
    <div className="absolute inset-0 -z-10 h-full w-full bg-black">
      <Canvas camera={{ position: [0, 0, 1] }}>
        <Stars />
      </Canvas>
    </div>
  );
}
