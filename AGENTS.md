# Universal Agency Pipeline v2.0 — Master Workflow Rules & Enterprise Guardrails

## 1. Crucial Rule: Token Guardrails & Multi-Agent Context Protocol
Every active MCP server injects its tool definitions into the prompt on every message:
- **Always-On Global Core** (`~/.gemini/config/mcp_config.json`):
  - **MemPalace**: ~170 tokens for local verbatim all-session memory and inter-agent checkpoints
  - **Headroom**: Token compression engine (shrinks tool outputs & logs by 47–92%)
  - **Context7**: Live documentation lookup (zero guesses on external APIs)
  - **GitHub MCP**: Branching, commits, pull requests (`josuva777`)
- **Workspace-Only** (`.agents/mcp_config.json` per client project):
  - **Web Project**: Playwright MCP + Supabase MCP (isolated dev branches)
  - **Mobile Project**: Swap Playwright for Maestro MCP
  - **Deploy Targets**: Vercel MCP / Cloudflare MCP (Streamable HTTP with browser OAuth)
- **Pre-Deploy Phase Only**:
  - Run **Strix** (security pentest) and **Promptfoo** (AI agent evaluations) via one-shot CLI skill (`pre-deploy-security`) right before opening the final PR, NOT as persistent MCP servers.
- **Output Token Compression (Ponytail)**:
  - Enforce minimal senior-dev surgical diffs via `replace_file_content`. Never rewrite entire files for small changes (cuts generation tokens by 54%+).
  - **30-Message Context Reset**: At turn 30 of any long session, compact context (`/compact`) or checkpoint decisions into `MemPalace` to avoid reasoning degradation.
- **Strict Limit**: Never exceed 6 active MCP servers in any single conversation turn.

---

## 2. Zero-Trust Security & Supply Chain Integrity
- **NEVER** commit or stage `.env`, `.env.local`, API tokens, private keys, or raw connection strings.
- Always use environment variable expansion (`${VAR}`) or OS-level environment variables.
- Before committing, verify git status is clean of private data via `.agents/secret_scan.py`.
- **SBOM Generation**: Every production release MUST generate a CycloneDX SBOM (`npx @cyclonedx/cyclonedx-npm --output-file releases/sbom.json`).
- **Dependency Scanning**: Run `pnpm audit --audit-level=high` in CI. Block merges on CRITICAL/HIGH vulnerabilities with reachability confirmation.
- **Content Security Policy**: All web deployments MUST include strict nonce-based CSP headers (NOT host allowlists).
- **Rate Limiting**: Authentication endpoints (`/login`, `/signup`, `/otp/send`) MUST enforce sliding-window rate limits (max 5 attempts per IP per 15 minutes).
- **Cryptographic Artifact Signing**: Release artifacts (APK, WebAPK, Windows launcher) MUST include SHA-256 checksums in `LATEST_RELEASE.json`.

---

## 3. Monorepo Architecture & End-to-End Type Safety
- **Default Architecture**: Turborepo + pnpm workspaces for multi-package projects:
  `apps/` (web, mobile, docs) + `packages/` (ui, database, api, config).
- **Shared Configs**: Root `tsconfig.base.json` with `strict: true`, `noUncheckedIndexedAccess: true`. Shared Biome/Tailwind configs in `packages/config/`.
- **Workspace Protocol**: Import shared packages via `@repo/ui`, `@repo/database`, `@repo/api`. Enforce clean package boundaries — no circular dependencies, no deep relative imports.
- **Remote Caching**: Enable Turborepo remote caching for CI (only rebuild affected packages on PR).
- **End-to-End Type Safety**: Shared Zod schemas (`@repo/api`) compile-time validate payloads across Next.js frontend, Expo mobile, and backend handlers.

---

