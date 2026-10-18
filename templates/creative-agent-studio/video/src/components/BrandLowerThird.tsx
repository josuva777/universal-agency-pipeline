import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface BrandLowerThirdProps {
  title: string;
  subtitle: string;
  accentColor?: string;
}

export const BrandLowerThird: React.FC<BrandLowerThirdProps> = ({
  title,
  subtitle,
  accentColor = '#6366f1',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  const translateX = interpolate(entrance, [0, 1], [-400, 0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);

  return (
    <div
      style={{
        position: 'absolute',
        bottom: '90px',
        left: '90px',
        display: 'flex',
        alignItems: 'center',
        gap: '20px',
        transform: `translateX(${translateX}px)`,
        opacity,
        zIndex: 40,
      }}
    >
      {/* Accent Vertical Bar */}
      <div
        style={{
          width: '6px',
          height: '64px',
          borderRadius: '4px',
          backgroundColor: accentColor,
          boxShadow: `0 0 16px ${accentColor}`,
        }}
      />

      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <div
          style={{
            fontSize: '28px',
            fontWeight: 800,
            color: '#ffffff',
            fontFamily: "system-ui, -apple-system, 'Geist Sans', sans-serif",
            letterSpacing: '-0.5px',
          }}
        >
          {title}
        </div>
        <div
          style={{
            fontSize: '15px',
            fontWeight: 600,
            color: 'rgba(255, 255, 255, 0.65)',
            fontFamily: "system-ui, -apple-system, 'Geist Mono', monospace",
            letterSpacing: '1px',
          }}
        >
          {subtitle.toUpperCase()}
        </div>
      </div>
    </div>
  );
};
