import { create } from 'zustand';

interface Agent {
  id: string;
  name: string;
  role: string;
  status: string;
  efficiency: number;
  current_task: string;
}

interface AgentsStore {
  agents: Agent[];
  loading: boolean;
  error: string | null;
  filteredSquad: string | null;
  searchQuery: string;
  setAgents: (agents: Agent[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setFilteredSquad: (squad: string | null) => void;
  setSearchQuery: (query: string) => void;
  getFilteredAgents: () => Agent[];
}

export const useAgentsStore = create<AgentsStore>((set, get) => ({
  agents: [],
  loading: false,
  error: null,
  filteredSquad: null,
  searchQuery: '',
  
  setAgents: (agents) => set({ agents }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  setFilteredSquad: (squad) => set({ filteredSquad: squad }),
  setSearchQuery: (query) => set({ searchQuery: query }),
  
  getFilteredAgents: () => {
    const { agents, filteredSquad, searchQuery } = get();
    let filtered = agents;
    
    if (filteredSquad) {
      filtered = filtered.filter(a => a.role === filteredSquad);
    }
    
    if (searchQuery) {
      filtered = filtered.filter(a => 
        a.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        a.current_task?.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    
    return filtered;
  },
}));