## 4. Quality, Performance & Accessibility Standards
- **Formatting & Linting**: Use **Biome** (`npx @biomejs/biome check --write .`) for ultra-fast <50ms linting and formatting. Fall back to Prettier if Biome is unconfigured.
- **Core Web Vitals Targets**: LCP < 2.5s, INP < 200ms, CLS < 0.1. Monitor field data via Vercel Speed Insights or CrUX.
- **Lighthouse CI Quality Gate**: Production builds MUST pass Lighthouse CI gates: Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 90, SEO ≥ 90.
- **WCAG 2.2 AA Compliance**: All interactive elements ≥ 24×24px touch targets (2.5.8). Focus never obscured by sticky headers (2.4.11). Color contrast ≥ 4.5:1. `axe-core` automated scans MUST report 0 violations.
- **Server Components First**: Default to React Server Components. Mark `'use client'` only for interactive leaf components requiring useState/useEffect/browser events. Heavy dependencies stay server-side.
- **Observability**: Production backends MUST implement structured JSON logging (`structlog` / `pino`) with `trace_id` correlation, Sentry error tracking, and `/health` monitoring endpoints.

---

## 5. Multi-Agent Autonomous Pipeline (5 Phases)

### Phase 0 — Task Decomposition & Multi-Agent Orchestration
1. **Task Complexity Classification**:
   - Simple (Single agent): Surgical bugs, copy updates, styling fixes.
   - Medium (2 agents): Isolated feature addition (Frontend + Backend).
   - Complex (3+ agents): Full-stack SaaS, cross-platform mobile, major architectural redesigns.
2. **Specialized Multi-Agent Roles**:
   - **Architect Agent** (Claude Opus / Gemini Pro): Generates `SPEC.md`, data schemas, API contracts, and security boundaries.
   - **Builder Agent(s)** (Claude Sonnet / Gemini Flash): Implements features in isolated Git worktrees (`Workspace: "branch"`).
   - **QA Engineer Agent**: Writes and runs Playwright, Lighthouse, and Axe-Core tests concurrently with the build.
   - **Security Reviewer Agent** (Senior Staff Persona): Adversarial code review, OWASP audit, and supply chain inspection.
   - **DevOps Agent**: CI/CD pipeline, Vercel/Railway deployments, and SLO baseline verification.
3. **Inter-Agent Checkpoints**: Every agent writes architectural decisions into **MemPalace** before handoff. Conflicts are resolved by the Architect Agent with full specification context.

### Phase 1 — Blueprint & Architecture (GSD Spec Engine)
1. Ingest requirements; generate a `SPEC.md` specifying boundaries, data schemas, and edge cases.
2. Generate an interactive **Generative UI prototype** sandbox for visual features.
3. Require the agent to generate an **Interactive Implementation Plan** (`PLAN.md`) artifact first.
4. User reviews the clickable checklist in the artifact viewer before approving code generation.

### Phase 2 — Isolated Branch Build (Git Worktree & Ponytail Diffs)
1. Spawn a branch subagent (using `invoke_subagent` with `Workspace: "branch"`, creating dedicated Git worktree `feature/<slug>`).
2. Main branch stays 100% untouched until testing and PR review.
3. Apply **Ponytail minimal diffs** (`replace_file_content`).
4. Use `LangGraph` or `Antigravity SDK` for AI workflows; Motion Primitives / React Three Fiber / Skia for visuals.
5. Apply expand-contract database migrations; zero destructive schema alterations without rollback verification.

### Phase 3 — The Ralph Loop (Automated Self-Healing Audits)
1. **Automated E2E Testing**:
   - Web: Playwright headless Chrome (clicks interactive UI, catches uncaught exceptions & console errors, records video proof).
   - Mobile: Maestro flow runner (`maestro test .maestro/flows/chat.yaml`).
2. **AI Evals**: Run Promptfoo adversarial red-teaming cases.
3. **Lighthouse CI & CWV Gate**: Assert Performance ≥ 90, Accessibility ≥ 95 on mobile and desktop viewports.
4. **WCAG 2.2 AA Audit**: Run `axe-core` across all interactive routes; assert 0 violations.
5. **Visual Regression Multi-Viewport Diff**: Screenshot diff at 375px, 1024px, 1440px widths with `< 2%` pixel tolerance.
6. **Supply Chain Audit**: Run `pnpm audit` and generate CycloneDX `sbom.json`.
7. **The Ralph Self-Healing Loop**: If tests fail, autonomously diagnose the error log, apply a surgical patch, and re-test (up to 3 automated attempts) before escalating.

