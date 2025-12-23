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
        color: '#00FFD0' 
    },
    { 
        id: 'observer', 
        title: 'THE OBSERVER', 
        desc: 'Monitoramento de segurança e logs.', 
        icon: Eye, 
        color: '#8B5CF6' 
    },
    { 
        id: 'strategist', 
        title: 'THE STRATEGIST', 
        desc: 'Análise de dados e ROI financeiro.', 
        icon: Zap, 
        color: '#F59E0B' 
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

            // Fundo
            ctx.fillStyle = '#000000';
            
            // Se estiver no WARP, rastro longo (Motion Blur)
            if (step === 'warp') {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
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

                    ctx.strokeStyle = '#FFFFFF';
                    ctx.lineWidth = 2 * scale;
                    ctx.beginPath();
                    ctx.moveTo(prevX, prevY);
                    ctx.lineTo(x, y);
                    ctx.stroke();
                } else {
                    // Se normal, desenha pontos
                    const size = (1 - star.z / 2000) * 3;
                    ctx.fillStyle = '#FFFFFF';
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

    // Verificar se já completou onboarding ao carregar a página
    useEffect(() => {
        const checkOnboarding = async () => {
            try {
                const supabase = createClient();
                const { data: { user } } = await supabase.auth.getUser();
                
                if (user) {
                    const { data: profile } = await supabase
                        .from('profiles')
                        .select('onboarding_completed')
                        .eq('id', user.id)
                        .single();

                    if (profile?.onboarding_completed) {
                        router.push('/dashboard');
                    }
                }
            } catch (error) {
                // Ignora erros silenciosamente
            }
        };

        if (step === 'select') {
            checkOnboarding();
        }
    }, [step, router]);

    const handleLaunch = async () => {
        if (!selectedClass || isSaving) return;

        setIsSaving(true);
        setStep('warp');

        try {
            const supabase = createClient();
            const { data: { user } } = await supabase.auth.getUser();

            if (!user) {
                console.error('[ONBOARDING] Usuário não autenticado');
                router.push('/login');
                return;
            }

            // Verificar se já completou onboarding para evitar salvamento duplicado
            const { data: existingProfile } = await supabase
                .from('profiles')
                .select('onboarding_completed')
                .eq('id', user.id)
                .single();

            if (existingProfile?.onboarding_completed) {
                console.log('[ONBOARDING] Onboarding já completado, redirecionando...');
                setTimeout(() => {
                    router.push('/dashboard');
                }, 1000);
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
        } catch (error) {
            console.error('[ONBOARDING] Erro inesperado:', error);
            setIsSaving(false);
            return;
        }

        // Tempo do salto no hiperespaço antes de ir pro dashboard
        setTimeout(() => {
            console.log('[ONBOARDING] Redirecionando para dashboard...');
            router.push('/dashboard');
        }, 2500);
    };

    return (
        <div className="min-h-screen w-full relative overflow-hidden font-sans text-white bg-black">
            
            {/* CANVAS BACKGROUND (STARFIELD) */}
            <canvas ref={canvasRef} className="absolute inset-0 w-full h-full z-0" />

            {/* CONTEÚDO */}
            <div className="relative z-10 flex flex-col items-center justify-center min-h-screen p-6">
                
                {/* FASE 1: BOOT SEQUENCE */}
                {step === 'boot' && (
                    <div className="w-full max-w-lg bg-black/80 border border-green-500/30 p-8 rounded-xl font-mono text-sm shadow-2xl backdrop-blur-sm">
                        <div className="flex items-center gap-2 mb-4 border-b border-green-500/20 pb-2">
                            <Terminal className="w-4 h-4 text-green-500" />
                            <span className="text-green-500 font-bold">SYSTEM BOOT</span>
                        </div>
                        <div className="space-y-1">
                            {bootLines.map((line, i) => (
                                <div key={i} className="text-green-400/80">
                                    <span className="mr-2 text-green-600">&gt;</span>
                                    {line}
                                </div>
                            ))}
                            <div className="animate-pulse text-green-500">_</div>
                        </div>
                    </div>
                )}

                {/* FASE 2: CLASS SELECTION */}
                {step === 'select' && (
                    <div className="w-full max-w-5xl animate-fadeIn">
                        <div className="text-center mb-12">
                            <h1 className="text-4xl md:text-5xl font-black tracking-tighter mb-2">INITIALIZE PROFILE</h1>
                            <p className="text-gray-400 font-mono text-sm uppercase tracking-widest">Select your operating paradigm</p>
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
                                                ? 'bg-white/10 border-white scale-105 shadow-[0_0_30px_rgba(255,255,255,0.2)]' 
                                                : 'bg-black/40 border-white/10 hover:bg-white/5 hover:border-white/30 hover:scale-102'
                                            }
                                        `}
                                    >
                                        <div>
                                            <div 
                                                className={`p-4 rounded-2xl w-fit mb-6 transition-colors ${isSelected ? 'bg-white text-black' : 'bg-white/5 text-white'}`}
                                                style={{ color: isSelected ? 'black' : cls.color }}
                                            >
                                                <cls.icon className="w-8 h-8" />
                                            </div>
                                            <h3 className="text-2xl font-bold mb-2 tracking-tight">{cls.title}</h3>
                                            <p className="text-sm text-gray-400 leading-relaxed">{cls.desc}</p>
                                        </div>

                                        <div className={`flex items-center gap-2 text-xs font-bold uppercase tracking-widest transition-colors ${isSelected ? 'text-white' : 'text-gray-600'}`}>
                                            {isSelected ? <Check className="w-4 h-4" /> : <div className="w-4 h-4 rounded-full border border-gray-600" />}
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
                                className="group relative px-8 py-4 bg-white text-black rounded-full font-bold text-sm tracking-[0.2em] uppercase hover:scale-105 transition-transform flex items-center gap-3 shadow-[0_0_20px_white] disabled:opacity-50 disabled:cursor-not-allowed"
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
                        <h1 className="text-6xl md:text-9xl font-black text-white tracking-tighter animate-ping opacity-50">
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
