import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const SmokeTest: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 12 } });
  const scale = interpolate(entrance, [0, 1], [0.6, 1.0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a0b0e',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <div
          style={{
            fontSize: '64px',
            fontWeight: 900,
            color: '#6366f1',
            letterSpacing: '-1.5px',
            fontFamily: 'sans-serif',
          }}
        >
          CREATIVE STUDIO ✓
        </div>
        <div
          style={{
            marginTop: '16px',
            fontSize: '22px',
            color: '#06b6d4',
            fontFamily: 'monospace',
            letterSpacing: '4px',
          }}
        >
          REMOTION ENGINE OPERATIONAL
        </div>
      </div>
    </AbsoluteFill>
  );
};
