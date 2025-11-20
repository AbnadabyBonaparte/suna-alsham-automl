export type AgentRole = 'CORE' | 'GUARD' | 'SPECIALIST' | 'ANALYST';
export type AgentStatus = 'IDLE' | 'PROCESSING' | 'LEARNING' | 'WARNING' | 'ERROR';

export interface Agent {
  id: string;
  name: string;
  role: AgentRole;
  status: AgentStatus;
  efficiency: number;
  currentTask: string;
  lastActive: string;
}

export interface SystemMetrics {
  roi: number;
  savings: number;
  activeAgents: number;
  systemLoad: number;
  quantumStability: number;
}

export interface QuantumState {
  agents: Agent[];
  metrics: SystemMetrics;
  isLive: boolean;
  toggleLiveMode: () => void;
  updateMetrics: (newMetrics: Partial<SystemMetrics>) => void;
  updateAgent: (id: string, data: Partial<Agent>) => void;
  simulatePulse: () => void;
}
