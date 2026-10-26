---
name: observability
description: >-
  Production observability, structured logging, distributed tracing (OpenTelemetry),
  error tracking (Sentry), health checks, synthetic monitoring, and SLO/error budget alerting.
  Trigger phrases: "observability", "setup logging", "sentry", "opentelemetry", "tracing",
  "error tracking", "health check", "slo", "sli", "monitor uptime".
---

# Observability, Telemetry & Reliability Engineering Standard

This skill establishes the production observability architecture demanded by Google, Stripe, and Netflix. Every production service must be observable from Day 1 with zero guesswork.

---

## 1. Structured JSON Logging Architecture

### Python (Backend / FastAPI) — `structlog` Standard
Plain string prints (`print("Error: user not found")`) are strictly forbidden in production.
All logs must emit single-line JSON with standardized fields:

```python
import structlog
import logging
import sys

def configure_logger():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(sys.stdout),
        cache_logger_on_first_use=True,
    )

logger = structlog.get_logger()

# Usage with context bindings:
logger.info(
    "auth.otp_dispatched",
    user_id="usr_94821a",
    email_domain="acmecorp.com",
    delivery_channel="smtp",
    latency_ms=142.5,
    trace_id="4bf92f3577b34da6a3ce929d0e0e4736",
    span_id="00f067aa0ba902b7"
)
```

### TypeScript / Next.js — `pino` Standard
```typescript
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  base: {
    env: process.env.NODE_ENV,
    service: 'sentinelops-web',
  },
});
```

---

## 2. Distributed Tracing (W3C OpenTelemetry)

Every incoming HTTP request must extract or generate a W3C `traceparent` header:
`version-trace_id-parent_id-trace_flags` (e.g. `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`).

```python
# FastAPI Middleware for W3C Trace Propagation
from fastapi import Request
import uuid
import structlog

@app.middleware("http")
async def trace_context_middleware(request: Request, call_next):
    trace_id = request.headers.get("x-trace-id") or uuid.uuid4().hex
    span_id = uuid.uuid4().hex[:16]
    
    structlog.contextvars.bind_contextvars(trace_id=trace_id, span_id=span_id)
    
    response = await call_next(request)
    response.headers["x-trace-id"] = trace_id
    return response
```

---

## 3. Production Health Check Standard (`/health`)

Every backend API service MUST expose an unauthenticated, zero-downtime health endpoint (`GET /health`) returning deep dependency state:

```json
{
  "status": "healthy",
  "version": "1.4.0",
  "timestamp": "2026-10-26T19:40:00Z",
  "uptime_seconds": 86420,
  "checks": {
    "database": {
      "status": "ok",
      "mode": "WAL",
      "latency_ms": 1.2
    },
    "smtp_gateway": {
      "status": "connected",
      "host": "smtp.gmail.com"
    },
    "ledger_integrity": {
      "status": "valid",
      "last_block_hash": "A94F8B2C..."
    }
  }
}
```

If a critical dependency fails (e.g. SQLite locked or disk full), return **HTTP 503 Service Unavailable** with `"status": "degraded"` or `"status": "unhealthy"`.

---

## 4. Error Tracking Architecture (Sentry)

- **Frontend (`@sentry/nextjs`)**:
  - Auto-captures uncaught React render exceptions.
  - Generates Session Replays only on error states (privacy-first: all input text and PII masked).
  - Source maps uploaded privately during production build (`sentry-cli`) and never exposed in browser devtools.
- **Backend (`sentry-sdk`)**:
  - Captures unhandled 500 errors with full local variable snapshots.
  - Automatically filters sensitive headers: `Authorization`, `Cookie`, `Stripe-Signature`.

---

## 5. Service Level Objectives (SLO) & Burn-Rate Alerting

Define user-centric Service Level Indicators (SLIs) over rolling 28-day windows:

| Service Area | Target SLI | SLO Target | Error Budget |
| :--- | :--- | :--- | :--- |
| **Gateway Availability** | % of non-5xx requests | ≥ 99.9% | 0.1% (~43 mins downtime/mo) |
| **API Latency** | % of calls completing in < 500ms | ≥ 95.0% | 5.0% |
| **Auth Verification** | % of OTPs verified in < 60s | ≥ 99.0% | 1.0% |

### Multi-Window Burn-Rate Alerting (No Alert Fatigue)
Instead of paging on every single transient 500 spike, alert on how fast the error budget is burning:
- **P1 Critical Page (Wake up engineer)**: 2% of 30-day budget consumed within 1 hour (14.4x burn rate).
- **P2 High Alert (Check during business hours)**: 5% of budget consumed within 6 hours (6x burn rate).
- **P3 Low Ticket (Jira/Linear backlog)**: 10% of budget consumed over 3 days (1x burn rate).

