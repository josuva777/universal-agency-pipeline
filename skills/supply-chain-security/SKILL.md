---
name: supply-chain-security
description: >-
  Supply chain security, Software Bill of Materials (SBOM) generation (CycloneDX),
  dependency vulnerability scanning, strict Content Security Policy (CSP) nonces,
  sliding-window rate limiting, and cryptographic release signing.
  Trigger phrases: "supply chain", "sbom", "cyclonedx", "dependency scan", "csp",
  "content security policy", "rate limiting", "release signing", "zero trust".
---

# Supply Chain Security, SBOM & Defense-in-Depth Standard

This skill establishes the enterprise supply-chain defense standards demanded by US Executive Order 14028, NIST SP 800-218, and OWASP Top 10 for LLM Applications (2025).

---

## 1. Machine-Readable Software Bill of Materials (SBOM)

Every production release MUST generate a standardized CycloneDX JSON SBOM documenting 100% of direct and transitive dependencies:

```bash
# Node / Next.js / Monorepos
npx @cyclonedx/cyclonedx-npm --output-format JSON --output-file releases/sbom.json

# Python / FastAPI Backends
cyclonedx-py poetry --output-format json --output-file releases/sbom_python.json
```

- **Retention**: The generated `sbom.json` MUST be committed or uploaded as an immutable artifact in `releases/sbom.json` and attached to the GitHub release.
- **Dependency Audit**: Run `pnpm audit --audit-level=high` in CI. Any vulnerability with a known public exploit (EPSS score > 0.1) and confirmed reachability in application code blocks merge.
- **Frozen Lockfiles**: CI build jobs MUST always invoke `pnpm install --frozen-lockfile` (or `npm ci`), never mutating the lockfile during build.

---

## 2. Modern Strict Nonce-Based Content Security Policy (CSP)

Host-based allowlists (`script-src 'self' https://trusted.com`) are obsolete and easily bypassed via JSONP endpoints and open redirects.
All production web consoles MUST inject a cryptographically randomized **nonce** per HTTP request:

```typescript
// middleware.ts (Next.js Edge Middleware)
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Generate 16-byte base64 cryptographic nonce
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64');
  
  const cspHeader = `
    default-src 'self';
    script-src 'self' 'nonce-${nonce}' 'strict-dynamic';
    style-src 'self' 'unsafe-inline';
    img-src 'self' blob: data: https://*.stripe.com;
    font-src 'self';
    object-src 'none';
    base-uri 'none';
    form-action 'self';
    frame-ancestors 'none';
    upgrade-insecure-requests;
  `.replace(/\s{2,}/g, ' ').trim();

  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-nonce', nonce);
  requestHeaders.set('Content-Security-Policy', cspHeader);

  const response = NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });
  
  response.headers.set('Content-Security-Policy', cspHeader);
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set(
    'Strict-Transport-Security',
    'max-age=63072000; includeSubDomains; preload'
  );

  return response;
}
```

---

## 3. Sliding-Window Rate Limiting Architecture

Static fixed-window rate limits allow 2x traffic bursts at boundary windows. All authentication and sensitive endpoints MUST enforce sliding-window counters:

```python
# FastAPI In-Memory Sliding-Window Rate Limiter
from collections import deque
import time
from fastapi import Request, HTTPException, status

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients: dict[str, deque[float]] = {}

    def is_allowed(self, client_id: str) -> tuple[bool, int, int]:
        now = time.time()
        cutoff = now - self.window_seconds
        
        if client_id not in self.clients:
            self.clients[client_id] = deque()
            
        timestamps = self.clients[client_id]
        
        # Evict timestamps older than cutoff
        while timestamps and timestamps[0] < cutoff:
            timestamps.popleft()
            
        if len(timestamps) >= self.max_requests:
            retry_after = int(self.window_seconds - (now - timestamps[0]))
            return False, 0, max(1, retry_after)
            
        timestamps.append(now)
        remaining = self.max_requests - len(timestamps)
        return True, remaining, self.window_seconds

# Global limiters
auth_limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=900)  # 5 attempts / 15 mins
api_limiter = SlidingWindowRateLimiter(max_requests=100, window_seconds=60)   # 100 calls / 1 min
```

- When triggered, return **HTTP 429 Too Many Requests** with standard headers:
  - `Retry-After: <seconds>`
  - `X-RateLimit-Limit: <limit>`
  - `X-RateLimit-Remaining: 0`
  - `X-RateLimit-Reset: <timestamp>`

---

## 4. Cryptographic Release Signing & Integrity

Every compiled mobile APK, WebAPK, Windows launcher, and production zip file MUST be hashed and verified:

```python
import hashlib
import json
import os

def generate_release_manifest(release_dir: str, version: str) -> dict:
    assets = []
    for root, _, files in os.walk(release_dir):
        for f in files:
            if f.endswith((".apk", ".zip", ".tar.gz", ".bat")):
                path = os.path.join(root, f)
                with open(path, "rb") as fp:
                    sha256 = hashlib.sha256(fp.read()).hexdigest().upper()
                assets.append({
                    "filename": f,
                    "size_bytes": os.path.getsize(path),
                    "sha256": sha256
                })
                
    manifest = {
        "version": version,
        "algorithm": "SHA-256",
        "assets": assets,
        "status": "OFFICIAL_RELEASE"
    }
    
    with open(os.path.join(release_dir, "LATEST_RELEASE.json"), "w") as out:
        json.dump(manifest, out, indent=2)
        
    return manifest
```

