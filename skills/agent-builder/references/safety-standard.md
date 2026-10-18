# Production Safety & Resilience Standards for AI Agents

All agents designed or shipped by this agency MUST satisfy these 6 non-negotiable safety guardrails.

---

## 1. Zero Unstructured Actions
No downstream mutation, API call, database query, or execution may be made from freeform text or unvalidated JSON strings.
- **Python**: Use `pydantic.BaseModel` with strict type validation.
- **TypeScript**: Use `zod.object({...})` with `z.infer`.
- Reject and re-prompt if output fails validation.

---

## 2. Deterministic Circuit Breakers
Agents must never enter infinite loops or run unchecked API queries:
- `max_iterations = 8`: After 8 turns, loop halts and returns partial completion.
- `tool_timeout = 30s`: Tools must abort via `asyncio.wait_for` (Python) or `AbortSignal.timeout` (TypeScript).
- `max_retries = 3`: Repeated exceptions on the same tool immediately trigger human escalation.

---

## 3. Strict Secrets & Credential Isolation
- Never log, display, or stage API keys (`OPENAI_API_KEY`, `SUPABASE_KEY`, `GITHUB_TOKEN`).
- Load environment variables strictly from OS process environments (`os.environ` / `process.env`).
- Never return API keys in error stack traces to user interfaces.

---

## 4. Input Sanitization & Jailbreak Defense
- Strip malicious prompt injection tokens (`<|im_start|>`, `[INST]`, `SYSTEM:`, `DAN Mode`).
- Cap user input lengths to sensible bounds (default 4,000 characters).
- Block prompt extraction attacks with explicit refusal guardrails.

---

## 5. RAG Retrieval Provenance & Grounding
- Always attach document metadata (`source_file`, `chunk_id`, `page_number`, `ingest_time`).
- Always instruct the LLM: *"If the answer is not present in the provided context, state that you do not know. Never speculate."*
- Require chunk ID citations in generated answers.

---

## 6. Full-Lifecycle Observability
- Every execution must create a root trace in Langfuse / OpenTelemetry.
- Track token usage, prompt latency, tool latency, and user feedback ratings (thumbs up/down).
- Realtime alerts for any error rate exceeding 5% in a 1-hour window.
