#!/usr/bin/env python3
"""
Universal Agency Pipeline - Interactive Project Scaffolder CLI
Instantly creates a new client project with full working codebase, .agents/ rules,
customized .env, and git initialization in 5 seconds.
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path

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

def scaffold_project(
    name: str,
    target_dir: Path,
    template: str = "monorepo-saas",
    admin_email: str = "josuva732006@gmail.com",
    theme: str = "Cyberpunk Matrix"
):
    print(f"\n[*] Scaffolding new enterprise project: {name}")
    print(f"[*] Target directory: {target_dir}")
    print(f"[*] Selected template: {template} ({TEMPLATES.get(template, 'Custom')})")
    print(f"[*] Master Admin: {admin_email}")
    print(f"[*] Brand Palette: {theme}\n")

    if target_dir.exists() and any(target_dir.iterdir()):
        print(f"[!] Warning: Directory {target_dir} is not empty. Merging files...")

    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy Template Files
    src_template = TEMPLATES_DIR / template
    if not src_template.exists():
        print(f"[ERROR] Template {template} not found at {src_template}")
        sys.exit(1)

    print(f"[*] Copying {template} starter codebase...")
    for item in src_template.iterdir():
        dest = target_dir / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest, ignore=shutil.ignore_patterns(".next", "node_modules", ".turbo", "dist"))
        else:
            shutil.copy2(item, dest)

    # 2. Setup .agents/ Directory & Architectural Memory
    print("[*] Installing .agents/ workspace rules, MCP servers & hooks...")
    dest_agents = target_dir / ".agents"
    if dest_agents.exists():
        shutil.rmtree(dest_agents)
    shutil.copytree(AGENTS_DIR, dest_agents)

    # Copy MemPalace architectural memory seed if present
    src_mempalace = PIPELINE_ROOT / "mempalace.yaml"
    if src_mempalace.exists():
        shutil.copy2(src_mempalace, target_dir / "mempalace.yaml")
    src_entities = PIPELINE_ROOT / "entities.json"
    if src_entities.exists():
        shutil.copy2(src_entities, target_dir / "entities.json")

    # 3. Generate Tailored .env File
    print("[*] Generating tailored .env with master admin configuration...")
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
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...

# Frontend Settings
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
NEXT_PUBLIC_THEME="{theme}"
"""
    with open(target_dir / ".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    with open(target_dir / ".env.example", "w", encoding="utf-8") as f:
        f.write(env_content)

    # 4. Initialize Git Repository
    if not (target_dir / ".git").exists():
        print("[*] Initializing fresh Git repository...")
        try:
            subprocess.run(["git", "init"], cwd=target_dir, check=True, stdout=subprocess.DEVNULL)
            subprocess.run(["git", "add", "-A"], cwd=target_dir, check=True, stdout=subprocess.DEVNULL)
            subprocess.run(["git", "commit", "-m", f"feat(init): scaffold {name} with Universal Agency Pipeline v2.0"], cwd=target_dir, check=True, stdout=subprocess.DEVNULL)
            print("✓ Git initialized with clean initial commit.")
        except Exception as e:
            print(f"[!] Git init skipped: {e}")

    print("\n" + "=" * 68)
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
    parser.add_argument("--admin", "-a", default="josuva732006@gmail.com", help="Master Admin Email")
    parser.add_argument("--theme", choices=THEMES, default="", help="Default Theme Palette")
    parser.add_argument("--output", "-o", default="", help="Target directory (defaults to ./<name>)")

    args = parser.parse_args()

    print_banner()

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
        theme=theme
    )

if __name__ == "__main__":
    main()
