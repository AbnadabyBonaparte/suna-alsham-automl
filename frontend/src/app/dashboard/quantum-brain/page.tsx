/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - QUANTUM BRAIN DASHBOARD
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/quantum-brain/page.tsx
 * 🧠 Interface do Cérebro Quântico - O Coração do Sistema
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useState, useEffect } from 'react';
import { 
  Brain, Zap, Activity, Cpu, Network, Sparkles, 
  Send, Loader2, CheckCircle, AlertTriangle, Terminal
} from 'lucide-react';

interface TaskResult {
  success: boolean;
  task_id: string;
  agent_name: string;
  result: string;
  execution_time_ms: number;
  tokens_used: number;
  cost_usd: number;
  timestamp: string;
}

export default function QuantumBrainPage() {
  const [prompt, setPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<TaskResult | null>(null);
  const [history, setHistory] = useState<TaskResult[]>([]);
  const [brainStats, setBrainStats] = useState({
    status: 'online',
    agents: 139,
    tasks_today: 0,
    avg_response_ms: 0,
  });

  // Fetch brain status on mount
  useEffect(() => {
    fetch('/api/quantum/brain/execute')
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setBrainStats(prev => ({
            ...prev,
            status: 'online',
            agents: data.agents_count || 139,
          }));
        }
      })
      .catch(() => {});
  }, []);

  const executeTask = async () => {
    if (!prompt.trim() || isProcessing) return;

    setIsProcessing(true);
    setResult(null);

    try {
      const response = await fetch('/api/quantum/brain/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          title: prompt,
          description: prompt 
        }),
      });

      const data = await response.json();
      
      if (data.success) {
        setResult(data);
        setHistory(prev => [data, ...prev].slice(0, 10));
        setBrainStats(prev => ({
          ...prev,
          tasks_today: prev.tasks_today + 1,
          avg_response_ms: Math.round((prev.avg_response_ms + data.execution_time_ms) / 2),
        }));
      }
    } catch (error) {
      console.error('Error executing task:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen p-6 space-y-8">
      {/* HEADER */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="absolute -inset-3 bg-purple-500/20 rounded-full blur-xl animate-pulse" />
            <div className="relative w-16 h-16 bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/50 rounded-2xl flex items-center justify-center">
              <Brain className="w-8 h-8 text-purple-400" />
            </div>
          </div>
          <div>
            <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
              QUANTUM BRAIN
              <span className="px-2 py-1 text-xs font-bold bg-purple-500/20 text-purple-400 border border-purple-500/30 rounded-lg">
                LIVE
              </span>
            </h1>
            <p className="text-gray-500 font-mono text-sm mt-1">
              O Cérebro Central do ALSHAM QUANTUM • 139 Agents Sincronizados
            </p>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="flex items-center gap-6">
          <div className="text-center">
            <div className="text-2xl font-black text-purple-400">{brainStats.agents}</div>
            <div className="text-[10px] text-gray-500 uppercase tracking-wider">Agents</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-black text-green-400">{brainStats.tasks_today}</div>
            <div className="text-[10px] text-gray-500 uppercase tracking-wider">Tasks Hoje</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-black text-cyan-400">{brainStats.avg_response_ms || '—'}ms</div>
            <div className="text-[10px] text-gray-500 uppercase tracking-wider">Avg Response</div>
          </div>
        </div>
      </div>

      {/* MAIN INTERFACE */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* LEFT: Input Terminal */}
        <div className="bg-black/40 border border-white/10 rounded-2xl p-6 space-y-6">
          <div className="flex items-center gap-3">
            <Terminal className="w-5 h-5 text-purple-400" />
            <h2 className="text-lg font-bold text-white">Command Terminal</h2>
          </div>

          <div className="space-y-4">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Digite sua task para o ALSHAM QUANTUM processar...&#10;&#10;Exemplo: Analise as tendências de mercado para ecommerce em 2025"
              className="w-full h-40 bg-black/60 border border-white/10 rounded-xl p-4 text-white placeholder-gray-600 font-mono text-sm resize-none focus:border-purple-500/50 focus:outline-none transition-colors"
              disabled={isProcessing}
            />

            <button
              onClick={executeTask}
              disabled={isProcessing || !prompt.trim()}
              className={`w-full py-4 rounded-xl font-bold text-sm tracking-wider uppercase flex items-center justify-center gap-3 transition-all ${
                isProcessing 
                  ? 'bg-purple-500/20 text-purple-400 cursor-wait'
                  : 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-500 hover:to-pink-500 hover:shadow-lg hover:shadow-purple-500/20'
              }`}
            >
              {isProcessing ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  PROCESSANDO COM 139 AGENTS...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  EXECUTAR NO QUANTUM BRAIN
                </>
              )}
            </button>
          </div>

          {/* Quick Actions */}
          <div className="flex flex-wrap gap-2">
            {[
              'Diga olá para o mundo',
              'Analise o mercado de IA',
              'Crie uma estratégia de vendas',
              'Explique quem você é',
            ].map((suggestion, i) => (
              <button
                key={i}
                onClick={() => setPrompt(suggestion)}
                className="px-3 py-1.5 text-xs bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-gray-400 hover:text-white transition-all"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>

        {/* RIGHT: Result Display */}
        <div className="bg-black/40 border border-white/10 rounded-2xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Sparkles className="w-5 h-5 text-cyan-400" />
              <h2 className="text-lg font-bold text-white">Response Output</h2>
            </div>
            {result && (
              <span className="flex items-center gap-2 text-xs text-green-400">
                <CheckCircle className="w-4 h-4" />
                {result.execution_time_ms}ms
              </span>
            )}
          </div>

          <div className="min-h-[300px] bg-black/60 border border-white/10 rounded-xl p-4 overflow-auto">
            {result ? (
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-xs text-gray-500">
                  <span className="px-2 py-0.5 bg-purple-500/20 text-purple-400 rounded">{result.agent_name}</span>
                  <span>•</span>
                  <span>{result.tokens_used} tokens</span>
                  <span>•</span>
                  <span>${result.cost_usd?.toFixed(6)}</span>
                </div>
                <p className="text-white font-mono text-sm leading-relaxed whitespace-pre-wrap">
                  {result.result}
                </p>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-gray-600">
                <Brain className="w-16 h-16 mb-4 opacity-20" />
                <p className="text-sm">Aguardando comando...</p>
                <p className="text-xs mt-1">O Quantum Brain está pronto para processar</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* HISTORY */}
      {history.length > 0 && (
        <div className="bg-black/40 border border-white/10 rounded-2xl p-6">
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-3">
            <Activity className="w-5 h-5 text-cyan-400" />
            Histórico de Tasks
          </h2>
          <div className="space-y-3">
            {history.map((task, i) => (
              <div 
                key={task.task_id + i}
                className="flex items-center justify-between p-3 bg-black/40 border border-white/5 rounded-lg hover:border-white/10 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  <span className="text-sm text-gray-400 truncate max-w-md">
                    {task.result?.slice(0, 80)}...
                  </span>
                </div>
                <div className="flex items-center gap-4 text-xs text-gray-500">
                  <span>{task.execution_time_ms}ms</span>
                  <span>{task.tokens_used} tokens</span>
                  <span className="text-gray-600">
                    {new Date(task.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* NEURAL ACTIVITY VISUALIZATION */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { icon: Cpu, label: 'Neural Load', value: '23%', color: 'text-purple-400' },
          { icon: Network, label: 'Sync Rate', value: '99.9%', color: 'text-cyan-400' },
          { icon: Zap, label: 'Power Output', value: '∞', color: 'text-yellow-400' },
          { icon: Activity, label: 'Heartbeat', value: 'LIVE', color: 'text-green-400' },
        ].map((stat, i) => (
          <div key={i} className="bg-black/40 border border-white/10 rounded-xl p-4 text-center">
            <stat.icon className={`w-6 h-6 mx-auto mb-2 ${stat.color}`} />
            <div className={`text-xl font-black ${stat.color}`}>{stat.value}</div>
            <div className="text-[10px] text-gray-500 uppercase tracking-wider">{stat.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

