/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - QUANTUM BRAIN GODMODE (THEME-AWARE)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/quantum-brain/page.tsx
 * 🧠 Central de Comando - O Trono do ALSHAM QUANTUM
 * 🎨 100% SUBMISSO AOS TEMAS - USA VARIÁVEIS CSS
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

// Squads disponíveis - USANDO VARIÁVEIS CSS
const SQUADS = [
  { id: 'COMMAND', name: 'COMMAND', icon: Crown },
  { id: 'VOID', name: 'VOID', icon: Eye },
  { id: 'NEXUS', name: 'NEXUS', icon: Network },
  { id: 'SENTINEL', name: 'SENTINEL', icon: Shield },
  { id: 'CHAOS', name: 'CHAOS', icon: AlertOctagon },
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
    if (statusFilter !== 'all' && task.status !== statusFilter) return false;
    
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
      <div 
        className="fixed inset-0 pointer-events-none"
        style={{ background: 'linear-gradient(to bottom right, var(--color-primary)/10, transparent, var(--color-secondary)/10)' }}
      />
      
      {/* TOP BAR - Métricas ao Vivo */}
      <div 
        className="sticky top-0 z-40 backdrop-blur-xl px-6 py-3"
        style={{ 
          background: 'var(--color-background)/80',
          borderBottom: '1px solid var(--color-border)/10'
        }}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div 
                className="absolute -inset-2 rounded-full blur-xl animate-pulse"
                style={{ background: 'var(--color-primary)/20' }}
              />
              <Brain className="w-8 h-8 relative" style={{ color: 'var(--color-primary)' }} />
            </div>
            <div>
              <h1 className="text-xl font-black tracking-tight flex items-center gap-2" style={{ color: 'var(--color-text)' }}>
                QUANTUM BRAIN
                <span 
                  className="px-2 py-0.5 text-[10px] font-bold text-white rounded-full animate-pulse"
                  style={{ background: 'linear-gradient(to right, var(--color-primary), var(--color-accent))' }}
                >
                  GODMODE
                </span>
              </h1>
              <p className="text-[10px] font-mono" style={{ color: 'var(--color-text-secondary)' }}>
                O Trono do ALSHAM QUANTUM • 139 Agents Sincronizados
              </p>
            </div>
          </div>
          
          {/* Live Stats */}
          <div className="hidden lg:flex items-center gap-6">
            <div 
              className="flex items-center gap-2 px-3 py-1 rounded-lg"
              style={{ 
                background: 'var(--color-success)/10',
                border: '1px solid var(--color-success)/30'
              }}
            >
              <div className="w-2 h-2 rounded-full animate-pulse" style={{ background: 'var(--color-success)' }} />
              <span className="text-xs font-bold" style={{ color: 'var(--color-success)' }}>
                {liveStats.agentsOnline} Agents Online
              </span>
            </div>
            
            <div className="text-center">
              <div className="text-sm font-black" style={{ color: 'var(--color-accent)' }}>
                {(liveStats.avgResponse / 1000).toFixed(1)}s
              </div>
              <div className="text-[9px] uppercase" style={{ color: 'var(--color-text-secondary)' }}>Avg Response</div>
            </div>
            
            <div className="text-center">
              <div className="text-sm font-black" style={{ color: 'var(--color-success)' }}>
                R${(liveStats.avgCost * 5.5).toFixed(4)}
              </div>
              <div className="text-[9px] uppercase" style={{ color: 'var(--color-text-secondary)' }}>Avg Cost</div>
            </div>
            
            <div className="text-center">
              <div className="text-sm font-black" style={{ color: 'var(--color-primary)' }}>
                {liveStats.tasksToday}
              </div>
              <div className="text-[9px] uppercase" style={{ color: 'var(--color-text-secondary)' }}>Tasks Today</div>
            </div>
            
            <div className="text-center">
              <div className="text-sm font-black" style={{ color: 'var(--color-warning)' }}>
                {liveStats.syncRate.toFixed(1)}%
              </div>
              <div className="text-[9px] uppercase" style={{ color: 'var(--color-text-secondary)' }}>Sync Rate</div>
            </div>
            
            <div className="flex items-center gap-2">
              <Gauge className="w-4 h-4" style={{ color: 'var(--color-warning)' }} />
              <div className="w-20 h-2 rounded-full overflow-hidden" style={{ background: 'var(--color-surface)' }}>
                <div 
                  className="h-full transition-all duration-500"
                  style={{ 
                    width: `${liveStats.neuralPower}%`,
                    background: 'linear-gradient(to right, var(--color-warning), var(--color-error))'
                  }}
                />
              </div>
              <span className="text-xs font-mono" style={{ color: 'var(--color-warning)' }}>{liveStats.neuralPower}%</span>
            </div>
          </div>
          
          {/* God View Toggle */}
          <button
            onClick={() => setGodViewMode(!godViewMode)}
            className="px-4 py-2 rounded-lg font-bold text-xs uppercase tracking-wider transition-all flex items-center gap-2"
            style={{
              background: godViewMode ? 'var(--color-primary)' : 'var(--color-surface)',
              color: godViewMode ? 'var(--color-background)' : 'var(--color-text-secondary)',
              boxShadow: godViewMode ? '0 0 20px var(--color-glow)/50' : 'none',
              border: `1px solid ${godViewMode ? 'var(--color-primary)' : 'var(--color-border)/20'}`
            }}
          >
            <Eye className="w-4 h-4" />
            God View
          </button>
        </div>
      </div>

      {/* GOD VIEW MODE */}
      {godViewMode && (
        <div className="fixed inset-0 z-50 backdrop-blur-xl overflow-auto p-6" style={{ background: 'var(--color-background)/95' }}>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-black flex items-center gap-3" style={{ color: 'var(--color-text)' }}>
              <Eye className="w-6 h-6" style={{ color: 'var(--color-primary)' }} />
              GOD VIEW - {agents?.length || 139} AGENTS
            </h2>
            <button
              onClick={() => setGodViewMode(false)}
              className="p-2 rounded-lg transition"
              style={{ background: 'var(--color-surface)', color: 'var(--color-text)' }}
            >
              <X className="w-6 h-6" />
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
                className="p-3 rounded-xl transition-all hover:scale-105 cursor-pointer"
                style={{
                  background: agent.status === 'active' ? 'var(--color-success)/10' : 'var(--color-surface)',
                  border: `1px solid ${agent.status === 'active' ? 'var(--color-success)/30' : 'var(--color-border)/10'}`
                }}
              >
                <div 
                  className={`w-3 h-3 rounded-full mb-2 ${agent.status === 'active' ? 'animate-pulse' : ''}`}
                  style={{ background: agent.status === 'active' ? 'var(--color-success)' : 'var(--color-text-secondary)/30' }}
                />
                <div className="text-[10px] font-bold truncate" style={{ color: 'var(--color-text)' }}>{agent.name}</div>
                <div className="text-[9px]" style={{ color: 'var(--color-text-secondary)' }}>{agent.efficiency || 85}%</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* MAIN CONTENT - 3 Colunas */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 p-6">
        
        {/* COLUNA ESQUERDA - Histórico */}
        <div className="lg:col-span-3 space-y-4">
          <div 
            className="backdrop-blur-xl rounded-2xl overflow-hidden"
            style={{ 
              background: 'var(--color-surface)/40',
              border: '1px solid var(--color-border)/10'
            }}
          >
            {/* Header */}
            <div className="p-4" style={{ borderBottom: '1px solid var(--color-border)/10', background: 'var(--color-surface)/50' }}>
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-sm font-bold uppercase tracking-wider flex items-center gap-2" style={{ color: 'var(--color-text)' }}>
                  <History className="w-4 h-4" style={{ color: 'var(--color-primary)' }} />
                  Histórico
                </h2>
                <span className="text-xs" style={{ color: 'var(--color-text-secondary)' }}>{filteredHistory.length} tasks</span>
              </div>
              
              {/* Filtros */}
              <div className="flex gap-2">
                <select
                  value={historyFilter}
                  onChange={(e) => setHistoryFilter(e.target.value as any)}
                  className="flex-1 px-2 py-1 text-xs rounded-lg"
                  style={{ 
                    background: 'var(--color-surface)',
                    border: '1px solid var(--color-border)/20',
                    color: 'var(--color-text)'
                  }}
                >
                  <option value="all">Todos</option>
                  <option value="today">Hoje</option>
                  <option value="week">Semana</option>
                </select>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value as any)}
                  className="flex-1 px-2 py-1 text-xs rounded-lg"
                  style={{ 
                    background: 'var(--color-surface)',
                    border: '1px solid var(--color-border)/20',
                    color: 'var(--color-text)'
                  }}
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
                <div className="p-8 text-center" style={{ color: 'var(--color-text-secondary)' }}>
                  <History className="w-12 h-12 mx-auto mb-3 opacity-20" />
                  <p className="text-sm">Nenhuma task encontrada</p>
                </div>
              ) : (
                filteredHistory.map((task, i) => (
                  <div
                    key={task.id || i}
                    onClick={() => setCurrentResult(task)}
                    className="p-4 cursor-pointer transition-all"
                    style={{
                      borderBottom: '1px solid var(--color-border)/5',
                      background: currentResult?.id === task.id ? 'var(--color-primary)/10' : 'transparent',
                      borderLeft: currentResult?.id === task.id ? '2px solid var(--color-primary)' : 'none'
                    }}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div 
                        className={`w-2 h-2 rounded-full mt-1.5 ${task.status === 'processing' ? 'animate-pulse' : ''}`}
                        style={{
                          background: task.status === 'completed' ? 'var(--color-success)' : 
                                     task.status === 'failed' ? 'var(--color-error)' : 'var(--color-warning)'
                        }}
                      />
                      <span className="text-[10px] font-mono" style={{ color: 'var(--color-text-secondary)' }}>
                        {new Date(task.timestamp).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                    <p className="text-sm font-medium truncate mb-1" style={{ color: 'var(--color-text)' }}>
                      {task.title || task.result?.slice(0, 50)}
                    </p>
                    <div className="flex items-center gap-2 text-[10px]" style={{ color: 'var(--color-text-secondary)' }}>
                      <span 
                        className="px-1.5 py-0.5 rounded"
                        style={{ background: 'var(--color-primary)/20', color: 'var(--color-primary)' }}
                      >
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
          <div 
            className="backdrop-blur-xl rounded-2xl p-6"
            style={{ 
              background: 'var(--color-surface)/40',
              border: '1px solid var(--color-border)/10'
            }}
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <Terminal className="w-5 h-5" style={{ color: 'var(--color-primary)' }} />
                <h2 className="text-lg font-bold" style={{ color: 'var(--color-text)' }}>Command Terminal</h2>
              </div>
              <button
                onClick={() => setMultiAgentMode(!multiAgentMode)}
                className="px-3 py-1.5 rounded-lg text-xs font-bold transition-all"
                style={{
                  background: multiAgentMode ? 'var(--color-primary)' : 'var(--color-surface)',
                  color: multiAgentMode ? 'var(--color-background)' : 'var(--color-text-secondary)',
                  border: `1px solid ${multiAgentMode ? 'var(--color-primary)' : 'var(--color-border)/20'}`
                }}
              >
                <Users className="w-3 h-3 inline mr-1" />
                Multi-Agent
              </button>
            </div>

            {/* Agent Selector */}
            <div className="mb-4 relative">
              <label className="text-[10px] uppercase tracking-wider block mb-2" style={{ color: 'var(--color-text-secondary)' }}>
                Selecionar Agent
              </label>
              <button
                onClick={() => setShowAgentDropdown(!showAgentDropdown)}
                className="w-full px-4 py-3 rounded-xl text-left flex items-center justify-between transition-all"
                style={{
                  background: 'var(--color-surface)',
                  border: '1px solid var(--color-border)/20',
                  color: 'var(--color-text)'
                }}
              >
                <span>
                  {selectedAgent === 'auto' ? '🤖 Automático (ORION decide)' : 
                   agents?.find((a: Agent) => a.id === selectedAgent)?.name || selectedAgent}
                </span>
                <ChevronDown className={`w-4 h-4 transition-transform ${showAgentDropdown ? 'rotate-180' : ''}`} style={{ color: 'var(--color-text-secondary)' }} />
              </button>
              
              {showAgentDropdown && (
                <div 
                  className="absolute top-full left-0 right-0 mt-2 rounded-xl overflow-hidden z-50 max-h-64 overflow-y-auto"
                  style={{ 
                    background: 'var(--color-background)/95',
                    border: '1px solid var(--color-border)/20'
                  }}
                >
                  <input
                    type="text"
                    placeholder="Buscar agent..."
                    value={agentSearch}
                    onChange={(e) => setAgentSearch(e.target.value)}
                    className="w-full px-4 py-3"
                    style={{ 
                      background: 'var(--color-surface)',
                      borderBottom: '1px solid var(--color-border)/10',
                      color: 'var(--color-text)'
                    }}
                  />
                  <button
                    onClick={() => { setSelectedAgent('auto'); setShowAgentDropdown(false); }}
                    className="w-full px-4 py-3 text-left transition"
                    style={{
                      background: selectedAgent === 'auto' ? 'var(--color-primary)/20' : 'transparent',
                      color: selectedAgent === 'auto' ? 'var(--color-primary)' : 'var(--color-text)'
                    }}
                  >
                    🤖 Automático (ORION decide)
                  </button>
                  {filteredAgents.slice(0, 20).map((agent: Agent) => (
                    <button
                      key={agent.id}
                      onClick={() => { setSelectedAgent(agent.id); setShowAgentDropdown(false); }}
                      className="w-full px-4 py-3 text-left transition flex items-center justify-between"
                      style={{
                        background: selectedAgent === agent.id ? 'var(--color-primary)/20' : 'transparent',
                        color: selectedAgent === agent.id ? 'var(--color-primary)' : 'var(--color-text)'
                      }}
                    >
                      <span>{agent.name}</span>
                      <span className="text-xs" style={{ color: 'var(--color-text-secondary)' }}>{agent.squad}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Priority Selector */}
            <div className="mb-4">
              <label className="text-[10px] uppercase tracking-wider block mb-2" style={{ color: 'var(--color-text-secondary)' }}>
                Prioridade
              </label>
              <div className="flex gap-2">
                {(['low', 'normal', 'high', 'critical'] as const).map((p) => (
                  <button
                    key={p}
                    onClick={() => setPriority(p)}
                    className="flex-1 px-3 py-2 rounded-lg text-xs font-bold uppercase transition-all"
                    style={{
                      background: priority === p 
                        ? p === 'critical' ? 'var(--color-error)' :
                          p === 'high' ? 'var(--color-warning)' :
                          p === 'normal' ? 'var(--color-primary)' :
                          'var(--color-text-secondary)'
                        : 'var(--color-surface)',
                      color: priority === p ? 'white' : 'var(--color-text-secondary)',
                      border: `1px solid ${priority === p ? 'transparent' : 'var(--color-border)/20'}`
                    }}
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
                className="w-full h-40 rounded-xl p-4 font-mono text-sm resize-none focus:outline-none transition-colors"
                style={{
                  background: 'var(--color-background)/60',
                  border: '1px solid var(--color-border)/10',
                  color: 'var(--color-text)'
                }}
                disabled={isProcessing}
              />
            </div>

            {/* Quick Actions */}
            <div className="mb-6">
              <label className="text-[10px] uppercase tracking-wider block mb-2" style={{ color: 'var(--color-text-secondary)' }}>
                Ações Rápidas
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                {QUICK_ACTIONS.map((action, i) => (
                  <button
                    key={i}
                    onClick={() => setPrompt(action.prompt)}
                    className="px-3 py-2 text-xs rounded-lg transition-all flex items-center gap-2"
                    style={{
                      background: 'var(--color-surface)',
                      border: '1px solid var(--color-border)/10',
                      color: 'var(--color-text-secondary)'
                    }}
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
              className="w-full py-4 rounded-xl font-bold text-sm tracking-wider uppercase flex items-center justify-center gap-3 transition-all disabled:opacity-50"
              style={{
                background: isProcessing 
                  ? 'var(--color-primary)/20'
                  : 'linear-gradient(to right, var(--color-primary), var(--color-accent))',
                color: isProcessing ? 'var(--color-primary)' : 'white',
                boxShadow: isProcessing ? 'none' : '0 0 30px var(--color-glow)/50'
              }}
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
          <div 
            ref={resultRef} 
            className="backdrop-blur-xl rounded-2xl overflow-hidden"
            style={{ 
              background: 'var(--color-surface)/40',
              border: '1px solid var(--color-border)/10'
            }}
          >
            {/* Header */}
            <div 
              className="p-4 flex items-center justify-between"
              style={{ 
                borderBottom: '1px solid var(--color-border)/10',
                background: 'var(--color-surface)/50'
              }}
            >
              <div className="flex items-center gap-3">
                <Sparkles className="w-5 h-5" style={{ color: 'var(--color-accent)' }} />
                <h2 className="text-sm font-bold uppercase tracking-wider" style={{ color: 'var(--color-text)' }}>Response Output</h2>
              </div>
              {currentResult && (
                <span 
                  className="px-2 py-1 rounded text-[10px] font-bold uppercase"
                  style={{
                    background: currentResult.success ? 'var(--color-success)/20' : 'var(--color-error)/20',
                    color: currentResult.success ? 'var(--color-success)' : 'var(--color-error)'
                  }}
                >
                  {currentResult.success ? '✓ SUCCESS' : '✗ FAILED'}
                </span>
              )}
            </div>

            {/* Result Content */}
            <div className="p-4 min-h-[300px] max-h-[500px] overflow-y-auto">
              {currentResult ? (
                <div className="space-y-4">
                  {/* Métricas */}
                  <div className="grid grid-cols-4 gap-2 mb-4">
                    <div className="rounded-lg p-2 text-center" style={{ background: 'var(--color-surface)' }}>
                      <div className="text-lg font-black" style={{ color: 'var(--color-accent)' }}>{currentResult.execution_time_ms}ms</div>
                      <div className="text-[9px] uppercase" style={{ color: 'var(--color-text-secondary)' }}>Tempo</div>
                    </div>
                    <div className="rounded-lg p-2 text-center" style={{ background: 'var(--color-surface)' }}>
                      <div className="text-lg font-black" style={{ color: 'var(--color-primary)' }}>{currentResult.tokens_used}</div>
                      <div className="text-[9px] uppercase" style={{ color: 'var(--color-text-secondary)' }}>Tokens</div>
                    </div>
                    <div className="rounded-lg p-2 text-center" style={{ background: 'var(--color-surface)' }}>
                      <div className="text-lg font-black" style={{ color: 'var(--color-success)' }}>${currentResult.cost_usd?.toFixed(5)}</div>
                      <div className="text-[9px] uppercase" style={{ color: 'var(--color-text-secondary)' }}>Custo</div>
                    </div>
                    <div className="rounded-lg p-2 text-center" style={{ background: 'var(--color-surface)' }}>
                      <div className="text-sm font-black truncate" style={{ color: 'var(--color-warning)' }}>{currentResult.agent_name?.split(' ')[0]}</div>
                      <div className="text-[9px] uppercase" style={{ color: 'var(--color-text-secondary)' }}>Agent</div>
                    </div>
                  </div>

                  {/* Agent Info */}
                  <div className="flex items-center gap-2 text-xs mb-3" style={{ color: 'var(--color-text-secondary)' }}>
                    <span className="px-2 py-0.5 rounded" style={{ background: 'var(--color-primary)/20', color: 'var(--color-primary)' }}>
                      {currentResult.agent_name}
                    </span>
                    <span>•</span>
                    <span className="px-2 py-0.5 rounded" style={{ background: 'var(--color-accent)/20', color: 'var(--color-accent)' }}>
                      {currentResult.squad}
                    </span>
                  </div>
                  
                  {/* Resultado */}
                  <div 
                    className="rounded-xl p-4"
                    style={{
                      background: 'var(--color-background)/40',
                      border: '1px solid var(--color-border)/10'
                    }}
                  >
                    <p className="font-mono text-sm leading-relaxed whitespace-pre-wrap" style={{ color: 'var(--color-text)' }}>
                      {currentResult.result}
                    </p>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex flex-wrap gap-2">
                    {[
                      { icon: Copy, label: 'Copiar', onClick: copyResult },
                      { icon: FileDown, label: 'Salvar PDF' },
                      { icon: MessageSquare, label: 'WhatsApp' },
                      { icon: Mail, label: 'Email' },
                    ].map((btn, i) => (
                      <button 
                        key={i}
                        onClick={btn.onClick}
                        className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs transition-all"
                        style={{
                          background: 'var(--color-surface)',
                          border: '1px solid var(--color-border)/10',
                          color: 'var(--color-text-secondary)'
                        }}
                      >
                        <btn.icon className="w-3 h-3" /> {btn.label}
                      </button>
                    ))}
                  </div>

                  {/* Neural Load Graph */}
                  <div className="mt-4">
                    <div className="text-[10px] uppercase tracking-wider mb-2 flex items-center gap-2" style={{ color: 'var(--color-text-secondary)' }}>
                      <Activity className="w-3 h-3" />
                      Neural Load durante execução
                    </div>
                    <div className="h-12 rounded-lg overflow-hidden flex items-end gap-px p-2" style={{ background: 'var(--color-surface)' }}>
                      {Array.from({ length: 30 }).map((_, i) => (
                        <div
                          key={i}
                          className="flex-1 rounded-t transition-all"
                          style={{ 
                            height: `${Math.random() * 60 + 40}%`,
                            background: 'linear-gradient(to top, var(--color-primary), var(--color-accent))',
                            animationDelay: `${i * 50}ms`
                          }}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="h-full flex flex-col items-center justify-center py-16" style={{ color: 'var(--color-text-secondary)' }}>
                  <Brain className="w-20 h-20 mb-4 opacity-20" />
                  <p className="text-sm font-medium">Aguardando comando...</p>
                  <p className="text-xs mt-1" style={{ color: 'var(--color-text-secondary)/70' }}>O Quantum Brain está pronto para processar</p>
                </div>
              )}
            </div>
          </div>

          {/* Emergency Controls */}
          <div 
            className="backdrop-blur-xl rounded-2xl p-4"
            style={{ 
              background: 'var(--color-surface)/40',
              border: '1px solid var(--color-error)/20'
            }}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <AlertOctagon className="w-5 h-5" style={{ color: 'var(--color-error)' }} />
                <span className="text-sm font-bold" style={{ color: 'var(--color-error)' }}>Emergency Controls</span>
              </div>
              <button 
                className="px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider transition-all"
                style={{
                  background: 'var(--color-error)/20',
                  border: '1px solid var(--color-error)',
                  color: 'var(--color-error)'
                }}
              >
                EMERGENCY STOP
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
