'use client';

import { useEffect } from 'react';
import { useUIStore } from '@/stores/useUIStore';

export function ThemeHydrator() {
  const currentTheme = useUIStore((s) => s.currentTheme);
  const applyTheme = useUIStore((s) => s.applyTheme);

  useEffect(() => {
    applyTheme();
  }, [currentTheme, applyTheme]);

  return null;
}
