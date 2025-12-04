// ═══════════════════════════════════════════════════════════════
// ALSHAM QUANTUM - TIPOS ADAPTADOS À ESTRUTURA EXISTENTE
// ═══════════════════════════════════════════════════════════════

// Status que JÁ EXISTEM no banco
export type AgentStatus = 'ACTIVE' | 'IDLE' | 'WARNING' | 'ERROR';
export type AgentRole = 'CORE' | 'GUARD' | 'ANALYST' | 'SPECIALIST';
export type TaskStatus = 'queued' | 'processing' | 'completed' | 'failed';
export type BrainStatus = 'initializing' | 'active' | 'evolving' | 'maintenance';

// Mapeamento ROLE → SQUAD (para UI)
export const ROLE_TO_SQUAD: Record<AgentRole, string> = {
  CORE: 'COMMAND',      // Coordenadores centrais
  GUARD: 'SENTINEL',    // Segurança e proteção
  ANALYST: 'ORACLE',    // Análise e dados
  SPECIALIST: 'NEXUS',  // Especialistas diversos
};

export const SQUAD_COLORS: Record<string, string> = {
  COMMAND: '#FFD700',   // Dourado
  SENTINEL: '#EF4444',  // Vermelho
  ORACLE: '#8B5CF6',    // Roxo
  NEXUS: '#10B981',     // Verde
};

// Interface que RESPEITA a estrutura existente do banco
export interface Agent {
  id: string;                    // text (ex: 'orc-alpha' ou UUID)
  name: string;                  // text
  role: AgentRole;               // text (CORE, GUARD, ANALYST, SPECIALIST)
  status: AgentStatus;           // text
  efficiency: number;            // numeric (0-100) - É O QUE VOCÊS CHAMAM DE PERFORMANCE
  current_task: string;          // text
  last_active: string;           // text (timestamp como string)
  neural_load: number;           // numeric (0-100)
  uptime_seconds: number;        // bigint
  version: string;               // text
  metadata: Record<string, any>; // jsonb - GUARDAR system_prompt AQUI
  created_at: string;
  updated_at: string;
}

// Request existente (FILA)
export interface Request {
  id: string;
  user_id: string;
  title: string;          // Tipo da tarefa
  description: string;    // Detalhes
  status: TaskStatus;
  priority: 'low' | 'normal' | 'high' | 'critical';
  created_at: string;
  updated_at: string;
}

// Task executada (NOVA - com métricas)
export interface QuantumTask {
  id: string;
  request_id?: string;
  agent_id: string;
  input: Record<string, any>;
  output?: Record<string, any>;
  status: TaskStatus;
  error_message?: string;
  execution_time_ms?: number;
  tokens_used?: number;
  cost_usd?: number;
  model_used: string;
  created_at: string;
  started_at: string;
  completed_at?: string;
}

// Estado do cérebro
export interface QuantumBrainState {
  id: string;
  status: BrainStatus;
  total_agents: number;
  active_agents: number;
  tasks_processed_today: number;
  tasks_processed_total: number;
  tasks_in_queue: number;
  average_efficiency: number;
  average_response_time_ms: number;
  success_rate: number;
  last_evolution_at?: string;
  current_evolution_cycle: number;
  uptime_started_at: string;
  uptime_seconds?: number; // Calculado
}

// Stats por role/squad
export interface RoleStats {
  role: AgentRole;
  squad: string;
  color: string;
  total_agents: number;
  active_agents: number;
  average_efficiency: number;
  tasks_today: number;
}

// Métricas em tempo real
export interface RealTimeMetrics {
  timestamp: string;
  tasks_per_minute: number;
  active_agents: number;
  queue_size: number;
  average_latency_ms: number;
  error_rate: number;
  top_agents: { id: string; name: string; efficiency: number }[];
}
