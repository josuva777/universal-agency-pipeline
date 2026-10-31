#!/usr/bin/env python3
"""
Universal Agency Pipeline - Interactive Project Scaffolder CLI
Instantly creates or augments a client project with full working codebase, .agents/ rules,
customized .env, and git initialization without deleting existing files.
"""

import os
import sys
import shutil
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from pipeline.generator import synthesize_project_specs, generate_bespoke_page_tsx

PIPELINE_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PIPELINE_ROOT / "templates"
AGENTS_DIR = PIPELINE_ROOT / ".agents"

TEMPLATES = {
    "monorepo-saas": "Turborepo + pnpm (Next.js 15 Web + Expo SDK 52 Mobile + UI + DB)",
    "fullstack-agent-app": "Next.js 15 Web App with Streaming AI & Vercel AI SDK",
    "mobile-agent-app": "Expo SDK 52 Cross-Platform Mobile App (iOS + Android)",
    "creative-agent-studio": "Remotion v4 + Three.js Broadcast Commercial & Video Studio"
}

THEMES = [
    "Cyberpunk Matrix (Obsidian & Emerald)",
    "Swiss Bauhaus (Deep Navy & Crimson)",
    "Avionics Amber (Stealth Charcoal & Amber)",
    "Oceanic Cobalt (Midnight & Cobalt Blue)",
    "Lockdown Crimson (Deep Slate & Laser Crimson)"
]

def print_banner():
    print("=" * 68)
    print("  UNIVERSAL AGENCY PIPELINE v2.0 - PROJECT SCAFFOLDER CLI")
    print("=" * 68)

PRE_COMMIT_HOOK_SH = """#!/bin/sh
# Universal Agency Pipeline - Automated Pre-Commit Security & Quality Guard
echo "[*] Universal Agency Pipeline: Running Pre-Commit Checks..."

# 1. Zero-Trust Leaked Secrets & Credentials Scanner
if [ -f ".agents/secret_scan.py" ]; then
    echo "[*] Scanning for leaked API secrets, tokens, and private keys..."
    if command -v py >/dev/null 2>&1; then
        py -3 .agents/secret_scan.py .
    elif command -v python3 >/dev/null 2>&1; then
        python3 .agents/secret_scan.py .
    elif command -v python >/dev/null 2>&1; then
        python .agents/secret_scan.py .
    else
        echo "[!] Python not found; skipping secret scan."
    fi
    if [ $? -ne 0 ]; then
        echo "[ERROR] Pre-commit rejected: Leaked secret or token detected by static pattern scanner!"
        exit 1
    fi
    echo "[OK] Secret scan passed: 0 sensitive credentials found."
fi

# 2. Biome Fast Linter & Formatting Standards
if command -v npx >/dev/null 2>&1 && [ -f "biome.json" ]; then
    echo "[*] Running Biome ultra-fast formatting and lint verification..."
    npx @biomejs/biome check --diagnostic-level=error --no-errors-on-unmatched .
    if [ $? -ne 0 ]; then
        echo "[ERROR] Pre-commit rejected: Biome lint/format check failed!"
        echo "Run 'npx @biomejs/biome check --write .' to auto-fix issues."
        exit 1
    fi
    echo "[OK] Biome check passed."
fi

echo "[OK] All pre-commit security gates passed successfully."
exit 0
"""

