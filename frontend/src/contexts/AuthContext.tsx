"use client";

import { createContext, useContext, useEffect, useState } from 'react';
import { User, Session, AuthError, SupabaseClient } from '@supabase/supabase-js';
import { createClient } from '@supabase/supabase-js';
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

interface AuthContextType {
    user: User | null;
    session: Session | null;
    loading: boolean;
    signIn: (email: string, password: string) => Promise<{ error: AuthError | null }>;
    signUp: (email: string, password: string) => Promise<{ error: AuthError | null }>;
    signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Lazy client initialization para evitar erros durante build
let _supabaseClient: SupabaseClient | null = null;

function getSupabaseClient(): SupabaseClient {
    if (_supabaseClient) {
        return _supabaseClient;
    }
    
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    
    if (!supabaseUrl || !supabaseAnonKey) {
        throw new Error('Missing Supabase environment variables');
    }
    
    _supabaseClient = createClient(supabaseUrl, supabaseAnonKey);
    return _supabaseClient;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [session, setSession] = useState<Session | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        // MODO DESENVOLVIMENTO - Mock user
        const isDevMode = process.env.NEXT_PUBLIC_DEV_MODE === 'true';
        console.log('🔍 DEV MODE check:', isDevMode, 'NEXT_PUBLIC_DEV_MODE:', process.env.NEXT_PUBLIC_DEV_MODE);

        if (isDevMode) {
            console.log('🛠️ DEV MODE: Usando mock user para desenvolvimento');
            setSession(DEV_SESSION);
            setUser(DEV_USER);
            setLoading(false);
            return;
        }

        const supabase = getSupabaseClient();

        supabase.auth.getSession().then(({ data: { session } }) => {
            setSession(session);
            setUser(session?.user ?? null);
            setLoading(false);
        });

        const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
            setSession(session);
            setUser(session?.user ?? null);
            setLoading(false);
        });

        return () => subscription.unsubscribe();
    }, []);

    const signIn = async (email: string, password: string) => {
        const supabase = getSupabaseClient();
        const { error } = await supabase.auth.signInWithPassword({
            email,
            password,
        });

        if (!error) {
            router.push('/dashboard');
        }

        return { error };
    };

    const signUp = async (email: string, password: string) => {
        const supabase = getSupabaseClient();
        const { error } = await supabase.auth.signUp({
            email,
            password,
        });

        if (!error) {
            router.push('/pricing');
        }

        return { error };
    };

    const signOut = async () => {
        const supabase = getSupabaseClient();
        await supabase.auth.signOut();
        router.push('/login');
    };

    return (
        <AuthContext.Provider value={{ user, session, loading, signIn, signUp, signOut }}>
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
