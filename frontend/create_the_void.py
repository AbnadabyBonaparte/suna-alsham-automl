import os

# 1. PÁGINA DO VAZIO (Visualização de Áudio/Dados)
void_page = """
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
"""

# 2. COMPONENTE DE ESCUTA GLOBAL (Klaatu Listener)
# Este componente será injetado no Layout principal para funcionar em qualquer lugar
listener_component = """
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const SECRET_CODE = "klaatu";

export function GlobalKeyListener() {
  const router = useRouter();
  const [inputBuffer, setInputBuffer] = useState("");

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Adiciona a tecla ao buffer (apenas letras)
      if (/^[a-zA-Z]$/.test(e.key)) {
        setInputBuffer((prev) => {
          const newBuffer = (prev + e.key.toLowerCase()).slice(-SECRET_CODE.length);
          
          if (newBuffer === SECRET_CODE) {
            console.log("👁️ O VAZIO TE CHAMA...");
            router.push("/dashboard/void");
          }
          
          return newBuffer;
        });
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [router]);

  return null; // Componente invisível
}
"""

# FUNÇÃO DE ESCRITA
def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Criado: {path}")
    except Exception as e:
        print(f"❌ Erro: {e}")

print("🕳️ Abrindo portal para o Vazio...")
write_file("src/app/dashboard/void/page.tsx", void_page)
write_file("src/components/layout/GlobalKeyListener.tsx", listener_component)
print("🏁 Portal configurado.")
