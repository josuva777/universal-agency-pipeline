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
