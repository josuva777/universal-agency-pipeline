"""Automated Unit Tests for Pipeline Scaffolder CLI."""
import os
import shutil
import tempfile
from pathlib import Path
from pipeline.cli import scaffold_project, TEMPLATES

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_scaffold_project_monorepo():
    """Tests scaffolding a project with monorepo-saas template."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target_dir = Path(tmp_dir) / "test-saas-app"
        admin_email = "testadmin@example.com"
        
        scaffold_project(
            name="Test SaaS App",
            target_dir=target_dir,
            template="monorepo-saas",
            admin_email=admin_email,
            theme="Cyberpunk Matrix"
        )
        
        # Verify files created
        assert target_dir.exists()
        assert (target_dir / "turbo.json").exists()
        assert (target_dir / "pnpm-workspace.yaml").exists()
        assert (target_dir / ".agents" / "mcp_config.json").exists()
        assert (target_dir / ".agents" / "hooks.json").exists()
        assert (target_dir / "mempalace.yaml").exists()
        assert (target_dir / "entities.json").exists()
        assert (target_dir / ".env").exists()
        
        # Verify .env contents
        env_text = (target_dir / ".env").read_text(encoding="utf-8")
        assert f'MASTER_ADMIN_EMAIL="{admin_email}"' in env_text
        assert 'PROJECT_NAME="Test SaaS App"' in env_text
        
        # Verify git initialization
        assert (target_dir / ".git").exists()

