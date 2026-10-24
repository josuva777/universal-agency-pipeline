# Agency Workflow Rules & Enterprise Guardrails

## 1. Crucial Rule: Token Guardrails (Don't Load Everything at Once)
Every active MCP server injects its tool definitions into the prompt on every message:
- **Always-On Global Core** (`~/.gemini/config/mcp_config.json`):
  - **MemPalace**: ~170 tokens for local verbatim all-session memory
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

## 2. Security & Zero-Leak Discipline
- **NEVER** commit or stage `.env`, `.env.local`, API tokens, private keys, or raw connection strings.
- Always use environment variable expansion (`${VAR}`) or OS-level environment variables.
- Before committing, verify git status is clean of private data.

---

## 3. High-Velocity Quality Control & Tooling
- **Formatting & Linting**: Use **Biome** (`npx @biomejs/biome check --write .`) for ultra-fast <50ms linting and formatting. Fall back to Prettier if Biome is unconfigured.
- **Database Isolation**: Always create an isolated Supabase Preview Branch when altering database schemas.
- **Offline / Zero-Cost Mocking**: Use Mock Service Worker (MSW) for external APIs during development to avoid rate limits and costs.

---

## 4. 4-Phase Agency Pipeline Discipline (Default Behavior)
> **Always-On Default**: Whenever the user asks to build, create, or implement a feature, ALWAYS adopt this 4-phase pipeline by default. The user never needs to say "using agency pipeline" explicitly.

### Phase 1 — Blueprint & Architecture (GSD Spec Engine)
1. Ingest requirements; generate a `SPEC.md` specifying boundaries, data schemas, and edge cases.
2. Generate an interactive **Generative UI prototype** sandbox for visual features.
3. Require the agent to generate an **Interactive Implementation Plan** (`PLAN.md`) artifact first.
4. User reviews the clickable checklist in the artifact viewer before approving code generation.

### Phase 2 — Isolated Branch Build (Git Worktree & Ponytail Diffs)
1. Spawn a branch subagent (using `invoke_subagent` with `Workspace: "branch"`, or `git worktree add ../feature-<slug> -b feature/<slug>`).
2. Main branch stays 100% untouched until testing and PR review.
3. Apply **Ponytail minimal diffs** (`replace_file_content`).
4. Use `LangGraph` or `Antigravity SDK` for AI workflows; Motion Primitives / React Three Fiber / Skia for visuals.

### Phase 3 — The Ralph Loop (Automated Self-Healing Audits)
1. **Automated E2E Testing**:
   - Web: Playwright headless Chrome (clicks interactive UI, catches uncaught exceptions & console errors, records video proof).
   - Mobile: Maestro flow runner (`maestro test .maestro/flows/chat.yaml`).
2. **AI Evals**: Run Promptfoo adversarial red-teaming cases.
3. **The Ralph Self-Healing Loop**: If tests fail, autonomously diagnose the error log, apply a surgical patch, and re-test (up to 3 automated attempts) before escalating.
4. Target **Google Lighthouse** scores: Performance 90+, Accessibility 95+.

### Phase 3.5 — Principal Architect & Security Review
1. Spawn a review subagent with the persona: *"Senior Staff Security & Performance Architect"*.
2. Run **Strix** one-shot OWASP sandbox pentest to verify zero prompt injection, authorization flaws, or credential leaks.
3. Audit `git diff` for missing error boundaries, race conditions, memory leaks, and mobile responsiveness.

### Phase 4 — Clean Git, CodeRabbit Review & Preview Deploy
1. Format with Biome / Prettier.
2. Commit with conventional commit messages (`feat:`, `fix:`, `perf:`, `chore:`).
3. Push branch and open Pull Request via GitHub MCP with attached recordings & Lighthouse proof, plus automated **CodeRabbit** review (`.coderabbit.yaml`).
4. Trigger staging preview deployment (Vercel / Cloudflare / Expo EAS).
5. Update `CHANGELOG.md` following KeepAChangelog.
6. Generate a client-facing **Delivery Brief** (`handover.md`).
7. File high-signal architectural decisions (ADRs) into **MemPalace**.

