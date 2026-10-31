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
        "tests/promptfoo.yaml",
        ".github/workflows/release.yml",
        "mempalace.yaml",
        "entities.json",
        "pipeline/cli.py",
    ]
    for rel_path in required_paths:
        target = REPO_ROOT / rel_path
        assert target.exists(), f"Critical required repository file missing: {rel_path}"

def test_promptfoo_configuration():
    """Verifies that promptfoo.yaml has OWASP LLM01-LLM10 test cases and valid provider target."""
    pf = REPO_ROOT / "tests" / "promptfoo.yaml"
    assert pf.exists()
    content = yaml.safe_load(pf.read_text(encoding="utf-8"))
    assert "prompts" in content
    assert "providers" in content
    assert "tests" in content
    assert len(content["tests"]) >= 50, f"Expected 50+ adversarial tests, found {len(content['tests'])}"

    # Verify provider file actually exists and has call_api entrypoint
    for prov in content["providers"]:
        prov_id = prov if isinstance(prov, str) else prov.get("id", "")
        if prov_id.startswith("python:"):
            target_path = REPO_ROOT / prov_id.replace("python:", "")
            assert target_path.exists(), f"Promptfoo provider target file not found on disk: {target_path}"
            provider_code = target_path.read_text(encoding="utf-8")
            assert "def call_api" in provider_code, f"Provider {target_path} missing call_api function"

def test_mempalace_structure():
    """Verifies mempalace.yaml rooms and entities.json knowledge graph seeds."""
    mp = REPO_ROOT / "mempalace.yaml"
    assert mp.exists()
    mp_data = yaml.safe_load(mp.read_text(encoding="utf-8"))
    assert mp_data.get("wing") == "universal_agency_pipeline"
    room_names = [r["name"] for r in mp_data.get("rooms", [])]
    expected_rooms = [
        "enterprise_guardrails",
        "architecture_and_monorepo",
        "security_and_auth",
        "creative_studio_video",
        "observability_and_performance",
        "skills_and_tooling",
        "adrs_and_decisions",
    ]
    for er in expected_rooms:
        assert er in room_names, f"Missing room in mempalace.yaml: {er}"

    ent = REPO_ROOT / "entities.json"
    assert ent.exists()
    ent_data = json.loads(ent.read_text(encoding="utf-8"))
    assert "people" in ent_data
    assert "projects" in ent_data
    assert "topics" in ent_data
    assert len(ent_data["topics"]) >= 10

def test_lighthouse_configuration():
    """Verifies that lighthouserc.js uses secure filesystem reporting instead of public upload."""
    lh_file = REPO_ROOT / "lighthouserc.js"
    assert lh_file.exists()
    content = lh_file.read_text(encoding="utf-8")
    assert "'filesystem'" in content or '"filesystem"' in content
    assert "temporary-public-storage" not in content
    assert "'./reports/lighthouse'" in content or '"./reports/lighthouse"' in content


