/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - STRIPE CLIENT
 * ═══════════════════════════════════════════════════════════════
 */

import { loadStripe } from '@stripe/stripe-js';

let stripePromise: Promise<any> | null = null;

export const getStripe = () => {
    if (!stripePromise) {
        stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY || '');
    }
    return stripePromise;
};

// Configuração dos planos
export const PLANS = {
    starter: {
        id: 'starter',
        name: 'Starter',
        price: 990,
        features: [
            '10 Agentes de IA',
            '1.000 requests/mês',
            'Dashboard básico',
        ],
        limits: {
            agents: 10,
            requests: 1000,
            features: ['dashboard_basic'],
        }
    },
    pro: {
        id: 'pro',
        name: 'Pro',
        price: 4900,
        features: [
            '50 Agentes de IA',
            '10.000 requests/mês',
            'ORION Voice',
            'Auto-evolução básica',
        ],
        limits: {
            agents: 50,
            requests: 10000,
            features: ['dashboard_full', 'orion_voice', 'auto_evolution_basic'],
        }
    },
    enterprise: {
        id: 'enterprise',
        name: 'Enterprise',
        price: 9900,
        features: [
            'Agentes ilimitados',
            'Requests ilimitados',
            'God Mode',
            'Auto-evolução 5 níveis',
        ],
        limits: {
            agents: Infinity,
            requests: Infinity,
            features: ['god_mode', 'auto_evolution_full', 'white_label', 'dedicated_support'],
        }
    },
} as const;

export type PlanId = keyof typeof PLANS;

export function getPlanById(planId: string) {
    return PLANS[planId as PlanId] || PLANS.starter;
}

export function hasFeature(planId: string, feature: string): boolean {
    const plan = getPlanById(planId);
    return plan.limits.features.includes(feature);
}

