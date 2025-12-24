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
    onboarding_completed?: boolean;
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
                .select('subscription_plan, subscription_status, founder_access, onboarding_completed')
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
                subscription_status: 'active',
                onboarding_completed: true
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
        try {
            console.log('[AUTH] Tentando fazer login para:', email);
            
            const { data, error } = await supabase.auth.signInWithPassword({
                email,
                password,
            });

            if (error) {
                console.error('[AUTH] Erro no login:', {
                    message: error.message,
                    status: error.status,
                    name: error.name,
                });
                return { error };
            }

            console.log('[AUTH] Login bem-sucedido, carregando usuário...');

            // Aguardar um pouco para garantir que a sessão está estabelecida
            await new Promise(resolve => setTimeout(resolve, 100));

            // Carregar metadata imediatamente após login
            const { data: { user }, error: userError } = await supabase.auth.getUser();
            
            if (userError) {
                console.error('[AUTH] Erro ao obter usuário:', userError);
                return { 
                    error: {
                        message: 'Erro ao obter dados do usuário após login',
                        status: 500,
                    } as AuthError
                };
            }

            if (user) {
                console.log('[AUTH] Usuário obtido:', user.id);
                const metadata = await loadUserMetadata(user.id);
                console.log('[AUTH] Metadata carregada:', metadata);
                setMetadata(metadata);

                // Redirecionar baseado no estado do onboarding
                // Usar router.push para evitar reload completo da página
                if (metadata?.onboarding_completed) {
                    console.log('[AUTH] Onboarding completo, redirecionando para dashboard');
                    router.push('/dashboard');
                } else {
                    console.log('[AUTH] Onboarding não completo, redirecionando para onboarding');
                    router.push('/onboarding');
                }
            } else {
                console.error('[AUTH] Usuário não encontrado após login');
                return { 
                    error: {
                        message: 'Usuário não encontrado após login',
                        status: 500,
                    } as AuthError
                };
            }

            return { error: null };
        } catch (err: any) {
            console.error('[AUTH] Erro inesperado no login:', err);
            return { 
                error: {
                    message: err.message || 'Erro ao fazer login. Verifique suas credenciais.',
                    status: 500,
                } as AuthError
            };
        }
    };

    const signUp = async (email: string, password: string) => {
        const { error } = await supabase.auth.signUp({
            email,
            password,
        });

        if (!error) {
            // Novos usuários sempre vão para onboarding
            router.push('/onboarding');
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
