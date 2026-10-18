---
name: pre-deploy-security
description: >-
  Use this skill right before opening a final Pull Request to run security
  pentesting (Strix) and AI agent evaluations (Promptfoo). These tools run
  as one-shot CLI commands to save token budget — they are NOT persistent MCP
  servers. Trigger phrases: "security check", "pre-deploy scan", "run strix",
  "run promptfoo", "security audit", "pentest".
---

# Pre-Deploy Security & Evaluation Checks

Run these checks right before opening the final Pull Request.

## Security Pentest (Strix)

Scan the codebase for security vulnerabilities:

```bash
npx strix scan --format json --output strix-report.json
```

Review the output:
- **CRITICAL / HIGH** findings → MUST fix before merging
- **MEDIUM** findings → Fix or document as accepted risk
- **LOW / INFO** findings → Document and track

Attach `strix-report.json` to the Pull Request description.

## AI Agent Evaluation (Promptfoo)

If the project includes AI agent integrations or LLM-powered features:

```bash
npx promptfoo eval --config promptfoo.yaml --output eval-results.json
```

Review evaluation metrics:
- Check pass rates across all test cases
- Flag any regression from previous baselines
- Attach `eval-results.json` to the Pull Request

## Checklist Before Opening PR

- [ ] All unit tests pass
- [ ] Browser/visual tests pass (screenshots attached)
- [ ] Strix security scan — no CRITICAL/HIGH findings
- [ ] Promptfoo eval — pass rate meets threshold (if applicable)
- [ ] Code formatted with Prettier
- [ ] Conventional commit messages used
- [ ] Branch is up to date with main

