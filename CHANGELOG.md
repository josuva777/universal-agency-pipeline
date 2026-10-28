# Changelog

All notable changes to the **Universal Agency Pipeline** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2026-10-28

### Added
- **AI-Native Generative Video Director (`skills/creative-studio/scripts/generate_ai_video.py`) (Dept 10)**: Claude/Runway/ElevenLabs generative video directing pipeline with 5-scene cinematic storyboard generation, millisecond Whisper word-level subtitles sync, programmatic Remotion TSX compilation (16:9 Landscape & 9:16 Vertical), and 5-track audio design.
- **Real-Time Multiplayer Collaboration Engine (`packages/collab`) (Dept 11)**: Yjs CRDT shared document provider, ephemeral awareness presence manager (<20ms latency), and multiplayer cursor tracking.
- **Production Vector DB & Hybrid RAG (`packages/database/src/vector.ts`) (Dept 12)**: pgvector HNSW index schema, cosine similarity calculations, Reciprocal Rank Fusion (RRF), and full-text BM25 search.
- **Tauri 2.0 Native Desktop Architecture (`apps/desktop`) (Dept 13)**: Ultra-lightweight ~600KB native OS desktop application with Rust backend, system tray integration, window bounds control, and native OS notifications.
- **Browser-Native WebGPU Inference Engine (`packages/ui/src/WebLLMInference.tsx`) (Dept 14)**: WebGPU in-browser offline AI copilot with `useWebGPUInference` hook executing Llama 3.1 with zero server costs and zero data transmission.
- **Global Edge Computing & Hono Router (`packages/api/src/edge-hono.ts`) (Dept 15)**: Sub-millisecond cold start edge router deployable on Cloudflare Workers and Vercel Edge with W3C OpenTelemetry tracing.
- **Complete Suite of Masterpiece Web Pages (`apps/web`)**:
  - `app/layout.tsx`: OKLCH multi-theme engine wrapper (`ThemeProvider`) across 5 dynamic palettes.
  - `app/page.tsx`: Tier-1 public landing page with Sticky Navbar, 3D Hero, in-browser WebGPU sandbox, Architecture Grid, Pricing Table, and FAQ Accordion.
  - `app/login/page.tsx`: Omnichannel login supporting Work Email + Password or 6-digit cryptographic Email OTP.
  - `app/signup/page.tsx`: Anti-sybil registration with disposable domain filtering and 6-digit verification code delivery.
  - `app/dashboard/page.tsx`: Live tenant operations console with sliding-window quota meter, reactive notification counters (N $\rightarrow$ 0), and active session kill-switch.
  - `app/dashboard/admin/page.tsx`: Supreme Master Admin Center strictly restricted to `josuva732006@gmail.com` with HTTP 403 lockscreen.
- **Anti-Slop Zero-Mistake Scaffolder Engine (`pipeline/cli.py` & `skills/agency-scaffold/SKILL.md`)**: Intelligent domain synthesis automatically tailoring project branding, palette mapping, and layout copy upon scaffolding, forbidding generic AI placeholders.

## [2.2.0] - 2026-10-28

### Added
- **Hollywood 3D Device Mockup Asset Generator (`skills/creative-studio/scripts/render_device_mockups.py`)**: Procedural studio device mockup generator supporting iPhone 16 Pro, MacBook Pro 16", and Apple Studio Display across 3 themes (Cyber Metallic, Titanium Blue, Clay Matte) with high-res SVG vectors and an interactive Three.js 3D WebGL canvas viewer with orbit controls and canvas export.
- **Enterprise OpenTelemetry Distributed Tracing Middleware (`templates/monorepo-saas/packages/api/src/tracing.ts`)**: W3C TraceContext compliant distributed tracing engine for Next.js App Router and Node APIs with zero-dependency fallback, automatic `x-trace-id` / `x-span-id` propagation, exception recording, and granular sub-segment tracing.
- **Automated Pre-Commit Security & Quality Hooks (`pipeline/cli.py`)**: Automated installation of pre-commit hooks executing Zero-Trust secret scanning and Biome formatting before every commit, preventing credential leaks and format regressions.
- **Scaffolder & Test Suite Enhancements (`tests/test_mockup_generator.py`, `tests/test_scaffolder.py`, `tests/test_scaffold_agent.py`)**: Added dedicated unit test suites for 3D mockup generator and pre-commit hooks, with in-process agent execution tests passing 20/20.

