import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { CaptionWord } from '../types';

interface SubtitlesProps {
  subtitles?: CaptionWord[];
  highlightColor?: string;
}

export const Subtitles: React.FC<SubtitlesProps> = ({
  subtitles = [],
  highlightColor = '#facc15', // Vibrant amber/yellow for karaoke
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  // Find active word
  const activeWordIndex = subtitles.findIndex(
    (w) => currentTime >= w.start_seconds && currentTime <= w.end_seconds
  );

  // Group into current 4-word window
  const windowStart = Math.max(0, activeWordIndex - 2);
  const activeWindow = subtitles.slice(windowStart, windowStart + 5);

  if (activeWindow.length === 0) {
    return null;
  }

  return (
    <div
      style={{
        position: 'absolute',
        bottom: '80px',
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '14px',
        padding: '0 40px',
        pointerEvents: 'none',
        zIndex: 50,
      }}
    >
      <div
        style={{
          background: 'rgba(10, 11, 14, 0.75)',
          backdropFilter: 'blur(16px)',
          padding: '12px 28px',
          borderRadius: '32px',
          border: '1px solid rgba(255, 255, 255, 0.12)',
          display: 'flex',
          gap: '12px',
          boxShadow: '0 12px 32px rgba(0, 0, 0, 0.5)',
        }}
      >
        {activeWindow.map((wordObj, i) => {
          const isSpoken = currentTime >= wordObj.start_seconds;
          const isCurrent =
            currentTime >= wordObj.start_seconds && currentTime <= wordObj.end_seconds;

          return (
            <span
              key={i}
              style={{
                fontSize: '28px',
                fontWeight: 800,
                color: isCurrent ? highlightColor : isSpoken ? '#ffffff' : 'rgba(255, 255, 255, 0.4)',
                transform: isCurrent ? 'scale(1.12)' : 'scale(1.0)',
                transition: 'all 0.1s ease-out',
                display: 'inline-block',
                textShadow: isCurrent ? `0 0 16px ${highlightColor}aa` : 'none',
                fontFamily: "system-ui, -apple-system, 'Geist Sans', sans-serif",
                letterSpacing: '-0.5px',
              }}
            >
              {wordObj.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
