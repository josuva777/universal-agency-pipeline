"""Automated Unit Tests for Pre-Commit Secret Scanner."""
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / ".agents"))

import secret_scan

def test_secret_scanner_detects_openai_key(tmp_path):
    leaky_file = tmp_path / "leaky_code.py"
    leaky_file.write_text("api_key = 'sk-proj-abc1234567890123456789012345678901234567890'")
    findings = secret_scan.scan_file(leaky_file)
    assert len(findings) == 1
    assert findings[0]["type"] == "OpenAI API Key"
    assert "***" in findings[0]["masked"]

def test_secret_scanner_detects_github_pat(tmp_path):
    leaky_file = tmp_path / "token.txt"
    leaky_file.write_text("ghp_123456789012345678901234567890123456")
    findings = secret_scan.scan_file(leaky_file)
    assert len(findings) == 1
    assert findings[0]["type"] == "GitHub Personal Access Token"

def test_secret_scanner_passes_on_clean_code(tmp_path):
    clean_file = tmp_path / "clean_code.py"
    clean_file.write_text("OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')\nprint('Safe!')")
    findings = secret_scan.scan_file(clean_file)
    assert len(findings) == 0
