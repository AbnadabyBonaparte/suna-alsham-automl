/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SIDEBAR COMPLETA (21 PÁGINAS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/layout/Sidebar.tsx
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  Users, 
  Network,
  Activity,
  Sparkles,
  Wallet,
  Trophy,
  MessageSquare,
  Terminal,
  Shield,
  Settings,
  Palette,
  PlayCircle,
  Zap,
  Eye,
  Star,
  Code,
  Database,
  Inbox
} from 'lucide-react';

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
  badge?: string;
  color?: string;
}

const navigation: NavItem[] = [
  { 
    name: 'Cockpit', 
    href: '/dashboard', 
    icon: LayoutDashboard,
    color: 'cyan'
  },
  { 
    name: 'Sentinelas', 
    href: '/dashboard/agents', 
    icon: Users,
    badge: '139',
    color: 'cyan'
  },
  { 
    name: 'Neural Nexus 3D', 
    href: '/dashboard/nexus', 
    icon: Network,
    color: 'purple'
  },
  { 
    name: 'The Matrix', 
    href: '/dashboard/matrix', 
    icon: Terminal,
    color: 'green'
  },
  { 
    name: 'Evolution Lab', 
    href: '/dashboard/evolution', 
    icon: Activity,
    color: 'orange'
  },
  { 
    name: 'The Void', 
    href: '/dashboard/void', 
    icon: Eye,
    color: 'purple'
  },
  { 
    name: 'Value Dash', 
    href: '/dashboard/value', 
    icon: Wallet,
    color: 'yellow'
  },
  { 
    name: 'Gamification', 
    href: '/dashboard/gamification', 
    icon: Trophy,
    color: 'amber'
  },
  { 
    name: 'Orion AI', 
    href: '/dashboard/orion', 
    icon: MessageSquare,
    color: 'blue'
  },
  { 
    name: 'Containment', 
    href: '/dashboard/containment', 
    icon: Shield,
    color: 'red'
  },
  { 
    name: 'Requests', 
    href: '/dashboard/requests', 
    icon: Inbox,
    color: 'pink'
  },
  { 
    name: 'API Playground', 
    href: '/dashboard/api', 
    icon: Code,
    color: 'indigo'
  },
  { 
    name: 'Settings', 
    href: '/dashboard/settings', 
    icon: Settings,
    color: 'zinc'
  },
  { 
    name: 'Admin Mode', 
    href: '/dashboard/admin', 
    icon: Database,
    badge: 'ADMIN',
    color: 'red'
  },
  { 
    name: 'Singularity', 
    href: '/dashboard/singularity', 
    icon: Star,
    color: 'yellow'
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  const getColorClass = (color?: string) => {
    switch (color) {
      case 'cyan': return 'text-cyan-400 group-hover:text-cyan-300';
      case 'purple': return 'text-purple-400 group-hover:text-purple-300';
      case 'green': return 'text-green-400 group-hover:text-green-300';
      case 'orange': return 'text-orange-400 group-hover:text-orange-300';
      case 'yellow': return 'text-yellow-400 group-hover:text-yellow-300';
      case 'amber': return 'text-amber-400 group-hover:text-amber-300';
      case 'blue': return 'text-blue-400 group-hover:text-blue-300';
      case 'red': return 'text-red-400 group-hover:text-red-300';
      case 'pink': return 'text-pink-400 group-hover:text-pink-300';
      case 'indigo': return 'text-indigo-400 group-hover:text-indigo-300';
      case 'zinc': return 'text-zinc-400 group-hover:text-zinc-300';
      default: return 'text-primary group-hover:text-accent';
    }
  };

  return (
    <div className="w-64 h-screen bg-surface/50 backdrop-blur-xl border-r border-border fixed left-0 top-0 z-50 overflow-y-auto">
      {/* Logo */}
      <div className="p-6 border-b border-border">
        <Link href="/dashboard">
          <div className="flex items-center gap-3 group cursor-pointer">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-accent rounded-xl flex items-center justify-center shadow-lg shadow-primary/20">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-white group-hover:text-primary transition-colors">
                ALSHAM Q
              </h1>
              <p className="text-xs text-textSecondary font-mono">
                REALITY CODEX v13.3
              </p>
            </div>
          </div>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="p-4 space-y-1">
        {navigation.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || 
                          (item.href !== '/dashboard' && pathname.startsWith(item.href));
          
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`group flex items-center justify-between gap-3 px-4 py-3 rounded-lg transition-all ${
                isActive
                  ? 'bg-primary/10 border border-primary/30 shadow-lg shadow-primary/10'
                  : 'hover:bg-white/5 border border-transparent hover:border-border'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-5 h-5 transition-colors ${
                  isActive ? 'text-primary' : getColorClass(item.color)
                }`} />
                <span className={`text-sm font-medium transition-colors ${
                  isActive ? 'text-white' : 'text-textSecondary group-hover:text-white'
                }`}>
                  {item.name}
                </span>
              </div>
              
              {item.badge && (
                <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                  isActive 
                    ? 'bg-primary/20 text-primary'
                    : 'bg-white/5 text-textSecondary'
                }`}>
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Footer Info */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-border bg-surface/80 backdrop-blur">
        <div className="flex items-center justify-between text-xs">
          <span className="text-textSecondary">139 Agentes</span>
          <span className="text-primary font-mono">99.7% Online</span>
        </div>
        <div className="mt-2 h-1 bg-black/30 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-primary to-accent rounded-full animate-pulse"
            style={{ width: '99.7%' }}
          />
        </div>
      </div>
    </div>
  );
}
