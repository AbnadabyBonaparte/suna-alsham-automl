import Link from 'next/link'
import { AlertCircle } from 'lucide-react'

export default function AuthErrorPage() {
    return (
        <div className="min-h-screen bg-black flex items-center justify-center p-4 relative overflow-hidden">
            {/* Animated Background */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-20" />
            <div className="absolute inset-0 bg-gradient-to-br from-red-900/20 via-black to-purple-900/20" />

            <div className="relative z-10 w-full max-w-md">
                <div className="bg-zinc-900/80 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl text-center">
                    <div className="flex justify-center mb-6">
                        <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center animate-pulse">
                            <AlertCircle className="w-8 h-8 text-red-500" />
                        </div>
                    </div>

                    <h1 className="text-2xl font-bold text-white mb-2">Authentication Error</h1>
                    <p className="text-zinc-400 mb-8">
                        There was a problem authenticating your account. This usually happens when the link has expired or the provider configuration is missing.
                    </p>

                    <div className="space-y-4">
                        <Link
                            href="/login"
                            className="block w-full bg-white text-black font-semibold py-3 px-4 rounded-lg hover:bg-zinc-200 transition-colors"
                        >
                            Return to Login
                        </Link>
                        <Link
                            href="/"
                            className="block w-full bg-zinc-800 text-white font-semibold py-3 px-4 rounded-lg hover:bg-zinc-700 transition-colors"
                        >
                            Back to Home
                        </Link>
                    </div>
                </div>

                <p className="text-center text-zinc-600 text-xs mt-6">
                    Error Code: AUTH_CALLBACK_FAILURE
                </p>
            </div>
        </div>
    )
}
