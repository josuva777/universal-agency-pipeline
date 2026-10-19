# 🎨 Interactive 3D Web & Mobile Motion Architecture

To ensure client applications never look flat, generic, or AI-generated, modern frontends demand real-time 3D, physics-driven typography, and momentum scrolling.

---

## 🌐 1. Web 3D & Advanced Motion Stack

### A. 3D Model Pipeline with `gltfjsx`
Never manually load raw GLTF files with boilerplate loaders. Use `gltfjsx` to auto-generate typed React Three Fiber components with Draco mesh compression:

```bash
# Convert GLB to optimized, typed React component
npx gltfjsx public/models/shoe.glb --transform --types --output src/components/ShoeModel.tsx
```

Features auto-enabled:
- WebP texture recompression
- Draco mesh compression (up to 80% smaller bundle)
- Automatic shadows, materials, and typed nodes

### B. Spline 3D Embeds
For interactive illustrative 3D without full Three.js scene boilerplate:
```bash
npm install @splinetool/react-spline @splinetool/runtime
```
```tsx
import Spline from '@splinetool/react-spline';

export function InteractiveHero3D() {
  return (
    <div className="w-full h-[600px] relative">
      <Spline scene="https://prod.spline.design/your-scene-id/scene.splinecode" />
    </div>
  );
}
```

### C. Lenis Smooth Momentum Scrolling
Eliminates stiff default browser scrolling and enables Apple/Nike-style fluid momentum:
```bash
npm install lenis
```
```tsx
import { useEffect } from 'react';
import Lenis from 'lenis';

export function SmoothScrollProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    });

    function raf(time: number) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    return () => lenis.destroy();
  }, []);

  return <>{children}</>;
}
```

### D. Procedural SVGs & Contrast Tools
- **Haikei.app**: Generate mathematical SVG background waves, layered grids, and polygon clusters directly into CSS backgrounds.
- **RealtimeColors.com**: Harmonize 60-30-10 color proportions with guaranteed WCAG AAA contrast before setting CSS variables.

---

## 📱 2. Mobile 60fps Physics: Skia + Reanimated 3

For high-end React Native and Expo apps, avoid standard View animations. Run hardware-accelerated shaders and worklets directly on the native UI thread.

### A. React Native Skia (`@shopify/react-native-skia`)
Enables custom shaders, gradient blurs, glowing orbs, and particle systems:
```tsx
import { Canvas, Circle, SweepGradient, vec } from '@shopify/react-native-skia';

export function GlowingOrb({ size = 200 }: { size?: number }) {
  const r = size / 2;
  return (
    <Canvas style={{ width: size, height: size }}>
      <Circle cx={r} cy={r} r={r}>
        <SweepGradient
          c={vec(r, r)}
          colors={['#06b6d4', '#6366f1', '#d946ef', '#06b6d4']}
        />
      </Circle>
    </Canvas>
  );
}
```

### B. React Native Reanimated 3 (`react-native-reanimated`)
Runs gesture-driven physics directly on the UI thread without crossing the JavaScript bridge:
```tsx
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';
import { GestureDetector, Gesture } from 'react-native-gesture-handler';

export function InteractiveCard({ children }: { children: React.ReactNode }) {
  const pressed = useSharedValue(false);

  const tap = Gesture.Tap()
    .onBegin(() => { pressed.value = true; })
    .onFinalize(() => { pressed.value = false; });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: withSpring(pressed.value ? 0.95 : 1.0) }],
  }));

  return (
    <GestureDetector gesture={tap}>
      <Animated.View style={animatedStyle}>
        {children}
      </Animated.View>
    </GestureDetector>
  );
}
```
