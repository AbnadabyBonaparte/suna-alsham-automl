"use client";

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';
import { Lock, Mail, AlertCircle, Loader2, CheckCircle } from 'lucide-react';
import { supabase } from '@/lib/supabase';

export default function SignupPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [loading, setLoading] = useState(false);
    const [oauthLoading, setOauthLoading] = useState<string | null>(null);
    const { signUp } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccess(false);

        // Validation
        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (password.length < 6) {
            setError('Password must be at least 6 characters');
            return;
        }

        setLoading(true);

        const { error } = await signUp(email, password);

        if (error) {
            setError(error.message);
            setLoading(false);
        } else {
            setSuccess(true);
            setLoading(false);
        }
    };

    const handleOAuthSignup = async (provider: 'google' | 'github') => {
        if (!supabase) {
            setError("Authentication service not configured");
            return;
        }
        setOauthLoading(provider);
        setError('');

        const { error } = await supabase.auth.signInWithOAuth({
            provider,
            options: {
                redirectTo: `${window.location.origin}/auth/callback`,
            },
        });

        if (error) {
            setError(error.message);
            setOauthLoading(null);
        }
    };

    return (
        <div className="min-h-screen bg-black flex items-center justify-center p-4 relative overflow-hidden">
            {/* Animated Background */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-20" />
            <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-black to-purple-900/20" />

            {/* Glowing Orbs */}
            <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-blue-500/30 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-purple-500/30 rounded-full blur-3xl animate-pulse delay-1000" />

            {/* Signup Card */}
            <div className="relative z-10 w-full max-w-md">
                <div className="bg-zinc-900/80 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl">
                    {/* Header */}
                    <div className="text-center mb-8">
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
                            ALSHAM QUANTUM
                        </h1>
                        <p className="text-zinc-400 text-sm">Operator Registration Portal</p>
                    </div>

                    {/* Success Alert */}
                    {success && (
                        <div className="mb-6 bg-green-500/10 border border-green-500/50 rounded-lg p-4 flex items-start gap-3">
                            <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                            <div>
                                <p className="text-green-400 text-sm font-medium">Registration Successful!</p>
                                <p className="text-green-400/70 text-xs mt-1">Check your email to confirm your account.</p>
                            </div>
                        </div>
                    )}

                    {/* Error Alert */}
                    {error && (
                        <div className="mb-6 bg-red-500/10 border border-red-500/50 rounded-lg p-4 flex items-start gap-3">
                            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                            <p className="text-red-400 text-sm">{error}</p>
                        </div>
                    )}

                    {/* OAuth Buttons */}
                    <div className="space-y-3 mb-6">
                        {/* Google OAuth */}
                        <button
                            onClick={() => handleOAuthSignup('google')}
                            disabled={oauthLoading !== null || success}
                            className="w-full bg-white hover:bg-gray-50 text-gray-800 font-semibold py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg border border-gray-200"
                        >
                            {oauthLoading === 'google' ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <svg className="w-5 h-5" viewBox="0 0 24 24">
                                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                                </svg>
                            )}
                            {oauthLoading === 'google' ? 'Connecting...' : 'Continue with Google'}
                        </button>

                        {/* GitHub OAuth */}
                        <button
                            onClick={() => handleOAuthSignup('github')}
                            disabled={oauthLoading !== null || success}
                            className="w-full bg-[#24292F] hover:bg-[#2c3137] text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                        >
                            {oauthLoading === 'github' ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                                </svg>
                            )}
                            {oauthLoading === 'github' ? 'Connecting...' : 'Continue with GitHub'}
                        </button>
                    </div>

                    {/* Divider */}
                    <div className="relative mb-6">
                        <div className="absolute inset-0 flex items-center">
                            <div className="w-full border-t border-white/10"></div>
                        </div>
                        <div className="relative flex justify-center text-sm">
                            <span className="px-4 bg-zinc-900 text-zinc-500">Or continue with email</span>
                        </div>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="space-y-5">
                        {/* Email Field */}
                        <div>
                            <label className="block text-zinc-300 text-sm font-medium mb-2">
                                Email Address
                            </label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                    className="w-full bg-black/50 border border-white/10 rounded-lg pl-11 pr-4 py-3 text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
                                    placeholder="operator@alsham.quantum"
                                />
                            </div>
                        </div>

                        {/* Password Field */}
                        <div>
                            <label className="block text-zinc-300 text-sm font-medium mb-2">
                                Password
                            </label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    className="w-full bg-black/50 border border-white/10 rounded-lg pl-11 pr-4 py-3 text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        {/* Confirm Password Field */}
                        <div>
                            <label className="block text-zinc-300 text-sm font-medium mb-2">
                                Confirm Password
                            </label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
                                <input
                                    type="password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    required
                                    className="w-full bg-black/50 border border-white/10 rounded-lg pl-11 pr-4 py-3 text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading || success || oauthLoading !== null}
                            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-500/50"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    Creating Access...
                                </>
                            ) : success ? (
                                <>
                                    <CheckCircle className="w-5 h-5" />
                                    Access Granted
                                </>
                            ) : (
                                'Request Neural Access'
                            )}
                        </button>
                    </form>

                    {/* Login Link */}
                    <div className="mt-6 text-center">
                        <p className="text-zinc-400 text-sm">
                            Already have access?{' '}
                            <Link href="/login" className="text-blue-400 hover:text-blue-300 font-medium transition-colors">
                                Sign In
                            </Link>
                        </p>
                    </div>
                </div>

                {/* Footer */}
                <p className="text-center text-zinc-600 text-xs mt-6">
                    Secured by Quantum Encryption • ALSHAM Neural Core
                </p>
            </div>
        </div>
    );
}
