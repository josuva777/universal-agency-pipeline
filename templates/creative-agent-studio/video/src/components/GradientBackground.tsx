import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';

interface GradientBackgroundProps {
  primaryColor?: string;
  secondaryColor?: string;
  accentColor?: string;
}

export const GradientBackground: React.FC<GradientBackgroundProps> = ({
  primaryColor = '#6366f1',
  secondaryColor = '#8b5cf6',
  accentColor = '#06b6d4',
}) => {
  const frame = useCurrentFrame();

  // Subtle breathing animation
  const pulse = Math.sin(frame * 0.02) * 8;
  const angle = 135 + Math.sin(frame * 0.01) * 15;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundColor: '#0a0b0e',
        overflow: 'hidden',
      }}
    >
      {/* Dynamic Animated Gradient Mesh */}
      <div
        style={{
          position: 'absolute',
          top: '-20%',
          left: '-20%',
          width: '140%',
          height: '140%',
          background: `
            radial-gradient(circle at 30% 30%, ${primaryColor}26 0%, transparent 50%),
            radial-gradient(circle at 75% 65%, ${secondaryColor}22 0%, transparent 55%),
            radial-gradient(circle at 50% 90%, ${accentColor}18 0%, transparent 45%)
          `,
          transform: `scale(${1 + pulse * 0.01}) rotate(${angle * 0.05}deg)`,
          filter: 'blur(60px)',
        }}
      />

      {/* Cinematic Vignette */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(circle at 50% 50%, rgba(10,11,14,0.1) 0%, rgba(10,11,14,0.85) 100%)',
          pointerEvents: 'none',
        }}
      />

      {/* Grid Architecture Texture Overlay */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage: `
            linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px)
          `,
          backgroundSize: '48px 48px',
          pointerEvents: 'none',
        }}
      />
    </div>
  );
};
