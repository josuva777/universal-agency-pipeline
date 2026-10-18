import React, { useMemo } from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';

interface Particle {
  x: number;
  y: number;
  size: number;
  speedY: number;
  opacity: number;
}

export const ParticleVFX: React.FC<{ count?: number; accentColor?: string }> = ({
  count = 50,
  accentColor = 'rgba(99, 102, 241,',
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const particles: Particle[] = useMemo(() => {
    return Array.from({ length: count }).map((_, i) => ({
      x: ((i * 137.5) % width),
      y: ((i * 89.3) % height),
      size: 2.0 + (i % 3) * 1.5,
      speedY: 0.4 + (i % 5) * 0.3,
      opacity: 0.3 + (i % 4) * 0.18,
    }));
  }, [count, width, height]);

  return (
    <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', overflow: 'hidden' }}>
      {particles.map((p, idx) => {
        const currentY = (p.y - frame * p.speedY + height) % height;
        const currentX = p.x + Math.sin((frame + idx * 15) * 0.03) * 25;

        return (
          <div
            key={idx}
            style={{
              position: 'absolute',
              left: currentX,
              top: currentY,
              width: p.size,
              height: p.size,
              borderRadius: '50%',
              backgroundColor: `${accentColor} ${p.opacity})`,
              boxShadow: `0 0 ${p.size * 4}px ${accentColor} 0.8)`,
            }}
          />
        );
      })}
    </div>
  );
};