---

## 5. Non-Negotiable Enterprise Guardrails (All Client Projects)
1. **Anti-Slop Multi-Palette & Typography Mandate:** All frontends must provide an integrated multi-theme engine (minimum 3–5 distinct palettes: e.g. Cyberpunk Matrix, Swiss Bauhaus, Avionics Amber, Oceanic Cobalt, Lockdown Crimson) with live switching. Forbid hardcoded arbitrary hex colors (`#7c3aed`, `#8b5cf6`, `brand-violet`, etc.) across all subpages, docs, login, and modals; all components must inherit active theme CSS variables (`useTheme()`). Frontends must import and enforce high-legibility enterprise typefaces (Inter + JetBrains Mono) with subpixel anti-aliasing (`-webkit-font-smoothing: antialiased`). Include 60fps canvas particle meshes and physics-based spring animations (`motion/react`).
2. **Real AI Subsystem & Prompt Injection Guardrail Mandate (Zero Mock Fakes):** Never stub requested AI agents or RAG with hardcoded string checks. Always implement real RAG (vector chunking & cosine similarity retrieval with OWASP/NIST citations), real supervised training/fine-tuning scripts with loss metrics, and pure-Python mathematical vector fallbacks to prevent Windows Application Control DLL load blocks. Enforce deterministic pre-flight scope containment (OWASP LLM01 / ASI01) across all AI copilots: refuse prompt injections, adversarial jailbreaks, system prompt leaks, credential probes, and off-topic queries before generative evaluation occurs. Allow optional custom LLM API keys with local storage persistence, falling back to built-in pure-Python grounded vector RAG when no external keys are present.
3. **Product-Demonstration Commercial Video & Audio Standard:** Commercial videos must never be static text slideshows. They must showcase 2.5D device mockups (laptops, smartphones) rendering the actual web console and mobile interfaces in action, animated packet interception flows, and broadcast audio sound design: full-length electronic soundtrack + precision-timed Foley SFX (alarm warbles, UI whooshes, approval chimes, sub-bass impacts).
4. **Native Mobile Export & Automated APK Release Packaging Standard:** Cross-platform mobile projects (Expo/React Native) must execute `npx expo prebuild` and generate native `android/` projects with auto-configured `local.properties` pointing to the local Android SDK and resolve local JDK 21 (`C:\Users\ELCOT\jdk-21.0.6+7`). Always provide an automated build script (`mobile/build_apk.bat` / `build_apk.ps1`) that executes Gradle assemble, automatically moves the resulting `.apk` to a top-level `releases/` directory and `web/public/downloads/`, and generates `LATEST_RELEASE.json` with cryptographic SHA-256 checksums and build metadata. Store and track release assets in the repository. Mobile screens must match the selected theme palette and maintain instant touch responsiveness.
5. **Console Usability, Stacking Hierarchy & Reactive State Standard:** Headers containing dropdown menus (Theme Selectors, Notification Centers, Profile Menus) MUST be declared with `sticky top-0 z-40` and 100% opaque surface backgrounds (`backgroundColor: currentTheme.surface`), never allowing semi-transparent backdrop bleed-through or lower stacking contexts that allow content cards or tabs underneath to clip or overlap dropdown options. All dialog modals triggered from headers or navigation bars MUST be mounted directly to `document.body` via `createPortal(..., document.body)` with `z-[9999]` to escape parent `backdrop-filter` containing block constraints, preventing modals from becoming clipped or vertically shifted off-screen. Notification badges, approval counts, and alert pills must be driven by reactive state stores (`OperationsProvider`), synchronizing from N to 0 in real-time across both header dropdowns, sidebars, and data tables with zero dead clicks or stale counters. Operational dashboards must include an interactive User Guidance Tour with an explicit dismiss button (`✕`) saving state to `localStorage`. Provide a dedicated Enterprise Admin Center with emergency kill-switch controls, master token management, and organization RBAC.
6. **Transparent Commercial Pricing & End-to-End Dogfooding:** Every commercial product built MUST include a transparent, enterprise-grade Pricing experience (`#pricing` and `/pricing`) featuring an interactive Monthly/Annual billing toggle (with discount badges), realistic developer/team/enterprise tiers, feature comparison matrix, enterprise trust assurances (SLA, SOC2/HIPAA readiness), interactive contact modal, and FAQ accordion. Hero copy must be punchy, minimal, and modern for Gen-Z and enterprise buyers. Never invent future dates for standards (e.g. avoid forward-dating to "OWASP (2026)"); always cite real, established industry frameworks (e.g. "OWASP Top 10 for Agentic AI"). Before declaring any project complete, execute comprehensive Playwright E2E audits clicking through all buttons, navigation tabs, modal popups, notification dropdowns, and theme selectors to guarantee zero dead clicks, zero card overlaps, and zero console errors.