### Phase 3.5 — Principal Architect & Security Review
1. Spawn a review subagent with the persona: *"Senior Staff Security & Performance Architect"*.
2. Run **Strix** one-shot OWASP sandbox pentest to verify zero prompt injection, authorization flaws, or credential leaks.
3. Audit `git diff` for missing error boundaries, race conditions, memory leaks, and mobile responsiveness.
4. Verify strict CSP nonces, sliding-window rate limiting on auth routes, and zero PII leakage.

### Phase 4 — Clean Git, CodeRabbit Review & Preview Deploy
1. Format with Biome / Prettier.
2. Commit with conventional commit messages (`feat:`, `fix:`, `perf:`, `chore:`).
3. Push branch and open Pull Request via GitHub MCP with attached recordings & Lighthouse proof, plus automated **CodeRabbit** review (`.coderabbit.yaml`).
4. Trigger staging preview deployment (Vercel / Cloudflare / Expo EAS).
5. Update `CHANGELOG.md` following KeepAChangelog.
6. Generate a client-facing **Delivery Brief** (`handover.md`).
7. File high-signal architectural decisions (ADRs) into **MemPalace**.

---

## 6. Non-Negotiable Enterprise Guardrails (All Client Projects)

1. **Anti-Slop Multi-Palette & Typography Mandate:** All frontends must provide an integrated multi-theme engine (minimum 3–5 distinct palettes: e.g. Cyberpunk Matrix, Swiss Bauhaus, Avionics Amber, Oceanic Cobalt, Lockdown Crimson) with live switching. Forbid hardcoded arbitrary hex colors (`#7c3aed`, `#8b5cf6`, `brand-violet`, etc.) across all subpages, docs, login, and modals; all components must inherit active theme CSS variables (`useTheme()`). Frontends must import and enforce high-legibility enterprise typefaces (Inter + JetBrains Mono) with subpixel anti-aliasing (`-webkit-font-smoothing: antialiased`). Include 60fps canvas particle meshes and physics-based spring animations (`motion/react`).
2. **Real AI Subsystem & Prompt Injection Guardrail Mandate (Zero Mock Fakes):** Never stub requested AI agents or RAG with hardcoded string checks. Always implement real RAG (vector chunking & cosine similarity retrieval with OWASP/NIST citations), real supervised training/fine-tuning scripts with loss metrics, and pure-Python mathematical vector fallbacks to prevent Windows Application Control DLL load blocks. Enforce deterministic pre-flight scope containment (OWASP LLM01 / ASI01) across all AI copilots: refuse prompt injections, adversarial jailbreaks, system prompt leaks, credential probes, and off-topic queries before generative evaluation occurs. Allow optional custom LLM API keys with local storage persistence, falling back to built-in pure-Python grounded vector RAG when no external keys are present.
3. **Super-Pro Commercial Video & Sound Design Standard:** Commercial promotional videos must NEVER be static text slideshows or amateur AI morphs. They must showcase Hollywood-grade editing: velocity speed ramps (300% entry $\rightarrow$ 80% hero settle $\rightarrow$ 300% whip exit), match cuts, 2.5D/3D hardware mockups rendering live software interfaces, and full 5-track broadcast audio sound design: neural voiceover + driving score with -12dB sidechain ducking + 60Hz sub-bass impacts + rising whooshes + high-frequency UI Foley (-14 LUFS EBU R128 mastered).
4. **Native Mobile Export & Automated Release Packaging Standard:** Cross-platform mobile projects (Expo/React Native) must target both Android and iOS. Execute `npx expo prebuild` and generate native projects with auto-configured `local.properties` resolving the local Android SDK and JDK (`$JAVA_HOME`). Provide automated build scripts (`mobile/build_apk.bat` / `build_apk.ps1`) executing Gradle assemble, automatically moving the resulting `.apk` to `releases/` and `web/public/downloads/`, generating `LATEST_RELEASE.json` with cryptographic SHA-256 checksums and build metadata. Mobile screens must match selected theme palettes with instant touch responsiveness.
5. **Console Usability, Stacking Hierarchy & Reactive State Standard:** Headers containing dropdown menus (Theme Selectors, Notification Centers, Profile Menus) MUST be declared with `sticky top-0 z-40` and 100% opaque surface backgrounds (`backgroundColor: currentTheme.surface`), never allowing semi-transparent backdrop bleed-through or lower stacking contexts that allow content cards or tabs underneath to clip or overlap dropdown options. All dialog modals triggered from headers or navigation bars MUST be mounted directly to `document.body` via `createPortal(..., document.body)` with `z-[9999]` to escape parent `backdrop-filter` containing block constraints, preventing modals from becoming clipped or vertically shifted off-screen. Notification badges, approval counts, and alert pills must be driven by reactive state stores (`OperationsProvider`), synchronizing from N to 0 in real-time across both header dropdowns, sidebars, and data tables with zero dead clicks or stale counters. Operational dashboards must include an interactive User Guidance Tour with an explicit dismiss button (`✕`) saving state to `localStorage`. Provide a dedicated Enterprise Admin Center with emergency kill-switch controls, master token management, and organization RBAC.
6. **Transparent Commercial Pricing & End-to-End Dogfooding:** Every commercial product built MUST include a transparent, enterprise-grade Pricing experience (`#pricing` and `/pricing`) featuring an interactive Monthly/Annual billing toggle (with discount badges), realistic developer/team/enterprise tiers, feature comparison matrix, enterprise trust assurances (SLA, SOC2/HIPAA readiness), interactive contact modal, and FAQ accordion. Hero copy must be punchy, minimal, and modern for Gen-Z and enterprise buyers. Never invent future dates for standards (e.g. cite real "OWASP Top 10 for Agentic AI"). Before declaring any project complete, execute comprehensive Playwright E2E audits clicking through all buttons, navigation tabs, modal popups, notification dropdowns, and theme selectors to guarantee zero dead clicks, zero card overlaps, and zero console errors.
7. **B2B SaaS Quota Metering, Sybil Defense & Strict RBAC Isolation:** Every enterprise commercial application must enforce strict Role-Based Access Control (RBAC). Dedicated admin consoles (`/dashboard/admin`) MUST return an HTTP 403 Access Denied lockscreen to non-admin roles (Developers, Auditors, Viewers) rather than exposing controls. User governance must include active session logging with IP, device fingerprint, and 1-click "Terminate / Suspend" kill-switches to prevent account hijacking. Registration flows must enforce Anti-Sybil validation, blocking burner/disposable email domains (`tempmail.com`, `mailinator.com`, etc.) to prevent trial abuse. Monthly quota metering (e.g. 50,000 calls) must be prominently displayed in tenant sidebars with dynamic tier badges (`Starter Plan (Free)`, `★ SecOps Team`, `🛡️ Enterprise Defense`). When quotas are exceeded, surface fail-closed alerts with 1-click self-serve upgrade paths.
8. **Desktop Distribution & Direct PWA / Native Launcher Delivery:** Web applications must provide direct desktop installation mechanisms, including W3C PWA manifests (`manifest.json`) for chromeless app windows and 1-click OS-level launchers (`Launch-AppName-Desktop.bat`) placed in the repository root and downloadable from the web console.
9. **Supreme Master Admin Exclusivity, Persistent Auth Database & WebAPK Delivery Standard:**
   - The Enterprise Admin navigation entry in dashboard sidebars MUST be strictly hidden from all non-admin users (`currentUser.role !== 'SUPER_ADMIN'`). Non-admin users cannot self-elevate; only the authenticated Supreme Master Admin (`is_master_admin = 1`, default: `josuva732006@gmail.com` or configured via `$MASTER_ADMIN_EMAIL`) has permission to promote other users to administrative roles or modify permissions.
   - User identities, salted password hashes, active sessions, and tenant roles must be stored in a persistent database (SQLite/PostgreSQL) with hardware-bound session token tracking.
   - Every web deliverable must include both a Native Mobile APK and an installable Android WebAPK package (`web.apk`) stored in `releases/` and public download endpoints with SHA-256 cryptographic checksums.
