---
name: agency-scaffold
description: >-
  Scaffolds a new project folder with the ultimate agency workflow.
  Creates .agents/ directory with workspace MCPs (Playwright/Maestro + Supabase + Vercel/Cloudflare),
  Biome/Prettier auto-formatting hooks, enterprise AGENTS.md rules, and CHANGELOG.md.
  Trigger phrases: "scaffold workspace", "setup project", "init agents", "add workspace config", "setup agents folder".
---

# Workspace Scaffold

When the user wants to set up a new project for the agency workflow, run this procedure in the project root:

## Step 1: Detect or Ask Project Type
- **Web Project** (default): Playwright MCP + Supabase MCP + Vercel/Cloudflare
- **Mobile Project**: Maestro MCP + Supabase MCP + Expo EAS

## Step 2: Create `.agents/mcp_config.json`

### Web Project:
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

### Mobile Project:
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

## Step 3: Create `.agents/hooks.json`

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

## Step 4: Create `.agents/AGENTS.md`

```markdown
# Project Workspace Rules

## 1. Zero-Leak Security
- NEVER stage or commit `.env`, `.env.local`, API tokens, or secrets.

## 2. 4-Phase Pipeline Discipline
- Phase 1 (Blueprint): Interactive Implementation Plan + Generative UI sandbox
- Phase 2 (Branch Build): Work in dedicated Git worktrees via branch subagent; use MSW for API mocking
- Phase 3 (Testing): Playwright headless testing, Lighthouse 90+ score check, Visual Regression, Self-Healing loop
- Phase 3.5 (Review): Principal Architect code review pass on git diff
- Phase 4 (Ship): Format with Biome, conventional commit, GitHub PR with recordings, staging deploy, and client handover.md
```

## Step 5: Create Initial `CHANGELOG.md`

```markdown
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]
### Added
- Project initialized with Antigravity Agency Workflow
```

## Step 6: Confirmation

Notify the user that the workspace is scaffolded and ready for development with all global and workspace tooling active.
