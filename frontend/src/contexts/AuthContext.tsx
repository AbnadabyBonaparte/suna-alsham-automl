"use client";

import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { User, Session, AuthError } from '@supabase/supabase-js';
import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';

// Mock user para desenvolvimento
const DEV_USER: User = {
    id: 'dev-user-123',
    email: 'dev@alsham.com',
    user_metadata: {
        name: 'Dev User',
        plan: 'enterprise',
        paid: true,
    },
    app_metadata: {},
    aud: 'authenticated',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    role: 'authenticated',
    email_confirmed_at: new Date().toISOString(),
} as User;

// Mock session para desenvolvimento
const DEV_SESSION: Session = {
    access_token: 'dev-token',
    refresh_token: 'dev-refresh-token',
    expires_at: Date.now() / 1000 + 3600, // 1 hora
    token_type: 'bearer',
    user: DEV_USER,
};

interface UserMetadata {
    founder_access?: boolean;
    subscription_plan?: string;
    subscription_status?: string;
}

interface AuthContextType {
    user: User | null;
    session: Session | null;
    metadata: UserMetadata | null;
    loading: boolean;
    hasFounderAccess: boolean;
    hasAccess: boolean;
    signIn: (email: string, password: string) => Promise<{ error: AuthError | null }>;
    signUp: (email: string, password: string) => Promise<{ error: AuthError | null }>;
    signOut: () => Promise<void>;
    refreshMetadata: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [session, setSession] = useState<Session | null>(null);
    const [metadata, setMetadata] = useState<UserMetadata | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();
    const supabase = useMemo(() => createClient(), []);

    // Função para carregar metadata do usuário
    const loadUserMetadata = async (userId: string) => {
        try {
            const { data: profile, error } = await supabase
                .from('profiles')
                .select('subscription_plan, subscription_status, founder_access')
                .eq('id', userId)
                .single();

            if (error) {
                console.error('Erro ao carregar metadata:', error);
                return null;
            }

            return profile;
        } catch (error) {
            console.error('Erro ao carregar metadata:', error);
            return null;
        }
    };

    useEffect(() => {
        // MODO DESENVOLVIMENTO - Mock user
        const isDevMode = process.env.NEXT_PUBLIC_DEV_MODE === 'true';
        console.log('🔍 DEV MODE check:', isDevMode, 'NEXT_PUBLIC_DEV_MODE:', process.env.NEXT_PUBLIC_DEV_MODE);

        if (isDevMode) {
            console.log('🛠️ DEV MODE: Usando mock user para desenvolvimento');
            setSession(DEV_SESSION);
            setUser(DEV_USER);
            setMetadata({
                founder_access: true,
                subscription_plan: 'enterprise',
                subscription_status: 'active'
            });
            setLoading(false);
            return;
        }

        const handleAuthChange = async (_event: any, session: Session | null) => {
            setSession(session);
            setUser(session?.user ?? null);

            if (session?.user) {
                const metadata = await loadUserMetadata(session.user.id);
                setMetadata(metadata);
            } else {
                setMetadata(null);
            }

            setLoading(false);
        };

        supabase.auth.getSession().then(async ({ data: { session } }) => {
            await handleAuthChange(null, session);
        });

        const { data: { subscription } } = supabase.auth.onAuthStateChange(handleAuthChange);

        return () => subscription.unsubscribe();
    }, []);

    const signIn = async (email: string, password: string) => {
        const { error } = await supabase.auth.signInWithPassword({
            email,
            password,
        });

        if (!error) {
            // Carregar metadata imediatamente após login
            const { data: { user } } = await supabase.auth.getUser();
            if (user) {
                const metadata = await loadUserMetadata(user.id);

                setMetadata(metadata);
            }

            router.push('/dashboard');
            router.refresh();
        }

        return { error };
    };

    const signUp = async (email: string, password: string) => {
        const { error } = await supabase.auth.signUp({
            email,
            password,
        });

        if (!error) {
            router.push('/dashboard');
        }

        return { error };
    };

    const signOut = async () => {
        await supabase.auth.signOut();
        setMetadata(null);
        router.push('/login');
    };

    const refreshMetadata = async () => {
        if (user) {
            const metadata = await loadUserMetadata(user.id);
            setMetadata(metadata);
        }
    };

    // Computed values
    const hasFounderAccess = user?.email === 'casamondestore@gmail.com' || metadata?.founder_access === true;
    const hasAccess = hasFounderAccess ||
                     (metadata?.subscription_plan === 'enterprise' && metadata?.subscription_status === 'active') ||
                     metadata?.subscription_status === 'active';

    return (
        <AuthContext.Provider value={{
            user,
            session,
            metadata,
            loading,
            hasFounderAccess,
            hasAccess,
            signIn,
            signUp,
            signOut,
            refreshMetadata
        }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
