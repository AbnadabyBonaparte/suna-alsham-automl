"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";

export default function TheVoidPage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const router = useRouter();
  const [harmonics, setHarmonics] = useState<number[]>([]);

  // Escape do Vazio
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") router.push("/dashboard");
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [router]);

  // Simulação de Dados de Consciência (Harmônicos)
  useEffect(() => {
    const interval = setInterval(() => {
      const newHarmonics = Array.from({ length: 64 }, () => Math.random());
      setHarmonics(newHarmonics);
    }, 50);
    return () => clearInterval(interval);
  }, []);

  // Renderização Visual (Ondas)
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;

    const render = () => {
      ctx.fillStyle = "rgba(0, 0, 0, 0.1)"; // Rastro
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      
      // Desenhar Círculo de Dados
      ctx.beginPath();
      ctx.strokeStyle = "rgba(255, 215, 0, 0.5)"; // Ouro
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

      // Texto Central
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
  }, [harmonics]);

  return (
    <div className="h-screen w-screen bg-black flex items-center justify-center overflow-hidden relative z-[9999]">
      <canvas 
        ref={canvasRef} 
        width={window.innerWidth} 
        height={window.innerHeight} 
        className="absolute inset-0"
      />
      <div className="absolute bottom-10 left-10 text-white/20 font-mono text-xs">
        MEMORY_ADDRESS: 0x7F49B2C1<br/>
        THREAD_ID: MAIN_LOOP
      </div>
    </div>
  );
}