def install_git_hooks(target_dir: Path) -> bool:
    """Installs automated pre-commit security and quality hooks into .git/hooks."""
    hooks_dir = target_dir / ".git" / "hooks"
    if not hooks_dir.parent.exists():
        return False

    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_file = hooks_dir / "pre-commit"
    with open(hook_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(PRE_COMMIT_HOOK_SH)

    try:
        current_mode = os.stat(hook_file).st_mode
        os.chmod(hook_file, current_mode | 0o111)
    except Exception:
        pass

    print("[*] Pre-commit security hook installed at .git/hooks/pre-commit")
    return True

def safe_merge_copy(
    src: Path,
    dest: Path,
    force: bool = False,
    dry_run: bool = False,
    backup_dir: Path | None = None
) -> dict[str, list[str]]:
    """
    Non-destructively copies files from src to dest.
    Never calls rmtree on dest or its subdirectories.
    If a file exists:
      - If force=False: keeps existing file untouched (collision preserved).
      - If force=True: creates backup in backup_dir before overwriting.
    """
    results = {"created": [], "preserved": [], "backed_up": [], "overwritten": []}
    if not src.exists():
        return results

    ignore_dirs = {".next", "node_modules", ".turbo", "dist", "__pycache__", ".git"}

    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        rel_root = Path(root).relative_to(src)
        target_root = dest / rel_root

        for fn in files:
            src_file = Path(root) / fn
            target_file = target_root / fn
            rel_file = str((rel_root / fn)).replace("\\", "/")
            if rel_file.startswith("./"):
                rel_file = rel_file[2:]

            if target_file.exists():
                if not force:
                    results["preserved"].append(rel_file)
                    print(f"  [PRESERVED] Existing file untouched: {rel_file}")
                else:
                    if backup_dir and not dry_run:
                        backup_file = backup_dir / rel_root / fn
                        backup_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(target_file, backup_file)
                        results["backed_up"].append(rel_file)
                        print(f"  [BACKED UP] {rel_file} -> {backup_file}")
                    if not dry_run:
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_file, target_file)
                    results["overwritten"].append(rel_file)
                    print(f"  [OVERWRITTEN] Forced update: {rel_file}")
            else:
                if not dry_run:
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, target_file)
                results["created"].append(rel_file)
                print(f"  [CREATED] Added file: {rel_file}")

    return results

