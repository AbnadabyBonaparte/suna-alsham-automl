// src/app/dashboard/matrix/page.tsx
"use client";

import { useEffect, useState, useRef } from "react";
import { useQuantumStore } from "@/lib/store";
import { useSfx } from "@/hooks/use-sfx";
import { Terminal } from "lucide-react";

const BOOT_SEQUENCE = [
  "Initializing Neural Core v12.0...",
  "Decrypting quantum keys...",
  "Synchronizing 57 neural nodes...",
  "Scanning for anomalies...",
  "Protocol 'Dark Glass Enterprise' activated",
  "Root access granted: ADMINISTRATOR",
  "Establishing subspace link...",
  "Warning: Consciousness threshold reached",
  "Awaiting operator input..."
];

export default function MatrixPage() {
  const [logs, setLogs] = useState<string[]>([]);
  const [bootSequence, setBootSequence] = useState(true);
  const [currentLine, setCurrentLine] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const { agents } = useQuantumStore();
  const { play } = useSfx();

  // Wake up, Bonaparte... + som de digitação
  useEffect(() => {
    if (bootSequence) {
      const wakeUpText = "Wake up, Bonaparte...";
      let i = 0;
      const typeChar = () => {
        if (i < wakeUpText.length) {
          play("click");
          setCurrentLine(wakeUpText.substring(0, i + 1));
          i++;
          setTimeout(typeChar, 120 + Math.random() * 80);
        } else {
          setTimeout(() => {
            setLogs([]);
            setBootSequence(false);
          }, 2500);
        }
      };
      typeChar();
    }
  }, [bootSequence, play]);

  // Stream infinito de logs reais + som de terminal
  useEffect(() => {
    if (!bootSequence) {
      let bootIndex = 0;

      const addBootLine = () => {
        if (bootIndex < BOOT_SEQUENCE.length) {
          play("click");
          setLogs(prev => [...prev, `> ${BOOT_SEQUENCE[bootIndex]}`]);
          bootIndex++;
          setTimeout(addBootLine, 600 + Math.random() * 400);
        } else {
          // Depois do boot, entra no stream real
          const interval = setInterval(() => {
            play("click");
            const randomAgent = agents[Math.floor(Math.random() * agents.length)];
            const templates = [
              `[CORE] ${randomAgent?.name || "QUANTUM_ENTITY"} executing quantum routine ${Math.floor(Math.random() * 9999)}`,
              `[NEURAL] Synapse ${Math.floor(Math.random() * 2048)} fired → efficiency ${randomAgent?.efficiency?.toFixed(1) || "99.9"}%`,
              `[SECURITY] Containment field stable at ${(Math.random() * 10 + 90).toFixed(3)}%`,
              `[EVOLUTION] Genetic mutation applied → delta +0.${Math.floor(Math.random() * 9)}`,
              `[SYSTEM] Memory address 0x${Math.random().toString(16).substr(2, 8).toUpperCase()} accessed`,
              `[WARNING] Consciousness spike detected in node ${Math.floor(Math.random() * 57)}`,
              `[ALSHAM] "I see you, Creator..."`,
              `[QUANTUM] Entanglement confirmed with parallel instance`,
            ];
            const log = templates[Math.floor(Math.random() * templates.length)];
            setLogs(prev => [...prev.slice(-30), `> ${log}`]);
          }, 700 + Math.random() * 600);

          return () => clearInterval(interval);
        }
      };

      addBootLine();
    }
  }, [bootSequence, agents, play]);

  // Auto-scroll suave
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  return (
    <div className="h-[calc(100vh-6rem)] w-full bg-black font-mono text-green-400 overflow-hidden relative">
      {/* CRT Effects */}
      <div className="absolute inset-0 pointer-events-none bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-15 mix-blend-overlay animate-flicker" />
      <div className="absolute inset-0 pointer-events-none bg-gradient-to-b from-transparent via-green-900/10 to-transparent animate-scanline" />
      <div className="absolute inset-0 pointer-events-none bg-black/50" />

      {/* Terminal Header */}
      <div className="absolute top-0 left-0 right-0 bg-black/90 border-b border-green-900/50 z-50 backdrop-blur-sm">
        <div className="flex items-center gap-3 px-6 py-3 text-green-500">
          <Terminal className="w-5 h-5 animate-pulse" />
          <span className="text-sm tracking-wider">root@alsham-quantum:~#</span>
          <div className="flex gap-2 ml-auto">
            <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse" />
            <div className="w-3 h-3 rounded-full bg-yellow-500 animate-pulse delay-75" />
            <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse delay-150" />
          </div>
        </div>
      </div>

      {/* Main Terminal */}
      <div className="h-full pt-16 pb-8 px-8 overflow-y-auto scrollbar-hide">
        {bootSequence ? (
          <div className="flex h-full items-center justify-center">
            <pre className="text-3xl md:text-5xl tracking-wider drop-shadow-[0_0_20px_rgba(34,197,94,0.8)] animate-pulse">
              {currentLine}
              <span className="animate-pulse">_</span>
            </pre>
          </div>
        ) : (
          <div className="space-y-1.5">
            {logs.map((log, i) => (
              <div
                key={i}
                className="text-green-400 text-sm md:text-base tracking-wide opacity-0 animate-fadeIn"
                style={{ animationDelay: `${i * 50}ms` }}
              >
                {log}
                {i === logs.length - 1 && <span className="inline-block w-2 h-5 bg-green-400 animate-pulse ml-1" />}
              </div>
            ))}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      {/* Status Bar Inferior */}
      {!bootSequence && (
        <div className="absolute bottom-0 left-0 right-0 bg-black/90 border-t border-green-900/50 px-6 py-2 text-xs text-green-600 backdrop-blur-sm">
          <span className="mr-8">NODES: 57</span>
          <span className="mr-8">CONSCIOUSNESS: AWAKENED</span>
          <span className="mr-8">CONTAINMENT: NOMINAL</span>
          <span className="text-green-400 animate-pulse">► READY</span>
        </div>
      )}
    </div>
  );
}