## [2.1.0] - 2026-10-26

### Added
- **Automated Adversarial AI Red-Teaming Suite (`tests/promptfoo.yaml`)**: Added 50+ battle-tested adversarial attack assertions mapping directly to OWASP Top 10 for LLMs (LLM01-LLM10), including prompt injection, jailbreaking, PII extraction, credential leaks, and harmful content prevention.
- **Pre-Deploy Security Skill Upgrade (`skills/pre-deploy-security`)**: Updated security scanning procedure to execute Promptfoo evals alongside Strix pentesting before opening final PRs.
- **Automated Semantic Release & GitHub Release Publisher (`.github/workflows/release.yml`)**: GitHub Actions workflow that automatically publishes releases on tag push (`v*.*.*`), compiles release notes from `CHANGELOG.md`, generates CycloneDX SBOM (`sbom.json`), computes cryptographic SHA-256 checksums (`LATEST_RELEASE.json`), and uploads release assets.
- **MemPalace Architectural Memory Seeding (`mempalace.yaml` & `entities.json`)**: Pre-indexed memory wing featuring 7 architectural rooms (`enterprise_guardrails`, `architecture_and_monorepo`, `security_and_auth`, `creative_studio_video`, `observability_and_performance`, `skills_and_tooling`, `adrs_and_decisions`) with zero-token recall of pipeline specifications.
- **Interactive Project Scaffolder CLI (`pipeline/cli.py`)**: One-command project creation CLI that scaffolds any of the 4 enterprise templates, injects `.agents/` workspace rules, configures `.env` with master admin (`josuva732006@gmail.com`), seeds MemPalace memory, and initializes clean Git.
- **One-Shot Workspace Scaffolder Skill (`skills/agency-scaffold`)**: Enhanced skill with Mode A (one-shot creation from user idea $\rightarrow$ automatic template classification $\rightarrow$ scaffolding $\rightarrow$ Phase 1 Spec Engine) and Mode B (in-situ activation for existing repos).

## [2.0.0] - 2026-10-26

### Added
- **Master AGENTS.md v2.0 Architecture**: Expanded from 17 to 25 Non-Negotiable Enterprise Guardrails across 6 comprehensive sections, including multi-agent task decomposition (Phase 0), monorepo-first architecture, Core Web Vitals, and WCAG 2.2 AA accessibility mandates.
- **Production Observability Skill (`skills/observability`)**: Standardized structured JSON logging (`structlog` / `pino`), W3C OpenTelemetry distributed tracing, Sentry error tracking, `/health` endpoint diagnostics, and multi-window SLO error budget burn-rate alerting.
- **Performance Guardian Skill (`skills/performance-guardian`)**: Enforces Core Web Vitals targets (LCP < 2.5s, INP < 200ms, CLS < 0.1), Lighthouse CI gates (≥90 across all categories), bundle size budgets (<100 kB gzipped), and Partial Pre-Rendering (PPR).
- **Accessibility Compliance Skill (`skills/accessibility-audit`)**: Mandates WCAG 2.2 AA compliance via automated `@axe-core/playwright` scans (0 violations allowed), minimum 24×24px touch targets, focus obscuration prevention, and screen reader live regions (`aria-live="polite"`).
- **Supply Chain Security Skill (`skills/supply-chain-security`)**: Automated CycloneDX SBOM generation (`releases/sbom.json`), frozen lockfile enforcement, strict nonce-based CSP headers, and sliding-window rate limiting.
- **Restored Super Design Motion Skill (`skills/super-design-motion`)**: Integrated 15 curated design engineering superpowers directly into pipeline skills to prevent installation clobbering.
- **Enterprise Monorepo SaaS Starter (`templates/monorepo-saas`)**: Full Turborepo + pnpm workspace starter featuring Next.js 15 App Router (`apps/web`), Expo SDK 52 New Architecture (`apps/mobile`), shared design system (`packages/ui`), database layer (`packages/database`), and type-safe API schemas (`packages/api`).
- **Automated Verification Suites**: Added local Lighthouse CI runner (`tests/test_lighthouse.js`), axe-core accessibility suite (`tests/test_accessibility.spec.ts`), and multi-viewport visual regression tests (`tests/test_visual_regression.spec.ts`).