7. **B2B SaaS Quota Metering, Sybil Defense & Strict RBAC Isolation:** Every enterprise commercial application must enforce strict Role-Based Access Control (RBAC). Dedicated admin consoles (`/dashboard/admin`) MUST return an HTTP 403 Access Denied lockscreen to non-admin roles (Developers, Auditors, Viewers) rather than exposing controls. User governance must include active session logging with IP, device fingerprint, and 1-click "Terminate / Suspend" kill-switches to prevent account hijacking. Registration flows must enforce Anti-Sybil validation, blocking burner/disposable email domains (`tempmail.com`, `mailinator.com`, etc.) to prevent trial abuse. Monthly quota metering (e.g. 50,000 calls) must be prominently displayed in tenant sidebars with dynamic tier badges (`Starter Plan (Free)`, `★ SecOps Team`, `🛡️ Enterprise Defense`). When quotas are exceeded, surface fail-closed alerts with 1-click self-serve upgrade paths.
8. **Desktop Distribution & Direct PWA / Native Launcher Delivery:** Web applications must provide direct desktop installation mechanisms, including W3C PWA manifests (`manifest.json`) for chromeless app windows and 1-click OS-level launchers (`Launch-AppName-Desktop.bat`) placed in the repository root and downloadable from the web console.
9. **Supreme Master Admin Exclusivity, Persistent Auth Database & WebAPK Delivery Standard:**
   - The Enterprise Admin navigation entry in dashboard sidebars MUST be strictly hidden from all non-admin users (`currentUser.role !== 'SUPER_ADMIN'`). Non-admin users cannot self-elevate; only the authenticated Supreme Master Admin (`is_master_admin = 1`) has permission to promote other users to administrative roles or modify permissions.
   - User identities, salted password hashes, active sessions, and tenant roles must be stored in a persistent database (SQLite/PostgreSQL) with hardware-bound session token tracking.
   - Every web deliverable must include both a Native Mobile APK and an installable Android WebAPK package (`web.apk`) stored in `releases/` and public download endpoints with SHA-256 cryptographic checksums.
10. **Clean Single-Line Navigation Spacing & Unified App Distribution Modal Mandate:**
   - Header navigation links (`Docs & API`, `About Us`, `Architecture`, `Simulator`, `Pricing`) MUST be styled with `whitespace-nowrap` to prevent awkward multi-line word wrapping and disjointed spacing across all responsive breakpoints.
   - Never clutter the navigation bar or hero CTA row with standalone `.apk` or `.bat` download buttons.
   - Consolidate all desktop and mobile downloads (Progressive Web App, Windows `.bat` Launcher, Android `web.apk`, and Android `mobile.apk`) into a single, cohesive `Desktop & Mobile App` modal triggered from header actions, ensuring a clean hero and uncluttered navbar.
