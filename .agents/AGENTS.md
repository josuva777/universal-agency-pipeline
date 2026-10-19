# Project Workspace Rules

## 1. Token & Output Guardrails
- **Ponytail Minimal Diffs**: Never rewrite whole files for small changes. Use surgical `replace_file_content` edits to reduce generation tokens by 54%+.
- **30-Message Reset Rule**: At turn 30, compact context (`/compact`) or write progress to an artifact before proceeding.

## 2. 4-Phase Agency Pipeline
- **Phase 1 (GSD Spec & Blueprint)**: Generate `SPEC.md` and an interactive Implementation Plan (`PLAN.md`) artifact before writing production code.
- **Phase 2 (Isolated Worktree Build)**: Always build inside a dedicated feature branch or Git worktree (`git worktree add ../feature-<slug> -b feature/<slug>`).
- **Phase 3 (The Ralph Loop)**:
  - Run automated E2E tests (Playwright for Web, Maestro for Mobile) + Promptfoo evals.
  - Autonomous Self-Healing: If red, diagnose, patch, and re-test (up to 3 iterations).
  - Strix OWASP security pentest in sandbox before PR.
- **Phase 4 (Ship & Review)**:
  - Format with Biome (`<50ms`).
  - Commit with conventional prefixes (`feat:`, `fix:`, `chore:`).
  - Open PR with attached automated **CodeRabbit** review (`.coderabbit.yaml`) and Lighthouse proof (90+).
