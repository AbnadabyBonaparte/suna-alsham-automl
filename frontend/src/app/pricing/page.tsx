/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - PRICING (THE GATEWAY TO BILLIONS)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/pricing/page.tsx
 * 💰 3 Planos Premium: Starter, Pro, Enterprise
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { 
    Check, Zap, Crown, Rocket, Shield, Brain, 
    Users, Database, ArrowRight, Sparkles, Star,
    Activity, Globe, Lock, ChevronRight, Hexagon
} from 'lucide-react';

const PLANS = [
    {
        id: 'starter',
        name: 'STARTER',
        price: 990,
        priceId: 'price_starter', // Substituir pelo ID real do Stripe
        description: 'Ideal para pequenas operações',
        badge: null,
        color: 'from-blue-500 to-cyan-500',
        borderColor: 'border-blue-500/30',
        glowColor: 'rgba(59, 130, 246, 0.3)',
        features: [
            '10 Agentes de IA',
            '1.000 requests/mês',
            'Dashboard básico',
            'Suporte via email',
            'API REST',
            'Relatórios semanais',
        ],
        limitations: [
            'Sem auto-evolução',
            'Sem ORION Voice',
        ]
    },
    {
        id: 'pro',
        name: 'PRO',
        price: 4900,
        priceId: 'price_pro', // Substituir pelo ID real do Stripe
        description: 'Para empresas em crescimento',
        badge: 'MAIS POPULAR',
        color: 'from-purple-500 to-pink-500',
        borderColor: 'border-purple-500/50',
        glowColor: 'rgba(168, 85, 247, 0.4)',
        features: [
            '50 Agentes de IA',
            '10.000 requests/mês',
            'Dashboard completo',
            'Suporte prioritário 24/7',
            'API REST + WebSocket',
            'Relatórios em tempo real',
            'Auto-evolução básica',
            'ORION Voice Assistant',
            'Integrações ilimitadas',
        ],
        limitations: []
    },
    {
        id: 'enterprise',
        name: 'ENTERPRISE',
        price: 9900,
        priceId: 'price_enterprise', // Substituir pelo ID real do Stripe
        description: 'Para operações de escala global',
        badge: 'MAIS VENDIDO',
        color: 'from-yellow-400 to-orange-500',
        borderColor: 'border-yellow-500/50',
        glowColor: 'rgba(250, 204, 21, 0.5)',
        features: [
            '∞ Agentes de IA ilimitados',
            '∞ Requests ilimitados',
            'Dashboard God Mode',
            'Suporte dedicado + SLA',
            'API completa + SDK',
            'Relatórios customizados',
            'Auto-evolução avançada (5 níveis)',
            'ORION Voice Premium',
            'White-label disponível',
            'Deploy on-premise opcional',
            'Treinamento personalizado',
            'Acesso antecipado a features',
        ],
        limitations: []
    }
];

