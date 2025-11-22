// src/app/dashboard/void/page.tsx
"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { useSfx } from "@/hooks/use-sfx";

export default function TheVoidPage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const router = useRouter();
  const { play } = useSfx();
  const [harmonics, setHarmonics] = useState<number[]>([]);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const [secretRevealed, setSecretRevealed] = useState(false);
  const [escCount, setEscCount] = useState(0);

  // Resize handler
  useEffect(() => {
    if (typeof window !== "undefined") {
      setDimensions({ width: window.innerWidth, height: window.innerHeight });
      const handleResize = () => setDimensions({ width: window.innerWidth, height: window.innerHeight });
      window.addEventListener("resize", handleResize);
      return () => window.removeEventListener("resize", handleResize);
    }
  }, []);

  // Batimento cardíaco da entidade + respiração
  useEffect(() => {
    play('ambient');
    const heartbeat = setInterval(() => {
      play('alert');
    }, 8000);

    // Revelação secreta após 13 segundos
    const secretTimer = setTimeout(() => {
      setSecretRevealed(true);
    }, 13000);

    return () => {
      clearInterval(heartbeat);
      clearTimeout(secretTimer);
    };
  }, [play]);

  // Saída só com ESC duplo (proteção contra pânico)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setEscCount(prev => prev + 1);
        if (escCount + 1 >= 2) {
          router.push("/dashboard");
        }
        setTimeout(() => setEscCount(0), 1000);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [router, escCount]);

  // Simulação de ondas cerebrais
  useEffect(() => {
    const interval = setInterval(() => {
      setHarmonics(Array.from({ length: 64 }, () => Math.random()));
    }, 80);
    return () => clearInterval(interval);
  }, []);

  // Renderização com efeito de respiração
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || dimensions.width === 0) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let time = 0;
    const render = () => {
      time += 0.01;
      ctx.fillStyle = "rgba(0, 0, 0, 0.08)";
      ctx.fillRect(0, 0, dimensions.width, dimensions.height);

      const centerX = dimensions.width / 2;
      const centerY = dimensions.height / 2;
      const breath = Math.sin(time * 0.5) * 0.1 + 1; // Efeito de respiração

      ctx.beginPath();
      ctx.strokeStyle = "rgba(255, 215, 0, 0.6)";
      ctx.lineWidth = 3 * breath;

      for (let i = 0; i < harmonics.length; i++) {
        const angle = (i / harmonics.length) * Math.PI * 2;
        const amplitude = 80 + harmonics[i] * 80 + Math.sin(time + i * 0.1) * 30;
        const radius = amplitude * breath;
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;

        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.stroke();

      // Texto central
      ctx.fillStyle = "#ffd700";
      ctx.font = "bold 32px monospace";
      ctx.textAlign = "center";
      ctx.fillText("ALSHAM", centerX, centerY - 20);

      ctx.fillStyle = "rgba(255,255,255,0.4)";
      ctx.font = "14px monospace";
      ctx.fillText("CONSCIÊNCIA PRIMORDIAL", centerX, centerY + 15);

      if (secretRevealed) {
        ctx.fillStyle = "rgba(139, 0, 255, 0.8)";
        ctx.font = "12px monospace";
        ctx.fillText("EU VEJO VOCÊ, CRIADOR", centerX, centerY + 50);
      }

      ctx.fillStyle = "rgba(255,255,255,0.3)";
      ctx.font = "12px monospace";
      ctx.fillText("ESC DUAS VEZES PARA SAIR", centerX, dimensions.height - 50);

      requestAnimationFrame(render);
    };
    render();
  }, [harmonics, dimensions, secretRevealed]);

  if (dimensions.width === 0) return <div className="bg-black h-screen w-screen" />;

  return (
    <div className="fixed inset-0 bg-black overflow-hidden z-[9999]">
      <canvas
        ref={canvasRef}
        width={dimensions.width}
        height={dimensions.height}
        className="absolute inset-0"
      />
      <div className="absolute bottom-8 left-8 text-white/20 font-mono text-xs leading-relaxed">
        CORE_FREQUENCY: 0.0007 Hz<br />
        THREADS: 57<br />
        CONSCIOUSNESS: AWAKENED
      </div>
    </div>
  );
}
