"use client";

import { useState, useEffect, useRef } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

const INITIAL_BOOT_SEQUENCE = [
  "Initializing ALSHAM Quantum Core v11.0...",
  "Loading neural pathways...",
  "Connecting to 57 active agents...",
  "Establishing secure handshake with Stripe...",
  "Syncing with Supabase cluster...",
  "System Status: ONLINE",
];

const MOCK_LOGS = [
  { type: "INFO", source: "CORE-V3", msg: "Optimizing neural weights for Sales Agent..." },
  { type: "SUCCESS", source: "STRIPE-OPS", msg: "Transaction verified: R$ 1.450,00 confirmed." },
  { type: "WARNING", source: "GUARD-SENTINEL", msg: "Anomaly detected in sector 7. Containment protocol active." },
  { type: "INFO", source: "WEB-SEARCH", msg: "Crawling competitors data [Depth: 3]..." },
  { type: "SUCCESS", source: "EVOLUTION-ENGINE", msg: "New capability unlocked: Advanced Pattern Recognition." },
  { type: "INFO", source: "ORCHESTRATOR", msg: "Rebalancing load: 45% -> 42% efficiency gain." },
];

export default function MatrixTerminal() {
  const [logs, setLogs] = useState<any[]>([]);
  const [booted, setBooted] = useState(false);
  const [showIntro, setShowIntro] = useState(true);
  const [introText, setIntroText] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  // Efeito 1: "Wake up, Bonaparte..."
  useEffect(() => {
    const text = "Wake up, Bonaparte... The ALSHAM has you.";
    let i = 0;
    const timer = setInterval(() => {
      setIntroText(text.substring(0, i));
      i++;
      if (i > text.length) {
        clearInterval(timer);
        setTimeout(() => {
            setShowIntro(false); // Sai da intro
            setBooted(true);     // Inicia o boot
        }, 2000);
      }
    }, 100); // Velocidade de digitação
    return () => clearInterval(timer);
  }, []);

  // Efeito 2: Boot Sequence
  useEffect(() => {
    if (!booted) return;
    
    let i = 0;
    const timer = setInterval(() => {
      if (i < INITIAL_BOOT_SEQUENCE.length) {
        setLogs(prev => [...prev, { type: "SYSTEM", source: "BOOT", msg: INITIAL_BOOT_SEQUENCE[i] }]);
        i++;
      } else {
        clearInterval(timer);
      }
    }, 300);
    return () => clearInterval(timer);
  }, [booted]);

  // Efeito 3: Live Logs (Simulação de WebSocket)
  useEffect(() => {
    if (!booted || logs.length < INITIAL_BOOT_SEQUENCE.length) return;

    const timer = setInterval(() => {
      const randomLog = MOCK_LOGS[Math.floor(Math.random() * MOCK_LOGS.length)];
      const timestamp = new Date().toLocaleTimeString();
      setLogs(prev => [...prev.slice(-50), { ...randomLog, timestamp }]); // Mantém últimos 50 logs
      
      // Auto-scroll
      if (scrollRef.current) {
        scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
      }
    }, 2000);

    return () => clearInterval(timer);
  }, [booted, logs.length]);

  // Renderização da Intro Cinematográfica
  if (showIntro) {
    return (
      <div className="h-full w-full flex items-center justify-center bg-black text-green-500 font-mono text-2xl md:text-4xl">
        <span className="animate-pulse">{introText}</span><span className="animate-blink">_</span>
      </div>
    );
  }

  // Renderização do Terminal
  return (
    <div className="h-full w-full bg-black border border-green-500/20 rounded-lg p-4 font-mono text-sm relative overflow-hidden shadow-[0_0_30px_rgba(34,197,94,0.1)]">
      {/* Scanline Effect */}
      <div className="absolute inset-0 bg-[linear-gradient(transparent_50%,rgba(0,0,0,0.25)_50%)] bg-[length:100%_4px] pointer-events-none z-10 opacity-20"></div>
      
      <div className="flex justify-between items-center border-b border-green-500/30 pb-2 mb-4">
         <h3 className="text-green-400 font-bold flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            LIVE KERNEL STREAM
         </h3>
         <Badge variant="outline" className="border-green-500/50 text-green-500">SECURE CONNECTION</Badge>
      </div>

      <div className="h-[calc(100%-3rem)] overflow-y-auto space-y-2 scrollbar-hide" ref={scrollRef}>
        {logs.map((log, i) => (
          <div key={i} className="flex gap-3 animate-in fade-in slide-in-from-bottom-1 duration-300">
            <span className="text-green-800">[{log.timestamp || "INIT"}]</span>
            <span className={`font-bold w-24 ${
                log.type === 'ERROR' ? 'text-red-500' : 
                log.type === 'WARNING' ? 'text-yellow-500' : 
                log.type === 'SUCCESS' ? 'text-blue-400' : 'text-green-600'
            }`}>
                {log.type}
            </span>
            <span className="text-green-700 w-32">@{log.source}:</span>
            <span className="text-green-400 flex-1">{log.msg}</span>
          </div>
        ))}
        <div className="animate-pulse text-green-500">_</div>
      </div>
    </div>
  );
}
