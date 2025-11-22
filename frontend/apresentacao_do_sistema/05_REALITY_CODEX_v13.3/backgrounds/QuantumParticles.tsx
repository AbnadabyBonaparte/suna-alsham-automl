"use client";

import { useEffect, useRef } from "react";
import { useTheme } from "@/contexts/ThemeContext";

/**
 * Quantum Lab Background - Interactive Particle Mesh
 * Based on Códice Visual Oficial - REALIDADE 1
 */
export default function QuantumParticles() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const { theme } = useTheme();

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        let animationFrameId: number;
        let particles: Particle[] = [];
        let mouse = { x: 0, y: 0 };

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };

        window.addEventListener("resize", resize);
        resize();

        class Particle {
            x: number;
            y: number;
            size: number;
            speedX: number;
            speedY: number;
            opacity: number;
            baseX: number;
            baseY: number;

            constructor(x: number, y: number) {
                this.x = x;
                this.y = y;
                this.baseX = x;
                this.baseY = y;
                this.size = Math.random() * 3 + 1;
                this.speedX = (Math.random() - 0.5) * 0.3;
                this.speedY = (Math.random() - 0.5) * 0.3;
                this.opacity = Math.random() * 0.6 + 0.2;
            }

            update() {
                // Gentle floating movement
                this.x += this.speedX;
                this.y += this.speedY;

                // Pull back to base position
                const dx = this.baseX - this.x;
                const dy = this.baseY - this.y;
                this.x += dx * 0.01;
                this.y += dy * 0.01;

                // Mouse interaction
                const distX = mouse.x - this.x;
                const distY = mouse.y - this.y;
                const distance = Math.sqrt(distX * distX + distY * distY);

                if (distance < 150) {
                    const force = (150 - distance) / 150;
                    this.x -= distX * force * 0.03;
                    this.y -= distY * force * 0.03;
                }

                // Wrap around edges
                if (this.x > canvas!.width) this.baseX = this.x = 0;
                if (this.x < 0) this.baseX = this.x = canvas!.width;
                if (this.y > canvas!.height) this.baseY = this.y = 0;
                if (this.y < 0) this.baseY = this.y = canvas!.height;
            }

            draw() {
                if (!ctx) return;
                ctx.fillStyle = `rgba(0, 255, 200, ${this.opacity})`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        const init = () => {
            particles = [];
            const particleCount = Math.floor((canvas.width * canvas.height) / 15000);
            for (let i = 0; i < particleCount; i++) {
                const x = Math.random() * canvas.width;
                const y = Math.random() * canvas.height;
                particles.push(new Particle(x, y));
            }
        };

        const drawConnections = () => {
            if (!ctx) return;
            const maxDistance = 120;

            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);

                    if (distance < maxDistance) {
                        const opacity = (1 - distance / maxDistance) * 0.2;
                        ctx.strokeStyle = `rgba(0, 255, 200, ${opacity})`;
                        ctx.lineWidth = 0.5;
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
        };

        const animate = () => {
            if (!ctx) return;

            // Gradient background
            const gradient = ctx.createRadialGradient(
                canvas.width / 2,
                canvas.height / 2,
                0,
                canvas.width / 2,
                canvas.height / 2,
                canvas.width / 2
            );
            gradient.addColorStop(0, '#000000');
            gradient.addColorStop(1, '#051015');

            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            drawConnections();

            particles.forEach((particle) => {
                particle.update();
                particle.draw();
            });

            animationFrameId = requestAnimationFrame(animate);
        };

        const handleMouseMove = (e: MouseEvent) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        };

        window.addEventListener('mousemove', handleMouseMove);

        init();
        animate();

        return () => {
            window.removeEventListener("resize", resize);
            window.removeEventListener('mousemove', handleMouseMove);
            cancelAnimationFrame(animationFrameId);
        };
    }, [theme]);

    return (
        <canvas
            ref={canvasRef}
            className="fixed inset-0 z-0 pointer-events-none"
        />
    );
}