10. **Clean Single-Line Navigation Spacing & Unified App Distribution Modal Mandate:**
   - Header navigation links (`Docs & API`, `About Us`, `Architecture`, `Simulator`, `Pricing`) MUST be styled with `whitespace-nowrap` to prevent awkward multi-line word wrapping and disjointed spacing across all responsive breakpoints.
   - Never clutter the navigation bar or hero CTA row with standalone `.apk` or `.bat` download buttons.
   - Consolidate all desktop and mobile downloads (Progressive Web App, Windows `.bat` Launcher, Android `web.apk`, and Android `mobile.apk`) into a single, cohesive `Desktop & Mobile App` modal triggered from header actions, ensuring a clean hero and uncluttered navbar.
11. **Bespoke Brand Identity & Automated Asset Generation Mandate:**
   - Every enterprise project built must automatically synthesize bespoke, project-specific visual identity assets (high-resolution SVG/PNG emblem, horizontal wordmark logo, square rounded app icon, and favicon) tailored specifically to the project's domain, theme palette, and naming.
   - Forbid generic placeholder icons (e.g. default generic Lucide shield/box) on primary brand touchpoints.
   - Brand assets must be systematically integrated across website headers, hero centerpieces, dashboard sidebars, PWA manifests, mobile icons, splash screens, and desktop launchers.