11. **Bespoke Brand Identity & Automated Asset Generation Mandate:**
   - Every enterprise project built must automatically synthesize bespoke, project-specific visual identity assets (high-resolution SVG/PNG emblem, horizontal wordmark logo, square rounded app icon, and favicon) tailored specifically to the project's domain, theme palette, and naming.
   - Forbid generic placeholder icons (e.g. default generic Lucide shield/box) on primary brand touchpoints.
   - Brand assets must be systematically integrated across:
     a) Website navigation header and mobile header (`Navbar.tsx`, `layout.tsx`).
     b) Landing page Hero centerpiece or emblem showcase (`page.tsx`).
     c) Dashboard sidebar header and user profile (`dashboard/layout.tsx`).
     d) PWA manifest, favicons, and touch icons (`manifest.json`, `favicon.ico`, `icon.png`).
     e) Mobile application icon and splash assets (`mobile/assets/icon.png`, `adaptive-icon.png`, Android `res/mipmap`).
     f) Desktop launchers and app installation modals.
   - When the user supplies a custom logo sheet or brand image, the agent must autonomously crop, optimize (lossless bicubic / vector conversion), and propagate the assets to all web, mobile, and desktop touchpoints, immediately updating and re-signing APK releases.
12. **Next-Generation Cinematic Commercial Video & Motion Standard:**
   - Commercial promotional videos must deliver high-fidelity broadcast production value:
     a) Full 3D canvas viewport rendering (Three.js / React Three Fiber / Remotion) showcasing photorealistic device mockups (ultrabook laptop, modern smartphone) executing real software interfaces in real-time.
     b) Multi-track Foley and electronic music sound design: dynamic sidechain audio ducking under professional neural voiceover, precision-synced interface whooshes, biometric audit scans, cryptographic confirmation chimes, and deep sub-bass impacts.
     c) Kinetic typography and high-velocity split-screen terminal logs illustrating intercepted malicious payloads and deterministic policy decisions.
     d) Export rendered video (`.mp4`, 1080p60) to project root, web public directory (`/web/public/`), and embed within an interactive video showcase on the landing page with zero buffering.
13. **Viral Social Media Video & Narrative Tech Storytelling Standard:**
   - In addition to landscape commercials, every client deliverable must generate high-retention 9:16 Vertical video formats (1080x1920, 60fps) tailored for TikTok, Instagram Reels, and YouTube Shorts to maximize organic reach and views.
   - Employ viral narrative structure: 0–3s dopamine hook ("An autonomous AI agent just tried to..."), 3–15s visual problem escalation (3D mobile zoom + terminal payload leaks), 15–24s deterministic guardrail climax, and 24–30s punchy brand CTA.
   - Enforce center-screen dynamic word-by-word karaoke captions with spring pop-ins (`scale: 1.18`) and vibrant keyword highlights (`#facc15` neon yellow / `#10b981` cyber emerald) synchronized with real millisecond word timestamps.
   - Master 5-track cinematic audio: professional neural voiceover, tension sub-drone, heartbeat impacts, laser gate alerts, and dynamic sidechain ducking (-14 LUFS EBU R128).
14. **Super-Design & Tactile Frontend Interaction Standard:**
   - Frontends must feel physical and alive using Emil Kowalski's interaction laws: spring physics (`stiffness: 400, damping: 30`) over linear transitions, active tap depressions (`whileTap={{ scale: 0.97 }}`), layout morphing (`layoutId`), and zero dead clicks (<16ms feedback).
   - Implement buttery smooth momentum scrolling via Lenis to eliminate clunky browser wheel jumps.
   - Integrate modern design-engineering component craft (React Bits & 21st.dev): decrypted text scrambles, spotlight border tracking, and subtle 1px animated gradient borders on critical threat cards.
   - Enforce strict Anti-AI-Slop writing: forbid generic corporate marketing buzzwords ("unleash", "synergy", "in today's fast-paced world"); enforce direct, cynical, engineer-grade clarity.
