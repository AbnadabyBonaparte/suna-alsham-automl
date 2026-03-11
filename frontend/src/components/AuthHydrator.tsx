'use client';

import { useEffect } from 'react';
import { useAuthStore } from '@/stores/useAuthStore';

export function AuthHydrator() {
  const initAuth = useAuthStore((s) => s.initAuth);

  useEffect(() => {
    const cleanup = initAuth();
    return cleanup;
  }, [initAuth]);

  return null;
}
