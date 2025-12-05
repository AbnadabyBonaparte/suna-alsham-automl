/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SIDEBAR GOD TIER (THEME-AWARE)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/components/layout/Sidebar.tsx
 * 📋 Design de vidro fosco com cores 100% submissas aos temas
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

// Configuração dos Grupos de Menu - SEM CORES FIXAS
const MENU_GROUPS = [
  {
    title: "COMMAND CENTER",
    items: [
      { name: 'Cockpit', href: '/dashboard', icon: LayoutDashboard },
      { name: 'Requests', href: '/dashboard/requests', icon: Inbox, badge: 'NEW' },
      { name: 'Quantum Brain', href: '/dashboard/quantum-brain', icon: Brain, badge: 'LIVE', special: true },
      { name: 'ORION Command', href: '/dashboard/orion', icon: Crown },
    ]
  },
  {
    title: "NEURAL LAYER",
    items: [
      { name: 'Neural Nexus', href: '/dashboard/nexus', icon: Network },
      { name: 'The Matrix', href: '/dashboard/matrix', icon: Terminal },
      { name: 'Evolution Lab', href: '/dashboard/evolution', icon: Dna, badge: 'AI' },
      { name: 'The VOID', href: '/dashboard/void', icon: Eye },
    ]
  },
  {
    title: "SECURITY",
    items: [
      { name: 'Containment', href: '/dashboard/containment', icon: Shield },
      { name: 'Network', href: '/dashboard/network', icon: Globe },
      { name: 'Singularity', href: '/dashboard/singularity', icon: Star, special: true },
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
      <aside 
        className={`
          fixed top-0 left-0 z-50 h-screen w-72 
          backdrop-blur-2xl border-r
          transition-transform duration-500 cubic-bezier(0.4, 0, 0.2, 1)
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
        style={{
          background: 'var(--color-background)/85',
          borderColor: 'var(--color-border)/10',
          boxShadow: '20px 0 50px rgba(0,0,0,0.5)'
        }}
      >
        
        {/* 1. HEADER: LOGO HOLOGRÁFICO */}
        <div 
          className="h-24 flex items-center px-6 relative overflow-hidden group"
          style={{ borderBottom: '1px solid var(--color-border)/10' }}
        >
          {/* Efeito de Brilho no Header */}
          <div 
            className="absolute top-0 left-0 w-full h-1 opacity-50"
            style={{ background: 'linear-gradient(to right, transparent, var(--color-primary), transparent)' }}
          />
          
          <Link href="/dashboard" className="flex items-center gap-4 w-full">
            <div className="relative">
              <div 
                className="absolute -inset-2 rounded-full blur-lg opacity-20 group-hover:opacity-40 transition-opacity duration-500"
                style={{ background: 'var(--color-primary)' }}
              />
              <div 
                className="relative w-10 h-10 rounded-xl flex items-center justify-center"
                style={{
                  background: 'linear-gradient(to bottom right, var(--color-primary)/20, transparent)',
                  border: '1px solid var(--color-primary)/50'
                }}
              >
                <Sparkles className="w-5 h-5" style={{ color: 'var(--color-primary)' }} />
              </div>
            </div>
            
            <div className="flex flex-col">
              <h1 
                className="text-lg font-bold tracking-[0.15em] leading-none transition-colors"
                style={{ color: 'var(--color-text)' }}
              >
                ALSHAM
              </h1>
              <span 
                className="text-[10px] font-mono mt-1 tracking-widest"
                style={{ color: 'var(--color-text-secondary)' }}
              >
                QUANTUM v13.3
              </span>
            </div>
          </Link>

          <button 
            onClick={onClose} 
            className="lg:hidden ml-auto transition-colors"
            style={{ color: 'var(--color-text-secondary)' }}
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* 2. NAVIGATION: SCROLL AREA */}
        <nav className="h-[calc(100vh-160px)] overflow-y-auto py-6 px-4 space-y-6 scrollbar-thin scrollbar-thumb-white/5 scrollbar-track-transparent">
          {MENU_GROUPS.map((group, groupIdx) => (
            <div key={groupIdx}>
              <h3 
                className="px-4 text-[10px] font-bold uppercase tracking-[0.2em] mb-3 font-mono flex items-center gap-2"
                style={{ color: 'var(--color-text-secondary)/70' }}
              >
                {group.title}
                <div 
                  className="h-[1px] flex-1"
                  style={{ background: 'linear-gradient(to right, var(--color-border)/10, transparent)' }}
                />
              </h3>
              
              <div className="space-y-1">
                {group.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname === item.href;
                  const isSpecial = item.special;
                  
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => onClose && onClose()}
                      className="group relative flex items-center justify-between px-4 py-3 rounded-lg transition-all duration-300 overflow-hidden"
                      style={{
                        color: isActive ? 'var(--color-text)' : 'var(--color-text-secondary)',
                      }}
                    >
                      {/* Active State: Laser Line Background */}
                      {isActive && (
                        <div 
                          className="absolute inset-0"
                          style={{
                            background: 'linear-gradient(to right, var(--color-primary)/15, transparent)',
                            borderLeft: '2px solid var(--color-primary)'
                          }}
                        />
                      )}

                      {/* Active State: Glow Effect */}
                      {isActive && (
                        <div 
                          className="absolute inset-0"
                          style={{ boxShadow: 'inset 10px 0 20px -10px var(--color-glow)/30' }}
                        />
                      )}

                      <div className="flex items-center gap-3 relative z-10">
                        <Icon 
                          className="w-5 h-5 transition-all duration-300"
                          style={{
                            color: isActive 
                              ? 'var(--color-primary)' 
                              : isSpecial 
                                ? 'var(--color-accent)'
                                : 'var(--color-text-secondary)',
                            filter: isActive ? 'drop-shadow(0 0 8px var(--color-glow)/50)' : 'none'
                          }}
                        />
                        
                        <span 
                          className={`text-sm font-medium tracking-wide ${isSpecial ? 'font-bold' : ''}`}
                          style={{ color: isSpecial && !isActive ? 'var(--color-accent)' : 'inherit' }}
                        >
                          {item.name}
                        </span>
                      </div>
                      
                      {/* Badges & Arrows */}
                      <div className="relative z-10 flex items-center">
                        {item.badge ? (
                          <span 
                            className="px-1.5 py-0.5 rounded text-[9px] font-bold tracking-wider"
                            style={{
                              background: isActive 
                                ? 'var(--color-primary)'
                                : item.badge === 'LIVE' 
                                  ? 'var(--color-success)/20'
                                  : item.badge === 'AI'
                                    ? 'var(--color-accent)/20'
                                    : 'var(--color-surface)',
                              color: isActive 
                                ? 'var(--color-background)'
                                : item.badge === 'LIVE'
                                  ? 'var(--color-success)'
                                  : item.badge === 'AI'
                                    ? 'var(--color-accent)'
                                    : 'var(--color-text-secondary)',
                              border: `1px solid ${isActive 
                                ? 'var(--color-primary)'
                                : item.badge === 'LIVE'
                                  ? 'var(--color-success)/30'
                                  : item.badge === 'AI'
                                    ? 'var(--color-accent)/30'
                                    : 'var(--color-border)/20'}`
                            }}
                          >
                            {item.badge}
                          </span>
                        ) : (
                          isActive && (
                            <ChevronRight 
                              className="w-4 h-4 animate-pulse"
                              style={{ color: 'var(--color-primary)' }}
                            />
                          )
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
        <div 
          className="absolute bottom-0 left-0 right-0 h-20 backdrop-blur-xl px-6 flex items-center justify-between group cursor-default"
          style={{
            borderTop: '1px solid var(--color-border)/10',
            background: 'var(--color-background)/40'
          }}
        >
            <div className="flex items-center gap-3">
                <div className="relative">
                    <div 
                      className="w-2 h-2 rounded-full animate-pulse"
                      style={{ background: 'var(--color-success)' }}
                    />
                    <div 
                      className="absolute inset-0 w-2 h-2 rounded-full blur-sm"
                      style={{ background: 'var(--color-success)' }}
                    />
                </div>
                <div className="flex flex-col">
                    <span 
                      className="text-[10px] font-mono uppercase tracking-wider"
                      style={{ color: 'var(--color-text-secondary)' }}
                    >
                      System Status
                    </span>
                    <span 
                      className="text-xs font-bold tracking-wide flex items-center gap-1"
                      style={{ color: 'var(--color-primary)' }}
                    >
                        OPERATIONAL <Zap className="w-3 h-3" />
                    </span>
                </div>
            </div>
            
            {/* Mini Graph Visual */}
            <div className="flex gap-[2px] items-end h-6 opacity-50 group-hover:opacity-100 transition-opacity">
                {[40, 70, 45, 90, 60, 80, 50].map((h, i) => (
                    <div 
                        key={i} 
                        className="w-1 rounded-t-sm"
                        style={{ 
                          height: `${h}%`,
                          background: 'var(--color-primary)'
                        }} 
                    />
                ))}
            </div>
        </div>
      </aside>
    </>
  );
}
