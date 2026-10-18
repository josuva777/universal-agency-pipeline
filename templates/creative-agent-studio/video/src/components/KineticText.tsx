import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface KineticTextProps {
  text: string;
  styleMode?: 'split-words' | 'split-chars' | 'typewriter' | 'scramble';
  color?: string;
  fontSize?: number;
  delayFrames?: number;
}

export const KineticText: React.FC<KineticTextProps> = ({
  text,
  styleMode = 'split-words',
  color = '#ffffff',
  fontSize = 72,
  delayFrames = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const words = text.split(' ');

  if (styleMode === 'split-words') {
    return (
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '18px',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        {words.map((word, index) => {
          const wordDelay = delayFrames + index * 4;
          const wordProgress = spring({
            frame: frame - wordDelay,
            fps,
            config: {
              damping: 14,
              mass: 0.8,
              stiffness: 120,
            },
          });

          const translateY = interpolate(wordProgress, [0, 1], [60, 0]);
          const opacity = interpolate(wordProgress, [0, 1], [0, 1]);
          const scale = interpolate(wordProgress, [0, 1], [0.85, 1.0]);

          return (
            <span
              key={index}
              style={{
                display: 'inline-block',
                transform: `translateY(${translateY}px) scale(${scale})`,
                opacity,
                fontSize: `${fontSize}px`,
                fontWeight: 800,
                color,
                letterSpacing: '-1.5px',
                textShadow: '0 8px 32px rgba(0,0,0,0.6)',
                fontFamily: "system-ui, -apple-system, 'Geist Sans', sans-serif",
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    );
  }

  // Typewriter Mode
  const charsCount = Math.floor(
    interpolate(frame - delayFrames, [0, words.join(' ').length * 2], [0, words.join(' ').length], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    })
  );
  const visibleText = text.slice(0, Math.max(0, charsCount));

  return (
    <div
      style={{
        fontSize: `${fontSize}px`,
        fontWeight: 800,
        color,
        letterSpacing: '-1px',
        fontFamily: "system-ui, -apple-system, 'Geist Sans', sans-serif",
        textAlign: 'center',
      }}
    >
      {visibleText}
      <span style={{ opacity: frame % 15 < 8 ? 1 : 0, color: '#6366f1' }}>|</span>
    </div>
  );
};
