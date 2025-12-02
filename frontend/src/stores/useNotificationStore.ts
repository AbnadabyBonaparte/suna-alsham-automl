/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - NOTIFICATION STORE
 * ═══════════════════════════════════════════════════════════════
 * Global toast notification system with Zustand + DevTools
 * ═══════════════════════════════════════════════════════════════
 */

import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message?: string;
  duration?: number; // milliseconds, 0 = no auto-dismiss
  timestamp: number;
}

interface NotificationStore {
  notifications: Notification[];
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  clearAll: () => void;
}

export const useNotificationStore = create<NotificationStore>()(
  devtools(
    (set) => ({
      notifications: [],

      addNotification: (notification) => {
        const id = `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        const newNotification: Notification = {
          ...notification,
          id,
          timestamp: Date.now(),
          duration: notification.duration ?? 5000, // Default 5s
        };

        set(
          (state) => ({
            notifications: [...state.notifications, newNotification],
          }),
          false,
          'ADD_NOTIFICATION'
        );

        // Auto-dismiss
        if (newNotification.duration && newNotification.duration > 0) {
          setTimeout(() => {
            set(
              (state) => ({
                notifications: state.notifications.filter((n) => n.id !== id),
              }),
              false,
              'AUTO_DISMISS_NOTIFICATION'
            );
          }, newNotification.duration);
        }
      },

      removeNotification: (id) =>
        set(
          (state) => ({
            notifications: state.notifications.filter((n) => n.id !== id),
          }),
          false,
          'REMOVE_NOTIFICATION'
        ),

      clearAll: () =>
        set(
          { notifications: [] },
          false,
          'CLEAR_ALL_NOTIFICATIONS'
        ),
    }),
    { name: 'NotificationStore' }
  )
);
