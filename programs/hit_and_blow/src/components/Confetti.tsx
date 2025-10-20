import React, { useEffect, useRef } from 'react';
import { Box } from '@chakra-ui/react';

interface ConfettiParticle {
    x: number;
    y: number;
    vy: number;
    size: number;
    color: string;
    rotation: number;
    rotationSpeed: number;
    life: number;
    opacity: number;
}

interface ConfettiProps {
    active: boolean;
}

const Confetti: React.FC<ConfettiProps> = ({ active }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const animationRef = useRef<number | null>(null);
    const particlesRef = useRef<ConfettiParticle[]>([]);

    useEffect(() => {
        if (!canvasRef.current) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d')!;

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        const colors = [
            '#FF0A47', '#FF6F00', '#FFD300',
            '#32CD32', '#1E90FF', '#8A2BE2', '#FF69B4'
        ];

        function launchConfetti() {
            const count = 100; // 紙吹雪の数
            for (let i = 0; i < count; i++) {
                // 画面の上部全体に分散して配置
                const x = Math.random() * canvas.width;
                const y = -50 - Math.random() * 50; // 画面上部の少し上から開始

                // 下向きの速度を基本とし、少し左右にばらつきを加える
                const vy = Math.random() * 2 + 1; // 下向きの初速度（軽め）

                particlesRef.current.push({
                    x,
                    y,
                    vy,
                    size: Math.random() * 8 + 4,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    rotation: Math.random() * 2 * Math.PI,
                    rotationSpeed: (Math.random() - 0.5) * 0.2,
                    life: 240, // 約4秒（60fps換算）- 少し長めに
                    opacity: 1
                });
            }
        }

        function updateAndDraw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            particlesRef.current.forEach(p => {
                p.y += p.vy;
                p.vy += 0.01; // 重力（少し弱めに）
                p.rotation += p.rotationSpeed;
                p.life--;
                p.opacity = Math.max(0, Math.min(1, p.life / 120));

                // 描画
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate(p.rotation);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.opacity;
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
                ctx.restore();
            });

            // 寿命の尽きたパーティクルを削除
            particlesRef.current = particlesRef.current.filter(p => p.life > 0);

            if (particlesRef.current.length > 0) {
                animationRef.current = requestAnimationFrame(updateAndDraw);
            } else {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
        }

        // activeが true になったときにconfettiを発射
        if (active) launchConfetti();

        updateAndDraw();

        return () => {
            if (animationRef.current) cancelAnimationFrame(animationRef.current);
            window.removeEventListener('resize', resizeCanvas);
        };
    }, [active]);

    // アクティブでない場合はアニメーションを停止
    useEffect(() => {
        if (!active && animationRef.current) {
            cancelAnimationFrame(animationRef.current);
            animationRef.current = null;
            particlesRef.current = [];
        }
    }, [active]);

    if (!active) return null;

    return (
        <Box
            position="fixed"
            top={0}
            left={0}
            width="100vw"
            height="100vh"
            pointerEvents="none"
            zIndex={9999}
        >
            <canvas
                ref={canvasRef}
                style={{
                    width: '100%',
                    height: '100%',
                }}
            />
        </Box>
    );
};

export default Confetti;