'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { supabase } from '@/lib/supabase';

interface GamificationContextType {
    points: number;
    level: number;
    badges: string[];
    streak: number;
    addPoints: (amount: number, reason: string) => void;
    unlockBadge: (badgeId: string) => void;
}

const GamificationContext = createContext<GamificationContextType | undefined>(undefined);

const POINTS_PER_LEVEL = 1000;

export const BADGES = {
    iniciante: { id: 'iniciante', name: 'Iniciante', icon: '🥇', requirement: 'Completou 10 tarefas' },
    streakMaster: { id: 'streakMaster', name: 'Streak Master', icon: '🔥', requirement: '7 dias consecutivos' },
    powerUser: { id: 'powerUser', name: 'Power User', icon: '🚀', requirement: '100 agentes ativados' },
    aiWhisperer: { id: 'aiWhisperer', name: 'AI Whisperer', icon: '🧠', requirement: '50 comandos ORION' },
    elite: { id: 'elite', name: 'Elite', icon: '💎', requirement: 'Top 5% dos usuários' },
};

export function GamificationProvider({ children }: { children: ReactNode }) {
    const [points, setPoints] = useState(0);
    const [level, setLevel] = useState(1);
    const [badges, setBadges] = useState<string[]>([]);
    const [streak, setStreak] = useState(0);

    // Load from localStorage
    useEffect(() => {
        const saved = localStorage.getItem('gamification');
        if (saved) {
            const data = JSON.parse(saved);
            setPoints(data.points || 0);
            setLevel(data.level || 1);
            setBadges(data.badges || []);
            setStreak(data.streak || 0);
        }
    }, []);

    // Save to localStorage
    useEffect(() => {
        localStorage.setItem('gamification', JSON.stringify({ points, level, badges, streak }));
    }, [points, level, badges, streak]);

    // Calculate level
    useEffect(() => {
        const newLevel = Math.floor(points / POINTS_PER_LEVEL) + 1;
        setLevel(newLevel);
    }, [points]);

    const addPoints = (amount: number, reason: string) => {
        setPoints(prev => prev + amount);

        // Show notification (will implement in Area 10)
        console.log(`+${amount} XP - ${reason}`);
    };

    const unlockBadge = (badgeId: string) => {
        if (!badges.includes(badgeId)) {
            setBadges(prev => [...prev, badgeId]);

            // Show confetti (will implement in Area 10)
            console.log(`🎉 Badge desbloqueado: ${BADGES[badgeId as keyof typeof BADGES]?.name}`);
        }
    };

    return (
        <GamificationContext.Provider value={{ points, level, badges, streak, addPoints, unlockBadge }}>
            {children}
        </GamificationContext.Provider>
    );
}

export function useGamification() {
    const context = useContext(GamificationContext);
    if (!context) throw new Error('useGamification must be used within GamificationProvider');
    return context;
}
