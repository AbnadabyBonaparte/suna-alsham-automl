/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - THE MATRIX (NEURAL NETWORK 3D)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/matrix/page.tsx
 * 🧬 Visualização 3D da rede neural com 139 nodes conectados
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef, FormEvent } from 'react';
import { supabase } from '@/lib/supabase';
import { Terminal, Shield, Wifi, Cpu, AlertOctagon, Command, Network, Users, Activity, Zap } from 'lucide-react';

interface LogEntry {
  id: number;
  timestamp: string;
  type: 'info' | 'success' | 'warning' | 'error' | 'system';
  message: string;
}

interface NetworkNode {
  id: string;
  name: string;
  squad: string;
  status: string;
  efficiency: number;
  connections: number;
}

export default function MatrixPage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [command, setCommand] = useState('');
  const [isGlitching, setIsGlitching] = useState(false);
  const [nodes, setNodes] = useState<NetworkNode[]>([]);
  const [selectedNode, setSelectedNode] = useState<NetworkNode | null>(null);
  const [networkStats, setNetworkStats] = useState({
    totalNodes: 0,
    activeNodes: 0,
    connections: 0,
    dataFlow: 0,
  });

  // Carregar agents como nodes da rede
  useEffect(() => {
    async function loadNodes() {
      try {
        const { data: agents, error } = await supabase
          .from('agents')
          .select('*')
          .limit(139);

        if (error) throw error;

        const networkNodes: NetworkNode[] = (agents || []).map((agent, i) => ({
          id: agent.id,
          name: agent.name || `NODE_${String(i).padStart(3, '0')}`,
          squad: agent.squad || 'NEXUS',
          status: agent.status || 'active',
          efficiency: agent.efficiency || Math.floor(Math.random() * 40 + 60),
          connections: Math.floor(Math.random() * 10 + 2),
        }));

        // Se menos de 139 agents, preencher com mock
        while (networkNodes.length < 139) {
          networkNodes.push({
            id: `mock_${networkNodes.length}`,
            name: `NODE_${String(networkNodes.length).padStart(3, '0')}`,
            squad: ['NEXUS', 'VOID', 'SENTINEL', 'CHAOS', 'COMMAND'][Math.floor(Math.random() * 5)],
            status: Math.random() > 0.1 ? 'active' : 'idle',
            efficiency: Math.floor(Math.random() * 40 + 60),
            connections: Math.floor(Math.random() * 10 + 2),
          });
        }

        setNodes(networkNodes);

        const activeNodes = networkNodes.filter(n => n.status === 'active').length;
        const totalConnections = networkNodes.reduce((sum, n) => sum + n.connections, 0);

        setNetworkStats({
          totalNodes: networkNodes.length,
          activeNodes,
          connections: totalConnections,
          dataFlow: Math.floor(Math.random() * 5000 + 1000),
        });

      } catch (err) {
        console.error('Failed to load nodes:', err);
      }
    }

    loadNodes();
  }, []);

  // MATRIX RAIN + NEURAL NETWORK VISUALIZATION
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

    // Matrix Rain
    const columns = Math.floor(canvas.width / 20);
    const drops: number[] = Array(columns).fill(1);
    const chars = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';

    // Neural Network Nodes
    const nodePositions: { x: number; y: number; vx: number; vy: number; node: NetworkNode }[] = [];
    
    const initNodes = () => {
      nodePositions.length = 0;
      const w = canvas.width;
      const h = canvas.height;
      
      nodes.slice(0, 50).forEach((node) => {
        nodePositions.push({
          x: Math.random() * w,
          y: Math.random() * h,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
          node,
        });
      });
    };

    if (nodes.length > 0) initNodes();

    let time = 0;

    const draw = () => {
      const w = canvas.width;
      const h = canvas.height;

      // Fundo com fade
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, w, h);

      time += 0.01;

      const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';
      
      // Matrix Rain
      ctx.font = '15px monospace';
      for (let i = 0; i < drops.length; i++) {
        const text = chars.charAt(Math.floor(Math.random() * chars.length));
        
        if (Math.random() > 0.95) {
          ctx.fillStyle = '#FFF';
        } else {
          ctx.fillStyle = primaryColor;
          ctx.globalAlpha = 0.3;
        }

        ctx.fillText(text, i * 20, drops[i] * 20);
        ctx.globalAlpha = 1;

        if (drops[i] * 20 > h && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }

      // Neural Network Visualization
      if (nodePositions.length > 0) {
        // Atualizar posições
        nodePositions.forEach(np => {
          np.x += np.vx;
          np.y += np.vy;
          
          if (np.x < 0 || np.x > w) np.vx *= -1;
          if (np.y < 0 || np.y > h) np.vy *= -1;
        });

        // Desenhar conexões
        ctx.strokeStyle = primaryColor;
        ctx.lineWidth = 0.5;
        ctx.globalAlpha = 0.2;
        
        for (let i = 0; i < nodePositions.length; i++) {
          for (let j = i + 1; j < nodePositions.length; j++) {
            const dx = nodePositions[i].x - nodePositions[j].x;
            const dy = nodePositions[i].y - nodePositions[j].y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist < 150) {
              ctx.beginPath();
              ctx.moveTo(nodePositions[i].x, nodePositions[j].y);
              ctx.lineTo(nodePositions[j].x, nodePositions[j].y);
              ctx.stroke();
            }
          }
        }
        ctx.globalAlpha = 1;

        // Desenhar nodes
        nodePositions.forEach(np => {
          const isActive = np.node.status === 'active';
          const pulse = Math.sin(time * 5 + np.x) * 0.3 + 1;
          
          ctx.beginPath();
          const size = (isActive ? 4 : 2) * pulse;
          ctx.arc(np.x, np.y, size, 0, Math.PI * 2);
          
          if (np.node.squad === 'VOID') ctx.fillStyle = '#8B5CF6';
          else if (np.node.squad === 'COMMAND') ctx.fillStyle = '#FFD700';
          else if (np.node.squad === 'SENTINEL') ctx.fillStyle = '#10B981';
          else if (np.node.squad === 'CHAOS') ctx.fillStyle = '#EF4444';
          else ctx.fillStyle = primaryColor;
          
          ctx.fill();
          
          // Glow
          ctx.shadowColor = ctx.fillStyle as string;
          ctx.shadowBlur = isActive ? 10 : 0;
          ctx.fill();
          ctx.shadowBlur = 0;
        });
      }
    };

    const interval = setInterval(draw, 33);
    return () => {
        clearInterval(interval);
        window.removeEventListener('resize', resize);
    };
  }, [nodes]);

  // Logs do sistema
  useEffect(() => {
    const systemMessages = [
        "Quantum Core: Syncing neural weights...",
        "Network: Handshake established with node 192.168.x.x",
        "Security: Scanning packet headers [OK]",
        "Memory: Garbage collection complete. Freed 240MB.",
        `Agent [${nodes[Math.floor(Math.random() * nodes.length)]?.name || 'Sentinel'}]: Ping 12ms`,
        "Orion AI: Processing natural language context...",
        "System: Optimization heuristic updated.",
        "Database: Transaction verified block #99281",
        "Neural: Synaptic connection established",
        "Matrix: Data flow optimized by 15%",
    ];

    const addLog = () => {
        const type = Math.random() > 0.9 ? 'warning' : Math.random() > 0.95 ? 'error' : 'info';
        const msg = systemMessages[Math.floor(Math.random() * systemMessages.length)];
        const suffix = Math.random().toString(16).substring(7).toUpperCase();
        
        const newLog: LogEntry = {
            id: Date.now(),
            timestamp: new Date().toLocaleTimeString('en-US', { hour12: false }),
            type,
            message: `${msg} [HASH: ${suffix}]`
        };

        setLogs(prev => [...prev.slice(-50), newLog]);
    };

    const interval = setInterval(addLog, 2000);
    
    setLogs([
        { id: 1, timestamp: new Date().toLocaleTimeString(), type: 'system', message: 'ALSHAM QUANTUM MATRIX v13.3 INITIALIZED' },
        { id: 2, timestamp: new Date().toLocaleTimeString(), type: 'system', message: `NEURAL NETWORK: ${nodes.length} NODES CONNECTED` },
        { id: 3, timestamp: new Date().toLocaleTimeString(), type: 'success', message: 'Connected to Mainframe.' },
    ]);

    return () => clearInterval(interval);
  }, [nodes]);

  useEffect(() => {
    if (scrollRef.current) {
        scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  const handleCommand = (e: FormEvent) => {
    e.preventDefault();
    if (!command.trim()) return;

    const cmd = command.trim().toLowerCase();
    const newLogs: LogEntry[] = [
        { id: Date.now(), timestamp: new Date().toLocaleTimeString(), type: 'info', message: `user@root:~$ ${command}` }
    ];

    switch(cmd) {
        case 'clear':
            setLogs([]);
            setCommand('');
            return;
        case 'help':
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'system', message: 'COMMANDS: help, clear, status, scan, nodes, stats, reboot, whoami' });
            break;
        case 'status':
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'success', message: `SYSTEM INTEGRITY: 100% | NODES: ${networkStats.activeNodes}/${networkStats.totalNodes} ACTIVE` });
            break;
        case 'scan':
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'warning', message: 'SCANNING NEURAL NETWORK... ALL NODES OPERATIONAL.' });
            break;
        case 'nodes':
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'info', message: `TOTAL: ${networkStats.totalNodes} | ACTIVE: ${networkStats.activeNodes} | CONNECTIONS: ${networkStats.connections}` });
            break;
        case 'stats':
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'info', message: `DATA FLOW: ${networkStats.dataFlow} MB/s | LATENCY: ${Math.floor(Math.random() * 20 + 5)}ms` });
            break;
        case 'reboot':
            setIsGlitching(true);
            setTimeout(() => setIsGlitching(false), 1000);
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'error', message: 'MATRIX REBOOT SIMULATED.' });
            break;
        case 'whoami':
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'info', message: 'USER: ADMIN [MATRIX GOD MODE]' });
            break;
        default:
            newLogs.push({ id: Date.now()+1, timestamp: '', type: 'error', message: `Command not found: ${cmd}` });
    }

    setLogs(prev => [...prev, ...newLogs]);
    setCommand('');
  };

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

      {/* CANVAS */}
      <canvas 
        ref={canvasRef} 
        className="absolute inset-0 w-full h-full"
      />

      {/* STATS OVERLAY */}
      <div className="absolute top-6 right-6 z-30 space-y-3">
        <div className="bg-black/60 backdrop-blur-xl border border-[var(--color-primary)]/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <Network className="w-5 h-5 text-[var(--color-primary)]" />
            <span className="text-sm font-bold text-white">Neural Network</span>
          </div>
          <div className="grid grid-cols-2 gap-3 text-center">
            <div>
              <div className="text-2xl font-black text-[var(--color-primary)]">{networkStats.totalNodes}</div>
              <div className="text-[9px] text-gray-500 uppercase">Nodes</div>
            </div>
            <div>
              <div className="text-2xl font-black text-green-400">{networkStats.activeNodes}</div>
              <div className="text-[9px] text-gray-500 uppercase">Active</div>
            </div>
            <div>
              <div className="text-xl font-black text-purple-400">{networkStats.connections}</div>
              <div className="text-[9px] text-gray-500 uppercase">Links</div>
            </div>
            <div>
              <div className="text-xl font-black text-cyan-400">{networkStats.dataFlow}</div>
              <div className="text-[9px] text-gray-500 uppercase">MB/s</div>
            </div>
          </div>
        </div>
      </div>

      {/* CRT EFFECT */}
      <div className="absolute inset-0 pointer-events-none z-20 bg-[url('/scanlines.png')] opacity-10" 
           style={{ backgroundSize: '100% 4px' }} />
      <div className="absolute inset-0 pointer-events-none z-20 bg-radial-gradient from-transparent to-black/80" />

      {/* TERMINAL */}
      <div className="relative z-30 h-full flex flex-col p-6 font-mono text-sm md:text-base">
        
        {/* Header */}
        <div className="flex justify-between items-center border-b border-white/10 pb-4 mb-4 select-none">
            <div className="flex items-center gap-3">
                <Terminal className="w-5 h-5 text-[var(--color-primary)]" />
                <span className="text-white font-bold tracking-widest">MATRIX_SHELL_V13.3</span>
            </div>
            <div className="flex gap-4 text-xs text-gray-500">
                <span className="flex items-center gap-1"><Wifi className="w-3 h-3" /> {networkStats.activeNodes} NODES</span>
                <span className="flex items-center gap-1"><Cpu className="w-3 h-3" /> CPU: 12%</span>
                <span className="flex items-center gap-1"><Shield className="w-3 h-3" /> FW: ON</span>
            </div>
        </div>

        {/* Log Output */}
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
            <div className="h-4" /> 
        </div>

        {/* Command Input */}
        <div className="mt-4 pt-4 border-t border-white/10 bg-black/40 backdrop-blur rounded-lg p-2 flex items-center gap-2 focus-within:ring-1 focus-within:ring-[var(--color-primary)] transition-all">
            <span className="text-[var(--color-primary)] font-bold select-none">{`root@matrix:~$`}</span>
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
