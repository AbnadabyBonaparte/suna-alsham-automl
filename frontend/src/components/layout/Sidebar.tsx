"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import { LogOut, ChevronDown } from "lucide-react";
import { ThemeSwitcher } from "@/components/ui/ThemeSwitcher";
import { useState } from "react";

export default function Sidebar() {
  const pathname = usePathname();
  const { user, signOut } = useAuth();
  const [expandedSections, setExpandedSections] = useState<string[]>(["core", "intel", "system"]);

  const toggleSection = (section: string) => {
    setExpandedSections(prev => 
      prev.includes(section) 
        ? prev.filter(s => s !== section)
        : [...prev, section]
    );
  };

  const menuSections = [
    {
      id: "core",
      title: "NÚCLEO",
      items: [
        { name: "COCKPIT", path: "/dashboard", icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" },
        { name: "SENTINELAS", path: "/dashboard/agents", icon: "M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" },
        { name: "NEXUS 3D", path: "/dashboard/network", icon: "M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" },
        { name: "THE MATRIX", path: "/dashboard/matrix", icon: "M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" },
      ]
    },
    {
      id: "intel",
      title: "INTELIGÊNCIA",
      items: [
        { name: "EVOLUTION LAB", path: "/dashboard/evolution", icon: "M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" },
        { name: "THE VOID", path: "/dashboard/void", icon: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" },
        { name: "VALUE DASH", path: "/dashboard/value", icon: "M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" },
        { name: "GAMIFICATION", path: "/dashboard/gamification", icon: "M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" },
        { name: "ORION AI", path: "/dashboard/orion", icon: "M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" },
      ]
    },
    {
      id: "system",
      title: "SISTEMA",
      items: [
        { name: "CONTAINMENT", path: "/dashboard/containment", icon: "M20.618 5.984A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" },
        { name: "API PLAYGROUND", path: "/dashboard/api", icon: "M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" },
        { name: "SETTINGS", path: "/dashboard/settings", icon: "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" },
        { name: "ADMIN MODE", path: "/dashboard/admin", icon: "M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" },
      ]
    },
    {
      id: "special",
      title: "ESPECIAL",
      items: [
        { name: "SINGULARITY", path: "/singularity", icon: "M13 10V3L4 14h7v7l9-11h-7z" },
        { name: "ONBOARDING", path: "/onboarding", icon: "M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" },
      ]
    },
  ];

  return (
    <div 
      className="h-screen w-64 flex flex-col z-50 overflow-hidden"
      style={{
        background: 'var(--sidebar-bg)',
        borderRight: '1px solid var(--sidebar-border)',
        boxShadow: 'var(--shadow-lg)',
      }}
    >
      {/* Logo */}
      <div 
        className="p-4 flex-shrink-0"
        style={{ borderBottom: '1px solid var(--border-subtle)' }}
      >
        <h1 
          className="text-xl font-bold tracking-tighter"
          style={{ 
            color: 'var(--text-primary)',
            fontFamily: 'var(--font-display)',
          }}
        >
          ALSHAM <span style={{ color: 'var(--accent)' }}>Q</span>
        </h1>
        <p 
          className="text-[10px] mt-1 tracking-[0.2em]"
          style={{ color: 'var(--text-muted)' }}
        >
          REALITY CODEX v13.3
        </p>
      </div>

      {/* Theme Switcher */}
      <div className="px-3 py-2 flex-shrink-0">
        <ThemeSwitcher />
      </div>

      {/* Menu Sections - Scrollable */}
      <nav className="flex-1 overflow-y-auto py-2">
        {menuSections.map((section) => (
          <div key={section.id} className="mb-2">
            {/* Section Header */}
            <button
              onClick={() => toggleSection(section.id)}
              className="w-full flex items-center justify-between px-4 py-2 text-[10px] font-bold tracking-widest transition-colors"
              style={{ color: 'var(--text-muted)' }}
            >
              {section.title}
              <ChevronDown 
                className={`w-3 h-3 transition-transform duration-200 ${
                  expandedSections.includes(section.id) ? 'rotate-180' : ''
                }`}
              />
            </button>

            {/* Section Items */}
            {expandedSections.includes(section.id) && (
              <div className="space-y-0.5">
                {section.items.map((item) => {
                  const isActive = pathname === item.path || pathname.startsWith(item.path + '/');
                  return (
                    <Link
                      key={item.path}
                      href={item.path}
                      className="relative flex items-center px-4 py-2 transition-all duration-200 group"
                      style={{
                        background: isActive ? 'var(--accent-subtle)' : 'transparent',
                        color: isActive ? 'var(--accent)' : 'var(--text-muted)',
                        borderLeft: isActive ? '3px solid var(--accent)' : '3px solid transparent',
                      }}
                    >
                      <svg
                        className={`w-4 h-4 mr-2 transition-transform duration-200 ${
                          isActive ? "scale-110" : "group-hover:scale-105"
                        }`}
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        style={{
                          filter: isActive ? 'drop-shadow(0 0 4px var(--accent-glow))' : 'none',
                        }}
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
                      </svg>
                      <span 
                        className="text-xs font-semibold tracking-wide"
                        style={{ fontFamily: 'var(--font-display)' }}
                      >
                        {item.name}
                      </span>
                    </Link>
                  );
                })}
              </div>
            )}
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div 
        className="p-3 flex-shrink-0 space-y-2"
        style={{ borderTop: '1px solid var(--border-subtle)' }}
      >
        {user && (
          <div 
            className="px-2 py-1.5 rounded-lg text-xs"
            style={{
              background: 'var(--bg-panel)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <p style={{ color: 'var(--text-muted)' }} className="text-[9px] uppercase tracking-wider">
              Operator
            </p>
            <p style={{ color: 'var(--text-primary)' }} className="font-mono truncate text-[11px]">
              {user.email}
            </p>
          </div>
        )}
        
        <button
          onClick={() => signOut()}
          className="w-full flex items-center justify-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
          style={{
            background: 'var(--error-bg)',
            border: '1px solid var(--error)',
            color: 'var(--error)',
          }}
        >
          <LogOut className="w-3 h-3" />
          Logout
        </button>
        
        <div className="flex items-center space-x-2">
          <div 
            className="w-1.5 h-1.5 rounded-full animate-pulse"
            style={{ 
              background: 'var(--success)',
              boxShadow: '0 0 8px var(--success)',
            }}
          />
          <span className="text-[10px] font-mono" style={{ color: 'var(--success)' }}>
            139 AGENTES • 21 PÁGINAS
          </span>
        </div>
      </div>
    </div>
  );
}
