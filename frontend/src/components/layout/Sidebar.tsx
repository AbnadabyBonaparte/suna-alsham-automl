/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SIDEBAR GOD TIER (HOLOGRAPHIC GLASS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/layout/Sidebar.tsx
 * 📋 Design de vidro fosco, indicadores laser e tipografia premium
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, Users, Network, Activity, Sparkles, Wallet, 
  Trophy, MessageSquare, Terminal, Shield, Settings, Database, 
  Inbox, Code, Star, Eye, Globe, Cpu, BarChart3, Radio, Headphones, X,
  ChevronRight, Zap, Brain, Crown, Dna
} from 'lucide-react';

// Props para controle Mobile
interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

// Configuração dos Grupos de Menu - ORDEM FINAL
const MENU_GROUPS = [
  {
    title: "COMMAND CENTER",
    items: [
      { name: 'Cockpit', href: '/dashboard', icon: LayoutDashboard },
      { name: 'Requests', href: '/dashboard/requests', icon: Inbox, badge: 'NEW' },
      { name: 'Quantum Brain', href: '/dashboard/quantum-brain', icon: Brain, badge: 'LIVE', special: true },
      { name: 'ORION Command', href: '/dashboard/orion', icon: Crown, color: 'text-yellow-500' },
    ]
  },
  {
    title: "NEURAL LAYER",
    items: [
      { name: 'Neural Nexus', href: '/dashboard/nexus', icon: Network, color: 'text-cyan-500' },
      { name: 'The Matrix', href: '/dashboard/matrix', icon: Terminal, color: 'text-green-500' },
      { name: 'Evolution Lab', href: '/dashboard/evolution', icon: Dna, badge: 'AI', color: 'text-purple-500' },
      { name: 'The VOID', href: '/dashboard/void', icon: Eye, color: 'text-purple-400' },
    ]
  },
  {
    title: "SECURITY",
    items: [
      { name: 'Containment', href: '/dashboard/containment', icon: Shield, color: 'text-red-500' },
      { name: 'Network', href: '/dashboard/network', icon: Globe, color: 'text-blue-500' },
      { name: 'Singularity', href: '/dashboard/singularity', icon: Star, special: true, color: 'text-yellow-400' },
    ]
  },
  {
    title: "AGENTS",
    items: [
      { name: 'Sentinelas', href: '/dashboard/agents', icon: Users, badge: '139' },
    ]
  },
  {
    title: "OPERATIONS",
    items: [
      { name: 'Sales Engine', href: '/dashboard/sales', icon: Wallet },
      { name: 'Social Pulse', href: '/dashboard/social', icon: Radio },
      { name: 'Support Ops', href: '/dashboard/support', icon: Headphones },
      { name: 'Analytics', href: '/dashboard/analytics', icon: BarChart3 },
      { name: 'Value Dash', href: '/dashboard/value', icon: Trophy },
    ]
  },
  {
    title: "SYSTEM",
    items: [
      { name: 'Gamification', href: '/dashboard/gamification', icon: Cpu },
      { name: 'API Playground', href: '/dashboard/api', icon: Code },
      { name: 'Settings', href: '/dashboard/settings', icon: Settings },
      { name: 'Admin God Mode', href: '/dashboard/admin', icon: Database, badge: 'ADM' },
    ]
  }
];

