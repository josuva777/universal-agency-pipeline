---
name: performance-guardian
description: >-
  Core Web Vitals enforcement (LCP < 2.5s, INP < 200ms, CLS < 0.1), Lighthouse CI gates (90+),
  bundle size budgets, Server Components optimization, PPR, image/font hygiene, and edge caching.
  Trigger phrases: "performance", "core web vitals", "lighthouse", "optimize bundle", "lcp",
  "inp", "cls", "fast website", "speed up", "edge cache".
---

# Performance Guardian & Core Web Vitals Standard

This skill establishes the high-velocity performance standards used by Vercel, Linear, and Figma. Every millisecond of latency costs 1% in conversion; web applications must run at silky 60fps with zero layout shifts.

---

## 1. The Core Web Vitals (CWV) Iron Triangle

| Metric | Target | What It Measures | Engineering Solution |
| :--- | :--- | :--- | :--- |
| **LCP** (Largest Contentful Paint) | **< 2.5s** | Loading speed of main visual element | Server Components, `next/image` with `priority`, edge HTML streaming |
| **INP** (Interaction to Next Paint) | **< 200ms** | Tactile responsiveness to user inputs | Remove heavy JS from main thread, use `startTransition`, zero long tasks |
| **CLS** (Cumulative Layout Shift) | **< 0.1** | Visual stability (no jarring jumping) | Explicit aspect ratios on images/videos, font fallback size-adjust |

---

## 2. Server Components (RSC) vs Client Components

Default to **React Server Components**. Treat `'use client'` as a strictly isolated leaf node:

```text
PAGE ROOT (Server Component - 0kB JS shipped to browser)
├── Navbar (Server Component - static shell)
│   └── ThemeDropdown ('use client' - tiny interactive island)
├── HeroSection (Server Component - static content, pre-rendered)
│   └── VideoModalTrigger ('use client' - click state only)
├── FeaturesGrid (Server Component - streamed from server)
└── Footer (Server Component - static HTML)
```

### Golden Rules:
1. **Never mark an entire page or layout as `'use client'`**. Push interactivity down to the smallest possible leaf component.
2. **Heavy Dependencies Stay on the Server**: Libraries like `date-fns`, `marked`, `zod` schemas for validation, and cryptographic hash utilities must remain inside Server Components or Route Handlers — never shipping to browser JS bundles.
3. **Partial Pre-Rendering (PPR)**: Next.js renders the static shell instantly from edge CDN cache while dynamic user data streams in via `<Suspense>` boundaries.

---

## 3. Media, Font & Asset Hygiene

### High-Performance Image Rules (`next/image`):
```tsx
import Image from 'next/image';

// 1. Hero images MUST have priority and fetchPriority="high"
<Image
  src="/hero-emblem.webp"
  alt="SentinelOps Security Core"
  width={600}
  height={600}
  priority
  fetchPriority="high"
  sizes="(max-width: 768px) 100vw, 600px"
  className="object-contain"
/>

// 2. Below-the-fold images MUST use lazy loading
<Image
  src="/features/architecture.webp"
  alt="Architecture diagram"
  width={1200}
  height={800}
  loading="lazy"
  sizes="(max-width: 1200px) 100vw, 1200px"
/>
```

### Zero-CLS Enterprise Typography (`next/font`):
Always use `next/font/google` or local fonts with CSS variable injection. This automatically inlines font definitions and generates fallback metrics (`size-adjust`) to guarantee **0.00 CLS** during font swaps:

```tsx
import { Inter, JetBrains_Mono } from 'next/font/google';

export const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-sans',
});

export const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
});
```

---

## 4. Automated Lighthouse CI Configuration (`lighthouserc.js`)

Every pull request must pass the Lighthouse CI quality gate:

```javascript
module.exports = {
  ci: {
    collect: {
      numberOfRuns: 3,
      startServerCommand: 'npm run start',
      url: ['http://localhost:3000/', 'http://localhost:3000/pricing'],
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.90 }],
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'categories:best-practices': ['error', { minScore: 0.90 }],
        'categories:seo': ['error', { minScore: 0.90 }],
        'first-contentful-paint': ['error', { maxNumericValue: 1800 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

---

## 5. Bundle Size Budget & Analysis

Keep initial JavaScript bundle sizes strictly below **100 kB (gzipped)** per page.

- Run `@next/bundle-analyzer` periodically:
  ```bash
  ANALYZE=true pnpm build
  ```
- **Dynamic Imports**: Code-split non-critical modals and 3D canvases:
  ```tsx
  import dynamic from 'next/dynamic';

  const Canvas3D = dynamic(() => import('@/components/Canvas3D'), {
    ssr: false,
    loading: () => <div className="h-96 w-full animate-pulse bg-slate-900 rounded-xl" />,
  });
  ```

