import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export interface Request {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  priority: 'low' | 'normal' | 'high';
  created_at: string;
  updated_at: string;
}

interface RequestsStore {
  requests: Request[];
  loading: boolean;
  error: string | null;
  
  setRequests: (requests: Request[]) => void;
  addRequest: (request: Request) => void;
  updateRequest: (id: string, updates: Partial<Request>) => void;
  deleteRequest: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useRequestsStore = create<RequestsStore>()(
  devtools(
    (set) => ({
      requests: [],
      loading: false,
      error: null,
      
      setRequests: (requests) => set({ requests }, false, 'requests/setRequests'),
      
      addRequest: (request) => set((state) => ({
        requests: [request, ...state.requests]
      }), false, 'requests/addRequest'),
      
      updateRequest: (id, updates) => set((state) => ({
        requests: state.requests.map(r => 
          r.id === id ? { ...r, ...updates } : r
        )
      }), false, 'requests/updateRequest'),
      
      deleteRequest: (id) => set((state) => ({
        requests: state.requests.filter(r => r.id !== id)
      }), false, 'requests/deleteRequest'),
      
      setLoading: (loading) => set({ loading }, false, 'requests/setLoading'),
      setError: (error) => set({ error }, false, 'requests/setError'),
    }),
    { name: 'RequestsStore' }
  )
);
