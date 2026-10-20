"""Automated Unit Tests for System Scanner Hardware Auditor."""
import sys
from pathlib import Path

# Add skills/agent-builder to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "skills" / "agent-builder"))

from system_scanner import SystemScanner, HardwareProfile

def test_hardware_scan_returns_valid_profile():
    profile = SystemScanner.scan(str(REPO_ROOT))
    assert isinstance(profile, HardwareProfile)
    assert profile.physical_cores >= 1
    assert profile.logical_cores >= 1
    assert profile.total_ram_gb > 0
    assert profile.available_ram_gb >= 0
    assert profile.free_disk_gb > 0
    assert profile.hardware_tier in {"tier1_light", "tier2_mid", "tier3_heavy"}
    assert len(profile.recommended_local_model) > 0
    assert len(profile.recommended_cloud_provider) > 0

def test_scanner_display_report_does_not_crash():
    profile = SystemScanner.display_report(str(REPO_ROOT))
    assert profile is not None
