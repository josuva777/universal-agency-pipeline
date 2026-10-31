#!/usr/bin/env python3
"""
Pre-Commit Secret Scanner & Credential Static Pattern Filter.
Performs fast static regex scanning for known API keys, tokens, and private certificates before staging.

Note: Static pattern scanning is an essential pre-commit heuristic filter, but not an absolute
guarantee against every possible secret format. For comprehensive historical audits,
pair with dedicated repository scanners (such as TruffleHog or Gitleaks).
"""

import os
import sys
import re
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows safely
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

# High-entropy & known credential signatures
SECRET_PATTERNS = [
    # AI / LLM Providers (specific prefixes first)
    (r'sk-ant-(?:api03-)?[A-Za-z0-9_-]{32,}', "Anthropic API Key"),
    (r'sk-(?!ant-)(?:proj-)?[A-Za-z0-9_-]{32,}', "OpenAI API Key"),
    (r'AIza[0-9A-Za-z-_]{35}', "Google API Key"),
    (r'hf_[A-Za-z0-9]{34,}', "HuggingFace Access Token"),

    # Cloud & VCS Credentials
    (r'ghp_[A-Za-z0-9]{36}', "GitHub Personal Access Token"),
    (r'gho_[A-Za-z0-9]{36}', "GitHub OAuth Token"),
    (r'github_pat_[A-Za-z0-9_]{82}', "GitHub Fine-Grained Personal Access Token"),
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID"),
    (r'(?i)aws_(?:secret_access_key|session_token)\s*[:=]\s*[\'"][A-Za-z0-9/+=]{40}[\'"]', "AWS Secret Key / Session Token"),
    (r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', "Private Key Certificate"),

    # Payment & SaaS Tokens
    (r'(?:sk|rk)_(?:live|test)_[0-9a-zA-Z]{24,}', "Stripe Secret / Restricted Key"),
    (r'xox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*', "Slack Bot / User Token"),
    (r'eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}', "JSON Web Token (JWT)"),

    # Databases
    (r'postgres(?:ql)?://[a-zA-Z0-9_-]+:[^@\s]+@[a-zA-Z0-9.-]+:\d+/[a-zA-Z0-9_-]+', "PostgreSQL Connection String with Password"),
    (r'mongodb(?:\+srv)?://[a-zA-Z0-9_-]+:[^@\s]+@', "MongoDB Connection String with Password"),

    # Generic High-Risk Assignment (evaluated only if specific patterns do not overlap)
    (r'(?i)(?:api_key|secret_key|private_key|auth_token)\s*[:=]\s*[\'"][A-Za-z0-9\-_]{20,}[\'"]', "Generic High-Entropy Credential Assignment"),
]

# Build artifacts, vendor directories, bytecode, and version control to ignore
IGNORED_PATTERNS = [
    r'\.git[\\/]',
    r'node_modules[\\/]',
    r'\.venv[\\/]',
    r'dist[\\/]',
    r'\.next[\\/]',
    r'__pycache__[\\/]',
    r'\.pyc$',
    r'\.env\.example$',
    r'package-lock\.json$',
]

def is_ignored(file_path: str) -> bool:
    for pat in IGNORED_PATTERNS:
        if re.search(pat, file_path, re.IGNORECASE):
            return True
    return False

def is_placeholder_match(match_text: str) -> bool:
    """Verifies whether the matched token itself is a documented placeholder."""
    lower = match_text.lower()
    return (
        "your_" in lower
        or "example" in lower
        or "placeholder" in lower
        or "dummy" in lower
        or "<token>" in lower
        or "generate-a-secure" in lower
        or "pk_test_" in lower
        or "whsec_placeholder" in lower
        or "sk_test_placeholder" in lower
    )

def scan_file(file_path: Path) -> list[dict]:
    findings = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    for line_num, line in enumerate(content.splitlines(), start=1):
        matched_spans = []
        for regex, desc in SECRET_PATTERNS:
            matches = re.finditer(regex, line)
            for m in matches:
                span = (m.start(), m.end())
                # If this span overlaps with an already-matched more specific pattern, skip it
                if any(span[0] < s[1] and span[1] > s[0] for s in matched_spans):
                    continue

                matched_val = m.group(0)
                # Check the matched token itself, not the entire line
                if is_placeholder_match(matched_val):
                    continue

                matched_spans.append(span)
                masked = matched_val[:4] + "*" * (len(matched_val) - 8) + matched_val[-4:] if len(matched_val) > 8 else "***"
                findings.append({
                    "file": str(file_path),
                    "line": line_num,
                    "type": desc,
                    "masked": masked
                })
    return findings

def get_staged_or_all_files(target_dir: str = ".") -> list[Path]:
    """Retrieves git staged files if in a git repo, otherwise scans text files in target_dir."""
    files = []
    try:
        output = subprocess.check_output(
            ["git", "diff", "--name-only", "--cached"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        if output:
            for f in output.splitlines():
                p = Path(f.strip())
                if p.exists() and p.is_file() and not is_ignored(str(p)):
                    files.append(p)
            return files
    except Exception:
        pass

    for root, dirs, filenames in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not is_ignored(d)]
        for fn in filenames:
            p = Path(root) / fn
            if not is_ignored(str(p)):
                files.append(p)
    return files

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    files_to_scan = get_staged_or_all_files(target)

    all_findings = []
    for f in files_to_scan:
        if f.name == ".env" or f.name.endswith(".env.local"):
            all_findings.append({
                "file": str(f),
                "line": 1,
                "type": "Critical: Unignored .env secret file staged for commit!",
                "masked": f.name
            })
            continue

        findings = scan_file(f)
        all_findings.extend(findings)

    if all_findings:
        print("\n[SECURITY AUDIT GATEKEEPER] Potential Secrets or Credentials Detected!")
        print("Commit or deployment blocked to prevent credential leakage:\n")
        for finding in all_findings:
            print(f"  * {finding['file']}:{finding['line']} - [{finding['type']}] -> {finding['masked']}")
        print("\nPlease remove real API keys, place them in .env (ignored), and use environment variables.")
        sys.exit(1)
    else:
        print("[Security Gatekeeper] Clean: 0 sensitive credentials detected by static scan.")
        sys.exit(0)

if __name__ == "__main__":
    main()
