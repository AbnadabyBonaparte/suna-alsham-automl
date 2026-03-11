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
        console.log('[DEV] Redirecionando para dashboard...');

        // Redirecionar para o dashboard real após um delay
        const timer = setTimeout(() => {
            router.push('/dashboard');
        }, 1000);

        return () => clearTimeout(timer);
    }, [router]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-background">
            <div className="text-center">
                <div className="w-20 h-20 rounded-full bg-success/20 border border-success/50 flex items-center justify-center mx-auto mb-6">
                    <Loader2 className="w-10 h-10 text-success animate-spin" />
                </div>
                <h1 className="text-2xl font-black text-text mb-2">
                    MODO DESENVOLVIMENTO
                </h1>
                <p className="text-textSecondary font-mono text-sm mb-4">
                    Bypass de autenticação ativado
                </p>
                <p className="text-textSecondary font-mono text-xs">
                    Redirecionando para dashboard...
                </p>
            </div>
        </div>
    );
}
