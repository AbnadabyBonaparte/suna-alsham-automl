/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - QUANTUM BRAIN GODMODE
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/quantum-brain/page.tsx
 * 🧠 Central de Comando - O Trono do ALSHAM QUANTUM
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useState, useEffect, useRef } from 'react';
import { supabase } from '@/lib/supabase';
import { useAgents } from '@/hooks/useAgents';
import { useDashboardStats } from '@/hooks/useDashboardStats';
import { 
  Brain, Zap, Activity, Cpu, Network, Sparkles, Crown,
  Send, Loader2, CheckCircle, AlertTriangle, Terminal,
  Clock, TrendingUp, Copy, FileDown, Mail, MessageSquare,
  RefreshCw, Filter, Search, ChevronDown, Play, Pause,
  AlertOctagon, Eye, Layers, Users, Target, History,
  BarChart3, Gauge, Power, Radio, Wifi, Shield, X
} from 'lucide-react';

// Tipos
interface TaskResult {
  id: string;
  success: boolean;
  task_id: string;
  agent_id: string;
  agent_name: string;
  squad: string;
  result: string;
  execution_time_ms: number;
  tokens_used: number;
  cost_usd: number;
  timestamp: string;
  status: string;
  title?: string;
  priority?: string;
}

interface Agent {
  id: string;
  name: string;
  role: string;
  squad: string;
  status: string;
  efficiency: number;
}

// Squads disponíveis
const SQUADS = [
  { id: 'COMMAND', name: 'COMMAND', color: '#FFD700', icon: Crown },
  { id: 'VOID', name: 'VOID', color: '#8B5CF6', icon: Eye },
  { id: 'NEXUS', name: 'NEXUS', color: '#06B6D4', icon: Network },
  { id: 'SENTINEL', name: 'SENTINEL', color: '#10B981', icon: Shield },
  { id: 'CHAOS', name: 'CHAOS', color: '#EF4444', icon: AlertOctagon },
];

// Quick Actions
const QUICK_ACTIONS = [
  { label: 'Analisar Contrato', prompt: 'Analise este contrato comercial e identifique pontos críticos, riscos e oportunidades de negociação.', icon: '📄' },
  { label: 'Gerar Proposta', prompt: 'Crie uma proposta comercial profissional para um serviço de consultoria em IA para uma empresa de médio porte.', icon: '💼' },
  { label: 'Campanha Marketing', prompt: 'Desenvolva uma campanha de marketing digital completa para lançamento de produto SaaS B2B.', icon: '📣' },
  { label: 'Script Cold Call', prompt: 'Crie um script de cold call persuasivo para prospecção de clientes enterprise.', icon: '📞' },
  { label: 'Análise de Mercado', prompt: 'Faça uma análise completa do mercado de Inteligência Artificial em 2025, incluindo tendências e oportunidades.', icon: '📊' },
  { label: 'Otimizar Funil', prompt: 'Sugira otimizações para um funil de vendas B2B com baixa taxa de conversão no meio do funil.', icon: '🔄' },
];

