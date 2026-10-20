# Changelog

All notable changes to the **Universal Agency Pipeline** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
