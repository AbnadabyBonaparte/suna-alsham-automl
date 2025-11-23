// frontend/src/lib/analytics.ts
// Reality Codex - Analytics & Tracking

type EventCategory = 'Theme' | 'UI' | 'Accessibility' | 'Performance';

interface AnalyticsEvent {
  event: string;
  event_category: EventCategory;
  event_label?: string;
  [key: string]: unknown;
}

function track(eventData: AnalyticsEvent) {
  if (typeof window !== 'undefined') {
    // Google Analytics 4
    if ((window as unknown as { gtag?: Function }).gtag) {
      (window as unknown as { gtag: Function }).gtag('event', eventData.event, eventData);
    }
    
    // Vercel Analytics
    if ((window as unknown as { va?: Function }).va) {
      (window as unknown as { va: Function }).va('event', { name: eventData.event, ...eventData });
    }
    
    // Console in development
    if (process.env.NODE_ENV === 'development') {
      console.log('[Analytics]', eventData);
    }
  }
}

export function trackThemeChange(themeId: string, themeName: string) {
  track({
    event: 'theme_change',
    event_category: 'Theme',
    event_label: themeName,
    theme_id: themeId,
    timestamp: new Date().toISOString(),
  });
}

export function trackThemeSwitcherOpen() {
  track({
    event: 'theme_switcher_open',
    event_category: 'UI',
  });
}

export function trackKeyboardShortcut(shortcut: string) {
  track({
    event: 'keyboard_shortcut',
    event_category: 'Accessibility',
    event_label: shortcut,
  });
}

export function trackPerformanceMetric(metric: string, value: number) {
  track({
    event: 'performance_metric',
    event_category: 'Performance',
    event_label: metric,
    value: Math.round(value),
  });
}
