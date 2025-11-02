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
    opacity: number;
    cosRotation: number;
    sinRotation: number;
}

interface ConfettiProps {
    active: boolean;
}

const Confetti: React.FC<ConfettiProps> = ({ active }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const animationRef = useRef<number | null>(null);
    const particlesRef = useRef<ConfettiParticle[]>([]);
    const frameCountRef = useRef<number>(0);

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
            const count = 300; // 紙吹雪の数
            for (let i = 0; i < count; i++) {
                // 画面の上部全体に分散して配置
                const x = Math.random() * canvas.width;
                const y = - Math.random() * 300; // 画面上部の少し上から開始

                // 下向きの速度を基本とし、少し左右にばらつきを加える
                const vy = Math.random() * 2 + 1; // 下向きの初速度（軽め）

                const rotation = Math.random() * 2 * Math.PI;

                particlesRef.current.push({
                    x,
                    y,
                    vy,
                    size: Math.random() * 8 + 4,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    rotation,
                    rotationSpeed: (Math.random() - 0.5) * 0.2,
                    opacity: 1,
                    cosRotation: Math.cos(rotation),
                    sinRotation: Math.sin(rotation)
                });
            }
        }

        function updateAndDraw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const particles = particlesRef.current;
            const frameCount = frameCountRef.current++;
            const maxLife = 240; // 約4秒（60fps換算）

            // 寿命チェック：すべてのパーティクルが同じ寿命なので一括判定
            if (frameCount >= maxLife) {
                particles.length = 0;
                ctx.globalAlpha = 1;
                return;
            }

            // 不透明度計算（残り寿命ベース） - 全パーティクル共通
            const remainingLife = maxLife - frameCount;
            const opacity = remainingLife > 120 ? 1 : remainingLife / 120;

            for (let i = 0; i < particles.length; i++) {
                const p = particles[i];

                // 物理演算
                p.y += p.vy;
                p.vy += 0.01; // 重力（少し弱めに）
                p.rotation += p.rotationSpeed;

                // 不透明度設定（全パーティクル共通値）
                p.opacity = opacity;

                // 三角関数を事前計算済みの値を更新
                p.cosRotation = Math.cos(p.rotation);
                p.sinRotation = Math.sin(p.rotation);

                // 描画（save/restoreを使わない高速な方法）
                const halfWidth = p.size / 4;
                const halfHeight = p.size / 2;

                // 回転した矩形の4つの角を計算
                const x1 = p.x + (-halfWidth * p.cosRotation - (-halfHeight) * p.sinRotation);
                const y1 = p.y + (-halfWidth * p.sinRotation + (-halfHeight) * p.cosRotation);
                const x2 = p.x + (halfWidth * p.cosRotation - (-halfHeight) * p.sinRotation);
                const y2 = p.y + (halfWidth * p.sinRotation + (-halfHeight) * p.cosRotation);
                const x3 = p.x + (halfWidth * p.cosRotation - halfHeight * p.sinRotation);
                const y3 = p.y + (halfWidth * p.sinRotation + halfHeight * p.cosRotation);
                const x4 = p.x + (-halfWidth * p.cosRotation - halfHeight * p.sinRotation);
                const y4 = p.y + (-halfWidth * p.sinRotation + halfHeight * p.cosRotation);

                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.opacity;
                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.lineTo(x3, y3);
                ctx.lineTo(x4, y4);
                ctx.closePath();
                ctx.fill();
            }

            if (particles.length > 0) {
                animationRef.current = requestAnimationFrame(updateAndDraw);
            } else {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.globalAlpha = 1; // アルファ値をリセット
            }
        }

        // activeが true になったときにconfettiを発射
        if (active) {
            frameCountRef.current = 0; // フレームカウンターをリセット
            launchConfetti();
        }

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
            frameCountRef.current = 0;
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