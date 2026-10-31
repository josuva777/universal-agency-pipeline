"""Automated Unit Tests for Pre-Commit Secret Scanner."""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / ".agents"))

import secret_scan

def test_secret_scanner_detects_openai_key(tmp_path):
    leaky_file = tmp_path / "leaky_openai.py"
    fake_token = "sk-" + "proj-" + ("A" * 32)
    leaky_file.write_text(f"api_key = '{fake_token}'")
    findings = secret_scan.scan_file(leaky_file)
    assert len(findings) == 1
    assert findings[0]["type"] == "OpenAI API Key"
    assert "***" in findings[0]["masked"]

def test_secret_scanner_detects_anthropic_key(tmp_path):
    leaky_file = tmp_path / "leaky_anthropic.py"
    fake_token = "sk-ant-api03-" + ("a" * 80)
    leaky_file.write_text(f"anthropic_key = '{fake_token}'")
    findings = secret_scan.scan_file(leaky_file)
    assert len(findings) == 1
    assert "Anthropic" in findings[0]["type"]

def test_secret_scanner_detects_stripe_key(tmp_path):
    leaky_file = tmp_path / "leaky_stripe.py"
    fake_token = "sk_live_" + ("1234567890abcdef" * 2)
    leaky_file.write_text(f"stripe_key = '{fake_token}'")
    findings = secret_scan.scan_file(leaky_file)
    assert len(findings) == 1
    assert "Stripe" in findings[0]["type"]

def test_secret_scanner_detects_slack_token(tmp_path):
    leaky_file = tmp_path / "leaky_slack.py"
    # Construct dynamically to avoid static scan trigger in test file
    fake_token = "xox" + "b-123456789012-1234567890123-abcdef123456"
    leaky_file.write_text(f"slack_token = '{fake_token}'")
    findings = secret_scan.scan_file(leaky_file)
    assert len(findings) == 1
    assert "Slack" in findings[0]["type"]

def test_secret_scanner_detects_huggingface_token(tmp_path):
    leaky_file = tmp_path / "leaky_hf.py"
    fake_token = "hf_" + ("a" * 34)
    leaky_file.write_text(f"hf_token = '{fake_token}'")
    findings = secret_scan.scan_file(leaky_file)
    assert len(findings) == 1
    assert "HuggingFace" in findings[0]["type"]

def test_secret_scanner_detects_jwt_token(tmp_path):
    leaky_file = tmp_path / "leaky_jwt.py"
    # Construct dynamically to avoid static scan trigger in test file
    fake_token = "ey" + "JhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." + "ey" + "JzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    leaky_file.write_text(f"token = '{fake_token}'")
    findings = secret_scan.scan_file(leaky_file)
    assert len(findings) == 1
    assert "JSON Web Token (JWT)" in findings[0]["type"]

def test_secret_scanner_detects_github_pat(tmp_path):
    leaky_file = tmp_path / "token.txt"
    fake_token = "ghp_" + ("1" * 36)
    leaky_file.write_text(f"token = '{fake_token}'")
    findings = secret_scan.scan_file(leaky_file)
    assert len(findings) == 1
    assert findings[0]["type"] == "GitHub Personal Access Token"

def test_secret_scanner_passes_on_placeholders(tmp_path):
    placeholder_file = tmp_path / "sample_env.txt"
    placeholder_file.write_text(
        "OPENAI_API_KEY=your_openai_api_key_here\n"
        "ANTHROPIC_API_KEY=your_anthropic_api_key_here\n"
        "STRIPE_SECRET_KEY=sk_test_placeholder\n"
        "GITHUB_TOKEN=ghp_your_github_token_here\n"
    )
    findings = secret_scan.scan_file(placeholder_file)
    assert len(findings) == 0, f"False positives on placeholders: {findings}"

def test_secret_scanner_passes_on_clean_code(tmp_path):
    clean_file = tmp_path / "clean_code.py"
    clean_file.write_text("OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')\nprint('Safe!')")
    findings = secret_scan.scan_file(clean_file)
    assert len(findings) == 0