export default function QuantumBrainPage() {
  // States principais
  const [prompt, setPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentResult, setCurrentResult] = useState<TaskResult | null>(null);
  const [taskHistory, setTaskHistory] = useState<TaskResult[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<string>('auto');
  const [priority, setPriority] = useState<'low' | 'normal' | 'high' | 'critical'>('normal');
  const [multiAgentMode, setMultiAgentMode] = useState(false);
  const [showAgentDropdown, setShowAgentDropdown] = useState(false);
  const [agentSearch, setAgentSearch] = useState('');
  const [historyFilter, setHistoryFilter] = useState<'all' | 'today' | 'week'>('all');
  const [statusFilter, setStatusFilter] = useState<'all' | 'completed' | 'failed' | 'processing'>('all');
  const [godViewMode, setGodViewMode] = useState(false);
  
  // Stats ao vivo
  const [liveStats, setLiveStats] = useState({
    agentsOnline: 139,
    avgResponse: 4200,
    avgCost: 0.0032,
    tasksToday: 0,
    syncRate: 99.9,
    neuralPower: 87,
  });

  // Hooks
  const { agents, loading: agentsLoading } = useAgents();
  const dashboardStats = useDashboardStats();
  
  const terminalRef = useRef<HTMLTextAreaElement>(null);
  const resultRef = useRef<HTMLDivElement>(null);

  // Carregar histórico de tasks do Supabase
  useEffect(() => {
    async function loadHistory() {
      try {
        const { data, error } = await supabase
          .from('requests')
          .select('*')
          .order('created_at', { ascending: false })
          .limit(50);
        
        if (error) throw error;
        
        const formattedHistory = (data || []).map(req => ({
          id: req.id,
          success: req.status === 'completed',
          task_id: req.id,
          agent_id: req.assigned_agent_id || 'orion',
          agent_name: req.assigned_agent_name || 'ORION Supreme',
          squad: 'COMMAND',
          result: req.response || req.description || '',
          execution_time_ms: req.processing_time_ms || 0,
          tokens_used: req.tokens_used || 0,
          cost_usd: req.cost_usd || 0,
          timestamp: req.created_at,
          status: req.status,
          title: req.title,
          priority: req.priority,
        }));
        
        setTaskHistory(formattedHistory);
        
        // Contar tasks de hoje
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const tasksToday = formattedHistory.filter(t => new Date(t.timestamp) >= today).length;
        setLiveStats(prev => ({ ...prev, tasksToday }));
        
      } catch (err) {
        console.error('Failed to load history:', err);
      }
    }
    
    loadHistory();
    
    // Refresh a cada 30s
    const interval = setInterval(loadHistory, 30000);
    return () => clearInterval(interval);
  }, []);

  // Atualizar stats ao vivo
  useEffect(() => {
    if (dashboardStats.totalAgents) {
      setLiveStats(prev => ({
        ...prev,
        agentsOnline: dashboardStats.totalAgents || 139,
        neuralPower: Math.round(dashboardStats.avgEfficiency) || 87,
      }));
    }
  }, [dashboardStats]);

  // Simular métricas ao vivo
  useEffect(() => {
    const interval = setInterval(() => {
      setLiveStats(prev => ({
        ...prev,
        syncRate: Math.min(100, Math.max(95, prev.syncRate + (Math.random() - 0.5) * 0.5)),
        neuralPower: Math.min(100, Math.max(60, prev.neuralPower + (Math.random() - 0.5) * 3)),
        avgResponse: Math.max(1000, prev.avgResponse + (Math.random() - 0.5) * 500),
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  // Executar task
  const executeTask = async () => {
    if (!prompt.trim() || isProcessing) return;

    setIsProcessing(true);
    setCurrentResult(null);

    try {
      const response = await fetch('/api/quantum/brain/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          title: prompt,
          description: prompt,
          agent_id: selectedAgent === 'auto' ? undefined : selectedAgent,
          priority,
          multi_agent: multiAgentMode,
        }),
      });

      const data = await response.json();
      
      const result: TaskResult = {
        id: data.task_id || `task_${Date.now()}`,
        success: data.success,
        task_id: data.task_id || `task_${Date.now()}`,
        agent_id: data.agent_id || 'orion',
        agent_name: data.agent_name || 'ORION Supreme',
        squad: data.squad || 'COMMAND',
        result: data.result || data.error || 'Erro desconhecido',
        execution_time_ms: data.execution_time_ms || 0,
        tokens_used: data.tokens_used || 0,
        cost_usd: data.cost_usd || 0,
        timestamp: new Date().toISOString(),
        status: data.success ? 'completed' : 'failed',
        title: prompt,
        priority,
      };
      
      setCurrentResult(result);
      setTaskHistory(prev => [result, ...prev]);
      setLiveStats(prev => ({
        ...prev,
        tasksToday: prev.tasksToday + 1,
        avgResponse: Math.round((prev.avgResponse + result.execution_time_ms) / 2),
        avgCost: (prev.avgCost + result.cost_usd) / 2,
      }));
      
      // Scroll para o resultado
      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
      
    } catch (error) {
      console.error('Error executing task:', error);
      setCurrentResult({
        id: `error_${Date.now()}`,
        success: false,
        task_id: `error_${Date.now()}`,
        agent_id: 'system',
        agent_name: 'SYSTEM',
        squad: 'SYSTEM',
        result: 'Erro de conexão com o Quantum Brain. Verifique sua conexão e tente novamente.',
        execution_time_ms: 0,
        tokens_used: 0,
        cost_usd: 0,
        timestamp: new Date().toISOString(),
        status: 'failed',
        title: prompt,
        priority,
      });
    } finally {
      setIsProcessing(false);
    }
  };

  // Copiar resultado
  const copyResult = () => {
    if (currentResult?.result) {
      navigator.clipboard.writeText(currentResult.result);
    }
  };

  // Filtrar histórico
  const filteredHistory = taskHistory.filter(task => {
    // Filtro de status
    if (statusFilter !== 'all' && task.status !== statusFilter) return false;
    
    // Filtro de tempo
    if (historyFilter === 'today') {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      if (new Date(task.timestamp) < today) return false;
    } else if (historyFilter === 'week') {
      const weekAgo = new Date();
      weekAgo.setDate(weekAgo.getDate() - 7);
      if (new Date(task.timestamp) < weekAgo) return false;
    }
    
    return true;
  });

  // Filtrar agents para dropdown
  const filteredAgents = (agents || []).filter((agent: Agent) => 
    agent.name?.toLowerCase().includes(agentSearch.toLowerCase()) ||
    agent.role?.toLowerCase().includes(agentSearch.toLowerCase()) ||
    agent.squad?.toLowerCase().includes(agentSearch.toLowerCase())
  );

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background Neural Grid */}
      <div className="fixed inset-0 bg-[url('/grid.svg')] opacity-5 pointer-events-none" />
      <div className="fixed inset-0 bg-gradient-to-br from-purple-900/10 via-transparent to-cyan-900/10 pointer-events-none" />
      
      {/* TOP BAR - Métricas ao Vivo */}
      <div className="sticky top-0 z-40 bg-black/80 backdrop-blur-xl border-b border-white/10 px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className="absolute -inset-2 bg-purple-500/20 rounded-full blur-xl animate-pulse" />
              <Brain className="w-8 h-8 text-purple-400 relative" />
            </div>
            <div>
              <h1 className="text-xl font-black text-white tracking-tight flex items-center gap-2">
                QUANTUM BRAIN
                <span className="px-2 py-0.5 text-[10px] font-bold bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full animate-pulse">
                  GODMODE
                </span>
              </h1>
              <p className="text-[10px] text-gray-500 font-mono">O Trono do ALSHAM QUANTUM • 139 Agents Sincronizados</p>
            </div>
          </div>
          
          {/* Live Stats */}
          <div className="hidden lg:flex items-center gap-6">
            <div className="flex items-center gap-2 px-3 py-1 bg-green-500/10 border border-green-500/30 rounded-lg">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-xs font-bold text-green-400">{liveStats.agentsOnline} Agents Online</span>
            </div>
            
            <div className="text-center">
              <div className="text-sm font-black text-cyan-400">{(liveStats.avgResponse / 1000).toFixed(1)}s</div>
              <div className="text-[9px] text-gray-500 uppercase">Avg Response</div>
            </div>
            
            <div className="text-center">
              <div className="text-sm font-black text-green-400">R${(liveStats.avgCost * 5.5).toFixed(4)}</div>
              <div className="text-[9px] text-gray-500 uppercase">Avg Cost</div>
            </div>
            
            <div className="text-center">
              <div className="text-sm font-black text-purple-400">{liveStats.tasksToday}</div>
              <div className="text-[9px] text-gray-500 uppercase">Tasks Today</div>
            </div>
            
            <div className="text-center">
              <div className="text-sm font-black text-yellow-400">{liveStats.syncRate.toFixed(1)}%</div>
              <div className="text-[9px] text-gray-500 uppercase">Sync Rate</div>
            </div>
            
            <div className="flex items-center gap-2">
              <Gauge className="w-4 h-4 text-orange-400" />
              <div className="w-20 h-2 bg-gray-800 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-orange-500 to-red-500 transition-all duration-500"
                  style={{ width: `${liveStats.neuralPower}%` }}
                />
              </div>
              <span className="text-xs text-orange-400 font-mono">{liveStats.neuralPower}%</span>
            </div>
          </div>
          
          {/* God View Toggle */}
          <button
            onClick={() => setGodViewMode(!godViewMode)}
            className={`px-4 py-2 rounded-lg font-bold text-xs uppercase tracking-wider transition-all flex items-center gap-2 ${
              godViewMode 
                ? 'bg-purple-500 text-white shadow-[0_0_20px_rgba(168,85,247,0.5)]' 
                : 'bg-white/5 text-gray-400 hover:bg-white/10'
            }`}
          >
            <Eye className="w-4 h-4" />
            God View
          </button>
        </div>
      </div>

      {/* GOD VIEW MODE - Grid de todos os agents */}
      {godViewMode && (
        <div className="fixed inset-0 z-50 bg-black/95 backdrop-blur-xl overflow-auto p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-black text-white flex items-center gap-3">
              <Eye className="w-6 h-6 text-purple-400" />
              GOD VIEW - {agents?.length || 139} AGENTS
            </h2>
            <button
              onClick={() => setGodViewMode(false)}
              className="p-2 bg-white/10 rounded-lg hover:bg-white/20 transition"
            >
              <X className="w-6 h-6 text-white" />
            </button>
          </div>
          
          <div className="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-8 xl:grid-cols-10 gap-3">
            {(agents || Array.from({ length: 139 }, (_, i) => ({
              id: `agent_${i}`,
              name: `AGENT_${String(i).padStart(3, '0')}`,
              status: Math.random() > 0.1 ? 'active' : 'idle',
              efficiency: Math.floor(Math.random() * 40 + 60),
              squad: SQUADS[Math.floor(Math.random() * SQUADS.length)].id,
            }))).map((agent: any, i: number) => (
              <div
                key={agent.id || i}
                className={`p-3 rounded-xl border transition-all hover:scale-105 cursor-pointer ${
                  agent.status === 'active' 
                    ? 'bg-green-500/10 border-green-500/30' 
                    : 'bg-white/5 border-white/10'
                }`}
              >
                <div className={`w-3 h-3 rounded-full mb-2 ${
                  agent.status === 'active' ? 'bg-green-500 animate-pulse' : 'bg-gray-600'
                }`} />
                <div className="text-[10px] font-bold text-white truncate">{agent.name}</div>
                <div className="text-[9px] text-gray-500">{agent.efficiency || 85}%</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* MAIN CONTENT - 3 Colunas */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 p-6">
        
        {/* COLUNA ESQUERDA - Histórico de Tasks */}
        <div className="lg:col-span-3 space-y-4">
          <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden">
            {/* Header */}
            <div className="p-4 border-b border-white/10 bg-white/5">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                  <History className="w-4 h-4 text-purple-400" />
                  Histórico
                </h2>
                <span className="text-xs text-gray-500">{filteredHistory.length} tasks</span>
              </div>
              
              {/* Filtros */}
              <div className="flex gap-2">
                <select
                  value={historyFilter}
                  onChange={(e) => setHistoryFilter(e.target.value as any)}
                  className="flex-1 px-2 py-1 text-xs bg-white/5 border border-white/10 rounded-lg text-white"
                >
                  <option value="all">Todos</option>
                  <option value="today">Hoje</option>
                  <option value="week">Semana</option>
                </select>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value as any)}
                  className="flex-1 px-2 py-1 text-xs bg-white/5 border border-white/10 rounded-lg text-white"
                >
                  <option value="all">Status</option>
                  <option value="completed">✓ Completed</option>
                  <option value="failed">✗ Failed</option>
                  <option value="processing">⏳ Processing</option>
                </select>
              </div>
            </div>
            
            {/* Lista de Tasks */}
            <div className="max-h-[calc(100vh-400px)] overflow-y-auto">
              {filteredHistory.length === 0 ? (
                <div className="p-8 text-center text-gray-500">
                  <History className="w-12 h-12 mx-auto mb-3 opacity-20" />
                  <p className="text-sm">Nenhuma task encontrada</p>
                </div>
              ) : (
                filteredHistory.map((task, i) => (
                  <div
                    key={task.id || i}
                    onClick={() => setCurrentResult(task)}
                    className={`p-4 border-b border-white/5 hover:bg-white/5 cursor-pointer transition-all ${
                      currentResult?.id === task.id ? 'bg-purple-500/10 border-l-2 border-l-purple-500' : ''
                    }`}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div className={`w-2 h-2 rounded-full mt-1.5 ${
                        task.status === 'completed' ? 'bg-green-500' : 
                        task.status === 'failed' ? 'bg-red-500' : 'bg-yellow-500 animate-pulse'
                      }`} />
                      <span className="text-[10px] text-gray-500 font-mono">
                        {new Date(task.timestamp).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                    <p className="text-sm text-white font-medium truncate mb-1">
                      {task.title || task.result?.slice(0, 50)}
                    </p>
                    <div className="flex items-center gap-2 text-[10px] text-gray-500">
                      <span className="px-1.5 py-0.5 bg-purple-500/20 text-purple-400 rounded">
                        {task.agent_name?.split(' ')[0] || 'ORION'}
                      </span>
                      <span>{task.execution_time_ms}ms</span>
                      <span>{task.tokens_used} tok</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* COLUNA CENTRAL - Command Terminal */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <Terminal className="w-5 h-5 text-purple-400" />
                <h2 className="text-lg font-bold text-white">Command Terminal</h2>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setMultiAgentMode(!multiAgentMode)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    multiAgentMode 
                      ? 'bg-purple-500 text-white' 
                      : 'bg-white/5 text-gray-400 hover:bg-white/10'
                  }`}
                >
                  <Users className="w-3 h-3 inline mr-1" />
                  Multi-Agent
                </button>
              </div>
            </div>

            {/* Agent Selector */}
            <div className="mb-4 relative">
              <label className="text-[10px] text-gray-500 uppercase tracking-wider block mb-2">
                Selecionar Agent
              </label>
              <button
                onClick={() => setShowAgentDropdown(!showAgentDropdown)}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-left flex items-center justify-between hover:border-purple-500/50 transition-all"
              >
                <span className="text-white">
                  {selectedAgent === 'auto' ? '🤖 Automático (ORION decide)' : 
                   agents?.find((a: Agent) => a.id === selectedAgent)?.name || selectedAgent}
                </span>
                <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${showAgentDropdown ? 'rotate-180' : ''}`} />
              </button>
              
              {showAgentDropdown && (
                <div className="absolute top-full left-0 right-0 mt-2 bg-black/95 border border-white/20 rounded-xl overflow-hidden z-50 max-h-64 overflow-y-auto">
                  <input
                    type="text"
                    placeholder="Buscar agent..."
                    value={agentSearch}
                    onChange={(e) => setAgentSearch(e.target.value)}
                    className="w-full px-4 py-3 bg-white/5 border-b border-white/10 text-white placeholder-gray-500"
                  />
                  <button
                    onClick={() => { setSelectedAgent('auto'); setShowAgentDropdown(false); }}
                    className={`w-full px-4 py-3 text-left hover:bg-white/10 transition ${
                      selectedAgent === 'auto' ? 'bg-purple-500/20 text-purple-400' : 'text-white'
                    }`}
                  >
                    🤖 Automático (ORION decide)
                  </button>
                  {filteredAgents.slice(0, 20).map((agent: Agent) => (
                    <button
                      key={agent.id}
                      onClick={() => { setSelectedAgent(agent.id); setShowAgentDropdown(false); }}
                      className={`w-full px-4 py-3 text-left hover:bg-white/10 transition flex items-center justify-between ${
                        selectedAgent === agent.id ? 'bg-purple-500/20 text-purple-400' : 'text-white'
                      }`}
                    >
                      <span>{agent.name}</span>
                      <span className="text-xs text-gray-500">{agent.squad}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Priority Selector */}
            <div className="mb-4">
              <label className="text-[10px] text-gray-500 uppercase tracking-wider block mb-2">
                Prioridade
              </label>
              <div className="flex gap-2">
                {(['low', 'normal', 'high', 'critical'] as const).map((p) => (
                  <button
                    key={p}
                    onClick={() => setPriority(p)}
                    className={`flex-1 px-3 py-2 rounded-lg text-xs font-bold uppercase transition-all ${
                      priority === p 
                        ? p === 'critical' ? 'bg-red-500 text-white' :
                          p === 'high' ? 'bg-orange-500 text-white' :
                          p === 'normal' ? 'bg-blue-500 text-white' :
                          'bg-gray-500 text-white'
                        : 'bg-white/5 text-gray-400 hover:bg-white/10'
                    }`}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            {/* Text Area */}
            <div className="mb-4">
              <textarea
                ref={terminalRef}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Digite sua task para o ALSHAM QUANTUM processar...&#10;&#10;Exemplo: Analise as tendências de mercado para ecommerce em 2025 e sugira estratégias de growth."
                className="w-full h-40 bg-black/60 border border-white/10 rounded-xl p-4 text-white placeholder-gray-600 font-mono text-sm resize-none focus:border-purple-500/50 focus:outline-none transition-colors"
                disabled={isProcessing}
              />
            </div>

            {/* Quick Actions */}
            <div className="mb-6">
              <label className="text-[10px] text-gray-500 uppercase tracking-wider block mb-2">
                Ações Rápidas
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                {QUICK_ACTIONS.map((action, i) => (
                  <button
                    key={i}
                    onClick={() => setPrompt(action.prompt)}
                    className="px-3 py-2 text-xs bg-white/5 hover:bg-white/10 border border-white/10 hover:border-purple-500/30 rounded-lg text-gray-300 hover:text-white transition-all flex items-center gap-2"
                  >
                    <span>{action.icon}</span>
                    <span className="truncate">{action.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Execute Button */}
            <button
              onClick={executeTask}
              disabled={isProcessing || !prompt.trim()}
              className={`w-full py-4 rounded-xl font-bold text-sm tracking-wider uppercase flex items-center justify-center gap-3 transition-all ${
                isProcessing 
                  ? 'bg-purple-500/20 text-purple-400 cursor-wait'
                  : 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-500 hover:to-pink-500 hover:shadow-[0_0_30px_rgba(168,85,247,0.5)] hover:scale-[1.02]'
              }`}
            >
              {isProcessing ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  PROCESSANDO COM {liveStats.agentsOnline} AGENTS...
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5" />
                  EXECUTAR COM ORION
                </>
              )}
            </button>
          </div>
        </div>

        {/* COLUNA DIREITA - Response Output */}
        <div className="lg:col-span-4 space-y-4">
          <div ref={resultRef} className="bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden">
            {/* Header */}
            <div className="p-4 border-b border-white/10 bg-white/5 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Sparkles className="w-5 h-5 text-cyan-400" />
                <h2 className="text-sm font-bold text-white uppercase tracking-wider">Response Output</h2>
              </div>
              {currentResult && (
                <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${
                  currentResult.success ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                }`}>
                  {currentResult.success ? '✓ SUCCESS' : '✗ FAILED'}
                </span>
              )}
            </div>

            {/* Result Content */}
            <div className="p-4 min-h-[300px] max-h-[500px] overflow-y-auto">
              {currentResult ? (
                <div className="space-y-4">
                  {/* Métricas do resultado */}
                  <div className="grid grid-cols-4 gap-2 mb-4">
                    <div className="bg-white/5 rounded-lg p-2 text-center">
                      <div className="text-lg font-black text-cyan-400">{currentResult.execution_time_ms}ms</div>
                      <div className="text-[9px] text-gray-500 uppercase">Tempo</div>
                    </div>
                    <div className="bg-white/5 rounded-lg p-2 text-center">
                      <div className="text-lg font-black text-purple-400">{currentResult.tokens_used}</div>
                      <div className="text-[9px] text-gray-500 uppercase">Tokens</div>
                    </div>
                    <div className="bg-white/5 rounded-lg p-2 text-center">
                      <div className="text-lg font-black text-green-400">${currentResult.cost_usd?.toFixed(5)}</div>
                      <div className="text-[9px] text-gray-500 uppercase">Custo</div>
                    </div>
                    <div className="bg-white/5 rounded-lg p-2 text-center">
                      <div className="text-sm font-black text-yellow-400 truncate">{currentResult.agent_name?.split(' ')[0]}</div>
                      <div className="text-[9px] text-gray-500 uppercase">Agent</div>
                    </div>
                  </div>

                  {/* Agent Info */}
                  <div className="flex items-center gap-2 text-xs text-gray-500 mb-3">
                    <span className="px-2 py-0.5 bg-purple-500/20 text-purple-400 rounded">{currentResult.agent_name}</span>
                    <span>•</span>
                    <span className="px-2 py-0.5 bg-cyan-500/20 text-cyan-400 rounded">{currentResult.squad}</span>
                  </div>
                  
                  {/* Resultado */}
                  <div className="bg-black/40 border border-white/10 rounded-xl p-4">
                    <p className="text-white font-mono text-sm leading-relaxed whitespace-pre-wrap">
                      {currentResult.result}
                    </p>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex flex-wrap gap-2">
                    <button 
                      onClick={copyResult}
                      className="flex items-center gap-2 px-3 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-xs text-gray-300 transition-all"
                    >
                      <Copy className="w-3 h-3" /> Copiar
                    </button>
                    <button className="flex items-center gap-2 px-3 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-xs text-gray-300 transition-all">
                      <FileDown className="w-3 h-3" /> Salvar PDF
                    </button>
                    <button className="flex items-center gap-2 px-3 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-xs text-gray-300 transition-all">
                      <MessageSquare className="w-3 h-3" /> WhatsApp
                    </button>
                    <button className="flex items-center gap-2 px-3 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-xs text-gray-300 transition-all">
                      <Mail className="w-3 h-3" /> Email
                    </button>
                  </div>

                  {/* Neural Load Graph (Fake animation) */}
                  <div className="mt-4">
                    <div className="text-[10px] text-gray-500 uppercase tracking-wider mb-2 flex items-center gap-2">
                      <Activity className="w-3 h-3" />
                      Neural Load durante execução
                    </div>
                    <div className="h-12 bg-white/5 rounded-lg overflow-hidden flex items-end gap-px p-2">
                      {Array.from({ length: 30 }).map((_, i) => (
                        <div
                          key={i}
                          className="flex-1 bg-gradient-to-t from-purple-500 to-cyan-500 rounded-t transition-all"
                          style={{ 
                            height: `${Math.random() * 60 + 40}%`,
                            animationDelay: `${i * 50}ms`
                          }}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-gray-600 py-16">
                  <Brain className="w-20 h-20 mb-4 opacity-20" />
                  <p className="text-sm font-medium">Aguardando comando...</p>
                  <p className="text-xs mt-1 text-gray-700">O Quantum Brain está pronto para processar</p>
                </div>
              )}
            </div>
          </div>

          {/* Emergency Controls */}
          <div className="bg-black/40 backdrop-blur-xl border border-red-500/20 rounded-2xl p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <AlertOctagon className="w-5 h-5 text-red-500" />
                <span className="text-sm font-bold text-red-400">Emergency Controls</span>
              </div>
              <button className="px-4 py-2 bg-red-500/20 hover:bg-red-500 border border-red-500 rounded-lg text-red-400 hover:text-white text-xs font-bold uppercase tracking-wider transition-all">
                EMERGENCY STOP
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
