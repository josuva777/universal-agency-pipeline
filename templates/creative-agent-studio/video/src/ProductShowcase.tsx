import React from 'react';
import { AbsoluteFill, useVideoConfig } from 'remotion';
import { CommercialProps } from './types';
import { GradientBackground } from './components/GradientBackground';
import { ParticleVFX } from './components/ParticleVFX';
import { DeviceMockup3D } from './components/DeviceMockup3D';
import { KineticText } from './components/KineticText';
import { BrandLowerThird } from './components/BrandLowerThird';

export const ProductShowcase: React.FC<CommercialProps> = ({
  brandName = 'NOVA',
  tagline = 'NEXT-GEN HARDWARE',
  theme = {
    primary: '#06b6d4',
    secondary: '#3b82f6',
    accent: '#10b981',
    background: '#090a0f',
  },
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor: theme.background }}>
      <GradientBackground
        primaryColor={theme.primary}
        secondaryColor={theme.secondary}
        accentColor={theme.accent}
      />
      <ParticleVFX count={60} accentColor={theme.primary} />

      <AbsoluteFill
        style={{
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '100px',
          padding: '0 100px',
        }}
      >
        <DeviceMockup3D accentColor={theme.primary} headline={brandName} />

        <div style={{ maxWidth: '600px' }}>
          <KineticText text={`${brandName.toUpperCase()} PRO`} fontSize={76} color="#ffffff" />
          <div style={{ marginTop: '20px' }}>
            <KineticText
              text="Zero latency. Aerospace-grade enclosure. Built for elite creative workflows."
              fontSize={28}
              color={theme.accent}
              styleMode="typewriter"
              delayFrames={20}
            />
          </div>
        </div>
      </AbsoluteFill>

      <BrandLowerThird
        title={`${brandName} HARDWARE SPEC`}
        subtitle="Titanium Grade 5 • 4K 60FPS"
        accentColor={theme.primary}
      />
    </AbsoluteFill>
  );
};
