import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from 'remotion';
import { CommercialProps } from './types';
import { GradientBackground } from './components/GradientBackground';
import { ParticleVFX } from './components/ParticleVFX';
import { KineticText } from './components/KineticText';
import { DeviceMockup3D } from './components/DeviceMockup3D';
import { Subtitles } from './components/Subtitles';
import { LogoReveal } from './components/LogoReveal';
import { BrandLowerThird } from './components/BrandLowerThird';

export const Commercial: React.FC<CommercialProps> = ({
  projectName = 'Apex Commercial',
  brandName = 'APEX',
  tagline = 'INTELLIGENCE AMPLIFIED',
  theme = {
    primary: '#6366f1',
    secondary: '#8b5cf6',
    accent: '#06b6d4',
    background: '#0a0b0e',
  },
  scenes = [
    { id: 1, type: 'hero', headline: 'THE NEXT ERA', subtext: 'Speed Without Compromise', duration_seconds: 3.5 },
    { id: 2, type: 'tension', headline: 'RETHINK EVERYTHING', subtext: 'Legacy tools hold you back', duration_seconds: 3.5 },
    { id: 3, type: 'mockup_3d', headline: 'ENGINEERED PRECISION', subtext: '3D Architecture at scale', duration_seconds: 5.0 },
    { id: 4, type: 'metrics', headline: '+400% FASTER', subtext: 'Validated by industry benchmarks', duration_seconds: 3.5 },
    { id: 5, type: 'cta', headline: 'APEX', subtext: 'Start Free Today', duration_seconds: 4.5 },
  ],
  voiceoverAudioPath,
  subtitles = [],
  logoSvgPath,
  brollClips = [],
}) => {
  const { fps } = useVideoConfig();

  let accumulatedFrames = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: theme.background }}>
      {/* 1. Universal Ambient Background & Particle VFX */}
      <GradientBackground
        primaryColor={theme.primary}
        secondaryColor={theme.secondary}
        accentColor={theme.accent}
      />
      <ParticleVFX count={55} accentColor={theme.primary} />

      {/* 2. Audio Voiceover Track if provided */}
      {voiceoverAudioPath && (
        <Audio src={voiceoverAudioPath} />
      )}

      {/* 3. Sequenced Video Scenes */}
      {scenes.map((scene, index) => {
        const sceneDurationFrames = Math.round(scene.duration_seconds * fps);
        const fromFrame = accumulatedFrames;
        accumulatedFrames += sceneDurationFrames;

        return (
          <Sequence
            key={scene.id}
            from={fromFrame}
            durationInFrames={sceneDurationFrames}
            name={`Scene ${scene.id}: ${scene.type}`}
          >
            <AbsoluteFill
              style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                padding: '0 80px',
              }}
            >
              {scene.type === 'hero' && (
                <div style={{ textAlign: 'center' }}>
                  <KineticText text={scene.headline} fontSize={88} color="#ffffff" />
                  <div style={{ marginTop: '20px' }}>
                    <KineticText
                      text={scene.subtext}
                      fontSize={32}
                      color={theme.accent}
                      styleMode="typewriter"
                      delayFrames={20}
                    />
                  </div>
                </div>
              )}

              {scene.type === 'tension' && (
                <div style={{ textAlign: 'center' }}>
                  <KineticText text={scene.headline} fontSize={84} color="#f43f5e" />
                  <div style={{ marginTop: '24px' }}>
                    <KineticText text={scene.subtext} fontSize={32} color="#ffffff" delayFrames={15} />
                  </div>
                </div>
              )}

              {scene.type === 'mockup_3d' && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '80px', width: '100%', justifyContent: 'center' }}>
                  <DeviceMockup3D accentColor={theme.primary} headline={brandName} />
                  <div style={{ maxWidth: '550px' }}>
                    <KineticText text={scene.headline} fontSize={64} color="#ffffff" />
                    <div style={{ marginTop: '16px' }}>
                      <KineticText text={scene.subtext} fontSize={28} color={theme.accent} delayFrames={10} />
                    </div>
                  </div>
                </div>
              )}

              {scene.type === 'metrics' && (
                <div style={{ textAlign: 'center' }}>
                  <div
                    style={{
                      fontSize: '120px',
                      fontWeight: 900,
                      color: theme.accent,
                      fontFamily: "system-ui, -apple-system, 'Geist Sans', sans-serif",
                      letterSpacing: '-3px',
                      textShadow: `0 0 50px ${theme.accent}88`,
                    }}
                  >
                    {scene.headline}
                  </div>
                  <div style={{ marginTop: '16px' }}>
                    <KineticText text={scene.subtext} fontSize={32} color="#ffffff" delayFrames={10} />
                  </div>
                  <BrandLowerThird title="VERIFIED BENCHMARK" subtitle="Q3 Performance Audit" accentColor={theme.primary} />
                </div>
              )}

              {scene.type === 'cta' && (
                <LogoReveal
                  brandName={brandName}
                  tagline={tagline}
                  primaryColor={theme.primary}
                  accentColor={theme.accent}
                />
              )}
            </AbsoluteFill>
          </Sequence>
        );
      })}

      {/* 4. Subtitles Overlay */}
      {subtitles.length > 0 && (
        <Subtitles subtitles={subtitles} highlightColor="#facc15" />
      )}
    </AbsoluteFill>
  );
};
