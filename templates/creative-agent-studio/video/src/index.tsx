import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { Commercial } from './Commercial';
import { ProductShowcase } from './ProductShowcase';
import { SmokeTest } from './SmokeTest';

export const RemotionVideo: React.FC = () => {
  return (
    <>
      {/* 60s High-Converting Commercial Master (1080p 60fps) */}
      <Composition
        id="Commercial"
        component={Commercial}
        durationInFrames={1200}
        fps={60}
        width={1920}
        height={1080}
        defaultProps={{
          projectName: 'Apex Commercial',
          brandName: 'APEX',
          tagline: 'INTELLIGENCE AMPLIFIED',
          theme: {
            primary: '#6366f1',
            secondary: '#8b5cf6',
            accent: '#06b6d4',
            background: '#0a0b0e',
          },
        }}
      />

      {/* 60s High-Converting Commercial Master (Native 4K UHD 3840x2160 60fps) */}
      <Composition
        id="Commercial-4K"
        component={Commercial}
        durationInFrames={1200}
        fps={60}
        width={3840}
        height={2160}
        defaultProps={{
          projectName: 'Apex Commercial 4K Master',
          brandName: 'APEX',
          tagline: 'INTELLIGENCE AMPLIFIED',
          theme: {
            primary: '#6366f1',
            secondary: '#8b5cf6',
            accent: '#06b6d4',
            background: '#0a0b0e',
          },
        }}
      />

      {/* 30s 3D Hardware / Product Showcase (1080p 60fps) */}
      <Composition
        id="ProductShowcase"
        component={ProductShowcase}
        durationInFrames={1800}
        fps={60}
        width={1920}
        height={1080}
        defaultProps={{
          brandName: 'NOVA',
          tagline: 'NEXT-GEN HARDWARE',
        }}
      />

      {/* 30s 3D Hardware / Product Showcase (Native 4K UHD 3840x2160 60fps) */}
      <Composition
        id="ProductShowcase-4K"
        component={ProductShowcase}
        durationInFrames={1800}
        fps={60}
        width={3840}
        height={2160}
        defaultProps={{
          brandName: 'NOVA',
          tagline: 'NEXT-GEN HARDWARE',
        }}
      />

      {/* Lightweight 3s Smoke Test */}
      <Composition
        id="SmokeTest"
        component={SmokeTest}
        durationInFrames={180}
        fps={60}
        width={1920}
        height={1080}
      />
    </>
  );
};

registerRoot(RemotionVideo);