12. **Next-Generation Cinematic Commercial Video & Motion Standard:**
   - Commercial promotional videos must deliver high-fidelity broadcast production value:
     a) Full 3D canvas viewport rendering (Three.js / React Three Fiber / Remotion) showcasing photorealistic device mockups executing real software interfaces in real time.
     b) Multi-track Foley and electronic music sound design: dynamic sidechain audio ducking under professional neural voiceover, precision-synced interface whooshes, biometric audit scans, cryptographic confirmation chimes, and deep sub-bass impacts.
     c) Kinetic typography, split-screen terminal logs, velocity speed curves, and anamorphic lens flares.
     d) Export rendered video (`.mp4`, 1080p60 / 4K) to project root, web public directory (`/web/public/`), and embed within an interactive video showcase on the landing page with zero buffering.
13. **Viral Social Media Video & Narrative Tech Storytelling Standard:**
   - In addition to landscape commercials, every client deliverable must generate high-retention 9:16 Vertical video formats (1080x1920, 60fps) tailored for TikTok, Instagram Reels, and YouTube Shorts to maximize organic reach and views.
   - **Strict Platform Separation Mandate:** The public website landing page strictly embeds the **16:9 Landscape Broadcast Commercial** (`sentinelops_commercial.mp4`). Vertical 9:16 reels are strictly delivered as external social distribution assets (`releases/social/` and desktop) for publishing to TikTok, Instagram, and YouTube Shorts, and MUST NOT be embedded directly onto the website landing page.
   - Employ viral narrative structure: 0–3s dopamine hook ("An autonomous AI agent just tried to..."), 3–15s visual problem escalation (3D mobile zoom + terminal payload leaks), 15–24s deterministic guardrail climax, and 24–30s punchy brand CTA.
   - Enforce center-screen dynamic word-by-word karaoke captions with spring pop-ins (`scale: 1.18`) and vibrant keyword highlights (`#facc15` neon yellow / `#10b981` cyber emerald) synchronized with real millisecond word timestamps.
   - Master 5-track cinematic audio: professional neural voiceover, tension sub-drone, heartbeat impacts, laser gate alerts, and dynamic sidechain ducking (-14 LUFS EBU R128).
14. **Super-Design & Tactile Frontend Interaction Standard (The 15 Superpowers):**
   - Frontends must feel physical and alive using the full 15-skill stack: **Skills.sh** standards, **Emil Kowalski’s** spring physics (`stiffness: 400, damping: 30`), active tap depressions (`whileTap={{ scale: 0.97 }}`), layout morphing (`layoutId`), and zero dead clicks (<16ms feedback).
   - Enforce **Impeccable** mathematical 4px/8px optical rhythm and **Awesome Designs** deep contrast dark mode palettes.
   - Implement **Three.js (Image 23js)** photorealistic 3D hardware viewports and **GSAP** timeline choreography.
   - Integrate **Transitions.dev** View Transitions API for fluid page routing, and **Make Interfaces Feel Better** tactile micro-feedback.
   - Design **Better Icons** (bespoke geometric SVG marks, zero generic icon stubs).
   - Implement buttery smooth momentum scrolling via **Lenis** to eliminate clunky browser wheel jumps.
   - Integrate modern design-engineering craft from **React Bits** (decrypted text scrambles, spotlight border tracking, magnetic buttons) and **21st.dev** component patterns, staged with **Draftly**.
   - Enforce strict **Anti-AI-Slop Writing & No AI Slop**: forbid generic corporate marketing buzzwords ("unleash", "synergy", "in today's fast-paced world"); enforce direct, cynical, engineer-grade clarity.
