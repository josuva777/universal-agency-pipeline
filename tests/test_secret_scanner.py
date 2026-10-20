"""Automated Unit Tests for Pre-Commit Secret Scanner."""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / ".agents"))

import secret_scan

def test_secret_scanner_detects_openai_key(tmp_path):
    leaky_file = tmp_path / "leaky_code.py"
    # Construct dynamically to avoid static scanner false positives in test source
    fake_token = "sk-" + "proj-" + ("A" * 32)
    leaky_file.write_text(f"api_key = '{fake_token}'")
    findings = secret_scan.scan_file(leaky_file)
    assert len(findings) == 1
    assert findings[0]["type"] == "OpenAI API Key"
    assert "***" in findings[0]["masked"]

def test_secret_scanner_detects_github_pat(tmp_path):
    leaky_file = tmp_path / "token.txt"
    fake_token = "ghp_" + ("1" * 36)
    leaky_file.write_text(f"token = '{fake_token}'")
    findings = secret_scan.scan_file(leaky_file)
    assert len(findings) == 1
    assert findings[0]["type"] == "GitHub Personal Access Token"

def test_secret_scanner_passes_on_clean_code(tmp_path):
    clean_file = tmp_path / "clean_code.py"
    clean_file.write_text("OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')\nprint('Safe!')")
    findings = secret_scan.scan_file(clean_file)
    assert len(findings) == 0
