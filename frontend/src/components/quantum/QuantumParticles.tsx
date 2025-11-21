"use client";

import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { useTheme } from '@/contexts/ThemeProvider';

export default function QuantumParticles() {
    const containerRef = useRef<HTMLDivElement>(null);
    const { theme } = useTheme();

    useEffect(() => {
        if (!containerRef.current) return;

        // Scene setup
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        camera.position.z = 400;

        const renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        containerRef.current.appendChild(renderer.domElement);

        // Particle system
        const particleCount = 3000;
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        const velocities = new Float32Array(particleCount * 3);

        // Define 4 core Quantum colors
        const colorPalette = [
            new THREE.Color(theme.primary),      // Quantum Purple
            new THREE.Color(theme.accent),       // Photon Gold
            new THREE.Color(theme.secondary),    // Secondary
            new THREE.Color(theme.particles)     // Particle color
        ];

        // Initialize particles
        for (let i = 0; i < particleCount; i++) {
            const i3 = i * 3;

            // Random positions in 3D space
            positions[i3] = (Math.random() - 0.5) * 1000;
            positions[i3 + 1] = (Math.random() - 0.5) * 1000;
            positions[i3 + 2] = (Math.random() - 0.5) * 500;

            // Random velocities
            velocities[i3] = (Math.random() - 0.5) * 0.2;
            velocities[i3 + 1] = (Math.random() - 0.5) * 0.2;
            velocities[i3 + 2] = (Math.random() - 0.5) * 0.1;

            // Assign random color from palette
            const color = colorPalette[Math.floor(Math.random() * colorPalette.length)];
            colors[i3] = color.r;
            colors[i3 + 1] = color.g;
            colors[i3 + 2] = color.b;
        }

        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 2.5, // <<< KEY: Large size makes them look like squares
            vertexColors: true,
            transparent: true,
            opacity: 0.9,
            blending: THREE.AdditiveBlending, // <<< KEY: Creates glow where particles overlap
            depthWrite: false
        });

        const particles = new THREE.Points(geometry, material);
        scene.add(particles);

        // Mouse interaction
        let mouseX = 0;
        let mouseY = 0;
        let scrollY = 0;

        const onMouseMove = (event: MouseEvent) => {
            mouseX = (event.clientX - window.innerWidth / 2) * 0.05;
            mouseY = (event.clientY - window.innerHeight / 2) * 0.05;
        };

        const onScroll = () => {
            scrollY = window.scrollY;
        };

        window.addEventListener('mousemove', onMouseMove);
        window.addEventListener('scroll', onScroll);

        // Animation loop
        let time = 0;
        const animate = () => {
            requestAnimationFrame(animate);
            time += 0.01;

            const positions = particles.geometry.attributes.position.array as Float32Array;

            // Continuous rotation
            particles.rotation.x += 0.0002;
            particles.rotation.y += 0.0004;

            // Parallax effect on scroll
            particles.position.y = scrollY * -0.5;

            // Mouse influence
            particles.rotation.x += (mouseY - particles.rotation.x) * 0.0001;
            particles.rotation.y += (mouseX - particles.rotation.y) * 0.0001;

            // Organic movement (Math.sin based)
            for (let i = 0; i < particleCount; i++) {
                const i3 = i * 3;

                // Add organic sinusoidal movement
                positions[i3] += Math.sin(time * 0.7 + i * 0.01) * 0.1;
                positions[i3 + 1] += Math.cos(time * 0.5 + i * 0.02) * 0.1;

                // Apply velocities
                positions[i3] += velocities[i3];
                positions[i3 + 1] += velocities[i3 + 1];
                positions[i3 + 2] += velocities[i3 + 2];

                // Reset particles that go out of bounds
                if (Math.abs(positions[i3]) > 500) {
                    positions[i3] = (Math.random() - 0.5) * 1000;
                }
                if (Math.abs(positions[i3 + 1]) > 500) {
                    positions[i3 + 1] = (Math.random() - 0.5) * 1000;
                }
                if (Math.abs(positions[i3 + 2]) > 250) {
                    positions[i3 + 2] = (Math.random() - 0.5) * 500;
                }
            }

            particles.geometry.attributes.position.needsUpdate = true;
            renderer.render(scene, camera);
        };

        animate();

        // Handle window resize
        const onResize = () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        };

        window.addEventListener('resize', onResize);

        // Cleanup
        return () => {
            window.removeEventListener('mousemove', onMouseMove);
            window.removeEventListener('scroll', onScroll);
            window.removeEventListener('resize', onResize);

            if (containerRef.current && renderer.domElement.parentNode) {
                containerRef.current.removeChild(renderer.domElement);
            }

            geometry.dispose();
            material.dispose();
            renderer.dispose();
        };
    }, [theme]); // Re-create particles when theme changes

    return (
        <div
            ref={containerRef}
            className="fixed inset-0 pointer-events-none"
            style={{ zIndex: 1 }}
        />
    );
}
