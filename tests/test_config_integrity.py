"""Automated Repository Integrity & Configuration Syntax Tests."""
import json
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_json_configurations():
    """Verifies that all JSON config files across the repo are valid syntax."""
    json_files = list(REPO_ROOT.glob("configs/**/*.json")) + list(REPO_ROOT.glob(".agents/**/*.json"))
    assert len(json_files) > 0, "No JSON config files found!"

    for jf in json_files:
        try:
            content = jf.read_text(encoding="utf-8")
            data = json.loads(content)
            assert isinstance(data, (dict, list)), f"Config {jf} is not an object/array"
        except Exception as e:
            assert False, f"Failed to parse JSON file {jf}: {e}"

def test_yaml_configurations():
    """Verifies that all YAML configs (.coderabbit.yaml, etc.) are valid syntax (supports multi-doc)."""
    yaml_files = list(REPO_ROOT.glob("**/*.yaml")) + list(REPO_ROOT.glob("**/*.yml"))
    # Filter out .venv or node_modules
    yaml_files = [y for y in yaml_files if ".venv" not in str(y) and "node_modules" not in str(y)]
    assert len(yaml_files) > 0, "No YAML config files found!"

    for yf in yaml_files:
        try:
            content = yf.read_text(encoding="utf-8")
            docs = list(yaml.safe_load_all(content))
            assert len(docs) > 0, f"YAML file {yf} is empty or invalid"
        except Exception as e:
            assert False, f"Failed to parse YAML file {yf}: {e}"

def test_required_repo_structure():
    """Verifies that all core documentation, skills, and templates are present."""
    required_paths = [
        "README.md",
        "AGENTS.md",
        ".coderabbit.yaml",
        "skills/agency-pipeline/SKILL.md",
        "skills/agency-scaffold/SKILL.md",
        "skills/agent-builder/scaffold_agent.py",
        "skills/agent-builder/system_scanner.py",
        "skills/ponytail/SKILL.md",
        "skills/taste-skill/SKILL.md",
        "skills/super-design-motion/SKILL.md",
        "skills/observability/SKILL.md",
        "skills/performance-guardian/SKILL.md",
        "skills/accessibility-audit/SKILL.md",
        "skills/supply-chain-security/SKILL.md",
        "templates/fullstack-agent-app/package.json",
        "templates/fullstack-agent-app/app/chat/page.tsx",
        "templates/fullstack-agent-app/.env.example",
        "templates/mobile-agent-app/package.json",
        "templates/creative-agent-studio/studio.ps1",
        "templates/monorepo-saas/turbo.json",
        "templates/monorepo-saas/pnpm-workspace.yaml",
        "templates/monorepo-saas/package.json",
    ]
    for rel_path in required_paths:
        target = REPO_ROOT / rel_path
        assert target.exists(), f"Critical required repository file missing: {rel_path}"

