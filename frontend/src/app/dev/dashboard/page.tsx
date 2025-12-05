/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - DEV DASHBOARD (BYPASS TOTAL)
 * ═══════════════════════════════════════════════════════════════
 * 📁 PATH: frontend/src/app/dev/dashboard/page.tsx
 * 🛠️ Rota de desenvolvimento - acesso direto sem auth
 * ═══════════════════════════════════════════════════════════════
 */

'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Loader2 } from 'lucide-react';

export default function DevDashboardPage() {
    const router = useRouter();

    useEffect(() => {
        // Mock de usuário logado e pago para desenvolvimento
        console.log('🛠️ DEV MODE: Simulando usuário logado e pago');

        // Redirecionar para o dashboard real após um delay
        const timer = setTimeout(() => {
            router.push('/dashboard');
        }, 1000);

        return () => clearTimeout(timer);
    }, [router]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-black">
            <div className="text-center">
                <div className="w-20 h-20 rounded-full bg-green-500/20 border border-green-500/50 flex items-center justify-center mx-auto mb-6">
                    <Loader2 className="w-10 h-10 text-green-400 animate-spin" />
                </div>
                <h1 className="text-2xl font-black text-white mb-2">
                    🛠️ MODO DESENVOLVIMENTO
                </h1>
                <p className="text-gray-400 font-mono text-sm mb-4">
                    Bypass de autenticação ativado
                </p>
                <p className="text-gray-500 font-mono text-xs">
                    Redirecionando para dashboard...
                </p>

                <div className="mt-6 p-4 bg-white/5 rounded-lg border border-white/10">
                    <div className="text-xs text-gray-500 mb-2">Mock Data (Dev Only):</div>
                    <div className="text-left text-xs font-mono text-green-400">
                        ✓ Usuário: dev@alsham.com<br/>
                        ✓ Plano: enterprise<br/>
                        ✓ Status: pago<br/>
                        ✓ Badge: dourada
                    </div>
                </div>
            </div>
        </div>
    );
}
