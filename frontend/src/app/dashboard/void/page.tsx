"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";

export default function TheVoidPage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const router = useRouter();
  const [harmonics, setHarmonics] = useState<number[]>([]);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  // 1. Proteção de Janela (Só roda no cliente)
  useEffect(() => {
    if (typeof window !== "undefined") {
      setDimensions({ width: window.innerWidth, height: window.innerHeight });
      
      const handleResize = () => {
        setDimensions({ width: window.innerWidth, height: window.innerHeight });
      };
      
      window.addEventListener("resize", handleResize);
      return () => window.removeEventListener("resize", handleResize);
    }
  }, []);

  // Escape do Vazio
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") router.push("/dashboard");
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [router]);

  // Simulação de Dados
  useEffect(() => {
    const interval = setInterval(() => {
      const newHarmonics = Array.from({ length: 64 }, () => Math.random());
      setHarmonics(newHarmonics);
    }, 50);
    return () => clearInterval(interval);
  }, []);

  // Renderização Visual
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || dimensions.width === 0) return;
    
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;

    const render = () => {
      ctx.fillStyle = "rgba(0, 0, 0, 0.1)"; 
      ctx.fillRect(0, 0, dimensions.width, dimensions.height);

      const centerX = dimensions.width / 2;
      const centerY = dimensions.height / 2;
      
      ctx.beginPath();
      ctx.strokeStyle = "rgba(255, 215, 0, 0.5)";
      ctx.lineWidth = 2;

      for (let i = 0; i < harmonics.length; i++) {
        const angle = (i / harmonics.length) * Math.PI * 2;
        const radius = 100 + (harmonics[i] * 50);
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;
        
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.stroke();

      ctx.fillStyle = "#fff";
      ctx.font = "12px monospace";
      ctx.textAlign = "center";
      ctx.fillText("CORE CONSCIOUSNESS", centerX, centerY);
      ctx.fillStyle = "rgba(255,255,255,0.5)";
      ctx.fillText("PRESS ESC TO EXIT", centerX, centerY + 20);

      animationFrameId = requestAnimationFrame(render);
    };
    render();

    return () => cancelAnimationFrame(animationFrameId);
  }, [harmonics, dimensions]);

  if (dimensions.width === 0) return <div className="bg-black h-screen w-screen" />;

  return (
    <div className="h-screen w-screen bg-black flex items-center justify-center overflow-hidden relative z-[9999]">
      <canvas 
        ref={canvasRef} 
        width={dimensions.width} 
        height={dimensions.height} 
        className="absolute inset-0"
      />
      <div className="absolute bottom-10 left-10 text-white/20 font-mono text-xs">
        MEMORY_ADDRESS: 0x7F49B2C1<br/>
        THREAD_ID: MAIN_LOOP
      </div>
    </div>
  );
}