15. **Omnichannel Authentication & 6-Digit Email OTP Verification Standard (Zero-Leak, Zero-Fake Mandate):**
   - **Dedicated Dual-Flow Onboarding Architecture (`/signup` vs `/login`)**:
     a) **New Users (`/signup`)**: Dedicated registration page collecting Full Name, Company Name, Work Email, and Password. Dispatches a single-use 6-digit cryptographic OTP to the user's real inbox (10m TTL, 60s countdown, rate-limited). User enters the 6-digit code to verify their identity before the tenant is committed to the database and automatically logged in.
     b) **Existing Users (`/login`)**: Dedicated sign-in page supporting instant Work Email + Password login, or passwordless 6-digit Email OTP login in 1 click.
     c) **Database Concurrency & WAL Isolation**: SQLite databases handling authentication and billing MUST enable `PRAGMA journal_mode=WAL` with `PRAGMA busy_timeout=30000`, and wrap every connection execution in `try ... finally: conn.close()` to guarantee zero `database is locked` operational errors under concurrent multi-user load.
   - **Zero Fake / Zero Mock Mandate**: Forbid simulated dev drawers, autofill testing buttons, cheesy demo shortcuts, or fake account chooser modals on the UI. Real users enter their email, receive their code in their real inbox via live SMTP, and manually enter the 6 digits. Never leak the OTP code over network JSON responses to the browser.
   - **Real Omnichannel SSO**: Provide standard, production-ready "Continue with Google" and "Continue with GitHub" OAuth buttons that redirect to official authorization endpoints (`accounts.google.com` and `github.com/login/oauth/authorize`), handled by dedicated OAuth callback routes (`/auth/callback`).
   - **Seamless Master Admin Exclusivity**: The Supreme Master Admin (`josuva732006@gmail.com`) logs in through the exact same standard login inputs as every other user (no separate "Master Login" tabs or demo badges). Super Admin role, enterprise tier, and fleet controls are resolved server-side based on verified identity.
16. **Enterprise Stripe Payment Gateway & Cryptographic Financial Ledger Standard:**
   - Dual-mode billing architecture: real Stripe API or deterministic cryptographic fallback simulator with instant checkout URL generation (`cs_test_...`) and zero real card costs.
   - Automated tenant provisioning: purchases atomically upgrade tenant tiers (`TEAM` / `ENTERPRISE`) and expand quota to 1,000,000+ monthly calls in persistent SQLite storage.
   - Immutable SHA-256 financial receipt ledger: every checkout writes a cryptographically hashed block to the tamper-evident audit ledger with transaction ID, amount, timestamp, and previous block hash.
   - Dedicated Billing & Receipts interface with live quota metering bar, plan upgrade CTAs, and immutable receipt history with 1-click hash copy.
