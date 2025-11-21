'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Terminal, Play, Clock, Trash2 } from 'lucide-react';
import { useToast } from '@/contexts/ToastProvider';

interface Command {
    id: string;
    agent: string;
    action: string;
    parameters: string;
    timestamp: Date;
    status: 'pending' | 'running' | 'completed' | 'failed';
}

export default function CommandCenterPage() {
    const { showToast } = useToast();
    const [commands, setCommands] = useState<Command[]>([]);
    const [selectedAgent, setSelectedAgent] = useState('');
    const [selectedAction, setSelectedAction] = useState('');
    const [parameters, setParameters] = useState('');

    const quickActions = [
        { icon: '🤖', label: 'Criar Agente', action: () => showToast('🤖 Wizard de criação de agente', 'info') },
        { icon: '📊', label: 'Gerar Relatório', action: () => showToast('📊 Gerando relatório...', 'success') },
        { icon: '⚡', label: 'Otimizar Sistema', action: () => showToast('⚡ Otimização iniciada!', 'success', '⚡') },
        { icon: '🔍', label: 'Análise Profunda', action: () => showToast('🔍 Análise em andamento', 'info', '🔍') },
    ];

    const executeCommand = () => {
        if (!selectedAgent || !selectedAction) {
            showToast('Selecione agente e ação', 'error');
            return;
        }

        const newCommand: Command = {
            id: Date.now().toString(),
            agent: selectedAgent,
            action: selectedAction,
            parameters,
            timestamp: new Date(),
            status: 'running'
        };

        setCommands(prev => [newCommand, ...prev]);
        showToast(`Comando executado: ${selectedAction}`, 'success', '🚀');

        // Simulate completion
        setTimeout(() => {
            setCommands(prev => prev.map(cmd =>
                cmd.id === newCommand.id ? { ...cmd, status: 'completed' } : cmd
            ));
        }, 2000);

        // Reset form
        setSelectedAgent('');
        setSelectedAction('');
        setParameters('');
    };

    return (
        <div className="min-h-screen p-6 md:p-8">
            {/* Header */}
            <div className="mb-8">
                <h1 className="font-orbitron text-4xl font-bold text-[var(--theme-text-primary)] mb-2 flex items-center gap-3">
                    <Terminal className="w-10 h-10" />
                    Command Center
                </h1>
                <p className="text-[var(--theme-text-secondary)]">
                    Interface de comando e controle de agentes
                </p>
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                {quickActions.map((action, index) => (
                    <motion.button
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.05 }}
                        onClick={action.action}
                        className="glass-card p-6 rounded-xl border border-[var(--theme-card-border)]
                       hover:border-[var(--theme-primary)] transition-all group"
                    >
                        <div className="text-4xl mb-2">{action.icon}</div>
                        <div className="text-sm font-medium text-[var(--theme-text-primary)]">
                            {action.label}
                        </div>
                    </motion.button>
                ))}
            </div>

            {/* Command Builder */}
            <div className="glass-card p-6 rounded-xl border border-[var(--theme-card-border)] mb-8">
                <h3 className="font-orbitron text-lg text-[var(--theme-text-primary)] mb-4">
                    Construtor de Comandos
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div>
                        <label className="block text-xs text-[var(--theme-text-secondary)] mb-2">
                            Agente Alvo
                        </label>
                        <select
                            value={selectedAgent}
                            onChange={(e) => setSelectedAgent(e.target.value)}
                            className="w-full bg-black/40 border border-[var(--theme-card-border)] rounded-lg px-4 py-2
                         text-[var(--theme-text-primary)] focus:border-[var(--theme-primary)] 
                         focus:outline-none"
                        >
                            <option value="">Selecione...</option>
                            <option value="ORCHESTRATOR ALPHA">ORCHESTRATOR ALPHA</option>
                            <option value="SECURITY GUARDIAN">SECURITY GUARDIAN</option>
                            <option value="DATA MINER">DATA MINER</option>
                            <option value="REVENUE HUNTER">REVENUE HUNTER</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-xs text-[var(--theme-text-secondary)] mb-2">
                            Ação
                        </label>
                        <select
                            value={selectedAction}
                            onChange={(e) => setSelectedAction(e.target.value)}
                            className="w-full bg-black/40 border border-[var(--theme-card-border)] rounded-lg px-4 py-2
                         text-[var(--theme-text-primary)] focus:border-[var(--theme-primary)] 
                         focus:outline-none"
                        >
                            <option value="">Selecione...</option>
                            <option value="Analyze">Analisar</option>
                            <option value="Execute">Executar</option>
                            <option value="Monitor">Monitorar</option>
                            <option value="Optimize">Otimizar</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-xs text-[var(--theme-text-secondary)] mb-2">
                            Parâmetros
                        </label>
                        <input
                            type="text"
                            value={parameters}
                            onChange={(e) => setParameters(e.target.value)}
                            placeholder="JSON ou texto..."
                            className="w-full bg-black/40 border border-[var(--theme-card-border)] rounded-lg px-4 py-2
                         text-[var(--theme-text-primary)] focus:border-[var(--theme-primary)] 
                         focus:outline-none placeholder:text-gray-600"
                        />
                    </div>
                </div>

                <button
                    onClick={executeCommand}
                    className="w-full md:w-auto px-6 py-3 bg-[var(--theme-primary)] hover:bg-[var(--theme-primary)]/80
                     text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                    <Play className="w-4 h-4" />
                    Executar Comando
                </button>
            </div>

            {/* Command History */}
            <div className="glass-card p-6 rounded-xl border border-[var(--theme-card-border)]">
                <h3 className="font-orbitron text-lg text-[var(--theme-text-primary)] mb-4">
                    Histórico de Comandos
                </h3>

                {commands.length === 0 ? (
                    <p className="text-sm text-[var(--theme-text-secondary)] text-center py-8">
                        Nenhum comando executado ainda
                    </p>
                ) : (
                    <div className="space-y-3">
                        {commands.map((cmd) => (
                            <motion.div
                                key={cmd.id}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="flex items-center justify-between p-4 bg-black/20 rounded-lg border border-[var(--theme-card-border)]"
                            >
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <span className="font-medium text-sm text-[var(--theme-text-primary)]">
                                            {cmd.agent} → {cmd.action}
                                        </span>
                                        <span className={`text-xs px-2 py-0.5 rounded-full ${cmd.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                                                cmd.status === 'running' ? 'bg-blue-500/20 text-blue-400 animate-pulse' :
                                                    cmd.status === 'failed' ? 'bg-red-500/20 text-red-400' :
                                                        'bg-gray-500/20 text-gray-400'
                                            }`}>
                                            {cmd.status}
                                        </span>
                                    </div>
                                    <p className="text-xs text-[var(--theme-text-secondary)]">
                                        {cmd.parameters || 'Sem parâmetros'}
                                    </p>
                                </div>

                                <div className="flex items-center gap-2">
                                    <span className="text-xs text-[var(--theme-text-secondary)] flex items-center gap-1">
                                        <Clock className="w-3 h-3" />
                                        {cmd.timestamp.toLocaleTimeString()}
                                    </span>
                                    <button className="p-2 hover:bg-red-500/20 rounded transition-colors">
                                        <Trash2 className="w-4 h-4 text-red-400" />
                                    </button>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
