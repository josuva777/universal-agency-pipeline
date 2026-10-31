---
name: agency-scaffold
description: >-
  Scaffolds a new project folder with the ultimate agency workflow.
  Creates .agents/ directory with workspace MCPs (Playwright/Maestro + Supabase + Vercel/Cloudflare),
  Biome/Prettier auto-formatting hooks, enterprise AGENTS.md rules, and CHANGELOG.md.
  Trigger phrases: "scaffold workspace", "setup project", "init agents", "add workspace config", "setup agents folder", "uap create".
---

# Universal Agency Workspace Scaffolder

This skill handles both **one-shot project generation from an idea** and **in-situ workspace activation** for existing folders.

---

## Operating Modes

### Mode A: One-Shot New Project Generation from Idea
**Triggers**: `"scaffold workspace [idea]"`, `"uap create [idea]"`, `"scaffold project [idea]"`
*(e.g., "scaffold workspace modern AI telehealth platform", "uap create mobile fintech wallet")*

When the user gives an idea or asks to scaffold a new project:

#### 1. Automatic Architecture & Template Selection
Analyze the user's idea and select the optimal starter template:
- **`monorepo-saas` (Default Recommended)**: For fullstack SaaS, web + mobile apps, B2B platforms, and enterprise solutions. Features Turborepo, pnpm workspaces, Next.js 15 App Router, Expo SDK 52 mobile, shared `@repo/ui`, `@repo/api` (Zod), and `@repo/database` (Prisma/SQLite WAL).
- **`fullstack-agent-app`**: For dedicated web-first AI apps (Next.js 15, Vercel AI SDK streaming copilot, Tailwind CSS).
- **`mobile-agent-app`**: For dedicated standalone iOS & Android mobile applications (Expo SDK 52 New Architecture, React Native).
- **`creative-agent-studio`**: For automated video production, marketing campaigns, and 3D device commercial rendering (Remotion v4 + Three.js).

#### 2. Execute Scaffolder CLI or Copy Starter
Run the pipeline scaffolder CLI or instantiate files into the target folder:
```powershell
python -m pipeline.cli "<ProjectName>" --template <template-name> --admin "admin@example.com"
```
Or programmatically copy:
1. `templates/<template-name>/` $\rightarrow$ Target project directory.
2. `.agents/` $\rightarrow$ Target project `.agents/` (with workspace MCP configs and Biome hooks).
3. `mempalace.yaml` and `entities.json` $\rightarrow$ Pre-seeds architectural memory rooms and guardrail entities.
4. Tailored `.env` & `.env.example` $\rightarrow$ Configured with master admin (`admin@example.com`), SQLite WAL URL, and Stripe keys.
5. Initialize Git repository with initial commit `feat(init): scaffold <ProjectName> with Universal Agency Pipeline v2.0`.

#### 3. Automatic Transition to Phase 1 (Blueprint & Spec Engine)
Do NOT stop at empty folder scaffolding or leave generic AI placeholders. Immediately ingest the user's idea and enforce the **Zero-Slop Quality Mandate**:
1. **Bespoke Domain Ingestion**: Analyze the client's industry and instantly tailor the application title, copy, value proposition, and feature architecture (no "Feature 1", no "Lorem Ipsum", no generic purple buttons).
2. **Deterministic Color Matching**: Automatically map the client industry to one of the 5 curated OKLCH palettes:
   - Security / DevTools $\rightarrow$ *Cyberpunk Matrix* (Obsidian & Emerald) or *Lockdown Crimson* (Deep Slate & Laser Crimson)
   - FinTech / B2B SaaS $\rightarrow$ *Oceanic Cobalt* (Midnight & Cobalt Blue)
   - Aerospace / Industrial / Hardware $\rightarrow$ *Avionics Amber* (Stealth Charcoal & Amber)
   - High-Design Media / Studio $\rightarrow$ *Swiss Bauhaus* (Deep Navy & Bauhaus Crimson)
