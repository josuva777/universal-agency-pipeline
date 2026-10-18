# 3D Visual Effects, Shaders & Camera Rigs

This reference details the code-driven VFX architecture used in the Creative Studio. Every effect is computed in real-time or rendered deterministically via Three.js / WebGL / React Three Fiber.

---

## 1. 3D Device Mockup (React Three Fiber)

```tsx
import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { RoundedBox, MeshReflectorMaterial, Float } from '@react-three/drei';
import * as THREE from 'three';

interface DeviceMockupProps {
  screenTextureUrl?: string;
  accentColor?: string;
}

export const ModernPhone3D: React.FC<DeviceMockupProps> = ({
  accentColor = '#6366f1',
}) => {
  const meshRef = useRef<THREE.Group>(null);

  useFrame(({ clock }) => {
    if (meshRef.current) {
      // Cinematic slow floating inertia
      const t = clock.getElapsedTime();
      meshRef.current.rotation.y = Math.sin(t * 0.5) * 0.25;
      meshRef.current.rotation.x = Math.cos(t * 0.3) * 0.1;
    }
  });

  return (
    <group ref={meshRef}>
      {/* Phone Chassis (Matte Titanium) */}
      <RoundedBox args={[2.5, 5.2, 0.25]} radius={0.18} smoothness={8}>
        <meshStandardMaterial
          color="#1e2024"
          metalness={0.85}
          roughness={0.2}
          envMapIntensity={1.5}
        />
      </RoundedBox>

      {/* Screen Glass Face */}
      <RoundedBox args={[2.35, 5.05, 0.02]} radius={0.14} smoothness={4} position={[0, 0, 0.13]}>
        <meshPhysicalMaterial
          color="#0f1115"
          roughness={0.05}
          transmission={0.1}
          reflectivity={0.9}
          clearcoat={1.0}
        />
      </RoundedBox>

      {/* Camera Island Pill */}
      <RoundedBox args={[0.7, 0.22, 0.04]} radius={0.08} smoothness={4} position={[0, 2.2, 0.14]}>
        <meshBasicMaterial color="#050507" />
      </RoundedBox>
    </group>
  );
};
```

---

## 2. Floating Atmospheric Particle Field (Canvas 2D / WebGL)

Floating dust motes and micro-sparks prevent video scenes from looking static.

```tsx
import React, { useMemo } from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';

interface Particle {
  x: number;
  y: number;
  size: number;
  speedY: number;
  opacity: number;
}

export const CinematicParticleField: React.FC<{ count?: number; color?: string }> = ({
  count = 60,
  color = 'rgba(255, 255, 255,',
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const particles: Particle[] = useMemo(() => {
    return Array.from({ length: count }).map((_, i) => ({
      x: ((i * 137.5) % width),
      y: ((i * 89.3) % height),
      size: 1.5 + (i % 3) * 1.2,
      speedY: 0.5 + (i % 5) * 0.4,
      opacity: 0.2 + (i % 4) * 0.15,
    }));
  }, [count, width, height]);

  return (
    <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', overflow: 'hidden' }}>
      {particles.map((p, idx) => {
        const currentY = (p.y - frame * p.speedY + height) % height;
        const currentX = p.x + Math.sin((frame + idx * 20) * 0.02) * 20;

        return (
          <div
            key={idx}
            style={{
              position: 'absolute',
              left: currentX,
              top: currentY,
              width: p.size,
              height: p.size,
              borderRadius: '50%',
              backgroundColor: `${color} ${p.opacity})`,
              boxShadow: `0 0 ${p.size * 3}px ${color} 0.6)`,
            }}
          />
        );
      })}
    </div>
  );
};
```

---

## 3. Post-Processing Chromatic Aberration & Grain

Adds high-budget lens characteristics:
- **RGB Split**: Red and blue channels shift slightly during fast motion.
- **Micro-Grain**: Removes digital quantization banding from gradients.

```css
/* Film grain overlay */
.cinematic-grain {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.04'/%3E%3C/svg%3E");
  mix-blend-mode: overlay;
}
```
