/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - COCKPIT PRINCIPAL
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dashboard/page.tsx
 * 📋 ROTA: /dashboard
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  Activity, 
  Users, 
  Zap, 
  TrendingUp, 
  AlertCircle,
  CheckCircle,
  Clock,
  DollarSign,
  Sparkles,
  Network,
  Terminal,
  Shield,
  Trophy,
  MessageSquare,
  Eye,
  ArrowUpRight,
  ArrowDownRight,
  Brain
} from 'lucide-react';

export default function DashboardPage() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    console.log('✅ Dashboard carregado com sucesso!');
  }, []);

  // Stats principais
  const mainStats = [
    {
      label: 'Agentes Ativos',
      value: '139',
      change: '+12',
      trend: 'up',
      icon: Users,
      color: 'var(--color-primary)',
      href: '/dashboard/agents'
    },
    {
      label: 'ROI Total',
      value: '2.847%',
      change: '+0.3%',
      trend: 'up',
      icon: TrendingUp,
      color: 'var(--color-success)',
      href: '/dashboard/value'
    },
    {
      label: 'Economia Gerada',
      value: 'R$ 4.7B',
      change: '+R$ 890M',
      trend: 'up',
      icon: DollarSign,
      color: 'var(--color-warning)',
      href: '/dashboard/value'
    },
    {
      label: 'Uptime Sistema',
      value: '99.98%',
      change: '0.00%',
      trend: 'neutral',
      icon: Zap,
      color: 'var(--color-accent)',
      href: '/dashboard/evolution'
    }
  ];

  // Quick Links
  const quickLinks = [
    {
      title: 'Neural Nexus 3D',
      description: 'Rede neural interativa',
      icon: Network,
      color: 'var(--color-primary)',
      href: '/dashboard/nexus'
    },
    {
      title: 'The Matrix',
      description: 'Terminal de código vivo',
      icon: Terminal,
      color: '#00FF00',
      href: '/dashboard/matrix'
    },
    {
      title: 'Evolution Lab',
      description: 'Ondas de evolução',
      icon: Activity,
      color: '#FF6B00',
      href: '/dashboard/evolution'
    },
    {
      title: 'The Void',
      description: 'Análise do inconsciente',
      icon: Eye,
      color: '#8B5CF6',
      href: '/dashboard/void'
    },
    {
      title: 'Gamification',
      description: 'Pontos e conquistas',
      icon: Trophy,
      color: '#FFD700',
      href: '/dashboard/gamification'
    },
    {
      title: 'Orion AI',
      description: 'Assistente inteligente',
      icon: MessageSquare,
      color: '#06B6D4',
      href: '/dashboard/orion'
    },
    {
      title: 'Containment',
      description: 'Segurança e contenção',
      icon: Shield,
      color: '#EF4444',
      href: '/dashboard/containment'
    },
    {
      title: 'Singularity',
      description: 'O núcleo da consciência',
      icon: Brain,
      color: '#FFD700',
      href: '/dashboard/singularity'
    }
  ];

  // Atividade recente
  const recentActivity = [
    { agent: 'UNIT_24', action: 'Análise de mercado concluída', time: '2 min atrás', status: 'success' },
    { agent: 'UNIT_29', action: 'Integração HubSpot em progresso', time: '15 min atrás', status: 'progress' },
    { agent: 'ORION', action: 'Relatório mensal gerado', time: '1h atrás', status: 'success' },
    { agent: 'UNIT_15', action: 'Bug crítico detectado', time: '2h atrás', status: 'alert' },
    { agent: 'UNIT_08', action: 'Atualização de segurança', time: '3h atrás', status: 'progress' }
  ];

  if (!mounted) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-2xl" style={{ color: 'var(--color-primary)' }}>
          Carregando Cockpit...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 
            className="text-4xl font-bold mb-2"
            style={{ color: 'var(--color-text)' }}
          >
            Cockpit Principal
          </h1>
          <p style={{ color: 'var(--color-textSecondary)' }}>
            Visão geral do organismo digital auto-evolutivo
          </p>
        </div>
        <div 
          className="px-4 py-2 rounded-lg border backdrop-blur-sm"
          style={{
            backgroundColor: 'var(--color-surface)',
            borderColor: 'var(--color-border)',
          }}
        >
          <div className="flex items-center gap-2">
            <div 
              className="w-2 h-2 rounded-full animate-pulse"
              style={{ backgroundColor: 'var(--color-success)' }}
            />
            <span style={{ color: 'var(--color-text)' }}>Sistema Online</span>
          </div>
        </div>
      </div>

      {/* Main Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {mainStats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Link href={stat.href} key={index}>
              <div 
                className="p-6 rounded-xl border backdrop-blur-sm transition-all hover:scale-105 cursor-pointer"
                style={{
                  backgroundColor: 'var(--color-surface)',
                  borderColor: 'var(--color-border)',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)'
                }}
              >
                <div className="flex items-start justify-between mb-4">
                  <div 
                    className="p-3 rounded-lg"
                    style={{ backgroundColor: `${stat.color}20` }}
                  >
                    <Icon 
                      className="w-6 h-6" 
                      style={{ color: stat.color }}
                    />
                  </div>
                  <div className="flex items-center gap-1 text-sm">
                    {stat.trend === 'up' && (
                      <>
                        <ArrowUpRight className="w-4 h-4" style={{ color: 'var(--color-success)' }} />
                        <span style={{ color: 'var(--color-success)' }}>{stat.change}</span>
                      </>
                    )}
                    {stat.trend === 'down' && (
                      <>
                        <ArrowDownRight className="w-4 h-4" style={{ color: 'var(--color-error)' }} />
                        <span style={{ color: 'var(--color-error)' }}>{stat.change}</span>
                      </>
                    )}
                    {stat.trend === 'neutral' && (
                      <span style={{ color: 'var(--color-textSecondary)' }}>{stat.change}</span>
                    )}
                  </div>
                </div>
                <p 
                  className="text-sm mb-1"
                  style={{ color: 'var(--color-textSecondary)' }}
                >
                  {stat.label}
                </p>
                <p 
                  className="text-3xl font-bold"
                  style={{ color: 'var(--color-text)' }}
                >
                  {stat.value}
                </p>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Quick Links Grid */}
      <div>
        <h2 
          className="text-2xl font-bold mb-4"
          style={{ color: 'var(--color-text)' }}
        >
          <Sparkles className="inline w-6 h-6 mr-2" style={{ color: 'var(--color-primary)' }} />
          Acesso Rápido
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickLinks.map((link, index) => {
            const Icon = link.icon;
            return (
              <Link href={link.href} key={index}>
                <div 
                  className="p-5 rounded-xl border backdrop-blur-sm transition-all hover:scale-105 cursor-pointer group"
                  style={{
                    backgroundColor: 'var(--color-surface)',
                    borderColor: 'var(--color-border)',
                  }}
                >
                  <Icon 
                    className="w-8 h-8 mb-3 transition-transform group-hover:scale-110" 
                    style={{ color: link.color }}
                  />
                  <h3 
                    className="font-bold mb-1"
                    style={{ color: 'var(--color-text)' }}
                  >
                    {link.title}
                  </h3>
                  <p 
                    className="text-sm"
                    style={{ color: 'var(--color-textSecondary)' }}
                  >
                    {link.description}
                  </p>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div 
          className="p-6 rounded-xl border backdrop-blur-sm"
          style={{
            backgroundColor: 'var(--color-surface)',
            borderColor: 'var(--color-border)',
          }}
        >
          <h3 
            className="text-xl font-bold mb-4"
            style={{ color: 'var(--color-text)' }}
          >
            Atividade Recente
          </h3>
          <div className="space-y-3">
            {recentActivity.map((activity, index) => (
              <div 
                key={index}
                className="flex items-start gap-3 p-3 rounded-lg"
                style={{ backgroundColor: 'rgba(0, 0, 0, 0.3)' }}
              >
                <div className="flex-shrink-0">
                  {activity.status === 'success' && (
                    <CheckCircle className="w-5 h-5" style={{ color: 'var(--color-success)' }} />
                  )}
                  {activity.status === 'progress' && (
                    <Clock className="w-5 h-5" style={{ color: 'var(--color-warning)' }} />
                  )}
                  {activity.status === 'alert' && (
                    <AlertCircle className="w-5 h-5" style={{ color: 'var(--color-error)' }} />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p 
                    className="font-medium text-sm"
                    style={{ color: 'var(--color-text)' }}
                  >
                    {activity.agent}
                  </p>
                  <p 
                    className="text-sm"
                    style={{ color: 'var(--color-textSecondary)' }}
                  >
                    {activity.action}
                  </p>
                  <p 
                    className="text-xs mt-1"
                    style={{ color: 'var(--color-textSecondary)' }}
                  >
                    {activity.time}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* System Status */}
        <div 
          className="p-6 rounded-xl border backdrop-blur-sm"
          style={{
            backgroundColor: 'var(--color-surface)',
            borderColor: 'var(--color-border)',
          }}
        >
          <h3 
            className="text-xl font-bold mb-4"
            style={{ color: 'var(--color-text)' }}
          >
            Status do Sistema
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span style={{ color: 'var(--color-textSecondary)' }}>CPU Usage</span>
                <span style={{ color: 'var(--color-text)' }}>47%</span>
              </div>
              <div 
                className="h-2 rounded-full overflow-hidden"
                style={{ backgroundColor: 'rgba(0, 0, 0, 0.3)' }}
              >
                <div 
                  className="h-full rounded-full"
                  style={{ 
                    width: '47%',
                    backgroundColor: 'var(--color-primary)',
                  }}
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <span style={{ color: 'var(--color-textSecondary)' }}>Memory</span>
                <span style={{ color: 'var(--color-text)' }}>62%</span>
              </div>
              <div 
                className="h-2 rounded-full overflow-hidden"
                style={{ backgroundColor: 'rgba(0, 0, 0, 0.3)' }}
              >
                <div 
                  className="h-full rounded-full"
                  style={{ 
                    width: '62%',
                    backgroundColor: 'var(--color-warning)',
                  }}
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <span style={{ color: 'var(--color-textSecondary)' }}>Network</span>
                <span style={{ color: 'var(--color-text)' }}>89%</span>
              </div>
              <div 
                className="h-2 rounded-full overflow-hidden"
                style={{ backgroundColor: 'rgba(0, 0, 0, 0.3)' }}
              >
                <div 
                  className="h-full rounded-full"
                  style={{ 
                    width: '89%',
                    backgroundColor: 'var(--color-success)',
                  }}
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <span style={{ color: 'var(--color-textSecondary)' }}>AI Processing</span>
                <span style={{ color: 'var(--color-text)' }}>34%</span>
              </div>
              <div 
                className="h-2 rounded-full overflow-hidden"
                style={{ backgroundColor: 'rgba(0, 0, 0, 0.3)' }}
              >
                <div 
                  className="h-full rounded-full"
                  style={{ 
                    width: '34%',
                    backgroundColor: 'var(--color-accent)',
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