3. **Full Suite of Real Pages**: Every scaffolded project automatically includes:
   - Public Landing Page with Three.js 3D canvas hero and social proof badges.
   - Transparent Pricing table with Monthly/Annual billing toggle and 20% discount badge.
   - Omnichannel Authentication (`/login` & `/signup`) with 6-digit cryptographic Email OTP and anti-sybil validation.
   - Real-time Operations Dashboard (`/dashboard`) with quota metering, reactive counters, and kill-switches.
   - Supreme Master Admin Center (`/dashboard/admin`) with HTTP 403 non-admin lockscreen (master: `admin@example.com`).
4. Generate `SPEC.md` specifying data schemas, API contracts, RBAC roles, and security boundaries.
5. Generate an interactive `PLAN.md` implementation plan artifact with clickable checklist.
6. Present the plan to the user for one-click approval before isolated branch build.

---

### Mode B: In-Situ Workspace Activation (Existing Codebase)
**Triggers**: `"scaffold workspace"`, `"init agents"`, `"setup project"` in an existing repository.

When run inside an existing codebase, do NOT overwrite application files. Set up the agency guardrails and workspace tooling:

#### Step 1: Detect Project Type
- **Web Project** (default): Playwright MCP + Supabase MCP + Vercel/Cloudflare
- **Mobile Project**: Maestro MCP + Supabase MCP + Expo EAS

#### Step 2: Create `.agents/mcp_config.json`
##### Web Project:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp", "--headless"]
    },
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server", "--project-ref", "${SUPABASE_PROJECT_REF}"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}"
      }
    },
    "vercel": {
      "url": "https://mcp.vercel.com/mcp"
    },
    "cloudflare": {
      "url": "https://mcp.cloudflare.com/mcp"
    }
  }
}
```

##### Mobile Project:
```json
{
  "mcpServers": {
    "maestro": {
      "command": "npx",
      "args": ["-y", "maestro-mcp"]
    },
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server", "--project-ref", "${SUPABASE_PROJECT_REF}"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}"
      }
    }
  }
}
```

#### Step 3: Create `.agents/hooks.json`
```json
{
  "auto-format": {
    "PostToolUse": [
      {
        "matcher": "write_to_file|replace_file_content",
        "hooks": [
          {
            "type": "command",
            "command": "cmd /c \"npx @biomejs/biome check --write . 2>nul || npx prettier --write . --ignore-unknown 2>nul || echo format-done\"",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

#### Step 4: Create `.agents/AGENTS.md`
```markdown
# Project Workspace Rules

## 1. Zero-Leak Security & Master Admin Exclusivity
- NEVER stage or commit `.env`, `.env.local`, API tokens, or secrets.
- Master Admin: admin@example.com (server-side enforced RBAC).

## 2. 5-Phase Universal Agency Pipeline Discipline
- Phase 0: Task Decomposition & Multi-Agent Orchestration (Architect, Builder, QA, Security, DevOps).
- Phase 1 (Blueprint): Interactive Implementation Plan + Generative UI sandbox.
- Phase 2 (Branch Build): Work in dedicated Git worktrees via branch subagent (`Workspace: "branch"`).
- Phase 3 (Testing): Playwright headless testing, Lighthouse 90+ score check, Visual Regression, Self-Healing loop.
- Phase 3.5 (Security Review): Senior Staff Security Architect code review + Promptfoo adversarial red-teaming.
- Phase 4 (Ship): Format with Biome, conventional commit, GitHub PR with recordings, staging deploy, and client handover.md.
```

#### Step 5: Seed MemPalace Memory (`mempalace.yaml`)
Create or verify `mempalace.yaml` in the project root with the 7 architectural rooms (`enterprise_guardrails`, `architecture_and_monorepo`, `security_and_auth`, `creative_studio_video`, `observability_and_performance`, `skills_and_tooling`, `adrs_and_decisions`).

#### Step 6: Create or Update `CHANGELOG.md`
```markdown
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]
### Added
- Project initialized with Universal Agency Pipeline v2.0 workflow tooling and enterprise guardrails.
```

#### Step 7: Confirmation & Status
Notify the user that the workspace is scaffolded and ready for development with all global and workspace tooling active.
