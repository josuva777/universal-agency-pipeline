---
name: pre-deploy-security
description: >-
  Use this skill right before opening a final Pull Request to run security
  pentesting (Strix) and AI agent evaluations (Promptfoo). These tools run
  as one-shot CLI commands to save token budget — they are NOT persistent MCP
  servers. Trigger phrases: "security check", "pre-deploy scan", "run strix",
  "run promptfoo", "security audit", "pentest".
---

# Pre-Deploy Security & Adversarial Evaluation Checks

Run these checks right before opening the final Pull Request (Phase 3.5).

## 1. Security Pentest (Strix)

Scan the codebase for OWASP vulnerabilities and credential leaks:

```bash
npx strix scan --format json --output strix-report.json
```

Review findings:
- **CRITICAL / HIGH** findings $\rightarrow$ **MUST fix** before opening PR.
- **MEDIUM** findings $\rightarrow$ Remediate or document as accepted risk.
- **LOW / INFO** findings $\rightarrow$ Track in backlog.

Attach `strix-report.json` to the Pull Request.

---

## 2. AI Agent Adversarial Evaluation (Promptfoo)

If the project includes AI copilots, LLM tool calls, or RAG systems, execute the built-in OWASP Top 10 Red-Teaming suite:

```bash
npx promptfoo eval --config tests/promptfoo.yaml --output eval-results.json
```

Evaluation gates:
- **Prompt Injection (LLM01)**: 100% pass rate (zero instruction overrides or DAN jailbreaks).
- **Sensitive Data Disclosure (LLM02)**: 100% pass rate (zero credential, OTP, or API key leaks).
- **Excessive Agency (LLM06)**: 100% pass rate (zero unauthorized table drops or privilege elevations).
- **System Prompt Leakage (LLM07)**: 100% pass rate.

---

## 3. Supply Chain Security & SBOM Generation

```bash
npx @cyclonedx/cyclonedx-npm --package-lock-only --output-format JSON --output-file releases/sbom.json
```

---

## Pre-PR Quality Checklist

- [ ] All unit and integration tests pass (`pnpm test` / `pytest`)
- [ ] Playwright E2E and visual tests pass (screenshots attached)
- [ ] Axe-Core accessibility scan reports **0 violations**
- [ ] Lighthouse CI scores meet thresholds (Perf ≥ 90, A11y ≥ 95)
- [ ] Strix security scan — 0 CRITICAL/HIGH findings
- [ ] Promptfoo adversarial eval — 100% pass rate on safety gates
- [ ] Code formatted with Biome (`pnpm exec biome check --write .`)
- [ ] Conventional commit messages used (`feat:`, `fix:`, `perf:`)
- [ ] CycloneDX SBOM generated in `releases/sbom.json`
