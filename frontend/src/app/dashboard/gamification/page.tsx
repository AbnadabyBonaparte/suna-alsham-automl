"use client";

import { useState, useEffect } from 'react';
import { 
    Trophy, 
    Star,
    Medal,
    Crown,
    Flame,
    Target,
    Zap,
    Award,
    TrendingUp,
    Users,
    Gift,
    Lock,
    Unlock,
    ChevronRight,
    Sparkles,
    Shield,
    Swords,
    Heart
} from 'lucide-react';

interface Achievement {
    id: string;
    name: string;
    description: string;
    icon: any;
    unlocked: boolean;
    progress: number;
    maxProgress: number;
    rarity: 'common' | 'rare' | 'epic' | 'legendary';
    xp: number;
}

interface LeaderboardEntry {
    rank: number;
    name: string;
    avatar: string;
    xp: number;
    level: number;
    streak: number;
}

export default function GamificationPage() {
    const [activeTab, setActiveTab] = useState<'achievements' | 'leaderboard' | 'rewards'>('achievements');
    const [userStats, setUserStats] = useState({
        xp: 12450,
        level: 24,
        nextLevelXp: 15000,
        streak: 7,
        rank: 3,
        totalAchievements: 18,
        unlockedAchievements: 12
    });

    const achievements: Achievement[] = [
        { id: '1', name: 'Primeiro Contato', description: 'Complete seu primeiro lead', icon: Zap, unlocked: true, progress: 1, maxProgress: 1, rarity: 'common', xp: 100 },
        { id: '2', name: 'Conversor', description: 'Converta 10 leads em clientes', icon: Target, unlocked: true, progress: 10, maxProgress: 10, rarity: 'common', xp: 250 },
        { id: '3', name: 'Streak Master', description: 'Mantenha 7 dias de streak', icon: Flame, unlocked: true, progress: 7, maxProgress: 7, rarity: 'rare', xp: 500 },
        { id: '4', name: 'Top Performer', description: 'Fique em 1º no ranking semanal', icon: Crown, unlocked: false, progress: 0, maxProgress: 1, rarity: 'epic', xp: 1000 },
        { id: '5', name: 'Mestre Quântico', description: 'Alcance o nível 50', icon: Sparkles, unlocked: false, progress: 24, maxProgress: 50, rarity: 'legendary', xp: 2500 },
        { id: '6', name: 'Caçador de Leads', description: 'Processe 100 leads', icon: Swords, unlocked: true, progress: 100, maxProgress: 100, rarity: 'rare', xp: 500 },
        { id: '7', name: 'Eficiência Máxima', description: 'Atinja 95% de eficiência', icon: Shield, unlocked: false, progress: 89, maxProgress: 95, rarity: 'epic', xp: 1000 },
        { id: '8', name: 'Networker', description: 'Conecte com 50 empresas', icon: Users, unlocked: true, progress: 50, maxProgress: 50, rarity: 'rare', xp: 500 },
    ];

    const leaderboard: LeaderboardEntry[] = [
        { rank: 1, name: 'UNIT_24', avatar: 'U', xp: 18500, level: 32, streak: 14 },
        { rank: 2, name: 'UNIT_29', avatar: 'U', xp: 16200, level: 28, streak: 9 },
        { rank: 3, name: 'Você', avatar: 'V', xp: 12450, level: 24, streak: 7 },
        { rank: 4, name: 'UNIT_25', avatar: 'U', xp: 11800, level: 23, streak: 5 },
        { rank: 5, name: 'UNIT_26', avatar: 'U', xp: 10500, level: 21, streak: 3 },
        { rank: 6, name: 'UNIT_28', avatar: 'U', xp: 9800, level: 20, streak: 2 },
        { rank: 7, name: 'UNIT_27', avatar: 'U', xp: 8900, level: 18, streak: 1 },
    ];

    const rewards = [
        { id: '1', name: 'Tema Exclusivo: Neural Dawn', cost: 5000, unlocked: true, type: 'theme' },
        { id: '2', name: 'Badge: Elite Operator', cost: 7500, unlocked: true, type: 'badge' },
        { id: '3', name: 'Turbo Mode Unlock', cost: 10000, unlocked: false, type: 'feature' },
        { id: '4', name: 'Tema Legendário: Void Protocol', cost: 15000, unlocked: false, type: 'theme' },
        { id: '5', name: 'API Priority Access', cost: 20000, unlocked: false, type: 'feature' },
    ];

    const getRarityColor = (rarity: string) => {
        switch (rarity) {
            case 'common': return 'from-zinc-400 to-zinc-500 border-zinc-500/30';
            case 'rare': return 'from-blue-400 to-cyan-500 border-blue-500/30';
            case 'epic': return 'from-purple-400 to-pink-500 border-purple-500/30';
            case 'legendary': return 'from-yellow-400 to-orange-500 border-yellow-500/30';
            default: return 'from-zinc-400 to-zinc-500 border-zinc-500/30';
        }
    };

    const getRarityLabel = (rarity: string) => {
        switch (rarity) {
            case 'common': return 'Comum';
            case 'rare': return 'Raro';
            case 'epic': return 'Épico';
            case 'legendary': return 'Lendário';
            default: return rarity;
        }
    };

    const getRankIcon = (rank: number) => {
        switch (rank) {
            case 1: return <Crown className="w-5 h-5 text-yellow-400" />;
            case 2: return <Medal className="w-5 h-5 text-zinc-300" />;
            case 3: return <Medal className="w-5 h-5 text-orange-400" />;
            default: return <span className="text-zinc-500 font-bold">{rank}</span>;
        }
    };

    const xpProgress = ((userStats.xp / userStats.nextLevelXp) * 100).toFixed(0);

    return (
        <div className="min-h-screen p-6 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-gradient-to-br from-yellow-500/20 to-orange-500/20 rounded-xl border border-yellow-500/30">
                        <Trophy className="w-8 h-8 text-yellow-400" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold text-white tracking-tight">
                            Gamification
                        </h1>
                        <p className="text-zinc-400">Achievements, Ranks & Rewards</p>
                    </div>
                </div>
            </div>

            {/* User Stats Card */}
            <div className="bg-gradient-to-r from-purple-900/30 via-zinc-900/50 to-cyan-900/30 border border-zinc-800 rounded-2xl p-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    {/* Level & XP */}
                    <div className="md:col-span-2">
                        <div className="flex items-center gap-4 mb-4">
                            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                                {userStats.level}
                            </div>
                            <div>
                                <p className="text-white font-semibold text-lg">Nível {userStats.level}</p>
                                <p className="text-zinc-400 text-sm">Quantum Operator</p>
                            </div>
                        </div>
                        <div className="space-y-2">
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-zinc-400">XP Progress</span>
                                <span className="text-white">{userStats.xp.toLocaleString()} / {userStats.nextLevelXp.toLocaleString()}</span>
                            </div>
                            <div className="h-3 bg-zinc-800 rounded-full overflow-hidden">
                                <div 
                                    className="h-full bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full transition-all duration-500"
                                    style={{ width: `${xpProgress}%` }}
                                />
                            </div>
                            <p className="text-xs text-zinc-500">{userStats.nextLevelXp - userStats.xp} XP para o próximo nível</p>
                        </div>
                    </div>

                    {/* Stats */}
                    <div className="flex flex-col justify-center items-center p-4 bg-black/30 rounded-xl">
                        <Flame className="w-8 h-8 text-orange-400 mb-2" />
                        <p className="text-2xl font-bold text-white">{userStats.streak} dias</p>
                        <p className="text-sm text-zinc-500">Streak Atual</p>
                    </div>
                    <div className="flex flex-col justify-center items-center p-4 bg-black/30 rounded-xl">
                        <Award className="w-8 h-8 text-cyan-400 mb-2" />
                        <p className="text-2xl font-bold text-white">{userStats.unlockedAchievements}/{userStats.totalAchievements}</p>
                        <p className="text-sm text-zinc-500">Conquistas</p>
                    </div>
                </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 bg-zinc-900/50 border border-zinc-800 rounded-xl p-1 w-fit">
                {[
                    { id: 'achievements', label: 'Conquistas', icon: Award },
                    { id: 'leaderboard', label: 'Ranking', icon: Trophy },
                    { id: 'rewards', label: 'Recompensas', icon: Gift },
                ].map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id as any)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                            activeTab === tab.id
                                ? 'bg-cyan-500/20 text-cyan-400'
                                : 'text-zinc-400 hover:text-white'
                        }`}
                    >
                        <tab.icon className="w-4 h-4" />
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Content */}
            {activeTab === 'achievements' && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {achievements.map((achievement) => (
                        <div
                            key={achievement.id}
                            className={`relative bg-zinc-900/50 border rounded-xl p-5 transition-all hover:scale-[1.02] ${
                                achievement.unlocked 
                                    ? `bg-gradient-to-br ${getRarityColor(achievement.rarity)}` 
                                    : 'border-zinc-800 opacity-60'
                            }`}
                        >
                            <div className="flex items-start justify-between mb-3">
                                <div className={`p-3 rounded-xl ${
                                    achievement.unlocked 
                                        ? `bg-gradient-to-br ${getRarityColor(achievement.rarity)}`
                                        : 'bg-zinc-800'
                                }`}>
                                    <achievement.icon className={`w-6 h-6 ${
                                        achievement.unlocked ? 'text-white' : 'text-zinc-500'
                                    }`} />
                                </div>
                                <div className="flex items-center gap-2">
                                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                                        achievement.rarity === 'legendary' ? 'bg-yellow-500/20 text-yellow-400' :
                                        achievement.rarity === 'epic' ? 'bg-purple-500/20 text-purple-400' :
                                        achievement.rarity === 'rare' ? 'bg-blue-500/20 text-blue-400' :
                                        'bg-zinc-500/20 text-zinc-400'
                                    }`}>
                                        {getRarityLabel(achievement.rarity)}
                                    </span>
                                    {achievement.unlocked ? (
                                        <Unlock className="w-4 h-4 text-green-400" />
                                    ) : (
                                        <Lock className="w-4 h-4 text-zinc-500" />
                                    )}
                                </div>
                            </div>
                            <h3 className="text-white font-semibold mb-1">{achievement.name}</h3>
                            <p className="text-sm text-zinc-400 mb-3">{achievement.description}</p>
                            
                            {/* Progress Bar */}
                            <div className="space-y-1">
                                <div className="flex items-center justify-between text-xs">
                                    <span className="text-zinc-500">Progresso</span>
                                    <span className="text-white">{achievement.progress}/{achievement.maxProgress}</span>
                                </div>
                                <div className="h-2 bg-black/50 rounded-full overflow-hidden">
                                    <div 
                                        className={`h-full rounded-full ${
                                            achievement.unlocked ? 'bg-green-500' : 'bg-zinc-600'
                                        }`}
                                        style={{ width: `${(achievement.progress / achievement.maxProgress) * 100}%` }}
                                    />
                                </div>
                            </div>

                            {/* XP Reward */}
                            <div className="flex items-center gap-1 mt-3 text-sm">
                                <Star className="w-4 h-4 text-yellow-400" />
                                <span className="text-yellow-400">+{achievement.xp} XP</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {activeTab === 'leaderboard' && (
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
                    <div className="space-y-3">
                        {leaderboard.map((entry) => (
                            <div
                                key={entry.rank}
                                className={`flex items-center justify-between p-4 rounded-xl transition-colors ${
                                    entry.name === 'Você' 
                                        ? 'bg-cyan-500/10 border border-cyan-500/30' 
                                        : 'bg-black/30 border border-zinc-800 hover:bg-zinc-800/50'
                                }`}
                            >
                                <div className="flex items-center gap-4">
                                    <div className="w-10 h-10 flex items-center justify-center">
                                        {getRankIcon(entry.rank)}
                                    </div>
                                    <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white font-bold">
                                        {entry.avatar}
                                    </div>
                                    <div>
                                        <p className={`font-semibold ${entry.name === 'Você' ? 'text-cyan-400' : 'text-white'}`}>
                                            {entry.name}
                                        </p>
                                        <p className="text-sm text-zinc-500">Nível {entry.level}</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-6">
                                    <div className="text-center">
                                        <div className="flex items-center gap-1">
                                            <Flame className="w-4 h-4 text-orange-400" />
                                            <span className="text-white">{entry.streak}</span>
                                        </div>
                                        <p className="text-xs text-zinc-500">Streak</p>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-white font-semibold">{entry.xp.toLocaleString()}</p>
                                        <p className="text-xs text-zinc-500">XP Total</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {activeTab === 'rewards' && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {rewards.map((reward) => (
                        <div
                            key={reward.id}
                            className={`bg-zinc-900/50 border rounded-xl p-5 ${
                                reward.unlocked ? 'border-green-500/30' : 'border-zinc-800'
                            }`}
                        >
                            <div className="flex items-start justify-between mb-4">
                                <div className={`p-3 rounded-xl ${
                                    reward.type === 'theme' ? 'bg-purple-500/20' :
                                    reward.type === 'badge' ? 'bg-yellow-500/20' :
                                    'bg-cyan-500/20'
                                }`}>
                                    {reward.type === 'theme' ? <Sparkles className="w-6 h-6 text-purple-400" /> :
                                     reward.type === 'badge' ? <Award className="w-6 h-6 text-yellow-400" /> :
                                     <Zap className="w-6 h-6 text-cyan-400" />}
                                </div>
                                {reward.unlocked && (
                                    <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs">
                                        Desbloqueado
                                    </span>
                                )}
                            </div>
                            <h3 className="text-white font-semibold mb-2">{reward.name}</h3>
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-1">
                                    <Star className="w-4 h-4 text-yellow-400" />
                                    <span className="text-yellow-400">{reward.cost.toLocaleString()} XP</span>
                                </div>
                                {!reward.unlocked && (
                                    <button 
                                        disabled={userStats.xp < reward.cost}
                                        className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                                            userStats.xp >= reward.cost
                                                ? 'bg-cyan-500 text-black hover:bg-cyan-400'
                                                : 'bg-zinc-800 text-zinc-500 cursor-not-allowed'
                                        }`}
                                    >
                                        Resgatar
                                    </button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