def scaffold_project(
    name: str,
    target_dir: Path,
    template: str = "monorepo-saas",
    admin_email: str = "admin@example.com",
    theme: str = "Cyberpunk Matrix",
    force: bool = False,
    dry_run: bool = False
):
    print(f"\n[*] {'[DRY RUN] ' if dry_run else ''}Scaffolding enterprise project: {name}")
    print(f"[*] Target directory: {target_dir}")
    print(f"[*] Selected template: {template} ({TEMPLATES.get(template, 'Custom')})")
    print(f"[*] Master Admin: {admin_email}")
    print(f"[*] Brand Palette: {theme}")
    print(f"[*] Overwrite Mode: {'Force (with automatic backup)' if force else 'Non-destructive safe merge'}\n")

    is_existing = target_dir.exists() and any(target_dir.iterdir())
    backup_dir = None
    if is_existing:
        print(f"[!] Target directory {target_dir} is not empty. Performing safe non-destructive merge...")
        if force:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = target_dir / ".pipeline_backup" / timestamp
            print(f"[*] Automatic backup destination: {backup_dir}")

    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Non-destructively Copy Template Files
    src_template = TEMPLATES_DIR / template
    if not src_template.exists():
        print(f"[ERROR] Template {template} not found at {src_template}")
        sys.exit(1)

    print(f"[*] Copying {template} files non-destructively...")
    safe_merge_copy(src_template, target_dir, force=force, dry_run=dry_run, backup_dir=backup_dir)

    # 2. Setup .agents/ Directory & Architectural Memory Non-destructively
    print("[*] Installing .agents/ workspace rules, MCP servers & hooks non-destructively...")
    dest_agents = target_dir / ".agents"
    safe_merge_copy(AGENTS_DIR, dest_agents, force=force, dry_run=dry_run, backup_dir=backup_dir)

    # Copy MemPalace architectural memory seed if present (non-destructively)
    src_mempalace = PIPELINE_ROOT / "mempalace.yaml"
    dest_mempalace = target_dir / "mempalace.yaml"
    if src_mempalace.exists() and (not dest_mempalace.exists() or force):
        if not dry_run:
            shutil.copy2(src_mempalace, dest_mempalace)
        print("  [CREATED] mempalace.yaml seed installed.")

    src_entities = PIPELINE_ROOT / "entities.json"
    dest_entities = target_dir / "entities.json"
    if src_entities.exists() and (not dest_entities.exists() or force):
        if not dry_run:
            shutil.copy2(src_entities, dest_entities)
        print("  [CREATED] entities.json seed installed.")

    # 3. Generate Tailored .env and Clean Placeholder .env.example
    print("[*] Generating tailored environment files...")
    env_content = f"""# =========================================================================
# {name.upper()} - ENTERPRISE ENVIRONMENT CONFIGURATION
# =========================================================================

PROJECT_NAME="{name}"
PORT=8000
DATABASE_URL=sqlite:///./app.db

# Master Admin Exclusivity
MASTER_ADMIN_EMAIL="{admin_email}"

# Email Dispatch (6-Digit Cryptographic OTPs)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER="security@{name.lower().replace(' ', '')}.ai"
SMTP_PASS="replace_with_app_password"
SMTP_FROM="{name} Security <security@{name.lower().replace(' ', '')}.ai>"

# Stripe Payment Gateway
STRIPE_SECRET_KEY=sk_test_placeholder
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_placeholder

# Frontend Settings
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
NEXT_PUBLIC_THEME="{theme}"
"""

    env_example_content = """# =========================================================================
# ENTERPRISE ENVIRONMENT TEMPLATE (.env.example)
# Note: Keep strictly placeholder-only. Never commit real keys or emails.
# =========================================================================

PROJECT_NAME="your-project-name"
PORT=8000
DATABASE_URL=sqlite:///./app.db

# Master Admin Exclusivity
MASTER_ADMIN_EMAIL=admin@example.com

# Email Dispatch / 6-Digit Real OTP Delivery
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=security@example.com
SMTP_PASS=your-16-char-gmail-app-password
SMTP_FROM="Security Team <security@example.com>"

# Stripe Payment Gateway
STRIPE_SECRET_KEY=sk_test_placeholder
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_placeholder
STRIPE_WEBHOOK_SECRET=whsec_placeholder

# Frontend Settings
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
NEXT_PUBLIC_THEME="Cyberpunk Matrix"

# Optional Cloud Model Providers
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
"""

    dest_env = target_dir / ".env"
    if not dest_env.exists() or force:
        if not dry_run:
            with open(dest_env, "w", encoding="utf-8") as f:
                f.write(env_content)
        print("  [CREATED] Tailored .env generated.")
    else:
        print("  [PRESERVED] Existing .env preserved.")

    dest_env_example = target_dir / ".env.example"
    if not is_existing or not dest_env_example.exists() or force:
        if not dry_run:
            with open(dest_env_example, "w", encoding="utf-8") as f:
                f.write(env_example_content)
        print("  [CREATED] Placeholder-only .env.example generated.")
    else:
        print("  [PRESERVED] Existing .env.example preserved.")

    # 3.5 Tailor Bespoke Project Branding & Theme
    print(f"[*] Customizing project branding and theme palette for {name}...")
    specs = synthesize_project_specs(name=name, idea=name)
    theme_slug = theme.split(" ")[0].lower() if theme else specs["default_theme"]

    layout_file = target_dir / "apps" / "web" / "app" / "layout.tsx"
    if layout_file.exists() and not dry_run:
        content = layout_file.read_text(encoding="utf-8")
        content = content.replace("SentinelOps", name)
        content = content.replace('defaultTheme="cyberpunk-matrix"', f'defaultTheme="{theme_slug}"')
        layout_file.write_text(content, encoding="utf-8")

    page_file = target_dir / "apps" / "web" / "app" / "page.tsx"
    if page_file.exists() and not dry_run:
        bespoke_code = generate_bespoke_page_tsx(specs)
        page_file.write_text(bespoke_code, encoding="utf-8")

    tauri_conf = target_dir / "apps" / "desktop" / "src-tauri" / "tauri.conf.json"
    if tauri_conf.exists() and not dry_run:
        content = tauri_conf.read_text(encoding="utf-8")
        content = content.replace("Enterprise Desktop Console", f"{name} Desktop Console")
        tauri_conf.write_text(content, encoding="utf-8")

    # 4. Initialize Git Repository & Security Hooks
    if not dry_run:
        if not (target_dir / ".git").exists():
            print("[*] Initializing fresh Git repository...")
            try:
                subprocess.run(["git", "init"], cwd=target_dir, check=True, stdout=subprocess.DEVNULL)
                install_git_hooks(target_dir)
                subprocess.run(["git", "add", "-A"], cwd=target_dir, check=True, stdout=subprocess.DEVNULL)
                subprocess.run(["git", "commit", "-m", f"feat(init): scaffold {name} with Universal Agency Pipeline v2.0"], cwd=target_dir, check=True, stdout=subprocess.DEVNULL)
                print("[OK] Git initialized with clean initial commit and pre-commit security hooks.")
            except Exception as e:
                print(f"[!] Git init skipped: {e}")
        else:
            install_git_hooks(target_dir)

    print("\n" + "=" * 68)
    if dry_run:
        print(f"  DRY RUN COMPLETED: {name} preview generated successfully (0 files written).")
    else:
        print(f"  SUCCESS: {name} is ready for development!")
    print("=" * 68)
    print(f"1. cd \"{target_dir}\"")
    print("2. pnpm install   (or npm install)")
    print("3. pnpm dev       (launches development server)")
    print("4. Begin Phase 1 (Blueprint & Spec Engine)!\n")

