'use client';

import MegaCounter from '@/components/value/MegaCounter';
import MetricCard from '@/components/value/MetricCard';
import { useValueCalculation } from '@/hooks/useValueCalculation';
import { motion } from 'framer-motion';

export default function ValueDashboard() {
    const metrics = useValueCalculation();

    return (
        <div className="min-h-screen p-6 md:p-8">
            {/* Header */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-8"
            >
                <h1 className="font-orbitron text-4xl font-bold text-[var(--theme-text-primary)] mb-2">
                    Dashboard de Valor
                </h1>
                <p className="text-[var(--theme-text-secondary)]">
                    Acompanhe o impacto real do SUNA ALSHAM na sua produtividade
                </p>
            </motion.div>

            {/* Mega Counter */}
            <div className="mb-8">
                <MegaCounter
                    value={metrics.totalValue}
                    label="VALOR TOTAL GERADO"
                    sublabel="Economia + Produtividade + Automação"
                />
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <MetricCard
                    icon="⏱️"
                    value={metrics.timeSaved}
                    label="TEMPO ECONOMIZADO"
                    description="Esta semana"
                    trend="+37%"
                />
                <MetricCard
                    icon="🤖"
                    value={metrics.tasksAutomated.toLocaleString('pt-BR')}
                    label="TAREFAS AUTOMATIZADAS"
                    description="Este mês"
                    trend="+124%"
                />
                <MetricCard
                    icon="📈"
                    value={metrics.productivityImprovement}
                    label="MELHORIA DE PRODUTIVIDADE"
                    description="vs mês anterior"
                    trend="🔥 Record!"
                />
                <MetricCard
                    icon="🎯"
                    value={metrics.rankingPercentile}
                    label="RANKING DE PERFORMANCE"
                    description="dos usuários"
                    badge="Elite"
                />
            </div>

            {/* Placeholder for future charts */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="glass-card p-8 rounded-2xl border border-[var(--theme-card-border)] text-center"
            >
                <h3 className="font-orbitron text-xl text-[var(--theme-text-primary)] mb-4">
                    Gráficos de Evolução
                </h3>
                <p className="text-[var(--theme-text-secondary)] text-sm">
                    Em breve: gráficos interativos de evolução de valor ao longo do tempo
                </p>
            </motion.div>
        </div>
    );
}
