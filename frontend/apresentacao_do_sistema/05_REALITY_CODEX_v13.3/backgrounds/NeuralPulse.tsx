"use client";

import { useEffect, useRef } from "react";

/**
 * Neural Singularity Background - Pulsing Neural Network (60bpm)
 * Based on Códice Visual Oficial - REALIDADE 3
 */
export default function NeuralPulse() {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        let animationFrameId: number;
        let nodes: Node[] = [];
        let pulsePhase = 0;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };

        window.addEventListener("resize", resize);
        resize();

        class Node {
            x: number;
            y: number;
            baseSize: number;
            connections: Node[];
            pulseOffset: number;

            constructor(x: number, y: number) {
                this.x = x;
                this.y = y;
                this.baseSize = Math.random() * 4 + 2;
                this.connections = [];
                this.pulseOffset = Math.random() * Math.PI * 2;
            }

            getPulseSize() {
                // 60 BPM = 1 Hz = 1 pulse per second
                const bpm = 60;
                const frequency = bpm / 60;
                const pulse = Math.sin(pulsePhase * frequency * Math.PI * 2 + this.pulseOffset);
                return this.baseSize * (1 + pulse * 0.3);
            }

            draw() {
                if (!ctx) return;
                const size = this.getPulseSize();
                const opacity = 0.6 + Math.sin(pulsePhase * 2 + this.pulseOffset) * 0.2;

                // Bioluminescent glow
                const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, size * 3);
                gradient.addColorStop(0, `rgba(208, 34, 255, ${opacity})`);
                gradient.addColorStop(0.5, `rgba(208, 34, 255, ${opacity * 0.3})`);
                gradient.addColorStop(1, 'rgba(208, 34, 255, 0)');

                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(this.x, this.y, size * 3, 0, Math.PI * 2);
                ctx.fill();

                // Core
                ctx.fillStyle = `rgba(208, 34, 255, ${opacity})`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, size, 0, Math.PI * 2);
                ctx.fill();
            }

            drawConnections() {
                if (!ctx) return;
                this.connections.forEach(node => {
                    const dx = node.x - this.x;
                    const dy = node.y - this.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    const opacity = (1 - distance / 300) * 0.15;

                    if (opacity > 0) {
                        // Synapse firing effect
                        const pulse = Math.sin(pulsePhase * 3 + this.pulseOffset);
                        const lineOpacity = opacity * (0.5 + pulse * 0.5);

                        const gradient = ctx.createLinearGradient(this.x, this.y, node.x, node.y);
                        gradient.addColorStop(0, `rgba(208, 34, 255, ${lineOpacity})`);
                        gradient.addColorStop(0.5, `rgba(34, 204, 255, ${lineOpacity})`);
                        gradient.addColorStop(1, `rgba(208, 34, 255, ${lineOpacity})`);

                        ctx.strokeStyle = gradient;
                        ctx.lineWidth = 1.5;
                        ctx.beginPath();
                        ctx.moveTo(this.x, this.y);
                        ctx.lineTo(node.x, node.y);
                        ctx.stroke();
                    }
                });
            }
        }

        const init = () => {
            nodes = [];
            const nodeCount = 30;

            for (let i = 0; i < nodeCount; i++) {
                const x = Math.random() * canvas.width;
                const y = Math.random() * canvas.height;
                nodes.push(new Node(x, y));
            }

            // Create organic connections
            nodes.forEach(node => {
                const nearbyNodes = nodes
                    .filter(n => n !== node)
                    .filter(n => {
                        const dx = n.x - node.x;
                        const dy = n.y - node.y;
                        return Math.sqrt(dx * dx + dy * dy) < 300;
                    })
                    .slice(0, 3);

                node.connections = nearbyNodes;
            });
        };

        const animate = () => {
            if (!ctx) return;

            // Deep purple void background
            ctx.fillStyle = '#050008';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Update pulse phase (60 BPM)
            pulsePhase += 0.016; // ~60 FPS

            // Draw connections first
            nodes.forEach(node => node.drawConnections());

            // Draw nodes over connections
            nodes.forEach(node => node.draw());

            animationFrameId = requestAnimationFrame(animate);
        };

        init();
        animate();

        return () => {
            window.removeEventListener("resize", resize);
            cancelAnimationFrame(animationFrameId);
        };
    }, []);

    return (
        <canvas
            ref={canvasRef}
            className="fixed inset-0 z-0 pointer-events-none"
        />
    );
}