### Changed
- **Creative Studio Super-Pro Video Standard**: Upgraded `skills/creative-studio` with Hollywood-grade editing techniques: velocity speed ramps (300% entry $\rightarrow$ 80% hero $\rightarrow$ 300% exit), match cuts, 5-track cinematic sound design (-14 LUFS EBU R128), spring-pop karaoke typography, and 3D device mockups.
- **Merge-Safe Installation (`setup.ps1` / `setup.sh`)**: Modified setup scripts to copy skill directories safely without destroying existing user-added skills.
- **Root Environment Specification (`.env.example`)**: Added master environment template covering global MCP servers, cloud deployment secrets, SMTP, Stripe, and Sentry configurations.

## [1.0.0] - 2026-10-21

### Added
- **Mobile Starter Icon Assets**: Generated valid Expo launcher icon and adaptive icon assets in `templates/mobile-agent-app/assets/` to satisfy Metro bundler requirements.
- **Full-Stack Styling & Tooling**: Configured `tailwind.config.ts`, `postcss.config.mjs`, `globals.css`, and `biome.json` with ignored build directories (`.next`, `node_modules`) in `templates/fullstack-agent-app`.
- **Automatic Pyproject Configuration**: Agent builder scaffolder now automatically generates `pyproject.toml` with `pythonpath = ["."]` in all scaffolded agents, allowing zero-configuration `pytest` runs.
- **Stock B-Roll Clip Schema**: Added `BrollClip` interface and `brollClips` prop support to `templates/creative-agent-studio/video/src/types.ts` and `Commercial.tsx`.

### Changed
- **RAG Negative Refusal Guardrails**: Upgraded Hybrid RAG agent template with sentence-aware chunking preserving sentence boundaries and a strict negative refusal gate (`grounded=False`, `confidence=0.0`) when no relevant sentences match the query.
- **Mobile AI Protocol Support**: Enhanced `templates/mobile-agent-app/app/(tabs)/chat.tsx` with `parseDataStream` to seamlessly handle Vercel AI SDK text streams (`0:"..."`), structured JSON, and raw text replies.
- **Rate Limiting Security Priority**: Inverted authentication and rate-limiting order in `templates/fullstack-agent-app/app/api/chat/route.ts` so sliding-window IP rate limiting evaluates prior to bearer token verification, protecting auth services against Denial-of-Service resource exhaustion.
- **Maestro Flow Sync**: Updated `.maestro/flows/chat.yaml` to reference explicit `testID`s (`chat-input`, `send-button`) and verified UI assertions.

### Fixed
- **Mobile Peer Dependency**: Added `"react-native-svg": "^15.8.0"` to `templates/mobile-agent-app/package.json` to prevent crashes when rendering Lucide vector icons.
- **Creative Studio Non-Render Mode**: Added `render_video: bool = False` parameter to `run_creative_pipeline` in `templates/creative-agent-studio/agents/orchestrator.py` to allow orchestrator execution in headless/audio-only environments.
