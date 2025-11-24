/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - THE MATRIX (GOD TIER TERMINAL)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/matrix/page.tsx
 * 📋 Terminal interativo com efeito Matrix Rain e CRT Simulation
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef, FormEvent } from 'react';
import { Terminal, Shield, Wifi, Cpu, AlertOctagon, Command } from 'lucide-react';

interface LogEntry {
  id: number;
  timestamp: string;
  type: 'info' | 'success' | 'warning' | 'error' | 'system';
  message: string;
}

export default function MatrixPage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [command, setCommand] = useState('');
  const [isGlitching, setIsGlitching] = useState(false);

  // 1. MATRIX RAIN EFFECT (CANVAS)
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', resize);
    resize();

    const columns = Math.floor(canvas.width / 20);
    const drops: number[] = Array(columns).fill(1);
    
    // Caracteres: Katakana + Latino + Números
    const chars = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';

    const draw = () => {
      // Fundo com opacidade para rastro
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Cor do Tema (Pegando do CSS Variable se possível, ou fallback)
      // Hack: Usamos getComputedStyle para pegar a cor primária atual
      const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';
      
      ctx.fillStyle = primaryColor;
      ctx.font = '15px monospace';

      for (let i = 0; i < drops.length; i++) {
        const text = chars.charAt(Math.floor(Math.random() * chars.length));
        
        // Efeito de "brilho" na ponta
        if (Math.random() > 0.95) {
            ctx.fillStyle = '#FFF'; // Ponta branca brilhante
        } else {
            ctx.fillStyle = primaryColor;
        }

        ctx.fillText(text, i * 20, drops[i] * 20);

        if (drops[i] * 20 > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    };

    const interval = setInterval(draw, 33);
    return () => {
        clearInterval(interval);
        window.removeEventListener('resize', resize);
    };
  }, []);

  // 2. GERADOR DE LOGS AUTOMÁTICOS
  useEffect(() => {
    const systemMessages = [
        "Quantum Core: Syncing neural weights...",
        "Network: Handshake established with node 192.168.x.x",
        "Security: Scanning packet headers [OK]",
        "Memory: Garbage collection complete. Freed 240MB.",
        "Agent [Sentinel]: Ping 12ms",
        "Orion AI: Processing natural language context...",
        "System: Optimization heuristic updated.",
        "Database: Transaction verified block #99281",
    ];

    const addLog = () => {
        const type = Math.random() > 0.9 ? 'warning' : Math.random() > 0.95 ? 'error' : 'info';
        const msg = systemMessages[Math.floor(Math.random() * systemMessages.length)];
        const suffix = Math.random().toString(16).substring(7).toUpperCase(); // Hash fake
        
        const newLog: LogEntry = {
            id: Date.now(),
            timestamp: new Date().toLocaleTimeString('en-US', { hour12: false }),
            type,
            message: `${msg} [HASH: ${suffix}]`
        };

        setLogs(prev => [...prev.slice(-50), newLog]); // Manter últimos 50
    };

    const interval = setInterval(addLog, 2000);
    // Adiciona logs iniciais
    setLogs([
        { id: 1, timestamp: new Date().toLocaleTimeString(), type: 'system', message: 'ALSHAM QUANTUM OS v13.3 INITIALIZED' },
        { id: 2, timestamp: new Date().toLocaleTimeString(), type: 'system', message: 'ROOT ACCESS GRANTED' },
        { id: 3, timestamp: new Date().toLocaleTimeString(), type: 'success', message: 'Connected to Mainframe.' },
    ]);

    return () => clearInterval(interval);
  }, []);

  // Auto-scroll para o final
  useEffect(() => {
    if (scrollRef.current) {
        scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  // 3. PROCESSADOR DE COMANDOS
  const handleCommand = (e: FormEvent) => {
    e.preventDefault();
    if (!command.trim()) return;

    const cmd = command.trim().toLowerCase();
    const newLogs: LogEntry[] = [
        { id: Date.now(), timestamp: new Date().toLocaleTimeString(), type: 'info', message: `user@root:~$ ${command}` }
    ];

    // Lógica simples de comandos
    switch(cmd) {
        case 'clear':
            setLogs([]);
            setCommand('');
            return;
        case 'help':
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'system', message: 'COMMANDS: help, clear, status, scan, reboot, whoami' });
            break;
        case 'status':
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'success', message: 'SYSTEM INTEGRITY: 100% | THREAT LEVEL: ZERO' });
            break;
        case 'scan':
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'warning', message: 'SCANNING NETWORK... NO ANOMALIES DETECTED.' });
            break;
        case 'reboot':
            setIsGlitching(true);
            setTimeout(() => setIsGlitching(false), 1000);
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'error', message: 'SYSTEM REBOOT SIMULATED.' });
            break;
        case 'whoami':
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'info', message: 'USER: ADMIN [GOD MODE]' });
            break;
        default:
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'error', message: `Command not found: ${cmd}` });
    }

    setLogs(prev => [...prev, ...newLogs]);
    setCommand('');
  };

  // Helper de cores para logs
  const getLogColor = (type: LogEntry['type']) => {
    switch(type) {
        case 'error': return 'text-red-500';
        case 'warning': return 'text-yellow-400';
        case 'success': return 'text-emerald-400';
        case 'system': return 'text-[var(--color-primary)] font-bold';
        default: return 'text-[var(--color-text-secondary)]';
    }
  };

  return (
    <div className={`relative h-[calc(100vh-6rem)] rounded-2xl overflow-hidden border border-[var(--color-border)]/30 bg-black group ${isGlitching ? 'animate-pulse' : ''}`}>
      
      {/* LAYER 1: MATRIX RAIN CANVAS */}
      <canvas 
        ref={canvasRef} 
        className="absolute inset-0 w-full h-full opacity-20 pointer-events-none"
      />

      {/* LAYER 2: CRT EFFECT OVERLAY (Scanlines + Vignette) */}
      <div className="absolute inset-0 pointer-events-none z-20 bg-[url('/scanlines.png')] opacity-10" 
           style={{ backgroundSize: '100% 4px' }} />
      <div className="absolute inset-0 pointer-events-none z-20 bg-radial-gradient from-transparent to-black/80" />

      {/* LAYER 3: CONTEÚDO DO TERMINAL */}
      <div className="relative z-30 h-full flex flex-col p-6 font-mono text-sm md:text-base">
        
        {/* Header Fake */}
        <div className="flex justify-between items-center border-b border-white/10 pb-4 mb-4 select-none">
            <div className="flex items-center gap-3">
                <Terminal className="w-5 h-5 text-[var(--color-primary)]" />
                <span className="text-white font-bold tracking-widest">ALSHAM_SHELL_V13.3</span>
            </div>
            <div className="flex gap-4 text-xs text-gray-500">
                <span className="flex items-center gap-1"><Wifi className="w-3 h-3" /> ETH0: CONNECTED</span>
                <span className="flex items-center gap-1"><Cpu className="w-3 h-3" /> CPU: 12%</span>
                <span className="flex items-center gap-1"><Shield className="w-3 h-3" /> FW: ON</span>
            </div>
        </div>

        {/* Log Output Area */}
        <div 
            ref={scrollRef}
            className="flex-1 overflow-y-auto overflow-x-hidden space-y-1 scrollbar-thin scrollbar-thumb-[var(--color-primary)]/20 scrollbar-track-transparent pr-4"
        >
            {logs.map((log) => (
                <div key={log.id} className="break-words font-mono leading-relaxed hover:bg-white/5 px-2 rounded transition-colors">
                    {log.timestamp && (
                        <span className="text-gray-600 mr-3">[{log.timestamp}]</span>
                    )}
                    <span className={getLogColor(log.type)}>
                        {log.message}
                    </span>
                </div>
            ))}
            {/* Cursor piscante no final dos logs se não houver input focado */}
            <div className="h-4" /> 
        </div>

        {/* Command Input Area */}
        <div className="mt-4 pt-4 border-t border-white/10 bg-black/40 backdrop-blur rounded-lg p-2 flex items-center gap-2 focus-within:ring-1 focus-within:ring-[var(--color-primary)] transition-all">
            <span className="text-[var(--color-primary)] font-bold select-none">{`root@nexus:~$`}</span>
            <form onSubmit={handleCommand} className="flex-1">
                <input 
                    ref={inputRef}
                    type="text" 
                    value={command}
                    onChange={(e) => setCommand(e.target.value)}
                    autoFocus
                    className="w-full bg-transparent border-none outline-none text-white font-mono placeholder-gray-700"
                    placeholder="Type 'help' for commands..."
                    autoComplete="off"
                />
            </form>
            <div className="hidden md:flex items-center gap-1 text-[10px] text-gray-600 border border-gray-800 rounded px-2 py-1 select-none">
                <Command className="w-3 h-3" /> <span>EXEC</span>
            </div>
        </div>

      </div>
    </div>
  );
}
