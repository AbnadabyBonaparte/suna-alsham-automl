'use client';

import React, { Component, ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';

interface Props {
    children: ReactNode;
}

interface State {
    hasError: boolean;
    error: Error | null;
}

export default class ErrorBoundary extends Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        console.error('ErrorBoundary caught an error:', error, errorInfo);
    }

    handleRetry = () => {
        this.setState({ hasError: false, error: null });
        window.location.reload();
    };

    render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen flex items-center justify-center p-6">
                    <div className="glass-card p-8 rounded-2xl border border-red-500/30 max-w-md w-full text-center">
                        <div className="w-16 h-16 rounded-full bg-red-500/10 border border-red-500/30
                            flex items-center justify-center mx-auto mb-4">
                            <AlertTriangle className="w-8 h-8 text-red-400" />
                        </div>

                        <h2 className="font-orbitron text-2xl font-bold text-[var(--theme-text-primary)] mb-2">
                            Erro Detectado
                        </h2>

                        <p className="text-sm text-[var(--theme-text-secondary)] mb-6">
                            Algo deu errado. O sistema detectou uma falha inesperada.
                        </p>

                        {this.state.error && (
                            <div className="bg-black/40 rounded-lg p-4 mb-6 text-left">
                                <code className="text-xs text-red-400 font-mono break-all">
                                    {this.state.error.message}
                                </code>
                            </div>
                        )}

                        <button
                            onClick={this.handleRetry}
                            className="w-full px-6 py-3 bg-[var(--theme-primary)] hover:bg-[var(--theme-primary)]/80
                         text-white font-medium rounded-lg transition-colors"
                        >
                            Tentar Novamente
                        </button>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}
