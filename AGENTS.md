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

### Phase 1 — Blueprint & Architecture
1. Ingest requirements; generate an interactive **Generative UI prototype** sandbox for visual features.
2. Require the agent to generate an **Interactive Implementation Plan** artifact first.
3. User reviews the clickable checklist in the artifact viewer before approving code generation.

### Phase 2 — Isolated Branch Build
1. Spawn a branch subagent (using `invoke_subagent` with `Workspace: "branch"`, creating a dedicated Git worktree `feature/<slug>`).
2. Main branch stays 100% untouched until testing and PR review.
3. Use `LangGraph` or `Antigravity SDK` for AI workflows; Motion Primitives / React Three Fiber for visuals.

### Phase 3 — Automated Visual, Unit & Performance Audits
1. Invoke the `/browser` subagent with Playwright headless Chrome:
   - Click through interactive and 3D UI
   - Catch console errors and uncaught exceptions
   - Capture video recordings and screenshots
2. Run **Visual Regression** (desktop & mobile viewport diffs).
3. Target **Google Lighthouse** scores: Performance 90+, Accessibility 95+.
4. **Self-Healing Loop**: If tests fail, autonomously diagnose, patch, and re-test (up to 2 attempts) before escalating.

### Phase 3.5 — Principal Architect Review
- Spawn a review subagent with the persona: *"Senior Staff Security & Performance Architect"*.
- Audit the `git diff` for missing error handlers, race conditions, memory leaks, and mobile responsiveness.

### Phase 4 — Clean Git, Preview Deploy & Client Handover
1. Format with Biome / Prettier.
2. Commit with conventional commit messages (`feat:`, `fix:`, `perf:`, `chore:`).
3. Push branch and open Pull Request via GitHub MCP with attached recordings & Lighthouse proof.
4. Trigger staging preview deployment (Vercel / Cloudflare / Expo EAS).
5. Update `CHANGELOG.md` following KeepAChangelog.
6. Generate a client-facing **Delivery Brief** (`handover.md`).
7. File high-signal architectural decisions (ADRs) into **MemPalace**.