17. **Production Cloud Deployment Architecture (Vercel Edge & Railway Persistent Engine):**
   - Frontend deploys to **Vercel** with hardened security headers (`X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`), video asset caching headers (`max-age=31536000`), and API reverse proxy rewrites (`/api/gateway/:path*` -> Railway backend).
   - Backend deploys to **Railway** via Nixpacks with `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, health check polling (`/health`), and persistent SQLite volume storage.
   - Comprehensive `.env.example` templates documenting Stripe, SMTP, and cloud gateway secrets.
18. **Monorepo-First Multi-Package Architecture Standard:**
   - Projects with both web and mobile applications MUST adopt Turborepo + pnpm workspaces.
   - Shared design system (`packages/ui`), database access layer (`packages/database`), shared API schemas (`packages/api`), and tooling configs (`packages/config`) MUST be extracted as reusable internal workspace packages.
   - Topological builds declared in `turbo.json` with remote caching enabled for CI.
19. **Core Web Vitals & Lighthouse CI Performance Gate:**
   - All production web applications MUST achieve: LCP < 2.5s, INP < 200ms, and CLS < 0.1.
   - Pull requests must pass automated Lighthouse CI gates: Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 90, SEO ≥ 90.
   - Enforce `next/image` with `priority` for above-the-fold heroes, `next/font` for zero layout shift typography, and `@next/bundle-analyzer` to maintain initial client JavaScript bundles strictly below 100 kB (gzipped).
20. **WCAG 2.2 AA Accessibility Compliance Mandate:**
   - All interactive touch targets MUST measure at least **24×24 CSS pixels** (WCAG 2.5.8).
   - Keyboard focus rings must never be obscured by sticky headers, footers, or floating action buttons (WCAG 2.4.11).
   - Dragging interactions must provide single-pointer click/touch alternatives (WCAG 2.5.7).
   - Text color contrast must achieve at least **4.5:1** for regular text and **3:1** for large text (18pt+).
   - Form inputs must possess explicit programmatic `<label>` elements; dynamic alerts must declare `aria-live="polite"`.
   - Automated `@axe-core/playwright` CI scans MUST report zero critical or serious accessibility violations prior to merge.
21. **Observability, Structured Logging & SLO Framework:**
   - Production backends MUST emit single-line structured JSON logs with auto-injected `trace_id` and `span_id` (W3C OpenTelemetry propagation).
   - Error tracking (Sentry) must capture unhandled exceptions with full stack traces on backend and sourcemapped replays on frontend.
   - Implement an unauthenticated `/health` endpoint returning detailed subsystem statuses (database WAL mode, SMTP connectivity, ledger hash).
   - Define user-centric SLO targets (99.9% availability, p95 latency < 500ms) with multi-window error budget burn-rate alerting.
22. **Database Migration & Zero-Downtime Schema Evolution:**
   - Schema modifications MUST follow the expand-contract pattern: add columns/tables $\rightarrow$ dual-write $\rightarrow$ backfill $\rightarrow$ contract old columns.
   - SQLite databases MUST enable `PRAGMA journal_mode=WAL` and `PRAGMA busy_timeout=30000`, enclosing all connections in `try ... finally: conn.close()`.
   - PostgreSQL projects must integrate migration tooling (Prisma Migrate / Atlas / Flyway) with automated schema-drift detection in CI.
   - Destructive migrations (DROP COLUMN/TABLE) without verified rollback scripts are strictly forbidden.
23. **API Versioning, Rate Limiting & Real-Time Patterns:**
   - REST APIs MUST enforce URL path versioning (`/api/v1/resource`).
   - Authentication endpoints MUST enforce sliding-window rate limiting (max 5 attempts per IP per 15 minutes) with HTTP 429 and `Retry-After` headers.
   - Real-time updates must leverage Server-Sent Events (SSE) for unidirectional streams (LLM generation, live audit feeds) or WebSockets for bidirectional collaboration.
   - Employ multi-tier caching: in-memory LRU $\rightarrow$ distributed Redis $\rightarrow$ CDN edge `stale-while-revalidate`.
24. **Cross-Platform Mobile (iOS + Android) & OTA Update Standard:**
   - Mobile applications MUST target both iOS and Android platforms via Expo SDK 52+ with the New Architecture enabled (`newArchEnabled: true`).
   - Native animations MUST execute on the native thread via `react-native-reanimated` and `react-native-gesture-handler`.
   - Over-The-Air (EAS Update) deployments are strictly permitted for bug fixes and UI updates; core feature changes require full binary resubmission.
   - Deep linking MUST configure both `apple-app-site-association` (iOS) and `assetlinks.json` (Android) hosted at `/.well-known/`.
25. **Supply Chain Security & Software Bill of Materials (SBOM):**
   - Every production release MUST generate a standardized CycloneDX JSON SBOM (`releases/sbom.json`).
   - CI builds MUST execute `pnpm install --frozen-lockfile` to prevent lockfile poisoning.
   - Run `pnpm audit --audit-level=high` in CI; resolve any vulnerability possessing a public exploit (EPSS > 0.1) and confirmed reachability before release.
   - Release binaries (APK, WebAPK, Windows launcher) MUST be accompanied by cryptographic SHA-256 manifests (`LATEST_RELEASE.json`).
