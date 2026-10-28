"""Automated Unit & Integration Tests for Agent Builder Scaffolder."""
import os
import sys
import importlib.util
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "skills" / "agent-builder"))

from scaffold_agent import create, TEMPLATES

@pytest.mark.parametrize("archetype", ["rag", "workflow", "action", "copilot"])
def test_scaffolding_generates_all_files(tmp_path, archetype):
    output_dir = tmp_path / "agents"
    agent_name = f"Test_{archetype.capitalize()}"
    create(name=agent_name, archetype=archetype, output_dir=str(output_dir))

    target_dir = output_dir / f"test_{archetype}"
    assert target_dir.exists(), f"Agent folder {target_dir} not created"
    assert (target_dir / "AGENT_SPEC.md").exists()
    assert (target_dir / "requirements.txt").exists()
    assert (target_dir / ".env.example").exists()
    assert (target_dir / "README.md").exists()
    assert (target_dir / "pyproject.toml").exists()

    code_file = target_dir / TEMPLATES[archetype]["code_filename"]
    assert code_file.exists()
    assert len(code_file.read_text(encoding="utf-8")) > 100

    test_file = target_dir / "tests" / "test_agent.py"
    assert test_file.exists()
    assert len(test_file.read_text(encoding="utf-8")) > 50

@pytest.mark.parametrize("archetype", ["rag", "workflow", "action", "copilot"])
def test_scaffolded_agent_code_syntax_and_import(tmp_path, archetype):
    """Verifies that generated code for each archetype compiles and is importable without errors."""
    output_dir = tmp_path / "agents"
    agent_name = f"Live_{archetype.capitalize()}"
    create(name=agent_name, archetype=archetype, output_dir=str(output_dir))

    target_dir = output_dir / f"live_{archetype}"
    code_file = target_dir / TEMPLATES[archetype]["code_filename"]

    spec = importlib.util.spec_from_file_location(f"agent_{archetype}", code_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Verify key classes/attributes exist in the dynamically loaded module
    if archetype == "rag":
        assert hasattr(mod, "ProductionRAGAgent")
        agent = mod.ProductionRAGAgent()
        assert agent.top_k == 3
    elif archetype == "workflow":
        assert hasattr(mod, "ProductionWorkflowEngine")
        engine = mod.ProductionWorkflowEngine()
        assert hasattr(engine, "run_until_terminal")
    elif archetype == "action":
        assert hasattr(mod, "ActionToolRegistry")
        registry = mod.ActionToolRegistry()
        res = registry.safe_calculate("2 + 3 * 4")
        assert res.success is True
        assert res.result == 14
    elif archetype == "copilot":
        assert hasattr(mod, "ProductionCopilot")
        copilot = mod.ProductionCopilot()
        assert copilot.cache_ttl_seconds == 60.0