export default function PricingPage() {
    const router = useRouter();
    const { user, hasAccess, loading: authLoading } = useAuth();
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [selectedPlan, setSelectedPlan] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<string | null>(null);
    const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');

    // Partículas de fundo
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        const particles: { x: number; y: number; vx: number; vy: number; size: number; color: string }[] = [];

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
        resize();

        // Criar partículas
        for (let i = 0; i < 100; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2,
                color: ['#FFD700', '#00FFD0', '#8B5CF6'][Math.floor(Math.random() * 3)]
            });
        }

        const render = () => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            particles.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;

                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

                ctx.beginPath();
                ctx.fillStyle = p.color;
                ctx.globalAlpha = 0.6;
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();
            });

            ctx.globalAlpha = 1;
            animationId = requestAnimationFrame(render);
        };

        render();
        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, []);

    const handleCheckout = async (plan: typeof PLANS[0]) => {
        setIsLoading(plan.id);
        
        try {
            const response = await fetch('/api/stripe/checkout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    priceId: plan.priceId,
                    planId: plan.id,
                    billingCycle,
                }),
            });

            const data = await response.json();

            if (data.url) {
                window.location.href = data.url;
            } else {
                throw new Error(data.error || 'Erro ao criar checkout');
            }
        } catch (error) {
            console.error('Checkout error:', error);
            alert('Erro ao processar pagamento. Tente novamente.');
        } finally {
            setIsLoading(null);
        }
    };

    const getYearlyPrice = (monthly: number) => Math.round(monthly * 10); // 2 meses grátis

    return (
        <div className="min-h-screen bg-black text-white relative overflow-hidden">
            {/* Canvas Background */}
            <canvas ref={canvasRef} className="absolute inset-0 w-full h-full opacity-30" />
            
            {/* Grid Overlay */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5 pointer-events-none" />
            
            {/* Gradient Overlays */}
            <div className="absolute top-0 left-0 w-full h-96 bg-gradient-to-b from-purple-900/20 to-transparent pointer-events-none" />
            <div className="absolute bottom-0 left-0 w-full h-96 bg-gradient-to-t from-black to-transparent pointer-events-none" />

            {/* Header */}
            <header className="relative z-10 pt-8 pb-4 px-6">
                <nav className="max-w-7xl mx-auto flex justify-between items-center">
                    <Link href="/" className="flex items-center gap-3 group">
                        <Hexagon className="w-8 h-8 text-[var(--color-primary)] group-hover:rotate-180 transition-transform duration-700" />
                        <span className="text-xl font-black tracking-tight">ALSHAM QUANTUM</span>
                    </Link>
                    <div className="flex items-center gap-6">
                        <Link href="/login" className="text-sm text-gray-400 hover:text-white transition-colors">
                            Login
                        </Link>
                        <Link
                            href="/signup"
                            className="px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg text-sm font-medium transition-all"
                        >
                            Criar Conta
                        </Link>
                    </div>
                </nav>
            </header>

            {/* Hero Section */}
            <section className="relative z-10 pt-16 pb-12 px-6 text-center">
                <div className="max-w-4xl mx-auto">
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-500/30 rounded-full mb-8">
                        <Sparkles className="w-4 h-4 text-yellow-400" />
                        <span className="text-sm font-medium text-yellow-300">
                            Oferta de Lançamento • Primeiros 100 Clientes
                        </span>
                    </div>
                    
                    <h1 className="text-5xl md:text-7xl font-black tracking-tight mb-6 leading-tight">
                        {user && !hasAccess
                            ? 'Upgrade seu plano para acessar o ALSHAM QUANTUM'
                            : 'Transforme sua empresa com'
                        }{' '}
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-500 to-yellow-400">
                            {user && !hasAccess ? 'Premium' : 'Inteligência Artificial'}
                        </span>
                    </h1>

                    <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-8 leading-relaxed">
                        {user && !hasAccess
                            ? 'Desbloqueie todo o potencial dos 139 agentes de IA trabalhando 24/7 para automatizar suas operações.'
                            : '139 agentes de IA trabalhando 24/7 para automatizar suas operações. Sem código. Sem complexidade. Resultados em 24 horas.'
                        }
                    </p>

                    {/* Billing Toggle */}
                    <div className="inline-flex items-center gap-4 p-1 bg-white/5 border border-white/10 rounded-full mb-12">
                        <button
                            onClick={() => setBillingCycle('monthly')}
                            className={`px-6 py-2 rounded-full text-sm font-medium transition-all ${
                                billingCycle === 'monthly' 
                                    ? 'bg-white text-black' 
                                    : 'text-gray-400 hover:text-white'
                            }`}
                        >
                            Mensal
                        </button>
                        <button
                            onClick={() => setBillingCycle('yearly')}
                            className={`px-6 py-2 rounded-full text-sm font-medium transition-all flex items-center gap-2 ${
                                billingCycle === 'yearly' 
                                    ? 'bg-white text-black' 
                                    : 'text-gray-400 hover:text-white'
                            }`}
                        >
                            Anual
                            <span className="px-2 py-0.5 bg-green-500 text-white text-[10px] font-bold rounded-full">
                                -17%
                            </span>
                        </button>
                    </div>
                </div>
            </section>

            {/* Pricing Cards */}
            <section className="relative z-10 px-6 pb-24">
                <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {PLANS.map((plan, index) => (
                        <div
                            key={plan.id}
                            onMouseEnter={() => setSelectedPlan(plan.id)}
                            onMouseLeave={() => setSelectedPlan(null)}
                            className={`
                                relative group rounded-3xl p-[1px] transition-all duration-500
                                ${selectedPlan === plan.id || plan.id === 'enterprise' 
                                    ? `bg-gradient-to-b ${plan.color} shadow-2xl scale-105` 
                                    : 'bg-white/10'}
                                ${plan.id === 'enterprise' ? 'lg:-mt-4 lg:mb-4' : ''}
                            `}
                            style={{
                                boxShadow: selectedPlan === plan.id || plan.id === 'enterprise'
                                    ? `0 0 60px ${plan.glowColor}`
                                    : 'none'
                            }}
                        >
                            {/* Badge */}
                            {plan.badge && (
                                <div className={`absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-gradient-to-r ${plan.color} rounded-full text-xs font-black tracking-wider text-white shadow-lg`}>
                                    {plan.badge}
                                </div>
                            )}

                            <div className="bg-[#0a0a0a] rounded-3xl p-8 h-full flex flex-col relative overflow-hidden">
                                {/* Background Effect */}
                                <div className={`absolute inset-0 bg-gradient-to-b ${plan.color} opacity-5 pointer-events-none`} />
                                
                                {/* Header */}
                                <div className="mb-6 relative z-10">
                                    <div className="flex items-center gap-3 mb-4">
                                        {plan.id === 'starter' && <Zap className="w-8 h-8 text-blue-400" />}
                                        {plan.id === 'pro' && <Rocket className="w-8 h-8 text-purple-400" />}
                                        {plan.id === 'enterprise' && <Crown className="w-8 h-8 text-yellow-400" />}
                                        <h3 className="text-2xl font-black tracking-wider">{plan.name}</h3>
                                    </div>
                                    <p className="text-sm text-gray-400">{plan.description}</p>
                                </div>

                                {/* Price */}
                                <div className="mb-8 relative z-10">
                                    <div className="flex items-baseline gap-2">
                                        <span className="text-sm text-gray-400">R$</span>
                                        <span className="text-5xl font-black">
                                            {billingCycle === 'monthly' 
                                                ? plan.price.toLocaleString('pt-BR')
                                                : getYearlyPrice(plan.price).toLocaleString('pt-BR')
                                            }
                                        </span>
                                        <span className="text-gray-400">
                                            /{billingCycle === 'monthly' ? 'mês' : 'ano'}
                                        </span>
                                    </div>
                                    {billingCycle === 'yearly' && (
                                        <p className="text-sm text-green-400 mt-2">
                                            Economia de R${(plan.price * 2).toLocaleString('pt-BR')}/ano
                                        </p>
                                    )}
                                </div>

                                {/* Features */}
                                <div className="flex-1 relative z-10">
                                    <ul className="space-y-3 mb-6">
                                        {plan.features.map((feature, i) => (
                                            <li key={i} className="flex items-start gap-3 text-sm">
                                                <Check className={`w-5 h-5 flex-shrink-0 ${
                                                    plan.id === 'enterprise' ? 'text-yellow-400' :
                                                    plan.id === 'pro' ? 'text-purple-400' :
                                                    'text-blue-400'
                                                }`} />
                                                <span className="text-gray-300">{feature}</span>
                                            </li>
                                        ))}
                                    </ul>
                                    
                                    {plan.limitations.length > 0 && (
                                        <ul className="space-y-2 border-t border-white/10 pt-4">
                                            {plan.limitations.map((limit, i) => (
                                                <li key={i} className="flex items-start gap-3 text-sm text-gray-500">
                                                    <span className="w-5 h-5 flex items-center justify-center flex-shrink-0">×</span>
                                                    <span>{limit}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    )}
                                </div>

                                {/* CTA Button */}
                                <button
                                    onClick={() => handleCheckout(plan)}
                                    disabled={isLoading !== null}
                                    className={`
                                        relative w-full mt-8 py-4 rounded-xl font-bold text-sm tracking-wider uppercase
                                        transition-all overflow-hidden group/btn
                                        ${plan.id === 'enterprise' 
                                            ? 'bg-gradient-to-r from-yellow-400 to-orange-500 text-black hover:shadow-[0_0_40px_rgba(250,204,21,0.5)]' 
                                            : plan.id === 'pro'
                                                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:shadow-[0_0_40px_rgba(168,85,247,0.5)]'
                                                : 'bg-white/10 hover:bg-white/20 text-white border border-white/20'
                                        }
                                        disabled:opacity-50 disabled:cursor-not-allowed
                                    `}
                                >
                                    {isLoading === plan.id ? (
                                        <span className="flex items-center justify-center gap-2">
                                            <div className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin" />
                                            Processando...
                                        </span>
                                    ) : (
                                        <span className="flex items-center justify-center gap-2">
                                            {user && !hasAccess
                                                ? (plan.id === 'enterprise' ? 'Upgrade para Enterprise' : `Upgrade para ${plan.name}`)
                                                : (plan.id === 'enterprise' ? 'Começar Agora' : 'Assinar Plano')
                                            }
                                            <ArrowRight className="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" />
                                        </span>
                                    )}
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Trust Section */}
            <section className="relative z-10 px-6 pb-24">
                <div className="max-w-5xl mx-auto">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
                        <div className="p-6">
                            <div className="text-4xl font-black text-white mb-2">139+</div>
                            <div className="text-sm text-gray-400">Agentes de IA Ativos</div>
                        </div>
                        <div className="p-6">
                            <div className="text-4xl font-black text-white mb-2">99.9%</div>
                            <div className="text-sm text-gray-400">Uptime Garantido</div>
                        </div>
                        <div className="p-6">
                            <div className="text-4xl font-black text-white mb-2">24/7</div>
                            <div className="text-sm text-gray-400">Auto-Evolução</div>
                        </div>
                        <div className="p-6">
                            <div className="text-4xl font-black text-white mb-2">&lt;50ms</div>
                            <div className="text-sm text-gray-400">Latência Média</div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Grid */}
            <section className="relative z-10 px-6 pb-24">
                <div className="max-w-6xl mx-auto">
                    <h2 className="text-3xl font-black text-center mb-12">
                        Por que escolher o ALSHAM QUANTUM?
                    </h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {[
                            { icon: Brain, title: 'IA que Evolui Sozinha', desc: 'Nossos agentes melhoram automaticamente a cada 10 minutos.' },
                            { icon: Shield, title: 'Segurança Enterprise', desc: 'Criptografia end-to-end e compliance com LGPD.' },
                            { icon: Globe, title: 'Escala Global', desc: 'Infraestrutura distribuída em 3 continentes.' },
                            { icon: Activity, title: 'Monitoramento Real-time', desc: 'Dashboard com métricas em tempo real.' },
                            { icon: Users, title: 'Suporte Dedicado', desc: 'Time de especialistas disponível 24/7.' },
                            { icon: Database, title: 'Integrações Ilimitadas', desc: 'Conecte com qualquer sistema via API.' },
                        ].map((feature, i) => (
                            <div 
                                key={i}
                                className="p-6 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 hover:border-white/20 transition-all group"
                            >
                                <feature.icon className="w-10 h-10 text-[var(--color-primary)] mb-4 group-hover:scale-110 transition-transform" />
                                <h3 className="text-lg font-bold mb-2">{feature.title}</h3>
                                <p className="text-sm text-gray-400">{feature.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Final */}
            <section className="relative z-10 px-6 pb-24">
                <div className="max-w-4xl mx-auto text-center">
                    <div className="p-12 bg-gradient-to-r from-purple-900/30 to-pink-900/30 border border-purple-500/30 rounded-3xl relative overflow-hidden">
                        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 pointer-events-none" />
                        
                        <h2 className="text-4xl font-black mb-4 relative z-10">
                            {user && !hasAccess
                                ? 'Pronto para desbloquear todo o potencial?'
                                : 'Pronto para transformar seu negócio?'
                            }
                        </h2>
                        <p className="text-xl text-gray-400 mb-8 relative z-10">
                            {user && !hasAccess
                                ? 'Faça upgrade hoje e tenha acesso completo ao ALSHAM QUANTUM.'
                                : 'Comece hoje e veja resultados em 24 horas.'
                            }
                        </p>

                        <button
                            onClick={() => handleCheckout(PLANS[2])}
                            className="px-12 py-5 bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-black text-lg rounded-xl hover:shadow-[0_0_60px_rgba(250,204,21,0.5)] transition-all relative z-10"
                        >
                            {user && !hasAccess
                                ? 'Upgrade para Enterprise • R$9.900/mês'
                                : 'Começar com Enterprise • R$9.900/mês'
                            }
                        </button>
                        
                        <p className="text-xs text-gray-500 mt-4 relative z-10">
                            Garantia de 30 dias • Cancele quando quiser • Suporte 24/7
                        </p>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="relative z-10 border-t border-white/10 py-12 px-6">
                <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
                    <div className="flex items-center gap-3">
                        <Hexagon className="w-6 h-6 text-[var(--color-primary)]" />
                        <span className="text-sm font-bold">ALSHAM QUANTUM</span>
                    </div>
                    <div className="flex items-center gap-6 text-sm text-gray-400">
                        <Link href="/terms" className="hover:text-white transition-colors">Termos</Link>
                        <Link href="/privacy" className="hover:text-white transition-colors">Privacidade</Link>
                        <Link href="/contact" className="hover:text-white transition-colors">Contato</Link>
                    </div>
                    <div className="text-sm text-gray-500">
                        © 2024 ALSHAM Global. Todos os direitos reservados.
                    </div>
                </div>
            </footer>
        </div>
    );
}

