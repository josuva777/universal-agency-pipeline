"""Automated Unit & Integration Tests for Agent Builder Scaffolder."""
import sys
import subprocess
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
def test_scaffolded_agent_tests_pass(tmp_path, archetype):
    """Executes pytest on the generated agent's own tests to prove it is genuinely functional."""
    output_dir = tmp_path / "agents"
    agent_name = f"Live_{archetype.capitalize()}"
    create(name=agent_name, archetype=archetype, output_dir=str(output_dir))

    target_dir = output_dir / f"live_{archetype}"

    # Run pytest inside the generated agent's directory
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_agent.py"],
        cwd=str(target_dir),
        capture_output=True,
        text=True
    )
    assert res.returncode == 0, f"Generated test failed for {archetype}:\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}"

