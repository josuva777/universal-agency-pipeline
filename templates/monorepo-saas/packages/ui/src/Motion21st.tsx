'use client';
import React, { useRef, useState } from 'react';
import { useTheme } from './ThemeEngine';

export interface SpotlightCardProps {
  children: React.ReactNode;
  className?: string;
  spotlightColor?: string;
}

/**
 * 21st.dev × UI/UX Pro Max: Dynamic Mouse Spotlight Tracking Card
 * Tracks cursor position with smooth radial gradient highlighting and 1px border.
 */
export const SpotlightCard: React.FC<SpotlightCardProps> = ({
  children,
  className = '',
  spotlightColor = 'rgba(16, 185, 129, 0.15)'
}) => {
  const divRef = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [opacity, setOpacity] = useState(0);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!divRef.current) return;
    const rect = divRef.current.getBoundingClientRect();
    setPosition({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  };

  return (
    <div
      ref={divRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setOpacity(1)}
      onMouseLeave={() => setOpacity(0)}
      className={`relative overflow-hidden rounded-2xl border transition-all duration-300 ${className}`}
      style={{
        backgroundColor: '#0b0f19',
        borderColor: 'rgba(255, 255, 255, 0.08)'
      }}
    >
      {/* 21st.dev Radial Spotlight Layer */}
      <div
        className="pointer-events-none absolute -inset-px transition-opacity duration-300"
        style={{
          opacity,
          background: `radial-gradient(600px circle at ${position.x}px ${position.y}px, ${spotlightColor}, transparent 40%)`
        }}
      />
      <div className="relative z-10">{children}</div>
    </div>
  );
};

export interface ShimmerButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  shimmerColor?: string;
  shimmerDuration?: string;
}

/**
 * 21st.dev × Framer Motion: Shimmer Button with Emil Kowalski Tap Physics
 */
export const ShimmerButton: React.FC<ShimmerButtonProps> = ({
  children,
  className = '',
  shimmerColor = '#10b981',
  onClick,
  ...props
}) => {
  const [isPressed, setIsPressed] = useState(false);

  // WebAudio Click Synthesis (UI/UX Pro Max tactile feedback)
  const playClick = () => {
    try {
      const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(800, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 0.03);
      gain.gain.setValueAtTime(0.04, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.03);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.03);
    } catch (_) {}
  };

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    playClick();
    if (onClick) onClick(e);
  };

  return (
    <button
      {...props}
      onClick={handleClick}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onMouseLeave={() => setIsPressed(false)}
      className={`relative inline-flex items-center justify-center px-6 py-3 rounded-xl font-mono text-xs font-bold uppercase tracking-wider text-slate-950 overflow-hidden shadow-xl transition-transform duration-100 ${className}`}
      style={{
        backgroundColor: shimmerColor,
        transform: isPressed ? 'scale(0.97)' : 'scale(1)'
      }}
    >
      <span className="relative z-10 flex items-center gap-2">{children}</span>
    </button>
  );
};
