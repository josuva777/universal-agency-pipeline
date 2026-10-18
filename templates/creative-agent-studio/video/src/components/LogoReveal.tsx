import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface LogoRevealProps {
  brandName?: string;
  tagline?: string;
  primaryColor?: string;
  accentColor?: string;
}

export const LogoReveal: React.FC<LogoRevealProps> = ({
  brandName = 'APEX',
  tagline = 'INTELLIGENCE AMPLIFIED',
  primaryColor = '#6366f1',
  accentColor = '#06b6d4',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  const scale = interpolate(entrance, [0, 1], [0.6, 1.0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);
  const strokeDashoffset = interpolate(frame, [0, 45], [600, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        transform: `scale(${scale})`,
        opacity,
      }}
    >
      {/* Animated SVG Geometric Mark */}
      <svg width="180" height="180" viewBox="0 0 200 200" style={{ overflow: 'visible' }}>
        <defs>
          <linearGradient id="logoRevGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={primaryColor} />
            <stop offset="100%" stopColor={accentColor} />
          </linearGradient>
          <filter id="revGlow">
            <feGaussianBlur stdDeviation="12" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        <g filter="url(#revGlow)">
          <polygon
            points="100,20 180,65 180,155 100,200 20,155 20,65"
            fill="none"
            stroke="url(#logoRevGrad)"
            strokeWidth="12"
            strokeLinejoin="round"
            strokeDasharray="600"
            strokeDashoffset={strokeDashoffset}
          />
          <circle
            cx="100"
            cy="110"
            r="24"
            fill="url(#logoRevGrad)"
            style={{
              opacity: interpolate(frame, [25, 45], [0, 1]),
              transform: `scale(${interpolate(frame, [25, 45], [0.2, 1])})`,
              transformOrigin: '100px 110px',
            }}
          />
        </g>
      </svg>

      {/* Brand Title Wordmark */}
      <div
        style={{
          marginTop: '36px',
          fontSize: '76px',
          fontWeight: 900,
          color: '#ffffff',
          letterSpacing: '-2px',
          fontFamily: "system-ui, -apple-system, 'Geist Sans', sans-serif",
          textShadow: `0 10px 40px ${primaryColor}66`,
        }}
      >
        {brandName.toUpperCase()}
      </div>

      {/* Architectural Tagline */}
      <div
        style={{
          marginTop: '12px',
          fontSize: '18px',
          fontWeight: 600,
          color: primaryColor,
          letterSpacing: '8px',
          fontFamily: "system-ui, -apple-system, 'Geist Mono', monospace",
          opacity: 0.9,
        }}
      >
        {tagline.toUpperCase()}
      </div>
    </div>
  );
};
