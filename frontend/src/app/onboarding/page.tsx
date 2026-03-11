/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - ONBOARDING (SYSTEM BOOT)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/onboarding/page.tsx
 * 📋 Sequência de inicialização estilo BIOS + Warp Speed
 * ═══════════════════════════════════════════════════════════════
 */

"use client";

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Cpu, Eye, Zap, Check, ChevronRight, Terminal } from 'lucide-react';
import { createClient } from '@/lib/supabase/client';

// Classes de Operador
const CLASSES = [
    { 
        id: 'architect', 
        title: 'THE ARCHITECT', 
        desc: 'Foco em construção e criação de agentes.', 
        icon: Cpu, 
        color: 'var(--color-primary)' 
    },
    { 
        id: 'observer', 
        title: 'THE OBSERVER', 
        desc: 'Monitoramento de segurança e logs.', 
        icon: Eye, 
        color: 'var(--color-accent)' 
    },
    { 
        id: 'strategist', 
        title: 'THE STRATEGIST', 
        desc: 'Análise de dados e ROI financeiro.', 
        icon: Zap, 
        color: 'var(--color-warning)' 
    },
];

export default function OnboardingPage() {
    const router = useRouter();
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    // Estados
    const [step, setStep] = useState<'boot' | 'select' | 'warp'>('boot');
    const [bootLines, setBootLines] = useState<string[]>([]);
    const [selectedClass, setSelectedClass] = useState<string | null>(null);
    const [isSaving, setIsSaving] = useState(false);
    const [hasCheckedOnboarding, setHasCheckedOnboarding] = useState(false);
    const isRedirectingRef = useRef(false);

    // 1. SEQUÊNCIA DE BOOT (TEXTO DE TERMINAL)
    useEffect(() => {
        if (step !== 'boot') return;

        const lines = [
            "INITIALIZING ALSHAM KERNEL v13.3...",
            "LOADING QUANTUM MODULES... [OK]",
            "DECRYPTING USER BIOMETRICS... [OK]",
            "CONNECTING TO NEURAL NET... [OK]",
            "ESTABLISHING SECURE UPLINK... [OK]",
            "MOUNTING VIRTUAL REALITY ENGINE...",
            "SYNCING WITH GLOBAL SERVERS...",
            "SYSTEM READY."
        ];

        let currentLine = 0;
        const interval = setInterval(() => {
            if (currentLine >= lines.length) {
                clearInterval(interval);
                setTimeout(() => setStep('select'), 1000);
            } else {
                setBootLines(prev => [...prev, lines[currentLine]]);
                currentLine++;
            }
        }, 300); // Velocidade do texto

        return () => clearInterval(interval);
    }, [step]);

    // 2. ENGINE VISUAL (WARP SPEED / STARS)
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationId: number;
        
        // Estrelas
        const stars: {x: number, y: number, z: number}[] = [];
        const STAR_COUNT = 1000;
        
        for(let i=0; i<STAR_COUNT; i++) {
            stars.push({
                x: (Math.random() - 0.5) * 2000,
                y: (Math.random() - 0.5) * 2000,
                z: Math.random() * 2000
            });
        }

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
        resize();

        const render = () => {
            const w = canvas.width;
            const h = canvas.height;
            const cx = w / 2;
            const cy = h / 2;

            const bgClr = getComputedStyle(document.documentElement).getPropertyValue('--color-background').trim() || '#000000';
            const textClr = getComputedStyle(document.documentElement).getPropertyValue('--color-text').trim() || '#FFFFFF';
            const primaryClr = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#00FFD0';
            ctx.fillStyle = bgClr;
            
            if (step === 'warp') {
                ctx.fillStyle = `${bgClr}1A`;
            }
            ctx.fillRect(0, 0, w, h);

            // Velocidade
            const speed = step === 'warp' ? 50 : (step === 'boot' ? 2 : 0.5);

            // Desenhar Estrelas
            stars.forEach(star => {
                star.z -= speed;
                
                if (star.z <= 0) {
                    star.z = 2000;
                    star.x = (Math.random() - 0.5) * 2000;
                    star.y = (Math.random() - 0.5) * 2000;
                }

                const scale = 500 / (500 + star.z); // Perspectiva
                const x = cx + star.x * scale;
                const y = cy + star.y * scale;

                // Se Warp, desenha linhas
                if (step === 'warp') {
                    const prevScale = 500 / (500 + star.z + speed * 2);
                    const prevX = cx + star.x * prevScale;
                    const prevY = cy + star.y * prevScale;

                    ctx.strokeStyle = textClr;
                    ctx.lineWidth = 2 * scale;
                    ctx.beginPath();
                    ctx.moveTo(prevX, prevY);
                    ctx.lineTo(x, y);
                    ctx.stroke();
                } else {
                    // Se normal, desenha pontos
                    const size = (1 - star.z / 2000) * 3;
                    ctx.fillStyle = textClr;
                    ctx.beginPath();
                    ctx.arc(x, y, size, 0, Math.PI * 2);
                    ctx.fill();
                }
            });

            animationId = requestAnimationFrame(render);
        };

        render();
        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationId);
        };
    }, [step]);

    // Verificar se já completou onboarding ao carregar a página (APENAS UMA VEZ)
    useEffect(() => {
        if (hasCheckedOnboarding || isRedirectingRef.current) return;

        const checkOnboarding = async () => {
            if (isRedirectingRef.current) return;
            
            try {
                const supabase = createClient();
                const { data: { user } } = await supabase.auth.getUser();
                
                if (user && !isRedirectingRef.current) {
                    const { data: profile } = await supabase
                        .from('profiles')
                        .select('onboarding_completed')
                        .eq('id', user.id)
                        .single();

                    if (profile?.onboarding_completed && !isRedirectingRef.current) {
                        console.log('[ONBOARDING] Onboarding já completo detectado, redirecionando imediatamente...');
                        isRedirectingRef.current = true;
                        setHasCheckedOnboarding(true);
                        // Usar window.location para forçar reload completo e evitar loops com RSC
                        // Adicionar pequeno delay para garantir que o estado foi atualizado
                        setTimeout(() => {
                            window.location.href = '/dashboard';
                        }, 100);
                        return;
                    }
                }
            } catch (error) {
                console.error('[ONBOARDING] Erro ao verificar onboarding:', error);
            } finally {
                setHasCheckedOnboarding(true);
            }
        };

        // Verificar imediatamente ao montar o componente
        checkOnboarding();
    }, []); // Sem dependências - executa uma vez ao montar

    const handleLaunch = async () => {
        if (!selectedClass || isSaving || isRedirectingRef.current) {
            console.log('[ONBOARDING] Bloqueado:', { selectedClass, isSaving, isRedirecting: isRedirectingRef.current });
            return;
        }

        setIsSaving(true);
        setStep('warp');

        try {
            const supabase = createClient();
            const { data: { user } } = await supabase.auth.getUser();

            if (!user) {
                console.error('[ONBOARDING] Usuário não autenticado');
                setIsSaving(false);
                router.push('/login');
                return;
            }

            // Verificar se já completou onboarding para evitar salvamento duplicado
            const { data: existingProfile } = await supabase
                .from('profiles')
                .select('onboarding_completed')
                .eq('id', user.id)
                .single();

            if (existingProfile?.onboarding_completed || isRedirectingRef.current) {
                console.log('[ONBOARDING] Onboarding já completado, redirecionando...');
                isRedirectingRef.current = true;
                setIsSaving(false);
                localStorage.setItem('onboarding_completed', 'true');
                // Usar window.location para forçar reload completo e evitar loops com RSC
                window.location.href = '/dashboard';
                return;
            }

            // Mapear ID da classe para o role correspondente
            const roleMap: Record<string, string> = {
                'architect': 'architect',
                'observer': 'observer',
                'strategist': 'strategist'
            };

            const role = roleMap[selectedClass] || 'user';

            console.log('[ONBOARDING] Salvando perfil:', { userId: user.id, role, selectedClass });

            // CRÍTICO: Salvar que completou onboarding E o role selecionado
            if (isRedirectingRef.current) {
                console.log('[ONBOARDING] Redirecionamento já em andamento, cancelando salvamento');
                setIsSaving(false);
                return;
            }

            // Marcar no localStorage antes de salvar para evitar loops
            localStorage.setItem('onboarding_saving', 'true');

            const { error } = await supabase
                .from('profiles')
                .update({
                    onboarding_completed: true,
                    role: role,
                    updated_at: new Date().toISOString()
                })
                .eq('id', user.id);

            if (error) {
                console.error('[ONBOARDING] Erro ao salvar perfil:', error);
                setIsSaving(false);
                return;
            }

            console.log('[ONBOARDING] Perfil salvo com sucesso!');
            
            // Limpar flag de salvamento e marcar como completado
            localStorage.removeItem('onboarding_saving');
            localStorage.setItem('onboarding_completed', 'true');
            
            // Marcar que está redirecionando ANTES do timeout
            isRedirectingRef.current = true;
            setHasCheckedOnboarding(true);
        } catch (error) {
            console.error('[ONBOARDING] Erro inesperado:', error);
            setIsSaving(false);
            return;
        }

        // Tempo do salto no hiperespaço antes de ir pro dashboard
        // Usar window.location para forçar reload completo e evitar loops com RSC
        setTimeout(() => {
            if (isRedirectingRef.current) {
                console.log('[ONBOARDING] Redirecionando para dashboard...');
                // Marcar no localStorage que onboarding foi completado
                localStorage.setItem('onboarding_completed', 'true');
                // Usar window.location para forçar reload completo e evitar loops com RSC
                window.location.href = '/dashboard';
            }
        }, 2500);
    };

    return (
        <div className="min-h-screen w-full relative overflow-hidden font-sans text-text bg-background">
            
            {/* CANVAS BACKGROUND (STARFIELD) */}
            <canvas ref={canvasRef} className="absolute inset-0 w-full h-full z-0" />

            {/* CONTEÚDO */}
            <div className="relative z-10 flex flex-col items-center justify-center min-h-screen p-6">
                
                {/* FASE 1: BOOT SEQUENCE */}
                {step === 'boot' && (
                    <div className="w-full max-w-lg bg-background/80 border border-success/30 p-8 rounded-xl font-mono text-sm shadow-2xl backdrop-blur-sm">
                        <div className="flex items-center gap-2 mb-4 border-b border-success/20 pb-2">
                            <Terminal className="w-4 h-4 text-success" />
                            <span className="text-success font-bold">SYSTEM BOOT</span>
                        </div>
                        <div className="space-y-1">
                            {bootLines.map((line, i) => (
                                <div key={i} className="text-success/80">
                                    <span className="mr-2 text-success/60">&gt;</span>
                                    {line}
                                </div>
                            ))}
                            <div className="animate-pulse text-success">_</div>
                        </div>
                    </div>
                )}

                {/* FASE 2: CLASS SELECTION */}
                {step === 'select' && (
                    <div className="w-full max-w-5xl animate-fadeIn">
                        <div className="text-center mb-12">
                            <h1 className="text-4xl md:text-5xl font-black tracking-tighter mb-2">INITIALIZE PROFILE</h1>
                            <p className="text-textSecondary font-mono text-sm uppercase tracking-widest">Select your operating paradigm</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {CLASSES.map((cls) => {
                                const isSelected = selectedClass === cls.id;
                                return (
                                    <button
                                        key={cls.id}
                                        onClick={() => setSelectedClass(cls.id)}
                                        className={`
                                            group relative p-8 rounded-3xl border transition-all duration-300 text-left
                                            flex flex-col justify-between h-80
                                            ${isSelected 
                                                ? 'bg-surface/10 border-text scale-105 shadow-[0_0_30px_rgba(255,255,255,0.2)]' 
                                                : 'bg-background/40 border-border/10 hover:bg-surface/5 hover:border-border/30 hover:scale-102'
                                            }
                                        `}
                                    >
                                        <div>
                                            <div 
                                                className={`p-4 rounded-2xl w-fit mb-6 transition-colors ${isSelected ? 'bg-text text-background' : 'bg-surface/5 text-text'}`}
                                                style={{ color: isSelected ? 'black' : cls.color }}
                                            >
                                                <cls.icon className="w-8 h-8" />
                                            </div>
                                            <h3 className="text-2xl font-bold mb-2 tracking-tight">{cls.title}</h3>
                                            <p className="text-sm text-textSecondary leading-relaxed">{cls.desc}</p>
                                        </div>

                                        <div className={`flex items-center gap-2 text-xs font-bold uppercase tracking-widest transition-colors ${isSelected ? 'text-text' : 'text-textSecondary'}`}>
                                            {isSelected ? <Check className="w-4 h-4" /> : <div className="w-4 h-4 rounded-full border border-textSecondary" />}
                                            {isSelected ? 'Selected' : 'Select'}
                                        </div>
                                    </button>
                                );
                            })}
                        </div>

                        {/* Launch Button */}
                        <div className={`flex justify-center mt-12 transition-opacity duration-500 ${selectedClass && !isSaving ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
                            <button
                                onClick={handleLaunch}
                                disabled={isSaving}
                                className="group relative px-8 py-4 bg-text text-background rounded-full font-bold text-sm tracking-[0.2em] uppercase hover:scale-105 transition-transform flex items-center gap-3 shadow-[0_0_20px_var(--color-glow)] disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {isSaving ? 'Initializing...' : 'Enter The System'}
                                <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                            </button>
                        </div>
                    </div>
                )}

                {/* FASE 3: WARP SPEED (APENAS CANVAS ATIVO) */}
                {step === 'warp' && (
                    <div className="absolute inset-0 flex items-center justify-center z-20">
                        <h1 className="text-6xl md:text-9xl font-black text-text tracking-tighter animate-ping opacity-50">
                            ALSHAM
                        </h1>
                    </div>
                )}

            </div>

            <style jsx>{`
                @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
                .animate-fadeIn { animation: fadeIn 0.8s ease-out forwards; }
            `}</style>
        </div>
    );
}
