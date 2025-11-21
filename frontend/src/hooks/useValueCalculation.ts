'use client';

import { useState, useEffect } from 'react';

export interface ValueMetrics {
    totalValue: number;
    timeSaved: string;
    tasksAutomated: number;
    productivityImprovement: string;
    rankingPercentile: string;
}

// Mock data - In production, this would come from Supabase
export function useValueCalculation(): ValueMetrics {
    const [metrics, setMetrics] = useState<ValueMetrics>({
        totalValue: 0,
        timeSaved: '0h 0min',
        tasksAutomated: 0,
        productivityImprovement: '+0%',
        rankingPercentile: 'Top 50%'
    });

    useEffect(() => {
        // Simulate calculation based on user activity
        // In production, fetch from Supabase and calculate
        const calculateMetrics = () => {
            // Example calculations
            const hoursSaved = Math.floor(Math.random() * 300) + 150; // 150-450 hours
            const minutesSaved = Math.floor(Math.random() * 60);
            const tasksCompleted = Math.floor(Math.random() * 2000) + 800; // 800-2800 tasks

            const timeValue = hoursSaved * 150; // R$ 150/hour
            const automationValue = tasksCompleted * 30; // R$ 30/task
            const insightValue = Math.floor(Math.random() * 50) * 500; // insights
            const optimizationValue = Math.floor(Math.random() * 100) * 200; // optimizations

            const totalValue = timeValue + automationValue + insightValue + optimizationValue;

            const productivity = Math.floor(Math.random() * 100) + 50; // 50-150%
            const ranking = Math.floor(Math.random() * 15) + 5; // Top 5-20%

            setMetrics({
                totalValue,
                timeSaved: `${hoursSaved}h ${minutesSaved}min`,
                tasksAutomated: tasksCompleted,
                productivityImprovement: `+${productivity}%`,
                rankingPercentile: `Top ${ranking}%`
            });
        };

        calculateMetrics();
    }, []);

    return metrics;
}
