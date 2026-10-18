# Brand Kit & Procedural Vector Identity System

High-end brands require deterministic vector graphics that maintain mathematical purity at any display size.

---

## 1. The 60-30-10 Color Harmonization Rule

Every generated brand system calculates a tri-color palette:
- **60% Dominant Base**: Deep Obsidian (`#0a0b0e`), Alabaster White (`#f8fafc`), or Slate Navy (`#0f172a`).
- **30% Secondary Structure**: Card backgrounds, border lines, muted typography (`#1e293b`, `#e2e8f0`).
- **10% Accent Flame**: High-voltage accent for buttons, highlights, and glowing VFX (`#6366f1` Indigo, `#06b6d4` Cyan, `#f59e0b` Amber, `#10b981` Emerald).

---

## 2. Procedural SVG Logo Generation Architecture

```svg
<!-- Example Procedural Geometric Hexagon Logo -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <!-- Metallic Gradient -->
    <linearGradient id="brandGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366f1" />
      <stop offset="50%" stop-color="#8b5cf6" />
      <stop offset="100%" stop-color="#d946ef" />
    </linearGradient>

    <!-- Volumetric Glow Filter -->
    <filter id="brandGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="12" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background Base (Optional Dark Mode Shield) -->
  <rect width="500" height="500" rx="100" fill="#090a0f" />

  <!-- Animated Stroke Path -->
  <g filter="url(#brandGlow)">
    <polygon points="250,90 390,170 390,330 250,410 110,330 110,170"
             fill="none"
             stroke="url(#brandGrad)"
             stroke-width="24"
             stroke-linejoin="round"
             stroke-linecap="round" />
    
    <!-- Inner Core Node -->
    <circle cx="250" cy="250" r="38" fill="url(#brandGrad)" />
  </g>
</svg>
```

---

## 3. Typography Hierarchy Rules
- **Headline Font**: Modern Geometric Sans (`Geist Sans`, `Inter Display`, or `Cabinet Grotesk`) with negative letter spacing (`-0.03em`).
- **Body & Captions**: High-legibility sans (`Inter`, `SF Pro`) with generous line-height (`1.6`).
- **Accent Monospace**: For metrics, timestamps, and technical stats (`Geist Mono`, `JetBrains Mono`).
