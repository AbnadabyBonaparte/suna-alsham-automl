/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM - SUBSCRIPTION HOOK
 * ═══════════════════════════════════════════════════════════════
 */

import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { getPlanById, hasFeature, type PlanId } from '@/lib/stripe';

interface SubscriptionState {
    isLoading: boolean;
    isSubscribed: boolean;
    plan: PlanId | null;
    planName: string;
    status: string;
    isEnterprise: boolean;
    isPro: boolean;
    canAccessFeature: (feature: string) => boolean;
    billingCycle: 'monthly' | 'yearly' | null;
    subscriptionEnd: string | null;
}

export function useSubscription(): SubscriptionState {
    const [state, setState] = useState<SubscriptionState>({
        isLoading: true,
        isSubscribed: false,
        plan: null,
        planName: '',
        status: '',
        isEnterprise: false,
        isPro: false,
        canAccessFeature: () => false,
        billingCycle: null,
        subscriptionEnd: null,
    });

    useEffect(() => {
        async function loadSubscription() {
            // MODO DESENVOLVIMENTO - Mock subscription
            const isDevMode = process.env.NEXT_PUBLIC_DEV_MODE === 'true';
            if (isDevMode) {
                console.log('🛠️ DEV MODE: Usando mock subscription (enterprise)');
                setState({
                    isLoading: false,
                    isSubscribed: true,
                    plan: 'enterprise',
                    planName: 'Enterprise',
                    status: 'active',
                    isEnterprise: true,
                    isPro: false,
                    canAccessFeature: () => true,
                    billingCycle: 'monthly',
                    subscriptionEnd: null,
                });
                return;
            }

            try {
                const { data: { user } } = await supabase.auth.getUser();

                if (!user) {
                    setState(prev => ({ ...prev, isLoading: false }));
                    return;
                }

                const { data: profile } = await supabase
                    .from('profiles')
                    .select('subscription_plan, subscription_status, billing_cycle, subscription_end')
                    .eq('id', user.id)
                    .single();

                if (profile) {
                    const plan = profile.subscription_plan as PlanId;
                    const planInfo = getPlanById(plan);
                    
                    setState({
                        isLoading: false,
                        isSubscribed: profile.subscription_status === 'active',
                        plan,
                        planName: planInfo.name,
                        status: profile.subscription_status,
                        isEnterprise: plan === 'enterprise',
                        isPro: plan === 'pro' || plan === 'enterprise',
                        canAccessFeature: (feature: string) => hasFeature(plan, feature),
                        billingCycle: profile.billing_cycle,
                        subscriptionEnd: profile.subscription_end,
                    });
                } else {
                    setState(prev => ({ ...prev, isLoading: false }));
                }
            } catch (error) {
                console.error('Error loading subscription:', error);
                setState(prev => ({ ...prev, isLoading: false }));
            }
        }

        loadSubscription();

        // Escutar mudanças na sessão
        const { data: { subscription } } = supabase.auth.onAuthStateChange(() => {
            loadSubscription();
        });

        return () => subscription.unsubscribe();
    }, []);

    return state;
}

