import os

code = r"""'use client';

import { useEffect, useState, useRef } from 'react';
import { useQuantumStore } from '@/lib/store';

const LOG_Stream = [
  "Conectando ao Neural Core v11...",
  "Descriptografando chaves quânticas...",
  "Sincronizando 57 nós neurais...",
  "Buscando padrões de anomalia...",
  "Protocolo 'Dark Glass' ativado.",
  "Acesso concedido: Nível Administrador.",
  "Monitorando frequências subespaciais...",
  "Aguardando input do Operador..."
];

export default function MatrixPage() {
  const [logs, setLogs] = useState<string[]>([]);
  const [bootSequence, setBootSequence] = useState(true);
  const bottomRef = useRef<HTMLDivElement>(null);
  const { agents } = useQuantumStore();

  // Efeito "Wake up, Neo"
  useEffect(() => {
    let timeout: NodeJS.Timeout;
    
    if (bootSequence) {
      const introText = "Wake up, Bonaparte...";
      let charIndex = 0;
      
      const typeWriter = () => {
        if (charIndex < introText.length) {
          setLogs(prev => [introText.substring(0, charIndex + 1)]);
          charIndex++;
          timeout = setTimeout(typeWriter, 100);
        } else {
          setTimeout(() => {
             setLogs([]);
             setBootSequence(false);
          }, 2000);
        }
      };
      typeWriter();
    } else {
      // Stream contínuo de dados
      let index = 0;
      const interval = setInterval(() => {
        const newLog = index < LOG_Stream.length 
          ? LOG_Stream[index] 
          : `[SYSTEM] Agente ${agents[Math.floor(Math.random() * agents.length)]?.name || 'GHOST'} processando bloco ${Math.floor(Math.random() * 9999)}`;
        
        setLogs(prev => [...prev.slice(-20), `> ${newLog}`]);
        index++;
      }, 800);
      
      return () => clearInterval(interval);
    }

    return () => clearTimeout(timeout);
  }, [bootSequence, agents]);

  // Auto-scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="h-[calc(100vh-6rem)] w-full bg-black font-mono p-6 overflow-hidden relative border border-green-900/30 rounded-lg shadow-[0_0_50px_rgba(0,255,0,0.1)]">
      {/* CRT Overlay Effect */}
      <div className="absolute inset-0 pointer-events-none bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10 mix-blend-overlay"></div>
      <div className="absolute inset-0 pointer-events-none bg-gradient-to-b from-transparent via-green-900/5 to-green-900/10 animate-scanline"></div>

      <div className="h-full overflow-y-auto scrollbar-hide space-y-2 z-10 relative">
        {logs.map((log, i) => (
          <div key={i} className="text-green-500 text-sm md:text-base tracking-wider drop-shadow-[0_0_5px_rgba(34,197,94,0.8)]">
            {log}
            {i === logs.length - 1 && <span className="animate-pulse ml-1">_</span>}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
"""

with open("src/app/dashboard/matrix/page.tsx", "w") as f:
    f.write(code)

print("✅ Matrix atualizada com Protocolo 'Wake Up'.")