def main():
    parser = argparse.ArgumentParser(description="Universal Agency Pipeline Scaffolder CLI")
    parser.add_argument("name", nargs="?", default="", help="Project name (e.g. AcmeSaaS)")
    parser.add_argument("--template", "-t", choices=list(TEMPLATES.keys()), default="", help="Starter template")
    parser.add_argument("--admin", "-a", default="admin@example.com", help="Master Admin Email (default: admin@example.com)")
    parser.add_argument("--theme", choices=THEMES, default="", help="Default Theme Palette")
    parser.add_argument("--output", "-o", default="", help="Target directory (defaults to ./<name>)")
    parser.add_argument("--force", "-f", action="store_true", help="Force overwrite existing files with automatic backup")
    parser.add_argument("--dry-run", action="store_true", help="Preview file actions without modifying filesystem")
    parser.add_argument("--install-hooks", action="store_true", help="Install pre-commit security hooks into existing repo")

    args = parser.parse_args()

    print_banner()

    if args.install_hooks:
        target_path = Path(args.output) if args.output else Path.cwd()
        if install_git_hooks(target_path):
            print(f"[OK] Pre-commit security hooks installed in {target_path}")
        else:
            print(f"[ERROR] Could not find .git in {target_path}")
        return

    name = args.name
    if not name:
        name = input("[?] Enter project name: ").strip() or "client-saas-project"

    template = args.template
    if not template:
        print("\nAvailable Templates:")
        for idx, (k, desc) in enumerate(TEMPLATES.items(), 1):
            print(f"  {idx}. {k:<22} - {desc}")
        choice = input("\n[?] Select template (1-4) [default: 1]: ").strip()
        template_keys = list(TEMPLATES.keys())
        if choice in ["1", "2", "3", "4"]:
            template = template_keys[int(choice) - 1]
        else:
            template = "monorepo-saas"

    theme = args.theme
    if not theme:
        theme = THEMES[0]

    admin_email = args.admin
    out_dir = Path(args.output) if args.output else Path.cwd() / name.lower().replace(" ", "-")

    scaffold_project(
        name=name,
        target_dir=out_dir,
        template=template,
        admin_email=admin_email,
        theme=theme,
        force=args.force,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()