export default function Sidebar({ isOpen = true, onClose }: SidebarProps) {
  const pathname = usePathname();

  return (
    <>
      {/* Overlay Escuro para Mobile */}
      <div 
        className={`fixed inset-0 bg-black/90 z-40 lg:hidden backdrop-blur-sm transition-opacity duration-500 ${
          isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        }`}
        onClick={onClose}
      />

      {/* Sidebar Container - GLASSMORPHISM PURO */}
      <aside className={`
        fixed top-0 left-0 z-50 h-screen w-72 
        bg-[#050505]/85 backdrop-blur-2xl border-r border-white/5
        transition-transform duration-500 cubic-bezier(0.4, 0, 0.2, 1)
        shadow-[20px_0_50px_rgba(0,0,0,0.5)]
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        
        {/* 1. HEADER: LOGO HOLOGRÁFICO */}
        <div className="h-24 flex items-center px-6 border-b border-white/5 relative overflow-hidden group">
          {/* Efeito de Brilho no Header */}
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[var(--color-primary)] to-transparent opacity-50" />
          
          <Link href="/dashboard" className="flex items-center gap-4 w-full">
            <div className="relative">
              <div className="absolute -inset-2 bg-[var(--color-primary)] rounded-full blur-lg opacity-20 group-hover:opacity-40 transition-opacity duration-500" />
              <div className="relative w-10 h-10 bg-gradient-to-br from-[var(--color-primary)]/20 to-transparent border border-[var(--color-primary)]/50 rounded-xl flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-[var(--color-primary)]" />
              </div>
            </div>
            
            <div className="flex flex-col">
              <h1 className="text-lg font-bold text-white tracking-[0.15em] leading-none group-hover:text-[var(--color-primary)] transition-colors">
                ALSHAM
              </h1>
              <span className="text-[10px] text-[var(--color-text-secondary)] font-mono mt-1 tracking-widest">
                QUANTUM v13.3
              </span>
            </div>
          </Link>

          <button onClick={onClose} className="lg:hidden text-gray-500 hover:text-white ml-auto">
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* 2. NAVIGATION: SCROLL AREA */}
        <nav className="h-[calc(100vh-160px)] overflow-y-auto py-6 px-4 space-y-6 scrollbar-thin scrollbar-thumb-white/5 scrollbar-track-transparent hover:scrollbar-thumb-[var(--color-primary)]/20">
          {MENU_GROUPS.map((group, groupIdx) => (
            <div key={groupIdx}>
              <h3 className="px-4 text-[10px] font-bold text-gray-500/70 uppercase tracking-[0.2em] mb-3 font-mono flex items-center gap-2">
                {group.title}
                <div className="h-[1px] flex-1 bg-gradient-to-r from-white/5 to-transparent" />
              </h3>
              
              <div className="space-y-1">
                {group.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname === item.href;
                  const isSpecial = item.special;
                  const itemColor = item.color;
                  
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => onClose && onClose()}
                      className={`group relative flex items-center justify-between px-4 py-3 rounded-lg transition-all duration-300 overflow-hidden
                        ${isActive 
                          ? 'text-white' 
                          : 'text-gray-400 hover:text-white hover:bg-white/[0.02]'
                        }
                      `}
                    >
                      {/* Active State: Laser Line Background */}
                      {isActive && (
                        <div className="absolute inset-0 bg-gradient-to-r from-[var(--color-primary)]/10 to-transparent border-l-2 border-[var(--color-primary)]" />
                      )}

                      {/* Active State: Glow Effect */}
                      {isActive && (
                        <div className="absolute inset-0 shadow-[inset_10px_0_20px_-10px_rgba(var(--color-primary-rgb),0.3)]" />
                      )}

                      <div className="flex items-center gap-3 relative z-10">
                        <Icon className={`w-5 h-5 transition-all duration-300 ${
                          isActive 
                            ? 'text-[var(--color-primary)] drop-shadow-[0_0_8px_rgba(var(--color-primary-rgb),0.5)]' 
                            : isSpecial 
                              ? 'text-[var(--color-accent)]'
                              : itemColor || 'text-gray-500 group-hover:text-gray-300'
                        }`} />
                        
                        <span className={`text-sm font-medium tracking-wide ${isSpecial ? 'text-[var(--color-accent)] font-bold' : ''}`}>
                          {item.name}
                        </span>
                      </div>
                      
                      {/* Badges & Arrows */}
                      <div className="relative z-10 flex items-center">
                        {item.badge ? (
                          <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold border tracking-wider ${
                            isActive 
                              ? 'bg-[var(--color-primary)] text-black border-[var(--color-primary)]'
                              : item.badge === 'LIVE' 
                                ? 'bg-green-500/20 text-green-400 border-green-500/30 animate-pulse'
                                : item.badge === 'AI'
                                  ? 'bg-purple-500/20 text-purple-400 border-purple-500/30'
                                  : 'bg-white/5 text-gray-400 border-white/10 group-hover:border-white/30'
                          }`}>
                            {item.badge}
                          </span>
                        ) : (
                          isActive && <ChevronRight className="w-4 h-4 text-[var(--color-primary)] animate-pulse" />
                        )}
                      </div>
                    </Link>
                  );
                })}
              </div>
            </div>
          ))}
        </nav>

        {/* 3. FOOTER: SYSTEM STATUS WIDGET */}
        <div className="absolute bottom-0 left-0 right-0 h-20 border-t border-white/5 bg-black/40 backdrop-blur-xl px-6 flex items-center justify-between group cursor-default">
            <div className="flex items-center gap-3">
                <div className="relative">
                    <div className="w-2 h-2 rounded-full bg-[var(--color-success)] animate-pulse" />
                    <div className="absolute inset-0 w-2 h-2 rounded-full bg-[var(--color-success)] blur-sm" />
                </div>
                <div className="flex flex-col">
                    <span className="text-[10px] text-gray-500 font-mono uppercase tracking-wider">System Status</span>
                    <span className="text-xs font-bold text-[var(--color-primary)] tracking-wide flex items-center gap-1">
                        OPERATIONAL <Zap className="w-3 h-3" />
                    </span>
                </div>
            </div>
            
            {/* Mini Graph Visual */}
            <div className="flex gap-[2px] items-end h-6 opacity-50 group-hover:opacity-100 transition-opacity">
                {[40, 70, 45, 90, 60, 80, 50].map((h, i) => (
                    <div 
                        key={i} 
                        className="w-1 bg-[var(--color-primary)] rounded-t-sm"
                        style={{ height: `${h}%` }} 
                    />
                ))}
            </div>
        </div>
      </aside>
    </>
  );
}
