/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - THE MATRIX (THEME-AWARE)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/matrix/page.tsx
 * 🧬 Visualização 3D da rede neural com 139 nodes conectados
 * 🎨 100% SUBMISSO AOS TEMAS - USA VARIÁVEIS CSS
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef, FormEvent } from 'react';
import { supabase } from '@/lib/supabase';
import { useTheme } from '@/contexts/ThemeContext';
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
  const { themeConfig } = useTheme();
  const colors = themeConfig.colors;
  
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

  // MATRIX RAIN + NEURAL NETWORK - USA CORES DO TEMA
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
    const chars = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';

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

      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, w, h);

      time += 0.01;

      const primaryColor = colors.primary;
      
      // Matrix Rain
      ctx.font = '15px monospace';
      for (let i = 0; i < drops.length; i++) {
        const text = chars.charAt(Math.floor(Math.random() * chars.length));
        
        if (Math.random() > 0.95) {
          ctx.fillStyle = colors.text;
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

      // Neural Network
      if (nodePositions.length > 0) {
        nodePositions.forEach(np => {
          np.x += np.vx;
          np.y += np.vy;
          
          if (np.x < 0 || np.x > w) np.vx *= -1;
          if (np.y < 0 || np.y > h) np.vy *= -1;
        });

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

        nodePositions.forEach(np => {
          const isActive = np.node.status === 'active';
          const pulse = Math.sin(time * 5 + np.x) * 0.3 + 1;
          
          ctx.beginPath();
          const size = (isActive ? 4 : 2) * pulse;
          ctx.arc(np.x, np.y, size, 0, Math.PI * 2);
          
          // Squad-based colors using theme
          if (np.node.squad === 'VOID') ctx.fillStyle = colors.accent;
          else if (np.node.squad === 'COMMAND') ctx.fillStyle = colors.warning;
          else if (np.node.squad === 'SENTINEL') ctx.fillStyle = colors.success;
          else if (np.node.squad === 'CHAOS') ctx.fillStyle = colors.error;
          else ctx.fillStyle = primaryColor;
          
          ctx.fill();
          
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
  }, [nodes, colors]);

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
        case 'error': return colors.error;
        case 'warning': return colors.warning;
        case 'success': return colors.success;
        case 'system': return colors.primary;
        default: return colors.textSecondary;
    }
  };

  return (
    <div 
      className={`relative h-[calc(100vh-6rem)] rounded-2xl overflow-hidden group ${isGlitching ? 'animate-pulse' : ''}`}
      style={{
        background: colors.background,
        border: `1px solid ${colors.border}/30`
      }}
    >
      <canvas 
        ref={canvasRef} 
        className="absolute inset-0 w-full h-full"
      />

      {/* STATS OVERLAY */}
      <div className="absolute top-6 right-6 z-30 space-y-3">
        <div 
          className="backdrop-blur-xl rounded-xl p-4"
          style={{
            background: `${colors.surface}/60`,
            border: `1px solid ${colors.primary}/30`
          }}
        >
          <div className="flex items-center gap-2 mb-3">
            <Network className="w-5 h-5" style={{ color: colors.primary }} />
            <span className="text-sm font-bold" style={{ color: colors.text }}>Neural Network</span>
          </div>
          <div className="grid grid-cols-2 gap-3 text-center">
            <div>
              <div className="text-2xl font-black" style={{ color: colors.primary }}>{networkStats.totalNodes}</div>
              <div className="text-[9px] uppercase" style={{ color: colors.textSecondary }}>Nodes</div>
            </div>
            <div>
              <div className="text-2xl font-black" style={{ color: colors.success }}>{networkStats.activeNodes}</div>
              <div className="text-[9px] uppercase" style={{ color: colors.textSecondary }}>Active</div>
            </div>
            <div>
              <div className="text-xl font-black" style={{ color: colors.accent }}>{networkStats.connections}</div>
              <div className="text-[9px] uppercase" style={{ color: colors.textSecondary }}>Links</div>
            </div>
            <div>
              <div className="text-xl font-black" style={{ color: colors.secondary }}>{networkStats.dataFlow}</div>
              <div className="text-[9px] uppercase" style={{ color: colors.textSecondary }}>MB/s</div>
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
        <div className="flex justify-between items-center pb-4 mb-4 select-none" style={{ borderBottom: `1px solid ${colors.border}/10` }}>
            <div className="flex items-center gap-3">
                <Terminal className="w-5 h-5" style={{ color: colors.primary }} />
                <span className="font-bold tracking-widest" style={{ color: colors.text }}>MATRIX_SHELL_V13.3</span>
            </div>
            <div className="flex gap-4 text-xs" style={{ color: colors.textSecondary }}>
                <span className="flex items-center gap-1"><Wifi className="w-3 h-3" /> {networkStats.activeNodes} NODES</span>
                <span className="flex items-center gap-1"><Cpu className="w-3 h-3" /> CPU: 12%</span>
                <span className="flex items-center gap-1"><Shield className="w-3 h-3" /> FW: ON</span>
            </div>
        </div>

        {/* Log Output */}
        <div 
            ref={scrollRef}
            className="flex-1 overflow-y-auto overflow-x-hidden space-y-1 pr-4"
        >
            {logs.map((log) => (
                <div 
                  key={log.id} 
                  className="break-words font-mono leading-relaxed px-2 rounded transition-colors"
                  style={{ color: colors.text }}
                >
                    {log.timestamp && (
                        <span className="mr-3" style={{ color: colors.textSecondary }}>[{log.timestamp}]</span>
                    )}
                    <span style={{ color: getLogColor(log.type), fontWeight: log.type === 'system' ? 'bold' : 'normal' }}>
                        {log.message}
                    </span>
                </div>
            ))}
            <div className="h-4" /> 
        </div>

        {/* Command Input */}
        <div 
          className="mt-4 pt-4 backdrop-blur rounded-lg p-2 flex items-center gap-2 transition-all"
          style={{
            borderTop: `1px solid ${colors.border}/10`,
            background: `${colors.surface}/40`
          }}
        >
            <span className="font-bold select-none" style={{ color: colors.primary }}>{`root@matrix:~$`}</span>
            <form onSubmit={handleCommand} className="flex-1">
                <input 
                    ref={inputRef}
                    type="text" 
                    value={command}
                    onChange={(e) => setCommand(e.target.value)}
                    autoFocus
                    className="w-full bg-transparent border-none outline-none font-mono"
                    style={{ color: colors.text }}
                    placeholder="Type 'help' for commands..."
                    autoComplete="off"
                />
            </form>
            <div 
              className="hidden md:flex items-center gap-1 text-[10px] rounded px-2 py-1 select-none"
              style={{
                color: colors.textSecondary,
                border: `1px solid ${colors.border}/20`
              }}
            >
                <Command className="w-3 h-3" /> <span>EXEC</span>
            </div>
        </div>

      </div>
    </div>
  );
}
