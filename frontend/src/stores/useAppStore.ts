import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  timestamp: number;
}

interface AppStore {
  // Global app state
  isOnline: boolean;
  lastSync: number | null;
  notifications: Notification[];
  
  // System health
  systemHealth: 'healthy' | 'degraded' | 'down';
  
  // Actions
  setOnline: (online: boolean) => void;
  setLastSync: (timestamp: number) => void;
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
  setSystemHealth: (health: 'healthy' | 'degraded' | 'down') => void;
}

export const useAppStore = create<AppStore>()(
  devtools(
    (set) => ({
      isOnline: true,
      lastSync: null,
      notifications: [],
      systemHealth: 'healthy',
      
      setOnline: (online) => set({ isOnline: online }, false, 'app/setOnline'),
      
      setLastSync: (timestamp) => set({ lastSync: timestamp }, false, 'app/setLastSync'),
      
      addNotification: (notification) => set((state) => ({
        notifications: [
          ...state.notifications,
          {
            ...notification,
            id: `notif-${Date.now()}-${Math.random()}`,
            timestamp: Date.now(),
          }
        ]
      }), false, 'app/addNotification'),
      
      removeNotification: (id) => set((state) => ({
        notifications: state.notifications.filter(n => n.id !== id)
      }), false, 'app/removeNotification'),
      
      clearNotifications: () => set({ notifications: [] }, false, 'app/clearNotifications'),
      
      setSystemHealth: (health) => set({ systemHealth: health }, false, 'app/setSystemHealth'),
    }),
    { name: 'AppStore' }
  )
);
