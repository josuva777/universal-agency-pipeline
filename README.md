# 🏢 Universal Agency Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![MCP Standard](https://img.shields.io/badge/MCP-Standard%20Compatible-green)](https://modelcontextprotocol.io/)
[![Agents Supported](https://img.shields.io/badge/Agents-Antigravity%20%7C%20Claude%20%7C%20Cursor%20%7C%20Windsurf-purple)](#-multi-agent-compatibility)

The **Universal Agency Pipeline** is an enterprise-grade, token-efficient autonomous development system. It transforms any AI coding assistant into a full-service software agency capable of building:
1. 🌐 **Full-Stack Web & Mobile Apps** (Next.js, Supabase, Tailwind, Stripe)
2. 🤖 **Production-Grade AI Agents** (Hybrid RAG, LangGraph State Machines, ReAct Loops, Streaming Copilots)
3. 🎬 **Broadcast-Quality 4K Commercials & Media** (Remotion, Three.js 3D mockups, GSAP kinetic text, Microsoft Neural voiceover)

Built on the open **Model Context Protocol (MCP)**, this stack works seamlessly across **Antigravity, Claude Desktop, Claude Code, Cursor, Windsurf, and VS Code (Cline / Roo Code)**.

---

## 🚀 Architecture Overview

```mermaid
flowchart TD
    subgraph GLOBAL["🌐 Always-On Core (Only ~840 Tokens)"]
        GH["GitHub MCP\nCommits, Branches & PRs"]
        CTX["Context7\nLive API & Docs Lookup"]
        MEM["MemPalace\nLong-Term Vector Memory (344 Drawers)"]
        HEAD["Headroom\n47-92% Token Compression"]
    end

    subgraph WORKSPACE["📂 Project On-Demand (.agents/)"]
        PW["Playwright (Web) / Maestro (Mobile)"]
        SUPA["Supabase (Dev Branches)"]
        DEP["Vercel / Cloudflare / Google Cloud"]
        BIOME["Biome Sub-50ms Auto-Formatter"]
    end

    subgraph DISCIPLINES["⚡ 3 Turnkey Agency Engines"]
        E1["🏭 Agent Factory\n4 Archetypes, Pydantic/Zod,\nLangfuse Tracing, Promptfoo Evals"]
        E2["🎬 Creative Studio\nRemotion 4K/60fps, Three.js 3D,\nEdge-TTS, EBU R128 (-14 LUFS)"]
        E3["📦 Full-Stack Monorepo\nApp + Agent + Marketing Video\nin 1 Unified Turnkey Folder"]
    end

    GLOBAL --> DISCIPLINES
    WORKSPACE --> DISCIPLINES
```

---

## ⚡ 1-Sentence Natural Language Triggers (Chat-First Workflow)

You never have to run complicated terminal scripts. Simply talk to your AI agent in chat:

| Service Wanted | What to Say in Chat | What Happens Automatically |
| :--- | :--- | :--- |
| **New Web/Mobile App** | `scaffold workspace` | Configures isolated dev MCPs, sub-50ms Biome auto-formatting, and tests. |
| **Build Any AI Agent** | `create agent for [description]` | Scans PC hardware, classifies archetype (RAG/Workflow/Action/Copilot), generates `AGENT_SPEC.md`, Pydantic/Zod schemas, and Langfuse tracing. |
| **Render 4K Video & Brand** | `create video for [brief]` | Runs AI Director, synthesizes neural voice, detects Veo AI / custom b-roll, renders 4K Remotion commercial, and exports straight to 5TB Google Drive. |
| **All-in-One Product Launch** | `build full app for [description]` | Builds the Next.js full-stack app, embeds the streaming agent in `/api/chat`, and puts both marketing & demo videos in `creative/`! |

---

## 🛡️ Multi-Model Automatic Failover (Zero-Crash Guarantee)

To ensure your agency runs continuously even when cloud APIs encounter rate limits or outages, our orchestration engine features a 4-tier automatic failover waterfall:

```mermaid
flowchart TD
    BRIEF["Client Creative / Agent Brief"] --> T1{"1. Google Gemini 1.5/2.0/3\n(Fastest Free Cloud Tier)"}
    T1 -- "Success" --> OUT["Production Script & 3D Scene Architecture"]
    T1 -- "429 Rate Limit / Error" --> T2{"2. Groq (Llama 3.3 70B)\n(500 tokens/sec Free Tier)"}
    T2 -- "Success" --> OUT
    T2 -- "Rate Limit / Error" --> T3{"3. OpenAI (GPT-4o-mini)\n(Alternative Cloud Provider)"}
    T3 -- "Success" --> OUT
    T3 -- "Offline / No Connection" --> T4["4. Deterministic Master Engine\n(100% Reliable Offline Baseline)"]
    T4 --> OUT
```

---

## 🔄 The Autonomous "GSD + Ralph Loop" Pipeline

Every feature, agent, and screen goes through an autonomous, self-healing verification loop before reaching production or opening a Pull Request:

```mermaid
flowchart LR
    SPEC["1. GSD Spec\n(SPEC.md & PLAN.md)"] --> BUILD["2. Ponytail Build\n(Minimal Senior Diffs\nin Git Worktree)"]
    BUILD --> BIOME["3. Biome Hook\n(<50ms Format & Lint\n0 Tokens Used)"]
    BIOME --> TEST{"4. Ralph Loop QA\n(Playwright / Maestro\n+ Promptfoo Evals)"}
    TEST -- "Console / UI Error" --> BUILD
    TEST -- "100% Green" --> STRIX{"5. Strix Security\n(Autonomous OWASP\nSandbox Pentest)"}
    STRIX -- "Vulnerability Found" --> BUILD
    STRIX -- "Passed" --> PR["6. GitHub PR + CodeRabbit\n-> Vercel / Cloudflare Deploy"]
```

---

## 📦 3-in-1 Turnkey Monorepo Architecture

When clients order an AI product, never build disconnected pieces in separate folders. Deliver a unified monorepo:

```
client-turnkey-project/
├── app/                        # 1. THE WEB APP & CHATBOT
│   ├── page.tsx                # High-converting Landing Page
│   ├── chat/page.tsx           # Real-time Streaming AI Chat UI
│   └── api/chat/route.ts       # 🤖 Streaming Agent Backend (Vercel AI SDK)
│
├── creative/                   # 2 & 3. BOTH VIDEOS & BRANDING
│   ├── commercial_promo.mp4    # 🎬 Video 1: 4K Commercial Ad (for social media)
│   ├── demo_how_to_use.mp4     # 📱 Video 2: "How to Use" Onboarding Walkthrough
│   ├── logo_master.svg         # Official vector brand logo
│   └── brand_kit.html          # Interactive Client Portal (swatches, audio, download links)
│
├── AGENT_SPEC.md               # Strict circuit breakers (max 8 steps) & schemas
└── README.md                   # Client handover instructions
```

---

## 🛡️ Zero-Freeze Hardware Scanner (`system_scanner.py`)
To prevent heavy AI models from freezing laptops with 8GB RAM, our built-in hardware scanner audits your CPU, RAM, and GPU:
- **Tier 1 (Light / $\le$ 12GB RAM, iGPU)**: Automatically restricts local models to lightweight 1B–3B weights (Llama-3.2-1B, Qwen2.5-Coder-1.5B, Kokoro 82M) and routes heavy reasoning to **Google Gemini Cloud APIs (0 MB local storage used)**.
- **Tier 2 (Mid / 16–24GB RAM, 6–8GB VRAM)**: Enables 7B–8B quantized models (Q4_K_M).
- **Tier 3 (Heavy / $\ge$ 32GB RAM, 12GB+ VRAM)**: Enables 14B–32B local inference.

---

## ☁️ Zero-Bloat Cloud Storage: Google Drive 5TB & Google Cloud
- **5 TB Google Drive (`G:\My Drive\Agency Deliverables`)**: All rendered 4K commercial videos, audio masters, and brand portals automatically sync to your Google Drive. Zero C: drive space consumed!
- **Google Cloud Storage (`gcs_uploader.py`)**: Direct bucket upload with public streaming URLs.
- **MemPalace Long-Term Memory**: All uploaded asset URLs are permanently remembered in local vector drawers (344 drawers active) so you can ask for them anytime in any session.

---

## 🤖 Multi-Agent Compatibility

| AI Coding Agent | Config File Location | How It Connects |
| :--- | :--- | :--- |
| **Google Antigravity** | `~/.gemini/config/mcp_config.json` | Native global MCP + skill auto-loading |
| **Claude Desktop** | `%APPDATA%\Claude\claude_desktop_config.json` | Automatic stdio & Streamable HTTP support |
| **Cursor** | `~/.cursor/mcp.json` | Loads all core tools into Cursor Composer |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` | Native Windsurf Cascade MCP integration |
| **Claude Code CLI** | `~/.claude.json` | Terminal agent with full MCP access |
| **VS Code (Cline / Roo Code)** | `.vscode/mcp.json` | Full stdio connection |

---

## 📁 Repository Structure

```
universal-agency-pipeline/
├── .github/
│   └── workflows/ci.yml            # Automated cross-platform CI test & verification pipeline
├── .agents/                        # Universal workspace template for client projects
│   ├── mcp_config.json             # Web MCPs (Playwright, Supabase, Vercel, Cloudflare)
│   ├── mcp_config.mobile.json      # Mobile MCPs (Maestro, Supabase, Expo EAS)
│   ├── hooks.json                  # Sub-50ms Biome auto-formatting + secret scan hook
│   ├── secret_scan.py              # Pre-commit credential leak gatekeeper
│   └── AGENTS.md                   # Enterprise zero-leak guardrails + 30-msg reset rule
├── configs/                        # Ready-to-use configs for every AI agent
│   ├── antigravity/mcp_config.json
│   ├── claude-desktop/claude_desktop_config.json
│   ├── cursor/mcp.json
│   ├── windsurf/mcp_config.json
│   ├── claude-code/mcp_config.json
│   └── vscode/mcp.json
├── skills/                         # Reusable agent skills
│   ├── agency-pipeline/SKILL.md    # GSD Spec Engine (SPEC.md -> PLAN.md) + Ralph Loop
│   ├── ponytail/SKILL.md           # ⚡ "Lazy Senior Dev" (54%+ output token reduction)
│   ├── agency-scaffold/SKILL.md    # "scaffold workspace" generator
│   ├── agent-builder/              # Universal AI Agent Factory (Hybrid RAG, LangGraph, E2B, Redis Cache)
│   │   ├── system_scanner.py       # Hardware safety auditor (Free RAM & Disk space)
│   │   ├── scaffold_agent.py       # Production agent generator (4 tested archetypes)
│   │   └── references/             # RAG, Workflow, ReAct, Copilot cards
│   ├── creative-studio/            # Broadcast Commercial & Brand Studio (4K Remotion, Three.js, Edge-TTS, EBU R128)
│   │   └── references/             # Shaders, 3D rigs, EBU R128 mastering
│   ├── taste-skill/                # 🎨 Anti-Slop Frontend Art Direction & 3D (R3F, gltfjsx, Spline, Motion Primitives)
│   │   ├── scripts/                # draw.mjs, inspect.mjs, assets.mjs
│   │   ├── references/             # 3D, Physics & Mobile Design Guide
│   │   └── library/                # 247 Curated Award-Winning Blueprints
│   └── pre-deploy-security/        # 🛡️ Strix OWASP Pentest + Promptfoo Evals + CodeRabbit check
├── templates/                      # Full Project Starters
│   ├── fullstack-agent-app/        # Turnkey Web Monorepo: Next.js + Streaming Chat + Verified Tools
│   ├── mobile-agent-app/           # 📱 Turnkey Mobile Monorepo: Expo + Skia + Reanimated 3 + Maestro
│   ├── creative-agent-studio/      # Complete Remotion Video & Audio Engine
│   │   ├── start_studio.bat        # 1-Click Desktop Launcher
│   │   ├── studio.ps1              # Portable Interactive Dashboard ($PSScriptRoot)
│   │   └── agents/                 # Orchestrator, Model Provider (2026), SFX, Logo, GCS
│   ├── handover-template.md        # Client delivery brief
│   └── CHANGELOG.md                # KeepAChangelog template
├── tests/                          # Automated Pytest Suite (100% Pass)
│   ├── test_config_integrity.py    # JSON & Multi-document YAML validator
│   ├── test_model_provider.py      # Multi-model 2026 failover tests
│   ├── test_scaffold_agent.py      # Scaffolding & live generated agent test executor
│   ├── test_secret_scanner.py      # Pre-commit secret detection tests
│   └── test_system_scanner.py      # Hardware profiling unit tests
├── benchmarks/
│   └── token_benchmark.py          # Empirical token efficiency measurement suite
├── .coderabbit.yaml                # Automated GitHub PR review configuration
├── setup.ps1                       # Windows 1-click safe installer (Masked tokens + JSON merge)
├── setup.sh                        # macOS / Linux 1-click safe installer (Non-destructive merge)
├── .gitignore                      # Zero-leak secret filter
├── AGENTS.md                       # Master rules file for AI agents (Worktrees + 30-msg rule)
└── README.md                       # Master Documentation
```

---

## 📊 Automated Verification & Benchmarks

The repository includes a comprehensive, multi-layered test and verification suite:

- **Automated CI Pipeline** (`.github/workflows/ci.yml`): Cross-platform verification across Ubuntu, Windows, and macOS on Python 3.11, 3.12, and 3.13.
- **Credential Leak Prevention** (`.agents/secret_scan.py`): Blocks commits containing API keys, OAuth tokens, or unignored `.env` files.
- **Configuration & Schema Integrity** (`tests/test_config_integrity.py`): Parses all JSON and multi-document YAML configurations.
- **Empirical Token Savings Benchmark** (`benchmarks/token_benchmark.py`): Empirically measures token generation reduction (achieving 54% to 88%+ savings via Ponytail minimal surgical diffs):

```
        [Universal Agency Pipeline: Token Efficiency Benchmark Results]         
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Benchmark     ┃      Baseline ┃      Ponytail ┃              ┃         Token ┃
┃ Task          ┃        Tokens ┃        Tokens ┃ Lines Dumped ┃   Reduction % ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Error Boundary│          1420 │           160 │    350 -> 14 │         88.7% │
│ Zod Validator │           580 │           125 │    120 -> 18 │         78.4% │
│ DB Connection │          1150 │            65 │     280 -> 6 │         94.3% │
│ Cohere Rerank │           890 │           185 │    210 -> 24 │         79.2% │
├───────────────┼───────────────┼───────────────┼──────────────┼───────────────┤
│ AGGREGATE AVG │          4040 │           535 │            - │ 86.8% SAVINGS │
└───────────────┴───────────────┴───────────────┴──────────────┴───────────────┘
```

---

## 🔒 Zero-Leak Security Discipline
- **NEVER** stages `.env`, `.env.local`, API tokens, or credentials.
- Multi-layer `.gitignore` protects credentials, model weights, and media temp files.
- Automated secret-scanning audit before commits.

---

## 📄 License
MIT License. Free to use for personal, commercial, and client agency projects.
