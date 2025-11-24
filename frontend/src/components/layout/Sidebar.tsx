/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SIDEBAR SUPREMA (22 PÁGINAS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/layout/Sidebar.tsx
 * 📋 Navegação completa, organizada por setores e responsiva.
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, Users, Network, Activity, Sparkles, Wallet, 
  Trophy, MessageSquare, Terminal, Shield, Settings, Database, 
  Inbox, Code, Star, Eye, Globe, Cpu, BarChart3, Radio, Headphones, X
} from 'lucide-react';

// Props para controle Mobile (recebidas do Layout)
interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

// Configuração dos Grupos de Menu
const MENU_GROUPS = [
  {
    title: "CORE",
    items: [
      { name: 'Cockpit', href: '/dashboard', icon: LayoutDashboard, color: 'text-cyan-400' },
      { name: 'Sentinelas', href: '/dashboard/agents', icon: Users, badge: '139', color: 'text-cyan-400' },
      { name: 'Requests', href: '/dashboard/requests', icon: Inbox, badge: 'NEW', color: 'text-pink-400' },
    ]
  },
  {
    title: "INTELLIGENCE",
    items: [
      { name: 'Neural Nexus', href: '/dashboard/nexus', icon: Network, color: 'text-purple-400' },
      { name: 'Orion AI', href: '/dashboard/orion', icon: MessageSquare, color: 'text-blue-400' },
      { name: 'The Void', href: '/dashboard/void', icon: Eye, color: 'text-violet-500' },
      { name: 'Evolution Lab', href: '/dashboard/evolution', icon: Activity, color: 'text-orange-400' },
      { name: 'Singularity', href: '/dashboard/singularity', icon: Star, color: 'text-yellow-400' },
    ]
  },
  {
    title: "OPERATIONS",
    items: [
      { name: 'Sales Engine', href: '/dashboard/sales', icon: Wallet, color: 'text-green-400' },
      { name: 'Social Pulse', href: '/dashboard/social', icon: Radio, color: 'text-pink-500' },
      { name: 'Support Ops', href: '/dashboard/support', icon: Headphones, color: 'text-indigo-400' },
      { name: 'Analytics', href: '/dashboard/analytics', icon: BarChart3, color: 'text-blue-500' },
      { name: 'Value Dash', href: '/dashboard/value', icon: Trophy, color: 'text-amber-400' },
    ]
  },
  {
    title: "SYSTEM",
    items: [
      { name: 'The Matrix', href: '/dashboard/matrix', icon: Terminal, color: 'text-green-500' },
      { name: 'Containment', href: '/dashboard/containment', icon: Shield, color: 'text-red-500' },
      { name: 'Network', href: '/dashboard/network', icon: Globe, color: 'text-blue-300' },
      { name: 'Gamification', href: '/dashboard/gamification', icon: Cpu, color: 'text-purple-300' },
      { name: 'API Playground', href: '/dashboard/api', icon: Code, color: 'text-gray-400' },
      { name: 'Settings', href: '/dashboard/settings', icon: Settings, color: 'text-gray-400' },
      { name: 'Admin God Mode', href: '/dashboard/admin', icon: Database, badge: 'ADM', color: 'text-red-600' },
    ]
  }
];

export default function Sidebar({ isOpen = true, onClose }: SidebarProps) {
  const pathname = usePathname();

  return (
    <>
      {/* Overlay Escuro para Mobile (Só aparece quando aberto em telas pequenas) */}
      <div 
        className={`fixed inset-0 bg-black/80 z-40 lg:hidden backdrop-blur-sm transition-opacity duration-300 ${
          isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        }`}
        onClick={onClose}
      />

      {/* Sidebar Container */}
      <aside className={`
        fixed top-0 left-0 z-50 h-screen w-64 
        bg-surface/95 backdrop-blur-xl border-r border-white/5
        transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        {/* Header Logo */}
        <div className="p-6 border-b border-white/5 flex items-center justify-between">
          <Link href="/dashboard" className="flex items-center gap-3 group">
            <div className="w-10 h-10 bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent)] rounded-xl flex items-center justify-center shadow-lg shadow-[var(--color-primary)]/20 transition-all group-hover:scale-105">
              <Sparkles className="w-6 h-6 text-black" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-white tracking-wider group-hover:text-[var(--color-primary)] transition-colors">
                ALSHAM
              </h1>
              <p className="text-[10px] text-gray-400 font-mono tracking-widest">
                QUANTUM v13.3
              </p>
            </div>
          </Link>
          
          {/* Mobile Close Button */}
          <button onClick={onClose} className="lg:hidden p-1 hover:bg-white/10 rounded-md text-gray-400">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Scrollable Navigation */}
        <nav className="h-[calc(100vh-88px)] overflow-y-auto p-4 space-y-6 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
          {MENU_GROUPS.map((group, groupIdx) => (
            <div key={groupIdx}>
              <h3 className="px-4 text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-2 font-mono">
                {group.title}
              </h3>
              <div className="space-y-1">
                {group.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname === item.href;
                  
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => onClose && onClose()} // Fecha menu no mobile ao clicar
                      className={`group flex items-center justify-between gap-3 px-4 py-2.5 rounded-lg transition-all duration-200 ${
                        isActive
                          ? 'bg-[var(--color-primary)]/10 border border-[var(--color-primary)]/20 shadow-[0_0_15px_-5px_var(--color-primary)]'
                          : 'hover:bg-white/5 border border-transparent hover:border-white/10'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <Icon className={`w-5 h-5 transition-colors ${
                          isActive ? 'text-[var(--color-primary)]' : item.color || 'text-gray-400'
                        }`} />
                        <span className={`text-sm font-medium transition-colors ${
                          isActive ? 'text-white' : 'text-gray-400 group-hover:text-gray-200'
                        }`}>
                          {item.name}
                        </span>
                      </div>
                      
                      {item.badge && (
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold border ${
                          isActive 
                            ? 'bg-[var(--color-primary)]/20 text-[var(--color-primary)] border-[var(--color-primary)]/30'
                            : 'bg-white/5 text-gray-400 border-white/10'
                        }`}>
                          {item.badge}
                        </span>
                      )}
                    </Link>
                  );
                })}
              </div>
            </div>
          ))}
          
          {/* Espaço extra no final para scroll */}
          <div className="h-20" />
        </nav>

        {/* Footer Info */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-white/5 bg-surface/95 backdrop-blur">
            <div className="flex items-center justify-between text-xs">
            <span className="text-gray-500">139 Agentes</span>
            <span className="text-[var(--color-primary)] font-mono">99.7% Online</span>
            </div>
            <div className="mt-2 h-1 bg-black/30 rounded-full overflow-hidden">
            <div 
                className="h-full bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] rounded-full animate-pulse"
                style={{ width: '99.7%' }}
            />
            </div>
        </div>
      </aside>
    </>
  );
}
