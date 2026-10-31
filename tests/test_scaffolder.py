"""Automated Unit Tests for Pipeline Scaffolder CLI."""
import os
import sys
import shutil
import tempfile
from pathlib import Path

# Ensure pipeline root is in sys.path before any local imports
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.cli import scaffold_project, safe_merge_copy, TEMPLATES

def test_scaffold_project_monorepo():
    """Tests scaffolding a project with monorepo-saas template into an empty directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target_dir = Path(tmp_dir) / "test-saas-app"
        admin_email = "custom_admin@example.com"

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
        assert (target_dir / ".env.example").exists()

        # Verify tailored .env contents
        env_text = (target_dir / ".env").read_text(encoding="utf-8")
        assert f'MASTER_ADMIN_EMAIL="{admin_email}"' in env_text
        assert 'PROJECT_NAME="Test SaaS App"' in env_text

        # Verify placeholder-only .env.example
        env_example_text = (target_dir / ".env.example").read_text(encoding="utf-8")
        assert "MASTER_ADMIN_EMAIL=admin@example.com" in env_example_text
        assert "sk_test_placeholder" in env_example_text

        # Verify git initialization and pre-commit hooks
        assert (target_dir / ".git").exists()
        assert (target_dir / ".git" / "hooks" / "pre-commit").exists()

        # Verify OpenTelemetry tracing in monorepo template
        assert (target_dir / "packages" / "api" / "src" / "tracing.ts").exists()

        # Verify tailored branding in page.tsx
        page_text = (target_dir / "apps" / "web" / "app" / "page.tsx").read_text(encoding="utf-8")
        assert 'projectName="Test SaaS App"' in page_text

def test_scaffold_non_destructive_merge():
    """Tests that scaffolding never deletes existing client files when directory is non-empty."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target_dir = Path(tmp_dir) / "existing-client-project"
        target_dir.mkdir(parents=True)

        # Create existing client files that MUST NOT be deleted
        client_code = target_dir / "custom_client_logic.py"
        client_code.write_text("# Client Intellectual Property - Do Not Delete", encoding="utf-8")

        existing_agents_rule = target_dir / ".agents" / "client_custom_rule.md"
        existing_agents_rule.parent.mkdir(parents=True, exist_ok=True)
        existing_agents_rule.write_text("# Client Specific Rule", encoding="utf-8")

        pre_existing_env = target_dir / ".env"
        pre_existing_env.write_text("CLIENT_CUSTOM_SECRET=keep_me_safe\n", encoding="utf-8")

        # Run scaffolder without force
        scaffold_project(
            name="Augmented Client SaaS",
            target_dir=target_dir,
            template="monorepo-saas",
            admin_email="admin@example.com",
            force=False
        )

        # Assert existing client files are 100% PRESERVED
        assert client_code.exists(), "Custom client file was deleted!"
        assert client_code.read_text(encoding="utf-8") == "# Client Intellectual Property - Do Not Delete"
        assert existing_agents_rule.exists(), "Existing .agents custom rule was deleted!"
        assert pre_existing_env.read_text(encoding="utf-8") == "CLIENT_CUSTOM_SECRET=keep_me_safe\n"

        # Assert template files were also merged in
        assert (target_dir / "turbo.json").exists()
        assert (target_dir / ".agents" / "mcp_config.json").exists()

def test_scaffold_force_with_backup():
    """Tests that force overwriting creates an automatic backup in .pipeline_backup."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target_dir = Path(tmp_dir) / "client-project"
        target_dir.mkdir(parents=True)

        # Existing turbo.json with custom client content
        custom_turbo = target_dir / "turbo.json"
        custom_turbo.write_text('{"client_custom": true}', encoding="utf-8")

        # Run scaffolder with force=True
        scaffold_project(
            name="Force Augmented SaaS",
            target_dir=target_dir,
            template="monorepo-saas",
            admin_email="admin@example.com",
            force=True
        )

        # Check that .pipeline_backup directory was created with the original file
        backup_root = target_dir / ".pipeline_backup"
        assert backup_root.exists(), "Backup directory was not created!"
        backup_turbos = list(backup_root.rglob("turbo.json"))
        assert len(backup_turbos) >= 1, "Original file was not backed up!"
        assert backup_turbos[0].read_text(encoding="utf-8") == '{"client_custom": true}'

def test_scaffold_dry_run_creates_no_files():
    """Tests that --dry-run previews actions without writing any files to disk."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target_dir = Path(tmp_dir) / "dry-run-target"

        scaffold_project(
            name="Dry Run App",
            target_dir=target_dir,
            template="monorepo-saas",
            dry_run=True
        )

        # Target directory should not have any files written
        if target_dir.exists():
            assert len(list(target_dir.iterdir())) == 0, "Dry run created files on disk!"
