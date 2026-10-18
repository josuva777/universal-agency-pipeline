# Full-Stack AI Agent App Architecture (Unified Monorepo)

When a client asks for **both an AI Agent and an Application (Web / Mobile / Dashboard)**, NEVER build them in separate disconnected folders. Build them together as a **Unified Full-Stack Project**.

---

## 1. Why Unified Full-Stack is Superior
- **Single Deployment**: 1 click to deploy to Vercel, Cloudflare, or Docker.
- **Shared Type Contracts**: The frontend UI and the backend Agent share the exact same Zod / Pydantic schemas.
- **Client Simplicity**: The client receives **ONE URL** (e.g., `https://client-ai.vercel.app`) with the frontend UI, file uploads, and streaming AI assistant working out of the box.

---

## 2. Recommended Directory Blueprint (Next.js 15 Full-Stack)

```
client-project/
├── app/
│   ├── page.tsx                      # Modern Landing Page & Hero
│   ├── chat/page.tsx                 # Interactive Agent Chat Interface
│   ├── dashboard/page.tsx            # Analytics & Knowledge Base Uploader
│   └── api/
│       └── chat/route.ts             # 🤖 THE AGENT LIVES HERE (Vercel AI SDK / LangGraph)
├── components/
│   ├── ui/                           # Radix / Tailwind UI components
│   ├── ChatInterface.tsx             # Streaming Chat with Citation Pills
│   └── DocumentUploader.tsx          # Drag & Drop PDF uploader to Vector DB
├── lib/
│   ├── agent/                        # Agent Logic & Tools
│   │   ├── tools.ts                  # Database lookup, API search, calculator
│   │   ├── circuit_breaker.ts        # Max 8 steps, timeouts, human escalation
│   │   └── guardrails.ts             # Prompt injection filter
│   └── vector_db.ts                  # Qdrant / Supabase pgvector adapter
├── creative/                         # 🎬 CLIENT PROMOTIONAL ASSETS
│   ├── logo_master.svg               # Vector brand logo
│   ├── brand_kit.html                # Interactive brand guidelines portal
│   └── commercial.mp4                # 4K promotional video
├── AGENT_SPEC.md                     # Agent architecture contract
├── .agents/                          # Agency MCPs (Playwright, Supabase, Biome)
├── promptfoo.yaml                    # Redteam security eval suite
├── package.json
└── README.md
```

---

## 3. How the UI Connects to the Agent

```mermaid
flowchart LR
    subgraph FRONTEND["Frontend UI (Next.js / React)"]
        UI["User Chat & File Upload"]
    end

    subgraph API["Backend API (app/api/chat/route.ts)"]
        STREAM["Vercel AI SDK\nstreamText() / LangGraph"]
    end

    subgraph AGENT["Core Agent Brain (lib/agent/)"]
        BRAIN["4-Archetype Engine\nRAG / Workflow / ReAct"]
        VEC["Vector DB (Qdrant / Supabase)"]
        TRACE["Langfuse Tracing"]
    end

    UI <-->|Server-Sent Events (SSE) Stream| STREAM
    STREAM <--> BRAIN
    BRAIN <--> VEC
    BRAIN -.-> TRACE
```

---

## 4. Trigger Phrases
Whenever the user prompts:
- `"build full app for [X]"`
- `"build an AI agent app for [X]"`
- `"create full project for [X]"`

The agency pipeline builds the unified full-stack structure automatically!
