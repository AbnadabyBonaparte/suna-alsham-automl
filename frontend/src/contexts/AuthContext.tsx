"use client";

/**
 * @deprecated AuthContext foi removido. Use useAuthStore de '@/stores/useAuthStore'.
 *
 * Este arquivo mantém apenas o re-export para retrocompatibilidade,
 * mas NÃO contém mock users, mock sessions ou qualquer dado fake.
 *
 * ADR-006: Zustand é o único mecanismo de state management.
 */

export { useAuthStore as useAuth } from '@/stores/useAuthStore';
