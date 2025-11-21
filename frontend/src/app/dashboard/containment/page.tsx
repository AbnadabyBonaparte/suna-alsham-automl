"use client";

import { useEffect, useState } from "react";
import { useSfx } from "@/hooks/use-sfx";
import { AlertTriangle, Lock, ShieldAlert } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

export default function ContainmentPage() {
    const { play } = useSfx();
    const router = useRouter();
    const [countdown, setCountdown] = useState(60);

    useEffect(() => {
        // Play alarm immediately and loop
        play("alert");
        const alarmInterval = setInterval(() => {
            play("alert");
        }, 2000);

        // Countdown timer
        const timer = setInterval(() => {
            setCountdown((prev) => (prev > 0 ? prev - 1 : 0));
        }, 1000);

        return () => {
            clearInterval(alarmInterval);
            clearInterval(timer);
        };
    }, [play]);

    const handleOverride = () => {
        play("click");
        // Logic to unlock (maybe require a password in v2)
        router.push("/dashboard");
    };

    return (
        <div className="fixed inset-0 z-[9999] bg-red-950 flex flex-col items-center justify-center text-red-500 overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-20 mix-blend-overlay" />
            <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black/50" />
            <div className="absolute inset-0 animate-pulse bg-red-900/20" />

            {/* Main Content */}
            <div className="relative z-10 text-center space-y-8 max-w-4xl p-8 border-4 border-red-600/50 bg-black/80 backdrop-blur-xl rounded-3xl shadow-[0_0_100px_rgba(220,38,38,0.5)]">

                <div className="flex justify-center mb-8">
                    <ShieldAlert className="w-32 h-32 text-red-500 animate-bounce" />
                </div>

                <h1 className="text-7xl md:text-9xl font-black tracking-tighter drop-shadow-[0_0_30px_rgba(220,38,38,0.8)]">
                    CONTAINMENT
                </h1>

                <div className="space-y-4">
                    <p className="text-3xl font-mono tracking-widest text-red-200">
                        PROTOCOL 66 ACTIVATED
                    </p>
                    <p className="text-xl text-red-400/80">
                        ALL NEURAL NODES FROZEN • NETWORK ISOLATED
                    </p>
                </div>

                <div className="py-8">
                    <div className="text-6xl font-mono font-bold text-white">
                        00:00:{countdown.toString().padStart(2, '0')}
                    </div>
                    <p className="text-xs text-red-500 mt-2 uppercase tracking-widest">Auto-Purge Sequence Initiated</p>
                </div>

                <div className="pt-8 border-t border-red-900/50">
                    <Button
                        onClick={handleOverride}
                        variant="destructive"
                        size="lg"
                        className="bg-red-600 hover:bg-red-700 text-white font-bold text-xl px-12 py-8 h-auto border-2 border-white/20 shadow-[0_0_30px_rgba(220,38,38,0.4)] hover:shadow-[0_0_50px_rgba(220,38,38,0.6)] transition-all"
                    >
                        <Lock className="w-6 h-6 mr-3" />
                        OVERRIDE PROTOCOL
                    </Button>
                </div>
            </div>

            {/* Scrolling Warning Tape */}
            <div className="absolute bottom-10 left-0 right-0 bg-yellow-500/20 overflow-hidden py-2 rotate-1">
                <div className="whitespace-nowrap animate-marquee text-yellow-500 font-black text-2xl tracking-widest">
                    WARNING • BIOHAZARD DETECTED • DO NOT POWER OFF • SYSTEM UNSTABLE • WARNING • BIOHAZARD DETECTED • DO NOT POWER OFF • SYSTEM UNSTABLE •
                </div>
            </div>
        </div>
    );
}
