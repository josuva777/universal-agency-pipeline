import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface DeviceMockupProps {
  accentColor?: string;
  headline?: string;
}

export const DeviceMockup3D: React.FC<DeviceMockupProps> = ({
  accentColor = '#6366f1',
  headline = 'INTELLIGENCE AT SCALE',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Floating inertia math
  const floatY = Math.sin(frame * 0.04) * 14;
  const rotateY = Math.sin(frame * 0.03) * 8;
  const rotateX = Math.cos(frame * 0.02) * 5;

  const entrance = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 80 },
  });

  const scale = interpolate(entrance, [0, 1], [0.75, 1.0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);

  return (
    <div
      style={{
        position: 'relative',
        width: '380px',
        height: '680px',
        perspective: '1200px',
        margin: '0 auto',
        transform: `scale(${scale})`,
        opacity,
      }}
    >
      {/* 3D Rotational Canvas */}
      <div
        style={{
          width: '100%',
          height: '100%',
          borderRadius: '48px',
          background: 'linear-gradient(145deg, #181920 0%, #0d0e12 100%)',
          boxShadow: `
            0 30px 80px rgba(0, 0, 0, 0.8),
            0 0 40px ${accentColor}33,
            inset 0 0 2px rgba(255, 255, 255, 0.4)
          `,
          border: '8px solid #232530',
          transform: `translateY(${floatY}px) rotateY(${rotateY}deg) rotateX(${rotateX}deg)`,
          transformStyle: 'preserve-3d',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '28px',
          boxSizing: 'border-box',
        }}
      >
        {/* Dynamic Island / Notch */}
        <div
          style={{
            position: 'absolute',
            top: '18px',
            width: '100px',
            height: '24px',
            borderRadius: '16px',
            backgroundColor: '#050507',
            zIndex: 10,
          }}
        />

        {/* Screen Content UI */}
        <div
          style={{
            width: '100%',
            height: '100%',
            borderRadius: '32px',
            background: 'linear-gradient(180deg, rgba(99, 102, 241, 0.15) 0%, rgba(10, 11, 14, 0.95) 100%)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            padding: '24px',
            textAlign: 'center',
          }}
        >
          {/* Glowing App Icon */}
          <div
            style={{
              width: '72px',
              height: '72px',
              borderRadius: '20px',
              background: `linear-gradient(135deg, ${accentColor} 0%, #d946ef 100%)`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: `0 10px 30px ${accentColor}66`,
              marginBottom: '24px',
            }}
          >
            <div
              style={{
                width: '32px',
                height: '32px',
                border: '4px solid #ffffff',
                borderRadius: '8px',
                transform: `rotate(${frame * 2}deg)`,
              }}
            />
          </div>

          <div
            style={{
              fontSize: '22px',
              fontWeight: 800,
              color: '#ffffff',
              letterSpacing: '-0.5px',
              fontFamily: 'sans-serif',
              marginBottom: '8px',
            }}
          >
            {headline}
          </div>

          <div
            style={{
              fontSize: '13px',
              color: 'rgba(255, 255, 255, 0.6)',
              fontFamily: 'monospace',
              letterSpacing: '1px',
            }}
          >
            ACTIVE • 60 FPS • NATIVE
          </div>
        </div>

        {/* Specular Glare Reflection */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: 'linear-gradient(115deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0) 50%)',
            pointerEvents: 'none',
          }}
        />
      </div>
    </div>
  );
};
